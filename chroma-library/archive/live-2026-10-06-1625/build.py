"""Compile a library source written in plain text (<name>.lib) into the engine's Python format (<name>.py).

python3 build.py earth                 reads earth.lib (or every earth-*.lib), checks the layout rules, writes earth.py
python3 build.py earth-adult.lib --out /tmp/x    one part file, compiled into /tmp/x/earth-adult.py (for its writer)

The .py it writes has no dependencies (plain dicts and tuples, like batch1.py), so the engine thread can pull it in
as is; check.py and render.py run on it. The text format keeps writers on the balance layout of library-spec.md:

    == a rainy afternoon with nothing to do
    tier: everyday                      everyday | life event | inner | echo | read
    stages: child                       stage names, "all", or "juvenile+" (that stage and every later one)
    age: 3-15
    calls: UR                           everyday only: the colors the moment calls up (alpha .4, the rest .1)
    tone: joy                           joy | trouble | mixed
    life: home, play
    horizon: moment                     moment | week | months | years
    roles: sibling, grandparent
    earth: rain keeps you indoors       the moment in each world (tribal:, magic:); only: magic for a world-only one
    per_year: .15 .05 0 0 0 0           life events: yearly rate per stage, child to elder
    drivers: prosper+.2 unrest-.4       life events: outside context that moves the rate
    times: / likelier: / rarer:         life events: in words (echoes and inner drivers use likelier/rarer too); times: and
                                        gap: lo-hi (years) are kept on every tier, as timing (the Book of Moments, point 12)
    requires:                           inner drivers: what must be true for the moment to come up
    after: mark 'hid a wrong'           echoes: what in the person's history it needs; delay: 1-15 (years)
    - W | set up a game with rules everyone keeps | v: conformity
    - U | take apart something old | habit | v: self-direction | mark: learned a skill | closed: approval: taking things apart; backfire: scolded
    - W>B | organise the game and referee it | v: power            one color's means for another color's end
    - WU | learn how to help and keep to it | binds | v: conformity  a combination (pair, triad, four, five)

Option fields after the label, separated by " | ": the flags habit, door, identity, binds; and v:, mark:, closed:,
body:, earth: / tribal: / magic: (wording in one world), tags: (engine tags such as win:money+.05), diff: (override),
act: (the act as the narrator says it, when the label reads badly in the third person), self_control: + or -
(engine v7: "+" an act of discipline that builds self-control, "-" giving in or giving up, which wears it down);
titles and perks (chroma-engine/perks-titles-format.md): title:, drops:, grants:, takes:, suspends: with for_years:,
requires: and without: (law, approval, means or impossible); chance: the base percent the act works for an ordinary
person of the moment's ages (95 an everyday act in one's own hands, 50 a fair try, 15 a long shot; the engine turns it into
the option's difficulty). On a situation, holds: names a perk or title the whole
moment needs (compiled to the engine's requires; a situation's requires: stays the inner driver's condition).
Read events (tier: read) take source:, base:, and five readings: "- R | the reading | impact: 1.2 | also: ... | say: ...".
The outer world (chroma-engine/world-fields.md, 2026-10-07), every field optional and every value from its list below:
moments take time_of_year:, holy:, who:, cast_want:, group:, where:, at: (one per line); options take law:, norm:, tech:,
lever:, pushes: (as "| law: drugs |"). Several values are separated by commas where the engine reads several.
Sex and gender (chroma-identity/for-the-engine.md, 2026-10-07): options take role: women | men | keep | cross (an act the
world reserves for one sex, or one that keeps or crosses the role the scene sets out), never beside norm: role crossing;
the story slot {seen_as} reads girl or boy, young woman or young man, woman or man, as the world sees the character.

Story fields for the game (game thread, 2026-10-04 22:54), third person and present tense with {N} (the character),
{Ns} (their possessive) and the game's role slots {parent} {grandparent} {elder} {sibling} {friend} {rival} {mentor}
{boss} {colleague} {partner} {prospect} {child} {dead} {place} {disaster}:
    scene: {N} is stuck indoors with {sibling} ...       untagged scene (modern Earth unless a world is named)
    scene W: ...   scene R child: ...   scene G older:   up to one variant per color; child = under 12, older = 12 and over
    works: ... (twice)   fails: ... (twice)               color-neutral outcome lines
A part file set: "python3 build.py earth" reads earth.lib, or every earth-*.lib in name order when there is no earth.lib.
Lines starting with # are comments.
"""
import sys, os, re, itertools, pprint
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
COLORS = "WUBRG"
STAGES = ["child", "juvenile", "young_adult", "adult", "mature", "elder"]
EVEN = "W.2 U.2 B.2 R.2 G.2"
CYCLES = {"s1": "W>U U>B B>R R>G G>W", "s2": "W>B U>R B>G R>W G>U", "s3": "W>R U>G B>W R>U G>B", "s4": "W>G U>W B>U R>B G>R"}
CYCLES = {k: frozenset(v.split()) for k, v in CYCLES.items()}
D = {"D1": ("BG BR UG WR WU", "RG UB UR WB WG"), "D2": ("BG BR UR WG WU", "RG UB UG WB WR"),
     "D3": ("BG RG UB WR WU", "BR UG UR WB WG"), "D4": ("BG RG UR WB WU", "BR UB UG WG WR"),
     "D5": ("BG UB UR WG WR", "BR RG UG WB WU"), "D6": ("BG UG UR WB WR", "BR RG UB WG WU")}
canon = lambda s: "".join(c for c in COLORS if c in s)
PAIRSETS = {}
for k, (a, b) in D.items():
    for half, s in (("a", a), ("b", b)):
        ps = frozenset(canon(x) for x in s.split())
        PAIRSETS[ps] = f"{k}{half} pairs"
        PAIRSETS[frozenset(canon(set(COLORS) - set(p)) for p in ps)] = f"{k}{half} triads"
PAIRSETS[frozenset(canon(set(COLORS) - {c}) for c in COLORS)] = "four-color set"
VALUES = ["self-direction", "stimulation", "hedonism", "achievement", "power", "security", "conformity", "tradition",
          "benevolence", "universalism", "none clear"]
MARKS = ["hid a wrong", "owned up", "kept your word", "broke your word", "learned a skill", "took a wild risk", "left home",
         "stayed home", "moved away", "turned down a chance", "helped someone in need", "refused someone in need",
         "made an enemy", "made a friend", "defied an authority", "gave in to pressure", "came home",
         # next batch (Emren's point 11, engine 21:06): identity, drugs, crime and violence
         "came out", "kept it hidden", "used drugs", "broke the law", "hurt someone badly", "took a life",
         "named their gender"]   # N1 (chroma-identity, 2026-10-07): own gender named, beside 'came out' for who they love
FLAGS = ("habit", "door", "identity", "binds")
COLOR_WORDS = re.compile(r"\b(white|blue|black|red|green)\b", re.I)
DEFAULTS = {"everyday": (0.5, 2.0), "life event": (1.0, 0.3), "inner": (0.8, 0.3), "echo": (0.7, 0.3)}
SIT_KEYS = {"tier", "stages", "age", "calls", "alpha", "stakes", "rate", "tone", "life", "horizon", "roles", "plans",
            "earth", "tribal", "magic", "only", "per_year", "drivers", "times", "likelier", "rarer", "window", "gap",
            "requires", "after", "delay", "domain", "needs", "excludes", "rite", "source", "base", "layout", "cycle", "set",
            "once", "kills", "ends", "moves", "holds", "variant_of", "title", "drops", "grants", "takes", "suspends",
            "tenure", "threshold", "step", "transform",   # next batch: title stages and threshold seasons (engine 21:06)
            "share",   # the real lifetime share of people who ever meet an everyday moment (Library 23:45, for the engine)
            "share_group",   # one plain word: moments in the same group use one share draw (engine 01:50, for the packs)
            "time_of_year", "holy", "who", "cast_want", "group", "where", "at"}   # the outer world (world-fields.md, 2026-10-07)
# The outer world's words (copied from chroma-engine/prototype/world_keys.py, settled 2026-10-07; the engine's load_batch
# checks them again and stops on an unknown one). Several values are separated by commas.
WORLD_SIT = {
    "time_of_year": ["winter", "spring", "summer", "autumn"],
    "holy": ["feast", "fast", "pilgrimage", "mourning"],
    "who": ["parent", "grandparent", "elder", "sibling", "friend", "rival", "mentor", "boss", "colleague", "partner", "ex",
            "prospect", "child", "dead", "teacher", "neighbour"],
    "cast_want": ["money", "care", "successor", "grandchild", "love", "rival", "forgiveness", "home", "stop", "secret"],
    "group": ["household", "class", "work", "congregation", "club", "scene", "online", "neighbours", "gang", "unit", "ward",
              "movement"],
    "where": ["city", "town", "village", "remote", "capital", "suburb", "university", "port", "coast", "industry", "mining",
              "farming", "fishing", "mountain", "resort", "boom"],
    "at": ["school", "university", "employer", "bank", "hospital", "police", "court", "prison", "army", "faith body", "media",
           "party", "union", "charity", "council", "ministry"]}
LAW_KEYS = ["drugs", "divorce", "abortion", "same-sex marriage", "conscription", "guns", "gambling", "alcohol", "sex work",
            "euthanasia", "home schooling", "death penalty", "adoption"]
WORLD_OPT = {
    "law": LAW_KEYS,
    "norm": LAW_KEYS + ["cohabiting", "tattoos", "single parenthood", "faith in public", "leaving a faith", "coming out",
                        "role crossing", "transition", "mixed marriage"],   # 'role crossing' replaced 'women at work' (N1)
    # the role the world expects for one's sex (chroma-identity/for-the-engine.md): an act the world reserves for women
    # or men, or one that keeps or crosses the role the scene has just set out; never with norm: role crossing
    "role": ["women", "men", "keep", "cross"],
    "tech": ["phone", "computer", "internet", "video calls", "online dating", "remote work", "ai helper", "modern medicine",
             "car", "plane"],
    "lever": ["exit", "voice", "loyalty", "neglect", "subvert"],
    "pushes": ["close", "group", "place", "institution", "state", "economy", "culture", "tech", "nature", "belief", "abroad"]}
ONE_ONLY = {"holy", "cast_want", "group", "at", "law", "norm", "tech", "lever", "pushes", "role"}   # the engine reads one value of these


def world_values(k, v):
    """The values of an outer-world field that are not in its list (empty when all are known)."""
    if k == "pushes":   # a domain, optionally followed by a group kind, an institution kind or a who slot
        d_, *sub = v.split(None, 1)
        voc_ = {"group": WORLD_SIT["group"], "institution": WORLD_SIT["at"], "close": WORLD_SIT["who"]}.get(d_)
        return ([] if d_ in WORLD_OPT["pushes"] else [d_]) + ([sub[0]] if sub and (voc_ is None or sub[0] not in voc_) else [])
    xs = [x.strip() for x in v.split(",") if x.strip()]
    voc = WORLD_SIT.get(k) or WORLD_OPT[k]
    return [x for x in xs if x not in voc] + ([f"{v} (it takes one value)"] if k in ONE_ONLY and len(xs) > 1 else [])


class Problems(list):
    def add(self, where, msg):
        self.append(f"{where}: {msg}")


def weights(cols, total=1.0):
    n = len(cols)
    if n == 1:
        return f"{cols}1" if total == 1.0 else f"{cols}{str(total).lstrip('0')}"
    base = [round(1 / n, 2)] * n
    base[0] = round(1 - sum(base[1:]), 2)
    return " ".join(f"{c}{str(w).lstrip('0')}" for c, w in zip(cols, base))


def stages_of(s):
    s = s.strip()
    if s == "all":
        return " ".join(STAGES)
    if s.endswith("+"):
        return " ".join(STAGES[STAGES.index(s[:-1].replace(" ", "_")):])
    out = [x.replace(" ", "_") for x in re.split(r"[,\s]+", s) if x]
    return " ".join(out)


def rng(s, cast=int):
    a, b = re.split(r"\s*-\s*", s.strip())
    return (cast(a), cast(b))


def parse_option(line, where, P, tier):
    parts = [p.strip() for p in line[1:].split(" | ")]
    code, label, rest = parts[0].replace(" ", ""), parts[1], parts[2:]
    note, tags, diff = {}, "", None
    for f in rest:
        if f in FLAGS:
            note[f] = True
            continue
        if ":" not in f:
            P.add(where, f"unknown field '{f}' on '{label}'")
            continue
        k, v = [x.strip() for x in f.split(":", 1)]
        if k in ("earth", "tribal", "magic"):
            note.setdefault("world", {})[k] = v
        elif k == "tags":
            tags = v
        elif k == "diff":
            diff = float(v)
        elif k in ("v", "mark", "closed", "body", "impact", "also", "want", "act", "say"):
            note[k] = v
            if k == "closed":   # 2026-10-06 (release check L1): the engine reads the kind before the first ':', so it must be one it knows
                kind = v.split(":", 1)[0].strip()
                if kind not in ("law", "approval", "means") or ":" not in v:
                    P.add(where, f"closed must start with law:, approval: or means: and say what (closed: law: theft; backfire: ...), not '{v[:40]}' on '{label}'")
        elif k in ("title", "drops", "grants", "takes", "suspends", "requires"):   # titles and perks (engine 08:15)
            note[k] = v
        elif k.endswith("_if_fails") and k[:-9] in ("title", "drops", "grants", "takes", "suspends"):   # the same when the act fails
            note[k] = v
        elif k == "death_if_fails":   # next batch (engine 21:06): the share of failures that end the character's life
            try:
                note[k] = float(v)
                if not 0 < note[k] <= 1:
                    raise ValueError
            except ValueError:
                P.add(where, f"death_if_fails must be a share above 0 and at most 1, not '{v}' on '{label}'")
        elif k == "lacking":   # engine 23:20 (packs): without what the option requires, this share of the written chance
            try:
                note[k] = float(v)
                if not 0 < note[k] <= 1:
                    raise ValueError
            except ValueError:
                P.add(where, f"lacking must be a share above 0 and at most 1, not '{v}' on '{label}'")
        elif k == "aims":   # content packs (engine 21:06): the title a plan aiming at it seeks this act for
            note[k] = v.strip()
        elif k in ("kills", "kills_if_fails"):   # next batch (engine 21:06): the person in this role dies if the act works;
            # kills_if_fails (engine 22:32): the person dies if the act fails (grief, not a crime)
            if v.strip() in ("child",):
                P.add(where, f"{k}: never a child, on '{label}'")
            note[k] = v.strip()
        elif k == "moves":   # engine 22:32: this act moves the person (new people around, ties drop), as a situation's moves:
            if v.strip().lower() not in ("yes", "true", "1"):
                P.add(where, f"moves must be yes, not '{v}' on '{label}'")
            note[k] = True
        elif k == "for_years":
            try:
                note[k] = float(v)
            except ValueError:
                P.add(where, f"for_years must be a number, not '{v}' on '{label}'")
        elif k == "chance":   # base chance the act works for an ordinary person of the moment's ages, in percent (engine turns it into DIFF)
            try:
                c_ = float(v.rstrip("%"))
                if not 1 <= c_ <= 99:
                    raise ValueError
                note[k] = round(c_ / 100, 2)
            except ValueError:
                P.add(where, f"chance must be a percent from 1 to 99, not '{v}' on '{label}'")
        elif k == "without":
            if v not in ("law", "approval", "means", "impossible"):
                P.add(where, f"without must be law, approval, means or impossible, not '{v}' on '{label}'")
            note[k] = v
        elif k in WORLD_OPT:   # the outer world (world-fields.md, 2026-10-07): law:, norm:, tech:, lever:, pushes:, role:
            bad = world_values(k, v)
            if bad:
                P.add(where, f"{k}: unknown value {', '.join(repr(b) for b in bad)} on '{label}' (known: {', '.join(WORLD_OPT[k])})")
            note[k] = v
        elif k == "self_control":   # v7 discipline: "+" an act of discipline, "-" giving in or giving up
            if v not in ("+", "-"):
                P.add(where, f"self_control must be + or -, not '{v}' on '{label}'")
            note[k] = v
        else:
            P.add(where, f"unknown field '{k}' on '{label}'")
    if "role" in note and note.get("norm") == "role crossing":   # the engine would close it by approval twice
        P.add(where, f"role: and norm: role crossing on one option; keep one: '{label}'")
    m = re.fullmatch(r"([WUBRG]+)(?:>([WUBRG]+))?", code)
    if not m:
        P.add(where, f"bad color code '{code}' on '{label}'")
        return None
    means, ends = m.group(1), m.group(2)
    if canon(means) != means or (ends and canon(ends) != ends):
        P.add(where, f"write colors in WUBRG order: '{code}'")
    words = len(label.split())
    if words > 16:
        P.add(where, f"label has {words} words: '{label}'")
    if (re.search(r"\b(with|to|for|at|on|about|like|than|let|make|makes|help|helps|tell|tells|ask|asks|give|gives|show|"
                  r"hold|holds|call|calls|bother|bothers|follow|follows|need|needs|love|loves|hurt|hurts|against|from|"
                  r"behind|without|before|after|wronged|beat|beats)\s+you\b|\byours\b", label)
            and "act" not in note and tier != "read"):
        P.add(where, f"label has 'you' as an object; add act: so the narrator can tell it: '{label}'")
    if COLOR_WORDS.search(label):
        P.add(where, f"label uses a color word (check it is not about Magic's colors): '{label}'")
    if tier != "read":
        vs = note.get("v", "")
        if not vs:
            P.add(where, f"no value on '{label}'")
        elif not any(vs.startswith(x) or f", {x}" in vs for x in VALUES):
            P.add(where, f"value '{vs}' is not one of Schwartz's ten on '{label}'")
        mk = note.get("mark")
        if mk and mk not in MARKS:
            P.add(where, f"new mark '{mk}' (fine if an echo needs it; add it to the spec)")
    return dict(code=code, means=means, ends=ends, label=label, note=note, tags=tags, diff=diff)


def parse(text, P):
    sits, cur, ln = [], None, 0
    for ln, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("== "):
            cur = dict(name=line[3:].strip(), _opts=[], _line=ln)
            sits.append(cur)
        elif line.startswith("- "):
            if cur is None:
                P.add(f"line {ln}", "option before any situation")
                continue
            cur["_opts"].append((ln, line))
        elif ":" in line and cur is not None:
            k, v = [x.strip() for x in line.split(":", 1)]
            if k.split()[0] == "scene":
                cur.setdefault("_scenes", []).append((ln, k.split()[1:], v))
                continue
            if k in ("works", "fails"):
                cur.setdefault("_" + k, []).append(v)
                continue
            if k not in SIT_KEYS:
                P.add(f"{cur['name']} (line {ln})", f"unknown key '{k}'")
            cur[k] = v
        else:
            P.add(f"line {ln}", f"cannot read: {line[:60]}")
    return sits


SLOTS = {"N", "Ns", "parent", "grandparent", "elder", "sibling", "friend", "rival", "mentor", "boss", "colleague",
         "partner", "prospect", "child", "dead", "place", "disaster",
         "title",   # next batch (engine 21:06): the name of the title held, on moments with holds: kind:<kind>
         "seen_as"}   # N1: girl or boy, young woman or young man, woman or man, by the role the world expects of them
AGES = {"child": "k", "older": "a"}


def narrative(s, d, P):
    """The game's story fields (game thread, 2026-10-04 22:54): scenes per world with up to one variant per color,
    third person and present tense with {N} and role slots; two 'works' and two 'fails' lines, color-neutral."""
    where = s["name"]
    scenes, seen = {}, set()
    for ln, bits, text in s.get("_scenes", []):
        world, color, age = "earth", "", ""
        for b in bits:
            if b in ("earth", "tribal", "magic"):
                world = b
            elif b in AGES:
                age = AGES[b]
            elif re.fullmatch(r"[WUBRG]", b):
                color = b
            else:
                P.add(f"{where} (line {ln})", f"scene marker '{b}' should be a world, a color W U B R G, child or older")
        if (world, color, age) in seen:
            P.add(f"{where} (line {ln})", f"two {world} scenes for {color or 'untagged'} {age}")
        seen.add((world, color, age))
        check_text(text, f"{where} (line {ln})", P)
        scenes.setdefault(world, []).append((color, text, age) if age else (color, text))
    for k in ("works", "fails"):
        for t in s.get("_" + k, []):
            check_text(t, where, P)
    if scenes:
        d["scenes"] = scenes
        if "earth" not in scenes and not s.get("only"):   # a world-only moment (only: tribal) has its own world's scenes
            P.add(where, "no modern Earth scene")
    elif s["tier"] != "read":
        P.add(where, "no scene for the story layer")
    w, f = s.get("_works", []), s.get("_fails", [])
    if w or f:
        if len(w) != 2 or len(f) != 2:
            P.add(where, f"outcomes want two works and two fails lines (found {len(w)} and {len(f)})")
        d["outcomes"] = (w, f)
    elif s["tier"] != "read":
        P.add(where, "no works / fails lines")


def check_text(text, where, P):
    for slot in re.findall(r"\{(\w+)\}", text):
        if slot not in SLOTS:
            P.add(where, f"slot {{{slot}}} is not in the game's list")
    if re.search(r"\b(you|your|yours|yourself)\b", text, re.I):
        P.add(where, f"story text should be third person: '{text[:50]}'")


def layout_check(s, opts, P):
    """The balance layout of library-spec.md section 3, per situation."""
    where, tier = s["name"], s["tier"]
    if s.get("layout") == "free":
        return
    ones = [o["means"] for o in opts if len(o["means"]) == 1 and not o["ends"]]
    cross = frozenset(f"{o['means']}>{o['ends']}" for o in opts if o["ends"])
    combos = frozenset(o["means"] for o in opts if len(o["means"]) > 1 and not o["ends"])
    if sorted(ones) != sorted(COLORS):
        P.add(where, f"one-color options should be W U B R G once each, found {' '.join(ones) or 'none'}")
    if tier == "everyday":
        if len(canon(s.get("calls", ""))) not in (2, 3):
            P.add(where, "an everyday moment calls up 2 or 3 colors")
        if cross not in CYCLES.values():
            P.add(where, f"cross options are not one full cycle s1-s4: {' '.join(sorted(cross))}")
        if combos:
            P.add(where, "combinations belong in life events and crossroads, not everyday moments")
    elif tier == "life event":
        if combos and combos not in PAIRSETS:
            P.add(where, f"combinations are not a balanced set (D1-D6 half, its triads, or the four-color set): {' '.join(sorted(combos))}")
        if cross and cross not in CYCLES.values():
            P.add(where, f"cross options are not one full cycle: {' '.join(sorted(cross))}")
    elif tier in ("inner", "echo"):
        if combos:
            P.add(where, "inner drivers and echoes hold one-color options (plus optionally one cross cycle)")
        if cross and cross not in CYCLES.values():
            P.add(where, f"cross options are not one full cycle: {' '.join(sorted(cross))}")


def build_sit(s, P):
    where = s["name"]
    tier = s.get("tier", "")
    if tier not in DEFAULTS and tier != "read":
        P.add(where, f"tier '{tier}' should be everyday, life event, inner, echo or read")
        tier = "everyday"
    s["tier"] = tier
    opts = [o for o in (parse_option(line, f"{where} (line {ln})", P, tier) for ln, line in s["_opts"]) if o]
    worlds = {k: s[k] for k in ("earth", "tribal", "magic") if k in s}
    if tier == "read":
        if sorted(o["means"] for o in opts) != sorted(COLORS):
            P.add(where, "a read event has five readings, one per color")
        timing = {k: s[k] for k in ("times", "likelier", "rarer") if k in s}
        if "window" in s:
            timing["window"] = rng(s["window"])
        if "gap" in s:
            timing["gap_years"] = rng(s["gap"], float)
        readings = []
        for o in opts:
            n = o["note"]
            if not n.get("say"):
                P.add(where, f"reading '{o['label']}' has no say: line for the story layer")
            else:
                check_text(n["say"], where, P)
            readings.append((o["label"], f"{o['means']}1", float(n.get("impact", 1.0)), n.get("also", ""), n.get("want", o["means"]),
                             n.get("say", "")))
        d = dict(name=where, source=s.get("source", ""), tone=s.get("tone", ""), base=s.get("base", ""),
                 worlds=worlds, timing=timing, readings=readings)
        if s.get("_scenes"):
            narrative(s, d, P)
        return "read", d
    layout_check(s, opts, P)
    stakes, rate = DEFAULTS[tier]
    d = dict(name=where, stages=stages_of(s.get("stages", "all")))
    if "age" in s:
        d["age"] = rng(s["age"])
    else:
        P.add(where, "no age range")
    if "alpha" in s:
        d["alpha"] = s["alpha"]
    elif tier == "everyday":
        calls = canon(s.get("calls", ""))
        s["calls"] = calls
        d["alpha"] = " ".join(f"{c}{'.4' if c in calls else '.1'}" for c in COLORS)
    else:
        d["alpha"] = EVEN
    d["stakes"] = float(s.get("stakes", stakes))
    d["rate"] = float(s.get("rate", rate))
    for k in ("domain", "needs", "excludes", "rite", "kills", "ends"):
        if k in s:
            d[k] = s[k]
    if tier == "life event":
        if "per_year" in s:
            py = tuple(float(x) for x in s["per_year"].split())
            if len(py) != 6:
                P.add(where, "per_year needs six numbers, child to elder")
            d["per_year"] = py
            for st, r in zip(STAGES, py):
                if r > 0 and st not in d["stages"].split():
                    P.add(where, f"per_year is above zero for {st}, which is not in its stages")
        else:
            P.add(where, "a life event needs per_year")
        d["drivers"] = s.get("drivers", "")
    d["tier"] = tier
    for k in ("tone", "life", "horizon", "plans", "roles"):
        if k in s:
            d[k] = s[k]
    if s.get("once", "").lower() in ("yes", "true", "1"):
        d["once"] = True
    if s.get("moves", "").lower() in ("yes", "true", "1"):   # the event is a move: new people around, ties drop (engine 06:29)
        d["moves"] = True
    if s.get("holds"):   # a perk or title the whole moment needs (engine's requires; requires: here is an inner condition)
        d["requires"] = s["holds"]
    for k in ("title", "drops", "grants", "takes", "suspends"):   # the moment itself gives it, whatever is chosen (engine 17:40)
        if s.get(k):
            d[k] = s[k]
    if s.get("variant_of"):   # an age version of another situation: the same event for once, kills, rates and rules
        d["variant_of"] = s["variant_of"]
    # next batch (engine 21:06): title stages and threshold seasons
    if s.get("tenure"):   # with holds: only while the title held has been held lo to hi years
        try:
            d["tenure"] = rng(s["tenure"], float)
        except ValueError:
            P.add(where, f"tenure must be lo-hi years, not '{s['tenure']}'")
        if not s.get("holds"):
            P.add(where, "tenure: needs holds: (the title whose years it counts)")
    if s.get("threshold"):   # the season of crossing into that stage, or title:<name> (the season a title opens)
        th = s["threshold"].strip()
        if th.replace(" ", "_") not in STAGES[1:] and not th.startswith("title:"):
            P.add(where, f"threshold must be a stage after child, or title:<name>, not '{th}'")
        d["threshold"] = th.replace(" ", "_") if not th.startswith("title:") else th
        if s.get("step", "").strip() not in ("1", "2", "3"):
            P.add(where, "a threshold moment needs step: 1, 2 or 3")
        else:
            d["step"] = int(s["step"])
    if s.get("transform", "").lower() in ("yes", "true", "1"):
        d["transform"] = True
    if s.get("share"):   # a share of people who ever meet the moment in real life (the engine may draw who is eligible)
        try:
            d["share"] = float(s["share"])
            if not 0 < d["share"] <= 1:
                raise ValueError
        except ValueError:
            P.add(where, f"share must be above 0 and at most 1, not '{s['share']}'")
    if "share_group" in s:   # engine 01:50: one share draw for the group, so a smaller share is a subset of a larger one
        if re.fullmatch(r"[a-z0-9_-]+", s["share_group"].strip().lower()):
            d["share_group"] = s["share_group"].strip().lower()
        else:
            P.add(where, f"share_group must be one plain word, not '{s['share_group']}'")
    for k in WORLD_SIT:   # the outer world's moment fields, copied as written once their words are known
        if s.get(k):
            bad = world_values(k, s[k].strip())
            if bad:
                P.add(where, f"{k}: unknown value {', '.join(repr(b) for b in bad)} (known: {', '.join(WORLD_SIT[k])})")
            d[k] = s[k].strip()
    for k in ("tone", "life", "horizon", "roles"):
        if k not in s:
            P.add(where, f"no {k}")
    if worlds:
        d["worlds"] = worlds
        if "only" in s:
            d["only"] = s["only"]
        elif s.get("only") is None and len(worlds) < 3 and "earth" not in worlds:
            P.add(where, "no modern Earth wording")
    else:
        P.add(where, "no world wording (earth: at least)")
    if tier == "life event":
        t = {k: s[k] for k in ("times", "likelier", "rarer") if k in s}
        if "window" in s:
            t["window"] = rng(s["window"])
        if "gap" in s:
            t["gap_years"] = rng(s["gap"], float)
        d["timing"] = t
    elif "times" in s or "gap" in s:   # every tier keeps them (Book of Moments; engine 22:02 honours gap on everyday and inner)
        t = {"times": s["times"]} if "times" in s else {}
        if "gap" in s:
            t["gap_years"] = rng(s["gap"], float)
        d["timing"] = t
    if tier == "inner":
        if "requires" not in s:
            P.add(where, "an inner driver needs requires:")
        d["trigger"] = dict(requires=s.get("requires", ""), likelier=s.get("likelier", ""), rarer=s.get("rarer", ""))
    if tier == "echo":
        if "after" not in s:
            P.add(where, "an echo needs after:")
        d["after"] = s.get("after", "")
        d["delay_years"] = rng(s["delay"]) if "delay" in s else None
        d["likelier"] = s.get("likelier", "")
        d["rarer"] = s.get("rarer", "")
    out = []
    for o in opts:
        means = weights(o["means"])
        ends = weights(o["ends"], 0.7) if o["ends"] else None
        diff = o["diff"] if o["diff"] is not None else (.45 if len(o["means"]) == 1 and not o["ends"] else .5)
        out.append((o["label"], means, ends, diff, o["tags"], o["note"]))
    narrative(s, d, P)
    d["options"] = out
    return ("echo" if tier == "echo" else "sit"), d


def emit(name, sits, echoes, reads, src_lines):
    pp = lambda x: pprint.pformat(x, width=118, sort_dicts=False)
    head = (f'"""Chroma library {name}: compiled by build.py from {name}.lib (edit the .lib, not this file).\n\n'
            "Format the engine reads: a situation is dict(name, stages, age, alpha, stakes, options, rate, ...), an option is\n"
            "(label, means, ends or None, difficulty, tags); the 6th option element and extra situation keys are notes the engine\n"
            'ignores until it has fields for them. See library-spec.md.\n"""\n')
    body = [head]
    for title, lst in (("SITUATIONS", sits), ("ECHOES", echoes)):
        body.append(f"{title} = [")
        for d in lst:
            opts = d.pop("options")
            s = pp(d)[:-1] + ",\n 'options': [\n"
            s += "".join(f"    {o!r},\n" for o in opts) + " ]},"
            body.append(s)
            d["options"] = opts
        body.append("]\n")
    body.append("EVENTS_READ = " + pp(reads) + "\n")
    body.append("MARKS = {}\n")
    return "\n".join(body)


def main(name, out=None):
    src = name if name.endswith(".lib") else os.path.join(HERE, f"{name}.lib")
    outdir = os.path.dirname(os.path.abspath(src))
    name = os.path.basename(src)[:-4]
    P = Problems()
    if os.path.exists(src):
        raw = parse(open(src).read(), P)
    else:
        import glob
        parts = sorted(glob.glob(os.path.join(outdir, f"{name}-*.lib")))
        if not parts:
            sys.exit(f"no {name}.lib and no {name}-*.lib parts")
        raw = []
        for part in parts:
            got = parse(open(part).read(), P)
            for g in got:
                g["_part"] = os.path.basename(part)
            raw += got
        print("parts: " + ", ".join(os.path.basename(x) for x in parts))
    sits, echoes, reads = [], [], []
    names = set()
    for s in raw:
        if s["name"] in names:
            P.add(s["name"], "name used twice")
        names.add(s["name"])
        kind, d = build_sit(s, P)
        {"sit": sits, "echo": echoes, "read": reads}[kind].append(d)
    # pairs of everyday moments (consecutive, with complementary calls) must share gates and domain weights
    ev = [s for s in raw if s.get("tier") == "everyday"]
    i = 0
    while i + 1 < len(ev):
        a, b = ev[i], ev[i + 1]
        ca, cb = canon(a.get("calls", "")), canon(b.get("calls", ""))
        if ca and cb and not set(ca) & set(cb) and len(ca + cb) == 5:
            for k in ("needs", "excludes", "domain"):
                if a.get(k, "") != b.get(k, ""):
                    P.add(f"{a['name']} / {b['name']}", f"a balanced pair should share {k}: ('{a.get(k, '')}' vs '{b.get(k, '')}')")
            i += 2
        else:
            i += 1
    taken = {}
    for f in (os.path.join(HERE, "batch1.py"), os.path.join(HERE, "..", "chroma-engine", "prototype", "library.py")):
        if os.path.exists(f) and os.path.abspath(f) != os.path.join(outdir, f"{name}.py"):
            for nm in re.findall(r"""(?:name=|'name': )["']([^"']+)["']""", open(f).read()):
                taken[nm] = os.path.basename(f)
    for d in sits + echoes + reads:
        if d["name"] in taken:
            P.add(d["name"], f"name already used in {taken[d['name']]}")
    labels = {}
    for d in sits + echoes:
        for o in d["options"]:
            labels.setdefault(o[0], []).append(d["name"])
    for lab, where in labels.items():
        if len(where) > 1:
            P.add("labels", f"'{lab}' appears in {len(where)} situations: {', '.join(where)}")
    py = emit(name, sits, echoes, reads, None)
    vf = os.path.join(outdir, f"{name}_voice.py")   # the inner voice and the lessons (engine v7 VOICE and LESSONS), plain data
    if os.path.exists(vf) and not name.endswith(".lib"):
        vns = {}
        exec(compile(open(vf).read(), vf, "exec"), vns)
        for tab in ("VOICE", "LESSONS", "HEART_WHY", "HEAD_WHY"):
            if tab in vns:
                py += f"\n{tab} = " + pprint.pformat(vns[tab], width=118, sort_dicts=False) + "\n"
        print(f"voice: {len(vns.get('VOICE', {}))} voice keys, {len(vns.get('LESSONS', {}))} lesson keys from {os.path.basename(vf)}")
    ns = {}
    exec(compile(py, f"{name}.py", "exec"), ns)
    if out:
        os.makedirs(out, exist_ok=True)
    open(os.path.join(out or outdir, f"{name}.py"), "w").write(py)
    n_opt = sum(len(d["options"]) for d in sits + echoes)
    print(f"{name}.py: {len(sits)} situations, {len(echoes)} echoes, {len(reads)} read events, {n_opt} options")
    if P:
        print(f"{len(P)} problems:")
        for p in P:
            print("  -", p)
    else:
        print("no layout problems")
    return P


if __name__ == "__main__":
    a = sys.argv[1:]
    out = a[a.index("--out") + 1] if "--out" in a else None
    a = [x for i, x in enumerate(a) if x != "--out" and (i == 0 or a[i - 1] != "--out")]
    main(a[0] if a else "earth", out)
