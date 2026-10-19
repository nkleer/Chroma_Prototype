"""Bold ways (GAME bold, with the Engine's bold_play): the game's proof rows B3 to B5, B9 and B10 (chroma-ideas/gameplay-
2026-10-17/bold-ways.md, Release bar). Whole Earth lives played with bold on, a card alternately left to them, pushed to
a bold way and pushed to the bold way's ordinary base way.

    python3 -B test/bold_check.py [--presets 1,2,3,4] [--seeds 1-6] [--jobs 4] [--mock]

    B3   life-event asks that carry a bold way (bar: 90% or more); the colours of the bold ways offered (each 20% +- 4
         points) and their mean written chance per colour (within +- 3 points of the mean)
    B4   bold tries that worked against the Engine's own mean odds for them, pooled (+- 5 points); at an ordinary start
         (preset 1) the Engine's odds against the card's written chance (+- 5 points)
    B5   every bold outcome left what the card stated (a win's title or perk gained, a failure's cost) and nothing
         lasting it did not state (titles and perks gained or lost through it)
    B9   every link follows its own try's side (a win link only after a win), one to three years after it (plus a
         season), at most 6 a life; asks a life (Release compares them with main's plus 5%)
    B10  "likelier" and "harder for them" true: shown exactly when their own odds sit 10 points or more from the written
         chance

--mock plays the hand-over with a stand-in for the Engine (two bold ways on the first two seen ways, its own pick bold
one year in three): only the game's plumbing, for the time before the Engine's bold_play is in; its B4 and B5 mean
nothing. Each life runs in its own process. Prints one line per life, then the rows with their bars; exit 0 when the
counts were made (the bars are Release's), 2 when the engine has no bold_play and --mock was not given."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)
ON = {"bold": True}


def mock(game):
    """The Engine's hand-over, played by a stand-in (see --mock)."""
    import numpy as np
    from game_bold import BoldMixin
    BoldMixin._bold_on = lambda self, loc: loc is not None and "P" in loc
    def choose(self, loc):
        self._bold_now, self._bold_pick = [], -1
        if self._bold_t is None or self._bold_t[0] != int(self.t):
            return
        ok = np.asarray(loc["mask"][0], bool) & ~np.asarray(loc["do_nothing"][0], bool) & np.asarray(loc["seen"][0], bool)
        ks = [int(k) for k in np.nonzero(ok)[0][:2]]
        s = int(loc["s"][0])
        self._bold_now = [dict(row=-1, base=k, label="go all in: " + loc["L"]["labels"][s][k], chance=0.35, p=0.3 + 0.12 * j)
                          for j, k in enumerate(ks)]
        self._bold_pick = 0 if ks and (int(self.t) // 52) % 3 == 0 else -1
        loc["P"]["bold_take"] = self._bold_pick
    BoldMixin._bold_choose = choose


def play(preset, seed, out, use_mock):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import numpy as np
    import game
    if use_mock:
        mock(game)
    elif "bold_play" not in game.E.DEFAULT:
        json.dump(dict(no_engine=True), open(out, "w"))
        return
    p = {k: v for k, v in game.PRESETS[preset].items() if k not in ("title", "blurb")}
    g = game.Game(name="Ari", seed=seed, **p)
    life_asks, offered, fits, asks, k = [], [], [], 0, 0
    while not g.over and k < 3000:
        if g.advance() != "checkpoint":
            continue
        cp = g.pending; loc = g.loc; asks += 1; k += 1
        life = ("had_ev" in loc and bool(np.asarray(loc["had_ev"]).ravel()[0])
                and int(np.asarray(loc["s_ev"]).ravel()[0]) == int(cp["s"]) and not cp.get("turning") and not cp["recon"])
        bold = [o for o in cp["options"] if o.get("bold")]
        if life:
            life_asks.append(bool(bold))
        for o in bold:
            offered.append(dict(c=o["colors"], chance=o["bold"]["chance"], p=o["bold"]["p"]))
            fits.append(dict(p=o["bold"]["p"], chance=o["bold"]["chance"], fit=o["bold"]["fit"]))
        pick = None
        if bold and k % 3 == 1:
            pick = bold[k % len(bold)]["idx"]
        elif bold and k % 3 == 2:
            pick = bold[0]["bold"]["base"]
        if cp.get("turning"):
            pick = None
        g.decide(pick)
    links = [x for x in g.history.get("bold", []) if x.get("link")]
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 1), asks=asks, life_asks=life_asks, offered=offered, fits=fits,
                   tries=g.history.get("bold", []), links=len(links)), open(out, "w"), default=str)


def run(preset, seed, out, use_mock):
    env = dict(os.environ, CHROMA_GAME=json.dumps(ON))
    subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), out, "1" if use_mock else "0"],
                   env=env, check=True, cwd=GAME_DIR)
    return json.load(open(out))


def seeds_of(txt):
    a, _, b = txt.partition("-")
    return list(range(int(a), int(b or a) + 1))


def rows(lives):
    out = []
    la = [x for l in lives for x in l["life_asks"]]
    out.append(f"B3  life-event asks with a bold way: {sum(la)} of {len(la)} ({100 * sum(la) / max(len(la), 1):.0f}%; bar 90%)")
    off = [x for l in lives for x in l["offered"]]
    if off:
        cols = {}
        for x in off:
            for c in x["c"].replace(">", "+").split("+")[:1]:
                cols.setdefault(c, []).append(x["chance"])
        mean = sum(x["chance"] for x in off) / len(off)
        out.append("    colours: " + ", ".join(f"{c} {100 * len(v) / len(off):.0f}% (chance {100 * sum(v) / len(v):.0f}%)"
                                         for c, v in sorted(cols.items())) + f"; mean chance {100 * mean:.0f}% (bar: each 20% +- 4, chance +- 3)")
    tries = [t for l in lives for t in l["tries"]]
    if tries:
        won = sum(t["ok"] for t in tries) / len(tries); mp = sum(t["p"] for t in tries) / len(tries)
        out.append(f"B4  bold tries {len(tries)}: worked {100 * won:.1f}% against the Engine's mean odds {100 * mp:.1f}% (bar +- 5 points)")
        p1 = [x for l in lives if l["preset"] == "1" for x in l["offered"]]
        if p1:
            d = sum(x["p"] - x["chance"] for x in p1) / len(p1)
            out.append(f"    preset 1: own odds minus written chance {100 * d:+.1f} points over {len(p1)} offers (bar +- 5)")
    bad5 = []
    for t in tries:
        st = t.get("stated") or {}
        ch = t.get("changed") or []
        said = {str(n) for f_, n in (st.get("win") or []) + (st.get("cost") or [])}
        kinds = {n[5:] for n in said if n.startswith("kind:")}     # drops_if_fails kind:<kind>: whatever title of that kind
        want = {str(n) for f_, n in (st.get("win") if t["ok"] else st.get("cost")) or ()
                if f_ != "break" and not str(n).startswith("kind:")}
        got = {c["name"] for c in ch}
        extra = {c["name"] for c in ch if c["name"] not in said and not (c["what"] == "lost" and c.get("kind") in kinds)}
        if want - got or extra:
            bad5.append(f"{t['moment']} at {t['age']}: stated {sorted(want)}, changed {sorted(got)}")
    out.append(f"B5  bold outcomes that left what the card said and nothing else: {len(tries) - len(bad5)} of {len(tries)}"
               + ("".join("\n      " + b for b in bad5[:8])))
    bad9, n_links = [], 0
    for l in lives:
        for t in l["tries"]:
            ln = t.get("link")
            if not ln:
                continue
            n_links += 1
            side = "well" if t["ok"] else "badly"
            if ln.get("side") not in (None, side) or not (1.0 - 0.01 <= ln["age"] - t["age"] <= 3.25):
                bad9.append(f"{t['moment']} at {t['age']} ({side}) -> {ln['moment']} at {ln['age']} ({ln.get('side')})")
        if l["links"] > 6:
            bad9.append(f"preset {l['preset']} seed {l['seed']}: {l['links']} links")
    asks = [l["asks"] for l in lives]
    out.append(f"B9  links {n_links}, wrong side, delay or count: {len(bad9)}; asks a life {sum(asks) / max(len(asks), 1):.1f} "
               "(Release: main's plus 5% at most)" + "".join("\n      " + b for b in bad9[:8]))
    fits = [x for l in lives for x in l["fits"]]
    bad10 = [x for x in fits if (x["fit"] is not None) != (abs(x["p"] - x["chance"]) >= 0.10 - 1e-9)
             or (x["fit"] == "likelier") != (x["fit"] is not None and x["p"] > x["chance"])]
    out.append(f"B10 fit hints true: {len(fits) - len(bad10)} of {len(fits)} (shown {sum(x['fit'] is not None for x in fits)})")
    return out


def main(argv):
    if argv[:1] == ["_play"]:
        return play(argv[1], int(argv[2]), argv[3], argv[4] == "1")
    a = {"presets": "1,2,3,4", "seeds": "1-6", "jobs": "4"}
    for k in a:
        if "--" + k in argv:
            a[k] = argv[argv.index("--" + k) + 1]
    use_mock = "--mock" in argv
    sys.path.insert(0, HERE)
    from pinned import ensure
    ensure(GAME_DIR)
    import tempfile
    tmp = tempfile.mkdtemp(prefix="bold_check_")
    jobs = [(p, s, os.path.join(tmp, f"{p}_{s}.json")) for p in a["presets"].split(",") for s in seeds_of(a["seeds"])]
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        lives = list(ex.map(lambda j: run(*j, use_mock), jobs))
    if any(l.get("no_engine") for l in lives):
        print("STOP: this engine has no bold_play (the Engine's part); --mock plays the game's plumbing with a stand-in")
        return 2
    for l in lives:
        print(f"preset {l['preset']} seed {l['seed']}: age {l['age']}, {l['asks']} asks, {sum(l['life_asks'])} of "
              f"{len(l['life_asks'])} life-event asks bold, {len(l['tries'])} bold tries, {l['links']} links")
    print("\n".join(rows(lives)) + ("\n(--mock: the Engine's part is a stand-in; B4 and B5 mean nothing)" if use_mock else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
