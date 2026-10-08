"""Every start works with the world on (the game's N=1 lives): the six game presets' settings and societies, many seeds.
Each preset burns in K worlds once (80 years alone, as the game does) and starts M single lives in a copy of each, so
the draws at birth (place, class, family tree, cast) vary over K x M seeds; each life runs Y years.
    python3 -B chroma-engine/tools/world_starts.py <first seed> <worlds K> <lives per world M> [years Y] [presets, e.g. 1,2,3]
Years above 10 print a line per life (age at death, if any); every failure prints its place in the code."""
import sys, os, json, copy, traceback
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
PROTO = _engine.ENGINE
import engine as E, batch, world as WM
s0 = int(sys.argv[1]); K = int(sys.argv[2]); M = int(sys.argv[3]); Y = int(sys.argv[4]) if len(sys.argv) > 4 else 2
PRE = (sys.argv[5] if len(sys.argv) > 5 else "1,2,3,4,5,6").split(",")
# the game's presets (chroma-game/prototype/game.py PRESETS): setting, and the society it rewards
PRESETS = {"1": ("earth", ""), "2": ("earth", "W.6 G.4"), "3": ("earth", "U.7 R.3"), "4": ("earth", "B.6 R.4"),
           "5": ("tribal", "G.5 W.3 R.2"), "6": ("magic", "U.5 W.3 B.2")}
LIBS = {}
fails = []; n = 0; felt_max = 0.0
for pk in PRE:
    setting, soc = PRESETS[pk]
    if setting not in LIBS:
        LIBS[setting] = batch.load_batch("earth", setting=setting)
    L = LIBS[setting]
    for k in range(K):
        ws = s0 + 1000 * k
        try:
            W0 = WM.World(ws, cfg=dict(setting=setting)); W0.burn_in(80)
        except Exception as ex:
            fails.append(dict(preset=pk, world=ws, error=repr(ex)[:200], where=traceback.format_exc().strip().splitlines()[-3][:200]))
            print(json.dumps(fails[-1]), flush=True); continue
        nf0 = len(fails)
        for j in range(M):
            sd = ws + j
            P = dict(E.DEFAULT); P.update(world=True, world_cfg=dict(setting=setting), world_obj=copy.deepcopy(W0))
            if soc:
                m = E.parse(soc); m = m / m.sum()
                P["f_world"] = 0.25 * (m - 0.2) * 5 / 4; P["world_profile"] = 0.6 * np.full(E.C, 0.2) + 0.4 * m
            try:
                o = E.run(N=1, years=Y, seed=sd, lib=L, P=P, log_lives=(0,))
                json.dumps(o["world"]["snapshot"]); json.dumps(o["world"]["reach"]); json.dumps(o["world"]["cast"])
                fr_ = max(max(v_["felt"]) for v_ in o["world"]["reach"].values()); felt_max = max(felt_max, fr_)
                assert 0 <= fr_ <= 1, "felt reach out of 0-1: %s" % fr_
                n += 1
                if Y > 10:
                    print(json.dumps(dict(preset=pk, world=ws, seed=sd, ok=True,
                                          died=(round(o["died"][0][1] / 52, 1) if o.get("died") else None))), flush=True)
            except Exception as ex:
                fails.append(dict(preset=pk, world=ws, seed=sd, error=repr(ex)[:200],
                                  where=traceback.format_exc().strip().splitlines()[-3][:200]))
                print(json.dumps(fails[-1]), flush=True)
        print(json.dumps(dict(preset=pk, world=ws, lives=M, failed=len(fails) - nf0)), flush=True)
print(json.dumps(dict(ran=n, failed=len(fails), felt_max=round(felt_max, 2), fails=fails[:20])))
