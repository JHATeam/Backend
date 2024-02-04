#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
echo "SCRIPT_DIR: $SCRIPT_DIR"
export TOP_DIR="${SCRIPT_DIR}/../.."


source "$TOP_DIR"/scripts/dev/env.sh
cd $TOP_DIR/src
echo "Running flask app"
export FLASK_APP=app
python3 -m flask run --host=0.0.0.0 --port=8080