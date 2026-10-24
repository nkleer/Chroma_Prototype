"""Checks a compiled batch for one world setting (tribal and magic worlds, v23). Library thread, 2026-10-07.

    python3 check_world.py <batch dir> <setting> [packs...]     setting: earth | tribal | magic

The engine keeps a moment in a life of setting S unless it says only: and S is not among its worlds
(chroma-engine/prototype/batch.py, load_batch). For S other than earth this reports:
  1. presence: moments in S, and how many are ready (a summary line and scenes for S) or would show Earth words;
  2. balance: for the moments in S, the weight per colour by stage (means and ends, each option counting 1 split
     over its colours), the base chance per means colour, and the pair, triad and cross counts, which must stay even
     in S on its own, as on Earth;
  3. anachronisms: words in S's player text (summary, scenes, world wording of options) that cannot exist there
     (tribal: a band 40,000 years ago; magic: a pre-industrial world with towers and guilds);
  4. world wording missing on options whose Earth label holds a word S cannot have.
Read only. Exit status 1 when a ready moment holds an anachronism or a stage is uneven by more than 3%.
"""
import collections
import importlib.util
import itertools
import os
import re
import sys

sys.dont_write_bytecode = True
D, S = sys.argv[1], sys.argv[2]
PACKS = sys.argv[3:]
COLORS = "WUBRG"
STAGES = ["child", "juvenile", "young_adult", "adult", "mature", "elder"]
MODERN = r"phone|phones|online|app|apps|screen|screens|email|internet|website|video|camera|tv|television|radio|" \
         r"car|cars|bus|buses|train|trains|motorbike|lorry|van|driving|plane|planes|flight|airport|computer|laptop|" \
         r"spreadsheet|electric|electricity|plastic|factory|factories|office|offices|bank|banks|loan|mortgage|" \
         r"pension|benefits|insurance|passport|visa|police|ambulance|hospital|clinic|vaccine|pill|pills|cigarette|" \
         r"cigarettes|gun|guns|rifle|shotgun|supermarket|cinema|gym|nightclub|university|degree|exam|exams|" \
         r"parliament|election|elections|minister|ministry|newspaper|lift|text message|group chat"
# Industrial and electric things: they exist in neither world. Offices, banks, loans, universities, ministers and
# elections can exist in a pre-industrial magic world, so only the tribal check carries those.
INDUSTRIAL = r"phone|phones|online|app|apps|screen|screens|email|internet|website|video|camera|tv|television|radio|" \
             r"car|cars|bus|buses|train|trains|motorbike|lorry|van|driving|plane|planes|flight|airport|computer|" \
             r"laptop|spreadsheet|electric|electricity|plastic|factory|factories|vaccine|pill|pills|cigarette|" \
             r"cigarettes|gun|guns|rifle|shotgun|supermarket|cinema|gym|nightclub|text message|group chat|" \
             r"ambulance|insurance|pension|benefits|mortgage|passport|visa"
ANACHRONISM = {
    "tribal": re.compile(r"\b(" + MODERN.replace("screen|screens|", "") + r"|money|coin|coins|pay|wage|wages|salary|shop|shops|market|town|towns|"
                         r"city|cities|school|schools|book|books|letter|letters|write|writes|wrote|written|"
                         r"iron|steel|bronze|metal|wheel|wheels|cart|horse|horses|farm|farms|field|fields|plough|"
                         r"bread|wheat|cattle|sheep|king|queen|lord|law|laws|court|prison|army|soldier|church|temple|"
                         r"magic|spell|spells|wizard|mage)\b", re.I),
    "magic": re.compile(r"\b(" + INDUSTRIAL + r")\b", re.I),
}
# Old senses and verbs of a flagged word, removed before matching: a river bank, to train for, to lift them, to the
# letter, reading the signs, a screen of hides (the
# tribal list does not flag screens at all: a phone screen still shows as phone).
VERBS = r"\b(train|trains|lift|lifts)( up)? (to|for|an?|the|them|him|her|their|his|its|every|young|with|hard)\b|" \
        r"\bto the letter\b|\bbank (a|the|some) (favour|favor|goodwill)\b|\b(on|by|along|up|down) the bank\b|"
ALLOW = {
    "tribal": re.compile(VERBS + r"\b(far|near|river|other|steep|muddy) banks?\b|"
                         r"\breading (the|of) (spirits|signs|sky|stars|tracks|weather|wind|bones|smoke|mood)\b", re.I),
    "magic": re.compile(VERBS + r"\b(hide|reed|carved|painted|woven|wooden) screens?\b", re.I),
}
FILLRX = re.compile(r"\{\w+\}")


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mods = [load(os.path.join(D, "earth.py"))] + [load(os.path.join(D, f"earth_{p}.py")) for p in PACKS]
sits = [x for m in mods for x in list(m.SITUATIONS) + list(getattr(m, "ECHOES", []))]
reads = [x for m in mods for x in getattr(m, "EVENTS_READ", [])]


def present(x):
    only = x.get("only")
    return not only or S in str(only).replace(",", " ").split()


def ready(x):
    return S == "earth" or (x.get("worlds", {}).get(S) and (x.get("scenes") or {}).get(S))


def weights(field):
    """'W1' -> {'W': 1.0}; 'W.5 B.5' -> {'W': .5, 'B': .5}; None -> {}."""
    out = {}
    for tok in str(field or "").split():
        if tok[:1] in COLORS:
            out[tok[0]] = float(tok[1:] or 1)
    return out


def opt_fields(o):
    """Compiled option: (label, means, ends or None, base chance, mark[, note]). Means and ends come back as
    colour strings in WUBRG order; a cross option has one means colour and one end colour."""
    label = o[0]
    note = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
    means = "".join(c for c in COLORS if c in weights(o[1]))
    ends = "".join(c for c in COLORS if c in weights(o[2] if len(o) > 2 else None))
    return label, means, ends, note


def stages_of(x):
    st = x.get("stages", "")
    if isinstance(st, (list, tuple)):
        st = " ".join(st)
    out = []
    for w in str(st).replace(",", " ").split():
        if w == "all":
            out += STAGES
        elif w.endswith("+") and w[:-1] in STAGES:
            out += STAGES[STAGES.index(w[:-1]):]
        elif w in STAGES:
            out.append(w)
    return sorted(set(out), key=STAGES.index)


inS = [x for x in sits if present(x)]
rd = [x for x in inS if ready(x)]
fails = []
print(f"# World check: {S}  ({D}{', packs ' + ' '.join(PACKS) if PACKS else ''})\n")
print(f"1. presence: {len(inS)} of {len(sits)} moments are in {S}; ready (summary and scenes for {S}): {len(rd)}; "
      f"would show Earth words: {len(inS) - len(rd)}. Outside events: {len([r for r in reads if present(r)])} of {len(reads)}.")

wt = {st: collections.Counter() for st in STAGES}
ch = {st: collections.defaultdict(list) for st in STAGES}
pairs, triads, cross = collections.Counter(), collections.Counter(), collections.Counter()
for x in inS:
    for o in x.get("options", []):
        label, means, ends, note = opt_fields(o)
        if not means:
            continue
        for st in stages_of(x):
            for c in means:
                wt[st]["m" + c] += 1 / len(means)
            for c in (ends or means):
                wt[st]["e" + c] += 1 / len(ends or means)
            if len(o) > 3 and isinstance(o[3], (int, float)):
                for c in means:
                    ch[st][c].append(float(o[3]))
        if ends:
            cross[f"{means}>{ends}"] += 1
        elif len(means) == 2:
            pairs[means] += 1
        elif len(means) == 3:
            triads[means] += 1
print("\n2. balance, weight per colour by stage (means / ends), and base chance per means colour:")
for st in STAGES:
    m = [wt[st]["m" + c] for c in COLORS]
    e = [wt[st]["e" + c] for c in COLORS]
    if sum(m) == 0:
        continue
    avg = sum(m) / 5
    spread = (max(m) - min(m)) / avg * 100 if avg else 0
    cm = [sum(ch[st][c]) / len(ch[st][c]) * 100 if ch[st][c] else 0 for c in COLORS]
    print(f"   {st:12s} means {' '.join(f'{v:6.1f}' for v in m)} | ends {' '.join(f'{v:6.1f}' for v in e)} | "
          f"spread {spread:.1f}% | chance {' '.join(f'{v:.0f}' for v in cm)}")
    if spread > 3:
        fails.append(f"stage {st} uneven: {spread:.1f}% between the most and least weighted colour")
print("   pairs " + ", ".join(f"{''.join(p)} {pairs[''.join(p)]}" for p in itertools.combinations(COLORS, 2)))
print("   triads " + ", ".join(f"{''.join(t)} {triads[''.join(t)]}" for t in itertools.combinations(COLORS, 3)))
print("   cross " + ", ".join(f"{a}>{b} {cross[a + '>' + b]}" for a in COLORS for b in COLORS if a != b))

print(f"\n3. anachronisms in {S} text:")
hits = 0
rx = ANACHRONISM.get(S)
for x in rd if rx else []:
    texts = [x["worlds"][S]] + [t[1] for t in x["scenes"][S]]
    texts += [opt_fields(o)[3].get("world", {}).get(S, "") for o in x.get("options", [])]
    for t in texts:
        for mm in rx.finditer(ALLOW[S].sub("", FILLRX.sub("", t or ""))):
            hits += 1
            if hits <= 40:
                print(f"   {x['name']}: '{mm.group(0)}' in: {t[:90]}")
print(f"   {hits} found")
if hits:
    fails.append(f"{hits} anachronisms in ready {S} moments")

print(f"\n4. options whose Earth label holds a word {S} cannot have, with no {S} wording (in ready moments):")
miss = []
for x in rd if rx else []:
    for o in x.get("options", []):
        label, _, _, note = opt_fields(o)
        if rx.search(ALLOW[S].sub("", label)) and not note.get("world", {}).get(S):
            miss.append(f"   {x['name']}: {label}")
print("\n".join(miss[:40]) + (f"\n   ... {len(miss) - 40} more" if len(miss) > 40 else ""))
print(f"   {len(miss)} found")

print("\nRESULT: " + ("PASS" if not fails else "FAIL\n" + "\n".join("  - " + f for f in fails)))
sys.exit(1 if fails else 0)
