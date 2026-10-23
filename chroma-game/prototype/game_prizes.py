"""Game's methods for v25 "what this world prizes" (Emren's decision file, chroma-ideas/next-table-2026-10-19/
v25-decisions-emren.md, #10, and Emren 10-20: which colours rise more easily is a fact about the world; sketch B in
chroma-ideas/v25-prep/gamification/screens.md), behind GAME prizes. Words only: reading it draws nothing.

Part of class Game (game.py), which inherits PrizesMixin. What it reads, from the Engine (other-shapes.md sections 1
and 6, contracts.md section 8):
- S["prizes"]: each week, {sphere: [W, U, B, R, G]} for the life's town now, 1 even, above 1 counting for more toward
  standing there. It differs by town and moves with the world (the town's sphere mixes, its institutions' profiles).
- S["prizes_moves"]: the moves so far, dict(sphere, age, cause), for the "moves with the times" lines.
The words are the Library's (earth_spheres SPHERE names and FACE motives: never a colour's name). A sphere cell counts
for more at PRIZE_HI or above and for less at PRIZE_LO or below; the person's climb in a sphere reads easier or steeper
at FOR_HI and FOR_LO (their colours dotted with the sphere's row, over their sum: the tilt moves standing between
colours and never adds any). A world where every cell is even says so."""
import numpy as np

from game_base import ESP, GAME
from game_words import clean

PRIZE_HI, PRIZE_LO = 1.15, 0.87      # a sphere cell: counts for more, for less (screens.md B, agreed with the Engine)
FOR_HI, FOR_LO = 1.08, 0.93          # the person's climb there: easier, steeper
COLS = "WUBRG"
SPHERE_ORDER = ("prod", "comm", "learn", "care", "rule", "prot", "faith", "arts", "gather")


class PrizesMixin:
    def _prizes_raw(self, loc):
        P = loc.get("prizes") if isinstance(loc, dict) else None
        if isinstance(P, (list, tuple)):
            P = P[0] if P else None
        return P if isinstance(P, dict) and P else None

    def prizes_view(self, loc=None):
        """dict(rows=[dict(sphere, name, more=[motive words], less=[...], for_me)], even, moves=[dict(sphere, name, age,
        cause)]) for the world page and the places rows; None when off or the Engine gives none."""
        if not GAME["prizes"]:
            return None
        loc = self.loc if loc is None else loc
        P = self._prizes_raw(loc)
        if P is None:
            return None
        w = np.asarray(loc["w"][0], float) if "w" in loc else np.full(5, 0.2)
        w = w / w.sum() if w.sum() > 0 else np.full(5, 0.2)
        nm = lambda s: ((ESP.SPHERE.get(s) or {}).get("name", s) if ESP is not None else s)
        face = lambda s, c: ((ESP.FACE.get(f"{s}.{c}") or {}).get("name", "") if ESP is not None else "").lower()
        rows = []
        for s in sorted(P, key=lambda s: SPHERE_ORDER.index(s) if s in SPHERE_ORDER else 99):
            r = np.asarray(P[s], float)
            hi = [c for c in np.argsort(-r) if r[c] >= PRIZE_HI][:2]
            lo = [c for c in np.argsort(r) if r[c] <= PRIZE_LO][:2]
            g = float(w @ r)
            rows.append(dict(sphere=s, name=nm(s), more=[face(s, COLS[c]) for c in hi], less=[face(s, COLS[c]) for c in lo],
                             more_c="".join(COLS[c] for c in hi),
                             for_me="easier" if g >= FOR_HI else "steeper" if g <= FOR_LO else "about even"))
        moves = loc.get("prizes_moves") or []
        if moves and isinstance(moves[0], (list, tuple)):
            moves = moves[0]
        moves = [dict(sphere=m["sphere"], name=nm(m["sphere"]), age=round(float(m["age"]), 1), cause=m.get("cause", ""))
                 for m in moves][-12:]
        even = all(not x["more"] and not x["less"] for x in rows)
        return clean(dict(rows=rows, even=even, moves=moves))

    def prizes_lines(self, V=None):
        """The terminal's lines for what this world prizes."""
        V = self.prizes_view() if V is None else V
        if not V:
            return []
        if V["even"]:
            return ["what it prizes: every way counts alike here"]
        L = []
        for x in V["rows"]:
            if x["more"] or x["less"]:
                L.append(f"prizes       {x['name']}: " + (f"{' and '.join(x['more'])} count for more" if x["more"] else "")
                         + ("; " if x["more"] and x["less"] else "") + (f"{' and '.join(x['less'])} for less" if x["less"] else "")
                         + f" (for {self.name}: {x['for_me']})")
        return L
