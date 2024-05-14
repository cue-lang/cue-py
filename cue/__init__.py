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
cue: Python bindings to CUE

CUE is an open source data constraint language which aims to simplify
tasks involving defining and using data.

This package provide programmatic access to CUE from Python. The
Python API roughly follows the Go API documented at
https://pkg.go.dev/cuelang.org/go/cue, but uses Python idioms when
appropiate.

A Value represents a CUE value. Values are created from a Context.
Multiple values involved in some operation must use the same Context.

For more information about the CUE language see https://cuelang.org.
"""

from .build import (
    BuildOption,
    FileName,
    ImportPath,
    InferBuiltins,
    Scope,
)
from .context import Context
from .error import Error
from .eval import (
    All,
    Attributes,
    Concrete,
    Definitions,
    DisallowCycles,
    Docs,
    ErrorsAsValues,
    EvalOption,
    Final,
    Hidden,
    InlineImports,
    Optionals,
    Raw,
    Schema,
)
from .value import Value

__all__ = [
    'All',
    'Attributes',
    'BuildOption',
    'Concrete',
    'Context',
    'Definitions',
    'DisallowCycles',
    'Docs',
    'Error',
    'ErrorsAsValues',
    'EvalOption',
    'FileName',
    'Final',
    'Hidden',
    'ImportPath',
    'InferBuiltins',
    'InlineImports',
    'Optionals',
    'Raw',
    'Schema',
    'Scope',
    'Value',
]
