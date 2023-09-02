from base64 import urlsafe_b64encode
from hashlib import sha256
from os import getenv
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .configuration import Configuration


class KeyManager:
    """Class for keys management.

    This class provides methods to generate unique salts and derive keys from passwords.
    The generated keys could be used to encrypt a file.

    Attributes:
        pepper (str): The environment variable name for pepper. Default is "PEPPER".
    """

    def __init__(self, **kwargs):
        self.pepper_var_name = kwargs.get("pepper", "PEPPER")
        self.__salt = self.generate_salt()

    def generate_salt(self) -> str:
        """Generates a unique salt based on environment variables.

        The salt creation is meant to be unique for each use, but still reproducible
        in order to recalculate the derived key.

        Returns:
            salt (str): Generated salt.
        """

        pepper = getenv(self.pepper_var_name, "default_pepper")
        user_name = getenv("USER", "default_user")

        salt_data = f"{pepper}-{user_name}".encode("utf-8")
        salt = sha256(salt_data).hexdigest()
        return salt

    def generate_key(self, password: str) -> str:
        """Generate a derived key from the provided password.

        Params:
            password (str): User's password.

        Returns:
            key (str): Generated key.
        """

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

        return key.decode("utf-8")


class Encryptor:
    def __init__(self, password: str, **kwargs) -> None:
        self.__generated_key = KeyManager().generate_key(password)
        self.__fernet_key = Fernet(self.__generated_key)

        self.encrypted_files_dir = kwargs.get(
            "encrypted_files_dir", Configuration().encrypted_files_dir
        )

    def get_encrypted_file(self, **kwargs) -> tuple[str, bool]:
        file: str = kwargs.get("file", Configuration().default_encryped_file)
        file = Path(file).with_suffix(".encrypted")
        filepath = Path(self.encrypted_files_dir) / file

        return (str(filepath), filepath.exists())

    def encryp_content(self, content: str):
        encrypted_content = self.__fernet_key.encrypt(content.encode()).decode()

        return encrypted_content

    def decrypt_content(self, encrypted_content: str):
        decrypted_content = self.__fernet_key.decrypt(
            encrypted_content.encode()
        ).decode()

        return decrypted_content

    def create_encrypted_file(self, content: str, **kwargs):
        file, _ = self.get_encrypted_file(**kwargs)

        encrypted_content = self.__fernet_key.encrypt(content.encode("utf-8"))

        with open(file, "+wb") as file:
            file.write(encrypted_content)

    def read_encrypted_file(self, **kwargs):
        file, exist = self.get_encrypted_file(**kwargs)

        if not exist:
            raise ValueError("Encrypted file does not exist.")

        with open(file, "r") as file:
            encrypted_content = file.read()

        decrypted_content = self.__fernet_key.decrypt(
            encrypted_content.encode("utf-8")
        ).decode("utf-8")

        return decrypted_content
