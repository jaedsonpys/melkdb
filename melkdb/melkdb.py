import os
import json
import struct

from typing import Union
from pathlib import Path

from .exceptions import *
from .__init__ import __version__

HOME_PATH = Path().home()
MELKDB_STORAGE_PATH = os.path.join(HOME_PATH, '.melkdb.databases')

INT_TYPE = -1
FLOAT_TYPE = -2
BOOL_TYPE = -3

if not os.path.isdir(MELKDB_STORAGE_PATH):
    os.mkdir(MELKDB_STORAGE_PATH)


class MelkDB:
    def __init__(self, name: str):
        self._db_path = os.path.join(MELKDB_STORAGE_PATH, name)
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


    @staticmethod
    def _create_item(value: Union[str, int, float, bool]) -> bytes:
        if isinstance(value, str):
            vlen = len(value)
            pack_fmt = f'{vlen}s'
            value = value.encode()
        elif isinstance(value, int):
            vlen = INT_TYPE
            pack_fmt = 'i'
        elif isinstance(value, float):
            vlen = FLOAT_TYPE
            pack_fmt = 'f'
        elif isinstance(value, bool):
            vlen = BOOL_TYPE
            pack_fmt = '?'
        else:
            raise ValueNotSupportedError(f'type {type(value)} is not supported')

        item = struct.pack(f'<h{pack_fmt}', vlen, value)
        return item

    def _map_key(self, key: str, previous_path: Union[str, None] = None) -> str:
        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]

        base_path = self._db_path

        if previous_path:
            base_path = previous_path

        return os.path.join(base_path, klen, first_letter, last_letter)

    def _prepare_block(self, key: str,
                       previous_key: Union[None, str] = None) -> str:
        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]

        base_path = self._db_path

        if previous_key:
            base_path = previous_key

        first_box_path = os.path.join(base_path, klen)

        if not os.path.isdir(first_box_path):
            os.mkdir(first_box_path)

        second_box_path = os.path.join(first_box_path, first_letter)

        if not os.path.isdir(second_box_path):
            os.mkdir(second_box_path)

        third_box_path = os.path.join(second_box_path, last_letter)

        if not os.path.isdir(third_box_path):
            os.mkdir(third_box_path)

        return third_box_path

    def add(self, path: str, value: Union[dict, str, int, float, bool]) -> None:
        if not isinstance(path, str):
            raise KeyIsNotAStringError('The path must be a string')

        key_list = path.split('/')
        prev_path = None

        for key in key_list:
            prev_path = self._prepare_block(key, prev_path)

        if isinstance(value, dict):
            for k, v in value.items():
                new_path = '/'.join((path, k))
                self.add(new_path, v)
        else:
            data_path = os.path.join(prev_path, key_list[-1])
            item = self._create_item(value)

            with open(data_path, 'wb') as f:
                f.write(item)

    def get(self, path: str) -> Union[None, str]:
        if not isinstance(path, str):
            raise KeyIsNotAStringError('The path must be a string')

        key_list = path.split('/')
        prev_path = None

        for key in key_list:
            if prev_path:
                key_path = self._map_key(key, previous_path=prev_path)
            else:
                key_path = self._map_key(key)

            prev_path = key_path
        
        data_file_path = os.path.join(prev_path, key_list[-1])

        if not os.path.isfile(data_file_path):
            return None

        with open(data_file_path, 'rb') as f:
            vlen, = struct.unpack('h', f.read(2))

            if vlen == INT_TYPE:
                fmt = 'i'
                rsize = 4
            elif vlen == FLOAT_TYPE:
                fmt = 'f'
                rsize = 4
            elif vlen == BOOL_TYPE:
                fmt = '?'
                rsize = 1
            else:
                fmt = f'{vlen}s'
                rsize = vlen

            value, = struct.unpack(f'<{fmt}', f.read(rsize))

            if isinstance(value, bytes):
                value = value.decode()

        return value
