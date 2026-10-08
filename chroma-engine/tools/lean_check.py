"""P12 (Emren's card 10:47, "Road per color"): do the holders of each pack road lean to the road's lead color?
    python3 -B chroma-engine/tools/lean_check.py <lib dir> <N> <seed> <out.npz>      one run (packs on, engine defaults)
    python3 -B chroma-engine/tools/lean_check.py sum <lib dir> <npz> [npz...]         the table
Per road: each holder's colors in the year after they first gain one of its titles, minus everyone's mean at that age,
pooled over the road's titles; the lead color should lean most. And per pack, its moments as met: the share of their open
options by means color, weighted by how often each moment is met (the Packs keep the offer even, .200 each).
Roads and lead colors: chroma-packs/<pack>/PACK.md, "Road(s) per color" (round 5)."""
import os, sys, importlib.util
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E, batch
ROADS = {
    "science": [("U", "the lab researcher", ["research assistant", "research scientist", "research software engineer", "professor"]),
                ("B", "the research leader", ["research project lead", "research group leader"]),
                ("R", "the communicator, the one who goes alone", ["science communication specialist", "independent investigator"]),
                ("W", "the evidence and the shared record", ["evidence synthesis specialist", "citizen scientist"]),
                ("G", "the place, the facility and the long record", ["research facility lead", "research data steward",
                  "participatory research coordinator", "community observer", "volunteer research organiser"])],
    "politics": [("W", "party and office", ["party official", "polling-station volunteer", "member of parliament", "minister", "head of government"]),
                 ("U", "policy and polling", ["policy analyst", "pollster"]),
                 ("B", "lobbying and the back room", ["lobbyist", "political adviser"]),
                 ("R", "campaigning and the bold bid", ["campaign volunteer", "campaign organiser", "speechwriter", "party leader"]),
                 ("G", "the ward, the caseworker and the town", ["constituency caseworker", "local party officer", "mayor"])],
    "stage": [("R", "acting and the lead", ["professional actor", "lead actor or actress"]),
              ("U", "writing, directing, voice and teaching", ["playwright or screenwriter", "director", "voice actor", "drama teacher"]),
              ("W", "stage management, casting and running a theatre", ["stage manager", "casting director", "artistic director"]),
              ("B", "producing and agents", ["producer", "talent agent"]),
              ("G", "community theatre and the extras", ["amateur actor", "community theatre director", "background artist",
                "youth theatre member", "a lead role to remember"])]}
COL = "WUBRG"


def pack_names(D):
    out = {}
    for pk in ROADS:
        s = importlib.util.spec_from_file_location("m_" + pk, os.path.join(D, f"earth_{pk}.py")); m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m); out[pk] = {x["name"] for x in m.SITUATIONS} | {x["name"] for x in getattr(m, "ECHOES", [])}
    return out


def load(D):
    batch.LIB_DIR = D
    return batch.load_batch("earth", roles=os.path.join(D, "earth_perks_titles.py"))


if sys.argv[1] != "sum":
    D, N, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    L = load(D)
    o = E.run(N=N, years=80, seed=seed, lib=L)
    W = np.asarray(o["W_hist"]); G = o["roles"]["names"]; NI = len(G)
    first = {}
    for n, t, i, what, how in o["roles"]["log"]:
        first.setdefault((n, i), t)
    dsum = np.zeros((NI, 5)); dcnt = np.zeros(NI)
    for (n, i), t in first.items():
        a = min(int(t / 52) + 1, len(W) - 1)
        dsum[i] += W[a][n] - W[a].mean(0); dcnt[i] += 1
    np.savez(out, names=np.array(G), dsum=dsum, dcnt=dcnt, sit_n=o["sit_n"].sum(0), sit_names=np.array(L["names"]), N=N,
             pie=np.array([W[a].mean(0) for a in (20, 40, 70)]))
    print(f"wrote {out}: {N} lives, {len(first)} title gains")
else:
    D = sys.argv[2]; fs = [np.load(f) for f in sys.argv[3:]]
    G = list(fs[0]["names"]); dsum = sum(f["dsum"] for f in fs); dcnt = sum(f["dcnt"] for f in fs); N = sum(int(f["N"]) for f in fs)
    sit_n = sum(f["sit_n"] for f in fs); names = list(fs[0]["sit_names"])
    print(f"{N} lives, packs on, engine defaults. Lean = holders' colors the year after first gaining the title, minus everyone's at that age.")
    allok = True
    for pk, roads in ROADS.items():
        print(f"\n== {pk}")
        for lead, road, titles in roads:
            ii = [G.index(t) for t in titles if t in G]
            miss = [t for t in titles if t not in G]
            n_ = dcnt[ii].sum(); d = dsum[ii].sum(0) / max(n_, 1)
            top = COL[int(np.argmax(d))]; ok = top == lead
            allok &= ok or n_ < 20
            print(f"  {lead} {road[:48]:48s} holders {int(n_):4d}  lean " + " ".join(f"{c}{x:+.3f}" for c, x in zip(COL, d))
                  + f"  leans most to {top}: {'few holders' if n_ < 20 else ('PASS' if ok else 'MISS')}" + (f"  (not in catalogue: {miss})" if miss else ""))
            for i in ii:
                if dcnt[i]:
                    di = dsum[i] / dcnt[i]
                    print(f"      {G[i][:40]:40s} {int(dcnt[i]):4d}  " + " ".join(f"{c}{x:+.3f}" for c, x in zip(COL, di)) + f"  top {COL[int(np.argmax(di))]}")
    # the offer as met: open options' means colors in each pack's moments, weighted by how often each moment is met
    L = load(D); M = np.asarray(L["M"]); MK = np.asarray(L["MASK"]); PN = pack_names(D)
    print("\n== the packs' moments as met: share of open options by means color (target about .200 each)")
    for pk in ROADS:
        acc = np.zeros(5); wt = 0.0
        for s, nm in enumerate(L["names"]):
            if nm in PN[pk] and nm in names:
                c = sit_n[names.index(nm)]
                if c <= 0:
                    continue
                k = MK[s] & (M[s].std(1) > 1e-9)
                if k.any():
                    acc += c * M[s][k].mean(0); wt += c
        sh = acc / max(wt, 1e-9)
        print(f"  {pk:9s} " + " ".join(f"{c} {x:.3f}" for c, x in zip(COL, sh)) + f"   largest gap from .200: {np.abs(sh - .2).max():.3f}")
    pie = sum(f["pie"] * int(f["N"]) for f in fs) / N
    for a, p in zip((20, 40, 70), pie):
        print(f"pie at {a}: " + " ".join(f"{c} {x:.3f}" for c, x in zip(COL, p)))
    print("\nALL ROADS LEAN TO THEIR LEAD COLOR" if allok else "\nSOME ROAD MISSES ITS LEAD COLOR")
