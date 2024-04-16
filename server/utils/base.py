import yaml
import dotenv
from typing import Optional


def load_config(file_path):
    with open(file_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            config = None
    return config


def load_env(path: Optional[str] = None):
    """Load ths the root environment variable

    Parameters
    ----------
    path : str
        path of the .env file thats needs to get loaded
    """
    if path:
        dotenv.load_dotenv(path)
    else:
        dotenv.load_dotenv()
