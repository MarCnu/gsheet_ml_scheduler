<a href="https://colab.research.google.com/github/ultralytics/ultralytics/blob/main/examples/tutorial.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
# Google Sheet ML Scheduler: Google Docs Sheets live editing flexibility to manage your Machine Learning experiments!
A simple experiment scheduler that allows multiple instances of Colab to fetch machine learning experiment metaparameters by reading/writing in a sheet from Google Docs Sheets.  

## A simple tool with only 3 features:  
1. Let your python script fetch a run config from a Sheet
2. Check during a run if the config has been updated (to manually change the learning rate for example)
3. Let your python script write in the Sheet a list of new new future runs (for a metaparameter grid search for example)

### Installation
```bash
# In the terminal
pip install git+https://github.com/MarCnu/gsheet_ml_scheduler.git
# In Colab
!pip install git+https://github.com/MarCnu/gsheet_ml_scheduler.git
```
### Basic use: Fetch run configs until none is left in "ready" status
1) Make a copy of this Google Docs Sheets file [GSheetMLScheduler Basic Template](https://docs.google.com/spreadsheets/d/1HSmobuuXsOgUOM5cQ-ecHJS9hVrEj6D3AZG8gokbj6I/edit?usp=sharing)  
   **File > Create a copy**  
![Basic Template](https://raw.githubusercontent.com/MarCnu/gsheet_ml_scheduler/main/readme_files/0_basic_template.png?token=GHSAT0AAAAAACJRPKEJEJORKRN53OTL2GLKZKGZVSA)

2) Retrieve the sharing link (no need to give read/write rights)  
   **Share > Copy link**  
   
3) Run this in Colab and replace the `sheet_link` by your own  
   <a href="https://colab.research.google.com/drive/1JsnfMWknoiij5l5V1lQSdofWJxudJwSN?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
```python
from gsheet_ml_scheduler.scheduler import GSheetMLScheduler
import time

# During the initialisation, a popup will open asking you to grant Colab read/write rights
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
    time.sleep(0.1)


  # Replaces status "running" by "done"
  scheduler.run_done()
```
```bash
Scheduler connected to GSheet, its name is worker <C0g3fQ>
Starting run 2 with config={'n_epoch': 10, 'learning_rate': '1,00E-04'}
Starting run 3 with config={'n_epoch': 10, 'learning_rate': '5,00E-05'}
No more ready runs
```
