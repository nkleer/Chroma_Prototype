"""NR1 commander fixture (test only, nothing in DEFAULT): the first half of N lives hold the general title from 40 (r_has
set at the week pause), then the route's own steps. Shipped set with --nat-test's climb odds.

    python3 -B chroma-engine/tools/nr1_general_fixture.py <tree> <N> <years> <seed>   (65ecdf9: 8 62 7)"""
import sys, json, collections
TREE = sys.argv[1]; N = int(sys.argv[2]); Y = int(sys.argv[3]); SEED = int(sys.argv[4])
sys.path.insert(0, TREE + '/chroma-engine/v22-speedpass'); import batch, engine as E
for k, v in E.SHIP_V25_BATCH.items(): setattr(batch, k, v)
batch.LIB_DIR = TREE + '/chroma-library'; batch.PACK_DIR = TREE + '/chroma-packs'
L = batch.load_batch('earth', packs=list(batch.PACKS)); P = dict(E.DEFAULT); P.update(E.SHIP_V25); P['world'] = True
P["wa_nat_par"] = dict(base=dict(recognition=0.5, influence=0.5, authority=0.5), rung_years=1)
gi = L["ROLES"]["names"].index("general"); FIX = list(range(N // 2)); T0 = 40 * 52
g = E.run_steps(N, Y, SEED, P, lib=L); pz = next(g)
try:
    while True:
        st = pz.state
        if pz.kind == "week" and pz.t == T0:
            for n in FIX:
                if not st["dead"][n]:
                    st["r_has"][n, gi] = True; st["r_ever"][n, gi] = True; st["r_since"][n, gi] = pz.t
        pz = g.send(pz.value)
except StopIteration as e:
    o = e.value
lg = o["national"]["log"] if isinstance(o.get("national"), dict) else []
print("fixture lives", FIX, "others", list(range(N // 2, N)))
print("general held at end:", [int(n) for n in range(N) if o["roles"]["has"][n][gi]] if "has" in o["roles"] else "?")
for x in lg:
    print(x)
wl = o.get("wa_ledger") or {}
for n, x in enumerate(wl.get("lives") or []):
    print("life", n, "decisions", x.get("decisions"), "known_weeks", x.get("known_weeks"))
nd = collections.Counter((d.get("n"), d.get("scope"), d.get("national")) for d in (wl.get("decisions_log") or wl.get("log") or []) if isinstance(d, dict))
print("decision rows (life, scope, national):", dict(nd))
