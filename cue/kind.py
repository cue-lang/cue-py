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
Classify CUE values.
"""

from enum import Enum
from typing import Dict
import libcue

class Kind(Enum):
    """
    The type of a Value.

    Corresponding Go functionality is documented at:
    https://pkg.go.dev/cuelang.org/go/cue#Kind.

    Attributes:
        BOTTOM: The bottom value.
        NULL: The null value.
        BOOL: A boolean.
        INT: An integral number.
        FLOAT: A decimal floating point number.
        STRING: A string.
        BYTES: A blob of data.
        STRUCT: A key-value map.
        LIST: A list of values.
        NUMBER: Any kind of number.
        TOP: The top value.
    """
    BOTTOM = libcue.KIND_BOTTOM
    NULL = libcue.KIND_NULL
    BOOL = libcue.KIND_BOOL
    INT = libcue.KIND_INT
    FLOAT = libcue.KIND_FLOAT
    STRING = libcue.KIND_STRING
    BYTES = libcue.KIND_BYTES
    STRUCT = libcue.KIND_STRUCT
    LIST = libcue.KIND_LIST
    NUMBER = libcue.KIND_NUMBER
    TOP = libcue.KIND_TOP

to_kind: Dict[int, Kind] = {
    libcue.KIND_BOTTOM: Kind.BOTTOM,
    libcue.KIND_NULL: Kind.NULL,
    libcue.KIND_BOOL: Kind.BOOL,
    libcue.KIND_INT: Kind.INT,
    libcue.KIND_FLOAT: Kind.FLOAT,
    libcue.KIND_STRING: Kind.STRING,
    libcue.KIND_BYTES: Kind.BYTES,
    libcue.KIND_STRUCT: Kind.STRUCT,
    libcue.KIND_LIST: Kind.LIST,
    libcue.KIND_NUMBER: Kind.NUMBER,
    libcue.KIND_TOP: Kind.TOP,
}
