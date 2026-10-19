"""Game's methods for v24 asks (chroma-ideas/next-table-2026-10-19/plan.md section 7: "asks chosen by what matters to the
character now: their aims, lacking needs, and the people at stake. That way each ask is pivotal from their point of view,
while the outer world keeps drifting them between asks"), behind GAME ask_matter (0, off: every moment weighs as before).
How often to be asked stays the player's setting (key f); this changes which moments are asked, not how many.

Part of class Game (game.py), which inherits AsksMixin. Read-only: what it reads draws nothing, so with ask_matter at 0
every life plays as before."""
import numpy as np

from game_base import E, GAME, KNAMES

PEOPLE_KINDS = ("partner", "children", "community")   # a commitment to people (foresee.PEOPLE_KINDS)
MATTER_SOON = 0.6                                     # a moment that matters this much may be asked as soon as a life event


class AsksMixin:
    def _matters(self, loc, s):
        """How much moment s matters to the character now, 0 to 1, and why: (score, dict(kind, say)) or (0.0, None).
        An option leads into the next step of an aim they hold (1); an option feeds a need they lack, by how low it is
        (up to .8); an option starts or ends a tie to people, a partner, children or a community (.6). The highest wins."""
        best = (0.0, None)
        mask = np.asarray(loc["mask"][0], bool) & ~np.asarray(loc["do_nothing"][0], bool)
        if GAME["aims"]:
            aw = self.aim_ways_view(loc) if hasattr(self, "aim_ways_view") else {}
            ws = [w for k, x in aw.items() if mask[k] for w in x]
            if ws:
                best = (1.0, dict(kind="aim", say=f"a step toward their aim, {ws[0]['aim']}"))
        if "need" in loc and best[0] < 0.8:
            need = np.asarray(loc["need"][0], float)
            fed = np.zeros(len(need))
            for k in np.nonzero(mask)[0]:
                fed = np.maximum(fed, E.NMAP @ np.maximum(loc["e"][0, k], 0))
            lack = GAME["hind_thin"]                   # a need under this is one they lack (the option row's "lift")
            low = [(float(need[j]), j) for j in range(len(need)) if fed[j] > 0.05 and need[j] < lack]
            if low:
                lv, j = min(low)
                sc = 0.4 + 0.4 * (1 - lv / lack)
                if sc > best[0]:
                    best = (round(sc, 3), dict(kind="need", say=f"something they lack, {E.NEEDS[j]}"))
        if best[0] < 0.6:
            com = np.asarray(loc["L"]["COMMIT"][s])[mask]
            ks = sorted({KNAMES[int(x)] for x in com if x >= 0 and KNAMES[int(x)] in PEOPLE_KINDS})
            if ks:
                best = (0.6, dict(kind="people", say=f"the people in their life ({ks[0]})"))
        return best
