"""Game's methods for v25 clash moments on the card (Emren's decision file, chroma-ideas/next-table-2026-10-19/
v25-decisions-emren.md, #3; sketch C in chroma-ideas/v25-prep/gamification/screens.md), behind GAME clash_card.
Words only: reading draws nothing.

Part of class Game (game.py), which inherits ClashMixin. A clash comes when an actual demand meets something that
matters to the life (an aim, a need, a value, a bond) with real stakes; a colour mismatch alone never makes one, so the
card names the demand's sphere and what is at stake, never the colours against each other. What it reads, from the
Engine (chroma-engine/notes/v25/contracts.md section 3):
- S["clash"]: per person, None or the clash put this week: dict(id, demand, spheres, holders, stakes, options (the
  feasible kinds), give_in_as (willing, strategic, constrained)).
- L["CLASH_TAG"][s, k]: each option's kind, an index into CLASH_KINDS (confront, give_in, leave, own_scene, bridge),
  -1 none. The option's words stay the Library's.
- S["disputes"]: per person, the open disputes, dict(id, key, since, last_asked, changed), for the agenda's count."""
import numpy as np

from game_base import ESP, GAME
from game_words import clean
from story_base import NEED_SAY

try:
    from world_keys import CLASH_KINDS
except Exception:                                    # the Engine's lane C names them (contracts.md section 3)
    CLASH_KINDS = ("confront", "give_in", "leave", "own_scene", "bridge")
KIND_SAY = dict(confront="stand up to it", give_in="go along with it", leave="leave it behind",
                own_scene="find people of their own", bridge="build a bridge")
GIVE_IN_SAY = dict(willing="they came to agree", strategic="they went along outwardly, keeping their own mind",
                   constrained="they had no real choice, and they remember it")


class ClashMixin:
    def _clash_raw(self, loc):
        c = loc.get("clash") if isinstance(loc, dict) else None
        if isinstance(c, (list, tuple)):
            c = c[0] if c else None
        return c if isinstance(c, dict) else None

    def clash_card(self, loc, s):
        """The clash this moment is about: dict(spheres=[names], stakes=[words], kinds={option k: kind}), or None when
        off, when the Engine put none this week, or when moment s is not its card."""
        if not GAME["clash_card"] or loc is None or "CLASH_TAG" not in self.L:
            return None
        c = self._clash_raw(loc)
        row = np.asarray(self.L["CLASH_TAG"])[s]
        if c is None or not (row >= 0).any():
            return None
        nm = lambda x: ((ESP.SPHERE.get(x) or {}).get("name", x) if ESP is not None else x)
        st = c.get("stakes") or {}
        aims = {}
        if hasattr(self, "_names"):
            aims = self._names(loc)
        stakes = ([aims.get(int(a), "an aim") for a in st.get("aims", [])] + [NEED_SAY.get(n, n) for n in st.get("needs", [])]
                  + [str(x) for x in st.get("commitments", [])] + (["their means"] if st.get("means") else [])
                  + [str(x) for x in st.get("access", [])])
        return clean(dict(id=str(c.get("id", "")), spheres=[nm(x) for x in c.get("spheres", [])], stakes=stakes[:4],
                          kinds={int(k): CLASH_KINDS[int(row[k])] for k in range(len(row)) if 0 <= int(row[k]) < len(CLASH_KINDS)}))

    def disputes_open(self, loc=None):
        """How many disputes are open and not asked again until something in them changes; 0 when off."""
        loc = self.loc if loc is None else loc
        if not GAME["clash_card"] or not isinstance(loc, dict):
            return 0
        d = loc.get("disputes") or []
        d = d[0] if d and isinstance(d[0], (list, tuple)) else d
        return len(d)
