"""Release's reader for the v24 bar row H1 hover_sizes (records/v24/scope.md): "before a pick the hover shows only the
three sizes for needs, means, people and titles, never a number, and each arrow's direction matches what the pick then
does in at least 9 picks in 10" (Release's reading; plan.md section 1 sets no number).

    python3 -B hover_check.py <game dir with engine_pin filled> [--presets 1,2,3,4] [--seeds 1-2] [--jobs 2]
                              [--policy reader] [--scope forecast] [--out report.txt] [--keep DIR] [--max-cp N]

Whole Earth lives on the Game object as the page plays it, with the game's arrows switch on (CHROMA_GAME
{"arrows": true, "because": true}; both are read-only, every step plays as with them off). The player is Release's
picks/impact.py: its setup (Console, preset, "Ari", random.seed(seed)) and its policy (default reader: it pushes when
what the moment shows beats their own pick by a margin, else it lets them choose, so own and pushed picks both occur).
Each life runs in its own process on one core (OMP_NUM_THREADS=1); --jobs lives at a time.

At every checkpoint, for the option the engine then acts on (loc["a"] at the week's end), the tool reads the option as
the page gets it (Game.cp_hud) and renders, as text, what the page's hover shows for it: the reading strip a desktop
hover fills (web/src/app/06-moment.js stripHTML) and the detail a tap opens on a phone (tipOption); the arrows as the
page draws them (arrowsHTML: non-need arrows first, the first five a side).

    H1a  hovers with a number: a digit or "%" in a hover row of the option taken. --scope sets which rows count:
         arrows (the two "Moves if ..." rows only), forecast (default, Release's reading of plan.md §1 "No exact
         numbers come before the choice": every row that forecasts what the pick does to needs, means, people and
         titles, that is kinds less Lacking, which reads a need's level now, not what the pick does), kinds (every row
         about needs, means, people and titles: Meets, Lacking, Costs, If it works, If it fails, For good, Could start,
         Titles and perks, and the arrows) or all (everything shown but the option's key number; the felt odds and
         the rows about the act itself, which the plan keeps, always hit). Malformed arrows (A2's form: kind, name, dir, size 1-3, its
         word, nothing else) count too. The rows outside the scope are listed as information.
    H1b  the arrows shown for the option taken, on the side that happened (works or fails), by kind and by size
    H1c  whether each shown arrow's direction matched what the pick then did, over the arrows that moved, overall, by
         kind, by size and by target; and the share of picks whose moved arrows all matched (the gate, at .90)

What the pick then did, at foresee.arrows' own horizon: the week of the act, from the "choose" pause (the hover) to the
week's "end" pause. foresee.arrows (chroma-engine/v22-speedpass/foresee.py:174) forecasts the act's own effect in the
week it is taken: needs by the engine's weekly rules for the act (run_13_learning.py, run_14_marks.py), means and ties
by the Library's PAY + WIN or LOSE applied once (run_12_commitments.py:6), a commitment's start by that week's draw
(run_12_commitments.py), titles by the act's own fields that week (run_14_marks.py:14). Measured:
    need        the Engine's own record of why each need moved (need_why, engine.py:826): the sources the game's
                "Because of you" counts as the pick's (act and player; game_because.py:15), end minus choose
    means, ties res[j] at the end minus res[j] at the choose pause (raw: the week's drift toward each means' level,
                run_12_commitments.py:195, and any event after the pick fall in it too)
    commitment  held[k] at the end minus at the choose pause (+1 started, -1 ended, 0 no move)
    title/perk  r_has[j] at the end minus at the choose pause (+1 gained, -1 lost or suspended, 0 no move)
A change under EPS in size is "no move", reported apart and left out of the matched share (counted as a miss in the
strict line). Arrows are compared on the side that happened (the engine's succ that week).

Prints one line per life, then the rows, then "H1: PASS" (H1a 0 and the picks' matched share at least .90) or
"H1: MISS"; the same goes to --out. --keep DIR keeps each life's record (hover_<preset>_<seed>.json and its log) in
DIR, else they go to a temporary folder that is removed; --max-cp N stops each life after N checkpoints (a quick
try of the tool, not a reading). Exit 0 on PASS, 1 on MISS, 2 when a life failed or the game has no arrows."""
import json, math, os, re, shutil, subprocess, sys, tempfile, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
PICKS = os.environ.get("RELEASE_PICKS", os.path.normpath(os.path.join(HERE, "..", "..", "..", "picks")))   # chroma-release/picks
EPS = 1e-4            # a hundredth of a point on the 0..1 scales; the smallest arrows are .003 (need) and .02 (means)
SHOWN = 5             # the page draws the first five arrows a side (06-moment.js arrowsHTML)
GATE = 0.90
NUM = re.compile(r"[0-9%]")
KINDS = ("need", "means", "people", "title")
WORDS = {1: "a little", 2: "clearly", 3: "a lot"}
YOU = ("act", "player")                         # game_because.py: the sources that are the pick's own
ARROW_ROWS = {"Moves if it works", "Moves if it fails"}
KIND_ROWS = ARROW_ROWS | {"Meets", "Lacking", "Costs", "If it works", "If it fails", "For good", "Could start", "Titles and perks"}
FORECAST_ROWS = KIND_ROWS - {"Lacking"}   # Lacking reads a need's level now; every other kind row forecasts the pick

# ------------------------------------------------------------------ the page's hover, as text (web/src/app/*.js)
NEED_LONG = {"safety": "safety", "belonging": "belonging", "autonomy": "room to choose", "competence": "a sense of skill",
             "meaning": "meaning"}
CNAME = {"W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green"}
ACC_WORD = {"would go with it": "Would go with it", "okay with it": "Okay with it", "reluctant": "Reluctant",
            "against it": "Against it", "their own pick": "Their own pick"}
CLOSED_WORD = {"law": "the law", "approval": "the approval of others", "means": "lack of means"}
MISREAD_WORD = {"hopeful": "they think it likelier than it is", "doubtful": "they think it less likely than it is",
                "fair": "they read it about right"}


def _round(v):                                  # JS Math.round
    return int(math.floor(float(v) * 100 + 0.5))


def pct(v):
    return f"{_round(v)}%"


def fpct(v):
    return f"{min(99, max(1, _round(v)))}%"


def base_word(b):
    b = float(b)
    return ("it almost always works" if b >= 0.95 else "it almost never works" if b < 0.05
            else f"it works about {max(1, min(9, int(math.floor(b * 10 + 0.5))))} times in 10")


def _sg(x):
    return ("+" if str(x)[:1] == "+" else "−") + str(x)[1:]


def shown_arrows(xs):
    """The arrows the page draws for one side: non-need arrows first (a stable sort), the first five."""
    return sorted(list(xs or []), key=lambda a: a.get("kind") == "need")[:SHOWN]


def arrows_text(xs):
    out = []
    for a in shown_arrows(xs):
        try:
            n = int(a.get("size") or 0)
        except (TypeError, ValueError):
            n = 0
        nm = NEED_LONG.get(a.get("name"), a.get("name")) if a.get("kind") == "need" else a.get("name")
        out.append(f"{nm} {('▲' if a.get('dir') == 'up' else '▼') * n} ({a.get('word')})")   # its word is the chip's title
    return " ".join(out)


def _colors(o):
    return " and ".join(CNAME.get(c, c) for c in dict.fromkeys(list(o.get("means") or []) + list(o.get("ends") or [])))


def _aims(ws):
    return "; ".join(f"{w.get('step')} ({w.get('aim')}{', ' + str(w['height']) if w.get('height') else ''}"
                     f"{', if it fails' if w.get('if_fails') else ''})" for w in ws)


def _stake_fails(sk):
    return ", and ".join(str(x) for x in (sk.get("cost"), sk.get("fails"), sk.get("risk")) if x)


def strip_rows(o):
    """stripHTML: what a desktop hover (or keyboard focus) fills the reading strip with, as (row, text)."""
    f = o.get("follows") or {}; sk = o.get("at_stake") or {}
    acc = "their own pick" if o.get("own") else o.get("accept") or "okay with it"
    pas = not o.get("means"); r = []
    r.append(("title", str(o.get("label", ""))))
    if not pas:
        bo = o.get("bold")
        if bo:
            r.append(("Bold", "lower odds, and it changes something for good either way" + (f"; {bo['fit_say']}" if bo.get("fit_say") else "")))
        re_ = o.get("reality")
        tail = ((", " + ("reality is harsher" if re_.get("misread") == "hopeful" else "reality is kinder")) if re_.get("misread") != "fair"
                else ", about right") if re_ else (f", looks {o['hint']}" if o.get("hint") else "")
        r.append(("Feels", fpct(o.get("felt", 0)) + tail))
        if o.get("base") is not None:
            r.append(("Most people", re.sub(r"^it ", "", base_word(o["base"]))))
    r.append(("How they feel", ACC_WORD.get(acc, acc) + (" · hadn't thought of it" if o.get("status") == "didn't think of it" else "")
              + (" · " + " and ".join(CNAME.get(c, c) for c in o["clash"]) + " against who they are"
                 if acc == "against it" and o.get("clash") else "")))
    if o.get("status") == "considered" and not o.get("own") and o.get("lean") is not None:
        r.append(("Their lean", pct(o["lean"])))
    if f.get("needs"):
        r.append(("Meets", ", ".join(f["needs"])))
    if f.get("lift"):
        r.append(("Lacking", "; ".join(f"{NEED_LONG.get(x.get('need'), x.get('need'))} at {pct(x.get('level', 0))}: {x.get('lift')} to "
                                       "satisfaction if it works" for x in f["lift"])))
    if not o.get("own") and not pas and float(o.get("rel") or 0) >= 0.02:
        rs = float(o.get("resent") or 0); tr = float(o.get("trust") or 0)
        r.append(("If you push", ("little resentment" if rs < 0.05 else "some resentment" if rs < 0.3 else
                                  "resentment: strain and pent-up wanting" if rs < 0.6 else "strong resentment")
                  + (f" ({'they trust you' if tr > 0 else 'they distrust you'} in these colors)" if abs(tr) >= 0.05 else "")
                  + "; it counts against their own life unless it gives them something they lack"))
    if f.get("cost"):
        r.append(("Costs", " ".join(str(x)[1:] for x in f["cost"])))
    if o.get("arrows"):
        r.append(("Moves if it works", arrows_text(o["arrows"].get("win"))))
        r.append(("Moves if it fails", arrows_text(o["arrows"].get("fail"))))
    if o.get("aims"):
        r.append(("Toward an aim", _aims(o["aims"])))
    if not pas:
        r.append(("If it works", (" ".join(_sg(x) for x in f["win"]) + ", " if f.get("win") else "") + "toward " + _colors(o)))
    if sk.get("win"):
        r.append(("For good", str(sk["win"])))
    if sk.get("people"):
        r.append(("For good", str(sk["people"])))
    if not pas:
        r.append(("If it fails", ", ".join(([_stake_fails(sk)] if _stake_fails(sk) else []) + [_sg(x) for x in f.get("lose") or []]
                                          + ["strain", "doubt"])))
    if o.get("commit"):
        r.append(("Could start", f"a {o['commit']}" + (f" (about {pct(f['commit_p'])})" if f.get("commit_p") else "")))
    if o.get("seen"):
        r.append(("Seen it done", str(o["seen"].get("text", ""))))
    if o.get("lever"):
        lv = o["lever"]
        r.append(("A push on the world", str(lv.get("what") or lv.get("name")) + (f" ({lv['target']})" if lv.get("target") else "")))
    if o.get("status") == "out of reach":
        r.append(("Out of reach", f"{o.get('why')}; can be forced, at higher risk"))
    if o.get("needs"):
        r.append(("Needs", str(o["needs"].get("line", "")) + (f"; without it {CLOSED_WORD.get(o['closed'], 'the world')} stands in the way"
                                                             if o.get("closed") else "")))
    if o.get("helped"):
        r.append(("Helped by", ", ".join(f"{h.get('pred')}" + (f" +{h['plus']}%" if h.get("plus") else "") for h in o["helped"])))
    if o.get("roles_fx"):
        r.append(("Titles and perks", "; ".join(str(x.get("line", "")) for x in o["roles_fx"])))
    return r


def tap_rows(o):
    """tipOption: the detail a tap opens on a touch screen (the phone's hover), as (row, text)."""
    f = o.get("follows") or {}; sk = o.get("at_stake") or {}
    acc = "their own pick" if o.get("own") else o.get("accept") or "okay with it"
    r = [("title", str(o.get("label", "")))]
    if o.get("heart_pick") or o.get("head_pick"):
        r.append(("Inner voice", ("the heart's pick " if o.get("heart_pick") else "") + ("the head's pick" if o.get("head_pick") else "")))
    r.append(("How they feel", ACC_WORD.get(acc, acc) + (" (they hadn't thought of it)" if o.get("status") == "didn't think of it" else "")
              + (" This goes against who they are" if acc == "against it" and o.get("clash") else "")))
    if o.get("lever"):
        lv = o["lever"]
        r.append(("A push on the world", f"{lv.get('name')}: {lv.get('what')}" + (f" ({lv['target']})" if lv.get("target") else "")))
    if o.get("means"):
        bo = o.get("bold")
        if bo:
            r.append(("Bold", "lower odds, and it changes something for good either way" + (f" {bo['fit_say']}" if bo.get("fit_say") else "")))
        r.append(("Feels", f"{fpct(o.get('felt', 0))} likely to work"))
        if o.get("base") is not None:
            r.append(("For most people", base_word(o["base"])))
        re_ = o.get("reality")
        if re_:
            r.append(("Reality, roughly", f"works {re_.get('band')}" + (f" {MISREAD_WORD.get(re_.get('misread'), '')}" if re_.get("misread") != "fair" else "")
                      + (f" ({re_['why']})" if re_.get("misread") != "fair" and re_.get("why") else "")))
        else:
            r.append(("Reality", f"looks {o['hint']}" if o.get("hint") else "–"))
        if o.get("heart") is not None:
            dr = o.get("drivers") or {}
            why = lambda side: ", ".join(("+" if v > 0 else "−") + str(n) for n, v in (dr.get(side) or []))
            r.append(("Heart and head", f"{why('heart')} {pct(o['heart'])} {why('head')} {pct(o.get('head') or 0)}"))
        r.append(("Colors", _colors(o)))
    if o.get("status") == "considered" and not o.get("own") and o.get("lean") is not None:
        r.append(("Their lean", f"{pct(o['lean'])} likely to pick it themselves"))
    if o.get("seen"):
        r.append(("Seen it done", str(o["seen"].get("text", ""))))
    if o.get("status") == "out of reach":
        r.append(("Out of reach", f"{o.get('why')}; can be forced, at higher risk"))
    if f.get("needs"):
        r.append(("Meets", ", ".join(f["needs"])))
    if f.get("cost"):
        r.append(("Costs", " ".join(str(x)[1:] for x in f["cost"])))
    if f.get("win"):
        r.append(("If it works", " ".join(_sg(x) for x in f["win"]) + ", draws them toward " + _colors(o)))
    elif o.get("means"):
        r.append(("If it works", "draws them toward " + _colors(o)))
    if o.get("arrows"):
        r.append(("Moves if it works", arrows_text(o["arrows"].get("win"))))
        r.append(("Moves if it fails", arrows_text(o["arrows"].get("fail"))))
    if o.get("aims"):
        r.append(("Toward an aim", _aims(o["aims"])))
    if sk.get("win"):
        r.append(("For good", str(sk["win"])))
    if sk.get("people"):
        r.append(("For good", str(sk["people"])))
    if o.get("means"):
        r.append(("If it fails", ", ".join(([_stake_fails(sk)] if _stake_fails(sk) else []) + [_sg(x) for x in f.get("lose") or []]
                                          + ["strain", "doubt in these ways"])))
    if o.get("commit"):
        r.append(("Could start", f"a {o['commit']}" + (f" (about {pct(f['commit_p'])})" if f.get("commit_p") else "")))
    if o.get("needs"):
        r.append(("Needs", str(o["needs"].get("line", "")) + (f". Without it, {CLOSED_WORD.get(o['closed'], 'the world')} stands in the way"
                                                             if o.get("closed") else "")))
    if o.get("helped"):
        r.append(("Helped by", ", ".join(f"{h.get('pred')}" + (f" +{h['plus']}%" if h.get("plus") else "") for h in o["helped"])))
    if o.get("roles_fx"):
        r.append(("Titles and perks", "; ".join(str(x.get("line", "")) for x in o["roles_fx"])))
    return r


def in_scope(label, scope):
    return label in ARROW_ROWS if scope == "arrows" else label in FORECAST_ROWS if scope == "forecast" \
        else label in KIND_ROWS if scope == "kinds" else True


def hover_hits(o):
    """Every hover row of option o that shows a digit or a percent sign, as [view, row, text]."""
    return [[v, lb, tx] for v, rows in (("hover", strip_rows(o)), ("tap", tap_rows(o))) for lb, tx in rows if NUM.search(tx)]


def malformed(o):
    """A2's form for every arrow the page gets for option o (both sides), as a list of what is wrong."""
    if not o.get("means"):
        return []
    ar = o.get("arrows")
    if not isinstance(ar, dict) or set(ar) != {"win", "fail"}:
        return [f"no arrows dict: {ar!r}"[:160]]
    bad = []
    for side in ("win", "fail"):
        for x in ar[side] or []:
            if (not isinstance(x, dict) or set(x) != {"kind", "name", "dir", "size", "word"} or x["kind"] not in KINDS
                    or x["dir"] not in ("up", "down") or x["size"] not in WORDS or x["word"] != WORDS[x["size"]]):
                bad.append(f"{side}: {x!r}"[:160])
    return bad


# ------------------------------------------------------------------ one life (a subprocess)
def play(gdir, preset, seed, policy, out, max_cp=0):
    t0 = time.time()
    os.environ.update(PRESET=preset, GAMEDIR=gdir)
    argv = sys.argv; sys.argv = argv[:1]           # impact rewrites argv[1] when it is imported
    sys.path.insert(0, PICKS)
    import impact                                  # puts the game first on sys.path and chdirs there
    sys.argv = argv
    import random
    import numpy as np
    random.seed(seed)                              # as impact.play: the seed, then the console's own setup
    from console import Console
    import game_base
    E, F, GAME = game_base.E, game_base.F, game_base.GAME
    if not GAME.get("arrows") or not hasattr(F, "arrows"):
        json.dump(dict(no_arrows=True, preset=preset, seed=seed), open(out, "w"))
        return
    NE, RS, KN = list(E.NEEDS), list(E.RESOURCES), list(E.KNAMES)
    SRC = list(getattr(E, "NSOURCES", []))
    you_i = [SRC.index(s_) for s_ in YOU if s_ in SRC]
    c = Console(); c.handle(""); c.handle(preset); c.handle("Ari")
    g = c.g; g.freq = "normal"
    prng = np.random.default_rng(seed + 31)       # impact.play's stream for its policies
    one = lambda v: np.asarray(v).ravel()[0]

    def state(loc):
        d = dict(need=np.array(loc["need"][0], float), res=np.array(loc["res"][0], float), held=np.array(loc["held"][0], bool))
        if dict.get(loc, "r_has") is not None:
            d["r_has"] = np.array(loc["r_has"][0], bool)
        if dict.get(loc, "nw") is not None and you_i:
            d["nw"] = np.array(loc["nw"][0], float)
        return d

    roles = {}                                     # a title's name -> its indexes in the Library's ROLES
    picks, cps, info = [], [], Counter()
    pend = {}
    orig_end = g._on_end

    def on_end(t, loc):                            # the week's "end" pause, before the game's own end-of-week steps
        p = pend.pop("p", None)
        if p is not None and p["t"] != t:
            info["no_end"] += 1; p = None
        if p is not None:
            try:
                measure(p, loc)
            except Exception as ex:                # a reading that fails is counted, never a crash of the life
                info["measure_error"] += 1; info["err:" + type(ex).__name__ + ": " + str(ex)[:120]] += 1
        return orig_end(t, loc)
    g._on_end = on_end

    def measure(p, loc):
        if not roles and "L" in loc and loc["L"].get("ROLES") is not None:
            for j, nm in enumerate(loc["L"]["ROLES"]["names"]):
                roles.setdefault(nm, []).append(j)
            info["role_name_clash"] = sum(1 for nm in roles if nm in KN or nm in RS or nm in NE)
        a = int(one(loc["a"])); ok = bool(one(loc["succ"])); s1 = state(loc); s0 = p["s0"]
        o = p["opts"].get(a)
        rec = dict(age=p["age"], sit=p["sit"], k=a, own=p["own"], pushed=bool(p["pick"] is not None and a != p["own"]),
                   turning=p["turning"], worked=ok, arrows=[], hits=[], bad=[])
        if o is None:
            info["act_not_shown"] += 1; picks.append(rec); return
        rec["pass"] = not o.get("means")
        rec["hits"] = hover_hits(o); rec["bad"] = malformed(o)
        ar = o.get("arrows") or {}
        side = "win" if ok else "fail"
        rec["both_sides"] = {sd: len(shown_arrows(ar.get(sd))) for sd in ("win", "fail")}
        shown_ids = {id(x) for x in shown_arrows(ar.get(side))}
        for x in ar.get(side) or []:
            kind, nm = x.get("kind"), x.get("name")
            tt, d, raw = None, None, None
            if kind == "need" and nm in NE:
                j = NE.index(nm); tt = "need"; raw = float(s1["need"][j] - s0["need"][j])
                d = float((s1["nw"] - s0["nw"])[you_i, j].sum()) if "nw" in s0 and "nw" in s1 else raw
            elif kind in ("means", "people") and nm in RS:
                j = RS.index(nm); tt = "ties" if nm == "ties" else "means"; d = float(s1["res"][j] - s0["res"][j])
            elif kind in ("people", "title") and nm in KN:
                j = KN.index(nm); tt = "commitment"; d = float(int(s1["held"][j]) - int(s0["held"][j]))
            elif kind == "title" and nm in roles and "r_has" in s0:
                ix = roles[nm]; tt = "title/perk"
                d = float(int(bool(s1["r_has"][ix].any())) - int(bool(s0["r_has"][ix].any())))
            rec["arrows"].append([kind, nm, x.get("dir"), x.get("size"), id(x) in shown_ids, tt, d, raw])
        picks.append(rec)

    k = 0
    while not g.over and k < 20000:
        r = g.advance()
        if r == "over" or g.over:
            break
        if r != "checkpoint":
            continue
        cp = g.pending; loc = g.loc; k += 1
        if max_cp and k > max_cp:                  # --max-cp: a short check, not a whole life
            break
        hud = g.cp_hud({o["idx"]: o["idx"] for o in cp["options"]})
        opts = {int(o["k"]): o for o in hud["options"]}
        nh = Counter()
        for o in hud["options"]:                   # every way shown at the card (information)
            if not o.get("means"):
                continue
            nh["ways"] += 1
            labs = {lb for _, lb, _ in hover_hits(o)}
            for sc in ("arrows", "kinds", "all"):
                nh[sc] += any(in_scope(lb, sc) for lb in labs)
        cps.append(dict(nh))
        own = int(cp["own"])
        if cp.get("turning"):                      # as impact.play: their own pick; the week goes on with it
            pick = None
        else:
            pick, _ = impact.choose(policy, g, cp, prng)
        pend["p"] = dict(t=int(cp["t"]), age=round(float(cp["age"]), 2), sit=cp["sit"], own=own, pick=pick,
                         turning=bool(cp.get("turning")), s0=state(loc), opts=opts)
        g.decide(pick)
    if pend.get("p") is not None:
        info["no_end"] += 1                        # the life ended in the week of its last choice
    json.dump(dict(preset=preset, seed=seed, policy=policy, age=round(g.age(), 2), secs=round(time.time() - t0, 1),
                   n_cp=k, picks=picks, cps=cps, info=dict(info)), open(out, "w"), default=str)


# ------------------------------------------------------------------ the report
def seeds_of(s):
    out = []
    for part in str(s).split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def share(a, b):
    return f"{a / b:.3f} ({a} of {b})" if b else "- (0 of 0)"


def sign_of(x):
    return 0 if x is None or abs(x) < EPS else (1 if x > 0 else -1)


def report(lives, scope):
    L = []
    say = L.append
    n_p = sum(len(r["picks"]) for r in lives)
    n_push = sum(p["pushed"] for r in lives for p in r["picks"])
    n_turn = sum(p["turning"] for r in lives for p in r["picks"])
    info = Counter()
    for r in lives:
        info.update(r.get("info") or {})
    say(f"lives read: {len(lives)}; picks read: {n_p} ({n_push} pushed, {n_p - n_push - n_turn} their own, {n_turn} turning points)"
        f"; checkpoints {sum(r['n_cp'] for r in lives)}; picks with no week's end {info.get('no_end', 0)}"
        + (f"; acts not among the ways shown {info['act_not_shown']}" if info.get("act_not_shown") else "")
        + (f"; readings failed {info['measure_error']}" if info.get("measure_error") else "")
        + (f"; title names that are also a need, means or commitment {info['role_name_clash']}" if info.get("role_name_clash") else ""))
    for k_, v_ in info.items():
        if k_.startswith("err:"):
            say(f"      {k_[4:]} x{v_}")
    # H1a
    picks = [p for r in lives for p in r["picks"]]
    hov = [p for p in picks if "pass" in p and not p["pass"]]
    hit_in = [p for p in hov if any(in_scope(lb, scope) for _, lb, _ in p["hits"]) or p["bad"]]
    by_row, out_row, ex = Counter(), Counter(), []
    for p in hov:
        for v, lb, tx in p["hits"]:
            (by_row if in_scope(lb, scope) else out_row)[f"{lb} ({v})"] += 1
            if in_scope(lb, scope) and len(ex) < 4:
                ex.append(f"age {p['age']} {p['sit']}: {lb} ({v}): {tx[:110]}")
    n_bad = sum(1 for p in hov if p["bad"])
    h1a = len(hit_in)
    say(f"H1a hovers with a number {dict(arrows='in the arrows rows', forecast='in rows forecasting needs, means, people and titles', kinds='in rows about needs, means, people and titles', all='in any row')[scope]}"
        f" (must be 0): {h1a} of {len(hov)} hovers of the option taken; in the arrows themselves "
        f"{sum(1 for p in hov if any(lb in ARROW_ROWS for _, lb, _ in p['hits']))}; malformed arrows {n_bad}")
    if by_row:
        say("      by row: " + ", ".join(f"{k} {v}" for k, v in by_row.most_common()))
    for e in ex:
        say("      e.g. " + e)
    for p in [p for p in hov if p["bad"]][:3]:
        say(f"      malformed at age {p['age']} {p['sit']}: {p['bad'][0]}")
    if out_row:
        say("      outside the scope (information): " + ", ".join(f"{k} {v}" for k, v in out_row.most_common()))
    cw = Counter()
    for r in lives:
        for c in r["cps"]:
            cw.update(c)
    say(f"      every way shown at a card (information): {cw['ways']} ways; with a number in the arrows {cw['arrows']}, "
        f"in a row about the four kinds {cw['kinds']}, anywhere {cw['all']}")
    # H1b
    kinds, sizes, unm = Counter(), Counter(), Counter()
    for p in picks:
        for kind, nm, dr, sz, sh, tt, d, raw in p["arrows"]:
            if sh:
                kinds[kind] += 1; sizes[sz] += 1
                if tt is None:
                    unm[f"{kind}:{nm}"] += 1
    both = sum(sum((p.get("both_sides") or {}).values()) for p in picks)
    sent = sum(len(p["arrows"]) for p in picks)
    say(f"H1b arrows shown for the option taken, on the side that happened: {sum(kinds.values())}; by kind "
        f"{ {k: kinds[k] for k in KINDS if kinds[k]} }, by size {dict(sorted(sizes.items()))}; on both sides shown {both}; "
        f"sent on the side that happened (the page draws five a side) {sent}")
    if unm:
        say("      not measurable (no target found): " + ", ".join(f"{k} {v}" for k, v in unm.most_common(8)))
    # H1c
    def tally(sel, field=6):
        t = defaultdict(Counter)
        for p in picks:
            for x in p["arrows"]:
                if not sel(x) or x[5] is None:
                    continue
                kind, nm, dr, sz, sh, tt, d, raw = x
                v = x[field] if field == 6 else (raw if raw is not None else d)
                sg = sign_of(v); want = 1 if dr == "up" else -1
                res_ = "nomove" if sg == 0 else ("match" if sg == want else "miss")
                for key in ("all", f"kind {kind}", f"size {sz}", f"target {tt}"):
                    t[key][res_] += 1
        return t
    t = tally(lambda x: x[4])
    def line(key):
        c = t.get(key, Counter())
        return share(c["match"], c["match"] + c["miss"])
    nm_ = t.get("all", Counter())
    say(f"H1c arrows whose direction matched (over the arrows that moved; no move under {EPS:g} apart): overall {line('all')}"
        f"; no move {nm_['nomove']}")
    say("      by kind: " + "; ".join(f"{k} {line('kind ' + k)}" for k in KINDS if ("kind " + k) in t))
    say("      by size: " + "; ".join(f"{s} {line(f'size {s}')}" for s in (1, 2, 3) if f"size {s}" in t))
    say("      by target: " + "; ".join(f"{k[7:]} {line(k)}, no move {t[k]['nomove']}" for k in sorted(t) if k.startswith("target ")))
    ok_p = tot_p = strict_p = strict_tot = 0
    split = defaultdict(lambda: [0, 0])
    for p in picks:
        xs = [x for x in p["arrows"] if x[4] and x[5] is not None]
        mv = [x for x in xs if sign_of(x[6]) != 0]
        if xs:
            strict_tot += 1
            strict_p += all(sign_of(x[6]) == (1 if x[2] == "up" else -1) for x in xs)
        if not mv:
            continue
        tot_p += 1
        good = all(sign_of(x[6]) == (1 if x[2] == "up" else -1) for x in mv)
        ok_p += good
        g_ = "turning" if p["turning"] else "pushed" if p["pushed"] else "own"
        split[g_][0] += good; split[g_][1] += 1
    say(f"H1c picks whose moved arrows all matched: {share(ok_p, tot_p)}; by pick "
        + "; ".join(f"{k} {share(*v)}" for k, v in sorted(split.items()))
        + f"; picks with no shown arrow that moved {sum(1 for p in picks if p['arrows']) - tot_p}")
    c = t.get("all", Counter())
    say(f"      strict (no move counts as a miss): arrows {share(c['match'], sum(c.values()))}; picks {share(strict_p, strict_tot)}")
    ta = tally(lambda x: True)
    ca = ta.get("all", Counter())
    say(f"      every arrow sent, not only the five drawn: {share(ca['match'], ca['match'] + ca['miss'])}")
    tr = tally(lambda x: x[4] and x[5] == "need", field=7)
    cr = tr.get("all", Counter())
    say(f"      needs on the week's whole change after the pick instead of the act's own part (information): "
        f"{share(cr['match'], cr['match'] + cr['miss'])}, no move {cr['nomove']}")
    mis = [(p, x) for p in picks for x in p["arrows"] if x[4] and x[5] is not None and sign_of(x[6]) not in (0, 1 if x[2] == "up" else -1)]
    for p, x in mis[:6]:
        say(f"      missed: age {p['age']} {p['sit']} ({'works' if p['worked'] else 'fails'}{', pushed' if p['pushed'] else ''}): "
            f"{x[0]} {x[1]} {x[2]} {x[3]}, moved {x[6]:+.4f}")
    passed = h1a == 0 and tot_p > 0 and ok_p / tot_p >= GATE
    say(f"H1: {'PASS' if passed else 'MISS'}")
    return L, passed


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, gdir, preset, seed, policy, out, max_cp = sys.argv
        return play(gdir, preset, int(seed), policy, out, int(max_cp)) or 0
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        print(__doc__.split("\n\n")[1]); return 2
    gdir = os.path.abspath(sys.argv[1])
    a = {"presets": "1,2,3,4", "seeds": "1-2", "jobs": "2", "policy": "reader", "scope": "forecast", "out": None, "keep": None,
         "max-cp": "0"}
    args = sys.argv[2:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    if a["scope"] not in ("arrows", "forecast", "kinds", "all"):
        print("--scope is arrows, forecast, kinds or all"); return 2
    pin = os.path.join(gdir, "engine_pin")
    if not os.path.isdir(pin) or len(os.listdir(pin)) < 10:
        print(f"{pin}: not filled (chroma-game/tools/build.py pins the engine there)"); return 2
    work = os.path.abspath(a["keep"]) if a["keep"] else tempfile.mkdtemp(prefix="hover_check_")
    os.makedirs(work, exist_ok=True)
    gs = {}
    if os.environ.get("CHROMA_GAME", "").startswith("{"):
        gs = json.loads(os.environ["CHROMA_GAME"])
    gs.update(arrows=True, because=True)
    env = dict(os.environ, CHROMA_GAME=json.dumps(gs), OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    jobs = [(p, s) for p in a["presets"].split(",") for s in seeds_of(a["seeds"])]
    lines = []

    def run(j):
        p, s = j
        out = os.path.join(work, f"hover_{p}_{s}.json"); log = out[:-5] + ".log"
        t0 = time.time()
        if a["keep"] and os.path.exists(out):     # a kept life is read again, not replayed
            r = json.load(open(out)); r.setdefault("wall", 0.0)
            return r
        with open(log, "w") as lf:
            rc = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", gdir, p, str(s), a["policy"], out,
                                 a["max-cp"]],
                                env=env, stdout=lf, stderr=subprocess.STDOUT).returncode
        wall = time.time() - t0
        if rc != 0 or not os.path.exists(out):
            tail = open(log).read()[-600:]
            return dict(failed=True, preset=p, seed=s, wall=wall, tail=tail)
        r = json.load(open(out)); r["wall"] = wall
        return r

    t0 = time.time()
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(run, jobs))
    bad = [r for r in res if r.get("failed")]
    noar = [r for r in res if r.get("no_arrows")]
    lives = [r for r in res if not r.get("failed") and not r.get("no_arrows")]
    head = (f"hover_check {gdir}: presets {a['presets']}, seeds {a['seeds']}, policy {a['policy']}, scope {a['scope']}, "
            f"jobs {a['jobs']}, {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append(head)
    for r in res:
        if r.get("failed"):
            lines.append(f"preset {r['preset']} seed {r['seed']}: FAILED after {r['wall']:.0f} s\n" + r["tail"])
        elif r.get("no_arrows"):
            lines.append(f"preset {r['preset']} seed {r['seed']}: the game has no arrows switch or the engine no foresee.arrows")
        else:
            np_ = len(r["picks"]); pu = sum(p["pushed"] for p in r["picks"])
            lines.append(f"preset {r['preset']} seed {r['seed']}: age {r['age']}, {r['n_cp']} checkpoints, {np_} picks read "
                         f"({pu} pushed), {r['wall']:.0f} s wall ({r['secs']:.0f} s in the life)"
                         + (", cut short (--max-cp)" if int(a['max-cp']) and r['n_cp'] > int(a['max-cp']) else ""))
    passed = False
    if lives:
        rl, passed = report(lives, a["scope"])
        lines += rl
    lines.append(f"wall {time.time() - t0:.0f} s for {len(res)} lives on {a['jobs']} jobs")
    txt = "\n".join(lines)
    print(txt)
    if a["out"]:
        with open(a["out"], "w") as f:
            f.write(txt + "\n")
    if not a["keep"]:
        shutil.rmtree(work, ignore_errors=True)
    return 2 if bad or noar or not lives else 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
