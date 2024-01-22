#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export TOP_DIR="${SCRIPT_DIR}/../.."
export FLASK_APP=hello.py
export FLASK_DEBUG=1