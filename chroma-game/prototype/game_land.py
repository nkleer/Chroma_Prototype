"""Game's methods for v25's land row and the land ways a person holds (land spec chroma-world/spheres/land-v1.md
sections 5 and 10, accepted by Emren 10-21; sketch D in chroma-ideas/v25-prep/gamification/screens.md), behind GAME
land_row. Words only, public facts only: reading draws nothing.

Part of class Game (game.py), which inherits LandMixin. What it reads (chroma-engine/notes/v25/other-shapes.md sections
4 and 6):
- the world's place, each week: `land` = [dict(stretch, health, wild, and the Engine's name, health_word, wild_word)]
  in the stretch order, `land_hazard` = dict(kind, age = the years since it came) or None, `harvest` (good, normal, poor,
  or 0 to 1);
- the person's `ways` = [dict(key, step, step_since_age, worked)], `bridges_open` and `bridges_held` (dict(a, b, opens),
  or "a+b" keys), in the place view beside the land (world_people_views.place_view), or in S;
- `company` at a land moment: dict(kind, cid), kind one of land.json's company kinds.
The names, hours, ladders and bridges are land.json's, as the Engine pins it (sphere_data.LAND); the words for health,
wildness and the ages are the game's, from land.json's portrait thresholds. Earth's land takes no side."""
from game_base import GAME
from game_words import clean
from game_agenda import years_say

try:
    import sphere_data
    LAND = getattr(sphere_data, "LAND", None)
except Exception:
    LAND = None
AGO = ("this year", "last year", "two years ago", "three years ago", "four years ago")
AGO_MORE = ((10, "some years ago"), (9e9, "long ago"))
HARVEST = dict(good="good", normal="fair", fair="fair", poor="poor")
COMPANY_SAY = dict(alone="alone", friend="with a friend", partner="with their partner", kin="with family", group="with a group",
                   stranger="a stranger there", witness="someone watching", rival="a rival there")


def _band(v, table):
    """land.json's portrait words: {word: lower bound}, the highest bound v reaches."""
    for w, lo in sorted(table.items(), key=lambda x: -x[1]):
        if v >= lo:
            return w
    return min(table.items(), key=lambda x: x[1])[0]


class LandMixin:
    def _land(self):
        return LAND if isinstance(LAND, dict) else None

    def land_line(self, place):
        """The portrait's land row in words, or "" when off or the Engine gives no land: each stretch's health and
        wildness, the last hazard and how long ago, the last harvest."""
        D = self._land()
        if not GAME["land_row"] or D is None or not isinstance(place, dict) or not place.get("land"):
            return ""
        words = D["portrait"]["words"]
        kind = str(place.get("kind", "")).replace("_", " ")
        names = D["stretches"]["kinds"].get(kind) or D["stretches"]["kinds"].get(place.get("kind", "")) or list(D["stretches"]["order"])
        order = list(D["stretches"]["order"])
        parts = []
        for x in place["land"]:
            st = x.get("stretch")
            i = order.index(st) if st in order else (st if isinstance(st, int) else 0)
            nm = x.get("name") or (names[i] if 0 <= i < len(names) else str(st))      # the world's own name first
            are = "are" if (nm.endswith("s") and not nm.endswith("ss")) or " and " in nm else "is"
            hw = x.get("health_word") or _band(float(x["health"]), words["health"])
            ww = x.get("wild_word") or _band(float(x["wild"]), words["wild"])
            parts.append(f"{nm} {are} {hw} and {ww}")
        hz = place.get("land_hazard")
        if hz:
            ago = max(0, int(float(hz["age"])))          # the years since it came (world_land.place)
            parts.append(f"the {str(hz['kind']).replace('_', ' ')} came "
                         f"{AGO[ago] if ago < len(AGO) else next(w for lim, w in AGO_MORE if ago < lim)}")
        hv = place.get("harvest")
        if hv is not None:
            hv = HARVEST.get(hv, hv) if isinstance(hv, str) else ("good" if hv >= 0.66 else "fair" if hv >= 0.33 else "poor")
            parts.append(f"the harvest was {hv}")
        s = "; ".join(parts)
        return s[:1].upper() + s[1:] + "." if s else ""

    def land_ways(self, loc=None):
        """The land ways they hold (at most three): dict(key, name, stretch, hours, meets, standing_in, steps=[dict(say,
        title, clock)], step, next), and the bridges: open (one half held: the other half is a door) and held (both); None
        when off or the Engine holds no ways."""
        loc = self.loc if loc is None else loc
        D = self._land()
        if not GAME["land_row"] or D is None or not isinstance(loc, dict):
            return None
        if "ways" not in loc:                           # the Engine's place view carries the life's ways and bridges
            try:
                wd = self.world_data()
                loc = (wd[0] or {}).get("place") if wd else None
            except Exception:
                loc = None
            if not isinstance(loc, dict) or "ways" not in loc:
                return None
        ws = loc["ways"]
        ws = ws[0] if ws and isinstance(ws[0], (list, tuple)) else ws
        cat = {w["key"]: w for w in D["uses"]["ways"]["list"]}
        held = []
        for x in ws or []:
            w = cat.get(x["key"])
            if w is None:
                continue
            k = int(x.get("step", 0))
            ys = w.get("ladder_years") or [None] * len(w["ladder"])
            steps = [dict(say=s_.split(" (")[0], title=(w.get("ladder_titles") or [""] * 3)[i], clock=years_say(ys[i]) if ys[i] else "")
                     for i, s_ in enumerate(w["ladder"])]
            held.append(dict(key=w["key"], name=w["name"], stretch=w["stretch"], hours=w["hours"], meets=w.get("meets", ""),
                             standing_in=w.get("standing_in", ""), steps=steps, step=k,
                             next=steps[k]["say"] if k < len(steps) else ""))
        held = held[:3]
        keys = {x["key"] for x in held}
        br = D["uses"]["ways"].get("bridges", [])
        bkey = lambda b: f"{b['a']}+{b['b']}" if isinstance(b, dict) else b
        pick = lambda v: [bkey(b) for b in ((v[0] if v and isinstance(v[0], (list, tuple)) else v) or [])]
        bopen = set(pick(loc.get("bridges_open"))); bheld = set(pick(loc.get("bridges_held")))
        bridges = []
        for b in br:
            key = f"{b['a']}+{b['b']}"
            if (b["a"] in keys and b["b"] in keys) or key in bheld:
                bridges.append(dict(opens=b["opens"], held=True, need=""))
            elif (b["a"] in keys or b["b"] in keys) and (not bopen or key in bopen or b["a"] in bopen or b["b"] in bopen):
                other = cat.get(b["b"] if b["a"] in keys else b["a"], {})
                bridges.append(dict(opens=b["opens"], held=False, need=other.get("name", "")))
        return clean(dict(ways=held, bridges=bridges[:3]))

    def company_say(self, loc):
        """Who is with them at a land moment, in words ("with a friend", "alone"), or "" when the Engine names none."""
        if not GAME["land_row"] or not isinstance(loc, dict):
            return ""
        c = loc.get("company")
        c = c[0] if isinstance(c, (list, tuple)) and c else c
        return COMPANY_SAY.get(c.get("kind", ""), "") if isinstance(c, dict) else ""
