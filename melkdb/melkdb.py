import os
from pathlib import Path

HOME_PATH = Path().home()
MELKDB_STORAGE_PATH = os.path.join(HOME_PATH, '.melkdb.databases')

if not os.path.isdir(MELKDB_STORAGE_PATH):
    os.mkdir(MELKDB_STORAGE_PATH)
