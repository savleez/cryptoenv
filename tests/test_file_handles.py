import os
import shutil
import unittest
from configparser import ConfigParser
from pathlib import Path

from cryptography.fernet import Fernet

from cryptoenv.webapp import Encryptor, Configuration


class TestConfiguration(unittest.TestCase):
    """Unit tests for the Configuration class."""

    def create_temp_dir(self):
        """Create a temporary directory for testing."""

        self.temp_dir = Path("temp_test_dir")
        self.delete_temp_dir() if self.temp_dir.exists() else None
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def delete_temp_dir(self):
        """Delete the temporary directory and its contents."""

        shutil.rmtree(self.temp_dir)

    def setUp(self):
        """Set up the test environment."""

        self.create_temp_dir()
        self.config_file_path = self.temp_dir / "config"

    def tearDown(self):
        """Clean up the test environment."""

        self.delete_temp_dir()

    def test_create_default_config(self):
        """Test the creation of a default configuration file."""

        Configuration.create_default_config_file(
            config_file_path=self.config_file_path.resolve(),
            encrypted_files_dir=self.temp_dir.resolve(),
        )

        self.assertTrue(self.config_file_path.exists())


class TestEncryptor(unittest.TestCase):
    """Unit tests for the Encryptor class."""

    def create_temp_dir(self):
        """Create a temporary directory for testing."""

        self.temp_dir = Path("temp_test_dir")
        self.delete_temp_dir() if self.temp_dir.exists() else None
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def delete_temp_dir(self):
        """Delete the temporary directory and its contents."""

        shutil.rmtree(self.temp_dir)

    def setUp(self):
        """Set up the test environment."""

        self.create_temp_dir()
        self.config_file_path = self.temp_dir / "config"

        Configuration.create_default_config_file(
            config_file_path=self.config_file_path.resolve(),
            encrypted_files_dir=self.temp_dir.resolve(),
        )

        self.password = "test_password"
        self.content = "This is a test content."
        self.file_name = "test_file.txt"

    def tearDown(self):
        """Clean up the test environment."""

        self.delete_temp_dir()

    def test_create_encrypted_file(self):
        """Test the creation of an encrypted file."""

        encryptor = Encryptor(
            password=self.password,
            encrypted_files_dir=self.temp_dir,
        )
        encryptor.create_encrypted_file(
            content=self.content,
            file=self.file_name,
        )

        encrypted_file_path = self.temp_dir / (
            Path(self.file_name).with_suffix(".encrypted")
        )
        self.assertTrue(encrypted_file_path.exists())

    def test_create_already_existing_encrypted_file(self):
        """Test the creation of an encrypted file when it already exists."""

        encryptor = Encryptor(
            password=self.password,
            encrypted_files_dir=self.temp_dir,
        )
        encryptor.create_encrypted_file(
            content=self.content,
            file=self.file_name,
        )

        encrypted_file_path = self.temp_dir / (
            Path(self.file_name).with_suffix(".encrypted")
        )
        self.assertTrue(encrypted_file_path.exists())

    def test_read_encrypted_file(self):
        """Test reading an encrypted file."""

        encryptor = Encryptor(
            password=self.password,
            encrypted_files_dir=self.temp_dir,
        )
        encryptor.create_encrypted_file(
            content=self.content,
            file=self.file_name,
        )

        decrypted_content = encryptor.read_encrypted_file(file=self.file_name)

        self.assertEqual(decrypted_content, self.content)

    def test_read_non_existing_encrypted_file(self):
        """Test reading a non-existing encrypted file."""

        encryptor = Encryptor(
            password=self.password,
            encrypted_files_dir=self.temp_dir,
        )

        with self.assertRaises(expected_exception=ValueError):
            decrypted_content = encryptor.read_encrypted_file(file=self.file_name)

    def test_get_encrypted_file(self):
        """Test getting the path of an encrypted file."""

        encryptor = Encryptor(
            password=self.password,
            encrypted_files_dir=self.temp_dir,
        )
        encryptor.create_encrypted_file(
            content=self.content,
            file=self.file_name,
        )

        encrypted_file_path, _ = encryptor.get_encrypted_file(file=self.file_name)

        expected_path = str(
            self.temp_dir / Path(self.file_name).with_suffix(".encrypted")
        )

        self.assertEqual(encrypted_file_path, expected_path)


if __name__ == "__main__":
    unittest.main()
