from google.colab import auth as colab_auth
from google.auth import default as google_auth_default

import gspread
from gspread.utils import rowcol_to_a1

import pandas as pd

import random
import string
import time

class GSheetMLScheduler():
  def __init__(self, gsheet_file_url, sheet_index=0, comma_number_format=False):
    """
    gsheet_file_url (str): The URL of the Google Sheets file
    sheet_index (int, optional): In case you don't want to use the default "Sheet1" tab (default is 0)
    comma_number_format (bool, optional): Some languages use decimal numbers with a comma, for example "-2,0" or "1,5E-3" (default is False, indicating period as the default decimal separator)
    """
    self.gsheet_file_url = gsheet_file_url
    self.worker_name = GSheetMLScheduler.generate_short_uuid()
    self.comma_number_format = comma_number_format

    self.all_sheets = self.login_and_get_sheets()
    self.sheet_index = sheet_index
    self.sheet = self.all_sheets.worksheets()[self.sheet_index]
    self.download_data()

    self.currently_running_run_id = None
    print(f'Scheduler connected to GSheet, its name is worker <{self.worker_name}>')

  @staticmethod
  def convert_str_to_bool_int_float_str(str_point_format):
    """
    Convert raw data str to bool/int/float/str. Hex isn't handled, nor other exotic types
    The number decimal separator must be a point
    """
    if str_point_format == '':
      return str_point_format

    str_lower_case = str_point_format.lower()
    if str_lower_case == 'true':
      return True
    if str_lower_case == 'false':
      return False
    
    if str_point_format.isdecimal(): # Positive integer
      try:
        return int(str_point_format)
      except:
        return str_point_format

    if str_point_format[0] == '-' and str_point_format[1:].isdecimal(): # Negative integer
      try:
        return int(str_point_format)
      except:
        return str_point_format

    try:
      return float(str_point_format) # We trust python's float convertion
    except:
      return str_point_format

  @staticmethod
  def generate_short_uuid(length=6):
    """
    Unique identifier, used to name workers (aka each Colab parallel session)
    """
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

  @staticmethod
  def complete_missing_config_params(gsheet_config, hardcoded_default_config):
    """
    Completes gsheet_config with hardcoded default key/values
    """
    full_config = dict(hardcoded_default_config)
    for gsheet_key in gsheet_config:
      full_config[gsheet_key] = gsheet_config[gsheet_key]
    return full_config
  
  def login_and_get_sheets(self):
    """
    This opens a popup to give your Colab file the reading/writing rights on the GSheet file
    Access rights do not persist after you close the Colab browser tab
    Rights are only given to that specific Colab browser tab

    This uses colab.auth library
    """
    colab_auth.authenticate_user() # That line is the only part that is Colab specific, I was too lazy to search how to make it work on other Python environments
    credentials, _ = google_auth_default()
    gclient = gspread.authorize(credentials)

    all_sheets = gclient.open_by_url(self.gsheet_file_url)
    return all_sheets

  def download_data(self):
    """
    This refreshes the data and converts the raw gspread data into an easier to manage format
    This also converts cell raw strings to comma format if required, then as int/float/str
    """
    data = self.sheet.get_all_values()

    dataframe = pd.DataFrame(data) # Panda is used for easier handling of 2d arrays with dataframe[i,j]
    size = (len(data), len(data[0]))
    keys = data[0]

    config_keys = list(keys)
    config_keys.remove("run_name")
    config_keys.remove("status")
    config_keys.remove("worker_name")

    key_ids = {}
    for i in range(size[1]):
      key_ids[keys[i]] = i
    config_defaults = {}
    for config_key in config_keys:
      config_defaults[config_key] = data[1][key_ids[config_key]]

    values = {}
    for key in keys:
      values[key] = list(dataframe.iloc[2:,key_ids[key]])

    # Here we handle the languages with comma decimal separators
    # There is no fancy way to check if it's a comma number and not a text with a comma
    # In all values of config_key, commas are replaced by points
    for config_key in config_keys:
      # Part 1: The default values
      str_value = config_defaults[config_key]
      if self.comma_number_format:
        point_value = str_value.replace(",", ".")
      else:
        point_value = str_value
      converted_type_value = GSheetMLScheduler.convert_str_to_bool_int_float_str(point_value)
      config_defaults[config_key] = converted_type_value

      # Part 2: The config values of all lines except the first 2 (first is key names, second is defaults)
      for i in range(len(values["status"])):
        str_value = values[config_key][i]

        if self.comma_number_format:
          point_value = str_value.replace(",", ".")
        else:
          point_value = str_value
        converted_type_value = GSheetMLScheduler.convert_str_to_bool_int_float_str(point_value)
        values[config_key][i] = converted_type_value

    self.size = size
    self.nb_runs = size[0]-2 # Not used in this code, but useful for users to iterate over get_run_config(run_id)
    self.keys = keys # All colmun names
    self.config_keys = config_keys # All column names except run_name/status/worker_name
    self.key_ids = key_ids # Key to column number conversion
    self.config_defaults = config_defaults # config_defaults[config_key] contains a list of the values of a column, with the first two lines excluded (first is key names, second is defaults)
    self.values = values # values[key] contains a list of the values of a column, with the first two lines excluded (first is key names, second is defaults)

  def get_run_config(self, run_id):
    """
    This uses the config_defaults to complete empty config cells
    """
    config = {}
    for key in self.config_keys:
      val = self.values[key][run_id]
      if val == "":
        val = self.config_defaults[key]
      config[key] = val
    return config

  def find_ready_run(self):
    """
    Searches the first cell of the "status" column with the string content "ready"
    This allows you to write things in other parts of the Google Sheet as drafts
    Write "ready" in the "status" column once you want this line to be runned

    Returns: run_id, config. In this function (unlike in find_claim_and_start_run) it returns the run_id
    """
    self.currently_running_run_id = None # In case we didn't use self.run_done()

    self.download_data()

    for i in range(len(self.values["status"])):
      if self.values["status"][i] == "ready" and self.values["worker_name"][i] == "":
        self.currently_running_config = self.get_run_config(i)
        return i, self.currently_running_config

    return None, None

  def claim_and_start_run(self, run_id):
    """
    In case you use multiple Colab sessions at the same time, there are some checks to claim a run,
    to avoid having two sessions starting the same run

    The claimer downloads the sheet and checks that the worker_name cell is empty
    The claimer writes its worker_name in the sheet and waits for 2 seconds
    Then, it downloads the sheet content a second time and if its worker_name didn't get erased by another worker, then it's safe to claim
    """
    # Part 1: Download and check that "worker_name" is empty aka no other worker claimed it
    self.download_data()
    if not(self.values["status"][run_id] == "ready"):
      print(f"Failure, run {run_id} ({self.values['run_name'][run_id]}) isn't ready to be claimed. Status: {self.values['status'][run_id]}")
      self.currently_running_config = None
      return False
    if not(self.values["worker_name"][run_id] == ""):
      print(f'Failure, run {run_id} ({self.values["run_name"][run_id]}) is already claimed by the worker <{self.values["worker_name"][run_id]}>')
      self.currently_running_config = None
      return False
    self.sheet.update_cell(1+2+run_id, 1+self.key_ids["worker_name"], self.worker_name) # Gsheet (0,0) cell is called (1,1)

    # Part 2: Wait long enough for another worker to eventually erase your claim
    time.sleep(2.0)

    # Part 3: If nobody erased your claim 
    self.download_data()
    if not(self.values["status"][run_id] == "ready"):
      print(f"Failure, run {run_id}  ({self.values['run_name'][run_id]}) isn't ready to be claimed. Status: {self.values['status'][run_id]}")
      self.currently_running_config = None
      return False
    if not(self.values["worker_name"][run_id] == self.worker_name):
      print(f'Failure, your claim on the run {run_id} ({self.values["run_name"][run_id]}) has been stolen by the worker <{self.values["worker_name"][run_id]}>')
      self.currently_running_config = None
      return False

    self.sheet.update_cell(1+2+run_id, 1+self.key_ids["status"], "running")
    #cell_name = rowcol_to_a1(1+2+run_id, 1+self.key_ids["status"])
    cell_name = rowcol_to_a1(1+2+run_id, 1) + ":" + rowcol_to_a1(1+2+run_id, self.size[1])
    self.sheet.format(cell_name, {'backgroundColor': {'red': 1.0, "green": 0.93, "blue": 0.8}})

    # Write in gray the config values copied from default
    for config_key in self.config_keys:
      if self.currently_running_config[config_key] != self.values[config_key][run_id]:
        self.sheet.update_cell(1+2+run_id, 1+self.key_ids[config_key], self.currently_running_config[config_key])
        cell_name = rowcol_to_a1(1+2+run_id, 1+self.key_ids[config_key])
        self.sheet.format(cell_name, {"textFormat": {"foregroundColor": {'red': 0.8, "green": 0.8, "blue": 0.8}}})

    self.currently_running_run_id = run_id
    return True

  def find_claim_and_start_run(self, auto_retry=3):
    """
    auto_retry is the number of retries in case another worker steals your claim
    Returns: run_name, config. In this function (unlike in find_ready_run) it returns run_name cell, not the run_id
    """
    while True:
      ready_run_id, config = self.find_ready_run()

      if ready_run_id is None:
        return None, None # No run is ready
      else:
        claim_success = self.claim_and_start_run(ready_run_id)
        if not claim_success:
          if auto_retry > 0:
            print(f"Retry finding another ready run ({auto_retry-1} retries left)")
            return self.find_claim_and_start_run(auto_retry=auto_retry-1)# Your claim got stolen, recursively retry
          else:
            print("Too much claim stealing, we abandon")
            return None, None # We abandon, as if there was no run ready
        else:
          return self.values["run_name"][ready_run_id], config # successful claim
  
  def run_done(self):
    """
    Writes "status" as "finished" and changes the line color
    """
    if self.currently_running_run_id is None:
      print("Failure, there is no active run")
      return False

    self.download_data()
    self.sheet.update_cell(1+2+self.currently_running_run_id, 1+self.key_ids["status"], "done")
    cell_name = rowcol_to_a1(1+2+self.currently_running_run_id, 1) + ":" + rowcol_to_a1(1+2+self.currently_running_run_id, self.size[1])
    self.sheet.format(cell_name, {'backgroundColor': {'red': 0.8, "green": 0.9, "blue": 1.0}})

    self.currently_running_config = None
    self.currently_running_run_id = None
    return True
  
  def update_status(self, new_status_str):
    """
    Update the status of the currently runnning run
    """
    if self.currently_running_run_id is None:
      print("Failure, no currently runnning run")
      return
    
    self.sheet.update_cell(1+2+self.currently_running_run_id, 1+self.key_ids["status"], new_status_str)

  def check_for_config_updates(self):
    """
    Downloads the sheet content and check if some config parameters changed

    Returns:
      updated_config = {config_key: config_value, ...} The most up-to-date dictionary of config metaparameters
      changed_keys = [changed_config_key, ...] The list of config keys for which the value was modified
    """
    if self.currently_running_run_id is None:
      print("Failure, no currently runnning run")
      return

    self.download_data()
    updated_config = self.get_run_config(self.currently_running_run_id)

    changed_keys = []
    for key in updated_config.keys():
      if key not in self.currently_running_config.keys():
        changed_keys.append(key)
      elif updated_config[key] != self.currently_running_config[key]:
        changed_keys.append(key)
    for key in changed_keys:
      cell_name = rowcol_to_a1(1+2+self.currently_running_run_id, 1+self.key_ids[key])
      self.sheet.format(cell_name, {"textFormat": {"foregroundColor": {'red': 0.0, "green": 0.7, "blue": 0.12}}})
    
    self.currently_running_config = updated_config
    return updated_config, changed_keys
  
  def sync_config_and_status(self, new_status_str=None):
    """
    Two actions in one: update_status(new_status_str) and check_for_config_updates()
    
    new_status_str (default: None) Provide None as input if you only want to fetch config updates
    
    Returns:
      updated_config = {config_key: config_value, ...} The most up-to-date dictionary of config metaparameters
      changed_keys = [changed_config_key, ...] The list of config keys for which the value was modified
    """
    if new_status_str is not None:
      self.update_status(new_status_str)
    updated_config, changed_keys = self.check_for_config_updates()
    return updated_config, changed_keys
