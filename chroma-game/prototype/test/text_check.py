"""The timeless check for a text edit, in about a second: every string literal in the game's own files that the page
loads (web/worker.js SOURCES) is scanned with test/timeless.py's own word list (REAL, read from that file, not copied),
and the hits are compared with a base, so only the words a change adds are reported. --pin scans engine_pin/ too (the
pinned engine, Library and packs; about 12 s). test/timeless.py plays four lives (7 to 9 minutes) and also sees text put
together while playing; it stays the check for releases and for code that builds text.

    python3 -B test/text_check.py               compare with origin/main (or --base REF); exit 1 on a new hit
    python3 -B test/text_check.py --all         list every hit in this tree, old ones too
    python3 -B test/text_check.py --pin         also scan engine_pin/ (a re-pin brings new Library or pack text)

Docstrings are left out (the page never shows them).
"""
import ast, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)


def words():
    """REAL and MARK as test/timeless.py defines them."""
    src = open(os.path.join(HERE, "timeless.py"), encoding="utf-8").read()
    got = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("REAL", "MARK"):
            got[n.targets[0].id] = eval(compile(ast.Expression(n.value), "timeless.py", "eval"), {"re": re})
    return got["REAL"], got["MARK"]


def literals(src):
    """Every string a file's code holds, docstrings left out; an f-string gives its literal parts."""
    t = ast.parse(src)
    docs = set()
    for n in ast.walk(t):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.body:
            d = n.body[0]
            if isinstance(d, ast.Expr) and isinstance(d.value, ast.Constant) and isinstance(d.value.value, str):
                docs.add(id(d.value))
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs:
            yield n.lineno, n.value


def sources(ref=None, pin=False):
    """{path: text} for the game's own files that web/worker.js SOURCES names (engine_pin/ too with pin), from this tree
    or from git REF (a REF without a committed engine_pin/: its owners' files, as chroma-game/tools/pin.py fills it)."""
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=GAME, capture_output=True, text=True).stdout.strip()
    src_of = {}
    if pin:
        import pinned
        pinned.ensure(GAME)
        sys.path.insert(0, pinned.TOOLS)
        import pin as P
        o = P.owners(top)
        src_of = {"engine_pin/" + d: s for s, d in P.plan(o["engine"], o["lib"], o["packs"])[0]}
    def read(p):
        if ref is None:
            return open(os.path.join(GAME, p), encoding="utf-8").read()
        for f in [os.path.join(GAME, p)] + ([src_of[p]] if p in src_of else []):
            rel = os.path.relpath(f, top).replace(os.sep, "/")
            r = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=top, capture_output=True, text=True)
            if r.returncode == 0:
                return r.stdout
        return None
    wjs = read("web/worker.js")
    out = {}
    for p in json.loads(re.search(r"const SOURCES = (\[[^\]]*\]);", wjs).group(1)):
        if p.startswith("engine_pin/") and not pin:
            continue
        s = read(p)
        if s is not None:
            out[p] = s
    return out


def hits(files, REAL, MARK):
    """(word, text) -> [where], for every word of REAL in a string literal."""
    out = {}
    for p, src in files.items():
        for line, s in literals(src):
            s2 = MARK.sub("", s)
            for m in REAL.finditer(s2):
                out.setdefault((m.group(0).lower(), s2[:160]), []).append(f"{p}:{line}")
    return out


def main():
    a = sys.argv[1:]
    base = a[a.index("--base") + 1] if "--base" in a else "origin/main"
    t0 = time.time()
    REAL, MARK = words()
    pin = "--pin" in a
    here = hits(sources(pin=pin), REAL, MARK)
    if "--all" in a:
        for (w, s), where in sorted(here.items()):
            print(f"  {w}: {s!r}  ({', '.join(where[:3])})")
        print(f"{len(here)} hits in this tree, {time.time() - t0:.1f} s")
        return 0
    old = hits(sources(base, pin), REAL, MARK)
    new = {k: v for k, v in here.items() if k not in old}
    for (w, s), where in sorted(new.items()):
        print(f"NEW {w}: {s!r}  ({', '.join(where[:3])})")
    print(f"text_check: {len(new)} new real-world word(s) against {base} ({len(here)} hits here, {len(old)} there; "
          f"--all lists them); {time.time() - t0:.1f} s")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
