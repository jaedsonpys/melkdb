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

    def add(self, key: str, value: str) -> None:
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

        data_path = os.path.join(third_box_path, 'data.melkdb')
        item = self._create_item(value)

        with open(data_path, 'wb') as f:
            f.write(item)
