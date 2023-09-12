import os
import shutil
import unittest
from configparser import ConfigParser
from pathlib import Path
from json import loads as json_loads

from cryptography.fernet import InvalidToken

from cryptoenv import Crypto, ConfigHandler, Configs
from .utils import delete_temp_dir, create_new_temp_dir, delete_files


class TestCrypto(unittest.TestCase):
    """Unit tests for the Encryptor class."""

    def delete_all_encrypted_files(self):
        delete_files(
            *[
                str(enc_file)
                for enc_file in Configs.encrypted_files_dir.glob("*.encrypted")
            ]
        )

    def setUp(self):
        """Set up the test environment."""

        self.password = "test_password"
        self.content = "This is a test content."

        self.temp_dir = create_new_temp_dir()
        (
            self.config_file_path,
            self.config_file_exists,
        ) = Configs.get_config_file_path()

        self.delete_all_encrypted_files()

    def tearDown(self):
        """Clean up the test environment."""

        delete_temp_dir()

        if self.config_file_exists:
            delete_files(self.config_file_path)

        self.delete_all_encrypted_files()

    def test_encrypt_string(self):
        crypto = Crypto(password=self.password)

        encrypted_content = crypto.encrypt(self.content)

        self.assertIsInstance(encrypted_content, str)

    def test_encrypt_with_same_password(self):
        """Generate different encrypted content using the same password."""

        crypto = Crypto(password=self.password)
        encrypted_content = crypto.encrypt(self.content)

        crypto2 = Crypto(password=self.password)
        encrypted_content2 = crypto2.encrypt(self.content)

        self.assertNotEqual(encrypted_content, encrypted_content2)

    def test_encrypt_with_different_password(self):
        """Generate different encrypted content using the different passwords."""

        crypto = Crypto(password="some-password")
        crypto2 = Crypto(password="some-other-password")

        encrypted_content = crypto.encrypt(self.content)
        encrypted_content2 = crypto2.encrypt(self.content)

        self.assertNotEqual(encrypted_content, encrypted_content2)

    def test_decrypt_string(self):
        crypto = Crypto(password=self.password)

        encrypted_content = crypto.encrypt(self.content)

        decrypted_content = crypto.decrypt(encrypted_content)

        self.assertIsInstance(decrypted_content, str)

    def test_decrypt_with_wrong_password(self):
        """Generate the same decrypted content using different passwords."""

        crypto = Crypto(password="some-password")
        encrypted_content = crypto.encrypt(self.content)

        crypto2 = Crypto(password="some-other-password")

        with self.assertRaises(expected_exception=InvalidToken):
            current_decrypted_content = crypto2.decrypt(encrypted_content)

    def test_decrypt_with_same_password(self):
        """Generate the same decrypted content using the same password."""

        crypto = Crypto(password=self.password)
        encrypted_content = crypto.encrypt(self.content)
        decrypted_content = crypto.decrypt(encrypted_content)

        crypto2 = Crypto(password=self.password)
        encrypted_content2 = crypto2.encrypt(self.content)
        decrypted_content2 = crypto2.decrypt(encrypted_content2)

        self.assertEqual(decrypted_content, decrypted_content2)

    def test_decrypt_with_different_password(self):
        """Generate the same decrypted content using different passwords."""

        crypto = Crypto(password="some-password")
        encrypted_content = crypto.encrypt(self.content)
        decrypted_content = crypto.decrypt(encrypted_content)

        crypto2 = Crypto(password="some-other-password")
        encrypted_content2 = crypto2.encrypt(self.content)
        decrypted_content2 = crypto2.decrypt(encrypted_content2)

        self.assertEqual(decrypted_content, decrypted_content2)

    def test_get_default_non_existing_encrypted_file(self):
        """Exist should return false for a non existing file."""

        crypto = Crypto(password=self.password)
        _, exists = crypto.get_encrypted_file()

        self.assertTrue(not (exists))

    def test_get_custom_non_existing_encrypted_file(self):
        """Exist should return false for a non existing file."""

        encrypted_file_name = "test_encrypted"

        crypto = Crypto(password=self.password)
        _, exists = crypto.get_encrypted_file(file=encrypted_file_name)

        self.assertTrue(not (exists))

    def test_create_default_encrypted_file(self):
        """Test the creation of an encrypted file."""

        crypto = Crypto(password=self.password)
        encrypted_file = crypto.create_encrypted_file(content=self.content)

        self.assertTrue(encrypted_file.exists())

    def test_create_custom_encrypted_file(self):
        """Test the creation of an encrypted file using a custom name."""

        encrypted_file_name = "test_encrypted"

        crypto = Crypto(password=self.password)
        encrypted_file = crypto.create_encrypted_file(
            content=self.content,
            filename=encrypted_file_name,
        )

        self.assertTrue(encrypted_file.exists())

        self.assertEqual(encrypted_file_name, encrypted_file.stem)

    def test_create_already_existing_encrypted_file(self):
        """Test the creation of an encrypted file when it already exists.

        It should overwrite the existing file.
        """

        crypto = Crypto(password=self.password)

        encrypted_file = crypto.create_encrypted_file(content="content1")
        with open(encrypted_file, "r") as f:
            encrypted_content = f.read()

        encrypted_file2 = crypto.create_encrypted_file(content="content2")
        with open(encrypted_file2, "r") as f2:
            encrypted_content2 = f2.read()

        self.assertEqual(encrypted_file, encrypted_file2)

        self.assertNotEqual(encrypted_content, encrypted_content2)

    def test_read_encrypted_file(self):
        """Test reading an encrypted file."""

        crypto = Crypto(password=self.password)

        encrypted_file = crypto.create_encrypted_file(content=self.content)

        decrypted_content = crypto.read_encrypted_file(filename=encrypted_file.name)

        self.assertEqual(decrypted_content, self.content)

    def test_read_non_existing_encrypted_file(self):
        """Test reading a non-existing encrypted file."""

        crypto = Crypto(password=self.password)

        with self.assertRaises(expected_exception=ValueError):
            decrypted_content = crypto.read_encrypted_file()


class TestConfigHandler(unittest.TestCase):
    def test_config_from_string(self):
        """Generate config object from string."""

        config_content = "[GENERAL]\nkey=value"

        config = ConfigHandler(config_content=config_content)

        config_obj = config.get_config_object()

        self.assertIsInstance(config_obj, ConfigParser)

    def test_config_from_dict(self):
        """Generate config object from dict."""

        config_content = {"GENERAL": {"key": "value"}}

        config = ConfigHandler(config_content=config_content)

        config_obj = config.get_config_object()

        self.assertIsInstance(config_obj, ConfigParser)

    def test_config_from_serialized_dict(self):
        """Generate config object from serialized config dict.

        Config content must be a dict because ConfigParser fails to
        parse from serialized dictionaries."""

        config_content = '{"GENERAL": {"key": "value"}}'

        with self.assertRaises(expected_exception=ValueError):
            config = ConfigHandler(config_content=config_content)

    def test_config_from_dict_from_serialized_dict(self):
        """Generate config object from dict generated from config dict
        string.
        """

        config_content = '{"GENERAL": {"key": "value"}}'
        config_content = json_loads(config_content)

        config = ConfigHandler(config_content=config_content)

        config_obj = config.get_config_object()

        self.assertIsInstance(config_obj, ConfigParser)

    def test_config_to_dict(self):
        """Convert config to dict."""

        config_content = {"GENERAL": {"key": "value"}}

        config = ConfigHandler(config_content=config_content)

        config_dict = config.config_to_dict()

        self.assertIsInstance(config_dict, dict)

        self.assertEqual(config_content, config_dict)

    def test_serialize_config(self):
        """Serialize config object."""

        config_content = '{"GENERAL": {"key": "value"}}'

        config_content_dict = json_loads(config_content)

        config = ConfigHandler(config_content=config_content_dict)

        serialized_config = config.serialize_config()

        self.assertIsInstance(serialized_config, str)

        self.assertEqual(serialized_config, config_content)
