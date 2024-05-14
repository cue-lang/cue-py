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
Compile CUE code.
"""

from cue.build import BuildOption, encode_build_opts
from cue.value import Value
from cue.error import Error
import libcue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cue.context import Context

def compile(ctx: 'Context', s: str, *opts: BuildOption) -> Value:
    val_ptr = libcue.ffi.new("cue_value*")
    buf = libcue.ffi.new("char[]", s.encode("utf-8"))

    build_opts = encode_build_opts(*opts)
    err = libcue.compile_string(ctx._ctx, buf, build_opts, val_ptr)
    if err != 0:
        raise Error(err)
    return Value(ctx, val_ptr[0])

def compile_bytes(ctx: 'Context', buf: bytes, *opts: BuildOption) -> Value:
    val_ptr = libcue.ffi.new("cue_value*")
    buf_ptr = libcue.ffi.from_buffer(buf)

    build_opts = encode_build_opts(*opts)
    err = libcue.compile_bytes(ctx._ctx, buf_ptr, len(buf), build_opts, val_ptr)
    if err != 0:
        raise Error(err)
    return Value(ctx, val_ptr[0])
