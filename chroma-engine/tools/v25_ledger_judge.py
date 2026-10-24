"""The judge for v25_ledger_run.py's files (Release's records/v25/checks.md): one line a row, PASS, FAIL or INCONCLUSIVE
with its numbers, then the detail.

    python3 -B chroma-engine/tools/v25_ledger_judge.py <LA files ...> [--base <LB files ...>] [--nat <nat-test files ...>]
        [--sk <SK files ...>] [--json out.json]

Mandatory: CL0, AM0 (LA's part: SC1 holds the save, load and queue cases, SK's lives are the game's), NR1 (LA's lives,
then the --nat-test lives as the targeted test). Read beside them: CL1, CL3, AM2, F5, WA8n's rates, RE3 (with --base).
--sk: played lives (v25_ledger_hook.record from heights_play.py, one life a file), read for CL0 and AM0 only, as their own
rows (CL0sk, AM0sk) under their own head line; never pooled with LA. SK files alone are enough.
"""
import json
import sys

import numpy as np

COL = "WUBRG"
args = sys.argv[1:]
groups = {"la": [], "base": [], "nat": [], "sk": []}; cur = "la"; jout = None
i = 0
while i < len(args):
    a = args[i]
    if a == "--base":
        cur = "base"
    elif a == "--nat":
        cur = "nat"
    elif a == "--sk":
        cur = "sk"
    elif a == "--json":
        jout = args[i + 1]; i += 1
    else:
        groups[cur].append(a)
    i += 1
if not groups["la"] and not groups["sk"]:
    sys.exit(__doc__)
LA = [json.load(open(p, encoding="utf-8")) for p in groups["la"]]
LB = [json.load(open(p, encoding="utf-8")) for p in groups["base"]]
NT = [json.load(open(p, encoding="utf-8")) for p in groups["nat"]]
SK = [json.load(open(p, encoding="utf-8")) for p in groups["sk"]]
if any("base" in x or "nat_test" in x for x in SK) or any("base" not in x for x in LA + LB + NT) or \
        any(x["base"] or x["nat_test"] for x in LA) or any(not x["base"] for x in LB) or any(not x["nat_test"] for x in NT):
    sys.exit("a file is in the wrong group (LA files are the shipped set, --base files are --base runs, --nat files --nat-test)")
lines, detail, out = [], [], {}


def say(row, verdict, text):
    lines.append(f"{row:5s} {verdict:12s} {text}"); out[row] = dict(verdict=verdict, text=text)


def viol(files, row):
    n = {}; first = []
    for x in files:
        for k, c in x["violation_counts"].items():
            if k.startswith(row + "|"):
                n[k.split("|", 1)[1]] = n.get(k.split("|", 1)[1], 0) + c
        first += [dict(v, seed=x.get("seed")) for v in x["violations"] if v["row"] == row]
    return n, first


def logic(X, tag=""):
    """CL0 and AM0 over the files X (LA's, or SK's with tag "sk")."""
    # ---- CL0
    cnt = {k: sum(x["counts"][k] for x in X) for k in X[0]["counts"]}
    n_, first = viol(X, "CL0")
    st = {}
    for x in X:
        for k, v in (x["clash"]["stats"] or {}).items():
            if isinstance(v, (int, float)):
                st[k] = st.get(k, 0) + v
    nums = (f"{cnt['puts']} clashes put, {cnt['answered']} answered, {sum(x['clash']['unanswered_at_end'] for x in X)} open at the end; "
            f"{cnt['merged_pairs']} connected pairs in one week; ceilings held {int(st.get('ceiling', 0))}, unchanged held "
            f"{int(st.get('repeat_held', 0))}, colour without stakes (never a clash) {int(st.get('by_colour_only', 0))}")
    if n_:
        say("CL0" + tag, "FAIL", f"{sum(n_.values())} breaks: " + "; ".join(f"{k} {v}" for k, v in n_.items()) + f". {nums}")
        detail.append(("CL0" + tag + " first breaks", first[:10]))
    elif cnt["puts"] == 0:
        say("CL0" + tag, "INCONCLUSIVE", "no clash was put in these lives")
    else:
        say("CL0" + tag, "PASS", nums)

    # ---- AM0
    n_, first = viol(X, "AM0")
    arr = sum(len(x["aims2"]["arrivals"]) for x in X)
    nums = (f"{cnt['arrived']} rungs reached ({cnt['deadline_week']} in a window's closing week, counted), {cnt['paused_close']} windows "
            f"closed while paused, {sum(x['aims2']['decisions'] or 0 for x in X)} forks decided by the lives' own pick; the save, load "
            f"and queue cases are SC1's, SK's lives the game's")
    if n_:
        say("AM0" + tag, "FAIL", f"{sum(n_.values())} breaks: " + "; ".join(f"{k} {v}" for k, v in n_.items()) + f". {nums}")
        detail.append(("AM0" + tag + " first breaks", first[:10]))
    else:
        say("AM0" + tag, "INCONCLUSIVE" if not cnt["arrived"] and tag else "PASS", nums)


heads = []
if SK:
    heads.append(f"SK: {len(SK)} played lives (one a file); presets {sorted({str(x.get('preset')) for x in SK})}, seeds "
                 f"{sorted({str(x.get('seed')) for x in SK})}, policies {sorted({str(x.get('policy')) for x in SK})}")
    logic(SK, "sk")
if not LA:
    print("\n".join(heads)); print("\n".join(lines))
    for t, d in detail:
        print(f"\n{t}:\n{json.dumps(d, indent=1)[:6000]}")
    if jout:
        json.dump(dict(sk_head=heads[0], rows=out, detail={t: d for t, d in detail}), open(jout, "w", encoding="utf-8"), indent=1)
    sys.exit(0)
lives = sum(x["N"] for x in LA)
seeds = ",".join(str(x["seed"]) for x in LA)
head = f"LA seeds {seeds}: {lives} lives x {LA[0]['years']} years, engine.py {LA[0]['engine_md5']}"
logic(LA)

# ---- NR1 and WA8n
routes = LA[0]["routes"]
def reached(files):
    by = {}
    for x in files:
        dec = x["wa"]
        for r in x["national"]["log"]:
            if r.get("what") == "reached" and r.get("route"):
                d = dec[r["n"]] if r["n"] < len(dec) else {}
                by.setdefault(r["route"], []).append(dict(seed=x["seed"], life=r["n"], kind=r["kind"], age=r["age"],
                                                          decisions=d.get("national"), nation=d.get("nation"),
                                                          known_weeks=d.get("known_weeks")))
    return by
rla, rnt = reached(LA), reached(NT)
used = lambda xs: sum(1 for y in xs if (y["decisions"] or 0) > 0)   # noqa: E731
miss = [r for r in routes if r not in rla and r not in rnt]
nla = sum(1 for r in routes if r in rla)
txt = f"{nla} of {len(routes)} routes reached in LA" + (f", {sum(1 for r in routes if r in rnt)} in the targeted lives" if NT else "")
noact = [r for r in routes if (r in rla or r in rnt) and used(rla.get(r, []) + rnt.get(r, [])) == 0]
if miss:
    say("NR1", "INCONCLUSIVE", txt + f"; not reached: {', '.join(miss)}" + ("" if NT else " (run --nat-test for the targeted lives)"))
elif noact:
    say("NR1", "FAIL", txt + f"; reached but no decision at national standing on: {', '.join(noact)}")
else:
    say("NR1", "PASS", txt + "; every route's lives took decisions at national standing")
detail.append(("NR1 routes: lives reaching each (LA, targeted) and those taking decisions",
               {r: dict(la=len(rla.get(r, [])), targeted=len(rnt.get(r, [])), deciding=used(rla.get(r, []) + rnt.get(r, [])))
                for r in routes}))
ever = sum(sum(1 for e in x["national"]["ever"] if e) for x in LA)
share = ever / max(lives, 1)
kinds = {}
for x in LA:
    for r in x["national"]["log"]:
        if r.get("what") == "reached":
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
nat_lead = {}
for x in LA:
    w40 = x["w"].get("40")
    for n, e in enumerate(x["national"]["ever"]):
        if e and w40 is not None:
            c = COL[int(np.argmax(w40[n]))]; nat_lead[c] = nat_lead.get(c, 0) + 1
say("WA8n", "PASS" if .01 <= share <= .03 else "FAIL" if ever >= 16 or share > .03 else "INCONCLUSIVE",
    f"{ever} of {lives} LA lives reached national standing ({share:.4f}; band .01 to .03), by kind {kinds}; routes taken in LA "
    f"{nla} of {len(routes)}; national lives by leading colour at 40 {nat_lead} (each under 30: the floor not read); "
    f"SK's share is the game's")

# ---- CL1 and CL3
sph_bad = dec_raw = dec_w = 0; nl = 0
rate = {c: [] for c in COL}
for x in LA:
    cy = x["clash"]["ceilings"]; ya = cy["young_age"]; yw = cy["young_w"]
    w40 = x["w"].get("40"); died = x["died"]
    for n, wk in enumerate(x["clash"]["weeks"] or []):
        nl += 1
        ts = sorted(int(e[0]) for e in wk)
        sp = {}
        for e in wk:
            for s in e[1]:
                sp.setdefault(s, []).append(int(e[0]))
        if any(b - a < 104 for v in sp.values() for a, b in zip(sorted(v), sorted(v)[1:])):
            sph_bad += 1
        if any(sum(1 for u in ts if t <= u < t + 520) > 3 for t in ts):
            dec_raw += 1
        if any(sum(yw if e[3] < ya else 1.0 for e in wk if t <= int(e[0]) < t + 520) > cy["decade_n"] + 1e-9 for t in ts):
            dec_w += 1
        end = min(x["years"], died[n] if died[n] is not None else x["years"])
        if w40 is not None and end >= 40:
            rate[COL[int(np.argmax(w40[n]))]].append(len(wk) / max(end - 10, 1))
say("CL1", "PASS" if sph_bad == 0 and dec_raw == 0 else "FAIL",
    f"lives with two clashes in one sphere within 2 years: {sph_bad} of {nl}; with more than 3 in 10 years: {dec_raw} "
    f"(counting a clash before 18 as {LA[0]['clash']['ceilings']['young_w']}, as the engine does: {dec_w})")
mean = np.mean([v for c in COL for v in rate[c]]) if any(rate.values()) else 0
rr = {c: (np.mean(rate[c]) / mean if mean > 0 and rate[c] else None) for c in COL}
ok3 = all(v is None or .8 <= v <= 1.25 for v in rr.values())
say("CL3", "PASS" if ok3 else "FLAG", "clash rate by leading colour at 40 over the mean: "
    + ", ".join(f"{c} {v:.2f} ({len(rate[c])})" if v is not None else f"{c} -" for c, v in rr.items()) + " (band .8 to 1.25, reported)")

# ---- AM2
# each arrival against the years stated for it: the life's own clock at the rung's start where the hook recorded one
# (aims2.Agenda.clock, what the preview says from f8c7aa1), else the field's catalogue years (older hooks)
clocks = LA[0].get("clocks") or {}
steps = {}; own = 0
for x in LA:
    for a_ in x["aims2"]["arrivals"]:
        n, j, f, r, yrs, kept, wk = a_[:7]; ck = a_[7] if len(a_) > 7 else None
        st_ = ck if ck is not None else (clocks.get(f) or [[None]])[r][0] if f in clocks and r < len(clocks[f]) else None
        own += ck is not None
        if kept >= .5 and st_ is not None and st_ > 0.05:
            steps.setdefault((f, r), []).append(yrs / st_)
rng = np.random.default_rng(0)
ratios, outside, inside_unsure = {}, [], []
for (f, r), ys in steps.items():
    if len(ys) < 10:
        continue
    ys = np.asarray(ys); m = float(np.median(ys))
    bs = [float(np.median(rng.choice(ys, len(ys)))) for _ in range(400)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    ratios[f"{f}|{r}"] = (round(m, 2), round(float(lo), 2), round(float(hi), 2), len(ys))
    if not (.5 <= m <= 2):
        (outside if (hi < .5 or lo > 2) else inside_unsure).append(f"{f} rung {r} {m:.2f} [{lo:.2f}, {hi:.2f}] n={len(ys)}")
say("AM2", "FAIL" if outside else "INCONCLUSIVE" if inside_unsure or not ratios else "PASS",
    f"{len(ratios)} steps with 10 or more arrivals among keepers (LA only; SK's are the game's; {own} arrivals read "
    "against the life's own clock, the rest against the catalogue's years); "
    + (f"outside .5 to 2: {'; '.join(outside + inside_unsure)}" if outside or inside_unsure else
       "every median in .5 to 2 of its stated years" if ratios else "none to read"))
detail.append(("AM2 steps: median over stated years [95%] n", ratios))

# ---- F5
def known(x):
    if "ht_names" not in x:
        return None
    k = x["ht_names"].index("Known")
    return [w[k] >= 0 for w in x["ht_week"]]
f5 = {c: [[0, 0], [0, 0]] for c in COL}   # [kept, left] x [Known, lives]
for x in LA:
    kn = known(x); w18, w40 = x["w"].get("18"), x["w"].get("40")
    if kn is None or w18 is None or w40 is None:
        continue
    for n in range(x["N"]):
        if x["died"][n] is not None and x["died"][n] < 40:
            continue
        c18, c40 = int(np.argmax(w18[n])), int(np.argmax(w40[n]))
        g = f5[COL[c18]][0 if c18 == c40 else 1]; g[0] += int(kn[n]); g[1] += 1
flag = []
parts = []
for c in COL:
    (a, an), (b, bn) = f5[c]
    ka, kb = a / max(an, 1), b / max(bn, 1)
    parts.append(f"{c} kept {ka:.3f} ({an}) left {kb:.3f} ({bn})")
    if an and bn and kb > 0 and ka < 2 / 3 * kb:
        flag.append(c)
say("F5", "FLAG" if flag else "PASS", "Known by leading colour at 18, kept to 40 against left: " + "; ".join(parts)
    + (f"; flagged: {', '.join(flag)}" if flag else ""))

# ---- RE3 (LA against LB)
def re3(files):
    w40 = np.concatenate([np.asarray(x["w"]["40"]) for x in files]); w70 = np.concatenate([np.asarray(x["w"]["70"]) for x in files])
    a40 = np.concatenate([[d is None or d >= 40 for d in x["died"]] for x in files])
    a70 = np.concatenate([[d is None or d >= 70 for d in x["died"]] for x in files])
    ent = -(w40 * np.log(np.maximum(w40, 1e-12))).sum(1)
    ch = np.concatenate([x["lead_changes18"] for x in files]); c2040 = np.concatenate([x["change_20_40"] for x in files])
    call = np.concatenate([x["change_all"] for x in files])
    w30 = np.concatenate([np.asarray(x["w"]["30"]) for x in files]); w50 = np.concatenate([np.asarray(x["w"]["50"]) for x in files])
    a50 = np.concatenate([[d is None or d >= 50 for d in x["died"]] for x in files])
    cor = np.mean([np.corrcoef(w30[a50, k], w50[a50, k])[0, 1] for k in range(5)])
    return dict(one40=float((w40[a40].max(1) > .5).mean()), one70=float((w70[a70].max(1) > .5).mean()), ent40=float(ent[a40].mean()),
                changes18=float(ch.mean()), share2040=float(c2040.sum() / max(call.sum(), 1e-12)), corr3050=float(cor))
if LB:
    if [x["seed"] for x in LB] != [x["seed"] for x in LA]:
        say("RE3", "INCONCLUSIVE", "LB's seeds are not LA's")
    else:
        a, b = re3(LA), re3(LB)
        ok = dict(one40=abs(a["one40"] - b["one40"]) <= .05, one70=abs(a["one70"] - b["one70"]) <= .05,
                  ent40=abs(a["ent40"] - b["ent40"]) <= .05, changes18=a["changes18"] - b["changes18"] <= .5,
                  share2040=a["share2040"] >= b["share2040"], corr3050=a["corr3050"] >= b["corr3050"] - .05)
        say("RE3", "PASS" if all(ok.values()) else "FLAG", "LA against LB: " + "; ".join(
            f"{k} {a[k]:.3f} vs {b[k]:.3f}{'' if ok[k] else ' (outside)'}" for k in a) + " (diagnostic)")
else:
    say("RE3", "INCONCLUSIVE", "no LB files (--base)")

print("\n".join([head] + heads))
print("\n".join(lines))
for t, d in detail:
    print(f"\n{t}:\n{json.dumps(d, indent=1)[:6000]}")
if jout:
    json.dump(dict(head=head, **(dict(sk_head=heads[0]) if heads else {}), rows=out, detail={t: d for t, d in detail}), open(jout, "w", encoding="utf-8"), indent=1)
