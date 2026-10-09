"""Steered lives: whole lives set up through the page's own bridge (console.Console, as web/worker.js runs it), then
played on the Game object with a scripted player, as the update's stage 1 checks need (Release's steered rows;
chroma-ideas/gameplay-feel.md §5.2, voice-mechanics.md §9). Two forms:

    python3 -B test/steer_check.py <target> [<target> ...|all]    Release's steered rows (below); the lives they need run
                                                                  once, on every core, shared between targets and kept in
                                                                  $STEER_CACHE (default /tmp/steer_cache) by preset, seed,
                                                                  player, stop age, settings and game.py; each target ends
                                                                  with "STEER <target>: PASS" (or MISS) under its numbers
    python3 -B test/steer_check.py <preset 1-6> <seed> <player> <out.json>     one life, its JSON record (calibration)

players:
  let          always lets them choose
  most:<C>     always pushes the open option with the most of color C in its ways (W U B R G); their own pick when it is
               already that option
  careful      always pushes the open option that leans most to safety (security vs freedom), when it leans more than
               their own
  random       a random option with ways, from the seed
  light:<C>    a light steer toward color C at every moment (P3): their own pick, tilted
Settings to try go in CHROMA_GAME as JSON (for example CHROMA_GAME='{"piv": 0.1}'), or "off" for stage 1's rules off
(game.GAME_OFF); game.py reads it when it loads.

targets (all on preset 1, modern Earth; whole lives come from one shared set: let 1-6, most:<C by seed> 1-6, random
1-2, careful 1-2):
  identity      steering one color at most picks puts it in the name at 40 in most lives, for each color (most:<C>,
                3 seeds, to 41): at least 2 of 3 for every color
  apart         the same life steered two ways (most:W, most:B) ends further apart at 60 than two different lives left
                alone (3 seeds; half the summed color gap)
  alone_names   a life left alone changes its shown name at most 3 to 4 times after 18 (6 seeds; mean at most 4)
  push_rare     pushed lives (most:<C>, C = WUBRG[seed % 5]) meet more rare moments (under 1 life in 10) than the same lives left
                alone (6 seeds; summed)
  world_lines   every world line (WL1) is an effect the engine reported for the character that year (STATE wfx, kept in
                the record of what the times did), and every year's line (WL4) falls in a year with such effects
  voice_quiet   always letting them choose: "a quiet voice" and no voice lines
  voice_careful always the careful pick: the voice named for safety ("the careful voice", or "the timid voice" when
                they doubt it) at the end of every life and at two moments in three once it has a name (a pure White pick
                stands at the safety pole and at three others too, so the first named moments can go to a neighbour)
  voice_trust   trust in a push's colors does better after steered picks that work than after ones that fail, and falls
                after failures (P2 as built: a push that worked but fed no need they lacked while reluctant is resented;
                read agreed 2026-10-09)
  voice_lines   every voice line (story lines, answers, outcomes) at most 25 words, with no color named
  voice_year    each year's chapter keeps at most one voice line
"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np

CI = {x: i for i, x in enumerate("WUBRG")}
COLOR_WORDS = ("White", "Blue", "Black", "Red", "Green")


def play(preset, seed, player, until=None):
    """One life with a scripted player; returns its record."""
    random.seed(seed)
    from console import Console
    import game as G
    try:
        from rarity import RARITY
    except Exception:
        RARITY = {}
    share = lambda sit: (RARITY.get("sit") or {}).get(sit)
    c = Console()
    c.handle(""); c.handle(str(preset)); c.handle("Ari")
    g = c.g
    prng = np.random.default_rng(seed + 31)
    asked, pushes, vnames = [], [], []
    tr_before = None
    while True:
        r = g.advance(until_age=until) if until else g.advance()
        if r == "resolved" and asked and g.resolution:  # what came of the last pick (told at the end of its week)
            res = g.resolution
            asked[-1].update(ok=bool(res.get("worked")), pivot=(res.get("pivot") or {}).get("kind"),
                             hind=(res.get("hindsight") or {}).get("kind"))
            v = res.get("voice") or {}
            asked[-1].update(answer=v.get("answer") or "", outcome=v.get("outcome") or "")
            if tr_before is not None and asked[-1].get("pushed"):
                t1 = g.trust_view()
                cols = [x for x in asked[-1]["colors"] if x in CI]
                if cols:
                    pushes.append(dict(ok=bool(res.get("worked")), d=float(np.mean([t1[x] - tr_before[x] for x in cols]))))
            tr_before = None
        if r in ("over", "paused") or g.over:
            break
        if r != "checkpoint":
            continue
        cp = g.pending; loc = g.loc
        if hasattr(g, "voice_name"):
            vnames.append((round(cp["age"], 2), g.voice_name(), g.history.get("voice", {}).get("steer", 0)))
        m = np.maximum(np.asarray(loc["m"][0], float), 0)
        opts = [o for o in cp["options"] if o["colors"] != "-" and m[o["idx"]].sum() > 0 and o.get("status") != "out of reach"]
        own = int(cp["own"])
        cv = lambda k: m[k] / m[k].sum() if m[k].sum() > 0 else np.full(5, 0.2)
        tr_before = g.trust_view() if hasattr(g, "trust_view") else None
        if player.startswith("light:"):
            g.decide(None, light=player[6:])
            f = g._force or {}
            asked.append(dict(age=round(cp["age"], 2), sit=cp["sit"], share=share(cp["sit"]), own=not f, pushed=bool(f),
                              light=(f.get("light") or {}).get("share"), colors=cp["by_idx"][f.get("idx", own)]["colors"]))
            continue
        pick = None
        if player.startswith("most:") and opts:
            ci = CI[player[5:]]
            pick = max(opts, key=lambda o: (cv(o["idx"])[ci], o["idx"] == own))["idx"]
        elif player == "careful" and opts:
            safe = np.array([1, 1, -1, -1, 0], float)          # security vs freedom (engine AXES)
            best = max(opts, key=lambda o: (float(safe @ cv(o["idx"])), o["idx"] == own))
            if float(safe @ cv(best["idx"])) > float(safe @ cv(own)) + 1e-9:
                pick = best["idx"]
        elif player == "random" and opts:
            pick = opts[int(prng.integers(len(opts)))]["idx"]
        pushed = pick is not None and pick != own
        asked.append(dict(age=round(cp["age"], 2), sit=cp["sit"], share=share(cp["sit"]), own=not pushed, pushed=pushed,
                          colors=cp["by_idx"][own if pick is None else pick]["colors"]))
        g.decide(pick)
    h = g.history
    feed = [dict(tag=x.get("tag"), age=x.get("age"), text=x.get("text") or "", chapter=x.get("chapter"))
            for x in g.feed if x.get("tag") in ("voice", "world_fx", "world_year")]
    return G.clean(dict(preset=preset, seed=seed, player=player, age=round(g.age(), 2), game=os.environ.get("CHROMA_GAME", ""),
                        w=h["w"], label=h["label"], name=h.get("name", []), asked=asked, pivots=h.get("pivots", []),
                        forced=h["forced"], own=h["own"], accepted=h.get("accepted", 0), resented=h.get("resented", 0),
                        trust=g.trust_view() if hasattr(g, "trust_view") else None,
                        voice=g.voice_view() if hasattr(g, "voice_view") else None, light=h.get("light", 0),
                        review_voice=(getattr(g, "review", None) or {}).get("voice"), feed=feed, times=h.get("times", []),
                        pushes=pushes, vnames=vnames))


def _key(a):
    import hashlib
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = hashlib.md5(open(os.path.join(here, "game.py"), "rb").read()).hexdigest()[:12]
    st = hashlib.md5(os.environ.get("CHROMA_GAME", "").encode()).hexdigest()[:8]
    return f"{a[0]}_{a[1]}_{a[2].replace(':', '')}_{a[3] or 'end'}_{st}_{src}.json"


def _job(a):
    d = os.environ.get("STEER_CACHE", "/tmp/steer_cache")
    f = os.path.join(d, _key(a))
    try:
        return json.load(open(f))
    except Exception:
        pass
    r = play(*a)
    try:
        os.makedirs(d, exist_ok=True)
        json.dump(r, open(f + ".tmp", "w")); os.replace(f + ".tmp", f)
    except Exception:
        pass
    return r


def run(jobs):
    """The lives, each once, from the cache when there; returns {job: record}."""
    from multiprocessing import Pool
    jobs = sorted(set(jobs), key=lambda a: (a[3] is not None, a))      # whole lives first: they take longest
    with Pool(max(1, min(len(jobs), os.cpu_count() or 2))) as p:
        return dict(zip(jobs, p.map(_job, jobs)))


MOST = lambda s: "most:" + "WUBRG"[s % 5]
LET = [(1, s, "let", None) for s in range(1, 7)]
PUSHED = [(1, s, MOST(s), None) for s in range(1, 7)]
RANDOM = [(1, s, "random", None) for s in (1, 2)]
NEEDS = {
    "identity": [(1, s, f"most:{c}", 41) for c in "WUBRG" for s in (1, 2, 3)],
    "apart": [(1, s, p, 61) for s in (1, 2, 3) for p in ("most:W", "most:B")] + LET[:3],
    "alone_names": LET, "push_rare": LET + PUSHED, "world_lines": LET[:2] + RANDOM, "voice_quiet": LET[:2],
    "voice_careful": [(1, s, "careful", None) for s in (1, 2)],
    "voice_trust": RANDOM + PUSHED[:2], "voice_lines": RANDOM + PUSHED[:2], "voice_year": RANDOM + PUSHED[:2],
}


def w_at(r, age):
    for a, w in r["w"]:
        if int(a) == age:
            return np.asarray(w, float)
    return np.asarray(r["w"][-1][1], float)


def name_at(r, age):
    out = ""
    for a, l, *_ in r["name"]:
        if a <= age + 0.5:
            out = l
    return out


def name_changes(r, after=18):
    n = r["name"]
    return sum(1 for i in range(1, len(n)) if n[i][0] >= after and n[i][1] != n[i - 1][1])


def rare(r):
    return sum(1 for a in r["asked"] if a.get("share") is not None and a["share"] < 0.1)


def voice_texts(r):
    return [x["text"] for x in r["feed"] if x["tag"] == "voice"] + \
           [s for a in r["asked"] for s in (a.get("answer"), a.get("outcome")) if s]


def target(t, R):
    ok, say = False, print
    rs = [R[a] for a in NEEDS[t]]
    if t == "identity":
        held = {c: sum(1 for r in rs if r["player"] == f"most:{c}" and c in name_at(r, 40)) for c in "WUBRG"}
        for c in "WUBRG":
            say(f"most:{c}: holds {c} in the name at 40 in {held[c]} of 3 ({', '.join(name_at(r, 40) or '-' for r in rs if r['player'] == f'most:{c}')})")
        ok = all(v >= 2 for v in held.values())
    elif t == "apart":
        by = {(r["seed"], r["player"]): w_at(r, 60) for r in rs}
        steer = [0.5 * np.abs(by[(s, "most:W")] - by[(s, "most:B")]).sum() for s in (1, 2, 3)]
        diff = [0.5 * np.abs(by[(a, "let")] - by[(b, "let")]).sum() for a, b in ((1, 2), (1, 3), (2, 3))]
        say(f"same life steered W and B, gap at 60: {' '.join(f'{x:.3f}' for x in steer)} (mean {np.mean(steer):.3f})")
        say(f"different lives left alone, gap at 60: {' '.join(f'{x:.3f}' for x in diff)} (mean {np.mean(diff):.3f})")
        ok = np.mean(steer) > np.mean(diff)
    elif t == "alone_names":
        ch = [name_changes(r) for r in rs]
        say(f"shown name changes after 18, left alone: {ch} (mean {np.mean(ch):.1f})")
        ok = np.mean(ch) <= 4
    elif t == "push_rare":
        a = [rare(r) for r in rs if r["player"] == "let"]; b = [rare(r) for r in rs if r["player"] != "let"]
        say(f"rare moments met, left alone: {a} (sum {sum(a)}); pushed: {b} (sum {sum(b)})")
        ok = sum(b) > sum(a)
    elif t == "world_lines":
        bad, n, ny, bady = [], 0, 0, []
        for r in rs:
            yrs = {int(x["age"]) for x in r["times"]}
            for x in r["feed"]:
                if x["tag"] == "world_fx":
                    n += 1
                    if not any(abs(y["age"] - x["age"]) <= 0.1 and y.get("told", True) for y in r["times"]):
                        bad.append((r["seed"], x["age"], x["text"][:60]))
                elif x["tag"] == "world_year":
                    ny += 1
                    if not ({int(x["age"]) - 1, int(x["age"])} & yrs):
                        bady.append((r["seed"], x["age"], x["text"][:60]))
        say(f"world lines {n}, without an engine effect {len(bad)}; year lines {ny}, in a year without effects {len(bady)}")
        for b in (bad + bady)[:5]:
            say("  " + str(b))
        ok = n > 0 and not bad and not bady
    elif t == "voice_quiet":
        names = sorted({v[1] for r in rs for v in r["vnames"] if v[0] >= 30})
        lines = [x for r in rs for x in voice_texts(r)]
        say(f"voice names after 30: {names}; voice lines {len(lines)}")
        for x in lines[:3]:
            say("  " + x)
        ok = names == ["a quiet voice"] and not lines
    elif t == "voice_careful":
        SAFE = ("the careful voice", "the timid voice")
        named = [v[1] for r in rs for v in r["vnames"] if v[2] >= 5]
        other = sorted({x for x in named if x not in SAFE})
        last = [r["voice"]["name"] for r in rs]
        share_ = sum(1 for x in named if x in SAFE) / max(1, len(named))
        say(f"moments with a named voice: {len(named)}, named for safety at {share_:.0%}; named otherwise: {other or 'none'}; "
            f"at the end: {last}")
        ok = bool(named) and all(x in SAFE for x in last) and share_ >= 2 / 3
    elif t == "voice_trust":
        up = [p["d"] for r in rs for p in r["pushes"] if p["ok"]]; dn = [p["d"] for r in rs for p in r["pushes"] if not p["ok"]]
        say(f"trust change in the push's colors: worked {len(up)} pushes, mean {np.mean(up) if up else 0:+.4f}; "
            f"failed {len(dn)}, mean {np.mean(dn) if dn else 0:+.4f}")
        ok = bool(up) and bool(dn) and np.mean(up) > np.mean(dn) and np.mean(dn) < 0
    elif t == "voice_lines":
        lines = [x for r in rs for x in voice_texts(r)]
        long_ = [x for x in lines if len(x.split()) > 25]
        col = [x for x in lines if any(w in x for w in COLOR_WORDS)]
        say(f"voice lines {len(lines)}; over 25 words {len(long_)}; naming a color {len(col)}")
        for x in (long_ + col)[:5]:
            say("  " + x)
        ok = bool(lines) and not long_ and not col
    elif t == "voice_year":
        worst = 0; where = None
        for r in rs:
            per = {}
            for x in r["feed"]:
                if x["tag"] == "voice":
                    per[int(x["age"])] = per.get(int(x["age"]), 0) + 1
            if per and max(per.values()) > worst:
                worst = max(per.values()); where = (r["seed"], r["player"], max(per, key=per.get))
        say(f"most voice lines in one year's chapter: {worst} {where or ''}")
        ok = worst <= 1
    say(f"STEER {t}: {'PASS' if ok else 'MISS'}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        ts = list(NEEDS) if sys.argv[1:] == ["all"] else sys.argv[1:]
        bad = [t for t in ts if t not in NEEDS]
        if bad or not ts:
            sys.exit(f"unknown target {' '.join(bad)}; targets: {' '.join(NEEDS)} (or all)")
        R = run([a for t in ts for a in NEEDS[t]])
        for t in ts:
            print(f"== {t}")
            target(t, R)
    else:
        preset, seed, player, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
        rec = play(preset, seed, player)
        json.dump(rec, open(out, "w"))
        print(preset, seed, player, "age", rec["age"], "asked", len(rec["asked"]), "pushed", rec["forced"])
