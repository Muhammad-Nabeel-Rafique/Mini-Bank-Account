import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from cryptography.fernet import InvalidToken

from Digiskills_bank_limited import (
    capture_security_image,
    _decrypt_security_image,
    _encrypt_security_image,
    _save_security_image,
    main,
)


class SecurityImageEncryptionTests(unittest.TestCase):
    def test_encrypted_image_round_trips_with_account_password(self):
        image_data = b"sample image bytes"

        encrypted = _encrypt_security_image(image_data, "Strong!Password1")

        self.assertNotIn(image_data, encrypted)
        self.assertEqual(
            _decrypt_security_image(encrypted, "Strong!Password1"), image_data
        )

    def test_encrypted_image_cannot_be_decrypted_with_wrong_password(self):
        encrypted = _encrypt_security_image(b"sample image bytes", "Strong!Password1")

        with self.assertRaises(InvalidToken):
            _decrypt_security_image(encrypted, "Wrong!Password2")

    def test_saved_image_is_encrypted_in_account_folder(self):
        account = SimpleNamespace(
            account_number="ACC1001", password="Strong!Password1"
        )
        image_data = b"sample image bytes"

        with tempfile.TemporaryDirectory() as storage_root:
            filepath = _save_security_image(account, image_data, storage_root)

            self.assertTrue(os.path.isfile(filepath))
            self.assertEqual(os.path.basename(os.path.dirname(filepath)), "ACC1001")
            with open(filepath, "rb") as file:
                encrypted = file.read()
            self.assertNotIn(image_data, encrypted)
            self.assertEqual(
                _decrypt_security_image(encrypted, account.password), image_data
            )

    def test_camera_capture_saves_an_encrypted_image(self):
        account = SimpleNamespace(
            account_number="ACC1001", password="Strong!Password1"
        )
        image_data = b"captured image bytes"
        camera = SimpleNamespace(
            isOpened=lambda: True,
            read=lambda: (True, object()),
            release=lambda: None,
        )
        fake_cv2 = SimpleNamespace(
            VideoCapture=lambda _device: camera,
            imencode=lambda _extension, _frame: (
                True,
                SimpleNamespace(tobytes=lambda: image_data),
            ),
            error=RuntimeError,
        )

        with tempfile.TemporaryDirectory() as storage_root:
            save_image = lambda account_arg, data: _save_security_image(
                account_arg, data, storage_root
            )
            with patch.dict("sys.modules", {"cv2": fake_cv2}):
                with patch(
                    "Digiskills_bank_limited._save_security_image",
                    side_effect=save_image,
                ):
                    with redirect_stdout(io.StringIO()):
                        capture_security_image(account)

            account_folder = os.path.join(storage_root, account.account_number)
            filenames = os.listdir(account_folder)
            self.assertEqual(len(filenames), 1)
            with open(os.path.join(account_folder, filenames[0]), "rb") as file:
                encrypted = file.read()
            self.assertNotIn(image_data, encrypted)
            self.assertEqual(
                _decrypt_security_image(encrypted, account.password), image_data
            )

    @patch("Digiskills_bank_limited.capture_security_image")
    def test_failed_login_attempt_triggers_security_capture(self, capture_image):
        user_inputs = iter(
            [
                "1",
                "Alice",
                "Strong!Password1",
                "0",
                "2",
                "ACC1001",
                "Wrong!Password2",
                "3",
            ]
        )

        with redirect_stdout(io.StringIO()):
            with patch("builtins.input", side_effect=lambda _prompt: next(user_inputs)):
                main()

        capture_image.assert_called_once()
        self.assertEqual(capture_image.call_args.args[0].password, "Strong!Password1")


if __name__ == "__main__":
    unittest.main()
