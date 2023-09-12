from configparser import ConfigParser, MissingSectionHeaderError
from json import dumps as json_dumps


class ConfigHandler:
    def __init__(self, config_content: str | dict):
        self.config_content = config_content

        self.__config = ConfigParser()

        if isinstance(self.config_content, str):
            try:
                self.__config.read_string(self.config_content)
            except MissingSectionHeaderError:
                raise ValueError("Error reading config file content.") from None
        elif isinstance(self.config_content, dict):
            self.__config.read_dict(self.config_content)
        else:
            raise ValueError("Config content must be a string or a dictionary.")

    def get_config_object(self):
        return self.__config

    def config_to_dict(self) -> dict:
        config_dict = {
            section: dict(self.__config[section])
            for section in self.__config.sections()
        }

        return config_dict

    def serialize_config(self) -> str:
        config_dict = self.config_to_dict()
        config_str = json_dumps(config_dict)

        return config_str
