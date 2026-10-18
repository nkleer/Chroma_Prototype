"""v22.2.1 V3 phone row: the candidate's phone fit against the v22.2 build's, by options, as the record's ruling words it.

    python3 -B chroma-release/check_phonefit.py <candidate report>[,<report>...] <base report>[,<report>...]

Each report is a probe_fit_cx3.js run at 390x844 (60 moments of one life). The ruling (records/v22.2.1/scope.md) asks
for no more covered or blocked options than the v22.2 build. The two builds play different lives (the clarity layer
shows fewer cards, so the probe's picks differ), so the options are counted per moment: covered options per moment and
blocked options per moment, each no more than the base's. A comma-separated list on either side pools its lives (v23,
SMALL COUNTS: one life moves about .15 a moment between runs, so the row may read more lives; the target stays): the
moments, options, covered and blocked of every report are summed before the per-moment counts are taken. Prints one
verdict line; exit 0 on PASS.
"""
import json, sys


def read1(path):
    for line in open(path):
        if line.startswith("[{"):
            m = json.loads(line)
            return {"lives": 1, "moments": len(m), "options": sum(x["n"] for x in m),
                    "covered": sum(len(x["covered"]) for x in m), "blocked": sum(len(x["blocked"]) for x in m),
                    "errors": "pageerror" in open(path).read()}
    sys.exit(f"no probe moments in {path}")


def read(paths):
    rs = [read1(p) for p in paths.split(",") if p]
    r = {k: sum(x[k] for x in rs) for k in ("lives", "moments", "options", "covered", "blocked")}
    r["errors"] = any(x["errors"] for x in rs)
    r["c"], r["b"] = r["covered"] / r["moments"], r["blocked"] / r["moments"]
    return r


cand, base = read(sys.argv[1]), read(sys.argv[2])
ok = cand["c"] <= base["c"] and cand["b"] <= base["b"] and not cand["errors"]


def say(r):
    return (f"{str(r['lives']) + ' lives, ' if r['lives'] > 1 else ''}{r['moments']} moments, {r['options']} options: "
            f"covered {r['covered']} ({r['c']:.2f} a moment), blocked {r['blocked']} ({r['b']:.2f} a moment)")


print(f"phone 390x844 by options: candidate {say(cand)}; v22.2 build {say(base)}"
      f"{'; page errors' if cand['errors'] else ''}: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
