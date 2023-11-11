from setuptools import setup

setup(
    name='gsheets-ml-scheduler',
    version='1.1',
    url='https://github.com/MarCnu/gsheets_ml_scheduler.git',
    author='MarCnu',
    description='A simple experiment scheduler that allows multiple instances of Colab to fetch machine learning experiment metaparameters by reading/writing in a sheet from Google Docs Sheets.',
    packages=['gsheets_ml_scheduler'],    
    install_requires=['pandas', 'gspread', 'google-auth'],
)
