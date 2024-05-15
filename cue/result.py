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
Return results or errors.
"""

from typing import Generic, TypeVar, Union
from dataclasses import dataclass

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    """
    Encode success.

    Args:
        value: result to encode
    """
    value: T

@dataclass
class Err(Generic[E]):
    """
    Encode failure.

    Args:
        err: error to encode
    """
    err: E

Result = Union[Ok[T], Err[E]]
