from setuptools import setup

setup(
    name='gsheet-ml-scheduler',
    version='1.0',
    url='https://github.com/MarCnu/gsheet_ml_scheduler.git',
    author='MarCnu',
    description='A simple scheduler that allows multiple instances of Colab to fetch machine learning run configs from a Google Docs Sheets',
    packages=['gsheet_ml_scheduler'],    
    install_requires=['pandas'],
)
