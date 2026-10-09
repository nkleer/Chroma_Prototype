"""Steered lives: one whole life set up through the page's own bridge (console.Console, as web/worker.js runs it), then
played on the Game object with a scripted player, as the implementation list's stage 1 checks need (Release's steered
rows; chroma-ideas/gameplay-feel.md §5 targets). Writes one JSON record of the life.
    python3 -B test/steer_check.py <preset 1-6> <seed> <player> <out.json>
player:
  let          always lets them choose
  most:<C>     always pushes the open option with the most of color C in its ways (W U B R G); their own pick when it is
               already that option
  random       a random option with ways, from the seed
  light:<C>    a light steer toward color C at every moment (P3): their own pick, tilted
The record: yearly colors and identity (history w, label; the name the player sees: name, becoming), the moments put to
the player (age, situation, own or pushed, the option's colors, success, rarity share), the pivots, the pushes accepted
and resented, trust per color, and the steps' count.
"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
preset, seed, player, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
random.seed(seed)
from console import Console
import game as G
if os.environ.get("CHROMA_GAME"):                 # settings to try, e.g. CHROMA_GAME='{"lean": 0.006}' (calibration only)
    G.GAME.update(json.loads(os.environ["CHROMA_GAME"]))
c = Console()
c.handle(""); c.handle(preset); c.handle("Ari")
g = c.g
try:
    from rarity import RARITY
except Exception:
    RARITY = {}
share = lambda sit: (RARITY.get("sit") or {}).get(sit)
prng = np.random.default_rng(seed + 31)
CI = {x: i for i, x in enumerate("WUBRG")}
asked = []
while True:
    r = g.advance()
    if r == "resolved" and asked and g.resolution:  # what came of the last pick (told at the end of its week)
        res = g.resolution
        asked[-1].update(ok=bool(res.get("worked")), pivot=(res.get("pivot") or {}).get("kind"),
                         hind=(res.get("hindsight") or {}).get("kind"))
    if r == "over" or g.over:
        break
    if r != "checkpoint":
        continue
    cp = g.pending; loc = g.loc
    m = np.maximum(np.asarray(loc["m"][0], float), 0)
    opts = [o for o in cp["options"] if o["colors"] != "-" and m[o["idx"]].sum() > 0]
    pick = None
    if player.startswith("light:"):
        k0 = int(cp["own"]); g.decide(None, light=player[6:])
        f = g._force or {}
        asked.append(dict(age=round(cp["age"], 2), sit=cp["sit"], share=share(cp["sit"]), own=not f, light=(f.get("light") or {}).get("share"),
                          colors=cp["by_idx"][f.get("idx", k0)]["colors"]))
        continue
    if player.startswith("most:") and opts:
        ci = CI[player[5:]]
        best = max(opts, key=lambda o: (m[o["idx"], ci] / m[o["idx"]].sum(), o["idx"] == cp["own"]))
        pick = best["idx"]
    elif player == "random" and opts:
        pick = opts[int(prng.integers(len(opts)))]["idx"]
    own = int(cp["own"])
    rec = dict(age=round(cp["age"], 2), sit=cp["sit"], share=share(cp["sit"]), own=pick is None or pick == own,
               colors=cp["by_idx"][own if pick is None else pick]["colors"])
    g.decide(pick)
    asked.append(rec)
h = g.history
rec = dict(preset=preset, seed=seed, player=player, age=round(g.age(), 2), game=os.environ.get("CHROMA_GAME", ""),
           w=h["w"], label=h["label"], name=h.get("name", []), asked=asked, pivots=h.get("pivots", []),
           forced=h["forced"], own=h["own"], accepted=h.get("accepted", 0), resented=h.get("resented", 0),
           trust=g.trust_view() if hasattr(g, "trust_view") else None,
           voice=g.voice_view() if hasattr(g, "voice_view") else None, light=h.get("light", 0),
           review_voice=(getattr(g, "review", None) or {}).get("voice"))
json.dump(G.clean(rec), open(out, "w"))
print(preset, seed, player, "age", rec["age"], "asked", len(asked), "pushed", rec["forced"])
