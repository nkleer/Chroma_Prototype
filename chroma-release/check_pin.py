"""Release check C-X1 (chroma-release/checklist.md, section 9): every file the game pinned equals its owner's copy.

Owners: the engine and world modules in the engine folder (--engine; default the frozen live v22 engine,
chroma-engine/archive/live-v22); earth.py and the pack batches in the Library batch folder (--lib; default
chroma-library, where v22's next3 is live); earth_perks_titles.py in the catalogue folder (--cat; default
chroma-library); every other earth*.py but earth_rules.py (the pack batches, earth_story.py, earth_play.py) in --lib;
dreams.py and earth_voice.py in chroma-library; the packs' catalogue, roles and helps in chroma-packs.
The game's rarity.py must hold the rarity table (--rarity; default chroma-engine/prototype/calib_v8/rarity.json, the
live one). Read only.

Defaults re-pointed 2026-10-08 after the folder cleanup (chroma-env/MAP.md): the live game is chroma-game/prototype
(staging-final was removed as a duplicate), chroma-engine/prototype carries paused v23 edits, and staging/next3 is gone
(identical to the top of chroma-library). For a v23 candidate pass --game, --engine chroma-engine/prototype, --lib and
--cat with the staged batch.

    python3 -B chroma-release/check_pin.py [--game DIR] [--engine DIR] [--lib DIR] [--cat DIR] [--rarity FILE]

Exit code 0 when every pinned file is identical to its owner's copy and nothing the engine needs is missing."""
import sys, os, argparse, filecmp, json, ast, time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py
ap = argparse.ArgumentParser()
ap.add_argument("--game", default=P["game_live"])
ap.add_argument("--engine", default=P["engine_live"])
ap.add_argument("--lib", default=P["library_live"])
ap.add_argument("--cat", default=P["library_live"])
ap.add_argument("--rarity", default=P["rarity_live"])
ap.add_argument("--live", action="store_true", help="kept for old calls; the live Library is now the default")
a = ap.parse_args()
PIN = os.path.join(a.game, "engine_pin")
EN = os.path.abspath(a.engine); LB = P["library_live"]
ST = os.path.abspath(a.lib); CAT = os.path.abspath(a.cat)


def owner(rel):
    f = os.path.basename(rel)
    if rel.startswith("packs/"):
        return path("packs_live", rel[len("packs/"):])
    if f == "earth_perks_titles.py":
        return os.path.join(CAT, f)
    if f in ("dreams.py", "earth_voice.py"):
        return os.path.join(LB, f)
    if f.startswith("earth") and f != "earth_rules.py":   # the Library's batches and story files (earth.py, the packs'
        return os.path.join(ST, f)                          # earth_<pack>.py, earth_story.py, earth_play.py); earth_rules is the engine's
    return os.path.join(EN, f)


print(f"C-X1 pin {PIN}, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC; engine {EN}; batch {ST}; catalogue {CAT}")
ok = True; n = 0
for r, _, fs in sorted(os.walk(PIN)):
    if "__pycache__" in r:
        continue
    for f in sorted(fs):
        if not f.endswith(".py"):
            continue
        rel = os.path.relpath(os.path.join(r, f), PIN); src = owner(rel); n += 1
        if not os.path.exists(src):
            print(f"MISS {rel}: no owner copy at {src}"); ok = False
        elif not filecmp.cmp(os.path.join(PIN, rel), src, shallow=False):
            print(f"MISS {rel}: differs from {src}"); ok = False
need = ["engine.py", "library.py", "combos.py", "batch.py", "earth_rules.py", "foresee.py", "explain.py", "life.py",
        "schwartz.py"] + sorted(f for f in os.listdir(EN) if f.startswith("world") and f.endswith(".py")
                                 and not f.startswith(("world_stats", "world_check", "world_test")))
for f in need:
    if not os.path.exists(os.path.join(PIN, f)):
        print(f"MISS {f}: the engine has it, the pin does not"); ok = False
rj = json.load(open(a.rarity))
rp = os.path.join(a.game, "rarity.py")
if os.path.exists(rp):
    tree = ast.parse(open(rp).read())
    val = next(ast.literal_eval(nd.value) for nd in tree.body if isinstance(nd, ast.Assign) and nd.targets[0].id == "RARITY")
    same = val == rj
    print(("ok  " if same else "MISS") + f" rarity.py {'equals' if same else 'differs from'} {a.rarity} ({rj['lives']} lives, {len(rj['sit'])} moments)")
    ok &= same
else:
    print("MISS rarity.py is not in the game copy"); ok = False
print(f"{n} pinned .py files compared")
print("C-X1:", "PASS" if ok else "FAIL")
import results; results.done('pin', 0 if ok else 1, "")   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
