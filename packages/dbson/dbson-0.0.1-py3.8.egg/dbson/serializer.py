from typing import Union, List, Dict, Sized
from typing import BinaryIO
from io import BytesIO
import struct


Serializable = Union[int, float, str,
                     List['Serializable'],
                     Dict['Serializable', 'Serializable'],
                     bool, None]


def serialize(x: Serializable,
              buffer: Union[BinaryIO, None] = None) -> Union[bytes, None]:
    serializers = {
        int: serialize_int,
        float: serialize_float,
        str: serialize_str,
        list: serialize_list,
        dict: serialize_dict,
        bool: serialize_bool,
        type(None): serialize_none
    }

    if type(x) not in serializers:
        raise TypeError(f'type {type(x)} is not serializable')

    if buffer is None:
        buffer = BytesIO()
        serializers[type(x)](x, buffer)
        return buffer.read(-1)
    else:
        serializers[type(x)](x, buffer)


def serialize_int(x: int, buffer: BinaryIO):
    buffer.write(b'i' + x.to_bytes(4, byteorder='big'))


def serialize_float(x: float, buffer: BinaryIO):
    buffer.write(b'r' + struct.pack('>d', x))


def serialize_len(obj: Sized, buffer: BinaryIO):
    l_bytes = len(obj).to_bytes(8, byteorder='big')
    if not any(l_bytes[:7]):
        l_bytes = l_bytes[-1:]
    elif not any(l_bytes[:6]):
        l_bytes = l_bytes[-2:]
    elif not any(l_bytes[:4]):
        l_bytes = l_bytes[-4:]
    buffer.write(bytes([len(l_bytes)]) + l_bytes)


def serialize_str(s: str, buffer: BinaryIO):
    str_bytes = bytes(s, 'utf-8')
    buffer.write(b's')
    serialize_len(str_bytes, buffer)
    buffer.write(str_bytes)


def serialize_array(lst: List[Serializable], buffer: BinaryIO):
    buffer.write(b'a')
    serialize_len(lst, buffer)
    for el in lst:
        serialize(el, buffer)


serialize_list = serialize_array


def serialize_assoc(assoc: Dict[Serializable, Serializable],
                    buffer: BinaryIO):
    buffer.write(b'o')
    serialize_len(assoc, buffer)
    assoc_list = assoc.items()
    try:
        assoc_list = sorted(assoc_list)
    except TypeError:
        # cannot sort, several types of keys
        pass
    for key, value in assoc_list:
        serialize(key, buffer)
        serialize(value, buffer)


serialize_dict = serialize_assoc


def serialize_bool(x: bool, buffer: BinaryIO):
    buffer.write(b't' if x else b'f')


def serialize_none(_: type(None), buffer: BinaryIO):
    buffer.write(b'n')
