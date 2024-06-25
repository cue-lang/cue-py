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
This module implements low-level bindings to libcue.
"""

# In ABI mode the bindings from libcue are generated at runtime.
# Silence the type checker about missing attributes (symbols) not
# known at type-check time.
# mypy: disable-error-code="attr-defined"

from typing import Optional
from cffi import FFI
import sys

ffi = FFI()

# We're mixing tabs and spaces because we want to be able to copy-paste
# these declarations from libcue/cue.h.
ffi.cdef("""
    typedef uintptr_t cue_ctx;
    typedef uintptr_t cue_value;
    typedef uintptr_t cue_error;

    typedef enum {
    	CUE_KIND_BOTTOM,
    	CUE_KIND_NULL,
    	CUE_KIND_BOOL,
    	CUE_KIND_INT,
    	CUE_KIND_FLOAT,
    	CUE_KIND_STRING,
    	CUE_KIND_BYTES,
    	CUE_KIND_STRUCT,
    	CUE_KIND_LIST,
    	CUE_KIND_NUMBER,
    	CUE_KIND_TOP,
    } cue_kind;

    typedef enum {
    	CUE_BUILD_NONE,
    	CUE_BUILD_FILENAME,
    	CUE_BUILD_IMPORT_PATH,
    	CUE_BUILD_INFER_BUILTINS,
    	CUE_BUILD_SCOPE,
    } cue_bopt_tag;

    typedef struct {
    	cue_bopt_tag tag;
    	cue_value value;
    	char *str;
    	bool b;
    } cue_bopt;

    typedef enum {
    	CUE_OPT_NONE,
    	CUE_OPT_ALL,
    	CUE_OPT_ATTR,
    	CUE_OPT_CONCRETE,
    	CUE_OPT_DEFS,
    	CUE_OPT_DISALLOW_CYCLES,
    	CUE_OPT_DOCS,
    	CUE_OPT_ERRORS_AS_VALUES,
    	CUE_OPT_FINAL,
    	CUE_OPT_HIDDEN,
    	CUE_OPT_INLINE_IMPORTS,
    	CUE_OPT_OPTIONALS,
    	CUE_OPT_RAW,
    	CUE_OPT_SCHEMA,
    } cue_eopt_tag;

    typedef struct {
    	cue_eopt_tag tag;
    	bool value;
    } cue_eopt;

    cue_ctx	cue_newctx(void);
    char*	cue_error_string(cue_error);

    cue_error	cue_compile_string(cue_ctx, char*, void*, cue_value*);
    cue_error	cue_compile_bytes(cue_ctx, void*, size_t, void*, cue_value*);

    cue_value	cue_top(cue_ctx);
    cue_value	cue_bottom(cue_ctx);
    cue_value	cue_unify(cue_value, cue_value);
    cue_error	cue_instance_of(cue_value, cue_value, void*);
    cue_error	cue_lookup_string(cue_value, char*, cue_value*);
    cue_value	cue_from_int64(cue_ctx, int64_t);
    cue_value	cue_from_uint64(cue_ctx, uint64_t);
    cue_value	cue_from_bool(cue_ctx, bool);
    cue_value	cue_from_double(cue_ctx, double);
    cue_value	cue_from_string(cue_ctx, char*);
    cue_value	cue_from_bytes(cue_ctx, void*, size_t);
    cue_error	cue_dec_int64(cue_value, int64_t*);
    cue_error	cue_dec_uint64(cue_value, uint64_t*);
    cue_error	cue_dec_bool(cue_value, bool*);
    cue_error	cue_dec_double(cue_value, double*);
    cue_error	cue_dec_string(cue_value, char**);
    cue_error	cue_dec_bytes(cue_value, uint8_t**, size_t*);
    cue_error	cue_dec_json(cue_value, uint8_t**, size_t*);
    cue_error	cue_validate(cue_value, void*);
    cue_value	cue_default(cue_value, bool*);
    cue_kind	cue_concrete_kind(cue_value);
    cue_kind	cue_incomplete_kind(cue_value);
    cue_error	cue_value_error(cue_value);
    bool	cue_is_equal(cue_value, cue_value);

    void	cue_free(uintptr_t);
    void	cue_free_all(uintptr_t*);
    void	libc_free(void*);
""")

if sys.platform != "win32":
    # When there are no more references to lib (such as when there
    # are no more references to this module), the Python runtime can
    # try to unload libcue. Go shared libraries cannot be unloaded.
    # Pass RTLD_NODELETE to dlopen to prevent this.
    #
    # Note that RTLD_NODELETE is Unix-only, so on Windows we do
    # something different (see below).
    #
    # Also note that the Python garbage collector could run at program
    # exit and it could determine that there are no more references
    # to libcue (because the program is exiting), triggering a
    # premature and dangerous dlclose. This prevents it.
    lib = ffi.dlopen("cue", ffi.RTLD_NODELETE)
else:
    # On Windows we don't have RTLD_NODELETE. Create an artificial
    # global reference to lib, so we prevent unloading the shared
    # library.
    lib = ffi.dlopen("cue")
    sys.modules[__name__]._lib_reference = lib

KIND_BOTTOM = lib.CUE_KIND_BOTTOM
KIND_NULL = lib.CUE_KIND_NULL
KIND_BOOL = lib.CUE_KIND_BOOL
KIND_INT = lib.CUE_KIND_INT
KIND_FLOAT = lib.CUE_KIND_FLOAT
KIND_STRING = lib.CUE_KIND_STRING
KIND_BYTES = lib.CUE_KIND_BYTES
KIND_STRUCT = lib.CUE_KIND_STRUCT
KIND_LIST = lib.CUE_KIND_LIST
KIND_NUMBER = lib.CUE_KIND_NUMBER
KIND_TOP = lib.CUE_KIND_TOP

BUILD_NONE = lib.CUE_BUILD_NONE
BUILD_FILENAME = lib.CUE_BUILD_FILENAME
BUILD_IMPORT_PATH = lib.CUE_BUILD_IMPORT_PATH
BUILD_INFER_BUILTINS = lib.CUE_BUILD_INFER_BUILTINS
BUILD_SCOPE = lib.CUE_BUILD_SCOPE

OPT_NONE = lib.CUE_OPT_NONE
OPT_ALL = lib.CUE_OPT_ALL
OPT_ATTR = lib.CUE_OPT_ATTR
OPT_CONCRETE = lib.CUE_OPT_CONCRETE
OPT_DEFS = lib.CUE_OPT_DEFS
OPT_DISALLOW_CYCLES = lib.CUE_OPT_DISALLOW_CYCLES
OPT_DOCS = lib.CUE_OPT_DOCS
OPT_ERRORS_AS_VALUES = lib.CUE_OPT_ERRORS_AS_VALUES
OPT_FINAL = lib.CUE_OPT_FINAL
OPT_HIDDEN = lib.CUE_OPT_HIDDEN
OPT_INLINE_IMPORTS = lib.CUE_OPT_INLINE_IMPORTS
OPT_OPTIONALS = lib.CUE_OPT_OPTIONALS
OPT_RAW = lib.CUE_OPT_RAW
OPT_SCHEMA = lib.CUE_OPT_SCHEMA

def newctx() -> int:
    return lib.cue_newctx()

def error_string(err: int) -> FFI.CData:
    return lib.cue_error_string(err)

def compile_string(ctx: int, str: FFI.CData, opts: Optional[FFI.CData], val_ptr: FFI.CData) -> int:
    if opts == None:
        return lib.cue_compile_string(ctx, str, ffi.NULL, val_ptr)
    return lib.cue_compile_string(ctx, str, opts, val_ptr)

def compile_bytes(ctx: int, buf: FFI.CData, len: int, opts: Optional[FFI.CData], val_ptr: FFI.CData) -> int:
    if opts == None:
        return lib.cue_compile_bytes(ctx, buf, len, ffi.NULL, val_ptr)
    return lib.cue_compile_bytes(ctx, buf, len, opts, val_ptr)

def top(ctx: int) -> int:
    return lib.cue_top(ctx)

def bottom(ctx: int) -> int:
    return lib.cue_bottom(ctx)

def unify(x: int, y: int) -> int:
    return lib.cue_unify(x, y)

def instance_of(v0: int, v1: int, opts: Optional[FFI.CData]) -> int:
    if opts == None:
        return lib.cue_instance_of(v0, v1, ffi.NULL)
    return lib.cue_instance_of(v0, v1, opts)

def lookup_string(v: int, path: FFI.CData, ptr: FFI.CData) -> int:
    return lib.cue_lookup_string(v, path, ptr)

def from_int64(ctx: int, val: int) -> int:
    return lib.cue_from_int64(ctx, val)

def from_uint64(ctx: int, val: int) -> int:
    return lib.cue_from_uint64(ctx, val)

def from_bool(ctx: int, val: bool) -> int:
    return lib.cue_from_bool(ctx, val)

def from_double(ctx: int, val: float) -> int:
    return lib.cue_from_double(ctx, val)

def from_string(ctx: int, val: FFI.CData) -> int:
    return lib.cue_from_string(ctx, val)

def from_bytes(ctx: int, buf: FFI.CData, len: int) -> int:
    return lib.cue_from_bytes(ctx, buf, len)

def dec_int64(val: int, ptr: FFI.CData) -> int:
    return lib.cue_dec_int64(val, ptr)

def dec_uint64(val: int, ptr: FFI.CData) -> int:
    return lib.cue_dec_uint64(val, ptr)

def dec_bool(val: int, ptr: FFI.CData) -> int:
    return lib.cue_dec_bool(val, ptr)

def dec_double(val: int, ptr: FFI.CData) -> int:
    return lib.cue_dec_double(val, ptr)

def dec_string(val: int, ptr: FFI.CData) -> int:
    return lib.cue_dec_string(val, ptr)

def dec_bytes(val: int, buf_ptr: FFI.CData, len_ptr: FFI.CData) -> int:
    return lib.cue_dec_bytes(val, buf_ptr, len_ptr)

def dec_json(val: int, buf_ptr: FFI.CData, len_ptr: FFI.CData) -> int:
    return lib.cue_dec_json(val, buf_ptr, len_ptr)

def validate(val: int, opts: Optional[FFI.CData]) -> int:
    if opts == None:
        return lib.cue_validate(val, ffi.NULL)
    return lib.cue_validate(val, opts)

def default(val: int, ok_ptr: FFI.CData) -> int:
    return lib.cue_default(val, ok_ptr)

def concrete_kind(v: int) -> int:
    return lib.cue_concrete_kind(v)

def incomplete_kind(v: int) -> int:
    return lib.cue_incomplete_kind(v)

def value_error(v: int) -> int:
    return lib.cue_value_error(v)

def is_equal(x: int, y: int) -> bool:
    return lib.cue_is_equal(x, y)

def free(x: int) -> None:
    lib.cue_free(x)

def libc_free(ptr: FFI.CData) -> None:
    lib.libc_free(ptr)
