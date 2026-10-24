"""v24 Q1 asks_same (records/v24/scope.md): one preset's test/same_life.py record with the commit's defaults against the
same life with the asks parts off, step by step (each step [input, text, busy, feed, hud], as prove.py hashes it).

    python3 -B q1same.py <on.jsonl> <off.jsonl> <preset> [<drop>] [<note>]

<drop>: HUD keys left out of both sides before comparing, comma list of dotted paths (life.steer,cp.talk); empty = byte
for byte. Only Emren's reading of Q1 sets it (their card). Prints one ok or MISS line; exit 0 when the lives match."""
import json, sys


def load(p):
    try:
        return [json.loads(l) for l in open(p) if l.strip()]
    except FileNotFoundError:
        return []


def drop(step, paths):
    if not paths or len(step) < 5 or not isinstance(step[4], dict):
        return step
    hud = json.loads(json.dumps(step[4]))
    for path in paths:
        *up, last = path.split(".")
        d = hud
        for k in up:
            d = d.get(k) if isinstance(d, dict) else None
        if isinstance(d, dict):
            d.pop(last, None)
    return step[:4] + [hud] + step[5:]


def main():
    a, b, p = sys.argv[1:4]
    paths = [x for x in (sys.argv[4] if len(sys.argv) > 4 else "").split(",") if x]
    note = sys.argv[5] if len(sys.argv) > 5 else ""
    A, B = load(a), load(b)
    if A and open(a, "rb").read() == open(b, "rb").read():
        print(f"ok   preset {p}: {len(A)} steps, identical byte for byte ({note})"); return 0
    X, Y = [drop(s, paths) for s in A], [drop(s, paths) for s in B]
    if A and X == Y:
        print(f"ok   preset {p}: {len(A)} steps, identical with {', '.join(paths)} left out ({note})"); return 0
    i = next((i for i, (x, y) in enumerate(zip(X, Y)) if x != y), min(len(X), len(Y)))
    x, y = (X[i] if i < len(X) else None), (Y[i] if i < len(Y) else None)
    what = "missing" if x is None or y is None else ", ".join(n for n, u, v in zip(("input", "text", "busy", "feed", "hud"), x, y) if u != v)
    hud = sorted(k for k in set(x[4]) | set(y[4]) if x[4].get(k) != y[4].get(k)) if x and y and isinstance(x[4], dict) and isinstance(y[4], dict) else []
    print(f"MISS preset {p}: {len(A)} steps with the defaults, {len(B)} with them off; the first step that differs is {i} ({what}"
          + (f"; hud keys {', '.join(hud[:8])}" if hud else "") + (f"; {', '.join(paths)} left out" if paths else "") + ")")
    return 1


if __name__ == "__main__":
    sys.exit(main())
