import struct
from typing import BinaryIO
from dbson.serializer import Serializable


def deserialize(s: BinaryIO) -> Serializable:
    deserializers = {
        b'i': deserialize_int,
        b'r': deserialize_float,
        b's': deserialize_str,
        b'a': deserialize_array,
        b'o': deserialize_assoc,
        b't': lambda _: True,
        b'f': lambda _: False,
        b'n': lambda _: None
    }

    prefix = read_exact(s, 1)
    if prefix not in deserializers:
        raise ValueError(f"prefix 0x{prefix.hex()} not found")

    return deserializers[prefix](s)


def read_exact(s: BinaryIO, n: int) -> bytes:
    buffer = b''
    while len(buffer) < n:
        new_bytes = s.read(n - len(buffer))
        if len(new_bytes) == 0:
            raise EOFError
        buffer += new_bytes
    return buffer


def deserialize_int(s: BinaryIO) -> int:
    return int.from_bytes(read_exact(s, 4), byteorder='big')


def deserialize_float(s: BinaryIO) -> float:
    return struct.unpack('>d', read_exact(s, 8))[0]


def deserialize_len(s: BinaryIO) -> int:
    length_size: int = read_exact(s, 1)[0]
    length_bytes = read_exact(s, length_size)
    return int.from_bytes(length_bytes, byteorder='big')


def deserialize_str(s: BinaryIO) -> str:
    length = deserialize_len(s)
    return read_exact(s, length).decode('utf-8')


def deserialize_array(s: BinaryIO) -> list:
    length = deserialize_len(s)
    arr = []
    for i in range(length):
        arr.append(deserialize(s))
    return arr


deserialize_list = deserialize_array


def deserialize_assoc(s: BinaryIO) -> dict:
    length = deserialize_len(s)
    assoc = {}
    for i in range(length):
        key = deserialize(s)
        value = deserialize(s)
        assoc[key] = value
    return assoc


deserialize_dict = deserialize_assoc
