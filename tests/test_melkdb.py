import bupytest

from melkdb import crypto
from melkdb import exceptions


class TestCryptography(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.crypto_key = 'secret-key'
        self.false_crypto_key = 'false-secret-key'
        self.crypto = crypto.Cryptography(self.crypto_key)
        self.second_crypto = crypto.Cryptography(self.false_crypto_key)

    def test_cryptography(self):
        data = b'Hello, world!'

        encrypted = self.crypto.encrypt(data)
        decrypted = self.crypto.decrypt(encrypted)

        self.assert_expected(decrypted, data, message='"decrypted" is not equal to original')

    def test_decrypt_with_different_key(self):
        data = b'Hello, world!'

        encrypted = self.crypto.encrypt(data)
        
        try:
            decrypted = self.second_crypto.decrypt(encrypted)
        except exceptions.DecryptFailed:
            self.assert_true(True)
        else:
            self.assert_true(False, message='Expected exception not raised')


if __name__ == '__main__':
    bupytest.this()
