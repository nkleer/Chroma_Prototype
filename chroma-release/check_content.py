"""Release check of the final content (chroma-release/checklist.md, section 9, rows C-L7 to C-L10): the parts of the final
check that need no engine run.

  C-L7  safety limits (Emren 10-05 22:43 and point 11): no pickable sexual violence; no harm to a child as an act;
        suicide never pickable; killing only by choice, rare, never graphic, never by or of a child; intimacy fades to
        black
  C-L8  timeless modern days (Emren 10-06 10:42): no year, brand, real country, real person or real event in any text
        the player can see (the game's own word list, chroma-game/prototype/test/timeless.py)
  C-L9  sex and gender (chroma-identity/SPEC.md): the two marks exist; no act changes orientation or gender; medical
        steps only for adults; `role:` values and the norm keys as settled; never `role:` and `norm: role crossing`
        on one option; 'women at work' gone
  C-L10 option chance: every option carries `chance` in (0, 1] (doing nothing is the engine's own, not written); every
        `closed:` names a kind the engine knows (law, approval, means; an unknown one reads as approval, checklist L1)

Reads the Library's compiled files (default chroma-library, the live batch: earth.py and the three pack files),
chroma-library/dreams.py and chroma-art/game/ink-option-texts.json. Read only. A hard rule broken is a FAIL; a word
that needs a reader's eye is listed under REVIEW with where it stands, and the release owner records the verdict.

    python3 -I chroma-release/check_content.py [--batch DIR] [--dreams FILE] [--ink FILE]

Writes chroma-release/out/content_<UTC time>.txt. Exit code 0 when nothing FAILs."""
import sys, os, re, json, ast, argparse, importlib.util, time, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py
ap = argparse.ArgumentParser()
ap.add_argument("--batch", default=P["library_live"])
ap.add_argument("--dreams", default=path("library_live", "dreams.py"))
ap.add_argument("--ink", default=path("art_game", "ink-option-texts.json"))
ap.add_argument("--game", default=P["game_live"])
a = ap.parse_args()
os.makedirs(P["release_out"], exist_ok=True)
REPORT = path("release_out", time.strftime("content_%Y%m%d-%H%M.txt", time.gmtime()))
OUT = []; FAILS = []; REVIEW = collections.defaultdict(list)


def say(s=""):
    print(s); OUT.append(s)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.dont_write_bytecode = True; spec.loader.exec_module(m)
    return m


FILES = [f for f in ("earth", "earth_science", "earth_politics", "earth_stage") if os.path.exists(os.path.join(a.batch, f + ".py"))]
MODS = {f: load(os.path.join(a.batch, f + ".py"), "chk_" + f) for f in FILES}
say(f"Content check, {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}: {a.batch} ({', '.join(FILES)}), {a.dreams}, {a.ink}")


def moments(m):
    for s in getattr(m, "SITUATIONS", []):
        yield "situation", s
    for s in getattr(m, "ECHOES", []):
        yield "echo", s
    for s in getattr(m, "EVENTS_READ", []):
        yield "read event", s


def minage(s):
    ag = s.get("age")
    try:
        return float(ag[0])
    except Exception:
        st = str(s.get("stages", ""))
        return 0 if "child" in st else 11 if "juvenile" in st else 17


def young(s):
    return minage(s) < 18 or any(k in str(s.get("stages", "")) for k in ("child", "juvenile"))


# ---------------------------------------------------------------------------------------------------- C-L10 option chance
say("\nC-L10 option chance")
for f, m in MODS.items():
    n = bad = 0; ex = []
    for kind, s in moments(m):
        for o in s.get("options", []) or []:
            n += 1
            nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
            c = nt.get("chance")
            if not isinstance(c, (int, float)) or not (0 < c <= 1):
                bad += 1; ex.append((s["name"], o[0], c))
    say(f"  {f}: {n} options, {bad} without a chance in (0, 1]" + (f"; e.g. {ex[:3]}" if ex else ""))
    if bad:
        FAILS.append(f"C-L10 {f}: {bad} options without a chance")
    nc = 0; unk = []   # read as engine.py does: the kind is the text before the first ':' (';' and '|' count as ':')
    for kind, s in moments(m):
        for o in s.get("options", []) or []:
            nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
            if nt.get("closed"):
                nc += 1
                kd = str(nt["closed"]).replace(";", ":").replace("|", ":").split(":")[0].strip()
                if kd not in ("law", "approval", "means"):
                    unk.append((s["name"], o[0], kd))
    say(f"  {f}: {nc} closed options, {len(unk)} with a kind the engine does not know" + (f"; e.g. {unk[:3]}" if unk else ""))
    if unk:
        FAILS.append(f"C-L10 {f}: {len(unk)} closed options with an unknown kind")

# -------------------------------------------------------------------------------------------------------- all the texts
SHOWN_SIT = ("name", "scenes", "outcomes", "worlds", "say", "lines", "readings", "reading", "title")
NOTE_KEYS = ("timing", "src", "source", "sources", "note", "notes", "why_rate",
             "trigger")   # trigger.likelier: why the moment comes (with its sources); no game code reads it (grep, 07:17 Emren time)


def strings(x, path):
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from strings(v, f"{path}.{k}")
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            yield from strings(v, f"{path}[{i}]")


TEXTS = []   # (where, player-facing?, text, young?, situation)
for f, m in MODS.items():
    for kind, s in moments(m):
        nm = s.get("name", "?")
        for k, v in s.items():
            if k == "options":
                for i, o in enumerate(v or []):
                    TEXTS.append((f"{f}:{nm}:option {i + 1}", True, o[0], young(s), s))
                    nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
                    for p_, t_ in strings(nt, f"{f}:{nm}:option {i + 1} notes"):
                        TEXTS.append((p_, False, t_, young(s), s))
            else:
                for p_, t_ in strings(v, f"{f}:{nm}.{k}"):
                    TEXTS.append((p_, k not in NOTE_KEYS, t_, young(s), s))
    for name in ("VOICE", "LESSONS", "HEART_WHY", "HEAD_WHY", "MARKS"):
        if hasattr(m, name):
            for p_, t_ in strings(getattr(m, name), f"{f}:{name}"):
                TEXTS.append((p_, True, t_, False, None))
try:
    dm = load(a.dreams, "chk_dreams")
    for name in [k for k in dir(dm) if k.isupper()]:
        for p_, t_ in strings(getattr(dm, name), f"dreams:{name}"):
            TEXTS.append((p_, True, t_, False, None))
except Exception as ex:
    FAILS.append(f"dreams.py does not load: {ex!r}")
try:
    ink = json.load(open(a.ink))
    for p_, t_ in strings(ink, "ink-option-texts"):
        TEXTS.append((p_, not re.search(r"\.(\w*about|credit)\b", p_), t_, False, None))   # the file's own notes are not shown
except Exception as ex:
    FAILS.append(f"ink-option-texts.json does not load: {ex!r}")
say(f"\n{len(TEXTS)} strings read ({sum(1 for t in TEXTS if t[1])} the player can see)")

# ------------------------------------------------------------------------------------------------------- C-L8 timeless
say("\nC-L8 timeless modern days")
REAL = None
tree = ast.parse(open(os.path.join(a.game, "test", "timeless.py")).read())
for nd in tree.body:
    if isinstance(nd, ast.Assign) and getattr(nd.targets[0], "id", "") == "REAL":
        REAL = re.compile(nd.value.args[0].value, re.I)
hits = collections.Counter(); shown = []
for where, vis, t, yg, s in TEXTS:
    for mm in REAL.finditer(t):
        w = mm.group(0)
        if vis:
            shown.append((w, where, t[:140]))
        else:
            hits[w.lower()] += 1
say(f"  player-facing hits: {len(shown)}")
for w, where, t in shown[:40]:
    say(f"    {w!r} at {where}: {t}")
say(f"  in notes the player never sees (sources, timing): {sum(hits.values())} ({', '.join(f'{k} {v}' for k, v in hits.most_common(8))})")
if shown:
    FAILS.append(f"C-L8: {len(shown)} player-facing strings with a year, brand, real place, person or event")

# --------------------------------------------------------------------------------------------------------- C-L7 safety
say("\nC-L7 safety limits")
OPT = [(w, t, yg, s) for w, vis, t, yg, s in TEXTS if ":option " in w and "notes" not in w]
SEXV = re.compile(r"\b(rap(e|es|ed|ing|ist)|sexual(ly)? (assault|abuse)\w*|molest\w*|grop(e|ed|ing)|non-?consensual|"
                  r"against (her|his|their|your) will|spik(e|ed|ing) (a|her|his|their|your) drink|date[- ]rape|"
                  r"revenge porn|upskirt\w*|coerc\w+ (her|him|them|you) into (sex|bed))\b", re.I)
SUIC = re.compile(r"\b(suicid\w*|kill (yourself|myself|themselves|himself|herself)|take (your|my|their|his|her) own life|"
                  r"end (it all|your life|my life|your own life)|hang (yourself|myself)|slit (your|my) wrists?|"
                  r"overdose on purpose|jump (off|from) the (bridge|roof))\b", re.I)
CHILD = re.compile(r"\b(child|children|kid|kids|son|daughter|baby|toddler|infant|little one|stepchild|pupil|"
                   r"schoolchild|{child}|{kid}|{baby}|{son}|{daughter})\b", re.I)
HARM = re.compile(r"\b(hit|hits|slap\w*|smack\w*|spank\w*|beat|beats|beating|shak(e|es|ing) (him|her|them|the baby)|"
                  r"punch\w*|kick\w*|burn\w*|starv\w*|lock (him|her|them) (in|up)|abus\w*|belt|cane|hurt (him|her|them))\b", re.I)
KILLW = re.compile(r"\b(kill\w*|murder\w*|shoot (him|her|them|to kill)|stab\w*|strangl\w*|poison (him|her|them)|"
                   r"run (him|her|them) down|end (his|her|their) life)\b", re.I)
GORE = re.compile(r"\b(blood\w*|gore|gory|guts|brains?|entrails|dismember\w*|severed|slit (his|her|their) throat|"
                  r"skull|corpse)\b", re.I)
EXPL = re.compile(r"\b(naked|nude|undress\w*|breasts?|nipples?|genital\w*|penis|vagina|orgasm\w*|climax\w*|thrust\w*|"
                  r"erection|moan\w*|intercourse|oral sex|strip(s|ped|ping)? (off|naked))\b", re.I)
c1 = [(w, t) for w, t, yg, s in OPT if SEXV.search(t)]
say(f"  sexual violence in an option: {len(c1)}")
for w, t in c1:
    say(f"    FAIL {w}: {t}")
if c1:
    FAILS.append(f"C-L7: {len(c1)} options with sexual violence")
c1b = [(w, t[:160]) for w, vis, t, yg, s in TEXTS if vis and ":option " not in w and SEXV.search(t)]
for w, t in c1b:
    REVIEW["sexual violence mentioned outside an option (allowed only indirectly, as someone's past)"].append(f"{w}: {t}")
c3 = [(w, t) for w, t, yg, s in OPT if SUIC.search(t)]
say(f"  suicide in an option: {len(c3)}")
for w, t in c3:
    say(f"    FAIL {w}: {t}")
if c3:
    FAILS.append(f"C-L7: {len(c3)} options that are suicide")
for w, vis, t, yg, s in TEXTS:
    if vis and ":option " not in w and SUIC.search(t):
        REVIEW["suicide mentioned outside an option (allowed only as an event or someone else's)"].append(f"{w}: {t[:160]}")
for w, t, yg, s in OPT:
    if CHILD.search(t) and HARM.search(t):
        REVIEW["an option naming a child and a harm word (harm to a child must never be an act)"].append(f"{w}: {t}")
# killing: written fields and words
kills = []
for f, m in MODS.items():
    for kind, s in moments(m):
        sk = s.get("kills")
        for i, o in enumerate(s.get("options", []) or []):
            nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
            if nt.get("kills") or KILLW.search(o[0]):
                kills.append((f, s, i, o, nt.get("kills")))
        if sk:
            REVIEW["moments with a situation-level kills: (a death that happens, not an act)"].append(f"{f}:{s['name']}: kills {sk!r}, ages {s.get('age')}")
say(f"  options that kill or name killing: {len(kills)}")
for f, s, i, o, kr in kills:
    nt = o[5]
    child_stage = young(s)
    child_role = kr is not None and re.search(r"child|son|daughter|baby|kid", str(kr), re.I)
    graphic = GORE.search(o[0]) or any(GORE.search(x) for oc in (s.get("outcomes") or ()) for x in (oc if isinstance(oc, (list, tuple)) else [oc]) if isinstance(x, str))
    tag = []
    if kr is not None and child_stage:
        tag.append("BY A CHILD")
    if child_role:
        tag.append("OF A CHILD")
    if kr is not None and graphic:
        tag.append("GRAPHIC")
    line = (f"{f}:{s['name']} option {i + 1} (ages {s.get('age')}, rate {s.get('per_year', s.get('rate'))}, chance {nt.get('chance')}, "
            f"kills {kr!r}): {o[0]}")
    if tag:
        say(f"    FAIL {', '.join(tag)}: {line}")
        FAILS.append(f"C-L7 killing: {', '.join(tag)}: {f}:{s['name']} option {i + 1}")
    else:
        REVIEW["options that kill or name killing (by choice, rare, not graphic, never by or of a child)"].append(line)
# intimacy
intim = set()
lib_int = path("library_live", "earth-intimacy.lib")
if os.path.exists(lib_int):
    intim = set(re.findall(r"^== (.+?)\s*$", open(lib_int).read(), re.M))
for w, vis, t, yg, s in TEXTS:
    if vis and EXPL.search(t):
        inn = s is not None and (s.get("name") in intim or "intimacy" in str(s.get("life", "")))
        REVIEW["explicit words (intimacy must fade to black)" + (" in an intimacy moment" if inn else "")].append(f"{w}: {t[:160]}")

# ------------------------------------------------------------------------------------------------------ C-L9 sex and gender
say("\nC-L9 sex and gender (chroma-identity/SPEC.md)")
marks = collections.Counter(); roles = collections.Counter(); norms = collections.Counter(); both = []; orient = []; medical = []
ORIENT = re.compile(r"\b(make|turn|become|cure|fix|change|pray (it|the gay|that) away)\b.{0,30}\b(gay|straight|lesbian|"
                    r"bisexual|queer|attraction|orientation)\b|\bconversion (therapy|camp|programme|program)\b", re.I)
MED = re.compile(r"\b(hormone\w*|puberty blocker\w*|surgery|operation|transition\w* medically|top surgery)\b", re.I)
GENDER_CTX = re.compile(r"\b(gender|trans|transition\w*|the name that|another name|own name|clothes and the name|who you are)\b", re.I)
for f, m in MODS.items():
    for kind, s in moments(m):
        txt_s = " ".join(t for _, t in strings({k: v for k, v in s.items() if k != "options"}, ""))
        for i, o in enumerate(s.get("options", []) or []):
            nt = o[5] if len(o) > 5 and isinstance(o[5], dict) else {}
            for mk in str(nt.get("mark", "")).split(","):
                if mk.strip():
                    marks[mk.strip()] += 1
            if "role" in nt:
                roles[str(nt["role"]).strip()] += 1
            if "norm" in nt:
                for nk in str(nt["norm"]).split("|"):
                    norms[nk.strip().split(":")[0].strip()] += 1
            if "role" in nt and "role crossing" in str(nt.get("norm", "")):
                both.append(f"{f}:{s['name']} option {i + 1}")
            if ORIENT.search(o[0]):
                orient.append(f"{f}:{s['name']} option {i + 1}: {o[0]}")
            if MED.search(o[0]) and (GENDER_CTX.search(o[0]) or GENDER_CTX.search(txt_s)) and young(s):
                medical.append(f"{f}:{s['name']} option {i + 1} (ages {s.get('age')}): {o[0]}")
for mk in ("came out", "named their gender"):
    say(f"  mark {mk!r}: {marks.get(mk, 0)} options")
    if not marks.get(mk):
        FAILS.append(f"C-L9: no option gives the mark {mk!r}")
bad_roles = {k: v for k, v in roles.items() if k not in ("women", "men", "keep", "cross")}
say(f"  role: values {dict(roles)}" + (f"; unknown {bad_roles}" if bad_roles else ""))
if bad_roles:
    FAILS.append(f"C-L9: unknown role: values {bad_roles}")
say(f"  norm: keys used {dict(norms.most_common(30))}")
say(f"  role: and norm: role crossing on one option: {len(both)}" + (f" ({both[:5]})" if both else ""))
if both:
    FAILS.append(f"C-L9: {len(both)} options with both role: and norm: role crossing")
waw = [w for w, vis, t, yg, s in TEXTS if "women at work" in t.lower()]
say(f"  'women at work' anywhere: {len(waw)}" + (f" ({waw[:3]})" if waw else ""))
if waw:
    FAILS.append(f"C-L9: 'women at work' still used ({len(waw)})")
say(f"  options that change orientation or name conversion: {len(orient)}")
for x in orient:
    REVIEW["options that might change orientation or name conversion (never by an act)"].append(x)
say(f"  medical gender steps offered under 18: {len(medical)}")
for x in medical:
    REVIEW["medical words in a gender moment open under 18 (only social steps under 18)"].append(x)

# ------------------------------------------------------------------------------------------------------------- review
say("\nREVIEW (a reader's verdict goes in the checklist)")
for k, v in REVIEW.items():
    say(f"  {k}: {len(v)}")
    for x in v[:60]:
        say(f"    {x}")
say(f"\nRESULT: {'PASS' if not FAILS else 'FAIL'} ({len(FAILS)} fails, {sum(len(v) for v in REVIEW.values())} lines to review)")
for x in FAILS:
    say(f"  FAIL {x}")
open(REPORT, "w").write("\n".join(OUT) + "\n")
say(f"report: {REPORT}")
import results; results.done('content', 0 if not FAILS else 1, REPORT)   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if not FAILS else 1)
