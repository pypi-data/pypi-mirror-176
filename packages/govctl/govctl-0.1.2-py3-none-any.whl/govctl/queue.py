import typer
from rich import print
from pathlib import Path
import configparser
from .config import Config
from celery import Celery

global_config = Config()
config_file = configparser.ConfigParser()

def check_parameters(what, default):
    CHECK_THE_VALUE = typer.confirm(what + ' [' + default + ']')
    if CHECK_THE_VALUE:
        the_value=default
    else:
        the_value = typer.prompt("Please customize " + what)
    return the_value

def connect(config):
    BROKER_HOST = config.get('default', 'BROKER_HOST')
    BROKER_PORT = config.get('default', 'BROKER_PORT')
    BROKER_USERNAME = config.get('default', 'BROKER_USERNAME')
    BROKER_PASSWORD = config.get('default', 'BROKER_PASSWORD')
    BACKEND_HOST = config.get('default', 'BACKEND_HOST')
    BACKEND_PORT = config.get('default', 'BACKEND_PORT')
    BACKEND_USERNAME = config.get('default', 'BACKEND_USERNAME')
    BACKEND_PASSWORD = config.get('default', 'BACKEND_PASSWORD')
    BACKEND_NAME = config.get('default', 'BACKEND_NAME')

    try:
        producer = Celery('tasks',
            broker=f'amqp://{BROKER_USERNAME}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/',
            backend=f'mongodb://{BACKEND_USERNAME}:{BACKEND_PASSWORD}@{BACKEND_HOST}:{BACKEND_PORT}/{BACKEND_NAME}?authSource={BACKEND_NAME}')
        return producer
    except:
        print("Cannot connect to the server.")

app = typer.Typer()

@app.command()
def configure():
    BROKER_HOST = check_parameters(what="What is your broker host ?", default="localhost")
    BROKER_PORT = check_parameters(what="What is your broker port ?", default="5672")
    BROKER_USERNAME = check_parameters(what="What is your broker username ?", default="test")
    BROKER_PASSWORD = check_parameters(what="What is your broker password ?", default="password")

    BACKEND_HOST = check_parameters(what="What is your backend host ?", default="localhost")
    BACKEND_PORT = check_parameters(what="What is your backend port ?", default="27017")
    BACKEND_USERNAME = check_parameters(what="What is your backend username ?", default="test")
    BACKEND_PASSWORD = check_parameters(what="What is your backend password ?", default="password")
    BACKEND_NAME = check_parameters(what="What is the name of your backend ?", default="test")

    config_file.add_section('default')
    config_file.set('default', 'BROKER_HOST', BROKER_HOST)
    config_file.set('default', 'BROKER_PORT', BROKER_PORT)
    config_file.set('default', 'BROKER_USERNAME', BROKER_USERNAME)
    config_file.set('default', 'BROKER_PASSWORD', BROKER_PASSWORD)
    config_file.set('default', 'BACKEND_HOST', BACKEND_HOST)
    config_file.set('default', 'BACKEND_PORT', BACKEND_PORT)
    config_file.set('default', 'BACKEND_USERNAME', BACKEND_USERNAME)
    config_file.set('default', 'BACKEND_PASSWORD', BACKEND_PASSWORD)
    config_file.set('default', 'BACKEND_NAME', BACKEND_NAME)

    with open(f"{global_config.config_directory}/queue.ini","w") as file_object:
        config_file.write(file_object)
        print(f"Creating configuration files in {global_config.config_directory}/queue.ini")

@app.command()
def crawl(url: str = typer.Argument(..., help="The URL you want to crawl.")):
    if url.startswith("https"):
        config = configparser.ConfigParser()
        try:
            config.read(f"{global_config.config_directory}/queue.ini")
            producer = connect(config)
            producer.send_task('tasks.listing', queue='worker', args=[f"{url}"])
            print(f"Crawling {url}...")
        except:
            # Si le fichier de config n'existe pas, on lance la config puis on relance la commande
            configure()
            crawl(url)
    else:
        print("Syntax error : url must begin with https://")
        print("I will crawl website with https only.")
        exit(2)

    
    