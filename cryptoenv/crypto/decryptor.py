from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from cryptoenv.core.configuration import Configs
from cryptoenv.crypto.keys import KeyGenerator


class Crypto:
    def __init__(self, password: str) -> None:
        self.__generated_key = KeyGenerator().generate_key(password)
        self.__fernet_key = Fernet(self.__generated_key)
        self.__config = Configs

    def get_encrypted_file(self, **kwargs) -> tuple[Path, bool]:
        """Function that returns the path of a given encrypted file.

        Kwargs:
            filename (str): Name of the encrypted file.

        Returns:
            tuple[Path, bool]: A tuple with the absolute path of the encrypted file,
            and a boolean that indicates if the file exists.
        """
        filename: str = kwargs.get("filename")

        if filename:
            filename = Path(filename).with_suffix(".encrypted")
            filepath = Path(self.__config.encrypted_files_dir) / filename
        else:
            filepath = self.__config.encryped_file

        return filepath, filepath.exists()

    def encrypt(self, content: str) -> str:
        """Method that encrypts a given string using the pre defined Fernet key.

        Args:
            content (str): String to encrypt.

        Returns:
            encrypted_content (str): Encrypted string.
        """
        encrypted_content = self.__fernet_key.encrypt(content.encode()).decode()

        return encrypted_content

    def decrypt(self, encrypted_content: str) -> str:
        """Method that decrypts a given encrypted string using the pre defined Fernet key.

        Args:
            encrypted_content (str): String to decrypt.

        Returns:
            decrypred_content (str): Decrypted string.
        """

        try:
            decrypted_msg = self.__fernet_key.decrypt(
                encrypted_content.encode()
            ).decode()

            return decrypted_msg

        except InvalidToken as itex:
            raise InvalidToken("Invalid password") from None

    def create_encrypted_file(self, content: str, **kwargs) -> Path:
        """Method that created an encrypted file with the specified content.

        Kwargs:
            filename (str): Name of the file. Defaults to config default encryped file name

        Args:
            content (str): Content to encrypt.

        Returns:
            file (Path): Absolute path of the created encrypted file.
        """

        file, _ = self.get_encrypted_file(**kwargs)

        encrypted_content = self.encrypt(content)

        with open(str(file), "+w") as f:
            f.write(encrypted_content)

        return file

    def read_encrypted_file(self, **kwargs) -> str:
        """Method that decryps an encrypted file.

        Kwargs:
            filename (str): Name of the file. Defaults to config default encryped file name

        Returns:
            decrypted_content (str): Decrypted content of the file.
        """

        file, exist = self.get_encrypted_file(**kwargs)

        if not exist:
            raise ValueError("Encrypted file does not exist.")

        with open(file, "r") as file:
            encrypted_content = file.read()

        decrypted_content = self.decrypt(encrypted_content)

        return decrypted_content
