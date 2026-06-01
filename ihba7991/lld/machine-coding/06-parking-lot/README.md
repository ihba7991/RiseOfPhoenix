# Parking Lot

**Tier 2 · ~90 min**

Multi-level, slot types, ticketing. Bedrock LLD problem.

## Bootstrap a Java workspace

From inside this folder:

```bash
bash "$(git rev-parse --show-toplevel)/.tools/init-java.sh"
```

That creates `src/<FolderName>MainApplication.java` (the class name is
derived from this folder, e.g. `06-parking-lot` →
`ParkingLotMainApplication`), a `run.sh` compile-and-run wrapper, and a
`.gitignore`. Edit the entry class, add more classes under `src/`, then
run `./run.sh`.

When you're done, tick the box in [`../../machine-coding.html`](../../machine-coding.html).
