from configparser import ConfigParser
from json import dumps as json_dumps


class DecryptedConfig:
    def __init__(self, config_content: str | dict):
        self.config_content = config_content

        self.config = ConfigParser()

        if isinstance(self.config_content, str):
            self.config.read_string(self.config_content)
        elif isinstance(self.config_content, dict):
            self.config.read_dict(self.config_content)
        else:
            raise ValueError("Config content must be a string or a dictionary.")
        
    def get_config(self):
        return self.config

    def config_to_dict(self) -> dict:
        config_dict = {
            section: dict(self.config_content[section])
            for section in self.config_content.sections()
        }

        return config_dict

    def serialize_config(self) -> str:
        config_dict = self.config_to_dict()
        config_str = json_dumps(config_dict)

        return config_str
