# Release's v25 kit for Emren's PC (wave 1 of the integrated assessment)

Not for merging. Release's scripts laid out as the shared folder holds them (`/mnt/project-files/chroma-release/`): main's
`chroma-release/` plus Release's untracked runners and readers (short-v24, short-v25, out/v24 readers, out/heights,
out/v25 hook and judges). The PC only runs lives; Release judges the returned files in the cloud.

## Set up (once)

    sudo mkdir -p /mnt/project-files && sudo chown "$USER" /mnt/project-files
    git clone -q --depth 1 -b pc/v25-kit https://github.com/nkleer/Chroma_Prototype /mnt/project-files/_kit
    cp -r /mnt/project-files/_kit/chroma-release /mnt/project-files/

Each job takes a checkout in REPO (default /tmp/v25_repo, cloned if missing; point REPO at the PC's own checkout to skip
the clone). NOPROBE=1 skips the cloud identity probe (PC lives differ from the cloud's by SIMD level; only relative and
fixed-target rows are read from them, records/v25/evaluation.md section 5).

## Jobs on E = feature/v25 225679d (each one is sized for a 4-core machine: run 3 or 4 at once)

    E=225679d46e1c1bd254453760c00f40940857a06c
    NOPROBE=1 SHA=$E REPO=<checkout> bash /mnt/project-files/chroma-release/short-v25/run.sh <job>

In this order: wa waoff s7 mech f9a f9b f9c f9d f9e f9f c26a c26b engB1 engB2 engB3 lives f8a f8b f8c fit4 fit6.
The engine jobs run v25 as shipped through out/v25/ship_hook (the job prints "ship_hook: N patches"; 0 means it did
not take, so report it).

## Returns

Push, on a pc/ branch as before: every new file under /mnt/project-files/chroma-release/out/ (v24/wa/225679d/,
f9_225679d/, roll8_225679d_*, v22checks_*/), the new lines of /mnt/project-files/chroma-release/out/results.jsonl,
each job's console output, and md5s.
