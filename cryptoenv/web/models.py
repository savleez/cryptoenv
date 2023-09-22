from pathlib import Path
import logging

from pydantic import BaseModel

from cryptoenv import Crypto, ConfigHandler


class EncryptedFile:
    def __init__(self, password: str, **kwargs) -> None:
        self.password = password
        self.filename = kwargs.get("filename")

        self.crypto = Crypto(self.password)

    #     self.encrypted_content = None
    #     self.decrypted_content = None

    # def encrypt_content(self, content: str) -> str:
    #     self.encrypted_content = self.crypto.encrypt(content)

    #     return self.encrypt_content

    # def decrypt_content(self, encrypted_content: str):
    #     try:
    #         self.decrypted_content = self.crypto.decrypt(encrypted_content)
    #     except Exception as ex:
    #         logging.exception("Error decrypting the content.")
    #         logging.exception(ex)
    #         raise ex from None
    #     else:
    #         return self.decrypted_content

    # def save_file(self) -> bool:
    #     pass


class RequestData(BaseModel):
    password: str
