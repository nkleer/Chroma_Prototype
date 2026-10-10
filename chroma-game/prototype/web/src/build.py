"""Builds web/index.html (the published page) from head.html, sprite.svg, the visuals thread's icon set and picture map
(chroma-art/game/ink-icons.svg, ink-icons.json and pictures.json, read only; Chroma's own icons since 2026-10-05, Emren
chose "All ours"), body.html and app.js, then the ink look over it: look.css and look.js, with the pictures' lights
(chroma-art/game/lights.json, read only, made by chroma-look/tools/extract_lights.js) packed into look.js.
While web/src/option-icons-live.json exists (made by live_icons.py), it stands in for the icon set's per-option map, which
follows the Library's audited batch; delete it once that batch is live.
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
app = app.replace("__PICS__", json.dumps({k: pics[k] for k in ("situation", "domain", "tier", "tarot", "texture", "portrait") if k in pics}, separators=(",", ":")))
# lights.json: picture -> [[x, y, size, kind, strength, colour], ...] (fractions of the picture, colour "#rrggbb" or "");
# packed as "x,y,d,kind,strength,rgb|..." in thousandths and hundredths, the colour in three hex digits
def pack(ls):
    c3 = lambda c: "".join(c[i] for i in (1, 3, 5)) if isinstance(c, str) and len(c) == 7 else ""
    return "|".join(f"{round(x * 1000)},{round(y * 1000)},{round(d * 1000)},{k},{round(a * 100)},{c3(c)}" for x, y, d, k, a, c in ls)
lp = os.path.join(art, "lights.json")
# only the pictures this build has (a release branch can carry fewer pictures than lights.json knows)
lights = {k: pack(v) for k, v in json.loads(part("lights.json", art)).items()
          if v and os.path.exists(os.path.join(art, "pics", k + ".webp"))} if os.path.exists(lp) else {}
look = part("look.js").replace("__LIGHTS__", json.dumps(lights, separators=(",", ":")))
out = part("head.html") + "\n" + part("sprite.svg") + "\n" + part("ink-icons.svg", art).strip() + "\n" + part("body.html") + "\n" + app + "\n" + part("look.css") + "\n" + look
open(os.path.join(here, "..", "index.html"), "w", encoding="utf-8").write(out)
print("built web/index.html", len(out))
