"""The world alone for 300 years: does the culture move, and do eras come from causes? Stage 3 of the v22 update,
LW1 (a culture that moves) and LW2 (history from causes), chroma-world/model/stage3-rules.md sections 2 and 3.

Runs 8 worlds of the first society ("typical rich", pace 1, seeds 1 to 8) for 300 years after the 80-year burn-in
and prints each check with its value, its target and ok or MISS, then a determinism check. On an engine without the
stage 3 rules (or with --rules off) the rows are printed as information only: that is today's baseline.

    OMP_NUM_THREADS=1 python3 -B chroma-engine/tools/world_alone.py [--worlds 8] [--years 300] [--pace 1]
        [--seed0 1] [--rules on|off] [--json FILE]

--years 500 gives the no-runaway check its full length. --json writes the numbers to FILE (under OUT_DIR when
relative; never into the repository). About 30 s for 8 x 300 years on one core.
"""
import sys, os, json, time, hashlib, argparse
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np
import world as WM
from world import World, COLORS, COMBO_KEYS, COMBO_MIX, _tv

C = 5
WK = 52
CALM, SHAKEN = 1.3, 1.8          # a decade's mean shake multiplier: calm below, shaken at or above (stage3-rules.md §2)
ACC_CALM, K_SH = 1.61, 2.0       # m_sh = clip(1 + k_sh (acc - acc_calm), 1, 3), unless the engine has its own (LW1 1g)
S3 = list(getattr(WM, "S3_RULES", []))   # the stage 3 world rules this engine has (empty before stage 3)
ROWS = []


def row(name, value, target, ok):
    """ok: True / False, or None for information only (always None when the rules are not on)."""
    flag = "" if ok is None or not RULES_ON else ("ok" if ok else "MISS")
    ROWS.append(dict(name=name, value=value, target=target, flag=flag))
    print(f"  {name:<52s} {value!s:<30s} {target:<34s} {flag}", flush=True)


def f(x, d=3):
    return "n/a" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{float(x):.{d}f}"


def kdir(key):
    v = np.array([1.0 / len(key) if c in key else 0.0 for c in COLORS]) - 0.2
    return v / np.linalg.norm(v)


def acc_now(W):
    """The shake index `acc` of World._society_q: read from the world when it keeps it (stage 3, LW1 1g), else
    recomputed here with the same formula from the state after the quarter (today's engine)."""
    if hasattr(W, "acc"):
        return float(W.acc)
    p = W.p
    rec = (W.phase == 1) * (1 + W.severity) / 3
    tn = np.array(W.tech_kind) >= 0
    tech = float((W.tech_adopt_v[tn] * (1 - W.tech_adopt_v[tn])).mean() * 4) if tn.any() else 0.0
    mixed = -5 <= W.regime < 6
    return float(1 + 1.0 * rec + 1.5 * W.unrest + 2.0 * (W._share_young() - 0.25) + 0.3 * tech
                 + 0.5 * (W.ext_trade.sum() + 10 * W.mig_in) * 0.3 + 0.5 * max(p["trust0"] - W.trust, 0) * 4
                 + 0.8 * (W.lost_war_q > 0) + p["mixed_acc"] * mixed)


_orig_society_q = World._society_q


def _society_q_logged(self):
    _orig_society_q(self)
    if getattr(self, "_wa_log", None) is not None:
        self._wa_log.append((int(self.t), acc_now(self), self.phase == 1, int(self.war), float(self.unrest)))


World._society_q = _society_q_logged


def run_world(seed, years, pace, rules):
    cfg = dict(trace=True, pace=pace)
    if S3:
        cfg["params"] = {r: (rules == "on") for r in S3}
    W = World(seed, cfg=cfg)
    W.burn_in(80)
    W._wa_log = []
    W.tick(W.t + years * WK)
    return W


def yearly(W, years):
    """Per run year: V, G, D0, the era vector e = era_i (era_p - 0.2), and the shake index (means over the year)."""
    t0 = W.t0
    tr = [x for x in W.trace if x["t"] > t0]
    by = {}
    for x in tr:
        by.setdefault((x["t"] - t0 - 1) // WK, []).append(x)
    V, G, D0, E = [], [], [], []
    for y in range(years):
        xs = by.get(y, [])
        V.append(np.mean([x["V"] for x in xs], 0)); G.append(np.mean([x["G"] for x in xs], 0))
        D0.append(np.mean([x["D0"] for x in xs], 0))
        e = np.zeros(C)
        for x in xs:
            if x["era"] is not None:
                e += x["era_i"] * (COMBO_MIX[COMBO_KEYS.index(x["era"])] - 0.2)
        E.append(e / max(len(xs), 1))
    acc = np.full(years, np.nan); calm = np.zeros(years, bool)
    lg = {}
    for t, a, rec, war, unrest in W._wa_log:
        lg.setdefault((t - t0 - 1) // WK, []).append((a, rec, war, unrest))
    for y in range(years):
        xs = lg.get(y, [])
        if xs:
            acc[y] = np.mean([a for a, *_ in xs])
            calm[y] = not any(r for _, r, _, _ in xs) and not any(w for _, _, w, _ in xs) and max(u for *_, u in xs) < 0.2
    return dict(V=np.array(V), G=np.array(G), D0=np.array(D0), E=np.array(E), acc=acc, calm=calm, tr=tr)


def main():
    global RULES_ON
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", type=int, default=8); ap.add_argument("--years", type=int, default=300)
    ap.add_argument("--pace", type=float, default=1.0); ap.add_argument("--seed0", type=int, default=1)
    ap.add_argument("--rules", choices=("on", "off"), default="on"); ap.add_argument("--json", default=None)
    a = ap.parse_args()
    RULES_ON = bool(S3) and a.rules == "on"
    print(f"engine {_engine.ENGINE}")
    print(f"stage 3 world rules in this engine: {', '.join(S3) or 'none (today: baseline, information only)'}; "
          f"rules {a.rules if S3 else 'n/a'}")
    print(f"{a.worlds} worlds, seeds {a.seed0} to {a.seed0 + a.worlds - 1}, {a.years} years after an 80-year burn-in, pace {a.pace}\n")
    t_start = time.time()
    worlds, recs = [], []
    for s in range(a.seed0, a.seed0 + a.worlds):
        W = run_world(s, a.years, a.pace, a.rules)
        worlds.append(W); recs.append(yearly(W, a.years))
    secs = time.time() - t_start
    Y = a.years
    out = {}

    # ---------------------------------------------------------------------------------- LW1: the culture
    print("LW1 A CULTURE THAT MOVES (stage3-rules.md §2)")
    acc_calm = float(worlds[0].p.get("acc_calm", ACC_CALM)); k_sh = float(worlds[0].p.get("k_sh", K_SH))
    med = float(np.nanmedian(np.concatenate([R["acc"][R["calm"]] for R in recs])))
    row("shake: acc_calm used / median yearly acc in calm years", f"{f(acc_calm, 2)} / {f(med, 2)}", "about 1.6", None)
    msh_of = lambda acc: np.clip(1 + k_sh * (acc - acc_calm), 1, 3)
    d10, msh, wid = [], [], []
    for i, R in enumerate(recs):
        m = msh_of(R["acc"])
        for y in range(0, Y - 10, 10):
            d10.append(float(np.abs(R["V"][y + 10] - R["V"][y]).mean()))
            msh.append(float(np.nanmean(m[y:y + 10]))); wid.append(i)
    d10, msh, wid = np.array(d10), np.array(msh), np.array(wid)
    calm, shk = msh < CALM, msh >= SHAKEN
    cm = float(np.median(d10[calm])) if calm.any() else np.nan
    sm = float(np.median(d10[shk])) if shk.any() else np.nan
    row("calm decades: V's change per colour (median)", f"{f(cm, 4)} (n={int(calm.sum())})", ".015 to .025 (Emren: about .02)",
        bool(0.015 <= cm <= 0.025) if np.isfinite(cm) else False)
    ratios = []
    for i in range(len(recs)):
        c_, s_ = d10[(wid == i) & calm], d10[(wid == i) & shk]
        if len(c_) and len(s_):
            ratios.append(float(np.median(s_) / max(np.median(c_), 1e-9)))
    rr = float(np.median(ratios)) if ratios else np.nan
    row("shaken decades: change per colour (median)", f"{f(sm, 4)} (n={int(shk.sum())})", "info", None)
    row("shaken over calm, same world (median of worlds)", f"{f(rr, 2)} (worlds={len(ratios)})", "2 to 3",
        bool(2 <= rr <= 3) if np.isfinite(rr) else False)
    cor = float(np.corrcoef(d10, msh)[0, 1]) if len(d10) > 2 and np.std(msh) > 0 else np.nan
    row("share of decades shaken", f"{f(shk.mean(), 2)} (calm {f(calm.mean(), 2)})", "info (some: about .15)", None)
    row("decade pace against its mean shake (correlation)", f(cor, 2), "above .4", bool(cor > 0.4) if np.isfinite(cor) else False)
    vd100 = [float(np.abs(R["V"][y + 100] - R["V"][y]).mean()) for R in recs for y in range(0, Y - 100, 100)]
    row("a century: V's change per colour (mean)", f(np.mean(vd100) if vd100 else np.nan, 4), "info (a century clearly)", None)
    dev = max(float(np.abs(R["V"] - R["V"][0]).max()) for R in recs)
    row("largest distance of any colour of V from its start", f(dev, 3), "within .12 (no runaway)", dev <= 0.12)
    h = Y // 2
    spr = float(np.mean([np.std(R["V"][h:], 0).mean() / max(np.std(R["V"][:h], 0).mean(), 1e-9) for R in recs]))
    row("spread of V, second half over first", f(spr, 2), "at most 1.5 (no trend)", spr <= 1.5)
    if Y < 500:
        row("(no-runaway check at full length)", f"{Y} years run", "run --years 500", None)
    # generations born 30 years apart differ in the direction of the eras of their youth
    pos, n_pairs = 0, 0
    for W, R in zip(worlds, recs):
        y0 = int(W.t0 // WK)                       # world year of the run's start
        for yb in range(-15, Y - 25 - 30):           # birth year in run years (formative years 15 to 25 inside the run)
            b1, b2 = W.Y0 + y0 + yb, W.Y0 + y0 + yb + 30
            if b1 < 0 or b2 >= len(W.coh) or not (W.coh_fixed[b1] and W.coh_fixed[b2]):
                continue
            if yb + 15 < 0:
                continue
            e1 = R["E"][yb + 15:yb + 26].sum(0); e2 = R["E"][yb + 45:yb + 56].sum(0)
            d = e2 - e1; dc = W.coh[b2] - W.coh[b1]
            if np.linalg.norm(d) < 1e-9 or np.linalg.norm(dc) < 1e-12:
                continue
            n_pairs += 1; pos += float(d @ dc) > 0
    sh = pos / n_pairs if n_pairs else np.nan
    row("generations 30 years apart differ in their eras' direction", f"{f(sh, 2)} (pairs={n_pairs})", "at least .70",
        bool(sh >= 0.7) if np.isfinite(sh) else False)
    out["lw1"] = dict(acc_calm=acc_calm, calm_median=cm, shaken_median=sm, ratio=rr, n_calm=int(calm.sum()),
                      n_shaken=int(shk.sum()), corr=cor, century=float(np.mean(vd100)) if vd100 else None, max_dev=dev,
                      spread_ratio=spr, gen_share=sh, gen_pairs=n_pairs)

    # ---------------------------------------------------------------------------------- LW2: history
    print("\nLW2 HISTORY FROM CAUSES (stage3-rules.md §3)")
    kinds, eras, lens, gaps, cos_next, turns, ans = [], 0, [], [], [], 0, []
    law_ch = 0
    for W in worlds:
        t0 = W.t0
        log = [e for e in W.log if e["t"] > t0]
        kinds += [e["key"] for e in log if e["domain"] == "era" and e["kind"] == "breakthrough"]
        el = [(e["t"], e["kind"], e["key"]) for e in W.log if e["domain"] == "era" and e["kind"] in ("era begins", "era ends")]
        seq = [k for t, kd, k in el if kd == "era begins" and t > t0]
        eras += len(seq)
        op = None
        for t, kd, k in el:
            if kd == "era begins":
                op = t
            elif op is not None and op > t0:
                lens.append((t - op) / WK)
        for (ta, ka, _), (tb, kb, _) in zip(el[:-1], el[1:]):
            if ka == "era ends" and kb == "era begins" and ta > t0:
                gaps.append((tb - ta) / WK)
        for x, y in zip(seq[:-1], seq[1:]):
            cs = float(kdir(x) @ kdir(y)); cos_next.append(cs); turns += cs < -1e-9
        law_ch += sum(1 for e in log if e["domain"] == "state" and e["kind"] == "law changed")
        for t, vec, era in getattr(W, "s3_era_ans", []):     # LW2 2d: the losers' grievance-weighted want at an era's start
            if t > t0 and era is not None:
                d = np.asarray(vec) - 0.2
                if np.linalg.norm(d) > 1e-9:
                    ans.append(float(kdir(era) @ (d / np.linalg.norm(d))))
    cen = len(worlds) * Y / 100
    ref = kinds.count("reform") / cen
    row("reform waves: one every ... years", f"{f(100 / ref if ref else np.inf, 1)} ({ref:.1f}/century)", "8 to 12",
        bool(ref and 8 <= 100 / ref <= 12))
    tps = turns / cen
    row("deep shifts (next era turns away): one every", f"{f(100 / tps if tps else np.inf, 1)} years", "20 to 35",
        bool(tps and 20 <= 100 / tps <= 35))
    rev = kinds.count("revolution") / cen
    row("revolutions per century", f(rev, 3), "essentially none", rev <= 0.05)
    row("eras per century", f(eras / cen, 2), "info (12-year eras, 8-year gaps)", None)
    row("era length, years", f"{f(np.mean(lens) if lens else np.nan, 1)} (n={len(lens)})", "near 12 (8 to 16)",
        bool(lens and 8 <= np.mean(lens) <= 16))
    row("gap between eras, years", f"{f(np.mean(gaps) if gaps else np.nan, 1)} (n={len(gaps)})", "near 8 (4 to 12)",
        bool(gaps and 4 <= np.mean(gaps) <= 12))
    mc = float(np.mean(cos_next)) if cos_next else np.nan
    row("consecutive eras: mean cosine of their directions", f"{f(mc, 2)} (n={len(cos_next)})", "-.6 to -.15 (swing back)",
        bool(-0.6 <= mc <= -0.15) if np.isfinite(mc) else False)
    am = float(np.mean(ans)) if ans else np.nan
    row("era direction against the last era's losers' want", f"{f(am, 2)} (n={len(ans)})", "cosine above .3",
        bool(am > 0.3) if np.isfinite(am) else (None if not RULES_ON else False))
    # government swings: the size of each change of government, and whether the next one is smaller in calm stretches
    sw_ratio, flips, sizes = [], [], []
    for W, R in zip(worlds, recs):
        tr = R["tr"]; t0 = W.t0
        ch = [i for i in range(1, len(tr)) if tr[i]["party"] != tr[i - 1]["party"]]
        s = [(tr[i]["t"], _tv(tr[i]["G"], tr[i - 1]["G"])) for i in ch]
        sizes += [x for _, x in s]
        for i in ch:
            g0, g1 = tr[i - 1]["G"] - tr[i - 1]["D0"], tr[i]["G"] - tr[i]["D0"]
            if np.linalg.norm(g0) > 1e-9 and np.linalg.norm(g1) > 1e-9:
                flips.append(float(g0 @ g1 / np.linalg.norm(g0) / np.linalg.norm(g1)))
        m = msh_of(R["acc"])
        for (ta, sa), (tb, sb) in zip(s[:-1], s[1:]):
            ya, yb = (ta - t0 - 1) // WK, (tb - t0 - 1) // WK
            if sa > 1e-6 and np.nanmean(m[max(ya, 0):yb + 1]) < CALM:
                sw_ratio.append(sb / sa)
    row("government changes per century", f(len(sizes) / cen, 1), "info", None)
    row("size of a change of government (TV, mean)", f(np.mean(sizes) if sizes else np.nan, 3), "info", None)
    fl = float(np.mean(flips)) if flips else np.nan
    row("lean against demand before and after a change (cos)", f(fl, 2), "info (today: the lean flips)", None)
    sr = float(np.median(sw_ratio)) if sw_ratio else np.nan
    row("next swing over the last, calm stretches (median)", f"{f(sr, 2)} (n={len(sw_ratio)})", ".6 to .9 (swings fade)",
        bool(0.6 <= sr <= 0.9) if np.isfinite(sr) else False)
    row("law changes per century", f(law_ch / cen, 1), "info (laws trail norms)", None)
    nr = float(np.mean([np.ptp(np.array([x["norms"] for x in R["tr"]]), 0).mean() for R in recs]))
    row("norms: mean range over the run", f(nr, 3), "info (S-curves; refit norm_v if they churn)", None)
    out["lw2"] = dict(reform_per_century=ref, deep_per_century=tps, revolutions=rev, eras_per_century=eras / cen,
                      era_len=float(np.mean(lens)) if lens else None, era_gap=float(np.mean(gaps)) if gaps else None,
                      era_cos=mc, era_answer=am, gov_changes=len(sizes) / cen,
                      swing_size=float(np.mean(sizes)) if sizes else None, flip_cos=fl, swing_ratio=sr,
                      laws_per_century=law_ch / cen, norm_range=nr)

    # ---------------------------------------------------------------------------------- determinism
    print("\nDETERMINISM")
    def fp(W):
        hs = hashlib.md5()
        for x in W.trace:
            hs.update(np.asarray(x["V"]).tobytes()); hs.update(np.asarray(x["G"]).tobytes()); hs.update(repr(x["era"]).encode())
        return hs.hexdigest()
    h1, h2 = fp(run_world(a.seed0, 60, a.pace, a.rules)), fp(run_world(a.seed0, 60, a.pace, a.rules))
    row("the same world seed twice (60 years): same history", "same" if h1 == h2 else "differs", "same", h1 == h2)
    out["deterministic"] = h1 == h2
    out.update(engine=_engine.ENGINE, rules=a.rules if S3 else None, s3_rules=S3, worlds=a.worlds, years=Y, pace=a.pace,
               seed0=a.seed0, seconds=round(secs, 1))
    n_miss = sum(r["flag"] == "MISS" for r in ROWS)
    print(f"\n{a.worlds} worlds x {Y} years in {secs:.0f} s. "
          + (f"{n_miss} MISS" if RULES_ON else "Baseline: no stage 3 rules on, rows are information only."))
    if a.json:
        p = a.json if os.path.isabs(a.json) else os.path.join(_engine.OUT, a.json)
        json.dump(dict(out, rows=ROWS), open(p, "w"), indent=1, default=float)
        print("wrote", p)
    return 1 if n_miss else 0


if __name__ == "__main__":
    sys.exit(main())
