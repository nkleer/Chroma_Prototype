#!/bin/bash
# G12's push_rare on N seeds, pooled (records/v22.4/scope.md, "push_rare's size"): the row's own lives are seeds 1 to 6;
# this plays seeds 1 to N, each pushed (most:<WUBRG[seed % 5]>) and left alone, and counts the rare moments each meets
# (under 1 life in 10 by the commit's game rarity table), with test/steer_check.py's own play and count. Passes, as the
# row, when the pushed lives' sum is over the left-alone lives' sum. Writes out/results.jsonl as push_rare_n<N> on SHA:
# G12 judges push_rare_n30 (Emren's "Judge on 30", 10-11 20:47 UTC).
#
#   SHA=<commit> [N=30] [PART=<first>-<last>|merge] [REPO=/tmp/v224_repo] bash chroma-release/short-v22.4/push_rare_n.sh
#
# With no PART one machine plays every seed. PART=1-6 plays seeds 1 to 6 only (each life is its own, so the counts are
# the same however the seeds split) into out/push_rare_parts_<sha12>/seed_<s>.json; PART=merge (once every seed's part
# is there) pools them into the same report and result.
F=/mnt/project-files; REPO=${REPO:-/tmp/v224_repo}; N=${N:-30}; PART=${PART:-}
[ -n "$SHA" ] || { echo "SHA=<commit> is needed"; exit 2; }
case $PART in
  ''|merge) ;;
  [0-9]*-[0-9]*) [ ${PART%-*} -ge 1 ] && [ ${PART#*-} -le $N ] && [ ${PART%-*} -le ${PART#*-} ] \
                   || { echo "PART $PART is not within seeds 1 to $N"; exit 2; } ;;
  *) echo "PART is <first>-<last> (seeds 1 to $N) or merge"; exit 2 ;;
esac
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
D=$F/chroma-release/out/push_rare_parts_${SHA:0:12}; mkdir -p $D
E=/tmp/v224_pr_$(date -u +%H%M%S); O=$F/chroma-release/out/push_rare_n${N}_$(date -u +%Y%m%d-%H%M%S).txt
[ -n "$PART" ] && [ "$PART" != merge ] && O=/dev/null
git -C $REPO worktree add -q --detach $E $SHA || exit 2
cd $E/chroma-game/prototype && STEER_CACHE=$E.cache python3 -B - $N $SHA $O "$PART" $D <<'PY' | tee $O
import sys, os, json
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "test"))
import steer_check as S
n, sha, rep, part, parts = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
if part and part != "merge":
    lo, hi = map(int, part.split("-"))
    let = [(1, s, "let", None) for s in range(lo, hi + 1)]
    push = [(1, s, S.MOST(s), None) for s in range(lo, hi + 1)]
    rs = S.run(let + push)
    for s, j, k in zip(range(lo, hi + 1), let, push):
        with open(os.path.join(parts, f"seed_{s}.json"), "w") as f:
            json.dump({"seed": s, "commit": sha, "let": S.rare(rs[j]), "push": S.rare(rs[k]), "most": k[2]}, f)
        print(f"seed {s}: left alone {S.rare(rs[j])}, pushed ({k[2]}) {S.rare(rs[k])}")
    print(f"PUSH_RARE_PART {lo}-{hi}: written to {parts}")
    sys.exit(0)
if part == "merge":
    miss = [s for s in range(1, n + 1) if not os.path.exists(os.path.join(parts, f"seed_{s}.json"))]
    if miss:
        sys.exit(f"STOP: no part yet for seeds {miss}")
    got = [json.load(open(os.path.join(parts, f"seed_{s}.json"))) for s in range(1, n + 1)]
    a, b = [g["let"] for g in got], [g["push"] for g in got]
else:
    let = [(1, s, "let", None) for s in range(1, n + 1)]
    push = [(1, s, S.MOST(s), None) for s in range(1, n + 1)]
    rs = S.run(let + push)
    a, b = [S.rare(rs[j]) for j in let], [S.rare(rs[j]) for j in push]
d = [y - x for x, y in zip(a, b)]
print(f"push_rare on {n} seeds (1 to {n}), commit {sha[:12]}" + (f", pooled from the parts in {parts}" if part else ""))
print(f"left alone: {a} (sum {sum(a)})")
print(f"pushed:     {b} (sum {sum(b)})")
print(f"seeds 1 to 6 (the row's own): left alone {sum(a[:6])}, pushed {sum(b[:6])}")
print(f"pushed minus left alone, a life: mean {sum(d) / n:+.2f}; higher in {sum(x > 0 for x in d)}, lower in {sum(x < 0 for x in d)}")
by = {c: sum(y for s, y in zip(range(1, n + 1), d) if "WUBRG"[s % 5] == c) for c in "WUBRG"}
print("by the pushed colour (summed difference): " + ", ".join(f"{c} {v:+d}" for c, v in by.items()))
ok = sum(b) > sum(a)
print(f"PUSH_RARE_N{n}: " + ("PASS" if ok else "MISS"))
sys.path.insert(0, "/mnt/project-files/chroma-release")
import results
results.add(f"push_rare_n{n}", "PASS" if ok else "FAIL", rep, f"pushed {sum(b)} against left alone {sum(a)}, seeds 1 to {n}",
            candidate={"commit": sha})
PY
rc=${PIPESTATUS[0]}; cd /; git -C $REPO worktree remove --force $E; rm -rf $E.cache
[ "$O" = /dev/null ] || echo "report $O"; exit $rc
