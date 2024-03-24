import os


class Block:
    def __init__(self, database_path: str) -> None:
        self._db_path = database_path

    def get_path(self, key: str) -> str:
        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]
        return os.path.join(self._db_path, klen, first_letter, last_letter)

    def make_path(self, key: str) -> str:
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
