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

	"github.com/SchemaStore/schemastore/src/schemas/json"
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

				json.#step & {
					uses: "cue-lang/setup-cue@v1.0.0"
					with: version: "v0.8.0"
				},

				_repo.earlyChecks,

				json.#step & {
					name: "Re-generate CI"
					run: """
						cue cmd importjsonschema ./vendor
						cue cmd gen
						"""
					"working-directory": "./internal/ci"
				},

				_repo.checkGitClean,

				_installGo,
				_installPython,

				// cachePre must come after installing Go,
				// because the cache locations
				// are established by running each tool.
				for v in _setupGoActionsCaches {v},

				_runPip,

				_checkoutLibcue,
				_buildLibcue,

				_mypy,
				_addLibcueToPATH,
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
			"go-version": [_repo.latestStableGo]
			"python-version": [_repo.latestStablePython]

			runner: [_repo.linuxMachine, _repo.macosMachine]
		}
	}

	_installGo: _repo.installGo & {
		with: "go-version": goVersionVal
	}

	_installPython: json.#step & {
		name: "Install Python"
		uses: "actions/setup-python@v5"
		with: {
			"python-version": pythonVersionVal
			cache: "pip"
		}
	}

	_runPip: json.#step & {
		name: "pip install"
		run: "pip install -r requirements.txt"
	}

	_checkoutLibcue: json.#step & {
		name: "Checkout libcue"
		uses: "actions/checkout@v4"
		with: {
			repository: "cue-lang/libcue"
			path: "libcue-checkout"
		}
	}

	_buildLibcue: json.#step & {
		name: "Build libcue"
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

	_mypy: json.#step & {
		name: "mypy"
		run: "mypy ."
	}

	_addLibcueToPATH: json.#step & {
		name: "Add libcue to PATH"
		if: "runner.os == 'Windows'"
		// On Windows LoadLibrary loads DLLs from PATH. GitHub
		// actions doesn't allow setting PATH via `env`,
		// rather we need to append to the file pointed to by
		// `$GITHUB_PATH`. This will only affect future steps,
		// so we do it before running `pytest`.
		run: """
			echo "${{ github.workspace }}/libcue-checkout" >> $GITHUB_PATH
			"""
	}

	_pytest: json.#step & {
		name: "pytest"
		env: LD_LIBRARY_PATH: "${{ github.workspace }}/libcue-checkout"
		env: DYLD_LIBRARY_PATH: "${{ github.workspace }}/libcue-checkout"
		run: "pytest"
	}
}
