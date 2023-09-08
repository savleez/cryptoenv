from base64 import urlsafe_b64encode
from hashlib import sha256
from os import getenv
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..core import Configuration
from .key import KeyGenerator


class Crypto:
    def __init__(self, password: str) -> None:
        self.__generated_key = KeyGenerator().generate_key(password)
        self.__fernet_key = Fernet(self.__generated_key)
        self.__config = Configuration()

    def get_encrypted_file(self, **kwargs) -> tuple[str, bool]:
        file: str = kwargs.get("file", self.__config.default_encryped_file)
        file = Path(file).with_suffix(".encrypted")
        filepath = Path(self.__config.encrypted_files_dir) / file

        return (str(filepath), filepath.exists())

    def encrypt(self, content: str):
        encrypted_msg = self.__fernet_key.encrypt(content.encode()).decode()

        return encrypted_msg

    def decrypt(self, encrypted_content: str):
        decrypted_msg = self.__fernet_key.decrypt(encrypted_content.encode()).decode()

        return decrypted_msg

    def create_encrypted_file(self, content: str, **kwargs):
        file, _ = self.get_encrypted_file(**kwargs)

        encrypted_content = self.encrypt(content)

        with open(file, "+wb") as f:
            f.write(encrypted_content)

    def read_encrypted_file(self, **kwargs):
        file, exist = self.get_encrypted_file(**kwargs)

        if not exist:
            raise ValueError("Encrypted file does not exist.")

        with open(file, "r") as file:
            encrypted_content = file.read()

        decrypted_content = self.decrypt(encrypted_content)

        return decrypted_content
