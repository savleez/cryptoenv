from configparser import ConfigParser
from pathlib import Path


class Configuration:
    """Singleton class for managing configuration settings.

    This class implements the Singleton pattern to ensure that only one instance of
    Configuration exists throughout the application.

    It manages the project configuration settings:
        - O

    Creates a new instance of the Configuration class if it doesn't exist.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__base_dir: Path = Path(__file__).resolve().parent.parent
        self.__app_dir: Path = self.__base_dir.parent

        # Project config file
        self.__config_file_dir: Path = self.__app_dir
        self.__config_file: Path = self.__config_file_dir / "config"

        # Output encrypted configs directory
        self.encrypted_files_dir: Path = self.__app_dir

        self.encryped_file_name: str = None
        self.default_encryped_file_name: str = "config.encrypted"

        self.__load_config()

        if self.encryped_file_name is None:
            self.encryped_file_name = self.default_encryped_file_name

        self.encryped_file = self.encrypted_files_dir / self.encryped_file_name

    def __load_config(self):
        """Loads configuration file or create a new one if it does not exist."""

        if not self.__config_file.exists():
            return

        config = ConfigParser()
        config.read(self.__config_file)

        # General settings block
        if "GENERAL" not in config:
            return

        if "encryped file name" in config["GENERAL"]:
            self.encryped_file_name = config["GENERAL"]["encryped file name"]
        else:
            self.encryped_file_name = self.default_encryped_file_name

        if "encrypted files dir" in config["GENERAL"]:
            self.encrypted_files_dir = Path(config["GENERAL"]["encrypted files dir"])

    def save_config(self, config: ConfigParser):
        """Save configuration settings to the file.

        Params:
            config (ConfigParser): Configuration instance.
        """

        with open(self.__config_file, "w") as config_file:
            config.write(config_file)

    def get_default_config(self) -> ConfigParser:
        config = ConfigParser()
        config["GENERAL"] = {}

        config["GENERAL"]["encryped file name"] = self.default_encryped_file_name

        config["GENERAL"]["encrypted files dir"] = str(
            self.encrypted_files_dir.resolve()
        )

        return config

    def get_config_file_path(self) -> tuple[Path, bool]:
        return self.__config_file, self.__config_file.exists()

    def get_encryped_file_path(self) -> tuple[Path, bool]:
        return self.encryped_file, self.encryped_file.exists()

    def create_default_config_file(self):
        config = self.get_default_config()
        self.save_config(config=config)


Configs = Configuration()
