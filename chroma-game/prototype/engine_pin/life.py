"""Simulate ONE individual life and print a readable report.

python3 life.py [seed] [framing] [want]   e.g.  python3 life.py 7 neutral W@30
want = COLOR@AGE: at that age the person resolves to become more of that color (only their wanting changes)
From code: report(seed, who=i, N=n) follows person i of a population of n (same seed = same population).
Writes life_<seed>.json with the full event log as well.
"""
import sys, json, numpy as np
from engine import *
from combos import IDEAS

def fmt(w):
    return "  ".join(f"{c} {x:.2f}" for c, x in zip(COLORS, w))

def row(v, f="{:.2f}"):
    return " | ".join(f.format(x) for x in v)

def named(label):
    key = "".join(c for c in COLORS if c in label)
    return f"{GUILD.get(label, label)}" + (f" ({IDEAS[key][1].split(':')[0]})" if key in IDEAS and len(key) > 1 else "")

def top(v, k=2):
    return ", ".join(COLORS[c] for c in np.argsort(-v)[:k])

def resolution(color, start, amount=1.5):
    def iv(t, P, nic, y):
        if t == int(start * 52):
            y[:, IDX[color]] += amount; y -= y.mean(1, keepdims=True)
    return iv

def report(seed=7, framing="mild", years=80, want=None, who=0, N=1, P=None, lib=None, title=None):
    iv = resolution(want[0], want[1]) if want else None
    o = run(N=N, seed=seed, years=years, P={"framing": framing, **(P or {})}, log_lives=(who,), intervention=iv, lib=lib)
    i = who
    ev = o["events"][i]; Wh = o["W_hist"][:, i]; Mh = o["M_hist"][:, i]; Sh = o["S_hist"][:, i]; Ah = o["A_hist"][:, i]
    V = o["V_hist"]; last = len(V["content"]) - 1
    labs = identity_path(Wh, Mh)
    out = [f"# {title or f'One life, seed {seed}'}", "",
           f"World framing: {framing}. " + ("Eras lived through: " + "; ".join(
               f"{a0 / 52:.0f} to {min(a1 / 52, years):.0f} {IDEAS[k][0]} ({IDEAS[k][1].split(':')[0]}, {kind}, strength {inten:.1f})"
               for a0, a1, k, inten, kind in o["history"]) if o["history"] else "No eras: calm times throughout.")]
    out += ["", "## Weights every five years", "",
            "| Age | Stage | W | U | B | R | G | Identity | Satisfaction | Peace |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for y in range(0, years + 1, 5):
        out.append(f"| {y} | {STAGE_NAMES[Sh[y]]} | {row(Wh[y])} | {named(labs[y]) if labs[y] else 'unformed'} | "
                   f"{V['content'][min(y, last)][i]:.2f} | {V['peace'][min(y, last)][i]:.2f} |")

    # the four color vectors (Emren's position, demand, accelerators, inertia)
    out += ["", "## Color vectors every ten years", "",
            "Position is where the person is. Demand is where they want to move (wanted minus actual). Accelerator is how fast they "
            "could move toward each color now (readiness x belief x open doors). Inertia is how strongly they hold each color above "
            "or below an even share (deep core, habit, roles). Velocity is how far each color actually moved over the past year.", "",
            "| Age | Vector | W | U | B | R | G | Notes |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for y in range(20, years, 10):
        v = color_vectors(o, i, y)
        src = v["demand_sources"]; mag = {k: 0.5 * np.abs(x).sum() for k, x in src.items()}
        main = [k for k in sorted(mag, key=lambda k: -mag[k]) if mag[k] > 0.05][:2]
        out.append(f"| {y} | position | {row(v['position'])} | {named(labs[y])} |")
        out.append(f"| | demand | {row(v['demand'], '{:+.2f}')} | strength {v['demand_strength']:.2f}; built mostly by {', '.join(main) or 'nothing much'} |")
        out.append(f"| | accelerator | {row(v['accelerator'])} | readiness {v['readiness']:.2f} |")
        out.append(f"| | inertia | {row(v['inertia'], '{:+.2f}')} | pent-up pressure {v['pressure']:.1f} of {v['threshold']:.1f} needed to break through |")
        out.append(f"| | velocity | {row(v['velocity'], '{:+.3f}')} | |")

    # satisfaction, peace, mindset, skillset
    out += ["", "## Satisfaction, peace, mindset and skillset", "",
            "Satisfaction comes from needs met (compared with what the person got used to), recent luck, and closeness to the person they "
            "want to be. Peace is disturbed by stress, by living against a commitment, by holding colors the world sees as opposed, and by "
            "pent-up wanting. Mindset is the lens (the colors the person notices) and belief in acting each way; skillset is how well each way works for them.", "",
            "| Age | Satisfaction | Peace | Needs met | Stress | Ought conflict | Color tension | Lens (top) | Belief (top) | Skill (top) |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for y in range(10, years, 10):
        m = meta(o, i, y); pp = m["parts"]
        out.append(f"| {y} | {m['satisfaction']:.2f} | {m['peace']:.2f} | {pp['needs_met']:.2f} | {pp['stress']:.2f} | {pp['ought_conflict']:.2f} | "
                   f"{pp['color_tension']:.2f} | {top(m['mindset']['lens'])} | {top(m['mindset']['belief'])} | {top(m['skillset'])} |")

    # temperament (v5): never preset, learned from the life lived
    out += ["", "## Temperament, as their life shaped it", "",
            "Nobody is born with a temperament here: everyone starts the same and these form from the life lived, fastest in "
            "childhood. Reactivity is how hard events hit (1 = average). Steadiness is how firmly they hold who they are "
            "(0 = not at all; it slows change). Baseline mood is their own usual satisfaction. Outlook is their sense of "
            "control: how often trying has worked out (it bends the odds they feel they have).", "",
            "| Age | Reactivity | Steadiness | Baseline mood | Outlook |", "| --- | --- | --- | --- | --- |"]
    for y in (5, 10, 15, 20, 30, 40, 50, 60, 70, 80):
        if y <= last:
            tp = temperament(o, i, y)
            out.append(f"| {y} | {tp['reactivity']:.2f} | {tp['steadiness']:.2f} | {tp['baseline_mood']:.2f} | {tp['outlook']:.2f} |")

    out += ["", "## What they wanted to be versus what drove them", "",
            "| Age | Wanted W | U | B | R | G | Gap |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for y in range(10, years + 1, 10):
        out.append(f"| {y} | {row(Ah[y])} | {0.5 * np.abs(Ah[y] - Wh[y]).sum():.2f} |")
    if want:
        c, a0 = IDX[want[0]], want[1]
        out += ["", f"## Resolving at {a0} to become more {want[0]}", "",
                "| Years after | Wanted " + want[0] + " | Actual " + want[0] + " |", "| --- | --- | --- |"]
        out.append(f"| before | {Ah[a0][c]:.2f} | {Wh[a0][c]:.2f} |")
        for h in (1, 2, 3, 5, 10):
            if a0 + h <= years:
                out.append(f"| {h} | {Ah[a0 + h][c]:.2f} | {Wh[a0 + h][c]:.2f} |")

    out += ["", "## The times they lived through", ""]
    eras = [e["era"] for e in ev if "era" in e]
    out += [f"- {e['age']:.0f}: an era of {e['name']} began ({e['idea']}; through {e['kind']}). "
            f"They {'embraced it' if e['took'] > 0.2 else 'pushed back against it' if e['took'] < -0.2 else 'took it in their stride'} ({e['took']:+.2f})."
            for e in eras] or ["- calm times, no eras"]

    outs = [e["outside"] for e in ev if "outside" in e and e["outside"]["took"] is not None]
    big = sorted(outs, key=lambda e: -abs(e["took"]))[:12]
    out += ["", "## What the world brought them (the twelve messages they took most strongly)", "",
            "| Age | Event | Source | Message | How they took it |", "| --- | --- | --- | --- | --- |"]
    for e in sorted(big, key=lambda e: e["age"]):
        msg = "".join(c for c, x in zip(COLORS, e["message"]) if x > 0.1)
        out.append(f"| {e['age']:.1f} | {e['name']} | {e['source']} | {msg} | "
                   f"{'embraced' if e['took'] > 0.2 else 'pushed back' if e['took'] < -0.2 else 'shrugged'} ({e['took']:+.2f}) |")
    out += ["", f"In all, {len([e for e in ev if 'outside' in e])} outside events reached them."]

    out += ["", "## Commitments", ""]
    cm = [e["commitment"] for e in ev if "commitment" in e]
    out += [f"- {c['age']:.1f}: {c['kind']} {c['what']}" + (f" through \"{c['through']}\"" if c.get("through") else "") +
            f"; it expects {top(np.array(c['profile']), 2)}" + (f" (strength {c['strength']:.2f})" if "strength" in c and c["what"] != "start" else "")
            for c in cm] or ["- none"]
    # v6: big life events at their real rates, with how the person met them and what support they had
    lev = [(t / 52, o["sit_names"][s_]) for n, t, s_ in o.get("life_events", []) if n == i]
    if lev:
        acts_by_age = {round(e["age"], 2): e for e in ev if "situation" in e}
        out += ["", "## Big life events", "", "| Age | Event | What they did | Result | Support (year after) | Satisfaction before, 1 and 3 years after |",
                "| --- | --- | --- | --- | --- | --- |"]
        for a_, nm in lev:
            e = acts_by_age.get(round(a_, 2))
            y0 = int(a_)
            sat_ = " / ".join(f"{V['content'][min(y, last)][i]:.2f}" for y in (max(y0 - 1, 0), y0 + 1, y0 + 3))
            sup_ = f"{V['support'][min(y0 + 1, last)][i]:.2f}" if "support" in V else ""
            out.append(f"| {a_:.1f} | {nm} | {e['choice'] if e else ''} | {('success' if e['success'] else 'failure') if e else ''} | {sup_} | {sat_} |")
    if o.get("goals"):   # v7: dreams, passions and plans
        out += ["", "## Dreams, passions and plans", ""]
        for g in (g for g in o["goals"] if g["life"] == i):
            ways = top(np.array(g["mix"]), 2)
            about = g["domain"] if g["domain"] != "a pursuit" else f"a pursuit in {ways} ways"
            if g.get("name"):   # the Library's concrete dream (dreams.py)
                about = f"{g['name']} ({about})"
            if g["what"] == "begins":
                src = f"sparked by {g['trigger']}" if g.get("trigger") else f"from {g['source']}"
                line = f"a {g['kind']} begins ({src}): {about}"
                if g["kind"] == "plan":
                    line += f", within {g['horizon']}, felt odds {g['felt']:.2f}"
            elif g["what"] == "became a passion":
                line = f"the dream ({about}) became a passion through {g['sealed_by']}, {'mostly harmonious' if g['harmonious'] >= 0.5 else 'mostly obsessive'} ({g['harmonious']:.2f})"
            else:
                line = f"the {g['kind']} ({about}): {g['what']}" + (f", progress {g['progress']:.2f}" if g["kind"] == "plan" else "")
            out.append(f"- {g['age']:.1f}: {line}")
    if "horizon" in V and len(V["horizon"]):
        out += ["", "## Felt horizon and discipline every ten years", "",
                "Felt horizon is how limited the person feels their time is (0 open, 1 short): age, health and deaths close by. "
                "Discipline multiplies the self-control of their life stage (1 even; learned from plans kept and broken and hard wins).", "",
                "| Age | Felt horizon | Discipline | Self-control |", "| --- | --- | --- | --- |"]
        for y in range(10, years + 1, 10):
            yy = min(y, last)
            out.append(f"| {y} | {V['horizon'][yy][i]:.2f} | {V['discipline'][yy][i]:.2f} | {V['ctrl'][yy][i]:.2f} |")
    if o.get("roles") is not None:   # titles and perks: the roles others know them by, and what they can do or reach
        R = o["roles"]; NT = R["NT"]
        rl = [e["role"] for e in ev if "role" in e]
        held_t = [R["names"][j] for j in np.nonzero(R["has"][i, :NT])[0]]
        held_p = [R["names"][NT + j] for j in np.nonzero(R["has"][i, NT:])[0]]
        out += ["", "## Titles and perks", "",
                f"At the end: {', '.join(held_t) or 'no titles'}; perks: {', '.join(held_p) or 'none'}. "
                f"Over the life {int(R['ever'][i, :NT].sum())} titles and {int(R['ever'][i, NT:].sum())} perks.", "",
                "| Age | | Title or perk | Kind | How |", "| --- | --- | --- | --- | --- |"]
        out += [f"| {r['age']:.1f} | {r['what']} | {r['name']} | {r['kind']} | {r['how']} |" for r in rl] or ["| | | none | | |"]
    out += ["", "## Clashes with a commitment, and how they ended", ""]
    out += [f"- {c['kind']}: from {c['start']:.1f} to {c['end']:.1f}, {c['how']}" for c in (e["clash"] for e in ev if "clash" in e)] or ["- none"]
    if lib is not None and "src" in lib:   # a Library batch: inner moments, echoes, marks, deaths, outside events as read
        from collections import Counter
        tier = {nm: s_.get("tier", "everyday") for nm, s_ in zip(lib["names"], lib["src"])}
        inner = [e for e in ev if "situation" in e and tier.get(e["situation"]) in ("inner", "echo")]
        out += ["", "## Inner moments and echoes", "", "| Age | Moment | Kind | What they did | Result |", "| --- | --- | --- | --- | --- |"]
        out += [f"| {e['age']:.1f} | {e['situation']} | {tier[e['situation']]} | {e['choice']} | {'worked' if e['success'] else 'did not work'} |"
                for e in inner] or ["| | none | | | |"]
        marks = Counter(e["mark"]["mark"] for e in ev if "mark" in e)
        out += ["", "## Marks their acts left (echoes read them years later)", ""] + ([f"- {m}: {n}" for m, n in marks.most_common()] or ["- none"])
        out += ["", "## People close to them who died", ""] + ([f"- {d['age']:.1f}: a {d['role']}" for d in (e["death"] for e in ev if "death" in e)] or ["- none"])
        reads = [e["read"] for e in ev if "read" in e]
        out += ["", f"## Outside events as they read them ({len(reads)} in all; the first 25)", "", "| Age | Event | Their reading |", "| --- | --- | --- |"]
        out += [f"| {r['age']:.1f} | {r['name']} | {r['reading']} |" for r in reads[:25]]
    open_cl = [(KNAMES[kk], t0 / 52) for n, kk, t0, t1, how, *_ in o["clashes"] if n == i and how == "still living with it"]
    out += [f"- {k}: from {a:.1f}, still living with it at the end" for k, a in open_cl]

    out += ["", "## Breakthroughs (pent-up wanting overcoming inertia)", ""]
    out += [f"- {b['age']:.1f}: gap {b['gap']:.2f}, holding {b['hold']:.2f}. Weights {fmt(b['before'])} became {fmt(b['w'])}"
            for b in (e["breakthrough"] for e in ev if "breakthrough" in e)] or ["- none"]
    out += ["", "## Rites of passage", ""]
    for e in ev:
        if "rite" in e:
            r = e["rite"]
            out.append(f"- {r['age']:.1f}: became {r['to']}" + (" quietly" if r["quiet"] else f" through {r['event']}") + f". Weights then: {fmt(r['w'])}")
    out += ["", "## Conversions (an identity crisis that disowns a color)", ""]
    cs = [e["conversion"] for e in ev if "conversion" in e]
    out += [f"- {c['age']:.1f}: disowned {c['disowned']}; weight went toward " +
            ", ".join(f"{COLORS[j]} {q:.2f}" for j, q in enumerate(c["toward"]) if q > 0.05) + f". Weights after: {fmt(c['w'])}" for c in cs] or ["- none"]
    acts = [e for e in ev if "push" in e]
    for e in acts:
        e["size"] = float(np.abs(np.array(list(e["push"].values()))).sum())
    topa = sorted(acts, key=lambda e: -e["size"])[:10]
    out += ["", "## Ten most formative choices", "", "| Age | Situation | Choice | Result | Biggest push |", "| --- | --- | --- | --- | --- |"]
    for e in sorted(topa, key=lambda e: e["age"]):
        tot = np.sum([np.array(v) for v in e["push"].values()], 0)
        up, dn = COLORS[int(np.argmax(tot))], COLORS[int(np.argmin(tot))]
        main = max(e["push"], key=lambda ch: np.abs(e["push"][ch]).sum())
        out.append(f"| {e['age']:.1f} | {e['situation']} | {e['choice']} | {'success' if e['success'] else 'failure'} | {up} up, {dn} down ({main}) |")
    ch = o["chan"][i]
    out += ["", "## Why the weights moved (sum of pushes over the life, log-ratio units)", "",
            "| Channel | " + " | ".join(COLORS) + " |", "| --- |" + " --- |" * 5]
    for j, name in enumerate(CHANNELS):
        out.append(f"| {name} | " + " | ".join(f"{x:+.2f}" for x in ch[j]) + " |")
    asrc = o["A_src"][-1][i]
    out += ["", "## What moved the want (sum over the life, log-ratio units)", "",
            "| Source | " + " | ".join(COLORS) + " |", "| --- |" + " --- |" * 5]
    for j, name in enumerate(ASOURCES):
        if np.abs(asrc[j]).sum() > 0.01:
            out.append(f"| {name} | " + " | ".join(f"{x:+.2f}" for x in asrc[j]) + " |")
    json.dump(dict(seed=seed, who=who, N=N, framing=framing, events=ev), open(f"life_{seed}" + (f"_{who}" if N > 1 else "") + ".json", "w"), default=float)
    return "\n".join(out)

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    framing = sys.argv[2] if len(sys.argv) > 2 else "mild"
    args = [x for x in sys.argv[3:] if x != "earth" and not x.startswith("roles=")]
    want = (args[0].split("@")[0], int(args[0].split("@")[1])) if args else None
    lib = None
    if "earth" in sys.argv[3:]:   # python3 life.py 7 mild earth: a life in the Library's modern Earth batch
        from batch import load_batch
        lib = load_batch("earth", roles=next((x.split("=", 1)[1] for x in sys.argv[3:] if x.startswith("roles=")), None))
    print(report(seed, framing, want=want, lib=lib))
