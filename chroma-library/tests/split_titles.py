"""Split a titles_by_source.py result into the base catalogue (the Library) and the pack catalogues (chroma-packs).
Usage: python3 split_titles.py <titles.json> <earth_perks_titles.py>. Pack titles are judged against the shared pack budget,
not their real share (Emren 10-06 14:41, card 08:11), so the L4 targets apply to the base catalogue only (2026-10-07)."""
import json, sys, re, os, importlib.util, glob
SC = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.environ.get("CHROMA_ROOT", "/mnt/project-files"), "chroma-env"))   # folder names: chroma-env/paths.py
from paths import P as PATHS

d = json.load(open(sys.argv[1]))["titles"]
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
lib = load(sys.argv[2], "c0")
base = {x["name"] for x in lib.TITLES + lib.PERKS}
packn = {}
for pk in ["science", "politics", "stage"]:
    sys.path.insert(0, os.path.join(PATHS["packs_live"], pk))
    try:
        m = load(os.path.join(PATHS["packs_live"], pk, "catalogue.py"), "c_" + pk)
        for x in getattr(m, "TITLES", []) + getattr(m, "PERKS", []): packn[x["name"]] = pk
    except Exception as e: print(pk, "ERR", e)
    sys.path.pop(0)
print("base names", len(base), "pack names", len(packn), "both", len(base & set(packn)))
for grp, keep in [("base catalogue", lambda k: k in base and k not in packn), ("pack catalogues", lambda k: k in packn)]:
    it = [(k, v) for k, v in d.items() if v["cat"] >= .01 and keep(k)]
    me = sum(abs(v["ever"] - v["cat"]) for k, v in it) / len(it)
    over = sorted([(round(v["ever"] / v["cat"], 1), k, v["cat"], round(v["ever"], 3)) for k, v in it if v["ever"] > 2 * v["cat"] and v["ever"] - v["cat"] > .03], reverse=True)
    under = [(k, v["cat"], round(v["ever"], 3)) for k, v in it if v["ever"] < .5 * v["cat"] and v["cat"] - v["ever"] > .03]
    print(f"\n== {grp}: {len(it)} titles/perks share>=.01; mean error {me:.3f}; over 2x {len(over)}; under half {len(under)}")
    for o in over: print("  over", o, d[o[1]]["src"][:3])
    for u in under: print("  under", u, d[u[0]]["src"][:3])
