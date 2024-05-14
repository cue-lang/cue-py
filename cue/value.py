# Copyright 2024 The CUE Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, final
from cue.error import Error
import libcue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cue.context import Context

@final
class Value:
    _ctx: 'Context'
    _val: int

    def __init__(self, ctx: 'Context', v: int):
        self._ctx = ctx
        self._val = v

    def __del__(self):
        libcue.free(self._val)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Value):
            return libcue.is_equal(self._val, other._val)
        return False

    def context(self) -> 'Context':
        return self._ctx

    def unify(self, other: 'Value') -> 'Value':
        v = libcue.unify(self._val, other._val)
        return Value(self._ctx, v)

    def to_int(self) -> int:
        return _to_int(self)

    def to_unsigned(self) -> int:
        return _to_unsigned(self)

    def to_bool(self) -> bool:
        return _to_bool(self)

    def to_float(self) -> float:
        return _to_float(self)

    def to_str(self) -> str:
        return _to_str(self)

    def to_bytes(self) -> bytes:
        return _to_bytes(self)

    def to_json(self) -> str:
        return _to_json(self)

def _to_int(val: Value) -> int:
    ptr = libcue.ffi.new("int64_t*")
    err = libcue.dec_int64(val._val, ptr)
    if err != 0:
        raise Error(err)
    return ptr[0]

def _to_unsigned(val: Value) -> int:
    ptr = libcue.ffi.new("uint64_t*")
    err = libcue.dec_uint64(val._val, ptr)
    if err != 0:
        raise Error(err)
    return ptr[0]

def _to_bool(val: Value) -> bool:
    ptr = libcue.ffi.new("bool*")
    err = libcue.dec_bool(val._val, ptr)
    if err != 0:
        raise Error(err)
    return ptr[0]

def _to_float(val: Value) -> float:
    ptr = libcue.ffi.new("double*")
    err = libcue.dec_double(val._val, ptr)
    if err != 0:
        raise Error(err)
    return ptr[0]

def _to_str(val: Value) -> str:
    ptr = libcue.ffi.new("char**")
    err = libcue.dec_string(val._val, ptr)
    if err != 0:
        raise Error(err)

    dec = libcue.ffi.string(ptr[0])
    if not isinstance(dec, bytes):
        raise TypeError

    s = dec.decode("utf-8")
    libcue.libc_free(ptr[0])
    return s

def _to_bytes(val: Value) -> bytes:
    buf_ptr = libcue.ffi.new("uint8_t**")
    len_ptr = libcue.ffi.new("size_t*")

    err = libcue.dec_bytes(val._val, buf_ptr, len_ptr)
    if err != 0:
        raise Error(err)

    dec = libcue.ffi.buffer(buf_ptr[0], len_ptr[0])

    # we slice the buffer to get a Python bytes instead of converting
    # to bytes directly to work around the lack of precise type information
    # in types-cffi.
    b = dec[:]

    libcue.libc_free(buf_ptr[0])
    return b

def _to_json(val: Value) -> str:
    buf_ptr = libcue.ffi.new("uint8_t**")
    len_ptr = libcue.ffi.new("size_t*")

    err = libcue.dec_json(val._val, buf_ptr, len_ptr)
    if err != 0:
        raise Error(err)

    dec = libcue.ffi.string(buf_ptr[0], len_ptr[0])
    if not isinstance(dec, bytes):
        raise TypeError

    s = dec.decode("utf-8")
    libcue.libc_free(buf_ptr[0])
    return s
