#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$PROJECT_DIR/.venv/bin/python" -m unittest discover \
    -s "$PROJECT_DIR/tests" \
    -p "test_*.py" \
    -v