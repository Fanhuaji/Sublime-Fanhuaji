#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="${SCRIPT_DIR}/.."

pushd "${PROJECT_DIR}" || exit

mypy -p plugin
flake8 plugin
black --check .

popd || exit
