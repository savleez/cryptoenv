from pathlib import Path
from shutil import rmtree

temp_dir_name = "temp_test_dir"


def get_temp_dir() -> tuple[Path, bool]:
    """Get the absolute path for a temporal directory.

    Returns:
        Path, bool: Path for temp dir and true if exists
    """

    global temp_dir_name

    try:
        temp_dir = Path(temp_dir_name).resolve()
        return temp_dir, temp_dir.exists()
    except Exception as ex:
        print(f"An error ocurred: {ex}")
        return None, False


def create_temp_dir() -> None:
    """Create a temporary directory for testing."""

    try:
        temp_dir, _ = get_temp_dir()
        temp_dir.mkdir(parents=True, exist_ok=True)
    except Exception as ex:
        print(f"An error ocurred: {ex}")


def delete_temp_dir():
    """Delete the temporary directory and its contents."""

    try:
        temp_dir, exists = get_temp_dir()
        if exists:
            rmtree(temp_dir)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"An error occurred while deleting the temp dir: {e}")


def create_new_temp_dir() -> Path:
    """Create a new temporary directory for testing.

    It deletes the temporal folder if it already exists.
    """

    try:
        delete_temp_dir()
        create_temp_dir()
        temp_dir, _ = get_temp_dir()

        return temp_dir
    except Exception as ex:
        print(f"An error ocurred: {ex}")
        raise ex


def delete_files(*args):
    for file_path in args:
        file_path = Path(file_path).resolve()

        if not file_path.exists():
            print(f"File '{file_path.name}' does not exist.")
            continue

        try:
            if file_path.is_file():
                file_path.unlink()
                print(f"File '{file_path.name}' deleted successfully.")
            else:
                print(f"'{file_path.name}' is not a file.")
                continue

        except Exception as e:
            print(f"An error occurred while deleting '{file_path}': {e}")
