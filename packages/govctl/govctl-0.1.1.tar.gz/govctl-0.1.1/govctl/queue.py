import typer
from rich import print
from pathlib import Path
import configparser
from .config import Config

global_config = Config()
config_file = configparser.ConfigParser()

def check_config(what, default):
    CHECK_THE_VALUE = typer.confirm(what + ' [' + default + ']')
    if CHECK_THE_VALUE:
        the_value=default
    else:
        the_value = typer.prompt("Please customize " + what)
    return the_value

app = typer.Typer()

@app.command()
def config():
    BROKER_HOST = check_config(what="What is your broker host ?", default="localhost")
    BROKER_PORT = check_config(what="What is your broker port ?", default="5672")
    BROKER_USERNAME = check_config(what="What is your broker username ?", default="test")
    BROKER_PASSWORD = check_config(what="What is your broker password ?", default="password")
    
    config_file[BROKER_HOST]={
        "BROKER_HOST": BROKER_HOST,
        "BROKER_PORT": int(BROKER_PORT),
        "BROKER_USERNAME": BROKER_USERNAME,
        "BROKER_PASSWORD": BROKER_PASSWORD
    }
 
    with open(f"{global_config.config_directory}/queue.ini","w") as file_object:
        config_file.write(file_object)
        print(f"Creating configuration files in {global_config.config_directory}/queue.ini")

@app.command()
def ping():
    pass