import os
from typing import Optional
from ml.llm.prompt_format import ModelConfig
import dotenv


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


def load_model_config(config_path: str) -> ModelConfig:
    """Load the model_config

    Parameters
    ----------
    config_path: str
        path where model config files reside
    """
    with open(config_path, "r") as stream:
        return ModelConfig.parse_yaml(stream)
