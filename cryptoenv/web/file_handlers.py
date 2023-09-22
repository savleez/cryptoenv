from pathlib import Path


def validate_filename(file):
    file = Path(file)

    if file.suffix != ".encrypted":
        raise ValueError(f"File {file.name} extension is not .encrypted.")

    if not file.exists():
        raise ValueError(f"File {file} does not exist.")
    

def get_encrypted_file() -> Path:
    file = ""

    return file


def get_config_template() -> dict:
    config = {
        "General": {
            "server_url": "https://example.com",
            "timeout": 30,
        },
        "Credentials": {
            "db_username": "my_username",
            "db_password": "my_password",
        },
    }

    return config
