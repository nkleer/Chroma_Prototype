"""v25's ledger readers on engine lives (Release's records/v25/checks.md): the mandatory CL0 (clash logic), AM0 (aim logic)
and NR1 (the fifteen national routes), with CL1, CL3, AM2, F5, RE3 and WA8n's rates read from the same lives. One seed a
call; v25_ledger_judge.py pools the seeds and gives one line a row.

    python3 -B chroma-engine/tools/v25_ledger_run.py <tree> <seed> <N> <years> <out.json> [--base] [--nat-test]

<tree> is a repository checkout (its chroma-engine/v22-speedpass, chroma-library and chroma-packs are run). The lives are
LA's: Earth with its packs, the outer world on, the shipped set (engine.SHIP_V25 over DEFAULT, batch.SHIP_V25_BATCH set
before the Library loads), every *_par as in code, no player. One core.
  --base       LB: the tree's DEFAULT with the world on, nothing laid over (the round 0 base, head 10, for RE3). The v25
               records are then absent and only the colours, heights and deaths are written.
  --nat-test   NR1's targeted lives: the shipped set with the national climb's yearly odds at .5 for each kind and its
               wider step after 1 year at rung 4 (wa_nat_par base .5, rung_years 1; a test setting, never shipped), so
               that every route a life can stand on is drawn. Its file is marked nat_test; the judge reads it for NR1 only.
  --nat-general  with --nat-test, NR1's commander: the general's callings ("the army needs a new general", "the war
               leader is chosen at the gathering") open after 1 year as an army officer instead of 12 or 6 (a test
               setting, never shipped), so that lives hold the general's summit and the route's step can be read; the
               file is marked nat_general

What is read, and how (no draw is added, so the lives are LA's own; the readers, v25_ledger_hook.py, wrap world_react.React
and aims2.Agenda methods in this process and only look; a played life uses the same hook, SK):
  CL0  every clash put (React._clash_check): its demand has stakes of the life's own (an aim, a commitment, its time or a
       need) at the clash threshold or more, never colour alone; no dispute put again with nothing changed (the same
       stakes and dependence and no new holder), and no new dispute on a settled one's stake with nothing changed; two
       demands on one stake with purposes as alike as clash_par merge_cos, put the same week, are one dispute (while the
       first is open); every clash answered (React._clash_apply) once, its demand and stakes on its record; at most one
       clash moment a week (a clash moment takes the week's moment, an optional ask, and adds none: an unplayed life has
       no other asks).
  AM0  over every life's agenda (aims2's log, entries and wrapped steps): a rung is reached only by a demonstrated
       outcome (a test, a contest or chance won, a title held), never by effort alone; rungs come in order; a window
       that closed is told once; no arrival after its window closed without a way round, and arrivals in the closing
       week counted (they count); a pause never moves a deadline unless the rung says pause_stops; an entry paid once a
       slot and rung; an integrated asset once a pair; an unattended life's forks resolved only by its own pick (the
       declared policy) and a player's never (with --players none are). The save, load and queue cases are SC1's.
  NR1  the national log: each route reached, by which kind and life, and the national decisions those lives took while
       Known (world answers' ledger), which is the route's asset in use.
  CL1, CL3, AM2, F5, RE3, WA8n: the clash weeks, the agenda's rung clocks, colours by year, heights, national lives.
"""
import json
import os
import sys
import time

argv = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(argv) != 5:
    sys.exit(__doc__)
TREE, SEED, N, YEARS, OUT = os.path.abspath(argv[0]), int(argv[1]), int(argv[2]), int(argv[3]), os.path.abspath(argv[4])
BASE = "--base" in sys.argv; NAT_GEN = "--nat-general" in sys.argv; NAT_TEST = "--nat-test" in sys.argv or NAT_GEN
ENG = os.path.join(TREE, "chroma-engine", "v22-speedpass")
sys.path.insert(0, ENG)
os.environ.setdefault("OMP_NUM_THREADS", "1")
import engine as E, batch   # noqa: E402
batch.LIB_DIR = os.path.join(TREE, "chroma-library"); batch.PACK_DIR = os.path.join(TREE, "chroma-packs")

import v25_ledger_hook as H   # noqa: E402  (the readers: this tools folder's v25_ledger_hook.py)

if not BASE:
    H.install()

PX = {}
if BASE:
    P = dict(E.DEFAULT)
else:
    for k_, v_ in E.SHIP_V25_BATCH.items():
        setattr(batch, k_, v_)
    P = dict(E.DEFAULT); P.update(E.SHIP_V25)
    if NAT_TEST:
        P["wa_nat_par"] = dict(base=dict(recognition=0.5, influence=0.5, authority=0.5), rung_years=1)
    if NAT_GEN:   # the general's callings after 1 year as an army officer (the Library's rule as the engine reads it)
        import earth_rules as ER
        lf_ = ER.PACK_RULES["callings"]["LIFE"]
        lf_["the army needs a new general"]["req"] = "~has('general') & (yrs_has('army officer') >= 1)"
        lf_["the war leader is chosen at the gathering"]["req"] = "~has('general') & (yrs_has('army officer') >= 1)"
P["world"] = True
L = batch.load_batch("earth", packs=list(batch.PACKS))
t0 = time.time()
o = E.run(N=N, years=YEARS, seed=SEED, lib=L, P=P)
secs = round(time.time() - t0, 1)

res = H.record(o, L, base=BASE, head=dict(
    tree=TREE, seed=SEED, N=N, years=YEARS, base=BASE, nat_test=NAT_TEST, nat_general=NAT_GEN, secs=secs,
    engine_md5=__import__("hashlib").md5(open(os.path.join(ENG, "engine.py"), "rb").read()).hexdigest()[:12]))
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f_:
    json.dump(res, f_)
print(f"{OUT}: seed {SEED}, {N} lives x {YEARS} years in {secs} s; "
      + ("base" if BASE else f"{H.CNT['puts']} clashes put, {H.CNT['answered']} answered, {H.CNT['arrived']} rungs reached, "
         f"{sum(H.VN.values())} violations ({len(H.VN)} kinds)"))
