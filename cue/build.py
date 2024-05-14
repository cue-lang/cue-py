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

from typing import Optional, assert_never
from dataclasses import dataclass
from cffi import FFI
from cue.value import Value
import libcue

@dataclass
class FileName:
    name: str

@dataclass
class ImportPath:
    path: str

@dataclass
class InferBuiltins:
    infer: bool

@dataclass
class Scope:
    scope: Value

BuildOption = FileName | ImportPath | InferBuiltins | Scope

def encode_build_opts(*opts: BuildOption) -> Optional[FFI.CData]:
    if len(opts) == 0:
        return None

    a = _alloc_bopt_array(len(opts))
    for i, opt in enumerate(opts):
        match opt:
            case FileName(name):
                c_str = libcue.ffi.new("char[]", name.encode("utf-8"))
                a[i].tag = libcue.BUILD_FILENAME
                a[i].str = c_str
            case ImportPath(path):
                c_str = libcue.ffi.new("char[]", path.encode("utf-8"))
                a[i].tag = libcue.BUILD_IMPORT_PATH
                a[i].str = c_str
            case InferBuiltins(b):
                a[i].tag = libcue.BUILD_INFER_BUILTINS
                a[i].b = b
            case Scope(scope):
                a[i].tag = libcue.BUILD_SCOPE
                a[i].value = scope._val
            case _:
                # use `assert_never` on `_` to enable
                # exhaustiveness matching.
                assert_never(opt)
    return a


def _alloc_bopt_array(num: int) -> FFI.CData:
    opts = libcue.ffi.new("cue_bopt[]", num + 1)
    opts[num].tag = libcue.BUILD_NONE
    return opts
