"""Run one engine check on the release files (C-X2, 2026-10-07): python3 -B cx2run.py <script> [args...]
FINAL_LIB=<folder>: the batch (staged next3 and its catalogue earth_perks_titles.py; the packs come from chroma-packs/ and
the compiled pack moments from the same folder). NOPACKS=1: no packs. PX='{json}': defaults laid over E.DEFAULT (world on)."""
import os, sys, json, runpy
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
PROTO = _engine.ENGINE
import engine as E, batch
FINAL = os.environ["FINAL_LIB"]
E.DEFAULT.update(json.loads(os.environ.get("PX", "{}")))
batch.LIB_DIR = FINAL
_lb = batch.load_batch


def load_batch(world="earth", symmetric=False, roles=None, packs=None, pack_moments=None, setting="earth"):
    batch.LIB_DIR = FINAL
    if roles is not False:
        roles = os.path.join(FINAL, f"{world}_perks_titles.py")
    if os.environ.get("NOPACKS"):
        packs = []
    return _lb(world, symmetric, roles, packs, pack_moments, setting)


batch.load_batch = load_batch
script = sys.argv[1]; sys.argv = sys.argv[1:]
if not os.path.exists(script):   # "calib_v8/death_check.py" (the old place) or "death_check.py": the tool beside this one
    script = os.path.join(_engine.HERE, os.path.basename(script))
runpy.run_path(script, run_name="__main__")
