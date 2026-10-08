"""Builds web/index.html (the published page) from head.html, sprite.svg, the visuals thread's icon set and picture map
(chroma-art/game/ink-icons.svg, ink-icons.json and pictures.json, read only; Chroma's own icons since 2026-10-05, Emren
chose "All ours"), body.html and app.js. While web/src/option-icons-live.json exists (made by live_icons.py), it stands in
for the icon set's per-option map, which follows the Library's audited batch; delete it once that batch is live.
The pictures themselves (chroma-art/game/pics/*.webp) are published next to the page as pics/...; without them the page
shows a glyph instead. Run from anywhere: python3 web/src/build.py"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
art = os.path.join(here, "..", "..", "..", "..", "chroma-art", "game")
part = lambda f, d=here: open(os.path.join(d, f), encoding="utf-8").read()
gi = json.loads(part("ink-icons.json", art))
if os.path.exists(os.path.join(here, "option-icons-live.json")):
    gi["map"]["option"] = json.loads(part("option-icons-live.json"))
pics = json.loads(part("pictures.json", art))
app = part("app.js").replace("__GI_DATA__", json.dumps(dict(map=gi["map"], credit=gi["credit"]), separators=(",", ":")))
app = app.replace("__PICS__", json.dumps({k: pics[k] for k in ("situation", "domain", "tier", "tarot", "texture") if k in pics}, separators=(",", ":")))
out = part("head.html") + "\n" + part("sprite.svg") + "\n" + part("ink-icons.svg", art).strip() + "\n" + part("body.html") + "\n" + app
open(os.path.join(here, "..", "index.html"), "w", encoding="utf-8").write(out)
print("built web/index.html", len(out))
