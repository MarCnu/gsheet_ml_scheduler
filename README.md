# Google Sheet ML Scheduler: Google Docs Sheets live editing flexibility to manage your Machine Learning experiments!
A simple experiment scheduler that allows multiple instances of Colab to fetch machine learning run configs by reading/writing in a sheet from Google Docs Sheets.  

### A simple tool with only 3 features:  
1. Let your python sript fetch a run config from a Sheet
2. Check during a run if the config has been updated (to manually change the learning rate for example)
3. Let your python script write in the Sheet a list of new new future runs (for a metaparameter grid search for example)
