from setuptools import setup, find_packages

setup(
    name='gsheet_ml_scheduler',
    version='1.0',
    url='https://github.com/MarCnu/gsheet_ml_scheduler.git',
    author='MarCnu',
    description='A simple scheduler that allows multiple instances of Colab to fetch machine learning run configs from a Google Docs Sheets',
    packages=find_packages(),    
    install_requires=['pandas'],
)
