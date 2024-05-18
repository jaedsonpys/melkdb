import os
from typing import Union, List


class Block:
    def __init__(self, database_path: str) -> None:
        """Create a instance of Block class

        In MelkDB, a block is a path of directories that
        are organized in sequence according to the
        specified key. The first part of the block is
        created using the length of the key, the second
        part is created using the first letter of the key,
        and the last part is created using the last
        letter of the key.

        With this, we have an optimized path to facilitate
        the search for items in the database.

        :param database_path: Database path
        :type database_path: str
        """

        self._db_path = database_path

    def get_tree_path(self, key_parts: List[str]) -> str:
        """Mount complex key block.

        A complex key is multiples keys separated
        by slash. Example: "user/name"

        :param key_parts: Splited key list
        :type key_parts: List[str]
        :return: Block path
        :rtype: str
        """

        tree_key_path = None

        for kp in key_parts:
            key_path = self.get_path(kp, tree_key_path)
            tree_key_path = os.path.join(key_path, kp)

        return tree_key_path

    def get_path(self, key: str, previous_path: Union[None, str] = None) -> str:
        """Mount key block.

        :param key: Item key
        :type key: str
        :return: Block path
        :rtype: str
        """

        base_path = self._db_path

        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]

        if previous_path:
            base_path = previous_path

        return os.path.join(base_path, klen, first_letter, last_letter)

    def make_path(self, key: str, previous_path: Union[None, str] = None) -> str:
        """Create a block.

        :param key: Item path
        :type key: str
        :return: Block path
        :rtype: str
        """

        klen = str(len(key))
        first_letter = key[0]
        last_letter = key[-1]

        base_path = self._db_path

        if previous_path:
            base_path = previous_path

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
