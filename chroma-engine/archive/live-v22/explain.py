"""v7 explanations for the game: the character's view of a choice before it is made, and what came of it after.

Emren (2026-10-05 08:15, 08:17): before a choice the player sees the character's perceived reality of each option and an
inner-voice hint drawn from the character's own variables ("I feel this one most, this one looks more logical, but I don't
care" is one Red example; every color and mix gets its own voice). After the choice comes a resolution: what happened,
what changed in the character and around them, and a small hint of how the world works.

The engine builds the mechanic and names each case with a key. The Library writes the voice: in the world's file, VOICE
and LESSONS map each key to (color, line) variants, the same shape as a situation's scenes ("" = any color). Until then
the plain defaults below are used.

All functions work on S, the dict of run_steps' locals at a pause (chroma-game link.py yields it), and n, the person.

    import explain as X
    b = X.before(S, n)          # at the "choose" pause: options as the character sees them, heart and head, the voice
    snap = X.snapshot(S, n)     # at the same pause: the state to compare against
    r = X.after(snap, S2, n)    # at the "end" pause of the same week (S2 = that pause's locals): outcome, changes, lesson

Nothing here changes the run. Odds the character cannot know are given only as a band of words ("reality").
"""
import numpy as np

import engine as E
from foresee import band

C = E.C
COLORS = E.COLORS if hasattr(E, "COLORS") else "WUBRG"

# ---------------------------------------------------------------- the voice: keys the Library writes lines for
# Fills: {N} the character, {heart} the option the heart wants, {head} the one the head picks, {heart_why} {head_why}
# (why each wants it, from the drivers below), {goal} a dream, passion or plan, {need} a need, {x} the option in question.
VOICE_DEFAULT = {
    # one primary key per moment
    "agree": [("", "Everything in {N} says the same: \u201c{heart}\u201d.")],
    "heart_over_head": [("", "\u201c{heart}\u201d is what {N} feels most. \u201c{head}\u201d makes more sense, and {N} knows it."),
                        ("R", "I feel \u201c{heart}\u201d most. \u201c{head}\u201d looks more logical, but I don't care.")],   # Emren's example
    "head_over_heart": [("", "\u201c{heart}\u201d pulls at {N}, but \u201c{head}\u201d is the sensible thing.")],
    "torn": [("", "Part of {N} wants \u201c{heart}\u201d, because {heart_why}. Part of {N} wants \u201c{head}\u201d, because {head_why}.")],
    "want_but_doubt": [("", "{N} wants \u201c{x}\u201d, but doubts it can be pulled off.")],
    "dream_calls": [("", "\u201c{x}\u201d would be a step toward {goal}.")],
    "duty": [("", "\u201c{x}\u201d is what is expected of {N}.")],
    "need_first": [("", "{N} needs {need} badly, and \u201c{x}\u201d would help.")],
    "habit": [("", "\u201c{x}\u201d, the way it is always done.")],
    "becoming": [("", "\u201c{x}\u201d is who {N} wants to become.")],
    "time_short": [("", "Time feels short, and \u201c{x}\u201d is what matters now.")],
    "stuck": [("", "{N} cannot see a way through this one.")],
    # asides: what in the character bent this moment (zero or more)
    "stressed": [("", "Under this much strain the heart speaks louder.")],
    "little_control": [("", "{N} rarely overrules a feeling.")],
    "disciplined": [("", "{N} has learned to hold to a decision.")],
    "undisciplined": [("", "{N} has got used to giving in.")],
    "blind_spot": [("", "There are ways through this that {N} does not even think of.")],
    "out_of_reach": [("", "What {N} would really want is not on offer here.")],
    "hopeful": [("", "{N} expects things to work out.")],
    "gloomy": [("", "{N} expects the worst.")],
    "short_horizon": [("", "{N} feels time running short.")],
    "lacks": [("", "To go the way {N} wants, {N} would have to fit this: {what}.")],   # {what}: "is a nurse", "can drive"
}
HEART_WHY = {"motives": "it feels right", "habit": "it is what {N} always does", "needs": "{need} is missing",
             "role": "it is expected", "goals": "{goal} still calls", "horizon": "time is short", "exit": "leaving would cost too much"}
HEAD_WHY = {"values": "it is what {N} believes in", "becoming": "it is who {N} wants to be", "odds": "it is the better bet",
            "needs": "it would fix what is missing", "role": "it is the duty", "goals": "it is a step toward {goal}",
            "horizon": "time is short", "exit": "leaving would cost too much",
            "exit_out": "staying no longer fits who {N} is"}   # exit for staying (what was put in); exit_out for leaving

# what a misread of the odds comes from (logit units, + = the character thinks it better than it is)
MISREAD = {"outlook": ("hope", "gloom"), "belief": ("self-belief", "self-doubt"),
           "world": ("a headwind {N} does not see", "a tailwind {N} does not see"),
           "fit": ("this moment calls for other ways", "this moment suits these ways")}

# ---------------------------------------------------------------- the resolution: words for change, and lessons
COLOR_NAME = {"W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green"}
COLOR_WORD = {"W": "more principled", "U": "more thoughtful", "B": "more driven", "R": "more passionate", "G": "more grounded"}
COLOR_WORD_DOWN = {"W": "less bound by rules", "U": "less guarded", "B": "less self-seeking", "R": "calmer", "G": "less settled"}
CHANNEL_WORD = {"instrumental": "what worked and what did not", "scarcity": "what was missing", "social": "the people around",
                "coherence": "being true to oneself", "upkeep": "keeping up who one is"}
# typical size of one week's change, so that changes of different kinds can be compared (1 = a notable week)
SCALE = dict(color=0.004, want=0.006, need=0.06, res=0.05, stress=0.15, content=0.02, peace=0.02, mood=0.05,
             outlook=0.005, discipline=0.01, skill=0.006, belief=0.01, strength=0.03, horizon=0.01, niche=0.004)
CHANGE_WORD = {"content": ("more content", "less content"), "peace": ("more at peace", "more restless"),
               "stress": ("more strained", "more at ease"), "mood": ("in better spirits", "in lower spirits"),
               "outlook": ("more confident", "less sure of themselves"), "discipline": ("more disciplined", "less disciplined"),
               "horizon": ("more aware of time passing", "less pressed by time"),
               "res:money": ("better off", "worse off"), "res:time": ("freer with time", "shorter of time"),
               "res:health": ("healthier", "worn"), "res:ties": ("closer to people", "more alone"),
               "res:freedom": ("freer", "more tied down"),
               "need:safety": ("safer", "less safe"), "need:belonging": ("more at home with people", "lonelier"),
               "need:autonomy": ("more their own person", "less their own person"),
               "need:competence": ("more capable", "less capable"), "need:meaning": ("more purposeful", "emptier")}

LESSONS_DEFAULT = {
    "practice": [("", "Acting in {c} ways makes {N} better at them.")],
    "hard_win": [("", "Doing a hard thing on purpose builds self-control.")],
    "self_control_up": [("", "Holding to it builds self-control, even when it does not work out.")],
    "self_control_down": [("", "Giving in wears self-control down a little.")],
    "surprise_teaches": [("", "Outcomes that surprise teach the most: {N} leans {dir} {c} now.")],
    "fail_own_ways": [("", "A big failure in {N}'s own ways turns them toward what the moment called for.")],
    "defended": [("", "{N} has done this long enough that one failure does not shake the belief.")],
    "habit": [("", "Repeating it makes it pull harder next time.")],
    "door": [("", "It opened a door: the people and places around {N} lean {c} now.")],
    "binding": [("", "A promise like this holds, and costs some freedom.")],
    "backfire": [("", "Going against the {kind} has a price when it fails.")],
    "need_met": [("", "Meeting a need that was lacking ({need}) lifts satisfaction most.")],
    "duty_kept": [("", "Living up to the {kind} deepens it.")],
    "commit_start": [("", "A {kind} brings its own ways: it will pull {N} toward {c}.")],
    "commit_end": [("", "Ending a {kind} costs what was put into it, and frees what it held.")],
    "goal_step": [("", "Each step that works feeds {goal}.")],
    "goal_setback": [("", "A setback weakens {goal}, more so when {N} doubts.")],
    "sealed": [("", "Tries that worked and felt like {N}'s own have made {goal} a passion.")],
    "goal_end": [("", "{goal}: {what}.")],
    "loss": [("", "Losing someone close makes time feel shorter.")],
    "stress_up": [("", "Stress makes the heart louder next time, and the head quieter.")],
    "regret": [("", "{N} chose with the heart against the head, and it went wrong. That stays with a person.")],
    "rite": [("", "A moment like this marks a passage: {N} is now {stage}.")],
    "rite_quiet": [("", "No one marked it, but {N} is {stage} now.")],
    "turning_point": [("", "Doubts that pile up eventually turn a person: {N} is turning away from {c}.")],
    "breakthrough": [("", "A want held back for long enough breaks through.")],
    "closer_to": [("", "{N} is closer to becoming {guild}.")],
    "drifting_from": [("", "{N} is letting go of being {lost}; what stays is {guild}.")],   # a color falling away
    # titles and perks
    "title_gain": [("", "{N} is {what} now: it brings its own ways and expectations.")],
    "title_loss": [("", "{N} is no longer {what}, and the place it gave goes with it.")],
    "status_gain": [("", "Others see {N} differently now: {what}.")],
    "perk_gain": [("", "{N} {what} now, and some doors open with it.")],
    "perk_loss": [("", "Without {perk}, some doors close; what {N} learned stays a while.")],
    "perk_helped": [("", "It helped that {N} {what}.")],
}


def _pick(table, default, key, color, rng=None):
    """A line for a key: the character's color lines and the any-color lines together, one drawn at random (rng);
    other colors' lines only when neither exists."""
    rows = (table or {}).get(key) or default.get(key) or []
    pool = [ln for c, ln in rows if (c and color in c) or not c] or [ln for c, ln in rows]
    if not pool:
        return ""
    return pool[0] if rng is None else pool[int(rng.integers(len(pool)))]


# point 7: how far a way's colors lean against the character's own (its colors' enemies in the world's framing, minus its
# share in their own colors) above which it is "against", "reluctant"; and how far below doing nothing (in units of the
# moment's randomness) a way may fall before the character would rather do nothing (measured: calib_v7/accept_check.py)
ACCEPT = (0.25, 0.13, -2.5)


def _rng(S, n, salt):
    """A draw that differs from week to week and person to person, and repeats for the same week (tests, replays)."""
    return np.random.default_rng([int(S["t"]), int(n), int(S["s"][n]), salt])


def _fill(line, **kw):
    out = line
    for _ in range(2):   # fills can carry fills ({heart_why} holds {need})
        for k_, v_ in kw.items():
            out = out.replace("{" + k_ + "}", str(v_))
    return out


def colors_of(v, lo=0.2):
    """'R G' for a mix whose shares stand out (above an even share), strongest first."""
    v = np.maximum(np.asarray(v, float), 0)
    if v.sum() <= 0:
        return ""
    v = v / v.sum()
    order = np.argsort(-v)
    return " ".join(COLORS[i] for i in order if v[i] > lo + 1e-9) or COLORS[int(order[0])]


def names(colors):
    """'R G' -> 'Red and Green'."""
    nm = [COLOR_NAME[c] for c in colors.split() if c in COLOR_NAME]
    return " and ".join([", ".join(nm[:-1]), nm[-1]] if len(nm) > 1 else nm)


def _sig(x):
    return 1 / (1 + np.exp(-x))


def _arr(x, N):
    return np.broadcast_to(np.asarray(x, float), (N,) + np.shape(x)[1:] if np.ndim(x) else (N,))


COLOR_ADJ = {"W": "principled", "U": "thoughtful", "B": "driven", "R": "passionate", "G": "grounded"}
COLOR_NOUN = {"W": "doing right", "U": "understanding", "B": "getting ahead", "R": "freedom", "G": "belonging"}
KIND_NOUN = {"career": "job", "partner": "relationship", "children": "family", "community": "community", "faith": "faith"}
KIND_REF = {"career": "their work", "partner": "their relationship", "children": "family life", "community": "the community",
            "faith": "their faith"}
KIND_GOAL = {"career": "a working life", "partner": "a life together", "children": "a family", "community": "a place among others",
             "faith": "a faith to live by"}
GOAL_LEAD = {"dream": "the dream of", "passion": "the passion for", "plan": "the plan for"}


def predicate(say):
    """A perk's say as something the character does or is: 'can swim' stays, 'a landlord' becomes 'is a landlord'."""
    return ("is " + say) if say.split(" ", 1)[0] in ("a", "an", "the", "in", "on", "known", "good", "from", "someone") else say


def _and(words):
    return " and ".join([", ".join(words[:-1]), words[-1]] if len(words) > 1 else words)


def plain_identity(colors):
    """'W U' -> 'principled and thoughtful' (the {guild} fill; the Magic name stays in {guild_name})."""
    return _and([COLOR_ADJ[c] for c in colors.replace(" ", "") if c in COLOR_ADJ]) or "no one in particular"


def plain_goal(kind, domain=-1, mix=None):
    lead = GOAL_LEAD.get(kind, "the " + kind + " of")
    if domain is not None and domain >= 0:
        return f"{lead} {KIND_GOAL[E.KNAMES[domain]]}"
    cs = colors_of(mix).split() if mix is not None else []
    return f"{lead} {_and([COLOR_NOUN[c] for c in cs[:2]])}" if cs else f"{lead} something of one's own"


def goal_name(S, n, j):
    """The goal's own words: the Library's concrete dream (chroma-library/dreams.py) when the engine named it, its passion,
    plan or life phrase as it grows; otherwise the plain name from its kind, domain and colors."""
    if "gname" in S and S["gname"][n, j] >= 0 and "dream_phrase" in S:
        return S["dream_phrase"](n, j)
    gk, gd, gm = S["gk"][n, j], S["gd"][n, j], S["gm"][n, j]
    return plain_goal(E.G_KINDS[gk], int(gd), gm)


# ---------------------------------------------------------------- before
def _parts(S, n):
    """The pull of each option, split into its named sources. Head (reflective) and heart (impulsive) parts, N x K each."""
    P = S["P"]; K = S["U_R"].shape[1]
    st = float(S["stress"][n])
    zero = np.zeros(K)

    def row(x):
        x = np.asarray(x, float)
        return x[n] if x.ndim == 2 else (zero + x if x.ndim == 0 else zero)

    head = dict(values=P["beta_V"] * S["VA"][n], becoming=P["beta_A"] * float(np.asarray(S["tryf"])[n]) * S["step"][n],
                odds=P["beta_P"] * (S["p_hat"][n] - 0.5) * float(S["stakes"][n]), needs=P["beta_N"] * S["relief"][n],
                role=P["beta_role"] * S["role"][n], goals=row(S["gU_R"]),
                horizon=row(S["hzU"]) if P.get("hz_k") and "hzU" in S else zero)
    heart = dict(motives=P["beta_V"] * S["V"][n], habit=P["beta_H"] * (1 + st) * S["H"][n], needs=P["beta_N"] * S["relief"][n],
                 role=P["beta_role"] * S["role"][n], goals=row(S["gU_I"]),
                 horizon=row(S["hzU"]) if P.get("hz_k") and "hzU" in S else zero)
    # what is left (walking away from a commitment: sunk cost and wanting out) goes under "exit"
    head["exit"] = S["U_R"][n] - sum(head.values())
    heart["exit"] = S["U_I"][n] - sum(heart.values())
    return head, heart


def _top(parts, k, among, n_=2):
    """The drivers that set option k apart from the others considered: (name, value above their mean)."""
    rel = {nm: round(float(v[k] - v[among].mean()), 3) for nm, v in parts.items()}
    rel = {nm: v for nm, v in rel.items() if abs(v) > 0.02}
    return sorted(rel.items(), key=lambda kv: -abs(kv[1]))[:n_]


def before(S, n, voice=None, rng=None):
    """The character's view of this week's choice, for person n at the "choose" pause.

    Returns a dict:
      situation, age, options: list of per-option dicts (index k, label, ways, ends, kind, felt, reality, heart, head,
        drivers), heart (index the heart wants most), head (index the head picks), lean (what the character would most
        likely do alone) and lean_p, self_control (0..1: how much the head decides), insight (key, line, fills), asides
        (list of key, line), voice_color.
    kind: "seen" (the character thinks of it), "unnoticed" (open, but not thought of), "out of reach" (not open to them:
        "the world" or "means"), "do nothing". closed: the Library's closed kind (law, approval, means) or None.
    felt: the character's felt chance it works. reality: a band of words and which way the character misreads it, with
        the main reason; true: the engine's chance (for tests and the game's hidden layer; Emren: show only the band).
    heart / head: the share each option would get if the heart (impulse) or the head (reflection) chose alone.
    """
    P = S["P"]; L = S["L"]; s = int(S["s"][n]); N = len(S["s"])
    K = S["U_R"].shape[1]
    rng = rng if rng is not None else _rng(S, n, 1)
    mask, seen, open_ = S["mask"][n], S["seen"][n], S["open_"][n]
    idle = S["do_nothing"][n]
    m, e, diff, alpha = S["m"][n], S["e"][n], S["diff"][n], S["alpha"][n]
    ctrl = float(S["ctrl"][n]); tau = float(P["tau0"] * (1 + 0.5 * S["stress"][n]))
    w = np.asarray(S["w"][n]); name = E.KNAMES
    head_p, heart_p = _parts(S, n)
    cons = np.nonzero(seen & ~idle)[0]                 # what the character actually weighs
    among = cons if len(cons) else np.nonzero(mask & ~idle)[0]
    U_R, U_I = S["U_R"][n], S["U_I"][n]

    def share(U):
        x = np.where(seen & ~idle, U / tau, -np.inf)
        if not np.isfinite(x).any():
            return np.zeros(K)
        x = np.exp(x - x[np.isfinite(x)].max()); return x / x.sum()
    sh_R, sh_I = share(U_R), share(U_I)
    pr = np.asarray(S["pr"][n])
    # true odds per option, as the engine will draw them (the same formula as p_true, for every option)
    sig, f_tot, fb = S["sig"][n], S["f_tot"][n], S["fb"][n]
    gain = P["gain"]
    fit_k = P["fit"] * (m * (alpha - alpha.mean())).sum(1)
    pb = np.asarray(S["pbump"][n]) if np.ndim(S.get("pbump", 0.0)) == 2 else np.zeros(K)   # titles and perks: better odds
    z_ = gain * ((m * (sig + f_tot)).sum(1) + fit_k - diff) + pb
    if np.ndim(S.get("earn", 0.0)) == 2 and "earned" in S:   # earned odds (preparation and timing for a title)
        z_ = S["earned"](z_, np.asarray(S["earn"][n]))
    p_true = _sig(z_)
    if np.ndim(S.get("lackf", 1.0)) == 2:                    # lacking: what the act requires, a share of the chance
        p_true = p_true * np.asarray(S["lackf"][n])
    TON = 1.0 if P["temperament"] else 0.0
    o_term = TON * P["o_bias"] * (float(S["outlook"][n]) - P["o_ref"])
    closed = np.asarray(S["closed_s"][n]) if S.get("closed_s") is not None else L["CLOSED"][s] if "CLOSED" in L else np.full(K, -1)
    GR = L.get("ROLES") if S.get("RON") else None
    need_k = np.full(K, -1)
    if GR is not None:                                 # what each option needs that the character lacks, and what helps it
        rq = GR["A_REQ"][s]; hs = np.asarray(S["r_has"][n])
        need_k = np.where((rq >= 0) & ~hs[np.maximum(rq, 0)], rq, -1)
        NT = GR["NT"]; lev = np.where(hs[NT:], 1.0, np.asarray(S["p_lev"][n]))
        helps = (lev * 4 * GR["odds"])[:, None] * GR["ind"][NT:]      # perks x colors, logit units
    need_a = np.full(K, -1)
    if S.get("AQ_ON"):                                 # v7 adjectives an option needs that the character is not (wealthy, fit)
        aq = L["ADJ_REQ"][s]; ah = np.asarray(S["adj"][n])
        need_a = np.where((aq >= 0) & ~ah[np.maximum(aq, 0)], aq, -1)
    CLOSED_KINDS = ("law", "approval", "means")
    opts = []
    for k in np.nonzero(mask)[0]:
        if idle[k]:
            kind = "do nothing"
        elif seen[k]:
            kind = "seen"
        elif open_[k]:
            kind = "unnoticed"
        else:
            kind = "out of reach"
        o = dict(k=int(k), label=L["labels"][s][k], ways=colors_of(m[k]), ends=colors_of(e[k]), kind=kind,
                 closed=CLOSED_KINDS[closed[k]] if closed[k] >= 0 else None)
        if kind == "out of reach":
            o["why"] = "means" if not S["open_r"][n, k] else "the world"
        if need_k[k] >= 0:
            o["needs"] = GR["names"][need_k[k]]
        elif need_a[k] >= 0:
            o["needs"] = E.ADJ_NAMES[need_a[k]]
        if GR is not None and not idle[k]:
            hc = helps @ m[k]
            o["helped_by"] = [GR["names"][NT + j] for j in np.argsort(-hc)[:2] if hc[j] > 0.05]
        if not idle[k]:
            unread = 1.0 - float(np.asarray(S["read_"])[n]) if "read_" in S else 1.0   # what the character does not sense
            causes = dict(outlook=o_term, belief=gain * float((m[k] * fb).sum()), world=-gain * unread * float((m[k] * f_tot).sum()),
                          fit=-gain * unread * float(fit_k[k]))
            gap = float(S["p_hat"][n, k] - p_true[k])
            way = "hopeful" if gap > 0.12 else "doubtful" if gap < -0.12 else "fair"
            main = max(causes, key=lambda c_: abs(causes[c_]) if np.sign(causes[c_]) == np.sign(gap) else 0)
            why = MISREAD[main][0 if causes[main] > 0 else 1] if way != "fair" else ""
            o.update(felt=round(float(S["p_hat"][n, k]), 3), felt_words=band(float(S["p_hat"][n, k])),
                     reality=dict(band=band(float(p_true[k])), misread=way, why=why),
                     true=round(float(p_true[k]), 3),
                     base=(None if "CHANCE" not in L or np.isnan(L["CHANCE"][s][k]) else round(float(L["CHANCE"][s][k]), 2)),
                     heart=round(float(sh_I[k]), 3), head=round(float(sh_R[k]), 3), chance_chosen=round(float(pr[k]), 3),
                     drivers=dict(heart=_top(heart_p, k, among), head=_top(head_p, k, among)))
        opts.append(o)
    # the moment as a whole
    heart_k = int(cons[np.argmax(U_I[cons])]) if len(cons) else -1
    head_k = int(cons[np.argmax(U_R[cons])]) if len(cons) else -1
    lean_k = int(np.argmax(pr))
    # how the character feels about each way (Emren 09:25, point 7). "would go with it": what they lean to, or close to it.
    # "okay with it": anything else they are not against; a way in colors other than theirs is still fine. "reluctant": its
    # colors lean against theirs (the colors their own colors are opposed to in this world), or they would rather do nothing.
    # "against": it belongs clearly to the colors opposed to who they are and who they want to be. reluctance (0 to 1) is
    # what forcing it costs; clash is how far its colors lean against theirs (an even person: 0)
    U_mix = ctrl * U_R + (1 - ctrl) * U_I
    cand_ = cons if len(cons) else np.nonzero(mask & ~idle)[0]
    Ub = float(U_mix[cand_].max()) if len(cand_) else 0.0
    idle_k = np.nonzero(mask & idle)[0]
    U0 = float(U_mix[idle_k[0]]) if len(idle_k) else None
    wh, ah = np.asarray(S["w_hat"][n]), np.asarray(S["a_hat"][n])
    FR_ = E.FRAMINGS[P["framing"]] if isinstance(P["framing"], str) else np.asarray(P["framing"], float)
    EN_ = (np.asarray(FR_) > 0).astype(float); EN_ = EN_ / np.maximum(EN_.sum(1, keepdims=True), 1)   # each color's opposed colors
    for o in opts:
        k = o["k"]
        if idle[k]:
            continue
        en = e[k] / e[k].sum() if e[k].sum() > 1e-9 else m[k]
        mix_ = 0.5 * m[k] + 0.5 * en                      # how it is done and what it is for
        fit_ = float(max(5 * mix_ @ wh - 1, 5 * mix_ @ ah - 1))
        clash_ = float(min(mix_ @ EN_ @ ref - mix_ @ ref for ref in (wh, ah)))
        rest_ = (U_mix[k] - U0) / tau if U0 is not None else 0.0
        near = len(cand_) and k in cand_ and (U_mix[k] - Ub) / tau > -1.0
        lvl = ("would go with it" if (k == lean_k or near) else "against" if clash_ >= ACCEPT[0]
               else "reluctant" if (clash_ >= ACCEPT[1] or rest_ < ACCEPT[2]) else "okay with it")
        rel_ = 0.0 if lvl in ("would go with it", "okay with it") else float(np.clip(max((clash_ - 0.05) / 0.3, -rest_ / 10), 0.1, 1))
        o["accept"] = dict(level=lvl, fit=round(fit_, 2), clash=round(clash_, 2), reluctance=round(rel_, 2))
    lab = lambda k_: L["labels"][s][k_] if k_ >= 0 else ""
    fills = dict(N="{N}", heart=lab(heart_k), head=lab(head_k), x=lab(head_k), goal="", need="", what="")
    # which goal and need are in play (for the fills)
    if S["P"].get("goals") and "wR" in S and len(cons):
        gj = np.argmax(np.asarray(S["wR"][n]) * np.asarray(S["rel"][n])[:, head_k]) if head_k >= 0 else -1
        if gj >= 0 and S["gk"][n, gj] >= 0 and S["rel"][n][gj, head_k] > 0:
            fills["goal"] = goal_name(S, n, gj)
    lack = np.asarray(S["lack"][n]); serves = np.asarray(S["serves"][n])
    kk_ = head_k if head_k >= 0 else lean_k
    fills["need"] = E.NEEDS[int(np.argmax(lack * serves[kk_]))] if (lack * serves[kk_]).max() > 0 else ""

    def why_of(table, parts, k_):
        top = _top(parts, k_, among, 3)
        top = [nm for nm, v in top if v > 0 and table.get(nm)]
        if top and top[0] == "exit" and float(parts["exit"][k_]) > 0 and table.get("exit_out"):
            top[0] = "exit_out"                            # the option itself carries it: wanting out, not what was put in
        return table[top[0]] if top else table["motives" if "motives" in table else "values"], (top[0] if top else "")
    if len(cons):
        fills["heart_why"], h_drv = why_of({**HEART_WHY, **(L.get("HEART_WHY") or {})}, heart_p, heart_k)
        fills["head_why"], r_drv = why_of({**HEAD_WHY, **(L.get("HEAD_WHY") or {})}, head_p, head_k)
    else:
        h_drv = r_drv = ""
    # the primary key
    if not len(cons):
        key = "stuck"
    elif heart_k == head_k:
        key = {"goals": "dream_calls", "role": "duty", "horizon": "time_short", "needs": "need_first",
               "becoming": "becoming", "habit": "habit"}.get(r_drv if r_drv in ("goals", "role", "horizon", "needs", "becoming") else h_drv, "agree")
        if key == "agree" and S["p_hat"][n, head_k] < 0.35:
            key = "want_but_doubt"
        if key == "dream_calls" and not fills["goal"] or key == "need_first" and not fills["need"]:
            key = "agree"
    else:   # heart and head disagree: whichever the character is clearly more likely to follow wins
        r_ = pr[heart_k] / max(pr[heart_k] + pr[head_k], 1e-12)
        key = "heart_over_head" if r_ > 0.58 else "head_over_heart" if r_ < 0.42 else "torn"
    # asides: what in the character bent this moment (at most two, the most telling first)
    asides = []
    st = float(S["stress"][n]); dsc = float(np.asarray(S.get("dsc", np.ones(N)))[n])
    split = heart_k != head_k
    UR_all = np.where(mask & ~idle, U_R, -np.inf)
    if np.isfinite(UR_all).any():
        want_k = int(np.argmax(UR_all))                    # what the head would pick if everything were in view
        if need_k[want_k] >= 0:
            j_ = need_k[want_k]                              # in predicate form: "is a nurse", "can drive"
            asides.append("lacks"); fills["what"] = ("is " + GR["say"][j_]) if j_ < GR["NT"] else predicate(GR["say"][j_])
        elif need_a[want_k] >= 0:
            asides.append("lacks"); fills["what"] = "is " + E.ADJ_SAY[need_a[want_k]]
        elif not open_[want_k]:
            asides.append("out_of_reach")
        elif not seen[want_k]:
            asides.append("blind_spot")
    if split and st > 1.0 or st > 1.5:
        asides.append("stressed")
    if split and dsc > 1.15:
        asides.append("disciplined")
    elif split and dsc < 0.85:
        asides.append("undisciplined")
    elif split and ctrl < 0.3 and int(S["stage"][n]) >= 2:
        asides.append("little_control")
    lo_ = next((o for o in opts if o["k"] == lean_k and "reality" in o), None)
    if lo_ is not None:
        o_ = float(S["outlook"][n])
        if o_ > 0.8 and lo_["reality"]["misread"] == "hopeful":
            asides.append("hopeful")
        elif o_ < 0.25 and lo_["reality"]["misread"] == "doubtful":
            asides.append("gloomy")
        drv_ = [nm for nm, v in lo_["drivers"]["heart"] + lo_["drivers"]["head"] if v > 0]
        if (P.get("hz_k") or P.get("hz_want")) and float(S["fhz"][n]) > 0.5 and "horizon" in drv_:
            asides.append("short_horizon")
    asides = asides[:2]
    vc = COLORS[int(np.argmax(w))]
    vt = voice if voice is not None else L.get("VOICE")
    line = _fill(_pick(vt, VOICE_DEFAULT, key, vc, rng), **fills)
    return dict(situation=L["names"][s], age=round(float(S["age"]), 2), stage=E.STAGE_NAMES[int(S["stage"][n])].replace("_", " "),
                options=opts, heart=heart_k, head=head_k, lean=lean_k, lean_p=round(float(pr[lean_k]), 3),
                self_control=round(ctrl, 3), voice_color=vc, colors=colors_of(w),
                states=[E.ADJ_SAY[i_] for i_ in np.nonzero(np.asarray(S["adj"][n]))[0]] if "adj" in S else [],
                insight=dict(key=key, line=line, heart_driver=h_drv, head_driver=r_drv,
                             fills={k_: v_ for k_, v_ in fills.items() if k_ != "N"}),
                asides=[dict(key=a_, line=_fill(_pick(vt, VOICE_DEFAULT, a_, vc, rng), **fills)) for a_ in asides],
                title_held=title_held(S, n, s))


def title_held(S, n, s=None):
    """The title (or perk) that brings person n to moment s (holds:, any of several or a kind; with tenure: one held for
    those years): its name, for the Library's {title} slot, or None when the moment holds nothing."""
    L = S["L"]; GR = L.get("ROLES") if isinstance(L, dict) else None
    s = int(S["s"][n]) if s is None else int(s)
    if not GR or "S_HOLDM" not in GR or not GR["S_HOLDM"][s].any():
        return None
    i = title_held_index(S, n, s)
    return GR["say"][i] if i >= 0 else None


def title_held_index(S, n, s=None):
    """The catalogue index of that title (-1 for none): what an act field naming {title} acts on (batch.TITLE_HELD in
    GR["A_FX"]); the title itself before a facet on it, then the one held longest, as the engine resolves it."""
    L = S["L"]; GR = L.get("ROLES") if isinstance(L, dict) else None
    s = int(S["s"][n]) if s is None else int(s)
    if not GR or "S_HOLDM" not in GR or not GR["S_HOLDM"][s].any():
        return -1
    since = np.asarray(S["r_since"][n])
    ii = np.nonzero(GR["S_HOLDM"][s] & np.asarray(S["r_has"][n]))[0]
    lo, hi = GR["S_TEN"][s]
    if not np.isnan(lo):
        y = (float(S["t"]) - since[ii]) / 52
        ii = ii[(y >= lo) & (y <= hi)]
    if len(ii) > 1:
        ii = sorted(ii, key=lambda i: (GR["refines"][i] >= 0, since[i]))
    return int(ii[0]) if len(ii) else -1


# ---------------------------------------------------------------- snapshot and after
_LOGS = ("goal_log", "commit_log", "clash_log", "rite_log", "conv_log", "brk_log", "mark_log", "read_log", "ev_log", "role_log",
         "adj_log")


def season(S, n):
    """Emren's point 6 (threshold season): the crossing person n is in, at any pause of run_steps, or None.
    dict(kind "stage" or "title", name (the stage entered, e.g. "young_adult", or the title gained), step 1 the crossing,
    2 the in-between, 3 settling in (the step this week's moment plays, else the last one played), this_week (this week's
    moment is the season's), transform (this week's choice is its transforming chance), weeks_in, weeks_left)."""
    if "TH_K" not in S or not S.get("SEA_ON"):
        return None
    TH_K, TH_STEP, TH_TR = S["TH_K"], S["TH_STEP"], S["TH_TR"]
    s_ = int(S["s"][n]); k_ = int(S["sea_k"][n]); here = TH_K[s_] >= 0
    if here:
        k_ = int(TH_K[s_])
    if k_ < 0:
        return None
    if k_ < E.NS:
        kind, name = "stage", E.STAGE_NAMES[k_]
    else:
        GR = S["L"]["ROLES"]; kind, name = "title", GR["say"][k_ - E.NS]
    t0 = int(S["sea_t0"][n]); wk = int(S["t"]) - t0
    step = int(TH_STEP[s_]) if here else int(np.asarray(S["sea_done"][n]).sum())
    return dict(kind=kind, name=name, step=step, this_week=bool(here), transform=bool(here and TH_TR[s_]),
                weeks_in=wk, weeks_left=max(int(S["P"]["season_len"]) - wk, 0))


def bands(w, label):
    """Emren's point 14 (2026-10-05): each color's place against the identity's buffer (E.identity: joins above .22,
    leaves below .18). "in": part of who they are; "fading": still part of it, but at or under .22 and held by the buffer;
    "rising": not yet part of it, but above .18 and within reach; "out": not part of it."""
    w = np.asarray(w, float)
    return ["in" if (c in label and w[i] > 0.22) else "fading" if c in label else "rising" if w[i] > 0.18 else "out"
            for i, c in enumerate(COLORS)]


def dynamics(S, n, prev_label=""):
    """Emren's points 2 and 7 (2026-10-05): one week's color dynamics for person n, for a spider graph that moves week by
    week. Works at any pause of run_steps (S = its locals). Per color (lists of five, W U B R G):
      position     where they are (motive weights, sum 1)
      want         where they want to be (aspiration, sum 1); demand = want - position (the shift they long for)
      inertia      how hard they hold on, above (+) or below (-) an even share, and its parts: core (deep, 40%), habit
                   (30%), roles (their commitments, 30%), as the engine weighs them
      accelerator  how fast they can move toward each color now: readiness (plasticity x self-control) x belief they
                   can act that way (0.5 = typical) x doors (their world and means let them)
      bands        in / fading / rising / out against the identity buffer (see bands)
    and per person:
      openness     how open they are to change right now (crisis units: a rite gives 1, a turning point or a hard event
                   adds some, it halves in about six months); window = openness above 0.3
      pressure, threshold   pent-up wanting and what their inertia can hold back; a breakthrough comes when pressure
                   passes threshold (near = pressure / threshold)
      steadiness   how firmly they hold who they are (temperament)
      label        the identity (E.identity, carried forward from prev_label)"""
    sm = E.softmax
    w = sm(S["z"][n]); a = sm(S["y"][n]); kw = sm(S["k"][n])
    habit = np.asarray(S["habit"][n], float)
    hs = habit / habit.sum() if habit.sum() > 0 else np.full(C, 0.2)
    rsh = (np.asarray(S["held"][n]) * np.asarray(S["I"][n])) @ np.asarray(S["prof"][n])
    role = rsh / rsh.sum() if rsh.sum() > 0 else np.full(C, 0.2)
    hold = np.asarray(S["hold"][n], float) if "hold" in S else 0.4 * kw + 0.3 * hs + 0.3 * role
    doors = np.asarray(S["doors"](S["nic"], S["res"])[n], float) if callable(S.get("doors")) else np.ones(C)
    ready = float(np.asarray(S["plast"])[n] * np.asarray(S["ctrl"])[n])
    belief = np.asarray(S["SE"][n], float) / 0.5
    Q = float(np.asarray(S["Q"])[n]); thr = float(np.asarray(S["q_thr"])[n]) if "q_thr" in S else float(S["P"]["q_theta"])
    B = float(np.asarray(S["B"])[n]) if "B" in S else 0.0
    B += float(np.asarray(S["TWo"])[n]) if "TWo" in S else 0.0      # a turning point's window (engine tw_sep)
    label = E.identity(w, float(np.asarray(S["M"])[n]), prev_label)
    r = lambda v: [round(float(x), 4) for x in v]
    return dict(t=int(S["t"]), age=round(float(S["t"]) / 52, 2), position=r(w), want=r(a), demand=r(a - w),
                inertia=r(hold - 0.2), inertia_parts=dict(core=r(kw - 0.2), habit=r(hs - 0.2), roles=r(role - 0.2)),
                accelerator=r(ready * belief * doors), readiness=round(ready, 4), belief=r(belief), doors=r(doors),
                openness=round(B, 3), window=B > 0.3, pressure=round(Q, 3), threshold=round(thr, 3),
                near=round(Q / max(thr, 1e-9), 3), steadiness=round(float(np.asarray(S["steady"])[n]), 3),
                label=label, bands=bands(w, label))


def snapshot(S, n, b=None):
    """The state of person n at the "choose" pause, to compare against at the "end" pause. Pass before()'s result as b
    to keep what the heart and head wanted (for regret and lessons)."""
    sm = E.softmax
    g = lambda k_: np.array(np.asarray(S[k_])[n], copy=True) if k_ in S else None
    snap = dict(t=int(S["t"]), w=sm(S["z"][n]), want=sm(S["y"][n]), core=sm(S["k"][n]), need=g("need"), res=g("res"),
                stress=float(S["stress"][n]), content=float(S["content"][n]), peace=float(S["peace"][n]),
                mood=float(S["mood"][n]), outlook=float(S["outlook"][n]), react=float(S["react"][n]),
                discipline=float(np.asarray(S["dsc"])[n]) if "dsc" in S else 1.0,
                horizon=float(np.asarray(S["fhz"])[n]) if "fhz" in S else 0.0,
                skill=g("sig"), belief=g("SE"), niche=g("nic"), held=g("held"), I=g("I"), sat=g("sat"),
                gk=g("gk"), gs=g("gs"), gid=g("gid"), M=float(S["M"][n]), stage=int(S["stage"][n]),
                alive=g("alive"), widowed=bool(np.asarray(S["widowed"])[n]) if "widowed" in S else False,
                regret=float(np.asarray(S["regret"])[n]) if "regret" in S else 0.0,
                logs={k_: len(S[k_]) for k_ in _LOGS if k_ in S}, before=b)
    snap["identity"] = E.identity(snap["w"], snap["M"])
    return snap


def _new(S, snap, key, n):
    """This week's new entries for person n in one of the run's logs."""
    if key not in S:
        return []
    out = []
    for r in S[key][snap["logs"].get(key, 0):]:
        life = r["life"] if isinstance(r, dict) else r[0]
        if life == n:
            out.append(r)
    return out


def after(snap, S, n, lessons=None, rng=None, top=3):
    """What came of this week's choice for person n, at the "end" pause (S = that pause's locals).

    Returns a dict:
      act: situation, label, ways, worked, felt (what the character expected), surprise (better, as expected, worse),
        outcome_lines (the Library's lines for success or failure, if any), with_heart / with_head (was this what the
        heart or head wanted; needs before() passed to snapshot), regret (bool)
      changes: list of dicts (what, delta, word, size), largest first; size 1 = a notable week for that quantity. These are
        the week's changes from the act and from everything else that happened in it
      color_push: what moved the colors through each learning channel ("what worked and what did not": toward R)
      became: the top words ("more passionate", "more disciplined", "lonelier")
      events: what else happened this week to the person (a commitment started or ended, a goal born, sealed or ended,
        a death, a mark, a rite of passage, a turning point, a breakthrough)
      identity: before and now, and closer_to (the guild a rising or falling color is moving the person toward)
      lessons: list of (key, line, weight), most telling first: how the world works, as this week showed it
    """
    P = S["P"]; L = S["L"]; s = int(S["s"][n]); a = int(S["a"][n]); sm = E.softmax
    rng = rng if rng is not None else _rng(S, n, 2)
    idle = bool(S["idle"][n]); succ = bool(S["succ"][n]); ma = np.asarray(S["ma"][n])
    ph = float(S["ph"][n]); delta = float(S["delta"][n]); stakes = float(S["stakes"][n])
    src = L["src"][s] if "src" in L else {}
    outc = src.get("outcomes")
    b = snap.get("before")
    act = dict(situation=L["names"][s], label=L["labels"][s][a], ways=colors_of(ma), idle=idle, worked=succ,
               felt=round(ph, 3), surprise="better" if delta > 0.15 * stakes else "worse" if delta < -0.15 * stakes else "as expected",
               outcome_lines=list(outc[0 if succ else 1]) if outc else [])
    if b is not None:
        act["with_heart"] = a == b["heart"]; act["with_head"] = a == b["head"]
    # ---- changes
    w1, y1 = sm(S["z"][n]), sm(S["y"][n])
    ch = []

    def add(what, d, scale, words=None):
        if words is None:
            words = CHANGE_WORD.get(what, (f"more {what}", f"less {what}"))
        ch.append(dict(what=what, delta=round(float(d), 4), word=words[0] if d > 0 else words[1], size=round(abs(float(d)) / scale, 2)))
    for i, c in enumerate(COLORS):
        add(f"color:{c}", w1[i] - snap["w"][i], SCALE["color"], (COLOR_WORD[c], COLOR_WORD_DOWN[c]))
    for nm, key, sc in (("content", "content", "content"), ("peace", "peace", "peace"), ("mood", "mood", "mood"),
                        ("stress", "stress", "stress"), ("outlook", "outlook", "outlook")):
        add(nm, float(S[key][n]) - snap[nm], SCALE[sc])
    if "dsc" in S:
        add("discipline", float(S["dsc"][n]) - snap["discipline"], SCALE["discipline"])
    if "fhz" in S:
        add("horizon", float(S["fhz"][n]) - snap["horizon"], SCALE["horizon"])
    for j, nm in enumerate(E.NEEDS):
        add(f"need:{nm}", S["need"][n, j] - snap["need"][j], SCALE["need"])
    for j, nm in enumerate(E.RESOURCES if hasattr(E, "RESOURCES") else ["money", "time", "health", "ties", "freedom"]):
        if nm == "time":
            continue   # free time is recomputed each week from what is held
        add(f"res:{nm}", S["res"][n, j] - snap["res"][j], SCALE["res"])
    dsk = np.asarray(S["sig"][n]) - snap["skill"]
    if dsk.max() > 0:
        c_ = int(np.argmax(dsk)); add(f"skill:{COLORS[c_]}", dsk[c_], SCALE["skill"], (f"more skilled in {COLORS[c_]} ways", ""))
    for kk, nm in enumerate(E.KNAMES):
        if snap["held"][kk] and S["held"][n, kk]:
            add(f"strength:{nm}", S["I"][n, kk] - snap["I"][kk], SCALE["strength"], (f"more bound to the {nm}", f"less bound to the {nm}"))
    # what moved the colors this week: the learning channels (what worked, what was missing, the people around, fitting
    # the self, keeping up who one is), drift back toward the core, a turning point or a breakthrough
    push = {}
    if "stepF" in S:
        for j, nm in enumerate(E.CHANNELS[:5]):
            v_ = np.asarray(S["stepF"][n, j])
            if np.abs(v_).max() > 1e-4:
                c_ = int(np.argmax(np.abs(v_)))
                push[CHANNEL_WORD.get(nm, nm)] = dict(color=COLORS[c_], dir="toward" if v_[c_] > 0 else "away from",
                                                      size=round(float(np.abs(v_).sum()) / SCALE["color"], 2))
    ch.sort(key=lambda d_: -d_["size"])
    became = [d_["word"] for d_ in ch if d_["size"] >= 1 and d_["word"]][:top]
    # ---- events this week
    ev = []
    for r in _new(S, snap, "commit_log", n):
        ev.append(dict(kind="commitment", what=r[3], domain=E.KNAMES[r[2]], ways=colors_of(r[4])))
        if r[3] == "left" and E.KNAMES[r[2]] == "faith" and "faith_drifted" in S and bool(S["faith_drifted"][n]):
            ev[-1]["drifted"] = True                     # it stopped mattering, without a decision
    for r in _new(S, snap, "goal_log", n):
        dk_ = E.KNAMES.index(r["domain"]) if r["domain"] in E.KNAMES else -1
        ev.append(dict(kind="goal", what=r["what"], goal=r["kind"], domain=r["domain"], ways=colors_of(r["mix"]),
                       name=r.get("name") or plain_goal(r["kind"], dk_, r["mix"])))
        for f_, k_ in (("dream", "dream"), ("passion", "passion"), ("plan", "plan"), ("life_goal", "life"), ("say", "say"), ("trigger", "trigger")):
            if r.get(f_):   # the Library's words for it (dreams.py); the log's own "life" is the person
                ev[-1][k_] = r[f_]
    for r in _new(S, snap, "rite_log", n):
        ev.append(dict(kind="rite", to=r["to"], quiet=r["quiet"]))
    for r in _new(S, snap, "conv_log", n):
        ev.append(dict(kind="turning point", away_from=COLORS[r[2]], toward=colors_of(r[3])))
    for r in _new(S, snap, "brk_log", n):
        ev.append(dict(kind="breakthrough", toward=colors_of(r[2]["want"])))
    for r in _new(S, snap, "mark_log", n):
        ev.append(dict(kind="mark", mark=L["MARKS"][r[2]], worked=r[3]))
    if snap["alive"] is not None and "alive" in S:
        for r_, (x0, x1) in enumerate(zip(snap["alive"], S["alive"][n])):
            if x1 < x0:
                ev.append(dict(kind="death", role=E.ROLES[r_]))
    if "widowed" in S and bool(S["widowed"][n]) and not snap["widowed"]:
        ev.append(dict(kind="death", role="partner"))
    GR = L.get("ROLES") if S.get("RON") else None
    for r in _new(S, snap, "role_log", n):           # titles and perks gained, lost, suspended, restored
        i_ = r[2]
        ev.append(dict(kind="title" if i_ < GR["NT"] else "perk", what=r[3], name=GR["names"][i_], say=GR["say"][i_],
                       of=GR["kindname"][i_], how=r[4]))
        if i_ >= GR["NT"]:
            ev[-1]["predicate"] = predicate(GR["say"][i_])
        elif "r_prof" in S and "pwords" in GR:   # the way they hold it (one of the title's profiles), and what it refines
            ev[-1]["profile"] = GR["pwords"][i_][int(S["r_prof"][n, i_])]
            if GR["refines"][i_] >= 0:                   # the refined title it sits on now (refines can name several)
                on_ = np.nonzero(GR["REFM"][i_] & np.asarray(S["r_has"][n])[:GR["NT"]])[0] if "REFM" in GR else []
                ev[-1]["refines"] = GR["names"][int(on_[0]) if len(on_) else GR["refines"][i_]]
    for r in _new(S, snap, "adj_log", n):            # v7 adjectives: a state begins or ends (happy, lonely, wealthy)
        say_ = E.ADJ_SAY[r[2]]
        ev.append(dict(kind="state", what=r[3], name=E.ADJ_NAMES[r[2]], say=say_,
                       line=("{N} is " + say_ + " now.") if r[3] == "gained" else ("{N} is no longer " + say_ + ".")))
    # ---- identity, and what the person is moving toward
    id0 = snap["identity"]; id1 = E.identity(w1, float(S["M"][n]), id0)
    closer = None
    dw = w1 - snap["w"]
    if float(S["M"][n]) >= 6.0:
        best = None
        for i, c in enumerate(COLORS):
            if c not in id1 and dw[i] > 0:            # rising toward joining
                dist = 0.22 - w1[i]; lab_ = "".join(x for x in COLORS if x in id1 + c); via_ = "rising"
            elif c in id1 and dw[i] < 0 and len(id1) > 1:   # falling toward leaving
                dist = w1[i] - 0.18; lab_ = id1.replace(c, ""); via_ = "falling"
            else:
                continue
            score = dist / max(abs(dw[i]), 1e-6)            # weeks to get there at this week's pace
            if best is None or score < best[0]:
                best = (score, lab_, round(float(dist), 3), via_, c)
        if best is not None:
            closer = dict(identity=best[1], guild=E.GUILD.get(best[1], best[1]), distance=best[2], via=best[3], color=best[4])
    # ---- lessons: how the world works, as this week showed it
    vc = COLORS[int(np.argmax(w1))]
    lt = lessons if lessons is not None else L.get("LESSONS")
    les = []

    def lesson(key, wt, **kw):
        les.append(dict(key=key, line=_fill(_pick(lt, LESSONS_DEFAULT, key, vc, rng), N="{N}", **kw), weight=round(float(wt), 2)))
    c_act = colors_of(ma).split(" ")[0] if not idle else ""
    tst = float(np.asarray(P["T_stage"], float)[snap["stage"]] / np.asarray(P["T_stage"], float)[2])
    if not idle:
        if succ:
            lesson("practice", 0.6, c=COLOR_NAME.get(c_act, c_act))
        p_true = float(S["p_true"][n])
        if P.get("disc_win") and b is not None and act.get("with_head") and succ and p_true < 0.4:
            lesson("hard_win", 1.5 * tst)
        sc_ = float(L["SC"][s, a]) if "SC" in L else 0.0
        if sc_ > 0:
            lesson("self_control_up", 1.2 * tst)
        elif sc_ < 0:
            lesson("self_control_down", 1.2 * tst)
        ins = np.asarray(S["stepF"][n, 0]) if "stepF" in S else dw     # what the outcome itself taught
        big_c = int(np.argmax(np.abs(ins)))
        if abs(delta) > 0.6 * stakes and abs(ins[big_c]) > SCALE["color"]:
            lesson("surprise_teaches", abs(delta) / max(stakes, 1e-6) * 2, c=COLOR_NAME[COLORS[big_c]],
                   dir="more" if ins[big_c] > 0 else "less")
        own = float((ma * snap["w"]).sum() / snap["w"].max())
        if not succ and stakes >= 1.0 and own > 0.8:
            lesson("fail_own_ways", 1.6)
        elif not succ and snap["M"] > 30 and own > 0.8:
            lesson("defended", 0.7)
        tg = L["TAG"][s, a] if "TAG" in L else np.zeros(4, bool)
        if tg[0]:
            lesson("habit", 0.8)
        if tg[1] and succ:
            lesson("door", 1.0, c=COLOR_NAME.get(c_act, c_act))
        if tg[3] and succ:
            lesson("binding", 0.9)
        clk = int(S["closed_s"][n, a]) if S.get("closed_s") is not None else int(L["CLOSED"][s, a]) if "CLOSED" in L else -1
        if GR is not None and succ and np.ndim(S.get("pbump", 0.0)) == 2 and float(S["pbump"][n, a]) >= 0.15:
            # a perk gained this past year that this act leaned on, in a try the character was unsure of: learning it paid off
            NT = GR["NT"]; hs = np.asarray(S["r_has"][n])
            hc = (hs[NT:] * 4 * GR["odds"]) * (GR["ind"][NT:] @ ma) * ((float(S["t"]) - np.asarray(S["r_since"][n, NT:])) < 52)
            if hc.max() >= 0.12 and ph < 0.7:
                j_ = NT + int(np.argmax(hc))
                lesson("perk_helped", 0.5 + float(S["pbump"][n, a]), what=predicate(GR["say"][j_]), perk=GR["names"][j_])
        if clk >= 0 and not succ:
            lesson("backfire", 1.8, kind=("law", "approval of others", "means")[clk])
        if b is not None and act.get("with_heart") and not act.get("with_head") and not succ and delta < -0.2:
            act["regret"] = True
            lesson("regret", 1.4)
        else:
            act["regret"] = False
        nd = np.asarray(S["need"][n]) - snap["need"]; j_ = int(np.argmax(nd))
        if succ and nd[j_] > 0.08 and snap["need"][j_] < 0.5 and (np.maximum(np.asarray(S["ea"][n]), 0) @ E.NMAP.T)[j_] > 0:
            lesson("need_met", 1.0, need=E.NEEDS[j_])
        dom = L["DOM"][s]
        for kk, nm in enumerate(E.KNAMES):
            if snap["held"][kk] and dom[kk] >= 0.7 and succ:
                lesson("duty_kept", 0.7, kind=KIND_NOUN[nm], kind_ref=KIND_REF[nm])
                break
    for e_ in ev:
        if e_["kind"] == "commitment" and e_["what"] in ("start", "inherited"):
            lesson("commit_start", 1.3, kind=KIND_NOUN[e_["domain"]], kind_ref=KIND_REF[e_["domain"]], c=names(e_["ways"]))
        elif e_["kind"] == "commitment":
            lesson("commit_end", 1.2, kind=KIND_NOUN[e_["domain"]], kind_ref=KIND_REF[e_["domain"]])
        elif e_["kind"] == "goal" and e_["what"] == "became a passion":
            lesson("sealed", 1.5, goal=e_.get("dream") or e_["name"].replace("the passion for", "the dream of", 1))
        elif e_["kind"] == "goal" and e_["what"] not in ("begins", "became a plan", "extended"):
            lesson("goal_end", 1.1, goal=e_["name"][0].upper() + e_["name"][1:], what=e_["what"])
        elif e_["kind"] == "death":
            lesson("loss", 1.6 if (P.get("hz_k") or P.get("hz_want")) else 0.0)
        elif e_["kind"] == "rite":
            lesson("rite_quiet" if e_["quiet"] else "rite", 1.4, stage=e_["to"].replace("_", " "))
        elif e_["kind"] == "turning point":
            lesson("turning_point", 2.0, c=COLOR_NAME[e_["away_from"]])
        elif e_["kind"] == "breakthrough":
            lesson("breakthrough", 2.0)
        elif e_["kind"] == "title" and e_["what"] == "gained":
            lesson("status_gain" if e_["of"] == "status" else "title_gain", 1.5, what=e_["say"])
        elif e_["kind"] == "title" and e_["what"] == "lost" and e_["how"] not in ("replaced",) and not e_["how"].startswith("became"):
            lesson("title_loss", 1.2, what=e_["say"])
        elif e_["kind"] == "perk" and e_["what"] in ("gained", "regained"):
            lesson("perk_gain", 1.0, what=e_["predicate"], perk=e_["name"])
        elif e_["kind"] == "perk" and e_["what"] in ("lost", "suspended"):
            lesson("perk_loss", 1.0, what=e_["predicate"], perk=e_["name"])
    if P.get("goals") and snap["gk"] is not None and not idle:
        for j in range(len(snap["gk"])):
            if snap["gk"][j] >= 0 and S["gk"][n, j] == snap["gk"][j] and S["gid"][n, j] == snap["gid"][j]:
                dg = float(S["gs"][n, j] - snap["gs"][j])
                if abs(dg) > 0.01:
                    lesson("goal_step" if dg > 0 else "goal_setback", 0.5 + 10 * abs(dg), goal=goal_name(S, n, j))
    if float(S["stress"][n]) - snap["stress"] > 0.3:
        lesson("stress_up", 1.0)
    if closer is not None and closer["distance"] < 0.02:   # a color rising toward joining, or falling away (drifting_from)
        if closer["via"] == "rising":
            lesson("closer_to", 0.9, guild=plain_identity(closer["identity"]), guild_name=closer["guild"])
        else:
            lesson("drifting_from", 0.9, guild=plain_identity(closer["identity"]), guild_name=closer["guild"],
                   lost=COLOR_ADJ[closer["color"]])
    nxt = []
    if GR is not None:                              # titles that grow from the ones held (a cook toward head chef), best fit first
        hs = np.asarray(S["r_has"][n]); NT = GR["NT"]
        for i_ in range(NT):
            fr_ = [j_ for j_ in GR["rule"][i_]["after"] if hs[j_]]
            if fr_ and not hs[i_] and GR["ages"][i_, 0] <= float(S["age"]) <= GR["ages"][i_, 1]:
                fit_ = float((GR["PW"][i_, :GR["PN"][i_]] @ w1).max()) if "PW" in GR else float(GR["ways"][i_] @ w1)
                nxt.append((fit_ if GR["ways"][i_].sum() else 0.2, GR["names"][i_], GR["names"][fr_[0]]))
        nxt = [dict(title=a_, from_=b_) for _, a_, b_ in sorted(nxt, reverse=True)[:2]]
    les = [l_ for l_ in les if l_["weight"] > 0]
    les.sort(key=lambda l_: -l_["weight"])
    return dict(act=act, changes=ch[:12], became=became, color_push=push, events=ev,
                identity=dict(before=id0, now=id1, guild=E.GUILD.get(id1, id1), closer_to=closer, next_titles=nxt), lessons=les[:top])


def self_view(ident, n, t=None):
    """N1b (chroma-identity/for-the-engine.md §6): who person n is, as far as the game may show it at week t (None: the
    end of the run). ident is the run's identity dict. Sex as raised is always shown; own gender, attraction, asexual and
    intersex only from the week a moment about them first came (found); nothing hidden is shown before it is found."""
    g = lambda k_, d_=None: (np.asarray(ident[k_])[n] if k_ in ident else d_)
    fd = ident.get("found", {})
    seen = lambda k_: (k_ in fd and int(np.asarray(fd[k_])[n]) > -10 ** 6 // 2 and (t is None or int(np.asarray(fd[k_])[n]) <= t))
    out = dict(raised_as="female" if bool(g("female")) else "male")
    if seen("intersex"):
        out["intersex"] = bool(g("intersex", False))
    if seen("gender"):
        out["own_gender"] = {0: "as raised", 1: "the other", 2: "neither or both"}[int(g("gender_self", 0))]
        out["named_gender"] = bool(g("named", False))
    if seen("attraction"):
        out["attraction"] = int(g("attr", 0)); out["came_out"] = bool(g("came_out", False))
    if seen("ace"):
        out["ace"] = bool(g("ace", False))
    for k_ in ("partner_same", "cross_title"):
        if k_ in ident:
            out[k_] = bool(g(k_))
    if "role_fit" in ident:
        out["role_fit"] = round(float(g("role_fit")), 2)
    for k_ in ("role_strict", "accept_trans"):
        if k_ in ident:
            out[k_] = float(ident[k_])
    out["found"] = {k_: int(np.asarray(v_)[n]) for k_, v_ in fd.items() if seen(k_)}
    return out


def say(d, name):
    """Replace {N} in every line of a before() or after() result with the character's name (in place)."""
    def walk(x):
        if isinstance(x, dict):
            return {k_: walk(v_) for k_, v_ in x.items()}
        if isinstance(x, list):
            return [walk(v_) for v_ in x]
        if isinstance(x, str):
            return x.replace("{N}", name)
        return x
    return walk(d)
