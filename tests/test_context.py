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

def test_compile_empty():
    ctx = cue.Context()

    val = ctx.compile("")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"")
    assert isinstance(val, cue.Value)

def test_compile_empty_with_options():
    ctx = cue.Context()

    val = ctx.compile("", cue.FileName("empty.cue"), cue.ImportPath("example.com/foo/bar"))
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"", cue.FileName("empty.cue"), cue.ImportPath("example.com/foo/bar"))
    assert isinstance(val, cue.Value)

def test_compile():
    ctx = cue.Context()

    val = ctx.compile("true")
    assert isinstance(val, cue.Value)

    val = ctx.compile("42")
    assert isinstance(val, cue.Value)

    val = ctx.compile("1.2345")
    assert isinstance(val, cue.Value)

    val = ctx.compile('"hello"')
    assert isinstance(val, cue.Value)

    val = ctx.compile("'world'")
    assert isinstance(val, cue.Value)

    val = ctx.compile("int")
    assert isinstance(val, cue.Value)

    val = ctx.compile("{}")
    assert isinstance(val, cue.Value)

    val = ctx.compile("x: 42")
    assert isinstance(val, cue.Value)

    val = ctx.compile("x: y: z: true")
    assert isinstance(val, cue.Value)

def test_compile_bytes():
    ctx = cue.Context()

    val = ctx.compile(b"true")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"42")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"1.2345")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b'"hello"')
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"'world'")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"int")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"{}")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"x: 42")
    assert isinstance(val, cue.Value)

    val = ctx.compile(b"x: y: z: true")
    assert isinstance(val, cue.Value)

def test_compile_with_options():
    ctx = cue.Context()

    val = ctx.compile("true", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile("42", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile("1.2345", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile('"hello"', cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile("'world'", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile("int", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile("{}", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile("x: 42", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

    val = ctx.compile("x: y: z: true", cue.FileName("empty.cue"))
    assert isinstance(val, cue.Value)

def test_compile_error():
    ctx = cue.Context()

    with pytest.raises(cue.Error):
        ctx.compile("<")

    with pytest.raises(cue.Error, match="expected operand, found 'EOF'"):
        ctx.compile("a: b: -")

    with pytest.raises(cue.Error, match="expected operand, found 'EOF'"):
        ctx.compile(b"a: b: -")

def test_to_value():
    ctx = cue.Context()

    val = ctx.to_value(1)
    assert val == ctx.compile("1")

    val = ctx.to_value(-1)
    assert val == ctx.compile("-1")

    val = ctx.to_value(42)
    assert val == ctx.compile("42")

    val = ctx.to_value(True)
    assert val == ctx.compile("true")

    val = ctx.to_value(False)
    assert val == ctx.compile("false")

    val = ctx.to_value(1.2345)
    assert val == ctx.compile("1.2345")

    val = ctx.to_value("hello")
    assert val == ctx.compile("\"hello\"")

    val = ctx.to_value(b"world")
    assert val == ctx.compile("'world'")

def test_encoding_decoding_equal():
    ctx = cue.Context()

    v = 1
    assert v == ctx.to_value(v).to_int()

    v = 0xcafebabe
    assert v == ctx.to_value(v).to_unsigned()

    v = True
    assert v == ctx.to_value(v).to_bool()

    v = 1.2345
    assert v == ctx.to_value(v).to_float()

    v = "hello"
    assert v == ctx.to_value(v).to_str()

    v = b"world"
    assert v == ctx.to_value(v).to_bytes()
