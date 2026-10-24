"""Release's reader for the v24 bar rows N1, N2 and N3, needs that fit life (records/v24/scope.md; plan.md section 4;
chroma-ideas/next-table-2026-10-19/needs-research.md sections 5 and 7). The Engine tunes its joint refit against this
reading, so every definition it uses is written here.

    python3 -B needs_check.py run <tree> <seed> <N> <years> <out.json> [--px '<json>']
    python3 -B needs_check.py judge <dir> [--base <dir>] [--out report.txt]

run   N engine lives left alone (no player, no intervention), Earth with its packs (batch.PACKS), the outer world on, from
      a whole tree (chroma-engine, chroma-library, chroma-packs), driven as Release's out/heights/heights_engine.py
      drives them: P = engine.DEFAULT, then world True, then --px on top. need_why is then set True whatever --px says:
      it is a record only (no draw; engine.py DEFAULT: "every life plays the same with it on or off") and the week's
      setback is read from it. The run goes through run_steps with every value sent back unchanged (the same lives as
      run()). Writes one small JSON: needs, satisfaction and peace by year of age, every setback with its world facts,
      and how many life-weeks each world fact was seen at (for the rates).
      The needs switches on (engine commit b2963ef, "needs that fit life (off)"; t_steps row 19's on values):
          --px '{"need_tab": "v7", "shared_hist": 0.3, "imp_age": true}'
      Release's real runs: 100 years (the U-shape needs ages to 70, N1 the bands to 79), 400 lives a seed, seeds 41 to
      44, one process a seed. 40 lives x 40 years took 74 s wall on one core (2026-10-19, t_519).
judge pools every run JSON in <dir> (one per seed) and prints one line per row (PASS or MISS, the numbers, how many
      lives were read), then the tables behind them. With --base <dir> (the same seeds, N and years on the base), each
      reading is put side by side with the base and its move. For the record the base is v23.2's lives (a
      release/v23.2 tree); main with the switches off is a tuning reading only.

What is read (Release's readings; the plan and the note set no numbers for N1 and N2):
- Needs: the engine's five (engine.NEEDS: safety, belonging, autonomy, competence, meaning, each 0 to 1), satisfaction
  (the engine's "content"; engine.reading calls it satisfaction) and peace, read from run()'s V_hist at the first week
  of each year of age, as chroma-engine/tools/t_satisf.py reads them. A band's mean (0-9, 10-19, ..., 80-89, and 90-99
  in a 100-year run) is over every living life-year in it; seeds pool by life-years.
- The U-shape, as Release reads the `satisf` row (t_satisf.py; checklist C-E10 "U-shape (lowest at 50)"; v22.5's F19
  "contentment at 50 below both 40 and 60, and 70 above 50"): pooled mean satisfaction at the single ages 20, 30, 40,
  50, 60 and 70 (the ages t_satisf prints). It holds when the lowest of the six is at 40, 50 or 60 (a midlife low) and
  both 20 and 70 lie above that low. A run that stops before 70 cannot show it: the rows that need it are then MISS.
  t_satisf runs Earth without packs and the world off; here it is read on these lives (packs, world on).
- N1 needs_age. PASS when the run has every needs switch on (need_tab "v7", shared_hist above 0, imp_age true), the
  U-shape holds, and no need's band mean in the bands 10-19 to 70-79 is below .10 (collapsed) or above .95
  (saturated). The research note gives sources for the tables, not targets by age, so the realism check is the U-shape
  `satisf` already reads plus no need collapsing or saturating over the working years.
- N2 needs_alone. Well-being: mean satisfaction and mean peace over the living life-years of ages 20 to 79 (to the
  run's last age when shorter). PASS when each is not below the base's by more than the noise, and the U-shape holds.
  The noise is two standard errors of the difference of the pooled means, 2 x sqrt(s_run^2 / k_run + s_base^2 / k_base),
  with s the standard deviation (ddof 1) of the per-seed means and k the number of seeds on that side. A side with
  fewer than two seeds cannot give s: its s / sqrt(k) is then replaced by the standard deviation of its per-life means
  over sqrt(lives), and the report says so (this understates the noise: the lives of one run share one world).
  Without --base, N2 is a MISS (there is no floor to read against).
- N3 needs_setbacks. Every setback is an IMPOSITIONS draw (engine run_14_marks.py, `imp = rng.random(N) < impose_p`),
  read at the week's end pause from need_why's nw_imp (the kind) and nw (its own need moves, source "setback"). The
  gate and "half to" ages are the note's section 5 table, held as data below (GATES, each row with its line). Counted:
    below gate   a setback at an age below its gate;
    half window  a setback at an age from its gate up to its "half to" age; it must be half size. Its size is the sum of
                 its own need moves over the five needs; it reads as halved when at most .75 of the median size of the
                 same kind at or after its "half to" age (half is .5; the margin is for the clip at 0, which can only
                 make a hit smaller). One at full size is counted;
    no cause     a setback with no cause handed over. The engine hands a cause over when its end-pause state has one of
                 CAUSE_KEYS (per life, this week's setback's cause; none exists at main). The Game's panel shows what
                 the engine hands it: the report also says whether the panel (chroma-game/prototype/game_because.py)
                 reads that key, since "a cause the panel names" needs both.
  PASS (Release's reading of the row, 10-19 21:10 UTC, with Emren's card "Cause now, world fit v25", 10-20) when none
  is below its gate and none is without a cause the panel reads (a cause key handed over and the panel reading it).
  The world fit is read and printed, not in the PASS until v25: every world-tied kind whose fact varies in the lives
  read follows its world when its rate where the fact is high exceeds its rate where it is low by two standard errors
  or more ((high - low) / sqrt(high + low) >= 2, the two halves holding equal life-weeks); a kind whose facts do not
  vary is not read. The half window is read and printed,
  not in the PASS: the plan asks that setbacks fit age, and halving is the note's proposal. The world reading (for
  each world-tied kind, its weekly rate where
  its world fact is in the upper half of the life-weeks seen against the lower half, at ages 18 and over, where every
  gate and half window has passed, so that a kind's rate is flat in age when nothing in the world moves it; all lives of
  a run share one age at a time, so a fact of the whole world is read across seeds best; above 1 means it follows its
  world), "made dependent" at 70 and over against 16 to 69 (the note: "rate rising after 70"), and the rates by kind
  and age. The world facts, per life and week: crime, the locality's crime (W.loc_crime at PP.loc); harm, 1 when the
  locality is struck by or recovering from a disaster or the country is at war (W.disaster_now, W.loc_disaster,
  W.war); frail, 1 minus the life's health (res "health"); and for the whole world weak, 1 minus the rule of law
  (W.law_rule), and repress, 1 minus the mean of the five rights (W.rights). The engine draws nothing before age 3
  (run_09_week.py: the rest of the week is skipped before 3), so a gate at 1 is met by the week itself.

Run on at most a core or two (OMP_NUM_THREADS=1), one process a seed. Timing: see the JSON's "secs"."""
import argparse, glob, json, math, os, re, sys, time

NEEDS_ON = dict(need_tab="v7", shared_hist=0.3, imp_age=True)   # the needs switches and their on values (see above)
NOTE = "chroma-ideas/next-table-2026-10-19/needs-research.md"
# needs-research.md section 5, "Setbacks by age and world" (md5 3edf1bec1c3a1c773c6cb5dddfbba2a6 on 2026-10-19):
# (setback, gate, "half to" age or None, the note's line and Gate cell). "none" and "birth" read as 0.
GATES = [
    ("a rule is imposed on you", 10, 12, "line 99: 10, half to 12"),
    ("an institution betrays its promise", 12, None, "line 100: 12"),
    ("you are lied to and misled", 5, None, "line 101: 5"),
    ("someone takes what you earned", 4, None, "line 102: 4"),
    ("your community or habitat is damaged", 0, None, "line 103: none"),
    ("you are forbidden to see someone you love", 1, None, "line 104: 1"),
    ("evidence you trusted is overturned", 14, 18, "line 105: 14, half to 18"),
    ("you are made dependent on others", 16, None, "line 106: 16; rate rising after 70"),
    ("your traditions are mocked or banned", 7, 12, "line 107: 7, half to 12"),
    ("lawlessness spreads around you", 0, None, "line 108: none"),
]
SHORT = {"a rule is imposed on you": "rule", "an institution betrays its promise": "betray",
         "you are lied to and misled": "lied", "someone takes what you earned": "taken",
         "your community or habitat is damaged": "damaged", "you are forbidden to see someone you love": "kept from",
         "evidence you trusted is overturned": "overturned", "you are made dependent on others": "dependent",
         "your traditions are mocked or banned": "mocked", "lawlessness spreads around you": "lawless"}
CAUSE_KEYS = ("nw_imp_cause", "imp_cause", "setback_cause", "nw_imp_why")   # where a setback's cause would be handed over
FACTS = ("crime", "harm", "frail", "weak", "repress")   # the first three per life, the last two the world's
KIND_FACTS = {   # the note's section 5 "World": which fact each world-tied setback should follow
    "lawlessness spreads around you": ("crime", "weak"),
    "an institution betrays its promise": ("weak", "crime"),
    "a rule is imposed on you": ("repress",),
    "your traditions are mocked or banned": ("repress",),
    "your community or habitat is damaged": ("harm",),
    "you are made dependent on others": ("frail",),
}
NB = 50                                    # bins of .02 for the facts' life-weeks
WORLD_FROM = 18                            # N3 world reading: ages from 18 (every gate and half window passed)
UAGES = (20, 30, 40, 50, 60, 70)           # t_satisf's ages
LO, HI = 0.10, 0.95                        # N1: collapse and saturation
N1_BANDS = (10, 79)                        # N1: the bands read for collapse and saturation
WELL = (20, 79)                            # N2: the ages of well-being
HALF_K = 0.75                              # N3: a half-window hit at most this share of the kind's full size
TAG = "needs_check run v1"


# ---------------------------------------------------------------------------------------------------------------- run
def cmd_run(a):
    tree = os.path.abspath(a.tree); eng = os.path.join(tree, "chroma-engine", "v22-speedpass")
    sys.path.insert(0, eng)
    import numpy as np
    import engine as E, batch
    batch.LIB_DIR = os.path.join(tree, "chroma-library"); batch.PACK_DIR = os.path.join(tree, "chroma-packs")
    px = json.loads(a.px) if a.px else {}
    t0 = time.time()
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    P = dict(E.DEFAULT); P["world"] = True; P.update(px); P["need_why"] = True
    N, Y = a.N, a.years
    kinds = [x[0] for x in E.IMPOSITIONS]
    SB = list(E.NSOURCES).index("setback"); HEA = E.RIDX["health"]
    ev = {k: [] for k in ("t", "n", "k", "size", "crime", "harm", "frail", "cause")}
    causes = []; cause_key = None; first_end = None; unread = 0
    expo_age = np.zeros(Y, np.int64)
    expo = {f: np.zeros((Y, NB), np.int64) for f in FACTS}
    wk = {"t0": None, "weak": [], "repress": [], "war": [], "unrest": []}

    def b(x):
        return np.clip((np.asarray(x, float) * NB).astype(int), 0, NB - 1)

    g = E.run_steps(N=N, years=Y, seed=a.seed, P=P, lib=L)
    p = next(g)
    try:
        while True:
            if p.kind == "end":
                S = p.state; t = int(p.t); ay = min(t // 52, Y - 1)
                if first_end is None:
                    first_end = t
                    cause_key = next((k for k in CAUSE_KEYS if k in S), None)
                dead = np.asarray(S.get("dead", np.zeros(N, bool)), bool); live = ~dead
                expo_age[ay] += int(live.sum())
                WL = S.get("WL"); fx = {}
                if WL is not None:
                    W, PP = WL.W, WL.PP; loc = np.asarray(PP.loc, int)
                    fx["crime"] = np.asarray(W.loc_crime, float)[loc]
                    fx["harm"] = ((np.asarray(W.loc_disaster, float)[loc] > 0) | (np.asarray(W.disaster_now, float)[loc] > 0)
                                  | (int(W.war) > 0)).astype(float)
                    fx["weak"] = np.full(N, 1 - float(W.law_rule)); fx["repress"] = np.full(N, 1 - float(np.mean(W.rights)))
                    if wk["t0"] is None:
                        wk["t0"] = t
                    wk["weak"].append(round(1 - float(W.law_rule), 3)); wk["repress"].append(round(1 - float(np.mean(W.rights)), 3))
                    wk["war"].append(int(W.war)); wk["unrest"].append(round(float(W.unrest), 3))
                fx["frail"] = 1 - np.asarray(S["res"], float)[:, HEA]
                for f, v in fx.items():
                    np.add.at(expo[f][ay], b(v)[live], 1)
                imp = S.get("nw_imp"); nw = S.get("nw")
                if imp is None or nw is None:   # an engine without need_why: no setback can be read
                    unread += 1; imp = np.full(N, -1)
                imp = np.asarray(imp)
                for n in np.nonzero((imp >= 0) & live)[0]:
                    ev["t"].append(t); ev["n"].append(int(n)); ev["k"].append(int(imp[n]))
                    ev["size"].append(int(round(1000 * float(np.abs(nw[n, SB]).sum()))))
                    for f, m in (("crime", 100), ("harm", 1), ("frail", 100)):
                        ev[f].append(int(round(m * float(fx[f][n]))) if f in fx else -1)
                    c = None
                    if cause_key is not None:
                        c = S[cause_key][n]
                        c = None if c is None or (isinstance(c, (int, float)) and c < 0) or str(c) in ("", "None") else str(c)
                    if c is None:
                        ev["cause"].append(-1)
                    else:
                        if c not in causes:
                            causes.append(c)
                        ev["cause"].append(causes.index(c))
            p = g.send(p.value)
    except StopIteration as done:
        o = done.value
    secs = round(time.time() - t0, 1)
    # needs, satisfaction and peace by year of age, over the living
    need = np.asarray(o["V_hist"]["need"], float); con = np.asarray(o["V_hist"]["content"], float)
    pz = np.asarray(o["V_hist"]["peace"], float); YH = need.shape[0]
    die_t = np.full(N, 10 ** 9)
    for d_ in (o.get("died") or []):
        die_t[int(d_[0])] = min(die_t[int(d_[0])], int(d_[1]))
    alive = (np.arange(YH)[:, None] * 52 < die_t[None, :])             # (age, life)
    cnt = alive.sum(1)
    def am(x):   # mean over the living at each age
        x = np.where(alive if x.ndim == 2 else alive[..., None], x, np.nan)
        with np.errstate(all="ignore"):
            return np.nanmean(x, 1)
    ages = dict(n=cnt.tolist(), need=np.round(am(need), 4).tolist(), content=np.round(am(con), 4).tolist(),
                peace=np.round(am(pz), 4).tolist())
    lo, hi = WELL[0], min(WELL[1], YH - 1)
    lm = {}
    for nm, x in (("content", con), ("peace", pz)):
        if hi >= lo:
            xs = np.where(alive[lo:hi + 1], x[lo:hi + 1], np.nan)
            with np.errstate(all="ignore"):
                v = np.nanmean(xs, 0)
            lm[nm] = [None if not np.isfinite(q) else round(float(q), 4) for q in v]
        else:
            lm[nm] = []
    # what the Game's panel reads from the engine's pause state
    pk = set()
    for fn in ("game_because.py", "game_life.py"):
        fp = os.path.join(tree, "chroma-game", "prototype", fn)
        if os.path.exists(fp):
            pk |= set(re.findall(r'loc\[\s*["\'](\w+)["\']\s*\]', open(fp, encoding="utf-8").read()))
    sw = {k: P.get(k) for k in sorted(P) if k.startswith(("need_", "imp_", "shared_hist"))}
    res = dict(tag=TAG, tree=tree, seed=a.seed, N=N, years=Y, px=px, secs=secs, switches=sw,
               switches_default={k: E.DEFAULT.get(k) for k in NEEDS_ON},
               needs=list(E.NEEDS), kinds=kinds, imp_age_engine=list(getattr(E, "IMP_AGE", ())), impose_p=P["impose_p"],
               imp_full=[round(0.5 * float(np.abs(r).sum()), 4) for r in np.asarray(L["IMP"], float)],
               first_end_age=None if first_end is None else round(first_end / 52, 2),
               cause_key=cause_key, causes=causes, panel_keys=sorted(pk), deaths=int((die_t < 10 ** 9).sum()),
               setbacks_unread_weeks=unread,
               ages=ages, well_ages=[lo, hi], life_means=lm, events=ev, wk=wk,
               expo_age=expo_age.tolist(), expo={f: v.tolist() for f, v in expo.items()})
    with open(a.out, "w") as f:
        json.dump(res, f, separators=(",", ":"))
    print(f"seed {a.seed}: {N} lives x {Y} years in {secs} s (wall); {len(ev['t'])} setbacks; px {json.dumps(px)}; "
          f"needs switches {json.dumps({k: sw.get(k) for k in NEEDS_ON})}; cause key {cause_key}; -> {a.out}")


# -------------------------------------------------------------------------------------------------------------- judge
def load(d):
    rs = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            r = json.load(open(f))
        except (ValueError, OSError):
            continue
        if isinstance(r, dict) and r.get("tag") == TAG:
            r["_file"] = f; rs.append(r)
    if not rs:
        sys.exit(f"no needs_check run JSON in {d}")
    return rs


def pool_ages(rs):
    """Per age: living count, and life-year-weighted means of each need, satisfaction and peace, pooled over seeds."""
    YH = max(len(r["ages"]["n"]) for r in rs); J = len(rs[0]["needs"])
    n = [0] * YH; s = {k: [0.0] * YH for k in ("content", "peace")}; sn = [[0.0] * J for _ in range(YH)]
    for r in rs:
        A = r["ages"]
        for a_, c in enumerate(A["n"]):
            if not c or A["content"][a_] is None:
                continue
            n[a_] += c
            for k in s:
                s[k][a_] += c * A[k][a_]
            for j in range(J):
                sn[a_][j] += c * A["need"][a_][j]
    out = dict(n=n, content=[s["content"][a] / n[a] if n[a] else None for a in range(YH)],
               peace=[s["peace"][a] / n[a] if n[a] else None for a in range(YH)],
               need=[[sn[a][j] / n[a] for j in range(J)] if n[a] else None for a in range(YH)])
    return out


def bands(A, J):
    rows = []
    for lo in range(0, len(A["n"]), 10):
        hi = min(lo + 9, len(A["n"]) - 1); idx = [a for a in range(lo, hi + 1) if A["n"][a]]
        if not idx:
            continue
        w = sum(A["n"][a] for a in idx)
        m = [sum(A["n"][a] * A["need"][a][j] for a in idx) / w for j in range(J)]
        m += [sum(A["n"][a] * A[k][a] for a in idx) / w for k in ("content", "peace")]
        rows.append((lo, lo + 9, hi, m))
    return rows


def ushape(A):
    v = {a: (A["content"][a] if a < len(A["content"]) else None) for a in UAGES}
    if any(x is None for x in v.values()):
        return None, v
    low = min(v, key=v.get)
    return (low in (40, 50, 60) and v[20] > v[low] and v[70] > v[low]), v


def well(rs):
    """Per-seed and pooled mean satisfaction and peace over ages WELL, by living life-years; and per-life means."""
    per = {"content": [], "peace": []}; tot = {"content": [0.0, 0], "peace": [0.0, 0]}; lives = {"content": [], "peace": []}
    for r in rs:
        A = r["ages"]; lo, hi = WELL[0], min(WELL[1], len(A["n"]) - 1)
        for k in per:
            w = sum(A["n"][a] for a in range(lo, hi + 1)); s = sum(A["n"][a] * A[k][a] for a in range(lo, hi + 1) if A["n"][a])
            if w:
                per[k].append(s / w); tot[k][0] += s; tot[k][1] += w
            lives[k] += [x for x in r["life_means"].get(k, []) if x is not None]
    pooled = {k: (tot[k][0] / tot[k][1] if tot[k][1] else None) for k in per}
    return pooled, per, lives


def sd(xs):
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def se_side(per, lives):
    """One side's standard error of its pooled mean: from the per-seed means when there are two or more seeds,
    else from the per-life means (flagged)."""
    if len(per) >= 2:
        return sd(per) / math.sqrt(len(per)), "seeds"
    s = sd(lives)
    return (s / math.sqrt(len(lives)) if s is not None else 0.0), "lives"


def gate_of(name):
    for nm, g, h, src in GATES:
        if nm == name.lower():
            return g, h, src
    return None, None, None


def note_check(tree_hint):
    """Re-read the note's section 5 gates, when the note is at hand, and say whether they are the tool's."""
    cands = [os.path.join("/mnt/project-files", NOTE)] + ([os.path.join(tree_hint, NOTE)] if tree_hint else [])
    fp = next((c for c in cands if os.path.exists(c)), None)
    if fp is None:
        return "the note is not at hand; GATES as held"
    lines = open(fp, encoding="utf-8").read().split("\n")
    seen = {}
    for ln in lines:
        c = [x.strip() for x in ln.split("|")]
        if len(c) > 4 and c[1].lower() in {g[0] for g in GATES}:
            m = re.match(r"(none|\d+)(?:,\s*half to\s*(\d+))?", c[3])
            if m:
                seen[c[1].lower()] = (0 if m.group(1) == "none" else int(m.group(1)), int(m.group(2)) if m.group(2) else None)
    diff = [g[0] for g in GATES if seen.get(g[0]) != (g[1], g[2])]
    return f"{fp}: " + ("the same gates as the tool's" if not diff else "DIFFERS on " + "; ".join(diff))


def setbacks(rs):
    """Pool the setbacks: per event (age, kind name, size, facts, cause), and the life-weeks by age and by fact."""
    E_ = []; YH = max(r["years"] for r in rs)
    expo_age = [0] * YH; expo = {f: [[0] * NB for _ in range(YH)] for f in FACTS}
    for r in rs:
        ev = r["events"]; kinds = r["kinds"]; wk = r.get("wk") or {}
        for i in range(len(ev["t"])):
            t = ev["t"][i]; wi = (t - wk["t0"]) if wk.get("t0") is not None else None
            fx = dict(crime=ev["crime"][i] / 100 if ev["crime"][i] >= 0 else None,
                      harm=float(ev["harm"][i]) if ev["harm"][i] >= 0 else None,
                      frail=ev["frail"][i] / 100 if ev["frail"][i] >= 0 else None,
                      weak=wk["weak"][wi] if wi is not None and 0 <= wi < len(wk["weak"]) else None,
                      repress=wk["repress"][wi] if wi is not None and 0 <= wi < len(wk["repress"]) else None)
            E_.append(dict(age=t / 52, kind=kinds[ev["k"][i]], size=ev["size"][i] / 1000, fx=fx,
                           cause=ev["cause"][i] >= 0, seed=r["seed"]))
        for a_, c in enumerate(r["expo_age"]):
            expo_age[a_] += c
        for f in FACTS:
            for a_, row in enumerate(r["expo"].get(f, [])):
                for j, c in enumerate(row):
                    expo[f][a_][j] += c
    return E_, expo_age, expo


def n3_read(E_, kinds):
    """The N3 counts: below gate, half window (and at full size), no cause; and the half sizes' reference."""
    below = {}; half = {}; full = {}; nocause = 0; ref = {}
    for k in kinds:
        g, h, _ = gate_of(k)
        if h is not None:
            xs = sorted(e["size"] for e in E_ if e["kind"] == k and e["age"] >= h)
            ref[k] = xs[len(xs) // 2] if xs else None
    for e in E_:
        g, h, _ = gate_of(e["kind"])
        if g is not None and e["age"] < g:
            below[e["kind"]] = below.get(e["kind"], 0) + 1
        elif h is not None and e["age"] < h:
            half[e["kind"]] = half.get(e["kind"], 0) + 1
            if ref.get(e["kind"]) and e["size"] > HALF_K * ref[e["kind"]]:
                full[e["kind"]] = full.get(e["kind"], 0) + 1
        nocause += not e["cause"]
    return below, half, full, nocause, ref


def world_read(E_, expo, k, f):
    """Rate of kind k where fact f is in the upper half of the life-weeks seen (at ages WORLD_FROM and over) against
    the lower half: (ratio, high events, low events, split value) or None when the fact does not vary."""
    g = WORLD_FROM
    ex = [sum(expo[f][a][j] for a in range(int(math.ceil(g)), len(expo[f]))) for j in range(NB)]
    tot = sum(ex)
    if tot == 0:
        return None
    best = None; cum = 0
    for s in range(1, NB):
        cum += ex[s - 1]
        if 0 < cum < tot and (best is None or abs(cum - tot / 2) < abs(best[1] - tot / 2)):
            best = (s, cum)
    if best is None:
        return None
    s = best[0]; exl = sum(ex[:s]); exh = tot - exl
    evh = evl = 0
    for e in E_:
        if e["kind"] != k or e["age"] < g or e["fx"].get(f) is None:
            continue
        j = min(max(int(e["fx"][f] * NB), 0), NB - 1)
        if j >= s:
            evh += 1
        else:
            evl += 1
    rl, rh = evl / exl, evh / exh
    return (rh / rl if rl > 0 else float("inf") if rh > 0 else None), evh, evl, s / NB


def f3(x, sign=False):
    if x is None:
        return "n/a"
    s = f"{x:+.3f}" if sign else f"{x:.3f}"
    return re.sub(r"^([+-]?)0\.", r"\1.", s)


def cmd_judge(a):
    rs = load(a.dir); bs = load(a.base) if a.base else None
    needs = rs[0]["needs"]; J = len(needs); kinds = rs[0]["kinds"]
    lives = sum(r["N"] for r in rs); seeds = sorted({r["seed"] for r in rs})
    bl = sum(r["N"] for r in bs) if bs else 0; bseeds = sorted({r["seed"] for r in bs}) if bs else []
    rep = []
    hdr = (f"needs_check judge, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC. Run: {a.dir}, {lives} lives over seeds "
           f"{seeds}, {sorted({r['years'] for r in rs})} years, tree {sorted({r['tree'] for r in rs})}, px "
           f"{sorted({json.dumps(r['px'], sort_keys=True) for r in rs})}.")
    if bs:
        hdr += (f" Base: {a.base}, {bl} lives over seeds {bseeds}, {sorted({r['years'] for r in bs})} years, tree "
                f"{sorted({r['tree'] for r in bs})}, px {sorted({json.dumps(r['px'], sort_keys=True) for r in bs})}.")
    # ---- N1
    A = pool_ages(rs); B = pool_ages(bs) if bs else None
    sw = rs[0]["switches"]
    sw_ok = all(r["switches"].get("need_tab") == "v7" and (r["switches"].get("shared_hist") or 0) > 0
                and bool(r["switches"].get("imp_age")) for r in rs)
    rows = bands(A, J); brows = {r[0]: r for r in bands(B, J)} if B else {}
    bad = []
    for lo, _, hi, m in rows:
        if lo >= N1_BANDS[0] and lo + 9 <= N1_BANDS[1]:
            for j in range(J):
                if m[j] < LO or m[j] > HI:
                    bad.append(f"{needs[j]} {m[j]:.3f} at {lo}-{lo + 9}")
    n1_read = [f"{lo}-{lo + 9}" for lo, _, _, _ in rows if lo >= N1_BANDS[0] and lo + 9 <= N1_BANDS[1]]
    u, uv = ushape(A); bu, buv = ushape(B) if B else (None, None)
    us = ("U-shape " + ("holds" if u else "does not hold" if u is not None else "not readable (the run stops before 70)")
          + " (" + ", ".join(f"{k} {f3(v)}" for k, v in uv.items()) + ")")
    n1_pass = sw_ok and u is True and not bad and len(n1_read) == 7
    n1 = (f"N1 needs_age     {'PASS' if n1_pass else 'MISS'}  every needs switch on: {'yes' if sw_ok else 'NO'} "
          f"({', '.join(f'{k} {sw.get(k)!r}' for k in NEEDS_ON)}); {us}; needs in bands 10-19 to 70-79 inside "
          f"[{LO:.2f}, {HI:.2f}]: {'yes' if not bad else 'NO, ' + '; '.join(bad[:6])} (bands read: "
          f"{', '.join(n1_read) or 'none'}{'' if len(n1_read) == 7 else '; all seven needed'}); {lives} lives")
    # ---- N2
    pw, pper, plv = well(rs)
    hi_ = min(WELL[1], len(A["n"]) - 1); wl = f"{WELL[0]} to {hi_}" if hi_ >= WELL[0] else f"{WELL[0]} to {WELL[1]}: none in the run"
    if bs:
        bw, bper, blv = well(bs)
        parts = []; ok = True; how = set()
        for k in ("content", "peace"):
            if pw[k] is None or bw[k] is None:
                ok = False; parts.append(f"{'satisfaction' if k == 'content' else 'peace'} not readable (no ages "
                                         f"{WELL[0]} to {WELL[1]} in the run or the base)")
                continue
            s1, h1 = se_side(pper[k], plv[k]); s2, h2 = se_side(bper[k], blv[k]); how |= {h1, h2}
            nz = 2 * math.sqrt(s1 ** 2 + s2 ** 2); mv = pw[k] - bw[k]; okk = mv >= -nz; ok &= okk
            parts.append(f"{'satisfaction' if k == 'content' else 'peace'} {f3(pw[k])} against {f3(bw[k])} "
                         f"(move {f3(mv, True)}, noise {f3(nz)}: {'not below' if okk else 'BELOW'})")
        how_s = ("noise from the per-seed means" if how == {"seeds"} else
                 "noise from the per-life means on a side with one seed (understates it: one world a run)")
        n2_pass = ok and u is True
        n2 = (f"N2 needs_alone   {'PASS' if n2_pass else 'MISS'}  ages {wl}: {'; '.join(parts)}; {how_s}; {us.split(' (')[0]}; {lives} lives, base {bl}")
    else:
        n2 = (f"N2 needs_alone   MISS  no --base (the floor is v23.2's); satisfaction {f3(pw['content'])}, peace "
              f"{f3(pw['peace'])} at ages {wl}; {us.split(' (')[0]}; {lives} lives")
    # ---- N3
    E_, ea, ex = setbacks(rs)
    below, half, full, nocause, ref = n3_read(E_, kinds)
    ck = sorted({r["cause_key"] for r in rs}, key=str); pk = set().union(*[set(r.get("panel_keys", [])) for r in rs])
    panel = [c for c in ck if c and c in pk]
    sized = all(ref.get(k) for k in half) if half else True
    unread = sum(r.get("setbacks_unread_weeks", 0) for r in rs)
    wv = {}                                                   # world-tied kinds: does each follow its world?
    for k_, fs_ in KIND_FACTS.items():
        if k_ not in kinds:
            continue
        rd_ = [w_ for w_ in (world_read(E_, ex, k_, f_) for f_ in fs_) if w_ is not None and w_[0] is not None]
        if rd_:
            wv[k_] = any((w_[1] - w_[2]) / max(1, w_[1] + w_[2]) ** 0.5 >= 2 for w_ in rd_)
    world_bad = [k_ for k_, v_ in wv.items() if not v_]
    n3_pass = bool(E_) and not unread and not below and not nocause and bool(panel)   # world fit: v25 (Emren's card)
    hw = ", ".join(f"{SHORT.get(k, k)} {half[k]}" for k in half) or "none"
    n3 = (f"N3 needs_setbacks {'PASS' if n3_pass else 'MISS'}  {len(E_)} setbacks"
          f"{f' (NOT READ in {unread} weeks: the engine has no need_why)' if unread else ''}; below gate "
          f"{sum(below.values())}{' (' + ', '.join(f'{SHORT.get(k, k)} {v}' for k, v in below.items()) + ')' if below else ''}; "
          f"half window {sum(half.values())} ({hw}), at full size {sum(full.values())}"
          f"{'' if sized else ' (some kinds have no full-size reference: run longer)'}; without a cause {nocause} "
          f"(cause key handed over: {', '.join(str(c) if c else 'none' for c in ck)}; the panel reads it: {'yes' if panel else 'no'}; "
          f"the panel reads {', '.join(sorted(k for k in pk if 'imp' in k or 'cause' in k)) or 'no setback key'}); "
          f"world (read only until v25): {len(wv) - len(world_bad)} of {len(wv)} world-tied kinds whose facts vary follow them"
          f"{' (not: ' + ', '.join(SHORT.get(k, k) for k in world_bad) + ')' if world_bad else ''}; half window read only")
    if bs:
        Eb, _, _ = setbacks(bs); bb, bh, bf, bnc, _ = n3_read(Eb, bs[0]["kinds"])
        n3 += (f"; base: {len(Eb)} setbacks, below gate {sum(bb.values())}, half window at full size {sum(bf.values())}, "
               f"without a cause {bnc}")
    n3 += f"; {lives} lives"
    rep += [hdr, "", n1, n2, n3, ""]
    # ---- tables
    rep.append("N1: needs, satisfaction and peace by age band (mean over living life-years)"
               + ("; each cell: run, base, move" if B else ""))
    cols = needs + ["satisfaction", "peace"]
    if B:
        rep.append(f"{'band':<7}" + "".join(f"{c[:15]:>20}" for c in cols))
        for lo, _, hi, m in rows:
            br = brows.get(lo)
            cells = []
            for j in range(len(cols)):
                if br:
                    cells.append(f"{f3(m[j])} {f3(br[3][j])} {f3(m[j] - br[3][j], True)}")
                else:
                    cells.append(f"{f3(m[j])}   n/a    n/a")
            rep.append(f"{lo:>2}-{hi:<4}" + "".join(f"{c:>20}" for c in cells))
    else:
        rep.append(f"{'band':<7}" + "".join(f"{c[:12]:>13}" for c in cols))
        for lo, _, hi, m in rows:
            rep.append(f"{lo:>2}-{hi:<4}" + "".join(f"{f3(x):>13}" for x in m))
    rep.append("")
    rep.append("U-shape (satisfaction at t_satisf's ages): run " + ", ".join(f"{k} {f3(v)}" for k, v in uv.items())
               + (("; base " + ", ".join(f"{k} {f3(v)}" for k, v in buv.items())) if B else ""))
    rep.append("N2 per-seed means, ages %s: run satisfaction %s, peace %s" % (
        wl, [round(x, 4) for x in pper["content"]], [round(x, 4) for x in pper["peace"]])
        + ("; base satisfaction %s, peace %s" % ([round(x, 4) for x in bper["content"]], [round(x, 4) for x in bper["peace"]])
           if bs else ""))
    rep.append("")
    # setbacks by kind
    rep.append(f"N3: setbacks by kind (gate and half-to ages from {NOTE} section 5; the engine's own ages "
               f"{rs[0].get('imp_age_engine')}; the first end pause at age {rs[0].get('first_end_age')}; "
               f"the gates: {note_check(rs[0]['tree'])})")
    rep.append(f"  {'kind':<11}{'gate':>5}{'half':>5}{'n':>7}{'below':>7}{'halfwin':>8}{'full':>6}{'size ref':>9}  rate per 100 life-years "
               f"by age band (3-9, 10-19, ...)")
    YH = len(ea)
    kb = {}
    for e in E_:
        kb[(e["kind"], int(e["age"] // 10))] = kb.get((e["kind"], int(e["age"] // 10)), 0) + 1
    for k in kinds:
        g, h, src = gate_of(k); n_ = sum(v for (k_, _), v in kb.items() if k_ == k)
        rts = []
        for lo in range(0, YH, 10):
            w = sum(ea[lo:lo + 10]) / 52
            c = kb.get((k, lo // 10), 0)
            rts.append(f"{100 * c / w:5.1f}" if w else "  n/a")
        rep.append(f"  {SHORT.get(k, k)[:10]:<11}{'?' if g is None else g:>5}{'-' if h is None else h:>5}{n_:>7}"
                   f"{below.get(k, 0):>7}{half.get(k, 0):>8}{full.get(k, 0):>6}"
                   f"{(f'{ref[k]:.3f}' if ref.get(k) else '-'):>9}  " + " ".join(rts))
    rep.append("")
    rep.append("N3 world reading (read only until v25, Emren's card; it passes on a two-sigma rise where the fact is high): the kind's rate "
               "where its fact is in the upper half of the life-weeks seen, over its rate in the lower half (above 1: "
               "it follows its world)")
    for k, fs in KIND_FACTS.items():
        if k not in kinds:
            continue
        for f in fs:
            w = world_read(E_, ex, k, f)
            rep.append(f"  {SHORT.get(k, k):<11}{f:<8} " + ("the fact does not vary in these lives (or no ages 18 and over)"
                       if w is None else
                       f"ratio {('inf' if w[0] == float('inf') else 'n/a' if w[0] is None else f'{w[0]:.2f}')} "
                       f"({w[1]} high, {w[2]} low; split at {w[3]:.2f})"))
    dep = "you are made dependent on others"
    if dep in kinds and YH > 70:
        w1 = sum(ea[16:70]) / 52; w2 = sum(ea[70:]) / 52
        c1 = sum(1 for e in E_ if e["kind"] == dep and 16 <= e["age"] < 70); c2 = sum(1 for e in E_ if e["kind"] == dep and e["age"] >= 70)
        rep.append(f"  made dependent, rate per 100 life-years: 16 to 69 {100 * c1 / w1:.1f}, 70 and over "
                   f"{(f'{100 * c2 / w2:.1f}' if w2 else 'n/a')} (the note: rising after 70)")
    else:
        rep.append("  made dependent after 70: not readable (the run stops before 70)")
    rep.append("")
    rep.append("Runs read: " + "; ".join(f"{os.path.basename(r['_file'])} seed {r['seed']} {r['N']}x{r['years']} {r['secs']} s"
                                       for r in rs + (bs or [])))
    txt = "\n".join(rep) + "\n"
    if a.out:
        with open(a.out, "w") as f:
            f.write(txt)
    print(txt)


def main():
    ap = argparse.ArgumentParser(description="Release's reader for v24 N1, N2, N3 (needs that fit life)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run"); r.add_argument("tree"); r.add_argument("seed", type=int); r.add_argument("N", type=int)
    r.add_argument("years", type=int); r.add_argument("out"); r.add_argument("--px", default="{}")
    j = sp.add_parser("judge"); j.add_argument("dir"); j.add_argument("--base"); j.add_argument("--out")
    a = ap.parse_args()
    cmd_run(a) if a.cmd == "run" else cmd_judge(a)


if __name__ == "__main__":
    main()
