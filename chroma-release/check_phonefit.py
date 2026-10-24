"""v22.2.1 V3 phone row: the candidate's phone fit against the v22.2 build's, by options, as the record's ruling words it.

    python3 -B chroma-release/check_phonefit.py [--covered strict|no-clear-rise] <candidate report>[,<report>...]
                                                <base report>[,<report>...]

Each report is a probe_fit_cx3.js run at 390x844 (60 moments of one life). The ruling (records/v22.2.1/scope.md) asks
for no more covered or blocked options than the v22.2 build. The two builds play different lives (the clarity layer
shows fewer cards, so the probe's picks differ), so the options are counted per moment: covered options per moment and
blocked options per moment, each no more than the base's. A comma-separated list on either side pools its lives (v23,
SMALL COUNTS: one life moves about .15 a moment between runs, so the row may read more lives; the target stays): the
moments, options, covered and blocked of every report are summed before the per-moment counts are taken. Prints one
verdict line; exit 0 on PASS.

--covered no-clear-rise (v23, Emren's card choice "No clear rise", 10-18): on a phone the button bar at the foot (.evf)
covers about 1.7 options a moment at rest in both builds, so the two read equal and the strict line is a coin toss.
Covered then passes unless the candidate's covered options a moment are above the base's by more than twice the
spread of that difference (the standard error from the per-moment counts of either side). Blocked stays strict.
The default is strict, as before.
"""
import json, sys


def read1(path):
    for line in open(path):
        if line.startswith("[{"):
            m = json.loads(line)
            return {"lives": 1, "moments": len(m), "options": sum(x["n"] for x in m),
                    "covered": sum(len(x["covered"]) for x in m), "blocked": sum(len(x["blocked"]) for x in m),
                    "per": [len(x["covered"]) for x in m], "errors": "pageerror" in open(path).read()}
    sys.exit(f"no probe moments in {path}")


def read(paths):
    rs = [read1(p) for p in paths.split(",") if p]
    r = {k: sum(x[k] for x in rs) for k in ("lives", "moments", "options", "covered", "blocked")}
    r["errors"] = any(x["errors"] for x in rs)
    r["per"] = [k for x in rs for k in x["per"]]
    r["c"], r["b"] = r["covered"] / r["moments"], r["blocked"] / r["moments"]
    return r


args = sys.argv[1:]
mode = "strict"
if args[:1] == ["--covered"]:
    mode, args = args[1], args[2:]
    if mode not in ("strict", "no-clear-rise"):
        sys.exit(f"--covered takes strict or no-clear-rise, not {mode}")
cand, base = read(args[0]), read(args[1])


def var(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1) if len(xs) > 1 else 0.0


rise = cand["c"] - base["c"]
spread = (var(cand["per"]) / len(cand["per"]) + var(base["per"]) / len(base["per"])) ** 0.5
ok_c = rise <= 0 if mode == "strict" else rise <= 2 * spread
ok = ok_c and cand["b"] <= base["b"] and not cand["errors"]


def say(r):
    return (f"{str(r['lives']) + ' lives, ' if r['lives'] > 1 else ''}{r['moments']} moments, {r['options']} options: "
            f"covered {r['covered']} ({r['c']:.2f} a moment), blocked {r['blocked']} ({r['b']:.2f} a moment)")


note = f"; covered {rise:+.3f} a moment +-{spread:.3f}, no clear rise (at most {2 * spread:+.3f})" if mode != "strict" else ""
print(f"phone 390x844 by options: candidate {say(cand)}; v22.2 build {say(base)}{note}"
      f"{'; page errors' if cand['errors'] else ''}: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
