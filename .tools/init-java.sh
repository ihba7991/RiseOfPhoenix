#!/usr/bin/env bash
# init-java.sh — scaffold a minimal plain-Java workspace in the current directory.
#
# Derives the entry-class name from the folder you're in:
#
#   06-parking-lot         → ParkingLotMainApplication
#   abstract-factory       → AbstractFactoryMainApplication
#   threads-runnable       → ThreadsRunnableMainApplication
#
# Run from inside any problem folder:
#
#     bash "$(git rev-parse --show-toplevel)/.tools/init-java.sh"
#
# Creates:
#   - src/<ClassName>.java   — entry-point stub you fill in
#   - run.sh                 — javac + java wrapper (compiles every .java under src/)
#   - .gitignore             — ignores build output
#
# No Maven, no Gradle. Add more .java files under src/ as you go.

set -euo pipefail

# Derive Java class name from the folder's basename.
# 1. Strip a leading "NN-" prefix (machine-coding uses 01-tic-tac-toe etc).
# 2. PascalCase the remaining hyphen-separated segments.
# 3. Append "MainApplication".
folder="$(basename "$PWD")"
stripped="$(printf '%s' "$folder" | sed 's/^[0-9][0-9]*-//')"
class_base="$(printf '%s' "$stripped" | awk -F- '
  { for (i = 1; i <= NF; i++) $i = toupper(substr($i,1,1)) substr($i,2) }
  { printf "%s", $0 }
' OFS='')"

if [[ -z "$class_base" ]]; then
  echo "init-java: could not derive a class name from folder '$folder'." >&2
  exit 1
fi

class_name="${class_base}MainApplication"
src_file="src/${class_name}.java"

if [[ -f run.sh || -f "$src_file" ]]; then
  echo "init-java: already initialized here ($src_file or run.sh exists)." >&2
  echo "          delete those files first to re-init." >&2
  exit 1
fi

mkdir -p src

# Use an unquoted heredoc so ${class_name} expands; escape any literal
# shell metacharacters that should remain in the generated file.
cat > "$src_file" <<EOF
public class ${class_name} {
    public static void main(String[] args) {
        // TODO: implement your solution here
        System.out.println("Hello from ${class_name}");
    }
}
EOF

cat > run.sh <<EOF
#!/usr/bin/env bash
# Compile every .java under src/ and run ${class_name}.
# Add classes freely under src/ — no extra config needed.
# Portable across macOS bash 3.2 and Linux bash 4+.
set -euo pipefail

out=out
mkdir -p "\$out"
# Word-split on the find output; Java class filenames don't contain spaces.
# shellcheck disable=SC2046
javac -d "\$out" \$(find src -name '*.java')
java -cp "\$out" ${class_name} "\$@"
EOF
chmod +x run.sh

cat > .gitignore <<'GI'
out/
*.class
GI

echo "init-java: scaffolded $src_file + run.sh"
echo "           run with: ./run.sh"
