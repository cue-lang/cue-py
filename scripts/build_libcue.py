#!/usr/bin/env python3
"""Build a platform libcue library into the package directory.

The source checkout and Go toolchain are deliberate build-time prerequisites.
This script never downloads either of them.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def shared_library_name() -> str:
    if sys.platform == 'darwin':
        return 'libcue.dylib'
    if sys.platform == 'win32':
        return 'cue.dll'
    return 'libcue.so'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='existing checkout of github.com/cue-lang/libcue')
    args = parser.parse_args()

    source: Path = args.source.resolve()
    if not (source / 'go.mod').is_file():
        parser.error(f'{source} is not a libcue checkout (go.mod is missing)')
    if shutil.which('go') is None:
        parser.error('Go is required to build libcue; install it before running this script')

    destination: Path = Path(__file__).resolve().parents[1] / 'libcue' / shared_library_name()
    subprocess.run(
        ['go', 'build', '-o', str(destination), '-buildmode=c-shared', '.'],
        cwd=source,
        check=True,
    )
    # Go emits a C header beside every c-shared output. Runtime consumers only
    # need the library, so do not leave the generated header in the package.
    destination.with_suffix('.h').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
