from pathlib import Path

class Config:
    home_directory = Path.home()
    config_directory = f"{home_directory}/.govctl/config"

    def __init__(self):    
        Path(self.config_directory).mkdir(parents=True, exist_ok=True)
