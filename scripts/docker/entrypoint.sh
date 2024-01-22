#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
echo "SCRIPT_DIR: $SCRIPT_DIR"
export TOP_DIR="${SCRIPT_DIR}/../.."


source "$TOP_DIR"/scripts/dev/env.sh
cd $TOP_DIR/src
echo "Running flask app"
python3 -m flask run -p 8080