from getpass import getpass

from cryptoenv import KeyManager, Config, Encryptor


def generate_secure_key() -> str:
    usr_pwd = getpass("Ingrese su contraseña: ")
    secure_key = KeyManager().generate_key(usr_pwd)
    return secure_key


def create_encrypted_file():
    usr_pwd = "pass"
    encryptor = Encryptor(password=usr_pwd)

    encryptor.create_encrypted_file(
        content="Mensaje de prueba",
    )


def read_encrypted_file():
    usr_pwd = "pass"
    encryptor = Encryptor(password=usr_pwd)

    encryptor.read_encrypted_file()


def main():
    read_encrypted_file()


if __name__ == "__main__":
    main()
