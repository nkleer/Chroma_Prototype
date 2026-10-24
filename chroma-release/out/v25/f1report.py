"""v25 F1 (records/v25/checks.md): the neutral world, reported, not judged.

    python3 -B f1report.py <sha7> [--heights FOLDER] [--out REPORT]

Reads <FOLDER>/engine_<sha7>_neutral/eng_*.json: lives left alone on the Engine's neutral realm (heights_engine24.py
with '{"realm": "neutral"}', LA's seeds). By leading colour at 40 and by the two leading colours at 40, the rate of
Known and of an aim half way (aim_half: some aim's ladder at least half climbed), each spread read as F2 reads its
floor (weakest over strongest, one-sided 95% bounds, cohorts of 100 lives or more) against the fair test's band, 2/3.
The verdict words are F2's arithmetic only; F1 itself is reported."""
import argparse, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r0judge as J   # noqa: E402

V = J.V


def main():
    a = argparse.ArgumentParser(); a.add_argument("sha7"); a.add_argument("--heights", default=J.H); a.add_argument("--out")
    a = a.parse_args()
    s7 = a.sha7[:7]; d = os.path.join(a.heights, f"engine_{s7}_neutral")
    L = V.engine_lives(os.path.join(d, "eng_*.json"))
    if not L:
        sys.exit(f"STOP: no lives in {d}")
    rep = [f"v25 F1, the neutral world (reported, not judged), on {s7}, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
           f"lives left alone: {len(L)} (seeds {sorted({l['seed'] for l in L})}) from {d}", ""]
    for k, lab in (("ge_known_strict", "Known"), ("aim_half", "an aim half way")):
        if all(l.get(k) is None for l in L):
            rep += [f"{lab}: not in these lives", ""]; continue
        for key, by in (("lead40", "colours"), ("pair40", "pairs")):
            r, rows, why = J.floor(L, key, k)
            rep += [f"F1 {lab} by {by}: {why} (against 2/3: {r})"] + rows + [""]
    txt = "\n".join(rep)
    print(txt)
    if a.out:
        open(a.out, "w").write(txt + "\n")


if __name__ == "__main__":
    main()
