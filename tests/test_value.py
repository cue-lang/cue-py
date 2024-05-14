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

import pytest
import cue

def test_context():
    ctx = cue.Context()

    val = ctx.compile("")
    assert val.context() == ctx

    val = ctx.compile("x: 42")
    assert val.context() == ctx

def test_equal():
    ctx = cue.Context()

    val0 = ctx.compile("")
    val1 = ctx.compile("")
    assert val0 == val1

    val2 = ctx.compile("x: 1")
    val3 = ctx.compile("x: 1")
    assert val2 == val3

    val4 = ctx.compile("a: b: { x: 42, y: \"hello\" }")
    val5 = ctx.compile("a: b: { x: 42, y: \"hello\" }")
    assert val4 == val5

def test_not_equal():
    ctx = cue.Context()

    val0 = ctx.compile("")
    val1 = ctx.compile("true")
    assert val0 != val1

    val2 = ctx.compile("x: 1")
    val3 = ctx.compile("x: 2")
    assert val2 != val3

    val4 = ctx.compile("a: b: { x: 42, y: \"hello\" }")
    val5 = ctx.compile("a: b: { x: 42, y: \"world\" }")
    assert val4 != val5

    val6 = ctx.compile("true")
    assert val6 != True
