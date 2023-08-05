import json
from .models import ConfigModel


def load_config(config_file_path: str):
    with open(config_file_path, 'r') as f:
        data = json.load(f)
        return ConfigModel(**data)
       