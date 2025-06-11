// Copyright 2024 The CUE Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package github

import (
	"list"
	"cue.dev/x/githubactions"
)

// The trybot workflow.
workflows: trybot: _repo.bashWorkflow & {
	name: _repo.trybot.name

	on: {
		push: {
			branches: list.Concat([[_repo.testDefaultBranch], _repo.protectedBranchPatterns]) // do not run PR branches
		}
		pull_request: {}
	}

	jobs: {
		test: {
			strategy:  _testStrategy
			"runs-on": "${{ matrix.runner }}"

			let _setupGoActionsCaches = _repo.setupGoActionsCaches & {
				#goVersion: goVersionVal
				#os:        runnerOSVal
				_
			}

			// Only run the trybot workflow if we have the trybot trailer, or
			// if we have no special trailers. Note this condition applies
			// after and in addition to the "on" condition above.
			if: "\(_repo.containsTrybotTrailer) || ! \(_repo.containsDispatchTrailer)"

			steps: [
				for v in _repo.checkoutCode {v},

				{
					uses: "cue-lang/setup-cue@v1.0.1"
					with: version: "latest"
				},

				for v in _installGo {v},
				_repo.earlyChecks,

				{
					name: "Re-generate CI"
					run: """
						cue cmd gen
						"""
					"working-directory": "./internal/ci"
				},

				_repo.checkGitClean,

				_installPython,

				// cachePre must come after installing Go,
				// because the cache locations
				// are established by running each tool.
				for v in _setupGoActionsCaches {v},

				_runPip,

				_checkoutLibcue,
				_buildLibcue,

				_mypy,
				_addLibcueToPath,
				_pytest,

				_repo.checkGitClean,
			]
		}
	}

	let runnerOS = "runner.os"
	let runnerOSVal = "${{ \(runnerOS) }}"
	let goVersion = "matrix.go-version"
	let goVersionVal = "${{ \(goVersion) }}"
	let pythonVersion = "matrix.python-version"
	let pythonVersionVal = "${{ \(pythonVersion) }}"

	_testStrategy: {
		"fail-fast": false
		matrix: {
			"go-version": ["stable"]
			"python-version": [_repo.latestStablePython]

			// TODO: Windows doesn't work yet, see issue #3253
			runner: [_repo.linuxMachine, _repo.macosMachine]
		}
	}

	_installGo: _repo.installGo & {
		#setupGo: with: "go-version": goVersionVal
		_
	}

	_installPython: githubactions.#Step & {
		name: "Install Python"
		uses: "actions/setup-python@v5"
		with: {
			"python-version": pythonVersionVal
			cache:            "pip"
		}
	}

	_runPip: githubactions.#Step & {
		name: "pip install"
		run:  "pip install -r requirements.txt"
	}

	_checkoutLibcue: githubactions.#Step & {
		name: "Checkout libcue"
		uses: "actions/checkout@v4"
		with: {
			repository: "cue-lang/libcue"
			path:       "libcue-checkout"
		}
	}

	_buildLibcue: githubactions.#Step & {
		name:                "Build libcue"
		"working-directory": "libcue-checkout"
		// The name of the shared library is target-dependent.
		// Build libcue with all possible names so we're covered
		// in all cases.
		run: """
			go build -o libcue.so -buildmode=c-shared
			cp libcue.so libcue.dylib
			cp libcue.so cue.dll
			"""
	}

	_mypy: githubactions.#Step & {
		name: "mypy"
		run:  "mypy ."
	}

	_addLibcueToPath: githubactions.#Step & {
		name: "Add libcue to PATH"
		if:   "runner.os == 'Windows'"
		// On Windows LoadLibrary loads DLLs from PATH. GitHub
		// actions doesn't allow setting PATH via `env`,
		// rather we need to append to the file pointed to by
		// `$GITHUB_PATH`. This will only affect future steps,
		// so we do it before running `pytest`.
		run: """
			echo '${{ github.workspace }}/libcue-checkout' >> $GITHUB_PATH
			"""
	}

	_pytest: githubactions.#Step & {
		name: "pytest"
		env: LD_LIBRARY_PATH:   "${{ github.workspace }}/libcue-checkout"
		env: DYLD_LIBRARY_PATH: "${{ github.workspace }}/libcue-checkout"
		run: "pytest"
	}
}
