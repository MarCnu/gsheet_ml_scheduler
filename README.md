# Google Sheets ML Scheduler: Google Docs Sheets live editing flexibility to manage your Machine Learning experiments!
A simple experiment scheduler that allows multiple instances of Colab to fetch machine learning experiment metaparameters by reading/writing in a spreadsheet from Google Docs Sheets.  

## A simple tool with only 3 features:  
1. Let your Colab script fetch a run config from a sheet
2. Check during a run if the config has been updated (to manually change the learning rate for example)
3. Let your Colab script write in the sheet a list of new future runs (for a metaparameter grid search for example)

### Installation
```bash
# In the terminal
pip install git+https://github.com/MarCnu/gsheets_ml_scheduler.git
# In Colab
!pip install git+https://github.com/MarCnu/gsheets_ml_scheduler.git
```
### BASIC USE: Fetch run configs until none is left in "ready" status
1) Make a copy of this Google Docs Sheets file [GSheetMLScheduler Basic Template](https://docs.google.com/spreadsheets/d/1HSmobuuXsOgUOM5cQ-ecHJS9hVrEj6D3AZG8gokbj6I/edit)  
   **File > Create a copy**  
![Basic Template](https://raw.githubusercontent.com/MarCnu/gsheets_ml_scheduler/main/readme_files/0_basic_template.png)

2) Retrieve the sharing link (no need to give read/write rights)  
   **Share > Copy link**  
   
3) Run this in Colab and replace the `sheets_link` by your own  
   <a href="https://colab.research.google.com/drive/1JsnfMWknoiij5l5V1lQSdofWJxudJwSN"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
```python
from gsheets_ml_scheduler.scheduler import GSheetsMLScheduler
import time

# Each time you restart a Colab session, a popup will ask for read/write rights again
sheets_link = "https://docs.google.com/spreadsheets/d/1HSmobuuXsOgUOM5cQ-ecHJS9hVrEj6D3AZG8gokbj6I/edit"
scheduler = GSheetsMLScheduler(sheets_link)

while True:
  # Finds a run with the status "ready" and replaces "ready" by "running"
  run_name, config = scheduler.find_claim_and_start_run()
  if run_name is None:
    print("No more ready runs")
    break
  print(f"Starting run {run_name} with config={config}")


  # Your learning loop here
  for epoch in range(config["n_epoch"]):
    time.sleep(0.5)


  # Replaces status "running" by "done"
  scheduler.run_done()
```
```bash
Scheduler connected to GSheets, its name is worker <43dLkW>
Starting run 1 with config={'n_epoch': 10, 'learning_rate': 0.0005}
Starting run 2 with config={'n_epoch': 10, 'learning_rate': 0.0001}
Starting run 3 with config={'n_epoch': 10, 'learning_rate': 5e-05}
No more ready runs
```

4) The sheet has been updated!  
   ![Running](https://raw.githubusercontent.com/MarCnu/gsheets_ml_scheduler/main/readme_files/1_running.png)

5) **Try again:**
   Copy/paste more runs.  
   Make copies of your Colab file to allow running multiple sessions at the same time.  
   ![Instance copies](https://raw.githubusercontent.com/MarCnu/gsheets_ml_scheduler/main/readme_files/2_instance_copies.png)  
   Run them all at the same time.  
   All the Colab workers will connect to the same Google Sheets and modify it!  
   Out of the box, nothing to program, no complicated 3rd party website, no account to create.  
   ![Multi Worker](https://raw.githubusercontent.com/MarCnu/gsheets_ml_scheduler/main/readme_files/3_multi_worker.png)
   
### ALL FEATURES: How to write new runs for metaparameter grid search. How to sync config metadata while an experiment is running.  
Run this in Colab and replace the `sheets_link` by your copy of the [GSheetsMLScheduler Basic Template](https://docs.google.com/spreadsheets/d/1HSmobuuXsOgUOM5cQ-ecHJS9hVrEj6D3AZG8gokbj6I/edit) (see the BASIC USE tutorial)  
<a href="https://colab.research.google.com/drive/1vxvmURd5_Ka_ui4UyH5DREf74V8vCtyD"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  
The result looks like that:  
![All features](https://raw.githubusercontent.com/MarCnu/gsheets_ml_scheduler/main/readme_files/4_all_features.png)

### Colab + Google Sheets + Weights & Biases
For a great and easy to use ML expriment environment, you can combine both this GSheetsMLScheduler for scheduling and the famous Weight & Biases platform for logging.  
You'll be able to track the progress of your learning with graphs on WandB in real time and then update your GSheets to change metaparameters on the fly!  
![Sheets WandB](https://raw.githubusercontent.com/MarCnu/gsheets_ml_scheduler/main/readme_files/5_gsheets_weight_and_biases.png)

## Authenticate with Google Service Account

In Colab, you can use `colab.auth` to give read/write rights to Google Drive  
Outside of Colab, you must authenticate through a Google Service Account to access the Google Sheets API  

To obtain a account.json file, follow this video: https://www.youtube.com/watch?v=IZrzdspl_3k  
1. Create a Project in [Google Cloud Console](https://console.cloud.google.com) (You can name it gspread-api for example)  
2. In the search bar, search for Google Sheets API (at the bottom, in the MarketPlace section) and activate the API for your Project  
3. Open the navigation menu on the left > APIs & Services > Credentials > Create credentials > Service account > Name it "gspread-access" for example > Done  
4. In the service account > Keys tab > Add Key > Json

Once you have downloaded the json file, open it, copy the value of `client_email` and in the sharing settings of your Sheets file, add this email to the Editors  
Finally, use the parameter `service_account_json_path` during the initialisation of `GSheetsMLScheduler` and `GSheetsMLRunWriter`  

## Documentation
### GSheetsMLScheduler
```python
from gsheets_ml_scheduler.scheduler import GSheetsMLScheduler

# gsheets_file_url (str): The sharing link of your Google Docs Sheets
# sheet_index(int, optional): In case you want to use a specific tab of the Google Docs Sheets
# hardcoded_default_config (dict, optional): For static metaparameters not provided to the sheet
# comma_number_format (bool, optional): For Google Docs languages that use comma separators for decimal numbers ("-2,0" "5,0E-3")
# service_account_json_path (str, optional): To use Google Service Account to access the Google Docs Sheets API, mandatory if you're not using Colab
scheduler = GSheetsMLScheduler(gsheets_file_url, sheet_index=0, hardcoded_default_config=None, comma_number_format=False, service_account_json_path=None)


# This can be used my multiple Colab instances (aka workers) in parallel
run_name, config = scheduler.find_claim_and_start_run()

# The same but in three separate functions, when using hardcoded_default_config=None
ready_run_id, gsheets_config = scheduler.find_ready_run()
claim_success = scheduler.claim_and_start_run(ready_run_id)
config = GSheetsMLScheduler.complete_missing_config_params(gsheets_config, hardcoded_default_config)


# This both downloads the sheet run config and changes the "status" at the same time
updated_config, changed_keys = scheduler.sync_config_and_status(new_status_str=None)

# The same but in three separate functions, when using hardcoded_default_config=None
scheduler.update_status(new_status_str)
gsheets_updated_config, changed_keys = scheduler.check_for_config_updates()
updated_config = GSheetsMLScheduler.complete_missing_config_params(gsheets_updated_config, hardcoded_default_config)

# Replaces "status" and sets a blue background
scheduler.run_done(new_status_str="done")
```  
### GSheetsMLRunWriter
```python
from gsheets_ml_scheduler.run_writer import GSheetsMLRunWriter

# gsheets_file_url (str): The sharing link of your Google Docs Sheets
# sheet_index(int, optional): In case you want to use a specific tab of the Google Docs Sheets
# comma_number_format (bool, optional): For Google Docs languages that use comma separators for decimal numbers ("-2,0" "5,0E-3")
# service_account_json_path (str, optional): To use Google Service Account to access the Google Sheets API, mandatory if you're not using Colab
run_writer = GSheetsMLRunWriter(gsheets_file_url, sheet_index=0, comma_number_format=False, service_account_json_path=None)

# configs (list of dicts): A list of configs to be added to the sheet
run_writer.write_runs(configs)
```
### Sheet format
```python
################
# Line 1 is reserved for naming config keys
# Line 2 is reversed for default_config values
# Lines below that are free to use for your runs
#
# Columns "run_name", "status" and "worker_name" are MANDATORY
# Column order doesn't matter (all is based on Line 1 column names)
################
```
### Misc
```python
print("Colors", scheduler.colors) # You can change the colors

scheduler.download_data() # Manually downloads the gsheets data

print("Nb_runs", scheduler.nb_runs)
print("Keys", scheduler.keys)
print("Key_ids", scheduler.key_ids)
print("Config_keys", scheduler.config_keys)
print("Config_defaults", scheduler.config_defaults)
print("Values", scheduler.values)

# Use get_run_config(run_index) to get value + config_defaults (but not hardcoded_config_defaults)
print("\nAll run-status-configs")
for i in range(scheduler.nb_runs):
  print([scheduler.values["run_name"][i], scheduler.values["status"][i], scheduler.get_run_config(i)])

# You can make manual read/write operations to the sheet using the gspread library
# scheduler.all_sheets contains the gspread file root, if you want to access another tab of the file
# scheduler.sheet can be used to call all gspread functions
# Google Sheets uses (1,1) for the top left cell, not (0,0) as in normal Python
_ = scheduler.sheet.update_cell(sheet_line, sheet_column, str_value)
_ = scheduler.sheet.update_cell(1+python_line_index, 1+python_column_index, str_value)
```
