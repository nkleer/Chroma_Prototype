"""v22.2.1 V3 phone row: the candidate's phone fit against the v22.2 build's, by options, as the record's ruling words it.

    python3 -B chroma-release/check_phonefit.py <candidate report> <base report>

Each report is a probe_fit_cx3.js run at 390x844 (60 moments of one life). The ruling (records/v22.2.1/scope.md) asks
for no more covered or blocked options than the v22.2 build. The two builds play different lives (the clarity layer
shows fewer cards, so the probe's picks differ), so the options are counted per moment: covered options per moment and
blocked options per moment, each no more than the base's. Prints one verdict line; exit 0 on PASS.
"""
import json, sys


def read(path):
    for line in open(path):
        if line.startswith("[{"):
            m = json.loads(line)
            k = len(m)
            c = sum(len(x["covered"]) for x in m)
            b = sum(len(x["blocked"]) for x in m)
            n = sum(x["n"] for x in m)
            return {"moments": k, "options": n, "covered": c, "blocked": b, "c": c / k, "b": b / k,
                    "errors": "pageerror" in open(path).read()}
    sys.exit(f"no probe moments in {path}")


cand, base = read(sys.argv[1]), read(sys.argv[2])
ok = cand["c"] <= base["c"] and cand["b"] <= base["b"] and not cand["errors"]


def say(r):
    return (f"{r['moments']} moments, {r['options']} options: covered {r['covered']} ({r['c']:.2f} a moment), "
            f"blocked {r['blocked']} ({r['b']:.2f} a moment)")


print(f"phone 390x844 by options: candidate {say(cand)}; v22.2 build {say(base)}"
      f"{'; page errors' if cand['errors'] else ''}: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
