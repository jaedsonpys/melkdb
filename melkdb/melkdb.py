import os
import json

from typing import Union
from pathlib import Path

from .__version__ import __version__
from .crypto import Cryptography
from .exceptions import *
from ._block import Block
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
        self._block = Block(self._db_path)

        db_config_path = os.path.join(self._db_path, 'config.json')
        
        if not os.path.isdir(self._db_path):
            os.mkdir(self._db_path)

            with open(db_config_path, 'w') as f:
                if crypto:
                    is_crypto = True
                else:
                    is_crypto = False

                config = {'version': __version__, 'iscrypto': is_crypto}
                json.dump(config, f)
        else:
            with open(db_config_path, 'rb') as f:
                config = json.load(f)

            db_version = config['version']
            db_crypto = config['iscrypto']

            if db_crypto and not encrypt_key:
                raise EncryptKeyRequiredError(f'{repr(name)} requires cryptography')
            elif not db_crypto and encrypt_key:
                raise DatabaseNotEncryptedError(f'{repr(name)} is created without cryptography')

            current_major_v = __version__.split('.')[0]
            db_major_v = db_version.split('.')[0]

            if current_major_v != db_major_v:
                raise IncompatibleDatabaseError(f'{repr(name)} created with {db_major_v}.x.x'
                                                 'MelkDB version')

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

        block_path = self._block.make_path(key)
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

        key_path = self._block.get_path(key)
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

        key_path = self._block.get_path(key)
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
