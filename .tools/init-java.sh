#!/usr/bin/env bash
# init-java.sh — scaffold a minimal plain-Java workspace in the current directory.
#
# Run from inside any problem folder (e.g. .../lld/machine-coding/06-parking-lot/):
#
#     bash "$(git rev-parse --show-toplevel)/.tools/init-java.sh"
#
# That creates:
#   - src/Main.java   — entry-point stub you fill in
#   - run.sh          — javac + java wrapper (compiles every .java under src/)
#   - .gitignore      — ignores build output
#
# No Maven, no Gradle. Add more .java files under src/ as you go.

set -euo pipefail

if [[ -f src/Main.java || -f run.sh ]]; then
  echo "init-java: already initialized here (src/Main.java or run.sh exists)." >&2
  echo "          delete those files first to re-init." >&2
  exit 1
fi

mkdir -p src

cat > src/Main.java <<'JAVA'
public class Main {
    public static void main(String[] args) {
        // TODO: implement your solution here
        System.out.println("Hello — start hacking");
    }
}
JAVA

cat > run.sh <<'SH'
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
SH
chmod +x run.sh

cat > .gitignore <<'GI'
out/
*.class
GI

echo "init-java: scaffolded src/Main.java + run.sh"
echo "           run with: ./run.sh"
