import unittest

from cryptoenv import Configs
from .utils import delete_temp_dir, create_new_temp_dir, delete_files


class TestConfiguration(unittest.TestCase):
    """Unit tests for the Configuration class."""

    def setUp(self):
        """Set up the test environment."""

        self.temp_dir = create_new_temp_dir()
        self.config_file_path, _ = Configs.get_config_file_path()

    def tearDown(self):
        """Clean up the test environment."""

        delete_temp_dir()

        if self.config_file_path.exists():
            delete_files(self.config_file_path)

    def test_create_default_config(self):
        """Test the creation of a default configuration file."""

        Configs.create_default_config_file()

        self.assertTrue(self.config_file_path.exists())
