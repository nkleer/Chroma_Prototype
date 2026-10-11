#!/bin/bash
# G12's push_rare on N seeds, pooled (records/v22.4/scope.md, "push_rare's size"): the row's own lives are seeds 1 to 6;
# this plays seeds 1 to N, each pushed (most:<WUBRG[seed % 5]>) and left alone, and counts the rare moments each meets
# (under 1 life in 10 by the commit's game rarity table), with test/steer_check.py's own play and count. Passes, as the
# row, when the pushed lives' sum is over the left-alone lives' sum. Writes out/results.jsonl as push_rare_n<N> on SHA:
# G12 judges push_rare_n30 (Emren's "Judge on 30", 10-11 20:47 UTC).
#
#   SHA=<commit> [N=30] [REPO=/tmp/v224_repo] bash chroma-release/short-v22.4/push_rare_n.sh
F=/mnt/project-files; REPO=${REPO:-/tmp/v224_repo}; N=${N:-30}
[ -n "$SHA" ] || { echo "SHA=<commit> is needed"; exit 2; }
SHA=$(git -C $REPO rev-parse "$SHA^{commit}") || exit 2
E=/tmp/v224_pr_$(date -u +%H%M%S); O=$F/chroma-release/out/push_rare_n${N}_$(date -u +%Y%m%d-%H%M%S).txt
git -C $REPO worktree add -q --detach $E $SHA || exit 2
cd $E/chroma-game/prototype && STEER_CACHE=$E.cache python3 -B - $N $SHA $O <<'PY' | tee $O
import sys, os
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "test"))
import steer_check as S
n, sha, rep = int(sys.argv[1]), sys.argv[2], sys.argv[3]
let = [(1, s, "let", None) for s in range(1, n + 1)]
push = [(1, s, S.MOST(s), None) for s in range(1, n + 1)]
rs = S.run(let + push)
a, b = [S.rare(rs[j]) for j in let], [S.rare(rs[j]) for j in push]
d = [y - x for x, y in zip(a, b)]
print(f"push_rare on {n} seeds (1 to {n}), commit {sha[:12]}")
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
echo "report $O"; exit $rc
