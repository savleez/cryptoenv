from base64 import urlsafe_b64encode
from configparser import ConfigParser
from getpass import getpass
from hashlib import sha256
from os import getenv
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Configuration:
    __instance = None

    def __new__(cls, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, **kwargs) -> None:
        self.config_file = "config"
        self.verbose = kwargs.get("verbose", False)

        self.__salt = self.generate_salt()
        self.__load_config()

    def __load_config(self):
        print("Loading config file") if self.verbose else None
        config = ConfigParser()

        if Path(self.config_file).exists():
            config.read(self.config_file)
        else:
            print(
                "Config file does not exist. Creating it..."
            ) if self.verbose else None
            self.__save_config(config)

        # General settings block
        if "GENERAL" not in config:
            print(
                "Config file GENERAL block does not exist. Creating it..."
            ) if self.verbose else None
            config["GENERAL"] = {}

        if "verbose" in config["GENERAL"]:
            self.verbose = config["GENERAL"]["verbose"].lower() == True
        else:
            self.verbose = False
            config["GENERAL"]["verbose"] = "False"
            self.__save_config(config)

    def __save_config(self, config):
        with open(self.config_file, "w") as config_file:
            config.write(config_file)

    def generate_salt(self):
        print("Generating salt with predefined arguments") if self.verbose else None
        pepper = getenv("PEPPER", "default_pepper")
        machine_name = getenv("HOSTNAME", "default_host")
        user_name = getenv("USER", "default_host")

        salt_data = f"{pepper}-{user_name}-{machine_name}".encode("utf-8")
        salt = sha256(salt_data).hexdigest()
        return salt

    def generate_key(self, password):
        print("Generating a secured derived key") if self.verbose else None
        password_bytes = password.encode("utf-8")
        salt_bytes = self.__salt.encode("utf-8")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=salt_bytes,
            length=32,
            backend=default_backend(),
        )
        key = urlsafe_b64encode(kdf.derive(password_bytes))

        return key


def main():
    config = Configuration(verbose=True)

    usr_pwd = getpass("Ingrese su contraseña: ")
    secure_key = config.generate_key(usr_pwd)
    print("Clave generada:", secure_key.decode("utf-8"))


if __name__ == "__main__":
    main()
