"""Option icons for the batch the game runs. The visuals thread drew one icon per option of the Library's audited batch
(chroma-art/game/ink-icons.json, map.option), for the texts kept in web/src/ink-option-texts.json (the staged batch of
2026-10-05 14:10, moment by moment in the same order). The game's batch (engine_pin/earth.py) can word an option
differently (the live batch until the audited one goes live; later, any rewording after Emren's review), so this keeps an
icon only where the game's option has the text the icon was drawn for (same moment, any position), or replaced those
words in the same place (a rewording in place), and leaves null elsewhere: the page then falls back to the act's icon or the color's sign. Writes web/src/option-icons-live.json, which
build.py uses in place of map.option. Re-run after every re-pin of earth.py, then build.py.
Since the v22 icon update it reads the three packs too (earth_science, earth_politics, earth_stage). With --check it only
counts, and writes nothing (release check C-G2: every option keeps its drawn icon).
Run from anywhere: python3 web/src/live_icons.py [--check]"""
import importlib.util, json, os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, "..", "..", "..", "..")
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
pin = os.path.join(here, "..", "..", "engine_pin")
batches = [load(os.path.join(pin, "earth.py"), "game_earth")]          # the Earth batch and every content pack's moments (C-G2)
for f in sorted(os.listdir(pin)):
    if f.startswith("earth_") and f[6:-3] in ("science", "politics", "stage") and f.endswith(".py"):
        batches.append(load(os.path.join(pin, f), "game_" + f[:-3]))
drawn_for = json.load(open(os.path.join(here, "ink-option-texts.json"), encoding="utf-8"))["option"]
ink = json.load(open(os.path.join(root, "chroma-art", "game", "ink-icons.json"), encoding="utf-8"))["map"]["option"]
out, kept, dropped, moved = {}, 0, 0, 0
for sit in [x for B in batches for x in list(B.SITUATIONS) + list(getattr(B, "ECHOES", []))]:
    name = sit["name"]
    texts, icons = drawn_for.get(name, []), ink.get(name, [])
    drawn = {t: ic for t, ic in zip(texts, icons)}
    now = [o[0] for o in sit["options"]]
    row = [drawn.get(t) for t in now]
    if len(texts) == len(now) == len(icons):   # an option reworded in place (same moment, same place, its old text gone)
        for i, t in enumerate(now):            # keeps the icon drawn for the words it replaced
            if row[i] is None and texts[i] not in now and icons[i]:
                row[i] = icons[i]; moved += 1
    kept += sum(1 for x in row if x); dropped += sum(1 for x in row if not x)
    out[name] = row
import sys
if "--check" not in sys.argv:
    open(os.path.join(here, "option-icons-live.json"), "w", encoding="utf-8").write(json.dumps(out, separators=(",", ":")))
print(f"option-icons-live.json: {len(out)} moments, {kept} options keep their drawn icon ({moved} of them reworded in place), {dropped} fall back")
