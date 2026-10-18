"""(Release's copy of chroma-ideas/player-impact/scripts/impact.py, md5 286b2b4430cc, 10-17, for check_picks.py; one change:
the start is env PRESET, default 1 as before.)

Player impact on a life: whole lives on the Game object (as the page runs them), played by stand-in players.

    python3 -B impact.py <out_dir> <policy> <seed> [<seed> ...]     (env FREQ=normal|often|rare, V224=1 for v22.4's switches)

policies:
  none     no voice at all: no moments are put to the player, and the weeks weigh whole (quiet_k 1): an unplayed life
  let      the voice is there and lets them choose at every moment (default pacing)
  random   a random open option at every moment
  reader   reads what the moment shows (felt odds with the reality hint, reluctance, needs it would feed, titles and perks it
           gives or takes, money and time it costs or wins, a commitment it may start) and pushes when that beats their
           own pick by a margin; otherwise lets them choose
  oracle   as reader, but with the true odds and every need's real gain (an upper bound for picking well)
  steer:C  always pushes the option with most of colour C (as test/steer_check.py most:C)
"""
import sys, os, json, random, time
GAMEDIR = os.environ.get("GAMEDIR", "/home/user/Chroma_Prototype/chroma-game/prototype")
if len(sys.argv) > 1:
    sys.argv[1] = os.path.abspath(sys.argv[1])
sys.path.insert(0, GAMEDIR)
os.chdir(GAMEDIR)
V224_ENGINE = dict(fair_read=True, sph_eyes=True, sph_odd=True, lead_ways=True, sacred=True, seen_done=True, role_practice=True,
                   read_skill=0.5, lens_want=0.5, app_vigil=True, green_jobs=True, acc_redraw=True, sh_will=0.5)
if os.environ.get("V224") == "1":
    gs = json.loads(os.environ.get("CHROMA_GAME") or "{}") if os.environ.get("CHROMA_GAME") not in (None, "", "off") else {}
    gs.update(own_ix=True, trust_judge=True)
    os.environ["CHROMA_GAME"] = json.dumps(gs)
    es = json.loads(os.environ.get("CHROMA_ENGINE") or "{}")
    es = {**{k: v for k, v in V224_ENGINE.items() if k != "sh_will"}, **es}   # sh_will is not in main's pin
    os.environ["CHROMA_ENGINE"] = json.dumps(es)
import numpy as np

CI = {x: i for i, x in enumerate("WUBRG")}
HINT_D = {"much worse": -0.3, "worse": -0.15, "about right": 0.0, "better": 0.15, "much better": 0.3, "": 0.0}
RNAMES = ["money", "time", "health", "ties", "freedom"]

# the reader's weights (what a thoughtful player would value, from what the screen shows)
W_LIFT = 12.0      # a need they lack: gain is ~.01-.05; x12 so a big lift (~.04) is worth about half a title
W_TITLE = 1.0      # a title or perk gained (more when rare)
W_RARE = 1.5       # extra for a title or perk under 1 life in 10
W_LOSE = 1.0       # a title or perk lost
W_RES = 0.6        # each resource step (+money, -time ...)
W_COMMIT = 1.2     # starting a commitment (partner, career, children, community, faith)
W_REL = 1.2        # reluctance (stress, pent-up wanting, less of "their own")
W_COL = 0.5        # an act whose ends are in the colours that feed a lacking need
W_GOAL = 1.5       # READ_GOALS=1: a step toward a plan (x1), passion (x.7) or dream (x.5) they hold, by its strength and fit
READ_GOALS = os.environ.get("READ_GOALS") == "1"
MARGIN = float(os.environ.get("MARGIN", "0.1"))


def rarity():
    try:
        from rarity import RARITY
        return RARITY
    except Exception:
        return {}


RAR = rarity()


def role_share(name):
    return (RAR.get("role") or {}).get(name)


TIERS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiers.json")))
W_PACK, W_SUMMIT = 3.0, 6.0   # the climber: a pack career's rung, a summit (the screen names the title; players know a professor)


def ev(o, g, oracle=False, loc=None, cp=None, climb=False):
    """What a pick is worth to the reader (or the oracle)."""
    if o["colors"] == "-":
        return 0.0, 0.0
    if oracle:
        p = float(o["true"])
    else:
        p = float(np.clip(o["felt"] + HINT_D.get(o.get("hint", ""), 0.0), 0.02, 0.98))
    f = o.get("follows") or {}
    lift = sum(x["gain"] for x in (f.get("lift") or []))
    if oracle and loc is not None and "need" in loc:     # every need's real refill, weighted by how much it matters now
        import engine as E
        e = np.maximum(loc["e"][0, o["idx"]], 0); nv = E.NMAP @ e
        need = loc["need"][0]; st = max(float(loc["L"]["STAKES"][int(loc["s"][0])]), 0.9)
        nimp = np.asarray(loc["nimp"][0], float) if "nimp" in loc else np.ones(len(need))
        lift = float((0.12 * st * nv * (1 - need) * nimp / nimp.mean() * (1 + (need < 0.5))).sum())
    ok, bad = 0.0, 0.0
    for d in o.get("roles_fx") or ():
        sh = role_share(d.get("name"))
        v = W_TITLE + (W_RARE if sh is not None and sh < 0.1 else 0.0)
        if climb:
            v = W_TITLE + {1: W_PACK, 2: W_SUMMIT}.get(TIERS.get(d.get("name"), 0), 0.0)
        if d["when"] == "ok":
            ok += v if d["gain"] else -W_LOSE
        else:
            bad += v if d["gain"] else -W_LOSE
    res = lambda xs: sum((1 if x[0] == "+" else -1) for x in xs)
    ok += W_RES * res(f.get("win") or []) + W_LIFT * lift + W_COMMIT * float(f.get("commit_p", 0.0)) / max(o["felt"], 0.05)
    bad += W_RES * res(f.get("lose") or [])
    cost = W_RES * res(f.get("cost") or [])
    # reading the colours: a need they lack (the panel's needs bar) is fed by acts whose ends are in its colours
    # (belonging by Red and Green, meaning by Blue, Black and White, safety by White), so a reader leans there
    if loc is not None and "need" in loc:
        import engine as E
        ends = o["colors"].split(">")[-1].replace("+", "")
        T = np.array([1.0 if c in ends else 0.0 for c in "WUBRG"]); T = T / T.sum() if T.sum() else np.full(5, 0.2)
        lack = np.maximum(0, 0.5 - np.asarray(loc["need"][0], float)) / 0.5
        ok += W_COL * float(lack @ (E.NMAP @ T)) * 5
    if READ_GOALS and loc is not None and "rel" in loc and np.ndim(loc["rel"]) == 3:   # the goals panel, read against the option
        gk_ = np.asarray(loc["gk"][0]); r_ = np.asarray(loc["rel"][0][:, o["idx"]], float) * (gk_ >= 0)
        kw_ = np.select([gk_ == 2, gk_ == 1, gk_ == 0], [1.0, 0.7, 0.5], 0.0)
        if len(r_):
            ok += W_GOAL * float((r_ * np.asarray(loc["gs"][0], float) * kw_).max())
    rel = float(o.get("rel", 0.0)) if o["idx"] != cp["own"] else 0.0
    if o.get("status") == "out of reach":
        bad -= 0.5
    return p * ok + (1 - p) * bad + cost - W_REL * rel, p


def choose(policy, g, cp, prng):
    loc = g.loc
    m = np.maximum(np.asarray(loc["m"][0], float), 0)
    opts = [o for o in cp["options"] if o["colors"] != "-" and m[o["idx"]].sum() > 0 and o.get("status") != "out of reach"]
    own = int(cp["own"])
    if policy == "let" or not opts:
        return None, {}
    if policy in ("free", "okay"):                   # a random push among the options they would not mind
        lim = 0.02 if policy == "free" else 0.3
        ok_ = [o for o in opts if o["idx"] != own and float(o.get("rel", 1)) < lim]
        return (ok_[int(prng.integers(len(ok_)))]["idx"], {}) if ok_ else (None, {})
    if policy.startswith("random"):
        return opts[int(prng.integers(len(opts)))]["idx"], {}
    if policy.startswith("steer:"):
        ci = CI[policy[6:]]
        cv = lambda k: m[k] / m[k].sum() if m[k].sum() > 0 else np.full(5, 0.2)
        return max(opts, key=lambda o: (cv(o["idx"])[ci], o["idx"] == own))["idx"], {}
    if policy in ("heart", "head"):                  # the screen's heart or head mark, when it is not their own pick
        k = (cp.get("view") or {}).get(policy, -1)
        if k is not None and k >= 0 and k != own and k in cp["by_idx"] and cp["by_idx"][k].get("status") != "out of reach":
            return k, {}
        return None, {}
    if policy == "anti":                             # a careless voice: the pick the reader likes least, when it is clearly worse
        cand = [o for o in cp["options"] if o.get("status") != "out of reach" and o["colors"] != "-"]
        vals = {o["idx"]: ev(o, g, False, loc, cp) for o in cand}
        if not vals:
            return None, {}
        own_v = vals.get(own, (0.0, 0.0))[0]
        worst = min(vals, key=lambda k: vals[k][0])
        if worst != own and own_v - vals[worst][0] > MARGIN:
            return worst, dict(own_v=round(own_v, 3), best_v=round(vals[worst][0], 3))
        return None, {}
    if policy in ("reader", "oracle", "wise", "climb", "wiseh"):
        orc = policy == "oracle"
        cand = [o for o in cp["options"] if o.get("status") != "out of reach" or o["idx"] == own]
        vals = {o["idx"]: ev(o, g, orc, loc, cp, climb=policy == "climb") for o in cand}
        if policy in ("wise", "climb", "wiseh"):                # also: what their heart (wise) or head (wiseh, climb) wants, and
            hk = (cp.get("view") or {}).get("heart" if policy == "wise" else "head", -1)   # no long shots that would fail
            vals = {k: (v + (0.3 if k == hk else 0.0) - (0.6 * max(0.0, 0.5 - p) if cp["by_idx"][k]["colors"] != "-" else 0.0), p)
                    for k, (v, p) in vals.items()}
        own_v = vals.get(own, (0.0, 0.0))[0]
        best = max(vals, key=lambda k: vals[k][0])
        info = dict(own_v=round(own_v, 3), best_v=round(vals[best][0], 3), n=len(vals))
        if best != own and vals[best][0] - own_v > MARGIN:
            return best, info
        return None, info
    raise ValueError(policy)


def play(seed, policy, freq="normal"):
    random.seed(seed)
    from console import Console
    import game as G
    VARS = {"quiet": dict(quiet_k=1.0), "piv": dict(piv_own=0.0, piv_steady=0.0), "off": dict(G.GAME_OFF),
            "nocost": dict(stress=0.0, backlash=0.0, effort=0.0, out_of_reach=0.0, backfire_stress=0.0, backfire_money=0.0),
            "nopiv": dict(piv=0.0, lean=0.0, backfire=0.0, plan_lean=0.0)}
    full = policy
    if "~" in policy:                          # a variant of the game's rules for this life: <policy>~<variant>
        policy, var = policy.split("~", 1)
        G.GAME.update(VARS[var])
    if policy == "none":
        G.GAME["quiet_k"] = 1.0
    c = Console()
    c.handle(""); c.handle(os.environ.get("PRESET", "1")); c.handle("Ari")   # PRESET: Release's copy (chroma-release/picks)
    g = c.g
    g.freq = freq
    yrs = []
    _orig_yearly = g._yearly

    def _yearly(t, loc):                       # the inner state once a year: needs, strain, pent-up wanting, want-self gap
        try:
            import engine as E
            w_ = E.softmax(loc["z"][0]); a_ = E.softmax(loc["y"][0])
            yrs.append(dict(age=round(t / 52, 1), need=[round(float(x), 3) for x in loc["need"][0]],
                            stress=round(float(loc["stress"][0]), 3), Q=round(float(loc["Q"][0]), 3),
                            gap=round(float(0.5 * np.abs(a_ - w_).sum()), 3), content=round(float(loc["content"][0]), 3),
                            peace=round(float(loc["peace"][0]), 3), held=[int(x) for x in np.asarray(loc["held"][0])],
                            res=[round(float(x), 3) for x in loc["res"][0]], w=[round(float(x), 3) for x in w_],
                            **{k: round(float(np.asarray(loc[k])[0]), 3) for k in ("mood", "regret", "wound", "trouble", "base_mood", "dsc", "ctrl")
                               if k in loc and np.ndim(loc[k]) == 1}))
        except Exception:
            pass
        return _orig_yearly(t, loc)
    g._yearly = _yearly
    goals_ev = []
    _orig_say = g._say

    def _say(line, level=0, tag="note", **meta):     # dreams, passions and plans begun, reached, let go
        if tag == "goal":
            goals_ev.append((round(g.t / 52, 1), meta.get("kind"), meta.get("what")))
        return _orig_say(line, level, tag, **meta)
    g._say = _say
    prng = np.random.default_rng(seed + 31 + 1000 * (int(policy.split(":")[1]) if policy.startswith("random:") else 0))
    asked = []
    t0 = time.time()
    yr = []
    last_y = -1
    while True:
        if policy == "none":
            r = g.advance(until_checkpoint=False)
        else:
            r = g.advance()
        if r == "resolved" and asked and g.resolution:
            res = g.resolution
            asked[-1].update(ok=bool(res.get("worked")), pivot=(res.get("pivot") or {}).get("kind"),
                             hind=(res.get("hindsight") or {}).get("kind"))
        if r in ("over",) or g.over:
            break
        if r != "checkpoint":
            continue
        cp = g.pending
        if cp.get("turning"):
            g.decide(None); asked.append(dict(age=round(cp["age"], 2), turning=True)); continue
        if policy.startswith("light:"):                # P3: a light steer toward a colour at every moment
            g.decide(None, light=policy[6:]); f_ = g._force or {}
            asked.append(dict(age=round(cp["age"], 2), sit=cp["sit"], pushed=bool(f_), rel=round(float(f_.get("rel", 0)), 3)))
            continue
        pick, info = choose(policy, g, cp, prng)
        own = int(cp["own"])
        pushed = pick is not None and pick != own
        loc = g.loc
        o = cp["by_idx"].get(pick if pushed else own, {})
        asked.append(dict(age=round(cp["age"], 2), sit=cp["sit"], pushed=pushed, rel=round(float(o.get("rel", 0)) if pushed else 0.0, 3),
                          felt=round(float(o.get("felt", 0)), 3), true=round(float(o.get("true", 0)), 3), stakes=round(cp["stakes"], 2),
                          life=bool("had_ev" in loc and bool(loc["had_ev"][0])), **info))
        g.decide(pick)
    h = g.history
    rv = getattr(g, "review", None) or {}
    bk = g.book() or {}
    titles = bk.get("titles", [])
    shares = [(t, role_share(t)) for t in titles]
    sit_sh = (RAR.get("sit") or {})
    moms = [m_[2:] for m_ in bk.get("moments", []) if m_.startswith("s|")]
    o = g.result or {}
    out = dict(seed=seed, policy=full, freq=freq, age=round(g.age(), 2), died=getattr(g, "died", None), secs=round(time.time() - t0),
               n_cp=len(asked), n_push=sum(1 for a in asked if a.get("pushed")),
               ok_push=sum(1 for a in asked if a.get("pushed") and a.get("ok")),
               ok_own=sum(1 for a in asked if not a.get("pushed") and a.get("ok")),
               n_own=sum(1 for a in asked if not a.get("pushed") and not a.get("turning")),
               backfire=sum(1 for a in asked if a.get("pivot") == "backfire"),
               accepted=h.get("accepted", 0), resented=h.get("resented", 0),
               ful=rv.get("fulfilment"), ser=rv.get("serenity"), integ=rv.get("integrity"), gifts=rv.get("gifts"),
               reading=(rv.get("reading") or {}).get("words"), bands=(rv.get("reading") or {}).get("bands"),
               well=(rv.get("reading") or {}).get("well"), own=(rv.get("reading") or {}).get("own"),
               content=[(round(a, 1), round(float(c_), 3)) for a, c_ in h["content"]],
               peace=[(round(a, 1), round(float(p_), 3)) for a, p_ in h["peace"]],
               titles=shares, n_titles=len(titles), rare_titles=sum(1 for _, s in shares if s is not None and s < 0.1),
               vrare_titles=sum(1 for _, s in shares if s is not None and s < 0.03),
               deeds=bk.get("deeds", []), rare_moments=sum(1 for m_ in moms if (sit_sh.get(m_) or 1) < 0.1),
               n_moments=len(moms), final=rv.get("final_label"), asked=asked,
               long=bk.get("long", []), yrs=yrs, goals=goals_ev)
    return out


def main():
    out_dir, policy = sys.argv[1], sys.argv[2]
    seeds = [int(x) for x in sys.argv[3:]]
    freq = os.environ.get("FREQ", "normal")
    os.makedirs(out_dir, exist_ok=True)
    for s in seeds:
        f = os.path.join(out_dir, f"{policy.replace(':', '').replace('~', '-')}_{freq}_{s}.json")
        if os.path.exists(f):
            continue
        r = play(s, policy, freq)
        json.dump(r, open(f + ".tmp", "w")); os.replace(f + ".tmp", f)
        print(policy, s, r["secs"], "s", r["n_cp"], "moments", r["n_push"], "pushed", "ful", round(r["ful"] or 0, 3),
              "ser", round(r["ser"] or 0, 3), "rare titles", r["rare_titles"], flush=True)


if __name__ == "__main__":
    main()
