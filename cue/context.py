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

from functools import singledispatchmethod
from typing import final
from cue.value import Value
from cue.build import BuildOption
from cue.compile import compile, compile_bytes
import libcue

@final
class Context:
    _ctx: int

    def __init__(self):
        self._ctx = libcue.newctx()

    def __del__(self):
        libcue.free(self._ctx)

    @singledispatchmethod
    def compile(self, s, *opts: BuildOption) -> Value:
        raise NotImplementedError

    @compile.register
    def _(self, s: str, *opts: BuildOption) -> Value:
        return compile(self, s, *opts)

    @compile.register
    def _(self, b: bytes, *opts: BuildOption) -> Value:
        return compile_bytes(self, b, *opts)

    def top(self) -> Value:
        return Value(self, libcue.top(self._ctx))

    def bottom(self) -> Value:
        return Value(self, libcue.bottom(self._ctx))

    @singledispatchmethod
    def to_value(self, arg) -> Value:
        raise NotImplementedError

    @to_value.register
    def _(self, arg: int):
        return Value(self, libcue.from_int64(self._ctx, arg))

    @to_value.register
    def _(self, arg: bool):
        return Value(self, libcue.from_bool(self._ctx, arg))

    @to_value.register
    def _(self, arg: float):
        return Value(self, libcue.from_double(self._ctx, arg))

    @to_value.register
    def _(self, arg: str):
        c_str = libcue.ffi.new("char[]", arg.encode("utf-8"))
        return Value(self, libcue.from_string(self._ctx, c_str))

    @to_value.register
    def _(self, arg: bytes):
        c_buf = libcue.ffi.from_buffer(arg)
        return Value(self, libcue.from_bytes(self._ctx, c_buf, len(arg)))

    def to_value_from_unsigned(self, arg: int) -> Value:
        return Value(self, libcue.from_uint64(self._ctx, arg))
