import os
import struct

from typing import Union
from pathlib import Path

HOME_PATH = Path().home()
MELKDB_STORAGE_PATH = os.path.join(HOME_PATH, '.melkdb.databases')

if not os.path.isdir(MELKDB_STORAGE_PATH):
    os.mkdir(MELKDB_STORAGE_PATH)


class MelkDB:
    def __init__(self, name: str):
        self._db_path = os.path.join(MELKDB_STORAGE_PATH, name)
        
        if not os.path.isdir(self._db_path):
            os.mkdir(self._db_path)

    @staticmethod
    def _create_item(value: str) -> bytes:
        vlen = len(value)
        item = struct.pack(f'h {vlen}s', vlen, value.encode())
        return item

    def _map_key(self, key: str, previous_path: Union[str, None] = None) -> str:
        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]

        base_path = self._db_path

        if previous_path:
            base_path = previous_path

        return os.path.join(base_path, klen, first_letter, last_letter)

    def add(self, path: str, value: str) -> None:
        key_list = path.split('/')
        prev_path = None

        for key in key_list:
            klen = str(len(key))
            first_letter = key[0]
            last_letter = key[-1]

            base_path = self._db_path

            if prev_path:
                base_path = prev_path

            first_box_path = os.path.join(base_path, klen)

            if not os.path.isdir(first_box_path):
                os.mkdir(first_box_path)

            second_box_path = os.path.join(first_box_path, first_letter)

            if not os.path.isdir(second_box_path):
                os.mkdir(second_box_path)

            third_box_path = os.path.join(second_box_path, last_letter)
            prev_path = third_box_path

            if not os.path.isdir(third_box_path):
                os.mkdir(third_box_path)

        if isinstance(value, dict):
            for k, v in value.items():
                new_path = '/'.join((path, k))
                self.add(new_path, v)
        else:
            data_path = os.path.join(third_box_path, 'data.melkdb')
            item = self._create_item(value)

            with open(data_path, 'wb') as f:
                f.write(item)

    def get(self, path: str) -> Union[None, str]:
        key_list = path.split('/')
        prev_path = None

        for key in key_list:
            if prev_path:
                key_path = self._map_key(key, previous_path=prev_path)
            else:
                key_path = self._map_key(key)

            prev_path = key_path
        
        data_file_path = os.path.join(prev_path, 'data.melkdb')

        if not os.path.isfile(data_file_path):
            return None

        with open(data_file_path, 'rb') as f:
            vlen, = struct.unpack('h', f.read(2))
            value, = struct.unpack(f'{vlen}s', f.read(vlen))

        return value.decode()
