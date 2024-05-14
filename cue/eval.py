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
import libcue

@dataclass
class All:
    pass

@dataclass
class Attributes:
    attrs: bool

@dataclass
class Concrete:
    concrete: bool

@dataclass
class Definitions:
    defs: bool

@dataclass
class DisallowCycles:
    disallow_cycles: bool

@dataclass
class Docs:
    docs: bool

@dataclass
class ErrorsAsValues:
    err_as_val: bool

@dataclass
class Final:
    pass

@dataclass
class Hidden:
    hidden: bool

@dataclass
class InlineImports:
    inline_imports: bool

@dataclass
class Optionals:
    optionals: bool

@dataclass
class Raw:
    pass

@dataclass
class Schema:
    pass

EvalOption = All | Attributes | Concrete | Definitions | DisallowCycles | Docs | ErrorsAsValues | Final | Hidden | InlineImports | Optionals | Raw | Schema


def _alloc_eopt_array(num: int) -> FFI.CData:
    opts = libcue.ffi.new("cue_eopt[]", num + 1)
    opts[num].tag = libcue.OPT_NONE
    return opts

def encode_eval_opts(*opts: EvalOption) -> Optional[FFI.CData]:
    if len(opts) == 0:
        return None

    a = _alloc_eopt_array(len(opts))
    for i, opt in enumerate(opts):
        match opt:
            case All():
                a[i].tag = libcue.OPT_ALL
            case Attributes(attrs):
                a[i].tag = libcue.OPT_ATTR
                a[i].value = attrs
            case Concrete(concrete):
                a[i].tag = libcue.OPT_CONCRETE
                a[i].value = concrete
            case Definitions(defs):
                a[i].tag = libcue.OPT_DEFS
                a[i].value = defs
            case DisallowCycles(disallow_cycles):
                a[i].tag = libcue.OPT_DISALLOW_CYCLES
                a[i].value = disallow_cycles
            case Docs(docs):
                a[i].tag = libcue.OPT_DOCS
                a[i].value = docs
            case ErrorsAsValues(err_as_val):
                a[i].tag = libcue.OPT_ERRORS_AS_VALUES
                a[i].value = err_as_val
            case Final():
                a[i].tag = libcue.OPT_FINAL
            case Hidden(hidden):
                a[i].tag = libcue.OPT_HIDDEN
                a[i].value = hidden
            case InlineImports(inline_imports):
                a[i].tag = libcue.OPT_INLINE_IMPORTS
                a[i].value = inline_imports
            case Optionals(optionals):
                a[i].tag = libcue.OPT_OPTIONALS
                a[i].value = optionals
            case Raw():
                a[i].tag = libcue.OPT_RAW
            case Schema():
                a[i].tag = libcue.OPT_SCHEMA
            case _:
                # use `assert_never` on `_` to enable
                # exhaustiveness matching.
                assert_never(opt)

    return a
