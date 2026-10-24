"""Stage 1 of v24 (plan.md §5, records/v24/scope.md A0): the heights a played life reaches, for each of Release's fixed
policies, on the Game object as the page plays it (Release's picks/impact.py play()).

    python3 -B heights_play.py <game dir with engine_pin filled> <policy> <preset> <seed> <out.json>   (env READ_GOALS=1 for reader+aims)

The record is impact.py's (well-being reading, titles) plus what the heights read: every title and perk ever held
(the engine's roles "ever" for the one life), the summit names, and each year's sphere rungs (floored), reach rings
and settings led, kept at their peak."""
import json, os, sys
gdir, policy, preset, seed, out = sys.argv[1:6]
os.environ.update(PRESET=preset, GAMEDIR=gdir, OMP_NUM_THREADS="1")
sys.path.insert(0, "/mnt/project-files/chroma-release/picks")
import impact                                      # puts the game first on sys.path and chdirs there
import numpy as np
import game as G, game_base
from world_people_base import G as GK, LEAD_KINDS

peak = dict(rung=None, standing=None, lead={k: False for k in LEAD_KINDS})
orig_y = G.Game._yearly


def _yearly(self, t, loc):
    peak["g"] = self                               # the Game playing this life
    PP = getattr(loc.get("WL"), "PP", None)
    if PP is not None:
        r = np.floor(np.asarray(PP.rung)[0])
        peak["rung"] = r if peak["rung"] is None else np.maximum(peak["rung"], r)
        if hasattr(PP, "standing"):
            s = np.asarray(PP.standing)[0]
            peak["standing"] = s if peak["standing"] is None else np.maximum(peak["standing"], s)
        me = PP.slead[0] == -2
        for k in LEAD_KINDS:
            peak["lead"][k] |= bool((me & (PP.skind[0] == GK[k])).any())
    return orig_y(self, t, loc)
G.Game._yearly = _yearly

r = impact.play(int(seed), policy)
for k in ("yrs", "asked", "content", "peace"):
    r.pop(k, None)
L = game_base._LIBS["earth"][0]
g = peak["g"]
roles = (g.result or {}).get("roles")
if roles:                                          # the life ran to its last year
    names, NT = list(roles["names"]), int(roles["NT"]); ever = np.asarray(roles["ever"]).astype(bool)[0]
else:                                              # the character died: the game keeps no result, the pause state holds it (as book() reads it)
    names, NT = list(L["ROLES"]["names"]), int(L["ROLES"]["NT"]); ever = np.asarray(g.loc["r_ever"]).astype(bool)[0]
tier = np.asarray(L["ROLES"]["TIER"])
r.update(preset=preset, read_goals=os.environ.get("READ_GOALS") == "1", NT=NT, from_result=bool(roles),
         ever=[names[i] for i in np.nonzero(ever)[0]],
         summits=[names[i] for i in range(len(names)) if i < len(tier) and tier[i] == 2],
         rung_peak=None if peak["rung"] is None else peak["rung"].tolist(),
         standing_peak=None if peak["standing"] is None else [float(x) for x in peak["standing"]], lead=peak["lead"])
json.dump(impact.json.loads(json.dumps(r, default=lambda x: x.item() if hasattr(x, "item") else str(x))), open(out + ".tmp", "w"))
os.replace(out + ".tmp", out)
print(policy, preset, seed, r["secs"], "s;", len(r["ever"]), "ever held; rung peak", r["rung_peak"], flush=True)
