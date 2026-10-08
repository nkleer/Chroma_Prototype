"""Release check C-P3 (chroma-release/checklist.md, section 9): every gate and echo each pack proposes in
chroma-packs/<pack>/engine-conditions.py (its ECHO_* and LIFE_* tables) is in the engine's
earth_rules.PACK_RULES[<pack>]["ECHO" | "LIFE"], and names a moment of the staged pack file.

A gate missing from PACK_RULES means that moment runs without its gate (ROUND5-HANDOFF.md section 5: "Until the
re-paste, the new long-shot life events run without their gates"). Read only.

    python3 -B chroma-release/check_pack_rules.py [--proto DIR] [--batch DIR] [--packs science,politics,stage]

Exit code 0 when every key is present."""
import sys, os, argparse, importlib.util

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py
ap = argparse.ArgumentParser()
ap.add_argument("--proto", default=P["engine_live"])   # the engine to check (v22_checks.py lays a candidate there)
ap.add_argument("--batch", default=P["library_live"])
ap.add_argument("--packs", default="science,politics,stage")
a = ap.parse_args()


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


R = load(os.path.join(a.proto, "earth_rules.py"), "earth_rules_checked")
print(f"C-P3 pack gates in {os.path.join(a.proto, 'earth_rules.py')}; moments from {a.batch}")
ok = True
for p in a.packs.split(","):
    m = load(path("packs_live", p, "engine-conditions.py"), "ec_" + p)
    L = load(os.path.join(a.batch, f"earth_{p}.py"), "lib_" + p)
    names = {s["name"] for k in ("SITUATIONS", "ECHOES") for s in getattr(L, k, []) or [] if isinstance(s, dict)}
    tot = 0; miss = []; nomoment = []; differ = []   # differ: the engine holds another wording (it may reword; info)
    for var in sorted(dir(m)):
        d = getattr(m, var)
        if not (var.startswith(("ECHO_", "LIFE_")) and isinstance(d, dict)):
            continue
        have = R.PACK_RULES.get(p, {}).get(var.split("_")[0], {})
        for k in d:
            tot += 1
            if k not in have:
                miss.append(f"{var}: {k!r}")
            elif have[k] != d[k]:
                differ.append(f"{var}: {k!r}")
            if k not in names:
                nomoment.append(f"{var}: {k!r}")
    print(f"  {'ok  ' if not (miss or nomoment) else 'MISS'} {p}: {tot} keys, {len(miss)} not in PACK_RULES, "
          f"{len(nomoment)} not a moment of the staged pack")
    for x in miss:
        print(f"       not in PACK_RULES: {x}")
    for x in nomoment:
        print(f"       no such moment: {x}")
    if differ:
        print(f"       info: {len(differ)} present with other conditions than the pack proposes (the engine may reword): "
              + "; ".join(differ[:6]) + (" ..." if len(differ) > 6 else ""))
    ok &= not (miss or nomoment)
print("C-P3:", "PASS" if ok else "FAIL")
import results; results.done('packrules', 0 if ok else 1, "")   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
