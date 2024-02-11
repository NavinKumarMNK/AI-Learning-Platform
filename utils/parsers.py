from typing import Dict

import yaml


class DictObjectParser:
    """Converts a dictionary to an object with attributes"""

    def __init__(self, data: Dict) -> None:
        if not isinstance(data, dict):
            raise ValueError("Input data is not a dictionary")
        for key, value in data.items():
            if isinstance(value, (list, tuple)):
                setattr(
                    self,
                    key,
                    [DictObjectParser(x) if isinstance(x, dict) else x for x in value],
                )
            else:
                setattr(
                    self,
                    key,
                    DictObjectParser(value) if isinstance(value, dict) else value,
                )

    def to_dict(self) -> dict:
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, DictObjectParser):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, DictObjectParser) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result


class YamlParser:
    """Parses a yaml file to a dictionary object"""

    def __init__(self, filepath: str):
        with open(filepath, "r") as file:
            data = yaml.safe_load(file)
        self.obj = DictObjectParser(data)  # noqa: F841

    def get_data(self):
        return self.obj


# Example usage:
if __name__ == "__main__":
    reader = YamlParser(filename="config.yaml")
    DATA = reader.obj

    print(DATA.app.model)
