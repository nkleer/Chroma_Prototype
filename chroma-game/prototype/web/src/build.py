"""Builds web/index.html (the published page) from head.html, sprite.svg, the visuals thread's icon set and picture map
(chroma-art/game/ink-icons.svg, ink-icons.json and pictures.json, read only; Chroma's own icons since 2026-10-05, Emren
chose "All ours"), body.html and the app (app/*.js, joined in name order inside one <script>; app.js before 10-17), then
the ink look over it: look.css and look.js, with the pictures' lights (chroma-art/game/lights.json, read only, made by
chroma-look/tools/extract_lights.js) packed into look.js, and last the clarity layer in both looks: clarity.css and
clarity.js (thread "HUD and story flow check", Emren 10-10 "apply all of them").
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
# pics-left-out.json: moment pictures this page leaves out so one published version stays within the artifact's file limit
# (511 files); those moments fall back to their part-of-life picture, as pictures.json's fallback_order says
lo = os.path.join(here, "pics-left-out.json")
out_sits = set(json.loads(part("pics-left-out.json"))["situation"]) if os.path.exists(lo) else set()
gone = {pics["situation"][k].split("/")[-1][:-5] for k in out_sits if k in pics["situation"]}
pics["situation"] = {k: v for k, v in pics["situation"].items() if k not in out_sits}
# picture packs: the rarer moments' pictures travel together in pics/pack-<n>.json ({path: base64}, PACK_SIZE to a pack;
# tools/webdir.py writes them) instead of one file each, so one published version stays under the 511 files. The
# OWN_PICS most-seen pictures (by the game's rarity.json; every domain, tier, tarot, texture and portrait picture first)
# stay files of their own. pic-packs.json records which pictures go in which pack, for webdir.py and for reading.
OWN_PICS, PACK_SIZE = 440, 25
fixed = {u for k in ("domain", "tier", "tarot", "texture") for u in pics.get(k, {}).values()} | \
        {u for d in pics.get("portrait", {}).values() for u in d.values()}
share = json.loads(part("rarity.json", os.path.join(here, "..", "..")))["sit"]
by_url = {}
for k, u in pics["situation"].items():
    by_url[u] = max(by_url.get(u, 0), share.get(k, 0))
ranked = sorted((u for u in by_url if u not in fixed), key=lambda u: (-by_url[u], u))
packed = sorted(ranked[max(0, OWN_PICS - len(fixed)):])
packs = [packed[i:i + PACK_SIZE] for i in range(0, len(packed), PACK_SIZE)]
pic_packs = {u: n for n, pk in enumerate(packs, 1) for u in pk}
open(os.path.join(here, "pic-packs.json"), "w", encoding="utf-8").write(json.dumps(dict(
    about="Moment pictures published in packs (pics/pack-<n>.json, path -> base64), made by web/src/build.py: the "
          "rarer ones by rarity.json; the page loads a pack when one of its moments shows", packs=packs), indent=1) + "\n")
# the app: web/src/app/NN-name.js, one part per group of sections, joined in name order
APP = os.path.join(here, "app")
app = "<script>\n" + "".join(part(f, APP) for f in sorted(os.listdir(APP)) if f.endswith(".js")) + "</script>\n"
app = app.replace("__GI_DATA__", json.dumps(dict(map=gi["map"], credit=gi["credit"]), separators=(",", ":")))
app = app.replace("__PIC_PACKS__", json.dumps(pic_packs, separators=(",", ":")))
app = app.replace("__PICS__", json.dumps({k: pics[k] for k in ("situation", "domain", "tier", "tarot", "texture", "portrait") if k in pics}, separators=(",", ":")))
# lights.json: picture -> [[x, y, size, kind, strength, colour], ...] (fractions of the picture, colour "#rrggbb" or "");
# packed as "x,y,d,kind,strength,rgb|..." in thousandths and hundredths, the colour in three hex digits
def pack(ls):
    c3 = lambda c: "".join(c[i] for i in (1, 3, 5)) if isinstance(c, str) and len(c) == 7 else ""
    return "|".join(f"{round(x * 1000)},{round(y * 1000)},{round(d * 1000)},{k},{round(a * 100)},{c3(c)}" for x, y, d, k, a, c in ls)
lp = os.path.join(art, "lights.json")
# only the pictures this build has (a release branch can carry fewer pictures than lights.json knows)
lights = {k: pack(v) for k, v in json.loads(part("lights.json", art)).items()
          if v and k not in gone and os.path.exists(os.path.join(art, "pics", k + ".webp"))} if os.path.exists(lp) else {}
look = part("look.js").replace("__LIGHTS__", json.dumps(lights, separators=(",", ":")))
out = part("head.html") + "\n" + part("sprite.svg") + "\n" + part("ink-icons.svg", art).strip() + "\n" + part("body.html") + "\n" + app + "\n" + part("look.css") + "\n" + look + "\n" + part("clarity.css") + "\n" + part("clarity.js")
open(os.path.join(here, "..", "index.html"), "w", encoding="utf-8").write(out)
print("built web/index.html", len(out))
