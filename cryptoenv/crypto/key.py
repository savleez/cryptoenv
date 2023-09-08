from base64 import urlsafe_b64encode
from hashlib import sha256
from os import getenv

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class KeyGenerator:
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
