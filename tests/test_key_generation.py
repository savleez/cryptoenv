import unittest
from unittest.mock import patch

from cryptoenv import KeyGenerator


class TestKeyGenerator(unittest.TestCase):
    @patch("os.getenv")
    def setUp(self, mock_getenv) -> None:
        self.key_manager = KeyGenerator(pepper="TEST_PEPPER")

        mock_getenv.side_effect = lambda x, default: {
            "PEPPER": "TEST_PEPPER",
            "USER": "testuser",
        }.get(x, default)

    def test_generate_salt(self):
        """Generate a random salt and confirm result is a string."""

        salt = self.key_manager.generate_salt()
        self.assertIsInstance(salt, str)

    def test_generate_same_salt(self):
        """Generate the same salt using two instances of KeyGenerator
        with the same pepper generate the same salt.
        """

        key_manager1 = KeyGenerator(pepper="TEST_PEPPER")
        key_manager2 = KeyGenerator(pepper="TEST_PEPPER")

        salt1 = key_manager1.generate_salt()
        salt2 = key_manager2.generate_salt()

        self.assertEqual(salt1, salt2)

    def test_generate_different_salt_using_pepper(self):
        """Generate two different salts using two instances of
        KeyGenerator with different pepper values.
        """

        key_manager1 = KeyGenerator(pepper="PEPPER")
        salt1 = key_manager1.generate_salt()

        with patch.dict("os.environ", {"PEPPER": "TEST_PEPPER_2"}):
            key_manager2 = KeyGenerator(pepper="PEPPER")
            salt2 = key_manager2.generate_salt()

        self.assertNotEqual(salt1, salt2)

    def test_generate_different_salt_using_user(self):
        """Generate two different salts using two instances of
        KeyGenerator with different user values.
        """

        key_manager1 = KeyGenerator(pepper="PEPPER")
        salt1 = key_manager1.generate_salt()

        with patch.dict("os.environ", {"USER": "DIFFERENT_USER"}):
            key_manager2 = KeyGenerator(pepper="PEPPER")
            salt2 = key_manager2.generate_salt()

        self.assertNotEqual(salt1, salt2)

    def test_generate_key(self):
        """Generate a key using a generic password."""

        test_password = "test_password"

        key = self.key_manager.generate_key(test_password)
        self.assertIsInstance(key, str)

    def test_generate_key_with_same_passwords(self):
        """Generate keys with the same passwords results in identical
        keys.
        """

        password1 = "password"
        password2 = "password"

        key1 = self.key_manager.generate_key(password1)
        key2 = self.key_manager.generate_key(password2)

        self.assertEqual(key1, key2)

    def test_generate_key_with_different_passwords(self):
        """Generate keys with different passwords results in different
        keys.
        """

        password1 = "password1"
        password2 = "password2"

        key1 = self.key_manager.generate_key(password1)
        key2 = self.key_manager.generate_key(password2)

        self.assertNotEqual(key1, key2)
