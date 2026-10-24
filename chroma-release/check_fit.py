"""v22.5 row K17 (records/v22.5/scope.md): moments fit the age and the start. Three checks, one results line each, on
lives with their switch on and every other switch as DEFAULT (the refit's settings on the record's commit):

  f4_age     (F4, batch.AGE_FIT) Earth with the live packs, the outer world on as presets 1 to 4 play it, every moment
             of every week read through engine.run_steps():
               F4.1  no moment whose start the Library's age fit raised (chroma-library/earth_age_fit.py) comes before
                     its new start age                                                                    0 weeks
               F4.2  no child version shut at 11.99 comes at 12 or over                                   0 weeks
               F4.3  a child version and its teen or adult twin never both come at 12 in one life         0 lives
             Reported: every other moment that comes outside its age window (the engine's other paths).
  f6_dreams  (F6, dream_grow) Earth as above, and the clan's and the towers' seed library as the game plays them; the
             dreams that begin (engine goal log), named by the Library's dreams.py DREAM_KIND and KIND_FROM:
               F6.1  no dream begins before its kind opens (play from 4, status from 9, own from 14), so every dream
                     begun at 4 to 8 is a play dream                                                       0 dreams
               F6.2  status dreams at 9 to 13: their share of the dreams begun at 9 to 13                  .20 or more
               F6.3  their own from 14: own dreams' share of the dreams begun at 14 or over                .20 or more
               F6.4  play dreams are short-lived: of those begun at 4 to 8, the median years held          2.0 or less,
                     and below the median of the dreams begun at 14 or over
               F6.5  the spark keeps its subject: a dream a spark begins is one the spark shows (TRIGGER_DREAMS),
                     at the ages its telling fits (TRIGGER_AGES)                                           every one
  f12_start  (F12, the game's world_hold with the engine's own_open and start_hold) as the game plays it (the game
             folder and its engine_pin):
               F12.1 the clan's and the towers' own words, played lives of presets 5 and 6: no story line the
                     game marks as modern Earth's for that world (story.WORLD_LEAKS) is told; no Earth word for a means
                     or work ("lacks money", "money lost", "loses their job", "loses their work"); every option and
                     moment the Library's worlds.py renames shows its world's words                       0 each
               F12.2 a culture's own acts always on offer: no own act (worlds.py OWN) shown "not on offer around
                     them" in those lives; and in the engine (seed library, own_open), no own act closed while the
                     means allow it, every week of every life                                             0 each
               F12.3 each start keeps its promise, presets 1 to 4 to age 7: the birth fits the start (world_link
                     start_fits: the place's kind, the family's class, a family faith or none, hard streets); a child
                     raised in a faith is raised in the family's own (its profile), and none where the family holds
                     none or the start promises none; the story's place is the world's; the four starts of one seed
                     are four worlds                                                                      every life
Each judged row passes or not; a check is PASS when all its rows pass, else FAIL. F6.2 to F6.4 read "status at 9 to
13, their own from 14" and "short-lived" (Emren's v22.5 realism list, F6) as tendencies, not walls (Emren 10-11 17:35
UTC): each kind opens at its age (a wall only below it, F6.1) and takes at least a fifth of the dreams begun in its
band; play dreams stay possible later, and the leading kind of each band is reported, not judged.

    python3 -B chroma-release/check_fit.py <f4_age|f6_dreams|f12_start|all> [--repo DIR] [--commit SHA]
                                           [--seeds 41-44] [--lives 300] [--jobs 4] [--out DIR] [--no-record]

--repo: the checkout to check (default the tree this script sits in): its chroma-engine/v22-speedpass with its
chroma-library and chroma-packs (f4_age, f6_dreams, F12.2's engine part) and its chroma-game/prototype (f12_start), its
engine_pin filled from those same folders first (gamepin.py; a committed pin is played as it is). Each unit of work
runs in its own process (--jobs at a time). Report: <out>/fit_<check>.txt (default out/fit_<UTC time>/); one results
line per check (results.py) unless --no-record. Exit code 0 when every check run
passes. About 15 minutes on 4 cores for all three at the defaults.
"""
import argparse, json, os, re, subprocess, sys, time
import gamepin
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = ("f4_age", "f6_dreams", "f12_start")
EARTH_WORLD = dict(setting="earth", pace=1.0, tech_level="modern", climate="middle")   # the game's Earth world (presets 1 to 4)
F4_YEARS = 50            # the latest start the age fit sets is 45
F6_YEARS = 40
F12_OWN_YEARS = 60
F12_WORD_SEEDS = range(1, 9)      # played lives a world (presets 5 and 6)
F12_START_SEEDS = range(1, 26)    # starts a preset (1 to 4), to age 7
EARTH_WORDS = ("lacks money", "money lost", "loses their job", "loses their work")   # the Earth words F12.1 rules out


# ---------------------------------------------------------------------------------------------------- the units
def engine(repo):
    """The checkout's engine and batch, reading its Library and packs."""
    sys.path.insert(0, os.path.join(repo, "chroma-engine", "v22-speedpass"))
    sys.dont_write_bytecode = True
    import engine as E, batch
    batch.LIB_DIR = os.path.join(repo, "chroma-library"); batch.PACK_DIR = os.path.join(repo, "chroma-packs")
    return E, batch


def library_module(repo, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"chroma_{name}", os.path.join(repo, "chroma-library", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def seed_library(E, batch, repo, world):
    """The seed library as the game plays the clan or the towers (game.with_dreams): its dreams, and its own acts."""
    L = E.compile_library()
    D = library_module(repo, "dreams")
    if world in D.DREAM_TRIGGERS:
        L["DREAM_TRIGGERS"] = list(D.DREAM_TRIGGERS[world])
        L["DREAMS"] = [d for d in D.DREAMS if world in d["worlds"].split()]
        batch.dream_grow_data(L, D, world)
    WD = library_module(repo, "worlds")
    if world in WD.OWN:
        batch.own_ways(L, WD.OWN[world])
    return L, D


def switched(E, on, world=False):
    """DEFAULT with these switches on (and the outer world as the game plays Earth); also which switches DEFAULT has
    off (switched on here)."""
    P = dict(E.DEFAULT)
    forced = [k for k, v in on.items() if P.get(k) != v]
    P.update(on)
    if world:
        P.update(world=True, world_cfg=dict(EARTH_WORLD))
    return P, forced


def steps(E, N, Y, seed, P, L, at, look):
    """Lives N lives through run_steps(), calling look(state) at every pause of kind `at`; returns run()'s result."""
    g = E.run_steps(N, Y, seed, P, lib=L)
    pz = next(g)
    try:
        while True:
            if pz.kind == at:
                look(pz.state)
            pz = g.send(pz.value)
    except StopIteration as e_:
        return e_.value


def unit_f4(repo, seed, lives):
    E, batch = engine(repo)
    forced = [] if batch.AGE_FIT else ["batch.AGE_FIT"]
    batch.AGE_FIT = True
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    AF = library_module(repo, "earth_age_fit").AGE_FIT
    names = list(L["names"]); ix = {n: i for i, n in enumerate(names)}
    AGE = np.asarray(L["AGE"], float)                  # the windows the engine gates with
    FIT = np.tile([-np.inf, np.inf], (len(names), 1))  # the Library's fitted windows, judged against (not the batch's)
    for nm, f in AF.items():
        if "age" in f and nm in ix:
            FIT[ix[nm]] = f["age"]
    fit = np.isfinite(FIT[:, 0])
    child = fit & (np.abs(FIT[:, 1] - 11.99) < 1e-6)
    twin = {i: ix.get(L["src"][i].get("variant_of")) for i in np.nonzero(child)[0]}
    P, f2 = switched(E, {}, world=True)
    early = {}; late12 = {}; outside = {}; at12 = {}            # moment -> weeks; (life, pair) -> what came at 12
    def look(st):
        s = np.asarray(st["s"]); age = float(st["age"]); live = ~np.asarray(st["dead"])
        for n in np.nonzero(live & (age < FIT[s, 0] - 1e-9))[0]:
            early[names[s[n]]] = early.get(names[s[n]], 0) + 1
        if age >= 12:
            for n in np.nonzero(live & child[s])[0]:
                late12[names[s[n]]] = late12.get(names[s[n]], 0) + 1
        for n in np.nonzero(live & ~fit[s] & ((age < AGE[s, 0] - 1e-9) | (age > AGE[s, 1] + 1e-9)))[0]:
            outside[names[s[n]]] = outside.get(names[s[n]], 0) + 1
        if 12 <= age < 13:
            for n in np.nonzero(live)[0]:
                si = int(s[n])
                if child[si]:
                    at12.setdefault((int(n), si), set()).add("child")
                for c_, t_ in twin.items():
                    if si == t_:
                        at12.setdefault((int(n), c_), set()).add("twin")
    steps(E, lives, F4_YEARS, seed, P, L, "choose", look)
    both = sorted({names[c_] for (n, c_), v in at12.items() if v == {"child", "twin"}})
    return dict(seed=seed, lives=lives, years=F4_YEARS, forced=forced + f2, fitted=int(fit.sum()), child=int(child.sum()),
                early=early, late12=late12, both12=[[names[c_], n] for (n, c_), v in at12.items() if v == {"child", "twin"}],
                both_names=both, outside=outside)


def unit_f6(repo, world, seed, lives):
    E, batch = engine(repo)
    if world == "earth":
        L = batch.load_batch("earth", packs=list(batch.PACKS))
        D = library_module(repo, "dreams")
        P, forced = switched(E, dict(dream_grow=True), world=True)
    else:
        L, D = seed_library(E, batch, repo, world)
        P, forced = switched(E, dict(dream_grow=True))
    o = E.run(N=lives, years=F6_YEARS, seed=seed, P=P, lib=L)
    KIND, FROM = D.DREAM_KIND, D.KIND_FROM
    TD = D.TRIGGER_DREAMS.get(world, {}); TA = D.TRIGGER_AGES.get(world, {})
    gl = [g for g in o["goals"] if g["kind"] == "dream"]
    ends = {}
    for g in gl:
        if g["what"] != "begins":
            ends.setdefault((g["life"], g["id"]), g["age"])
    bands = {"under 4": {}, "4-8": {}, "9-13": {}, "14+": {}}; held = {"play 4-8": [], "14+": []}
    early = []; spark_n = spark_off = spark_age = 0
    for g in gl:
        if g["what"] != "begins":
            continue
        a = g["age"]; nm = g.get("dream"); k = KIND.get(nm, "unnamed") if nm else "unnamed"
        b = "under 4" if a < 4 else "4-8" if a < 9 else "9-13" if a < 14 else "14+"
        bands[b][k] = bands[b].get(k, 0) + 1
        if nm and k in FROM and a < FROM[k] - 1e-9:
            early.append([nm, k, a])
        e_ = ends.get((g["life"], g["id"]))
        if e_ is not None:
            if b == "4-8" and k == "play":
                held["play 4-8"].append(e_ - a)
            elif b == "14+":
                held["14+"].append(e_ - a)
        tr = g.get("trigger")
        if tr in TD:
            spark_n += 1
            spark_off += nm not in TD[tr]
            lo, hi = TA.get(tr, (0.0, 1e9))
            spark_age += not (lo - 1e-9 <= a <= hi + 1e-9)
    return dict(world=world, seed=seed, lives=lives, years=F6_YEARS, forced=forced, bands=bands, early=early[:20],
                n_early=len(early), held=held, spark=[spark_n, spark_off, spark_age],
                per_life=sum(sum(v.values()) for v in bands.values()) / lives)


def unit_f12_own(repo, world, seed, lives):
    E, batch = engine(repo)
    L, _ = seed_library(E, batch, repo, world)
    P, forced = switched(E, dict(own_open=True))
    OWN = np.asarray(L["OWN"], bool)
    c = dict(own_offered=0, own_open=0, own_means=0, closed=0, other_offered=0, other_open=0)
    def look(st):
        s = np.asarray(st["s"]); live = ~np.asarray(st["dead"])[:, None]
        mask = np.asarray(st["mask"], bool) & live & ~np.asarray(st["do_nothing"], bool)
        own = OWN[s] & mask; oth = mask & ~OWN[s]
        op = np.asarray(st["open_"], bool); opr = np.asarray(st["open_r"], bool)
        c["own_offered"] += int(own.sum()); c["own_open"] += int((own & op).sum())
        c["own_means"] += int((own & ~opr).sum()); c["closed"] += int((own & opr & ~op).sum())
        c["other_offered"] += int(oth.sum()); c["other_open"] += int((oth & op).sum())
    steps(E, lives, F12_OWN_YEARS, seed, P, L, "choose", look)
    return dict(world=world, seed=seed, lives=lives, years=F12_OWN_YEARS, forced=forced, own_acts=int(OWN.sum()), **c)


def game_env(repo):
    """The game of the checkout, with the settings the unit's CHROMA_GAME and CHROMA_ENGINE give it (checks only, as
    the game reads them: world_hold on, and the engine's own_open and start_hold; none for f12defaults)."""
    G = os.path.join(repo, "chroma-game", "prototype")
    sys.path.insert(0, G)
    sys.dont_write_bytecode = True
    import game as GM
    return GM


def unit_f12_defaults(repo):
    """Which of F12's switches the checkout's game plays with off (so the other units switch them on): the game as
    loaded with neither CHROMA_GAME nor CHROMA_ENGINE set (run_units leaves both out here), its GAME["world_hold"]
    after everything game.py does at import (a GAME.update at a re-pin too), and its pinned engine's DEFAULT."""
    GM = game_env(repo)
    out = [] if GM.GAME.get("world_hold") else ["GAME world_hold"]
    return dict(forced=out + [k for k in ("own_open", "start_hold") if not GM.E.DEFAULT.get(k)])


def unit_f12_words(repo, preset, seed):
    GM = game_env(repo)
    import story as ST
    picked = []
    pick0 = ST.Story.pick
    def pick(self, pool, stage=None, v=None):
        t_ = pick0(self, pool, stage, v); picked.append(t_); return t_
    ST.Story.pick = pick
    said = []
    say0 = GM.Game._say
    def say(self, line, level=0, tag="note", **meta):
        said.append(str(line)); return say0(self, line, level, tag, **meta)
    GM.Game._say = say
    p = GM.PRESETS[preset]; world = p["setting"]; code = ST.SETTINGS[world]["code"] if hasattr(ST, "SETTINGS") else world[0].upper()
    g = GM.Game(name="Ari", seed=seed, **p)
    WD = GM.WDS
    LAB = {k: v for k, v in WD.LABELS.get(world, {}).items() if k != v}; TIT = {k: v for k, v in WD.TITLES.get(world, {}).items() if k != v}
    OWNL = set(WD.OWN.get(world, ()))
    r = dict(preset=preset, seed=seed, world=world, cps=0, label_seed=[], title_seed=[], own_shown=0, own_not_on_offer=[],
             own_means=0, why_earth=[])
    for _ in range(100000):
        st_ = g.advance()                               # "checkpoint", "resolved" (a moment that resolved itself), "over"
        if st_ == "over" or g.over:
            break
        if st_ != "checkpoint":
            continue
        cp = g.pending; r["cps"] += 1
        Lg = g.loc["L"]; s = cp["s"]
        if cp["sit"] in TIT and cp["title"] != TIT[cp["sit"]]:
            r["title_seed"].append(cp["title"])
        for op in cp["options"]:
            seed_lab = Lg["labels"][s][op["idx"]]
            if seed_lab in LAB and op["label"] == seed_lab:
                r["label_seed"].append(seed_lab)
            if seed_lab in OWNL:
                r["own_shown"] += 1
                if op["status"] == "out of reach":
                    if op["why"].startswith("not on offer"):
                        r["own_not_on_offer"].append(seed_lab)
                    else:
                        r["own_means"] += 1
            if any(w in (op.get("why") or "") for w in EARTH_WORDS):
                r["why_earth"].append(op["why"])
        g.decide(None)
    leaks = ST.WORLD_LEAKS.get(code, set())
    r["age"] = round(g.age(), 1)
    r["leaks"] = sorted({t_ for t_ in picked if t_ in leaks})
    r["earth_words"] = sorted({w for w in EARTH_WORDS for l_ in said if w in l_})
    r["money_mentions"] = sum(len(re.findall(r"\bmoney\b", l_, re.I)) for l_ in said)
    return r


def unit_f12_start(repo, seed):
    GM = game_env(repo)
    import world_link as WLM
    E = GM.E
    FAI = [c[0] for c in E.COMMITMENTS].index("faith")
    out = dict(seed=seed, starts={})
    for preset in ("1", "2", "3", "4"):
        p = GM.PRESETS[preset]
        g = GM.Game(name="Ari", seed=seed, **p)
        g.advance(until_checkpoint=False, until_age=0.05)     # the birth, before any move
        WL = g.loc.get("WL")
        if WL is None or not getattr(WL, "start", None):
            out["starts"][preset] = dict(error="no world or no start in the world (start_hold needs the world on)")
            continue
        fits = bool(np.asarray(WLM.start_fits(WL.PP, WL.W, WL.start)).all())
        kind0 = WL.W.loc_kind_key[int(WL.PP.loc[0])]; cls0 = int(WL.PP.cls[0])
        g.advance(until_checkpoint=False, until_age=7)
        loc = g.loc; WL = loc.get("WL"); P = loc["P"]
        pf = int(WL.PP.pfaith[0])
        fp = np.asarray(WL.W.faith_profile, float); fp = fp / fp.sum(1, keepdims=True)
        inh = [c for c in loc["commit_log"] if c[0] == 0 and c[2] == FAI and c[3] == "inherited"]
        prof_ok = None
        if inh:
            prof_ok = pf >= 0 and bool(np.allclose(np.asarray(inh[0][4], float), fp[min(pf, len(fp) - 1)].round(2), atol=0.006))
        kind = WL.W.loc_kind_key[int(WL.PP.loc[0])]
        out["starts"][preset] = dict(fits=fits, pfaith=pf, faith=p.get("faith"), inherited=bool(inh), prof_ok=prof_ok,
                                     held7=bool(loc["held"][0, FAI]), place=g.story.place, world_place=GM.place_word(kind),
                                     kind=kind0, cls=cls0, kind7=kind, world_seed=P.get("world_seed"),
                                     start_hold=bool(P.get("start_hold")), world_hold=bool(GM.GAME["world_hold"]))
    return out


UNITS = dict(f4=unit_f4, f6=unit_f6, f12own=unit_f12_own, f12words=unit_f12_words, f12start=unit_f12_start,
             f12defaults=unit_f12_defaults)


# ---------------------------------------------------------------------------------------------------- running
def run_units(repo, jobs, todo, out, log):
    """Runs (name, args, env) units, `jobs` at a time, each in its own process; returns their JSON results."""
    res, running, todo = [], [], list(todo)
    while todo or running:
        while todo and len(running) < jobs:
            nm, args, env = todo.pop(0)
            e = {k: v for k, v in os.environ.items() if k not in ("CHROMA_GAME", "CHROMA_ENGINE")}   # the game reads both
            e.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", **env)                           # as JSON settings
            f = open(os.path.join(out, f"{nm}_{'_'.join(map(str, args))}.json"), "w")
            pr = subprocess.Popen([sys.executable, "-B", os.path.abspath(__file__), "unit", repo, nm] + [str(a) for a in args],
                                  stdout=f, stderr=subprocess.PIPE, env=e, text=True)
            running.append((pr, f, nm, args, time.time()))
        time.sleep(1)
        for it in list(running):
            pr, f, nm, args, t0 = it
            if pr.poll() is None:
                continue
            running.remove(it); f.close()
            err = pr.stderr.read()
            try:
                r = json.loads(open(f.name).read().strip().splitlines()[-1])
            except (ValueError, IndexError):
                r = dict(error=(err or "no output").strip().splitlines()[-1][:300])
                log(f"  unit {nm} {args} failed: {err.strip()[-2000:]}")
            r["_unit"] = [nm] + list(args); r["_secs"] = round(time.time() - t0)
            res.append(r)
    return res


class Rows:
    def __init__(self, rid):
        self.rid, self.lines, self.ok = rid, [], True

    def row(self, name, ok, what):
        self.ok &= bool(ok)
        self.lines.append(f"  {'ok  ' if ok else 'MISS'} {name}: {what}")

    def note(self, line):
        self.lines.append("       " + line)


def errors(rs, R):
    bad = [r for r in rs if "error" in r]
    for r in bad:
        R.row("ran", False, f"unit {r['_unit']}: {r['error']}")
    return [r for r in rs if "error" not in r]


def judge_f4(rs):
    R = Rows("f4_age"); rs = errors(rs, R)
    if not rs:
        return R
    early, late, outside = {}, {}, {}
    for r in rs:
        for d_, k in ((early, "early"), (late, "late12"), (outside, "outside")):
            for nm, v in r[k].items():
                d_[nm] = d_.get(nm, 0) + v
    both = [b for r in rs for b in r["both12"]]
    lives = sum(r["lives"] for r in rs)
    R.note(f"{lives} lives x {rs[0]['years']} years, seeds {', '.join(str(r['seed']) for r in rs)}; {rs[0]['fitted']} moments "
           f"with an age fit, {rs[0]['child']} child versions shut at 11.99; switched on here: {', '.join(rs[0]['forced']) or 'none'}")
    R.row("F4.1 no fitted moment before its new start", not early,
          f"{sum(early.values())} weeks" + (": " + "; ".join(f"{k} {v}" for k, v in sorted(early.items())) if early else ""))
    R.row("F4.2 no child version at 12 or over", not late,
          f"{sum(late.values())} weeks" + (": " + "; ".join(f"{k} {v}" for k, v in sorted(late.items())) if late else ""))
    R.row("F4.3 a child version and its twin never both at 12", not both, f"{len(both)} lives")
    if outside:
        R.note("reported, not judged: other moments outside their age window (weeks): "
               + "; ".join(f"{k} {v}" for k, v in sorted(outside.items(), key=lambda x: -x[1])[:15]))
    else:
        R.note("reported: no other moment came outside its age window")
    return R


def judge_f6(rs):
    R = Rows("f6_dreams"); rs = errors(rs, R)
    for world in ("earth", "tribal", "magic"):
        w = [r for r in rs if r["world"] == world]
        if not w:
            continue
        bands = {}
        for r in w:
            for b, ks in r["bands"].items():
                for k, v in ks.items():
                    bands.setdefault(b, {}); bands[b][k] = bands[b].get(k, 0) + v
        share = lambda b, k: bands.get(b, {}).get(k, 0) / max(sum(bands.get(b, {}).values()), 1)
        early = sum(r["n_early"] for r in w)
        hp = [x for r in w for x in r["held"]["play 4-8"]]; h14 = [x for r in w for x in r["held"]["14+"]]
        mp = float(np.median(hp)) if hp else None; m14 = float(np.median(h14)) if h14 else None
        sp = [sum(r["spark"][i] for r in w) for i in range(3)]
        R.note(f"{world}: {sum(r['lives'] for r in w)} lives x {w[0]['years']} years, seeds "
               f"{', '.join(str(r['seed']) for r in w)}, {np.mean([r['per_life'] for r in w]):.1f} dreams a life; "
               f"switched on here: {', '.join(w[0]['forced']) or 'none'}")
        for b in ("under 4", "4-8", "9-13", "14+"):
            tot = sum(bands.get(b, {}).values())
            R.note(f"  begun {b:7s} {tot:5d}: " + ", ".join(f"{k} {share(b, k):.2f}" for k in ("play", "status", "own", "unnamed")))
        ex = [e_ for r in w for e_ in r["early"]][:5]
        R.row(f"F6.1 {world}: no dream before its kind opens", early == 0,
              f"{early} dreams" + (": " + "; ".join(f"{n} ({k}) at {a}" for n, k, a in ex) if ex else ""))
        R.row(f"F6.2 {world}: status dreams' share at 9 to 13", share("9-13", "status") >= .20, f"{share('9-13', 'status'):.2f} (.20 or more)")
        R.row(f"F6.3 {world}: own dreams' share from 14", share("14+", "own") >= .20, f"{share('14+', 'own'):.2f} (.20 or more)")
        ok4 = mp is not None and mp <= 2.0 and (m14 is None or mp < m14)
        R.row(f"F6.4 {world}: play dreams of 4 to 8 short-lived", ok4,
              f"median held {mp if mp is None else round(mp, 2)} years (2.0 or less; dreams begun from 14: "
              f"{m14 if m14 is None else round(m14, 2)}), {len(hp)} ended")
        R.row(f"F6.5 {world}: the spark keeps its subject and its ages", sp[1] == 0 and sp[2] == 0,
              f"{sp[0]} dreams a spark began; {sp[1]} name a dream it does not show, {sp[2]} outside its ages")
    return R


def judge_f12(rs):
    R = Rows("f12_start"); rs = errors(rs, R)
    fo = [x for r in rs if r["_unit"][0] == "f12defaults" for x in r["forced"]]
    R.note(f"played lives switched on here: {', '.join(fo) or 'none'} (the game as it loads)")
    words = [r for r in rs if r["_unit"][0] == "f12words"]
    own = [r for r in rs if r["_unit"][0] == "f12own"]
    st = [r for r in rs if r["_unit"][0] == "f12start"]
    for world in ("tribal", "magic"):
        w = [r for r in words if r["world"] == world]
        if not w:
            continue
        leaks = sorted({x for r in w for x in r["leaks"]}); ew = sorted({x for r in w for x in r["earth_words"]})
        why = sorted({x for r in w for x in r["why_earth"]})
        lab = sorted({x for r in w for x in r["label_seed"]}); tit = sorted({x for r in w for x in r["title_seed"]})
        non = [x for r in w for x in r["own_not_on_offer"]]
        R.note(f"{world}: {len(w)} played lives (seeds {', '.join(str(r['seed']) for r in w)}), {sum(r['cps'] for r in w)} "
               f"moments put to the player, own acts shown {sum(r['own_shown'] for r in w)} (closed by the means "
               f"{sum(r['own_means'] for r in w)}); 'money' said {sum(r['money_mentions'] for r in w)} times (reported)")
        R.row(f"F12.1 {world}: no modern Earth story line", not leaks, f"{len(leaks)} told" + (": " + " | ".join(leaks[:3]) if leaks else ""))
        R.row(f"F12.1 {world}: no Earth word for a means or work", not ew and not why,
              f"{len(ew) + len(why)}" + (": " + ", ".join(ew + why[:3]) if ew or why else ""))
        R.row(f"F12.1 {world}: renamed options and moments in the world's words", not lab and not tit,
              f"{len(lab)} seed labels, {len(tit)} seed titles shown" + (": " + "; ".join((lab + tit)[:4]) if lab or tit else ""))
        R.row(f"F12.2 {world}: own acts never 'not on offer' (played)", not non,
              f"{len(non)}" + (": " + "; ".join(sorted(set(non))[:4]) if non else ""))
    for world in ("tribal", "magic"):
        w = [r for r in own if r["world"] == world]
        if not w:
            continue
        c = {k: sum(r[k] for r in w) for k in ("own_offered", "own_open", "own_means", "closed", "other_offered", "other_open")}
        R.row(f"F12.2 {world}: own acts never closed while the means allow (engine)", c["closed"] == 0,
              f"{c['closed']} of {c['own_offered']} own acts offered over {sum(r['lives'] for r in w)} lives x {w[0]['years']} "
              f"years (on offer {c['own_open'] / max(c['own_offered'], 1):.2f}, closed by the means "
              f"{c['own_means'] / max(c['own_offered'], 1):.2f}; other acts on offer {c['other_open'] / max(c['other_offered'], 1):.2f}); "
              f"{w[0]['own_acts']} own options in the library; switched on here: {', '.join(w[0]['forced']) or 'none'}")
    if st:
        lives = [(r["seed"], p, v) for r in st for p, v in r["starts"].items()]
        bad = [(s_, p) for s_, p, v in lives if "error" in v]
        ok = [(s_, p, v) for s_, p, v in lives if "error" not in v]
        R.row("F12.3 the four modern starts play with the world and the start", not bad and all(v["start_hold"] and v["world_hold"] for _, _, v in ok),
              f"{len(ok)} starts" + (f"; {len(bad)} without a world or a start" if bad else ""))
        nf = [(s_, p) for s_, p, v in ok if not v["fits"]]
        R.row("F12.3 the birth fits the start", not nf, f"{len(ok) - len(nf)} of {len(ok)}" + (f"; misses {nf[:6]}" if nf else ""))
        wrong = []
        for s_, p, v in ok:
            if v["pfaith"] < 0 and v["inherited"]:
                wrong.append((s_, p, "raised in a faith the family does not hold"))
            if v["inherited"] and v["prof_ok"] is False:
                wrong.append((s_, p, "raised in another faith than the family's"))
            if v["faith"] == "none" and v["held7"]:
                wrong.append((s_, p, "a faith at 7 in a start that promises none"))
            if v["faith"] not in (None, "none") and not v["inherited"]:
                wrong.append((s_, p, "a start that promises a faith, not raised in it"))
        R.row("F12.3 raised in the family's own faith, or none", not wrong, f"{len(wrong)} lives" + (f": {wrong[:4]}" if wrong else ""))
        pl = [(s_, p, v["place"], v["world_place"]) for s_, p, v in ok if v["place"] != v["world_place"]]
        R.row("F12.3 the story's place is the world's", not pl, f"{len(pl)} lives" + (f": {pl[:4]}" if pl else ""))
        same = [r["seed"] for r in st if len({v.get("world_seed") for v in r["starts"].values()}) < len(r["starts"])]
        R.row("F12.3 the four starts of a seed are four worlds", not same, f"{len(same)} seeds with a shared world")
        fam = {}
        for s_, p, v in ok:
            fam.setdefault(p, []).append(f"{v['kind']} c{v['cls']}{'' if v['pfaith'] < 0 else ' f'}")
        for p, xs in sorted(fam.items()):
            R.note(f"start {p}: " + ", ".join(f"{k} {xs.count(k)}" for k in sorted(set(xs), key=lambda k: -xs.count(k))[:6]))
    return R


JUDGE = dict(f4_age=judge_f4, f6_dreams=judge_f6, f12_start=judge_f12)


def plan(check, seeds, lives):
    if check == "f4_age":
        return [("f4", (s, lives), {}) for s in seeds]
    if check == "f6_dreams":
        return ([("f6", ("earth", s, lives), {}) for s in seeds]
                + [("f6", (w, s, lives), {}) for w in ("tribal", "magic") for s in seeds[:2]])
    if check == "f12_start":
        env = dict(CHROMA_GAME=json.dumps(dict(world_hold=True)), CHROMA_ENGINE=json.dumps(dict(own_open=True, start_hold=True)))
        return ([("f12defaults", (), {})]
                + [("f12words", (p, s), env) for p in ("5", "6") for s in F12_WORD_SEEDS]
                + [("f12start", (s,), env) for s in F12_START_SEEDS]
                + [("f12own", (w, s, min(lives, 200)), {}) for w in ("tribal", "magic") for s in seeds[:2]])
    raise ValueError(check)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "unit":
        repo, nm, args = sys.argv[2], sys.argv[3], sys.argv[4:]
        conv = [a if (nm == "f12words" and i == 0) or not re.fullmatch(r"\d+", a) else int(a) for i, a in enumerate(args)]
        print(json.dumps(UNITS[nm](repo, *conv), default=lambda o: o.item() if hasattr(o, "item") else str(o)))
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("check", choices=CHECKS + ("all",))
    ap.add_argument("--repo", default=os.path.dirname(HERE))
    ap.add_argument("--commit", default=None)
    ap.add_argument("--seeds", default="41-44")
    ap.add_argument("--lives", type=int, default=300)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-record", action="store_true")
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    lo, _, hi = a.seeds.partition("-")
    seeds = list(range(int(lo), int(hi or lo) + 1))
    commit = a.commit
    if commit is None:
        try:
            commit = subprocess.run(["git", "-C", repo, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or None
        except OSError:
            commit = None
    out = a.out or os.path.join(HERE, "out", time.strftime("fit_%Y%m%d-%H%M%S", time.gmtime()))
    os.makedirs(out, exist_ok=True)
    game = os.path.join(repo, "chroma-game", "prototype")   # its engine_pin from the folders the engine lives read
    gamepin.fill(game, root=repo, engine=os.path.join(repo, "chroma-engine", "v22-speedpass"),
                 lib=os.path.join(repo, "chroma-library"), packs=os.path.join(repo, "chroma-packs"))
    checks = CHECKS if a.check == "all" else (a.check,)
    rc = 0
    for check in checks:
        t0 = time.time(); lines = []
        log = lambda s: (lines.append(s), print(s, flush=True))
        log(f"{check} (K17), {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC; repo {repo}, commit {commit or '?'}; "
            f"the game plays {gamepin.where(game)}")
        R = JUDGE[check](run_units(repo, a.jobs, plan(check, seeds, a.lives), out, log))
        for l_ in R.lines:
            log(l_)
        res = "PASS" if R.ok else "FAIL"
        log(f"{check}: {res} ({round(time.time() - t0)} s)")
        rep = os.path.join(out, f"fit_{check}.txt")
        open(rep, "w").write("\n".join(lines) + "\n")
        if not a.no_record:
            sys.path.insert(0, HERE)
            import results
            results.add(check, res, os.path.relpath(rep, os.path.dirname(HERE)), note=f"K17, seeds {a.seeds}, {a.lives} lives",
                        candidate={"commit": commit} if commit else None, run=" ".join(sys.argv), secs=round(time.time() - t0))
        rc |= not R.ok
    return rc


if __name__ == "__main__":
    sys.exit(main())
