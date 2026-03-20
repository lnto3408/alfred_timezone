#!/bin/bash
# Build .alfredworkflow package from workflow/ directory
set -e

OUTPUT="Universal-Converter.alfredworkflow"

cd "$(dirname "$0")/workflow"
rm -f "../$OUTPUT"
zip -r "../$OUTPUT" . -x '__pycache__/*' '*.pyc' '.DS_Store'
echo "Built: $OUTPUT"
