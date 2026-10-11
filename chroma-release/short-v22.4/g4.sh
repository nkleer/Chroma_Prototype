#!/bin/bash
# G4 "Off is v22.3" for v22.4 (records/v22.4/scope.md, ruling "G4 on the record's code with v22.3's numbers", 10-11):
# same-lives.sh part 1 (seed 41, worlds off, on and seed, and sweeps A and B) of the commit's engine, Library and packs
# against the live v22.3 engine, byte for byte, with
#  - every switch whose DEFAULT the commit moved from live v22.3 set to its UPD_OFF value (PNEW, read from the two
#    engines, not listed by hand: run.sh's OFFKEYS missed sh_will, cur_will and gap_move on ef7f273);
#  - earth_rules.py and batch.py from TABLES (default a28f91c, #207: every v22.4 part merged and off, before the refit),
#    after checking that the commit changes in them nothing but the refit's numbers: the career tables (TIER_LIFT,
#    ROLE_NORM, ROLE_ACC_FIRST, ROLE_ACC_MOVE) and the batch's pack list and moment flags (PACKS, EYES_MOMENTS,
#    SACRED_MOMENTS, LEAD_MOMENTS, GREEN_JOBS). The refit re-fits the career tables, which act on every life, so with
#    the refit's tables no switch can give v22.3's lives; G4 proves that every part's code is shut by its switch;
#  - CHROMA_PACKS=science,politics,stage (art plays in no v22.3 life; packs load before the run, so no switch can).
#
#   SHA=<commit> [TABLES=<commit>] [REPO=/tmp/v224_repo] [DRY=1] bash chroma-release/short-v22.4/g4.sh
#
# Results go to out/results.jsonl as speedpass_s41, speedpass_sweepA and speedpass_sweepB on SHA (same-lives.sh).
F=/mnt/project-files; R=${R:-$F/chroma-release}; REPO=${REPO:-/tmp/v224_repo}; TABLES=${TABLES:-a28f91c}
[ -n "$SHA" ] || { echo "SHA=<commit> is needed"; exit 2; }
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") && TABLES=$(git -C $REPO rev-parse "$TABLES^{commit}") || exit 2
E=/tmp/v224_g4/$(date -u +%H%M%S); rm -rf $E; mkdir -p $E
git -C $REPO archive $SHA chroma-engine/v22-speedpass chroma-library chroma-packs | tar -x -C $E || exit 2
D=chroma-engine/v22-speedpass
python3 -B - $REPO $TABLES $SHA <<'PY' || exit 2
import ast, subprocess, sys
repo, a, b = sys.argv[1:4]
ALLOW = {"earth_rules.py": {"TIER_LIFT", "ROLE_NORM", "ROLE_ACC_FIRST", "ROLE_ACC_MOVE"},
         "batch.py": {"PACKS", "EYES_MOMENTS", "SACRED_MOMENTS", "LEAD_MOMENTS", "GREEN_JOBS"}}
def body(c, f):
    src = subprocess.run(["git", "-C", repo, "show", f"{c}:chroma-engine/v22-speedpass/{f}"], capture_output=True,
                         text=True, check=True).stdout
    out = []
    for n in ast.parse(src).body:   # a top-level assignment to an allowed name keeps only its name
        names = {t.id for t in getattr(n, "targets", []) if isinstance(t, ast.Name)}
        out.append(("=" + ",".join(sorted(names))) if names and names <= ALLOW[f] else ast.dump(n))
    return out
bad = [f for f in ALLOW if body(a, f) != body(b, f)]
if bad:
    sys.exit(f"STOP: {', '.join(bad)} differ between {a[:12]} and {b[:12]} beyond the refit's numbers")
print(f"g4: earth_rules.py and batch.py from {a[:12]}; {b[:12]} changes nothing in them but {sorted(set().union(*ALLOW.values()))}")
PY
for f in earth_rules.py batch.py; do git -C $REPO show $TABLES:$D/$f > $E/$D/$f || exit 2; done
pnew=$(python3 -B - $E/$D $F/chroma-engine/v22-speedpass <<'PY'
import sys, os, json, importlib.util
import numpy as np
def load(d, name):
    sys.path.insert(0, d)
    sp = importlib.util.spec_from_file_location(name, os.path.join(d, "engine.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); sys.path.remove(d)
    return m
def same(x, y):
    if hasattr(x, "shape") or hasattr(y, "shape"):
        return bool(np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)))
    return x == y
N, L = load(sys.argv[1], "engine_g4"), load(sys.argv[2], "engine_live")
P, stop, note = {}, [], []
for k, v in N.DEFAULT.items():
    if k in L.DEFAULT and same(L.DEFAULT[k], v):
        continue
    if k not in N.UPD_OFF:
        (stop if k in L.DEFAULT else note).append(k)   # a new part's own setting, read only with its switch on
    elif not same(N.UPD_OFF[k], L.DEFAULT.get(k, N.UPD_OFF[k])):
        stop.append(k)
    elif not same(N.UPD_OFF[k], v):
        P[k] = N.UPD_OFF[k]
if stop:
    sys.exit("STOP: DEFAULT moved from live v22.3 with no UPD_OFF value to set back: " + ", ".join(stop))
print("g4: settings new with their parts, left as they are: " + ", ".join(note), file=sys.stderr)
print(json.dumps(P))
PY
) || { echo "$pnew"; exit 2; }
echo "g4: PNEW=$pnew CHROMA_PACKS=science,politics,stage, $SHA against the live engine"
[ -n "$DRY" ] && { echo "g4: DRY, the lives not run ($E)"; exit 0; }
cd $F && CHROMA_PACKS=science,politics,stage PNEW="$pnew" NEW=$E/$D LIB=$E/chroma-library PACKS=$E/chroma-packs \
  COMMIT=$SHA bash $R/same-lives.sh 1
