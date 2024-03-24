import os
import json

from typing import Union
from pathlib import Path

from .__version__ import __version__
from .crypto import Cryptography
from .exceptions import *
from ._item import Item
from . import utils

HOME_PATH = Path().home()
MELKDB_STORAGE_PATH = os.path.join(HOME_PATH, '.melkdb.databases')

if not os.path.isdir(MELKDB_STORAGE_PATH):
    os.mkdir(MELKDB_STORAGE_PATH)


class MelkDB:
    def __init__(self, name: str, encrypt_key: Union[None, str] = None):
        """Create a instance of MelkDB class.

        A database with the specified name will be
        created if not exists.

        To encrypt data, you must be pass a strong key
        to `encrypt_key` parameter. Weak encrypt keys
        are a potential risk to the database.

        :param name: Database name
        :type name: str
        :param encrypt_key: Encrypt key , defaults to None
        :type encrypt_key: Union[None, str], optional
        :raises IncompatibleDatabaseError: If database version not
        match with current MelkDB version.
        """

        self._db_path = os.path.join(MELKDB_STORAGE_PATH, name)
        crypto = None

        if encrypt_key:
            crypto = Cryptography(encrypt_key)

        self._item = Item(crypto)
        db_config_path = os.path.join(self._db_path, 'config.json')
        
        if not os.path.isdir(self._db_path):
            os.mkdir(self._db_path)

            with open(db_config_path, 'w') as f:
                json.dump({'version': __version__}, f)
        else:
            with open(db_config_path, 'rb') as f:
                config = json.load(f)

            db_version = config['version']

            current_major_v = __version__.split('.')[0]
            db_major_v = db_version.split('.')[0]

            if current_major_v != db_major_v:
                raise IncompatibleDatabaseError(f'Database created with {db_major_v}.x.x'
                                                 'MelkDB version')

    def _map_key(self, key: str) -> str:
        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]
        return os.path.join(self._db_path, klen, first_letter, last_letter)

    def _prepare_block(self, key: str) -> str:
        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]

        first_box_path = os.path.join(self._db_path, klen)

        if not os.path.isdir(first_box_path):
            os.mkdir(first_box_path)

        second_box_path = os.path.join(first_box_path, first_letter)

        if not os.path.isdir(second_box_path):
            os.mkdir(second_box_path)

        third_box_path = os.path.join(second_box_path, last_letter)

        if not os.path.isdir(third_box_path):
            os.mkdir(third_box_path)

        return third_box_path

    def add(self, key: str, value: Union[str, int, float, bool]) -> None:
        """Add a item to database.

        :param key: Item key
        :type key: str
        :param value: Item value
        :type value: Union[str, int, float, bool]
        :raises KeyIsNotAStringError: If key is not string
        :raises InvalidCharInKeyError: If key has a invalid char
        """

        if not isinstance(key, str):
            raise KeyIsNotAStringError('The key must be a string')

        if not utils.key_is_valid(key):
            raise InvalidCharInKeyError(f'Key {repr(key)} is not valid')

        block_path = self._prepare_block(key)
        data_path = os.path.join(block_path, key)
        item = self._item.encode(value)

        with open(data_path, 'wb') as f:
            f.write(item)

    def get(self, key: str) -> Union[None, str, int, float, bool]:
        """Get a item from database

        :param key: Item key
        :type key: str
        :raises KeyIsNotAStringError: If key is not a string
        :raises InvalidCharInKeyError: If key has a invalid char
        :return: Returns the item value
        :rtype: Union[None, str, int, float, bool]
        """

        if not isinstance(key, str):
            raise KeyIsNotAStringError('The key must be a string')
        
        if not utils.key_is_valid(key):
            raise InvalidCharInKeyError(f'Key {repr(key)} is not valid')

        key_path = self._map_key(key)
        data_file_path = os.path.join(key_path, key)

        if os.path.isfile(data_file_path):
            with open(data_file_path, 'rb') as f:
                value = self._item.decode(f)

            return value

    def delete(self, key: str) -> None:
        """Delete a item from database

        A exception must be raised if item
        not exists in database.

        :param key: Item key
        :type key: str
        :raises KeyIsNotAStringError: If key is not a string
        :raises InvalidCharInKeyError: If key has a invalid char
        :raises ItemNotExistsError: If item not exists
        """
        
        if not isinstance(key, str):
            raise KeyIsNotAStringError('The key must be a string')
        
        if not utils.key_is_valid(key):
            raise InvalidCharInKeyError(f'Key {repr(key)} is not valid')

        key_path = self._map_key(key)
        data_file_path = os.path.join(key_path, key)

        if os.path.isfile(data_file_path):
            os.remove(data_file_path)
        else:
            raise ItemNotExistsError(f'Item {repr(key)} not exists')

    def update(self, key: str, value: Union[str, int, float, bool]) -> None:
        """Update a item in database.

        This method is just a shortcut to use
        `delete()` and `add()` methods.

        A exception will be raised if key not 
        exists in database.

        :param key: Item key
        :type key: str
        :param value: Item value
        :type value: Union[str, int, float, bool]
        """

        self.delete(key)
        self.add(key, value)
