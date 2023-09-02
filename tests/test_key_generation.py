import unittest
from unittest.mock import patch

from cryptoenv import KeyManager


class TestKeyManager(unittest.TestCase):
    @patch("os.getenv")
    def setUp(self, mock_getenv) -> None:
        self.key_manager = KeyManager(pepper="TEST_PEPPER")

        mock_getenv.side_effect = lambda x, default: {
            "PEPPER": "TEST_PEPPER",
            "USER": "testuser",
        }.get(x, default)

    def test_generate_salt(self):
        """Test the generation of a salt using test environment variables."""

        expected_salt = (
            "b6fd0fafb1abcb3e25ef507d8fcb840732eaba49cacfa03afc3d3110af5f51c5"
        )

        actual_salt = self.key_manager.generate_salt()
        self.assertEqual(actual_salt, expected_salt)

    def test_generate_key(self):
        """Test the generation of a key using a test password and environment variables."""

        test_password = "test_password"

        # Pre-Generated key created using a test pepper and user environment variables
        expected_key = "YhaohQ7IhEEAJrPYrw3y9gwVgPWeGXD5Ot6Sj6Y10AE="

        actual_key = self.key_manager.generate_key(test_password)
        self.assertEqual(actual_key, expected_key)

    def test_generate_same_salt(self):
        """Test that two instances of KeyManager with the same pepper generate the same salt."""

        key_manager1 = KeyManager(pepper="TEST_PEPPER")
        key_manager2 = KeyManager(pepper="TEST_PEPPER")

        salt1 = key_manager1.generate_salt()
        salt2 = key_manager2.generate_salt()

        self.assertEqual(salt1, salt2)

    def test_generate_unique_salt(self):
        """Test that two instances of KeyManager with different pepper values generate different salts."""

        key_manager1 = KeyManager(pepper="PEPPER")
        salt1 = key_manager1.generate_salt()

        with patch.dict("os.environ", {"PEPPER": "TEST_PEPPER_2"}):
            key_manager2 = KeyManager(pepper="PEPPER")
            salt2 = key_manager2.generate_salt()

        self.assertNotEqual(salt1, salt2)

    def test_generate_key_with_different_passwords(self):
        """Test that generating keys with different passwords results in different keys."""

        password1 = "password1"
        password2 = "password2"

        key1 = self.key_manager.generate_key(password1)
        key2 = self.key_manager.generate_key(password2)

        self.assertNotEqual(key1, key2)


if __name__ == "__main__":
    unittest.main()
