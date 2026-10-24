"""The spheres finishing pack (chroma-world/spheres/finish-pack-draft.md): Release's rows W2 to W5 (records/v23/scope.md).

    python3 -B chroma-release/check_pack.py run --repo DIR --commit SHA --out DIR [--px JSON] [--moments]
                 [--seeds 41-52] [--lives 100] [--years 80] [--test-seeds 41-44] [--test-lives 60] [--jobs 4]
    python3 -B chroma-release/check_pack.py judge DIR [--no-record]

run lives batch lives on a git archive of the commit (engine, tools, Library, packs, chroma-env), every switch as
DEFAULT plus --px, the world on, Earth. Each seed is one world (world_seed = seed) with --lives lives in it, at one of
the game's presets 1 to 4 in turn (seed 41 preset 1, 42 preset 2, ...; the society as chroma-engine/tools/
world_starts.py sets it): "a typical rich modern world" (Emren's card, 10-17 08:54 UTC). --px names the pack's
switches when they are not on in DEFAULT yet, e.g. '{"place_turnover": true, "body_trust": true, "prison_ties": true,
"grey_gate": true}'; --moments sets batch.TURNOVER_MOMENTS, TRUST_MOMENTS, INMATE_MOMENTS and SHADOW_MOMENTS on, for a
commit where they are not on yet. The test seeds run W4's tie layer with prison_par test (25, 3): every life serves a
term from 25 to 28, so the ties have lives to form in (natural releases are few). One JSON a seed: what the rows read
from the Engine's readouts (chroma-engine/notes/world-fields.md, "Spheres finish pack"), not the readouts themselves.

judge pools the seeds and writes chroma-release/out/pack_<UTC>.txt and one results line per row:
    sph_places   W2 a town loses .03 to .07 of its places a year (closings over the town's places, 31 haunt kinds x 3,
                 over the towns and years of the run), and no haunt kind is empty in a town for more than 6 quarters
    sph_trust    W3 mean btrust per lead colour (at 40) within 1.2x; the share of adults' btrust under .3, over lives,
                 years and the eight spheres with bodies (a fifth to a third, as the surveys count one body at a time),
                 .15 to .35. Arts is left out: it names no body of its own (Outer world, 10-17 11:26 UTC)
    sph_inmates  W4 ties made 1 or 2 a year inside (made at release over the years of the term), never with a life
                 under 18, and every tie ended within 10 years
    sph_grey     W5 the share of lives whose town passes the grey gate (any sphere, any year they live) under .20; the
                 gate is the commit's own, sphere_data.SHADOW grey_gate (.25 as filed; the refit may move it)
The rest of each row is behaviour the readouts do not show, and is read from the Engine's t_steps rows (K3) and the
content checks (K1): a closing frees its regulars, steps their rung down one and ends the keeper's post (W2); care
seeking follows btrust (W3); strength .3, the pull back x1.2 ending with a partner or steady work,
tie_values.safety (W4); the gate's moments show only past it (W5).
Small counts: a row whose value sits inside its spread of its band's edge reads more seeds (the SMALL COUNTS ruling);
its target stays.
"""
import argparse, glob, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = "WUBRG"
DIRS = ["chroma-engine/v22-speedpass", "chroma-engine/tools", "chroma-library", "chroma-packs", "chroma-env"]
PRESETS = {1: "", 2: "W.6 G.4", 3: "U.7 R.3", 4: "B.6 R.4"}   # chroma-engine/tools/world_starts.py, the game's presets
FLAGS = ["TURNOVER_MOMENTS", "TRUST_MOMENTS", "INMATE_MOMENTS", "SHADOW_MOMENTS"]
LOW = 0.3


def span(s):
    out = []
    for part in s.split(","):
        lo, _, hi = part.partition("-")
        out += list(range(int(lo), int(hi or lo) + 1))
    return out


def one(a):
    """One seed (a subprocess of run): one world, its lives, what the rows read."""
    import numpy as np
    os.environ.update(CHROMA_ROOT=a.tree, OMP_NUM_THREADS="1")
    os.environ.pop("CHROMA_ENGINE", None)
    sys.path.insert(0, os.path.join(a.tree, "chroma-engine", "tools"))
    import _engine  # noqa: F401  (the tree's engine first on sys.path)
    import engine as E, batch, world as WM, sphere_data as SD, world_keys as WK
    if a.moments:
        for f in FLAGS:
            setattr(batch, f, True)
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    pr = (a.seed - 41) % 4 + 1
    P = dict(E.DEFAULT); P.update(json.loads(a.px)); P.update(world=True, world_seed=a.seed, world_cfg=dict(setting="earth"))
    if PRESETS[pr]:
        m = E.parse(PRESETS[pr]); m = m / m.sum()
        P["f_world"] = 0.25 * (m - 0.2) * 5 / 4; P["world_profile"] = 0.6 * np.full(E.C, 0.2) + 0.4 * m
    if a.test:
        P["prison_par"] = {**E.DEFAULT["prison_par"], **(P.get("prison_par") or {}), "test": (25, 3)}
    t0 = time.time()
    o = E.run(N=a.lives, years=a.years, seed=a.seed, lib=L, P=P)
    N, Y = a.lives, a.years
    dage = np.full(N, np.inf)
    for n_, t_, _ in o["died"]:
        dage[n_] = t_ / 52
    r = dict(seed=a.seed, preset=pr, lives=N, years=Y, test=bool(a.test), px=a.px, moments=bool(a.moments),
             secs=round(time.time() - t0), keys=sorted(k for k in ("place_turnover", "pt_lives", "btrust_y", "grey_y",
                                                                   "prison_ties") if k in o))
    if not a.test and "place_turnover" in o:   # W2
        q0 = int(o["world"]["t0"]) // 13; nq = 4 * Y; nl = len(WM.LOC_TABLE); kinds = list(WM.HAUNT_KINDS); slots = WM.N_PLACES
        log = [x for x in o["place_turnover"] if q0 <= int(x["q"]) < q0 + nq]
        cl = np.zeros((nl, Y), np.int64); why = {}
        for x in log:
            if x["what"] == "closed":
                cl[int(x["town"]), (int(x["q"]) - q0) // 4] += 1; why[x["why"].split(":")[0]] = why.get(x["why"].split(":")[0], 0) + 1
        # empty spells: a kind with none of its slots open in a town; slots open at the run's start unless the burn-in's
        # last closing in that slot came after its last opening
        state = {}
        for x in o["place_turnover"]:
            if int(x["q"]) < q0:
                state[(int(x["town"]), x["kind"], int(x["slot"]))] = x["what"]
        open_ = {(l, k): sum(state.get((l, k, i), "opened") == "opened" for i in range(slots)) for l in range(nl) for k in kinds}
        run_ = {key: 0 for key in open_}; longest = 0; where = None
        byq = {}
        for x in log:
            byq.setdefault(int(x["q"]), []).append(x)
        for q in range(q0, q0 + nq):
            for x in byq.get(q, ()):
                key = (int(x["town"]), x["kind"]); open_[key] += 1 if x["what"] == "opened" else -1
            for key, v in open_.items():
                run_[key] = run_[key] + 1 if v <= 0 else 0
                if run_[key] > longest:
                    longest, where = run_[key], f"town {key[0]} {key[1]}"
        r["w2"] = dict(per_town=slots * len(kinds), towns=nl, closed_y=cl.tolist(), why=why, longest_empty_q=longest,
                       where=where, haunts_closed_life_y=float(np.asarray(o["pt_lives"]).sum() / max(1, (np.minimum(dage, Y)).sum())))
    if not a.test and "btrust_y" in o:   # W3
        bt = np.asarray(o["btrust_y"], float)   # N x years x 9, NaN before 15
        W = np.asarray(o["W_hist"]); lead = np.argmax(W[min(40, Y)], 1)
        ages = np.arange(bt.shape[1])[None, :]
        adult = (ages >= 18) & (ages < dage[:, None])
        bod = [j for j, s_ in enumerate(WK.SPHERES) if s_ != "arts"]   # the eight spheres with bodies of their own
        x = np.where(adult[:, :, None], bt, np.nan)[:, :, bod]
        ok = ~np.isnan(x)
        per_life = np.nanmean(x.reshape(N, -1), 1) if ok.any() else np.full(N, np.nan)
        a40 = dage > 40
        r["w3"] = dict(spheres=[WK.SPHERES[j] for j in bod], values=int(ok.sum()), low=int((x[ok] < LOW).sum()),
                       low_sph=[[int((x[:, :, j][ok[:, :, j]] < LOW).sum()), int(ok[:, :, j].sum())] for j in range(x.shape[2])],
                       lead={COLS[c]: [float(np.nansum(per_life[a40 & (lead == c)])), int((a40 & (lead == c) & ~np.isnan(per_life)).sum())]
                             for c in range(5)})
    if "grey_y" in o:   # W5 (the test seeds' lives are all inside for three years; W5 reads the other seeds)
        g = np.asarray(o["grey_y"], float)   # N x records x 9, each life's own town
        rec = np.arange(g.shape[1])[None, :]
        alive = rec < dage[:, None]
        gg = SD.SHADOW["grey_gate"]; gate = float(gg["threshold"] if isinstance(gg, dict) else gg)
        mx = np.where(alive, g.max(2), -1.0)
        r["w5"] = dict(lives=N, gate=gate, past=int((mx >= gate).any(1).sum()), town_max=[float(v) for v in np.sort(mx.max(1))])
    if "prison_ties" in o:   # W4
        made, end = {}, {}
        young = 0
        for x in o["prison_ties"]:
            key = (int(x["n"]), int(x["other"]))
            if x["what"] == "made":
                made.setdefault(key, []).append(int(x["t"]))
                young += int(x["t"]) < 52 * 18
            else:
                end.setdefault(key, []).append((int(x["t"]), x["why"]))
        span_ = []; open_late = 0; why = {}
        for key, ts in made.items():
            for t_ in ts:
                e_ = [e for e in end.get(key, []) if e[0] >= t_]
                if e_:
                    span_.append(min(e_)[0] - t_); why[min(e_)[1]] = why.get(min(e_)[1], 0) + 1
                elif t_ + 520 <= 52 * Y:
                    open_late += 1
        per = {}
        for (n_, _), ts in made.items():
            per[n_] = per.get(n_, 0) + len(ts)
        r["w4"] = dict(made=sum(len(v) for v in made.values()), lives_with=len(per), per_life=sorted(per.values()),
                       young=young, longest_w=max(span_) if span_ else None, open_past_10y=open_late, why=why,
                       released=int(N - (dage < 28).sum()) if a.test else None)
    json.dump(r, open(a.out + ".tmp", "w")); os.replace(a.out + ".tmp", a.out)
    print("seed", a.seed, "preset", pr, "test" if a.test else "", r["secs"], "s", flush=True)


def run(a):
    os.makedirs(a.out, exist_ok=True)
    sha = subprocess.run(["git", "-C", a.repo, "rev-parse", a.commit], check=True, capture_output=True, text=True).stdout.strip()
    tree = os.path.join(a.out, "tree")
    stamp = os.path.join(tree, "tree.sha")
    if not (os.path.exists(stamp) and open(stamp).read().strip() == sha):   # never reuse another commit's tree
        subprocess.run(["rm", "-rf", tree], check=True); os.makedirs(tree)
        subprocess.run(f"git -C {a.repo} archive {sha} {' '.join(DIRS)} | tar -x -C {tree}", shell=True, check=True)
        open(stamp, "w").write(sha + "\n")
        for f in glob.glob(os.path.join(a.out, "seed*.json")) + glob.glob(os.path.join(a.out, "test*.json")):
            os.remove(f)   # worlds of another commit
    json.dump(dict(commit=sha, px=a.px, moments=a.moments, seeds=a.seeds, lives=a.lives, years=a.years,
                   test_seeds=a.test_seeds, test_lives=a.test_lives, time=time.strftime("%Y-%m-%d %H:%M", time.gmtime())),
              open(os.path.join(a.out, "meta.json"), "w"))
    env = {k: v for k, v in os.environ.items() if k not in ("CHROMA_ROOT", "CHROMA_ENGINE", "CHROMA_GAME")}
    base = [sys.executable, "-B", os.path.abspath(__file__), "one", "--tree", tree, "--px", a.px] + (["--moments"] if a.moments else [])
    jobs = []
    for sd in span(a.test_seeds) if a.test_seeds else []:
        f = os.path.join(a.out, f"test{sd}.json")
        if not os.path.exists(f):
            jobs.append(base + ["--seed", str(sd), "--lives", str(a.test_lives), "--years", "45", "--test", "--out", f])
    for sd in span(a.seeds) if a.seeds else []:   # --seeds "": the test worlds only
        f = os.path.join(a.out, f"seed{sd}.json")
        if not os.path.exists(f):
            jobs.append(base + ["--seed", str(sd), "--lives", str(a.lives), "--years", str(a.years), "--out", f])
    log = open(os.path.join(a.out, "run.log"), "a")
    live, bad = [], 0
    while jobs or live:
        while jobs and len(live) < a.jobs:
            live.append(subprocess.Popen(jobs.pop(0), env=env, stdout=log, stderr=log))
        time.sleep(2)
        for p in [p for p in live if p.poll() is not None]:
            live.remove(p); bad += p.returncode != 0
    print(f"run {sha[:12]} px {a.px}: {len(glob.glob(os.path.join(a.out, 'seed*.json')))} seeds and "
          f"{len(glob.glob(os.path.join(a.out, 'test*.json')))} test seeds in {a.out}, {bad} failed")
    return 1 if bad else 0


def judge(a):
    import numpy as np
    meta = json.load(open(os.path.join(a.dir, "meta.json")))
    S = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(a.dir, "seed*.json")))]
    T = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(a.dir, "test*.json")))]
    lines = [f"Spheres finishing pack, rows W2 to W5, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
             f"  {a.dir}: commit {meta['commit'][:12]} px {meta['px']} moments {meta['moments']}; {len(S)} seeds "
             f"({sum(s['lives'] for s in S)} lives, {meta['years']} years, presets {sorted({s['preset'] for s in S})}), {len(T)} test seeds"]
    res = {}
    # W2
    w2 = [s["w2"] for s in S if "w2" in s]
    if w2:
        sh = np.concatenate([np.asarray(x["closed_y"], float).ravel() / x["per_town"] for x in w2])
        m = float(sh.mean()); lo, hi = np.percentile(sh, [10, 90]); se = float(sh.std(ddof=1) / len(sh) ** 0.5)
        lng = max(x["longest_empty_q"] for x in w2); wh = [x["where"] for x in w2 if x["longest_empty_q"] == lng][0]
        why = {}
        for x in w2:
            for k, v in x["why"].items():
                why[k] = why.get(k, 0) + v
        ok = 0.03 <= m <= 0.07 and lng <= 6
        res["sph_places"] = (ok, f"closed {m:.3f} of a town's places a year (.03 to .07); longest empty kind {lng} quarters (at most 6)")
        lines.append(f"{'ok  ' if ok else 'MISS'} W2 places close: {m:.4f} of a town's places a year (+-{se:.4f}; town-years 10% to 90%: "
                     f"{lo:.3f} to {hi:.3f}), target .03 to .07; why {why}; longest a haunt kind stood empty in a town: {lng} "
                     f"quarters ({wh}), target at most 6; a life's own haunts closed {np.mean([x['haunts_closed_life_y'] for x in w2]):.3f} a year")
    else:
        res["sph_places"] = (False, "no place_turnover readout (switch off?)"); lines.append("MISS W2: no place_turnover readout")
    # W3
    w3 = [s["w3"] for s in S if "w3" in s]
    if w3:
        ALL9 = ['rule', 'gather', 'arts', 'faith', 'care', 'learn', 'prod', 'comm', 'prot']   # a seed file from before arts was left out
        for x in w3:
            if "spheres" not in x:
                keep = [j for j, nm in enumerate(ALL9) if nm != "arts"]
                x["low_sph"] = [x["low_sph"][j] for j in keep]; x["spheres"] = [ALL9[j] for j in keep]
                x["low"] = sum(v[0] for v in x["low_sph"]); x["values"] = sum(v[1] for v in x["low_sph"])
        vals = sum(x["values"] for x in w3); low = sum(x["low"] for x in w3); share = low / max(1, vals)
        lead = {c: [sum(x["lead"][c][0] for x in w3), sum(x["lead"][c][1] for x in w3)] for c in COLS}
        means = {c: v[0] / v[1] for c, v in lead.items() if v[1]}
        ratio = max(means.values()) / min(means.values()) if len(means) == 5 else float("nan")
        hi_c, lo_c = max(means, key=means.get), min(means, key=means.get)
        per = [sum(x["low_sph"][j][0] for x in w3) / max(1, sum(x["low_sph"][j][1] for x in w3)) for j in range(len(w3[0]["low_sph"]))]
        ok = ratio <= 1.2 and 0.15 <= share <= 0.35
        res["sph_trust"] = (ok, f"lead colours {ratio:.3f}x (at most 1.2), under .3 {share:.3f} (.15 to .35)")
        lines.append(f"{'ok  ' if ok else 'MISS'} W3 trust: mean btrust by the colour leading at 40 "
                     + ", ".join(f"{c} {means[c]:.3f} ({lead[c][1]})" for c in means)
                     + f"; highest over lowest {ratio:.4f} ({hi_c} over {lo_c}), target at most 1.2; adults' values under .3 "
                     f"{share:.4f} ({low} of {vals}), target .15 to .35; by sphere "
                     + " ".join(f"{nm} {v:.3f}" for nm, v in zip(w3[0].get("spheres", range(len(per))), per)))
    else:
        res["sph_trust"] = (False, "no btrust_y readout (switch off?)"); lines.append("MISS W3: no btrust_y readout")
    # W4
    w4 = [s["w4"] for s in T if "w4" in s]
    if w4:
        rel = sum(x["released"] or 0 for x in w4); made = sum(x["made"] for x in w4)
        per = [v for x in w4 for v in x["per_life"]]
        out_ = [v for v in per if not 3 <= v <= 6]   # 1 or 2 a year over the 3-year term (cap 6)
        young = sum(x["young"] for x in w4) + sum(s.get("w4", {}).get("young", 0) for s in S)
        late = sum(x["open_past_10y"] for x in w4); lw = max((x["longest_w"] or 0) for x in w4)
        why = {}
        for x in w4:
            for k, v in x["why"].items():
                why[k] = why.get(k, 0) + v
        nat = [s["w4"] for s in S if "w4" in s]
        ok = bool(per) and not out_ and not young and not late and lw <= 520
        res["sph_inmates"] = (ok, f"{len(per)} lives made {made} ties over 3 years inside, {len(out_)} outside 1 to 2 a year; "
                                  f"{young} with a child; {late} past 10 years")
        lines.append(f"{'ok  ' if ok else 'MISS'} W4 former inmates: test term 25 to 28, {rel} lives out alive, {len(per)} made ties "
                     f"({made}, {made / max(1, len(per)) / 3:.2f} a year inside; {len(out_)} lives outside 1 to 2 a year); {young} ties "
                     f"made before 18; longest {lw / 52:.1f} years, {late} still open past 10 years; ended {why}; natural lives made "
                     f"{sum(x['made'] for x in nat)} ties in {sum(x['lives_with'] for x in nat)} of {sum(s['lives'] for s in S)} lives")
    else:
        res["sph_inmates"] = (False, "no prison_ties readout on the test seeds"); lines.append("MISS W4: no prison_ties readout on the test seeds")
    # W5
    w5 = [s["w5"] for s in S if "w5" in s]
    if w5:
        gate = w5[0].get("gate", 0.25)   # the commit's gate (a seed file from before it was read: the filed .25)
        mx = np.concatenate([x["town_max"] for x in w5])
        nl = sum(x["lives"] for x in w5); past = int((mx >= gate).sum()); share = past / max(1, nl)
        se = (share * (1 - share) / max(1, nl)) ** 0.5
        ok = share < 0.20
        res["sph_grey"] = (ok, f"{share:.3f} of lives see their town past {gate:.2f} (under .20)")
        lines.append(f"{'ok  ' if ok else 'MISS'} W5 grey: {past} of {nl} lives ({share:.4f} +-{se:.4f}) live in a town past the gate {gate:.2f} "
                     f"in some sphere, target under .20; the most grey a life's town got, median {np.median(mx):.3f}, 90% {np.percentile(mx, 90):.3f}")
    else:
        res["sph_grey"] = (False, "no grey_y readout (switch off?)"); lines.append("MISS W5: no grey_y readout")
    lines.append("  Behaviour each row also needs, read from t_steps (K3) and the content checks (K1): W2 regulars, rung and post; "
                 "W3 care seeking; W4 strength .3, the pull back and its end, tie_values.safety; W5 the gate's moments.")
    allok = all(v[0] for v in res.values())
    lines.append(f"pack: {'PASS' if allok else 'FAIL'} ({sum(v[0] for v in res.values())} of {len(res)} rows)")
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "chroma-env"))
    os.environ.setdefault("CHROMA_ROOT", os.path.dirname(HERE))
    from paths import path
    rep = path("release_out", f"pack_{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}.txt")
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    open(rep, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); print("report:", rep)
    if not a.no_record:
        sys.path.insert(0, HERE)
        from results import add
        for k, (ok_, note) in res.items():
            add(k, "PASS" if ok_ else "FAIL", rep, note=note, candidate={"commit": meta["commit"]}, run=" ".join(sys.argv))
    return 0 if allok else 1


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("run")
p.add_argument("--repo", required=True); p.add_argument("--commit", required=True); p.add_argument("--out", required=True)
p.add_argument("--px", default="{}"); p.add_argument("--moments", action="store_true")
p.add_argument("--seeds", default="41-52"); p.add_argument("--lives", type=int, default=100); p.add_argument("--years", type=int, default=80)
p.add_argument("--test-seeds", default="41-44"); p.add_argument("--test-lives", type=int, default=60)
p.add_argument("--jobs", type=int, default=4)
p = sub.add_parser("one")
p.add_argument("--tree", required=True); p.add_argument("--px", default="{}"); p.add_argument("--moments", action="store_true")
p.add_argument("--seed", type=int, required=True); p.add_argument("--lives", type=int, required=True)
p.add_argument("--years", type=int, required=True); p.add_argument("--test", action="store_true"); p.add_argument("--out", required=True)
p = sub.add_parser("judge")
p.add_argument("dir"); p.add_argument("--no-record", action="store_true", help="write the report but no results lines (a trial)")
a = ap.parse_args()
sys.exit({"run": run, "one": one, "judge": judge}[a.cmd](a) or 0)
