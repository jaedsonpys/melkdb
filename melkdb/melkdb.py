import os
from pathlib import Path

HOME_PATH = Path().home()
MELKDB_STORAGE_PATH = os.path.join(HOME_PATH, '.melkdb.databases')
