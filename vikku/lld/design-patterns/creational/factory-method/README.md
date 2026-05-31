# Factory Method

Define an interface for creating an object, but let subclasses decide which class to instantiate.

## Bootstrap a Java workspace

From inside this folder:

```bash
bash "$(git rev-parse --show-toplevel)/.tools/init-java.sh"
```

That creates `src/Main.java`, a `run.sh` compile-and-run wrapper, and a
`.gitignore`. Edit `src/Main.java`, add more classes under `src/` as you
need, then run `./run.sh`.

When you're done, tick the box in [`../../../design-patterns.html`](../../../design-patterns.html).
