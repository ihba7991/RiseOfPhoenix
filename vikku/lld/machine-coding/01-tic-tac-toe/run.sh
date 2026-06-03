#!/usr/bin/env bash
# Compile every .java under src/ and run Main.
# Add classes freely under src/ — no extra config needed.
# Portable across macOS bash 3.2 and Linux bash 4+.
set -euo pipefail

out=out
mkdir -p "$out"
# Word-split on the find output; Java class filenames don't contain spaces.
# shellcheck disable=SC2046
javac -d "$out" $(find src -name '*.java')
java -cp "$out" Main "$@"
