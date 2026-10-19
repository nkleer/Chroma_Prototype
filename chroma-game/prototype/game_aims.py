"""Game's methods for v24 aims (chroma-ideas/next-table-2026-10-19/plan.md section 5, Game: "an aims track on the
sheet and in the HUD: where they stand, the next step, what helps; choosing among the aims the character already feels,
or setting one; the hover shows which aim a pick serves"), behind GAME aims, with the Engine's aims and heights.

Part of class Game (game.py), which inherits AimsMixin. What it reads, from the Engine's foresee.py (none of it draws):
- aims(S, n): the aims held, each with its ladder of steps, how far along, the next step and the titles and perks that
  make it; "set by you" until a spark makes it the character's own; a calling when held long and leading to a height.
- aim_choices(S, n): the aims the character already feels (their dreams, passions and plans read as aims), then the
  nearest to who they are now.
- set_aim(S, n, name), drop_aim(S, n, slot): the player's two acts. These change the life; nothing else here does.
- aim_ways(S, n), when the Engine has it: at a choice, which options are a way into an aim's next step."""
import numpy as np

from game_base import E, F, GAME
from game_words import clean


class AimsMixin:
    def aims_view(self, loc=None):
        """The aims track: [dict(slot, aim, face, domain, own, by_player, strength, calling, steps=[dict(say, height,
        reached)], reached, next, helps)], strongest first; None when off."""
        loc = self.loc if loc is None else loc
        if not GAME["aims"] or loc is None or not hasattr(F, "aims"):
            return None
        out = [dict(x, steps=[dict(s_) for s_ in x["steps"]], helps=[self.gword(h) for h in x["helps"]])
               for x in F.aims(loc, 0)]
        return clean(sorted(out, key=lambda x: (not x["calling"], -x["strength"])))

    def aim_choices_view(self, k=6):
        """The aims they could take up now: the ones they already feel first. [] when off or not paused."""
        S = self._paused_locals()
        if not GAME["aims"] or S is None or not hasattr(F, "aim_choices"):
            return []
        return clean(F.aim_choices(S, 0, k))

    def aim_set(self, name):
        """The player sets an aim by its name: (slot, None) or (-1, why)."""
        S = self._paused_locals()
        if not GAME["aims"] or S is None or not hasattr(F, "set_aim"):
            return -1, "aims are off"
        q, err = F.set_aim(S, 0, name)
        if q >= 0:
            self.history.setdefault("aims_set", []).append((round(self.age(), 1), name))
        return int(q), err

    def aim_drop(self, slot):
        """The player lets an aim go; True when there was one in that slot."""
        S = self._paused_locals()
        if not GAME["aims"] or S is None or not hasattr(F, "drop_aim"):
            return False
        x = [a for a in (self.aims_view(S) or []) if a["slot"] == int(slot)]
        ok = bool(F.drop_aim(S, 0, int(slot)))
        if ok and x:
            self.history.setdefault("aims_dropped", []).append((round(self.age(), 1), x[0]["aim"]))
        return ok

    def aim_ways_view(self, loc):
        """At a choice: {option k: [dict(aim, step, height, if_fails)]} for the options that lead into an aim's next step;
        {} when off or the Engine has no aim_ways."""
        if not GAME["aims"] or loc is None or not hasattr(F, "aim_ways"):
            return {}
        return {int(k): [dict(aim=w["aim"], step=w["step"], height=w["height"], if_fails=bool(w["if_fails"])) for w in ws]
                for k, ws in F.aim_ways(loc, 0).items()}

    def aim_lines(self, loc=None):
        """The sheet's aims rows (status, the terminal)."""
        L = []
        for x in self.aims_view(loc) or []:
            k = x["reached"]; n = len(x["steps"])
            tags = (["a calling"] if x["calling"] else []) + (["set by you"] if not x["own"] else [])
            L.append(f"aim          {x['aim']} [{x['face']}]: step {k} of {n}"
                     + (f", next: {x['next']}" if x["next"] else ", every step reached")
                     + (f" (helps: {', '.join(x['helps'][:3])})" if x["helps"] else "")
                     + (f" [{', '.join(tags)}]" if tags else "") + f", strength {x['strength'] * 100:.0f}%")
        return L

    def heights_view(self, loc=None):
        """The heights reached (Known, Notable, Historic) and the age at each, when the Engine records them; [] else."""
        loc = self.loc if loc is None else loc
        if not GAME["aims"] or loc is None or loc.get("ht_t") is None:
            return []
        ht = np.asarray(loc["ht_t"])[0]
        names = getattr(E, "AIM_HEIGHTS", ("Known", "Notable", "Historic"))
        return [dict(height=names[i], age=round(float(ht[i]) / 52, 1)) for i in range(min(len(names), len(ht))) if ht[i] >= 0]
