"""Real-data anchor (v6): read every simulated person as Schwartz's ten basic human values and compare with surveys.

The translation is not hand-tuned per color. Each of Schwartz's ten values is placed on Wizards' five enemy axes
(engine.AXES) from Schwartz's own definition of it; a color's weight on a value is then how far the color and the
value agree across the five axes. A person's value scores are their color weights pushed through that map and
centred within the person, the way survey answers are centred (Schwartz 2012).

python3 schwartz.py [N] [seed] [sym]     (sym=1 uses the balanced library; mean age trends then vanish by design)
"""
import sys, json, numpy as np
from engine import *

VALUES = ["self-direction", "stimulation", "hedonism", "achievement", "power",
          "security", "conformity", "tradition", "benevolence", "universalism"]     # Schwartz's circle order
SHORT = ["SD", "ST", "HE", "AC", "PO", "SE", "CO", "TR", "BE", "UN"]

# Each value on the five axes, from Schwartz's definitions (+ = group, security, head, destiny, nature;
# - = individual, freedom, heart, free will, nurture). 1 = the defining side, 0.5 = a secondary side.
VALUE_AXES = {                #  group  security  head  destiny  nature
    "self-direction": [-1.0, -1.0,  0.0, -1.0, -0.5],   # independent thought and action; choosing, creating, cultivating own abilities
    "stimulation":    [-0.5, -1.0, -1.0,  0.0,  0.0],   # excitement, novelty, challenge
    "hedonism":       [-1.0, -0.5, -1.0,  0.0,  0.0],   # pleasure and sensuous gratification for oneself
    "achievement":    [-1.0,  0.0,  0.5, -0.5, -1.0],   # personal success through competence; effort and self-improvement
    "power":          [-1.0,  0.0,  0.0, -0.5,  0.0],   # status, control and dominance over people and resources
    "security":       [ 0.0,  1.0,  0.5,  0.0,  0.0],   # safety, harmony, stability of society, relationships and self
    "conformity":     [ 1.0,  1.0,  1.0,  0.0,  0.0],   # restraint of impulses that would upset others or break norms
    "tradition":      [ 1.0,  0.5,  0.0,  1.0,  1.0],   # respect for customs and religion; accepting one's portion in life
    "benevolence":    [ 1.0,  0.0,  0.0,  0.0,  0.0],   # the welfare of people close to one
    "universalism":   [ 1.0, -0.5,  0.0,  0.0,  0.5],   # understanding, tolerance, justice for all people and for nature
}
AX = np.array([AXES[k] for k in AXES], float)                      # 5 axes x 5 colors
LOAD = np.array([VALUE_AXES[v] for v in VALUES]) @ AX               # 10 values x 5 colors
HIGHER = {"openness to change": ["self-direction", "stimulation"],
          "self-enhancement": ["achievement", "power"],
          "conservation": ["security", "conformity", "tradition"],
          "self-transcendence": ["benevolence", "universalism"]}       # hedonism sits between openness and self-enhancement
HI = {k: [VALUES.index(v) for v in vs] for k, vs in HIGHER.items()}


def scores(W):
    """Color weights (..., 5) -> centred value scores (..., 10)."""
    raw = W @ LOAD.T
    return raw - raw.mean(-1, keepdims=True)


def higher(S):
    return {k: S[..., ix].mean(-1) for k, ix in HI.items()}


def color_angles():
    """Where each color lands on Schwartz's circle (values equally spaced), from the map alone."""
    ang = np.radians(np.arange(10) * 36)
    out = {}
    for c in range(C):
        L = LOAD[:, c] - LOAD[:, c].mean()
        out[COLORS[c]] = int(round(np.degrees(np.arctan2((L * np.sin(ang)).sum(), (L * np.cos(ang)).sum())) % 360))
    return out


def r(a, b):
    return round(float(np.corrcoef(a, b)[0, 1]), 2)


def survey(o, lo=15, hi=80, seed=0):
    """Each person answers once, at a random age between lo and hi, as in a cross-sectional survey."""
    W = o["W_hist"]; N = W.shape[1]
    rng = np.random.default_rng(seed)
    age = rng.integers(lo, min(hi, len(W) - 1) + 1, N)
    return age, scores(W[age, np.arange(N)])


def age_trends(o):
    age, S = survey(o)
    H = higher(S)
    sd = S.std(0)
    young, old = age < 30, age >= 60
    return {"age r, values": {v: r(age, S[:, i]) for i, v in enumerate(VALUES)},
            "age r, higher order": {k: r(age, x) for k, x in H.items()},
            "60+ minus under 30, in SD": {v: round(float((S[old, i].mean() - S[young, i].mean()) / sd[i]), 2) for i, v in enumerate(VALUES)}}


def youth_trends(o, a0=8, a1=20):
    """Longitudinal mean change from childhood to early adulthood, in SD units at a0."""
    S0 = scores(o["W_hist"][a0]); S1 = scores(o["W_hist"][a1]); sd = S0.std(0) + 1e-9
    H0, H1 = higher(S0), higher(S1)
    return {"values": {v: round(float((S1[:, i].mean() - S0[:, i].mean()) / sd[i]), 2) for i, v in enumerate(VALUES)},
            "higher order": {k: round(float((H1[k].mean() - H0[k].mean()) / (H0[k].std() + 1e-9)), 2) for k in H0}}


def stability(o, pairs=((10, 12), (14, 16), (20, 22), (20, 28), (30, 32), (45, 47), (60, 62), (16, 66))):
    W = o["W_hist"]; out = {}
    for a, b in pairs:
        if b >= len(W): continue
        Sa, Sb = scores(W[a]), scores(W[b])
        out[f"{a}->{b}"] = round(float(np.mean([np.corrcoef(Sa[:, i], Sb[:, i])[0, 1] for i in range(10)])), 2)
    return out


def structure(o, age=40):
    """Correlations between the ten values across people, and the circle order they imply (first two components)."""
    S = scores(o["W_hist"][age])
    R = np.corrcoef(S.T)
    near = np.mean([R[i, (i + 1) % 10] for i in range(10)])
    far = np.mean([R[i, (i + 5) % 10] for i in range(10)])
    ev, vec = np.linalg.eigh(R); v1, v2 = vec[:, -1], vec[:, -2]
    ang = np.degrees(np.arctan2(v2, v1)) % 360
    order = [SHORT[i] for i in np.argsort(ang)]
    return {"mean r, neighbours on the circle": round(float(near), 2), "mean r, opposite values": round(float(far), 2),
            "order around the first two components": " ".join(order),
            "power vs universalism": round(float(R[4, 9]), 2), "stimulation vs tradition": round(float(R[1, 7]), 2),
            "benevolence vs universalism": round(float(R[8, 9]), 2), "security vs conformity": round(float(R[5, 6]), 2)}


def wellbeing(o, age=40):
    S = scores(o["W_hist"][age]); sat = o["V_hist"]["content"][age]; pc = o["V_hist"]["peace"][age]
    H = higher(S)
    growth = (S[:, [0, 1, 8, 9]].mean(1) - S[:, [4, 5, 6, 7]].mean(1))     # growth minus self-protection (Schwartz 2012)
    return {"satisfaction r, values": {v: r(sat, S[:, i]) for i, v in enumerate(VALUES)},
            "satisfaction r, higher order": {k: r(sat, x) for k, x in H.items()},
            "satisfaction r, growth minus self-protection": r(sat, growth), "peace r, growth minus self-protection": r(pc, growth)}


def life_event(o, kind="children", lo=22, hi=45, before=1, after=3):
    """Change in each higher-order value around taking on a commitment, against people of the same age who did not."""
    K = o["K_hist"][:, :, KIDX[kind]] > 0; W = o["W_hist"]; N = W.shape[1]; Y = len(W)
    start = np.full(N, -1)
    for n in range(N):
        ys = np.nonzero(K[:, n])[0]
        if len(ys): start[n] = ys[0]
    H = {a: higher(scores(W[a])) for a in range(Y)}
    sdv = {k: np.std(H[40][k]) for k in HI}
    res = {k: [] for k in HI}
    for n in np.nonzero((start >= lo) & (start <= hi))[0]:
        a = start[n]
        if a - before < 0 or a + after >= Y: continue
        others = ~K[a + after] & ~K[a - before]
        for k in HI:
            d = H[a + after][k][n] - H[a - before][k][n]
            d0 = (H[a + after][k][others] - H[a - before][k][others]).mean()
            res[k].append((d - d0) / sdv[k])
    return {"people": len(res["conservation"]), **{k: round(float(np.mean(v)), 2) for k, v in res.items()}}


def top_value(o, age=40):
    S = scores(o["W_hist"][age]); t = np.bincount(S.argmax(1), minlength=10) / len(S)
    return {v: round(float(x), 2) for v, x in zip(VALUES, t)}


# Real targets. Age correlations: European Social Survey, pooled rounds (Schwartz 2006; Robinson 2013), cross-sectional
# r with age, higher-order values approximated from their member values. Stability: test-retest correlations of single
# values (Vecchione et al. 2016, 2 years in young adults; Milfont, Milojev & Sibley 2016, 3 years; Leijen et al. 2022,
# 12 years, .42 to .55 by generation). Well-being: values relate weakly to life satisfaction, |r| < .15, growth values a
# little positive (Sagiv & Schwartz 2000; Sortheix & Schwartz 2017). Parenthood: new parents move toward conservation
# and away from openness (Loennqvist et al. 2018). Ranges are what counts as a match.
TARGETS = {
    # simulated people share one birth cohort, so they show ageing alone: about half the ESS cross-sectional slope,
    # which mixes ageing with generation (Library notes E10; Leijen et al. 2022). Full ESS r: CON .30, OC -.25, SE -.20, ST .15
    "age r, conservation": (0.15, 0.08, 0.30, "ESS, ageing half"),
    "age r, openness to change": (-0.13, -0.25, -0.06, "ESS, ageing half"),
    "age r, self-enhancement": (-0.10, -0.20, -0.04, "ESS, ageing half"),
    "age r, self-transcendence": (0.08, 0.02, 0.15, "ESS, ageing half"),
    # stability as surveys measure it: simulated correlations times REL, the survey's own test-retest reliability
    "2-year stability around 20": (0.55, 0.45, 0.70, "Vecchione 2016; Bardi 2009"),
    "2-year stability around 45": (0.70, 0.60, 0.85, "Milfont 2016"),
    "12-year stability, adults": (0.50, 0.40, 0.60, "Leijen 2022"),
    "50-year stability, 16 to 66": (0.30, 0.15, 0.45, "extrapolated"),
    "satisfaction r, growth values": (0.08, -0.05, 0.15, "Sortheix 2017"),
    "parenthood, conservation (SD)": (0.20, 0.0, 0.5, "Loennqvist 2018"),
    "parenthood, openness (SD)": (-0.20, -0.5, 0.0, "Loennqvist 2018"),
}


REL = 0.8   # test-retest reliability of a value measured twice a few weeks apart (PVQ, about .66 to .88; Schwartz et al. 2001)


def compare(o):
    """Simulated against real, one row per target: (name, simulated, real, low, high, source, inside range)."""
    a = age_trends(o)["age r, higher order"]; st = stability(o, ((20, 22), (45, 47), (30, 42), (40, 52), (50, 62), (16, 66)))
    wb = wellbeing(o); par = life_event(o, "children")
    st = {k_: round(REL * v_, 2) for k_, v_ in st.items()}   # a survey measures each value with error
    sim = {"age r, conservation": a["conservation"], "age r, openness to change": a["openness to change"],
           "age r, self-enhancement": a["self-enhancement"], "age r, self-transcendence": a["self-transcendence"],
           "2-year stability around 20": st["20->22"], "2-year stability around 45": st["45->47"],
           "12-year stability, adults": round(float(np.mean([st["30->42"], st["40->52"], st["50->62"]])), 2),
           "50-year stability, 16 to 66": st["16->66"],
           "satisfaction r, growth values": wb["satisfaction r, growth minus self-protection"],
           "parenthood, conservation (SD)": par["conservation"], "parenthood, openness (SD)": par["openness to change"]}
    return [(k, sim[k], t, lo, hi, src, bool(lo <= sim[k] <= hi)) for k, (t, lo, hi, src) in TARGETS.items()]


def load_or_run(N, seed, sym, cache_dir=None):
    """Runs a population once and keeps only what the survey needs, so the map can be re-read without rerunning."""
    import os
    cache_dir = cache_dir or os.environ.get("CHROMA_CACHE", "/tmp")
    f = f"{cache_dir}/chroma_survey_{N}_{seed}_{int(sym)}.npz"
    if os.path.exists(f):
        d = np.load(f)
        return {"W_hist": d["W"], "K_hist": d["K"], "V_hist": {"content": d["content"], "peace": d["peace"]}}
    if sym:
        from grid import LIB_SYM
    o = run(N=N, seed=seed, lib=LIB_SYM if sym else None)
    np.savez_compressed(f, W=o["W_hist"], K=o["K_hist"], content=o["V_hist"]["content"], peace=o["V_hist"]["peace"])
    return o


def report(o):
    return {"against real data": [f"{k}: simulated {v:+.2f}, real {t:+.2f} ({src}) {'ok' if ok else 'OFF'}" for k, v, t, lo, hi, src, ok in compare(o)],
            "color angles on the circle": color_angles(), "age trends": age_trends(o), "childhood to 20": youth_trends(o),
            "rank-order stability": stability(o), "structure at 40": structure(o), "well-being at 40": wellbeing(o),
            "becoming a parent": life_event(o, "children"), "taking on a career": life_event(o, "career", 16, 35),
            "joining a faith": life_event(o, "faith", 12, 60), "top value at 40": top_value(o)}


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 11
    sym = len(sys.argv) > 3 and sys.argv[3] == "1"
    o = load_or_run(N, seed, sym)
    print("loadings (values x W U B R G):")
    for v, row in zip(VALUES, LOAD): print(f"  {v:15s}", " ".join(f"{x:+5.1f}" for x in row))
    print(json.dumps(report(o), indent=1))
