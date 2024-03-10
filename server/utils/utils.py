import yaml


def load_config(file_path):
    with open(file_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            config = None
    return config
