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
Encode evaluation options.

Corresponding Go functionality is documented at:
https://pkg.go.dev/cuelang.org/go/cue#Option
"""

from typing import Optional, assert_never
from dataclasses import dataclass
from cffi import FFI
import libcue

@dataclass
class All:
    """
    Indicate that all fields and values should be included in
    processing even if they can be elided or omitted.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#All
    """
    pass

@dataclass
class Attributes:
    """
    Indicate whether attributes should be included.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Attributes

    Args:
        attrs: True IFF attributes should be included.
    """
    attrs: bool

@dataclass
class Concrete:
    """
    Indicate whether non-concrete values are interpreted as errors.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Concrete

    Args:
        concrete: True IFF encountered non-concrete values are an error.
    """
    concrete: bool

@dataclass
class Definitions:
    """
    Indicate whether definitions should be included.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Definitions

    Args:
        defs: True IFF definitions should be included.
    """
    defs: bool

@dataclass
class DisallowCycles:
    """
    Force validation in the presence of cycles.

    Force validation in the presence of cycles, even if non-concrete values are allowed. This is implied by Concrete.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#DisallowCycles

    Args:
        disallow_cycles: True IFF cycles are not allowed.
    """
    disallow_cycles: bool

@dataclass
class Docs:
    """
    Indicate whether docs should be included.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Docs

    Args:
        docs: True IFF docs should be included.
    """
    docs: bool

@dataclass
class ErrorsAsValues:
    """
    Treat errors as regular values.

    Treat errors as a regular value, including them at the location
    in the tree where they occur, instead of interpreting them as
    a configuration-wide failure that is returned instead of root
    value.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#ErrorsAsValues

    Args:
        err_as_val: True IFF treating errors as value
    """
    err_as_val: bool

@dataclass
class Final:
    """
    Indicate a value is final.

    Implicitly close all structs and lists in a value and select defaults.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Final
    """
    pass

@dataclass
class Hidden:
    """
    Indicate whether definitions and hidden fields should be included.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Hidden

    Args:
        hidden: True IFF definitions and hidden fields are included.
    """
    hidden: bool

@dataclass
class InlineImports:
    """
    Inline imported references.

    Inline references to values within imported packages. References
    to builtin packages are not inlined.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#InlineImports

    Args:
        inline_imports: True IFF imported references should be inlined
    """
    inline_imports: bool

@dataclass
class Optionals:
    """
    Indicate whether optional fields should be included.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Optional

    Args:
        optionals: True IFF optional fields are included.
    """
    optionals: bool

@dataclass
class Raw:
    """
    Generate value without simplification.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Raw
    """
    pass

@dataclass
class Schema:
    """
    Specify input to be a schema.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Schema
    """
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
