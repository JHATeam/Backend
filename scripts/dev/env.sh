#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export TOP_DIR="${SCRIPT_DIR}/../.."
export FLASK_APP=hello
export FLASK_ENV=development