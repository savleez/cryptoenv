from configparser import ConfigParser
from pathlib import Path


class Configuration:
    """Singleton class for managing configuration settings.

    This class implements the Singleton pattern to ensure that only one instance of
    Configuration exists throughout the application. It manages configuration settings,
    both stored in a configuration file like the verbose mode, and a generated salt
    using predefined arguments.

    Creates a new instance of the Configuration class if it doesn't exist.
    """

    __instance = None

    def __new__(cls, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, **kwargs):
        self.__base_dir: Path = Path(__file__).resolve().parent
        self.__app_dir: Path = self.__base_dir.parent

        self.__config_file_dir: Path = kwargs.get("config_file_dir", self.__app_dir)
        self.__config_file: Path = self.__config_file_dir / "config"

        self.verbose: bool = False
        self.encrypted_files_dir: Path = kwargs.get(
            "encrypted_files_dir", self.__app_dir
        )
        self.default_encryped_file: str = "encrypted_file.encrypted"

        self.__load_config()

    def __load_config(self):
        """Loads configuration file or create a new one if it does not exist."""

        config = ConfigParser()

        if self.__config_file.exists():
            config.read(self.__config_file)

        # General settings block
        if "GENERAL" not in config:
            config["GENERAL"] = {}

        if not "verbose" in config["GENERAL"]:
            config["GENERAL"]["verbose"] = "False"

        if not "encrypted files dir" in config["GENERAL"]:
            config["GENERAL"]["encrypted files dir"] = str(self.encrypted_files_dir)

        # Update configs settings
        self.verbose = config["GENERAL"]["verbose"].lower() == "true"
        self.encrypted_files_dir = Path(config["GENERAL"]["encrypted files dir"])

    def __save_config(self, config: ConfigParser):
        """Save configuration settings to the file.

        Params:
            config (ConfigParser): Configuration instance.
        """

        with open(self.__config_file, "w") as config_file:
            config.write(config_file)

    def create_default_config_file(config_file_path: str, encrypted_files_dir: str):
        config_file_path = Path(config_file_path)
        encrypted_files_dir = Path(encrypted_files_dir)

        config_file_path.parent.mkdir(exist_ok=True, parents=True)
        encrypted_files_dir.mkdir(exist_ok=True, parents=True)

        config = ConfigParser()
        config["GENERAL"] = {}
        config["GENERAL"]["verbose"] = "False"
        config["GENERAL"]["encrypted files dir"] = str(encrypted_files_dir.resolve())

        with open(config_file_path, "w") as config_file:
            config.write(config_file)
