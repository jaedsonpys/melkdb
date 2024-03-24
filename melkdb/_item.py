import struct
from typing import Union
from io import BufferedReader, BytesIO

from .crypto import Cryptography
from .exceptions import *

INT_TYPE = -1
FLOAT_TYPE = -2
BOOL_TYPE = -3


class Item:
    def __init__(self, crypto: Union[Cryptography, None] = None) -> None:
        """Create a instance of Item class.

        :param crypto: Cryptography class instance, defaults to None
        :type crypto: Union[Cryptography, None], optional
        """

        self._crypto = crypto

    def encode(self, value: Union[str, int, float, bool]) -> bytes:
        """Encode item value.

        The format of pure data encoding is: two bytes
        to store the size of the value and a fixed or
        dynamic size of bytes to store the value.

        Value will be encrypted if cryptography is enabled.

        :param value: Item value
        :type value: Union[str, int, float, bool]
        :raises ValueNotSupportedError: If value is not supported
        :return: Encoded value
        :rtype: bytes
        """

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

        if self._crypto:
            item = self._crypto.encrypt(item)

        return item

    def decode(self, buf_reader: BufferedReader) -> Union[str, int, float, bool]:
        """Decode a item value from file.

        Value will be decrypted if cryptography is enabled.

        :param buf_reader: File buffered reader
        :type buf_reader: BufferedReader
        :return: Decoded value
        :rtype: Union[str, int, float, bool]
        """

        if self._crypto:
            buf_reader = self._crypto.decrypt(buf_reader.read())
            buf_reader = BytesIO(buf_reader)

        vlen, = struct.unpack('h', buf_reader.read(2))

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

        value, = struct.unpack(f'<{fmt}', buf_reader.read(rsize))

        if isinstance(value, bytes):
            value = value.decode()

        return value
