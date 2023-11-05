# Google Sheet ML Scheduler: Google Docs Sheets live editing flexibility to manage your Machine Learning experiments!
A simple experiment scheduler that allows multiple instances of Colab to fetch machine learning experiment metaparameters by reading/writing in a Sheet from Google Docs Sheets.  

## A simple tool with only 3 features:  
1. Let your Colab script fetch a run config from a Sheet
2. Check during a run if the config has been updated (to manually change the learning rate for example)
3. Let your Colab script write in the Sheet a list of new future runs (for a metaparameter grid search for example)

### Installation
```bash
# In the terminal
pip install git+https://github.com/MarCnu/gsheet_ml_scheduler.git
# In Colab
!pip install git+https://github.com/MarCnu/gsheet_ml_scheduler.git
```
### BASIC USE: Fetch run configs until none is left in "ready" status
1) Make a copy of this Google Docs Sheets file [GSheetMLScheduler Basic Template](https://docs.google.com/spreadsheets/d/1HSmobuuXsOgUOM5cQ-ecHJS9hVrEj6D3AZG8gokbj6I/edit?usp=sharing)  
   **File > Create a copy**  
![Basic Template](https://raw.githubusercontent.com/MarCnu/gsheet_ml_scheduler/main/readme_files/0_basic_template.png?token=GHSAT0AAAAAACJRPKEJ7EW3I4QL3MAZEGB6ZKG2OMQ)

2) Retrieve the sharing link (no need to give read/write rights)  
   **Share > Copy link**  
   
3) Run this in Colab and replace the `sheet_link` by your own  
   <a href="https://colab.research.google.com/drive/1JsnfMWknoiij5l5V1lQSdofWJxudJwSN?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
```python
from gsheet_ml_scheduler.scheduler import GSheetMLScheduler
import time

# During the initialisation, a popup will ask you to grant Colab read/write rights (revoked each time the Colab runtime VM is disconnected/restarted)
sheet_link = "https://docs.google.com/spreadsheets/d/1HSmobuuXsOgUOM5cQ-ecHJS9hVrEj6D3AZG8gokbj6I/edit?usp=sharing"
scheduler = GSheetMLScheduler(sheet_link)

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
Scheduler connected to GSheet, its name is worker <dF53M7>
Starting run 1 with config={'n_epoch': 10, 'learning_rate': 0.0005}
Starting run 2 with config={'n_epoch': 10, 'learning_rate': 0.0001}
Starting run 3 with config={'n_epoch': 10, 'learning_rate': 5e-05}
No more ready runs
```

4) The sheet has been updated!  
   ![Running](https://raw.githubusercontent.com/MarCnu/gsheet_ml_scheduler/main/readme_files/1_running.png?token=GHSAT0AAAAAACJRPKEJ2YNSZAKOEE3KYIIYZKG2O2Q)

5) **Try again:**
   Copy/paste more runs.  
   Make copies of your Colab file to allow running multiple sessions at the same time.  
   ![Instance copies](https://raw.githubusercontent.com/MarCnu/gsheet_ml_scheduler/main/readme_files/3_instance_copies.png?token=GHSAT0AAAAAACJRPKEJRXSHNR7ELQVGFWPKZKHMQIQ)  
   Run them all at the same time.  
   All the Colab workers will connect to the same Google Sheet and modify it!  
   Out of the box, nothing to program, no complicated 3rd party website, no account to create.  
   ![Multi Worker](https://raw.githubusercontent.com/MarCnu/gsheet_ml_scheduler/main/readme_files/2_multi_worker.png?token=GHSAT0AAAAAACJRPKEJOUVUSE23BHJ5OAGGZKG3BJA)
   
### ALL FEATURES: How to write new runs for metaparameter grid search How to sync config metadata while an experiment is running.  
Run this in Colab and replace the `sheet_link` by your copy of the Sheets Basic Template (see the BASIC USE tutorial)  
<a href="https://colab.research.google.com/drive/1vxvmURd5_Ka_ui4UyH5DREf74V8vCtyD"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  
The result looks like that:  
![All features](https://raw.githubusercontent.com/MarCnu/gsheet_ml_scheduler/main/readme_files/4_all_features.png?token=GHSAT0AAAAAACJRPKEJIDSE5I3IG54GTHBCZKHSXMQ)

## Documentation

```python
from gsheet_ml_scheduler.scheduler import GSheetMLScheduler

# gsheet_file_url (str): The sharing link of your Google Docs Sheets
# sheet_index(int, optional): In case you want to use a specific tab of the Google Docs Sheets
# hardcoded_default_config (dict, optional): For static metaparameters not provided to the Sheet
# comma_number_format (bool, optional): For Google Docs languages that use comma separators for decimal numbers ("-2,0" "5,0E-3")
# google_service_account_json_path (str, optional): To use Google Service Account to access the Google Docs Sheets API, mandatory if you're not using Colab
GSheetMLScheduler(gsheet_file_url, sheet_index=0, hardcoded_default_config=None, comma_number_format=False, google_service_account_json_path=None)


# This can be used my multiple Colab instances (aka workers) in parallel
run_name, config = scheduler.find_claim_and_start_run()

# The same but in three separate functions, when using hardcoded_default_config=None
ready_run_id, gsheet_config = scheduler.find_ready_run()
claim_success = scheduler.claim_and_start_run(ready_run_id)
config = GSheetMLScheduler.complete_missing_config_params(gsheet_config, hardcoded_default_config)


# This both downloads the Sheet run config and changes the "status" at the same time
updated_config, changed_keys = scheduler.sync_config_and_status(new_status_str=None)

# The same but in three separate functions, when using hardcoded_default_config=None
gsheet_updated_config, changed_keys = scheduler.check_for_config_updates()
scheduler.update_status(new_status_str)
updated_config = GSheetMLScheduler.complete_missing_config_params(gsheet_updated_config, hardcoded_default_config)
```  

```python
from gsheet_ml_scheduler.run_writer import GSheetMLRunWriter

# gsheet_file_url (str): The sharing link of your Google Docs Sheets
# sheet_index(int, optional): In case you want to use a specific tab of the Google Docs Sheets
# comma_number_format (bool, optional): For Google Docs languages that use comma separators for decimal numbers ("-2,0" "5,0E-3")
# google_service_account_json_path (str, optional): To use Google Service Account to access the Google Docs Sheets API, mandatory if you're not using Colab
GSheetMLRunWriter(gsheet_file_url, sheet_index=0, comma_number_format=False, google_service_account_json_path=None)

# configs (list of dicts): A list of configs to be added to the Sheet
run_writer.write_runs(configs)
```
