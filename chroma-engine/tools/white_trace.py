"""White's lift, traced (v25 lane A; chroma-engine/notes/v25/other-shapes.md section 1, "White's lift"): for lives left
alone in the outer world, each part that may lift White is switched off one at a time, and the W-led share of a good
name and of Known is read against the W-led share of all lives.

Parts (each one's own switch, or the test-only engine knob trace_off):
  climb        a year present counts 1, not S3's good-name speed (trace_off "climb")
  good_name    S3, their places' eyes, off (sph_eyes; the climb's speed goes with it)
  rank         rank in a group no longer moves with an act's fit (trace_off "rank")
  lead_take    S7, ways to lead, off (lead_ways: who takes a post, and how it is held)
  title_odds   a title's weight by practice or colours 1 (trace_off "title_odds")
  footprints   foot_on off
  world_ans    the world answers off (world_answers, wa_phase2)
  callings     the Five Callings pack out of the batch
  cause_fit    cause_fit off (the loose title and perk rules)
Read at the end of the run: W-led = White the largest share of the life's pie; a good name = the title "good name in
town" ever held; Known (strict) = a height reached (the engine's heights: rung 4 leading a sphere, a good name in town,
a master's stand-in, Notable or Historic; realm_earth.HEIGHT_NAMES).

    python3 -B chroma-engine/tools/white_trace.py [N] [years] [seed] [part ...]
Defaults 40 lives, 60 years, seed 7, every part. A run of the defaults is long (each part is a whole run); the Engine
thread runs it on helpers. Library and packs: the tree's (tools/_engine.py), or CHROMA_ENGINE / its env."""
import sys, os, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np
import engine as E, batch
batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS

PARTS = {   # name: (P changes, batch without the callings pack)
    "all on": ({}, False),
    "climb": (dict(trace_off=("climb",)), False),
    "good_name": (dict(sph_eyes=False), False),
    "rank": (dict(trace_off=("rank",)), False),
    "lead_take": (dict(lead_ways=False), False),
    "title_odds": (dict(trace_off=("title_odds",)), False),
    "footprints": (dict(foot_on=False), False),
    "world_ans": (dict(world_answers=False, wa_phase2=False), False),
    "callings": ({}, True),
    "cause_fit": (dict(cause_fit=False), False),
}


def life_end(L, N, Y, seed, P_):
    """Run lives left alone (run_steps, answering nothing) and read the end: leading colour, good name, Known."""
    Pd = dict(E.DEFAULT); Pd["world"] = True; Pd.update(P_)
    g = E.run_steps(N=N, years=Y, seed=seed, lib=L, P=Pd); msg = next(g); S = None
    while True:
        kind, t, S, val = msg
        try:
            msg = g.send(val)
        except StopIteration:
            break
    w = np.asarray(S["w"], float); lead = w.argmax(1)
    names = list(L["ROLES"]["names"]); gn = names.index("good name in town") if "good name in town" in names else -1
    good = np.asarray(S["r_ever"])[:, gn].astype(bool) if gn >= 0 else np.zeros(N, bool)
    ht = S.get("ht_t")
    known = (np.asarray(ht) >= 0).any(1) if ht is not None else np.zeros(N, bool)
    return lead, good, known


def share(lead, m):
    return (f"{(lead[m] == 0).mean():.2f} ({int(m.sum())})" if m.any() else "  -  (0)")


if __name__ == "__main__":
    a = sys.argv[1:]
    N = int(a[0]) if len(a) > 0 else 40; Y = int(a[1]) if len(a) > 1 else 60; seed = int(a[2]) if len(a) > 2 else 7
    want = a[3:] or list(PARTS)
    full = batch.load_batch("earth", packs=list(batch.PACKS))
    nocall = None
    print(f"White's lift: {N} lives left alone x {Y} years, seed {seed}, world on (W-led share, and how many)")
    print(f"{'part off':<12} {'all lives':>11} {'good name':>11} {'Known':>11} {'s':>6}")
    for nm in want:
        if nm not in PARTS:
            print(f"{nm:<12} unknown part"); continue
        P_, no_call = PARTS[nm]
        if no_call and nocall is None:
            nocall = batch.load_batch("earth", packs=[p_ for p_ in batch.PACKS if p_ != "callings"])
        t0 = time.process_time()
        lead, good, known = life_end(nocall if no_call else full, N, Y, seed, P_)
        print(f"{nm:<12} {share(lead, np.ones(N, bool)):>11} {share(lead, good):>11} {share(lead, known):>11} "
              f"{time.process_time() - t0:>6.0f}", flush=True)
