"""Join a long stretch of code kept in several files back into one text, to compile as it always was.

engine._run (the life loop) lives in run_01_start.py to run_18_integrate.py and earth_rules's tables in rules_*.py:
each file holds one stretch of the lines, unchanged and at their own indent, and the owner module lists them in order
(engine.RUN_PARTS, earth_rules.RULES_PARTS). join() reads them beside the owner's own file, joins them and gives the
text and a file name to compile(); the owner runs that where the code used to stand, so the code Python runs is the
same (only file names and line numbers differ). The parts are not modules: never import or run one alone.

Python compiles a call on an imported name (np.maximum(...)) a little differently from a call on any other name, and it
knows a name is imported from the imports of the text it compiles. So join() ends the text with the owner's own
module-level imports under `if 0:` (never run, no code): the parts compile to the very code they did inside the owner.
For the same reason an owner calls this module as __import__("parts"), never `import parts`: that would make `parts`
an imported name, and a local named parts in a part (wfx_track has one) would compile differently.

A traceback names the joined text "<owner>.py+parts" and its line number in it; where() turns that into the part's
file and line (python3 -B -c "import parts, engine; print(parts.where(2345))")."""
import ast
import linecache
import os

JOINED = {}   # joined file name -> [(first line, part file)], in order


def join(names, near):
    """The joined text of the parts `names` (files <name>.py beside the file `near`) and the file name to compile it
    under. The text is put in linecache, so a traceback shows its lines."""
    here = os.path.dirname(os.path.abspath(near))
    text, at, n = [], [], 1
    for nm in names:
        with open(os.path.join(here, nm + ".py"), encoding="utf-8") as f:
            s = f.read()
        if not s.endswith("\n"):
            s += "\n"
        at.append((n, nm + ".py"))
        n += s.count("\n")
        text.append(s)
    src = "".join(text)
    with open(near, encoding="utf-8") as f:
        src += _imports(ast.parse(f.read()))
    fname = os.path.join(here, os.path.splitext(os.path.basename(near))[0] + ".py+parts")
    linecache.cache[fname] = (len(src), None, src.splitlines(True), fname)
    JOINED[fname] = at
    return src, fname


def _imports(tree):
    """`if 0:` and the module-level imports of `tree` (not those inside a function or class), one per bound name."""
    seen, out, todo = set(), [], list(tree.body)
    while todo:
        nd = todo.pop(0)
        if isinstance(nd, (ast.Import, ast.ImportFrom)):
            for a in nd.names:
                nm = a.asname or a.name.split(".")[0]
                if nm != "*" and nm not in seen:
                    seen.add(nm); out.append(f"    import os as {nm}\n")
        elif not isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            todo += [c for c in ast.iter_child_nodes(nd) if isinstance(c, ast.stmt)]
    return "if 0:   # parts.join: the owner's imports, so the parts compile as they did there (never run)\n" + "".join(out) \
        if out else ""


def where(lineno, fname=None):
    """The part file and line of line `lineno` of a joined text (the engine's _run unless `fname` names another)."""
    fname = fname or next((f for f in JOINED if f.endswith("engine.py+parts")), None)
    at = JOINED[fname]
    first, nm = max(((a, b) for a, b in at if a <= lineno), key=lambda x: x[0])
    return f"{nm}:{lineno - first + 1}"
