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
