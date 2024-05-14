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

def test_unify():
    ctx = cue.Context()

    a = ctx.top()
    b = ctx.compile("true")
    r = ctx.compile("true")
    assert r == a.unify(b)

    a = ctx.compile("int")
    b = ctx.compile("42")
    r = ctx.compile("42")
    assert r == a.unify(b)

    a = ctx.compile("<100")
    b = ctx.compile("5")
    r = ctx.compile("5")
    assert r == a.unify(b)

    a = ctx.compile("x: y: string")
    b = ctx.compile('x: y: "hello"')
    r = ctx.compile('x: y: "hello"')
    assert r == a.unify(b)

def test_unify_error():
    ctx = cue.Context()

    a = ctx.compile("true")
    b = ctx.compile("false")
    r = ctx.bottom()
    assert r == a.unify(b)

def test_decode():
    ctx = cue.Context()

    val = ctx.compile("1")
    assert val.to_int() == 1

    val = ctx.compile("-1")
    assert val.to_int() == -1

    val = ctx.compile("true")
    assert val.to_bool() == True

    val = ctx.compile("false")
    assert val.to_bool() == False

    val = ctx.compile("1.2345")
    assert val.to_float() == 1.2345

    val = ctx.compile("\"hello\"")
    assert val.to_str() == "hello"

    val = ctx.compile("'world'")
    assert val.to_bytes() == b"world"

    val = ctx.compile("x: { a: 1, b: true }")
    assert val.to_json() == r'{"x":{"a":1,"b":true}}'

def test_decode_error():
    ctx = cue.Context()

    with pytest.raises(cue.Error):
        ctx.compile("1").to_bool()

    with pytest.raises(cue.Error):
        ctx.compile("-1").to_str()

    with pytest.raises(cue.Error):
        ctx.compile("true").to_float()

    with pytest.raises(cue.Error):
        ctx.compile("false").to_unsigned()

def test_lookup():
    ctx = cue.Context()

    val = ctx.compile("x: true")
    assert val.lookup("x").to_bool() == True

    val = ctx.compile(r'x: y: { a: 1, b: "hello"}')
    assert val.lookup("x").lookup("y").lookup("b").to_str() == "hello"

def test_default():
    ctx = cue.Context()

    v = ctx.compile("int")
    assert v.default() == None

    v = ctx.compile("1")
    assert v.default() == None

    v = ctx.compile("int | *1")
    assert v.default() == ctx.to_value(1)

    v = ctx.compile(r'string | *"hello"')
    assert v.default() == ctx.to_value("hello")

    v = ctx.compile(r'(int | *1) & 2')
    assert v.default() == None
