"""v7 foreseen outcome of a plan, for the game.

Emren (2026-10-04 21:39, 2026-10-05 04:57): the player can decide long plans and the game shows the foreseen odds; it
shows the character's felt odds, and reality only as a rough hint.

All functions work on S, the dict of run_steps' locals at a pause (chroma-game link.py yields it), and n, the person.

    from foresee import preview, add_plan, foresee, drop_plan, plans
    preview(S, n, "five years", domain="career")      # what the character feels before deciding (changes nothing)
    j, f = add_plan(S, n, "year", mix="U R")          # the player's plan: a pursuit in these ways, or a domain
    foresee(S, n, j)                                  # felt odds now, and a rough hint of how such plans go
    drop_plan(S, n, j)                                # the player lets it go (costs what was put in)

The hint is not the engine's true chance for this one life (no one can know it): it is how plans like this one, held
with these felt odds by people with this much self-control, free time and stress and this fit with who they are, turned
out in simulated lives (HINT, measured by calib_v7/foresee_table.py), told as a band of words.
"""
import numpy as np

import engine as E

BANDS = [(0.15, "rarely"), (0.35, "now and then"), (0.6, "about half the time"), (0.8, "more often than not"), (1.01, "usually")]

# logistic model of "reached in time" per horizon: intercept, logit(felt), self-control, free time, stress, fit, domain plan.
# Measured on simulated lives (calib_v7/foresee_table.py); refresh when the goal defaults change.
# Measured 2026-10-07 on 400 Earth lives with the world on (as the game plays), release engine and batch
# (calib_v10/cx2/foresee_on.out); Brier of the hint under the felt odds' in each horizon: year .077 vs .237,
# five years .129 vs .236, life .023 vs .078.
HINT = {
    'week': [0.0, 1.0, 0, 0, 0, 0, 0],
    'year': [-14.017, 1.636, 12.112, 5.467, 0.211, 2.863, 0.0],
    'five years': [-5.431, 0.61, 4.277, 1.793, 0.116, 1.302, 0.44],
    'life': [0.324, 2.349, 6.035, 4.051, 0.113, -3.327, 0.0],
}


def band(p):
    for hi, word in BANDS:
        if p < hi:
            return word
    return BANDS[-1][1]


def _logit(p):
    p = np.clip(p, 0.01, 0.99)
    return float(np.log(p / (1 - p)))


def hint(horizon, felt, self_control, free_time, stress, fit, domain):
    """How plans like this turned out in simulated lives: a rate, and its band in words."""
    b = HINT[horizon]
    x = [1.0, _logit(felt), self_control, free_time, stress, fit, float(domain)]
    p = 1 / (1 + np.exp(-float(np.dot(b, x))))
    return p, band(p)


def _mix(S, n, mix):
    if mix is None:
        m = np.asarray(S["w"][n], float).copy()
    elif isinstance(mix, str):
        m = E.parse(mix)
    else:
        m = np.asarray(mix, float)
    return m / max(m.sum(), 1e-9)


def _fit(S, n, mix):
    """Self-concordance (Sheldon & Elliot 1999): how well a plan's ways fit who the person is and wants to be."""
    og = 0.5 * (S["w"][n] + E.softmax(S["y"][n]))
    return float(np.clip(2 * (mix * og).sum() / og.max() - 1, -0.5, 1))


def _context(S, n):
    return float(S["ctrl"][n]), float(S["res"][n, E.RIDX["time"]]), float(S["stress"][n])


def _horizon(h):
    return E.HORIZONS.index(h) if isinstance(h, str) else int(h)


def _domain(d):
    if d is None or d == "a pursuit":
        return -1
    return E.KNAMES.index(d) if isinstance(d, str) else int(d)


def _what(S, n, felt, hz, dom, mix, weeks):
    ct, ft, st = _context(S, n)
    fit = _fit(S, n, mix)
    p, word = hint(E.HORIZONS[hz], felt, ct, ft, st, fit, dom >= 0)
    t = S["t"]
    return dict(felt=round(felt, 2), hint=word, hint_rate=round(float(p), 2), horizon=E.HORIZONS[hz],
                domain=E.KNAMES[dom] if dom >= 0 else "a pursuit", colors=dict(zip(E.COLORS, mix.round(2).tolist())),
                fit=round(fit, 2), due_age=round((t + weeks) / 52, 1),
                left_out=[nm for nm, bad in (("busy weeks", ft < 0.35), ("stress", st > 0.6), ("little self-control", ct < 0.4),
                                             ("a poor fit with who they are", fit < 0.1)) if bad])


def preview(S, n, horizon="year", domain=None, mix=None, strength=0.6):
    """What the character would feel about a plan before it is made (changes nothing)."""
    hz, dom, m = _horizon(horizon), _domain(domain), _mix(S, n, mix)
    _, _, weeks, felt = S["plan_odds"](n, m, dom, hz, strength)
    return _what(S, n, felt, hz, dom, m, weeks)


def add_plan(S, n, horizon="year", domain=None, mix=None, strength=0.6):
    """The player's plan. The character holds it (it does not fade from a poor fit, and they do not let it go on their
    own); it pulls on what they do as their own plans do. When their plans are full, their weakest own plan is pushed
    aside. Returns (slot, foresee) or (-1, reason)."""
    hz, dom, m = _horizon(horizon), _domain(domain), _mix(S, n, mix)
    gk, gs, gby = S["gk"], S["gs"], S["gby"]
    if dom >= 0 and S["held"][n, dom]:
        return -1, f"already holds a {E.KNAMES[dom]}"
    mine = np.nonzero(gk[n] == 2)[0]
    if len(mine) >= S["P"]["max_plans"]:
        own = [j for j in mine if not gby[n, j]]
        if not own:
            return -1, "the character already holds as many plans as they can"
        S["end_goal"](n, min(own, key=lambda j: gs[n, j]), "pushed aside")
    j = S["new_goal"](n, 2, m, dom, E.GSRC["player"], hz=hz, by=1, s0=strength)
    if j < 0:
        return -1, "no room for another goal"
    return j, foresee(S, n, j)


def foresee(S, n, j):
    """A plan's felt odds now (they change as the character learns how often chances come and how steps go), its odds
    at the start, progress, and the rough hint of reality."""
    if S["gk"][n, j] != 2:
        return None
    hz, dom = int(S["ghz"][n, j]), int(S["gd"][n, j])
    out = _what(S, n, float(S["gfelt"][n, j]), hz, dom, S["gm"][n, j], int(S["gh"][n, j] - S["t"]))
    out.update(felt_at_start=round(float(S["gfelt0"][n, j]), 2), progress=round(float(S["gp"][n, j]), 2),
               by_player=bool(S["gby"][n, j]), source=E.G_SOURCES[S["gsrc"][n, j]])
    return out


def plans(S, n):
    """Every plan the person holds now, the player's and their own: [(slot, foresee)]."""
    return [(int(j), foresee(S, n, j)) for j in np.nonzero(S["gk"][n] == 2)[0]]


def drop_plan(S, n, j):
    """The player lets a plan go: it costs what was put in, less for a person who has learned to let go."""
    if S["gk"][n, j] != 2:
        return False
    fa = np.clip((S["tries"][n] - S["wins"][n] + S["blocked"][n] - S["P"]["flex_exp"][0]) / S["P"]["flex_exp"][1], 0, 1)
    S["quit_"](n, j, "let go", 0.3 + 0.7 * fa)
    return True
