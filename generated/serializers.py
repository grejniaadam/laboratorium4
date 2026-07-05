from __future__ import annotations
import struct

def _write_uint8(v):
    return struct.pack('<B', v)

def _read_uint8(b, offset):
    return struct.unpack_from('<B', b, offset)[0], offset+1

def _write_int32(v):
    return struct.pack('<i', v)

def _read_int32(b, offset):
    return struct.unpack_from('<i', b, offset)[0], offset+4

def _write_uint32(v):
    return struct.pack('<I', v)

def _read_uint32(b, offset):
    return struct.unpack_from('<I', b, offset)[0], offset+4

def _write_float64(v):
    return struct.pack('<d', v)

def _read_float64(b, offset):
    return struct.unpack_from('<d', b, offset)[0], offset+8

def _write_string(s: str):
    data = s.encode('utf-8')
    return _write_uint32(len(data)) + data

def _read_string(b, offset):
    length, offset = _read_uint32(b, offset)
    s = b[offset:offset+length].decode('utf-8')
    return s, offset+length

def _write_array(items_bytes_list):
    out = _write_uint32(len(items_bytes_list))
    for it in items_bytes_list:
        out += it
    return out

def _read_array(b, offset, item_reader):
    length, offset = _read_uint32(b, offset)
    items = []
    for _ in range(length):
        item, offset = item_reader(b, offset)
        items.append(item)
    return items, offset

class Person:
    def __init__(self, id: int = None, name: str = None, age: int = None):
        self.id = id
        self.name = name
        self.age = age

    def serialize(self) -> bytes:
        parts = []
        parts.append(_write_int32(self.id or 0))
        parts.append(_write_string(self.name or ''))
        parts.append(_write_uint8(self.age or 0))
        return b''.join(parts)

    @classmethod
    def deserialize(cls, b: bytes, offset: int = 0):
        obj = cls()
        obj.id, offset = _read_int32(b, offset)
        obj.name, offset = _read_string(b, offset)
        obj.age, offset = _read_uint8(b, offset)
        return obj, offset

class Message:
    def __init__(self, sender: Person = None, text: str = None):
        self.sender = sender
        self.text = text

    def serialize(self) -> bytes:
        parts = []
        parts.append(self.sender.serialize() if self.sender is not None else b'')
        parts.append(_write_string(self.text or ''))
        return b''.join(parts)

    @classmethod
    def deserialize(cls, b: bytes, offset: int = 0):
        obj = cls()
        obj.sender, offset = Person.deserialize(b, offset)
        obj.text, offset = _read_string(b, offset)
        return obj, offset
