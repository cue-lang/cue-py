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
Manage lifecycle of CUE resources coming from the CUE Go API.
"""

from typing import Any, Callable, final
import libcue

@final
class _Resource:
    """
    A CUE resource.

    Resource holds any external value that is managed by the CUE Go API.
    """

    _val: int

    """
    Returns the underlying Go resoure handle.
    """
    def res(self) -> int:
        if self._val != 0:
            return self._val
        else:
            raise RuntimeError("Fatal: use of invalid resource.")

    def __init__(self, v: int):
        self._val = v

    def close(self):
        if self._val != 0:
            self.__release()

    def __release(self):
        libcue.free(self._val)
        self._val = 0

    def __del__(self):
        self.close()
