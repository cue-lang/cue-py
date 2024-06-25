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
Handle CUE errors.
"""

from typing import final
from cue.res import Resource
import libcue

@final
class Error(Exception):
    """
    CUE evaluation error.
    """

    _err: Resource

    def res(self):
        return self._err.res()

    def __init__(self, err: int):
        self._err = Resource(err)

    def __str__(self):
        c_str = libcue.error_string(self.res())
        s = libcue.ffi.string(c_str).decode("utf-8")
        libcue.libc_free(c_str)
        return s
