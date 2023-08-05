import os

from pathlib import Path
from dotenv import load_dotenv, dotenv_values

def load_flow_configurations():

    if 'ENV' in os.environ:
        running_environment = os.environ.get("ENV").lower()
    else:
        running_environment = 'test'

    #load all configuration files {env}.config from the folders up the tree
    config_file_name = running_environment + '.config'
    global_config_file = str(Path(os.getcwd()).parent.parent) + '/' + config_file_name
    project_config_file = str(Path(os.getcwd()).parent) + '/' + config_file_name
    flow_config_file = str(Path(os.getcwd())) + '/' + config_file_name

    load_dotenv(global_config_file, override=True) #global prefect flow level config
    load_dotenv(project_config_file, override=True) #project level flow config
    load_dotenv(flow_config_file, override=True) #project level flow config

    config_dictionary = dotenv_values(global_config_file)
    config_dictionary.update(dotenv_values(project_config_file))
    config_dictionary.update(dotenv_values(flow_config_file))

    #are we in CI or not
    if not 'ENV' in os.environ:
        #DEBUGGING in VSCODE - have you set "cwd": "${fileDirname}" in launch.json
        #running locally so use .env files and projects/test.env
        load_dotenv(str(Path(os.getcwd()).parent.parent) + '/.env', override=True) #global prefect flow level secrets
        load_dotenv(str(Path(os.getcwd()).parent) + '/.env', override=True) #project level flow secrets
        load_dotenv(str(Path(os.getcwd())) + '/.env', override=True) #flow level secrets

    return config_dictionary