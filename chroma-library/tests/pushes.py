"""Count the outer-world levers and push domains the Engine infers for a batch (world_link._infer_pushes).
Usage: pushes.py <lib dir> <engine copy>"""
import sys, os, types, collections, numpy as np
sys.dont_write_bytecode = True
LIB = os.path.abspath(sys.argv[1]); P = os.path.abspath(sys.argv[2]); sys.path.insert(0, P); os.chdir(P)
import engine as E, batch as B, world_link as WLm, world_keys as WK
B.LIB_DIR = LIB
L = B.load_batch("earth", roles=LIB + "/earth_perks_titles.py", packs=[])
S = L["S"]; K = np.asarray(L["W_LEVER"]).shape[1]
ns = types.SimpleNamespace(lever=np.asarray(L["W_LEVER"]), push=np.asarray(L["W_PUSH"]), group=np.asarray(L.get("W_GROUP", np.full(S, -1))),
                           norm=np.asarray(L.get("W_NORM", np.full((S, K), -1))), law=np.asarray(L.get("W_LAW", np.full((S, K), -1))))
WLm.WorldLink._infer_pushes(ns, E, L, S, K)
real = np.zeros((S, K), bool)
for si in range(S):
    real[si, :len(L["notes"][si])] = True
lev = ns.lev_i[real]; dom = ns.dom_i[real]
print(f"{LIB}: {S} moments, {real.sum()} options; with a lever {int((lev >= 0).sum())}")
print("  levers:", {WK.LEVERS[i]: int((lev == i).sum()) for i in range(len(WK.LEVERS))})
print("  domains:", {WK.DOMAINS[i]: int((dom == i).sum()) for i in range(len(WK.DOMAINS)) if (dom == i).any()})
outer = (dom >= 3)
print(f"  outer rings (institution and beyond): {int(outer.sum())} options in {int((ns.dom_i >= 3).any(1).sum())} moments")
tg = collections.Counter(str(ns.tgt_i[si, ki]) for si, ki in zip(*np.nonzero(ns.dom_i == WK.DOMAINS.index('institution'))))
print("  institution targets:", dict(tg))
