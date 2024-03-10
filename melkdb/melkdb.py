import os
import struct

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

        print(self._create_item('Jaedson'))

    @staticmethod
    def _create_item(value: str) -> bytes:
        vlen = len(value)
        item = struct.pack(f'h {vlen}s', vlen, value.encode())
        return item
