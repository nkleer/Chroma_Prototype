"""Whether two engine folders hold the same code: a split or a move that keeps every line can be shown here in seconds,
before the lives proof. Compares, between the two folders, Python's code (bytecode, constants, names; not file names or
line numbers) of engine._run with every function nested in it, of every function of engine, world_link and earth_rules,
and of every method of WorldLink, People and World (the mixins' too), and the value of every other module-level name of
those modules (pickled). Each folder is read in its own process, with PYTHONHASHSEED=0 so sets pickle alike.

usage: python3 -B chroma-engine/tools/same_code.py <old engine folder> <new engine folder>
       (e.g. a `git archive origin/main chroma-engine/v22-speedpass` in a scratch folder, and the branch's folder)
Exit code 0 when everything is the same; names only one side has are listed and do not count (a new part list, a
mixin class)."""
import hashlib
import json
import os
import pickle
import subprocess
import sys
import types

MODS = ("engine", "world_link", "earth_rules", "world_people", "world")
CLASSES = (("world_link", "WorldLink"), ("world_people", "People"), ("world", "World"))


def dump(folder):
    """{key: digest} for the folder's code and values (run in a child process)."""
    sys.path.insert(0, folder)
    import importlib
    out = {}

    def walk(co, path):
        for a in ("co_code", "co_names", "co_varnames", "co_freevars", "co_cellvars", "co_flags", "co_argcount",
                  "co_kwonlyargcount", "co_exceptiontable", "co_stacksize"):
            out[path + "." + a] = hashlib.md5(repr(getattr(co, a, None)).encode()).hexdigest()
        for i, c in enumerate(co.co_consts):
            if isinstance(c, types.CodeType):
                walk(c, path + "/" + c.co_name)
            else:
                out[f"{path}.const{i}"] = hashlib.md5(repr(c).encode()).hexdigest()

    for mn in MODS:
        m = importlib.import_module(mn)
        for k, v in sorted(vars(m).items()):
            if k.startswith("__"):
                continue
            if isinstance(v, types.FunctionType):
                if v.__module__ == mn or v.__module__.startswith(mn + "_") or mn == "engine" and k == "_run":
                    walk(v.__code__, f"{mn}.{k}()")
            elif isinstance(v, types.ModuleType):
                out[f"{mn}.{k} module"] = v.__name__
            elif not isinstance(v, type):
                try:
                    out[f"{mn}.{k}"] = hashlib.md5(pickle.dumps(v, 4)).hexdigest()
                except Exception:
                    out[f"{mn}.{k}"] = "unpicklable " + type(v).__name__
    for mn, cn in CLASSES:
        c = getattr(importlib.import_module(mn), cn)
        for k in sorted(dir(c)):
            v = getattr(c, k)
            if isinstance(v, types.FunctionType):
                walk(v.__code__, f"{cn}.{k}()")
    return out


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--dump":
        json.dump(dump(os.path.abspath(sys.argv[2])), sys.stdout)
        sys.exit(0)
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    env.pop("CHROMA_ENGINE", None)
    side = []
    for f in sys.argv[1:]:
        r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--dump", os.path.abspath(f)], env=env,
                           capture_output=True, text=True, cwd="/")
        if r.returncode:
            sys.exit(f"{f}: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'failed'}")
        side.append(json.loads(r.stdout))
    a, b = side
    both = set(a) & set(b)
    diff = sorted(k for k in both if a[k] != b[k])
    only = sorted(set(a) ^ set(b))
    print(f"same_code: {len(both)} entries in both folders, {len(diff)} differ")
    for k in diff[:40]:
        print("  DIFFERS", k)
    for k in only[:40]:
        print("  only in", "old" if k in a else "new", k)
    print("SAME CODE" if not diff else "NOT THE SAME CODE")
    sys.exit(1 if diff else 0)
