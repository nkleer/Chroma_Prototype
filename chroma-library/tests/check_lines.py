"""v25 line tables (decisions 2, 4 and 9): earth_react_lines.py (reactions, compliance, purpose and method, why
clauses, states) and earth_aim_lines.py (why now, previews, agenda states, bottlenecks, funding, upkeep, expiry,
review, linked forks, integrated assets). Plain data that the Game fills; nothing reads them until the Engine's
react, seek and aims_v2 switches are on.
python3 -B tests/check_lines.py [chroma-library dir]    ends "no problems" or lists them
Rules checked on every string: no colour words, Magic terms or unsafe words (check_aims.py's lists); no "you" or
"your" (lines speak of {N}); the slots used are listed, so the Game knows what to fill.
Standard library only; nothing is written.
"""
import collections, os, re, sys
sys.dont_write_bytecode = True

LIB = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
sys.path.insert(0, os.path.join(LIB, "tests"))
import check_aims as CA   # its word checks and loader

FILES = ("earth_react_lines", "earth_aim_lines")
YOU = re.compile(r"\byou(r|rs|rself)?\b", re.I)
SLOT = re.compile(r"\{(\w+(?:\.\w+)?)\}")


def strings(x, path):
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from strings(v, f"{path}[{k!r}]")
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            yield from strings(v, f"{path}[{i}]")


def main():
    prob = []
    for f in FILES:
        M = CA.load(os.path.join(LIB, f + ".py"), f)
        slots, n = collections.Counter(), 0
        for name in [k for k in vars(M) if k.isupper()]:
            for where, s in strings(getattr(M, name), f"{f}.{name}"):
                n += 1
                CA.words(where, s, prob)
                if YOU.search(s):
                    prob.append(f"{where}: \"you\" in {s!r}")
                slots.update(SLOT.findall(s))
        print(f"{f}: {n} strings; slots " + ", ".join(f"{k} {v}" for k, v in sorted(slots.items())))
    if prob:
        print(f"{len(prob)} problems:")
        for p in prob:
            print("  -", p)
    else:
        print("no problems")
    return prob


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
