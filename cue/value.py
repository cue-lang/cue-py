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

"""
Perform operations on CUE values.
"""

from typing import Any, Optional, final
from cue.error import Error
import libcue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cue.context import Context

@final
class Value:
    """
    A CUE value.

    Value holds any value that can be encoded by CUE.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Value.
    """

    _ctx: 'Context'
    _val: int

    def __init__(self, ctx: 'Context', v: int):
        self._ctx = ctx
        self._val = v

    def __del__(self):
        libcue.free(self._val)

    def __eq__(self, other: Any) -> bool:
        """
        Check whether two CUE values are equal.

        Reports whether two values are equal, ignoring optional
        fields. The result is undefined for incomplete values.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.Equals

        Args:
            other: the other value to compare with.

        Returns:
            bool: True if the two values are complete and equal CUE values, False otherwise.
        """
        if isinstance(other, Value):
            return libcue.is_equal(self._val, other._val)
        return False

    def context(self) -> 'Context':
        """The Context that created this Value."""
        return self._ctx

    def unify(self, other: 'Value') -> 'Value':
        """
        Compute the greatest lower bound of two CUE values.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.Unify
        """
        v = libcue.unify(self._val, other._val)
        return Value(self._ctx, v)

    def lookup(self, path: str) -> 'Value':
        """
        Return the CUE value at path.

        Args:
            path: CUE path relative to self.

        Returns:
            Value: the value reached at path, starting from self.
        """
        return _lookup(self, path)

    def to_int(self) -> int:
        """
        Convert CUE value to integer.

        Convert the underlying value, which must be a CUE int64,
        to a Python int.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.Int64

        Returns:
            int: a Python int denoting the same CUE value.

        Raises:
            Error: if the CUE value is not an int64.
        """
        return _to_int(self)

    def to_unsigned(self) -> int:
        """
        Convert unsigned CUE value to integer.

        Convert the underlying value, which must be a CUE uint64,
        to a Python int.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.Uint64

        Returns:
            int: a Python int denoting the same CUE value.

        Raises:
            Error: if the CUE value is not an uint64.
        """
        return _to_unsigned(self)

    def to_bool(self) -> bool:
        """
        Convert bool CUE value to bool.

        Convert the underlying value, which must be a CUE bool,
        to a Python bool.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.Bool

        Returns:
            bool: a Python bool denoting the same CUE value.

        Raises:
            Error: if the CUE value is not a bool.
        """
        return _to_bool(self)

    def to_float(self) -> float:
        """
        Convert float64 CUE value to float.

        Convert the underlying value, which must be a CUE float64,
        to a Python float.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.Float64

        Returns:
            float: a Python float denoting the same CUE value.

        Raises:
            Error: if the CUE value is not a float64.
        """
        return _to_float(self)

    def to_str(self) -> str:
        """
        Convert string CUE value to str.

        Convert the underlying value, which must be a CUE string,
        to a Python string.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.String

        Returns:
            str: a Python string denoting the same CUE value.

        Raises:
            Error: if the CUE value is not a string.
        """
        return _to_str(self)

    def to_bytes(self) -> bytes:
        """
        Convert bytes CUE value to bytes.

        Convert the underlying value, which must be a CUE bytes,
        to a Python bytes.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.Bytes

        Returns:
            bytes: a Python bytes denoting the same CUE value.

        Raises:
            Error: if the CUE value is not a bytes.
        """
        return _to_bytes(self)

    def to_json(self) -> str:
        """
        Marshall CUE value to JSON.

        Corresponding Go functionality is documented at:
        https://pkg.go.dev/cuelang.org/go/cue#Value.MarshalJSON

        Returns:
            str: the JSON encoding of the value

        Raises:
            Error: if the CUE value can not be mashalled to JSON.
        """

        return _to_json(self)

    def default(self) -> Optional['Value']:
        """
        Return default value.

        Returns:
            Optional[Value]: the default value, if it exists, or None otherwise.
        """
        return _default(self)

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

def _lookup(val: Value, path: str) -> Value:
    val_ptr = libcue.ffi.new("cue_value*")
    path_ptr = libcue.ffi.new("char[]", path.encode("utf-8"))

    err = libcue.lookup_string(val._val, path_ptr, val_ptr)
    if err != 0:
        raise Error(err)
    return Value(val._ctx, val_ptr[0])

def _default(val: Value) -> Optional[Value]:
    ok_ptr = libcue.ffi.new("bool*")
    res = libcue.default(val._val, ok_ptr)
    if ok_ptr[0] == 1:
        return Value(val._ctx, res)
    return None
