"""diff_tree.py <base dir> <new dir> [allowed relative paths...]: md5 every file under both trees (no __pycache__ or .pyc)
and list files that differ, are new, or are gone. Exit 0 when only the allowed paths differ. Thread "What made it into
v21" (release checks); read only."""
import hashlib, os, sys
def tree(root):
    out = {}
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            if f.endswith(".pyc"):
                continue
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = hashlib.md5(open(p, "rb").read()).hexdigest()[:12]
    return out
a, b, allowed = tree(sys.argv[1]), tree(sys.argv[2]), set(sys.argv[3:])
diff = sorted(k for k in a.keys() & b.keys() if a[k] != b[k])
new = sorted(b.keys() - a.keys()); gone = sorted(a.keys() - b.keys())
print(f"base {sys.argv[1]}: {len(a)} files; new {sys.argv[2]}: {len(b)} files")
for k in diff: print(f"  differs {k}: {a[k]} -> {b[k]}{'' if k in allowed else '   NOT ALLOWED'}")
for k in new: print(f"  new     {k}: {b[k]}{'' if k in allowed else '   NOT ALLOWED'}")
for k in gone: print(f"  gone    {k}: {a[k]}   NOT ALLOWED")
bad = [k for k in diff + new if k not in allowed] + gone
print("RESULT", "PASS: only the allowed files differ" if not bad else f"FAIL: {len(bad)} unexpected")
sys.exit(1 if bad else 0)
