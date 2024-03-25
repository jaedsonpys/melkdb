import struct
from io import BytesIO

import bupytest

from melkdb import crypto
from melkdb import melkdb
from melkdb import _item
from melkdb import exceptions

INT_TYPE = -1
FLOAT_TYPE = -2
BOOL_TYPE = -3


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


class TestItem(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.item_handle = _item.Item()

    def test_encode(self):
        data = 'MelkDB'
        data_len = len(data)

        encoded = self.item_handle.encode(data)
        item_io = BytesIO(encoded)

        enc_data_len, = struct.unpack('<h', item_io.read(2))
        enc_data, = struct.unpack(f'<{enc_data_len}s', item_io.read(enc_data_len))

        self.assert_expected(enc_data_len, data_len, message='Invalid data length')
        self.assert_expected(enc_data.decode(), data, message='Invalid encoded data')

    def test_decode(self):
        encoded = self.item_handle.encode('MelkDB')
        decoded = self.item_handle.decode(BytesIO(encoded))
        self.assert_expected(decoded, 'MelkDB', message='Invalid decoded data')


class TestMelkDBEncrypted(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.db = melkdb.MelkDB('cache', encrypt_key='thisisanotsecurekey')
    
    def test_add(self):
        self.db.add('latest_user_online', 'Melk')
        self.db.add('latest_user_added', 'Jaedson')
    
    def test_get(self):
        data = self.db.get('latest_user_online')
        self.assert_expected(data, 'Melk', message='Data is not equal to original')
    
    def test_update(self):
        self.db.update('latest_user_online', 'Jaedson')
        new_data = self.db.get('latest_user_online')
        self.assert_expected(new_data, 'Jaedson', message='Data not updated in database')
    
    def test_delete(self):
        self.db.delete('latest_user_online')
        deleted_data = self.db.get('latest_user_online')
        self.assert_expected(deleted_data, None, message='Data not deleted from database')

    def test_check_secundary_item(self):
        data = self.db.get('latest_user_added')
        self.assert_expected(data, 'Jaedson', message='Secundary item modified')


if __name__ == '__main__':
    bupytest.this()
