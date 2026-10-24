"""Checks for the inner voice and the lessons (earth_voice.py), engine v7 explain.py keys.

    python3 check_voice.py [path/to/earth_voice.py] > checks_voice.md

Standard library only. The data file is loaded by path and no bytecode is written; so is earth_perks_titles.py from
the same folder, for the perk says. Nothing from the engine is imported: the few engine pieces needed (_fill,
predicate, plain_goal's words, KIND_NOUN, KIND_REF, plain_identity's words) are copied below. Exit status 1 if a check
fails.

What is checked, per line and per key:
  1. coverage: every voice, aside and lesson key is present (rite_quiet included), with exactly 2 "" (any color)
     variants and 2 or more for each of W U B R G, the same number for every color (4 for the most frequent keys), and
     no other keys or color tags; the five shadow states (next version, shadows.md: rigid, indecisive, ruthless,
     reckless, stuck in their ways) are optional voice keys, and when present hold exactly 4 "" variants and 2 in the
     shadow's own color, no other tags, no fills (engine, 2026-10-07);
  2. fills: a line uses only fills the engine replaces for its key (explain.before for voice keys and asides,
     explain.after's lesson(...) calls for lessons), and among those only the ones that are always filled and fit
     ({heart_why}/{head_why} only in torn, heart_over_head and head_over_heart, and only right after "because ";
     no {goal} or {need} outside the keys that guarantee them; never {perk} or {guild_name});
     plus the grammar the fill values need ("the {kind}", {kind_ref} never after an article or possessive, "becoming
     {guild}", "the {stage} years", goal_end starting "{goal}: {what}.", {dir} only as "{dir} {c}", no lower-case fill
     at a sentence start), and {c} used sparingly: only in a "" variant of the five keys whose default uses it, once a
     key at most; {what} after "is", "being" or "no longer" for a title's say; for perk_gain, perk_loss and
     perk_helped (a perk's say through explain.predicate: "can drive", "is a landlord") right after "{N} " or
     "someone who "; in the lacks aside (the raw say, a title's or a perk's) after a colon at the end of the line;
  3. length: at most 25 words for a voice line, 14 for an aside, 18 for a lesson, a fill counting as one word
     (the longest filled length over the sample fills and every engine value tried in check 11 is reported too);
  4. duplicates: no line appears twice anywhere in the file;
  5. color words: no white, blue, black, red, green (or their forms), and no Magic terms;
  plus style: voice lines in the first person without {N}; asides and lessons in the third person, asides with {N};
  option fills in curly quotes; no straight double quotes or curly apostrophes; every line ends a sentence; no digits;
  lessons without numbers or verdict words; a short safety word list; and the engine's own fill routine (copied
  from explain._fill) leaves no placeholder behind;
  10. why phrases: HEART_WHY and HEAD_WHY exist with exactly the engine's driver keys, each phrase in the first person
     (a first-person word, no {N}, no they/them/their for the character, no second person), under 9 words, with no
     fills, starting lower case (or "I") so it follows "because", without end punctuation, different from the other
     side's phrase for a shared driver, and free of color words, Magic terms, digits and safety words; every why is
     filled into every line that uses it, both passes of explain._fill, and the result must read as whole sentences
     with no placeholder left (the filled lengths are reported);
  11. engine values: every lesson line with a variable fill is filled with every value the engine can give it (all
     goal names plain_goal builds, the five kind nouns and references, every plain identity for {guild}, the five
     stages, every perk say in earth_perks_titles.py through explain.predicate); no placeholder may be left, no word
     doubled ("is is", "the the"), no article before {kind_ref}'s own, and every perk predicate must start with a
     present-tense verb (a past-tense say reads wrongly after "{N} ").
"""
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "earth_voice.py")
COLORS = "WUBRG"
TAGS = ("",) + tuple(COLORS)

VOICE_KEYS = ["agree", "heart_over_head", "head_over_heart", "torn", "want_but_doubt", "dream_calls", "duty",
              "need_first", "habit", "becoming", "time_short", "stuck"]
ASIDE_KEYS = ["stressed", "little_control", "disciplined", "undisciplined", "blind_spot", "out_of_reach", "hopeful",
              "gloomy", "short_horizon", "lacks"]
LESSON_KEYS = ["practice", "hard_win", "self_control_up", "self_control_down", "surprise_teaches", "fail_own_ways",
               "defended", "habit", "door", "binding", "backfire", "need_met", "duty_kept", "commit_start", "commit_end",
               "goal_step", "goal_setback", "sealed", "goal_end", "loss", "stress_up", "regret", "rite", "rite_quiet",
               "turning_point", "breakthrough", "closer_to", "drifting_from", "title_gain", "title_loss", "status_gain",
               "perk_gain", "perk_loss", "perk_helped"]
SHADOW_KEYS = {"rigid": "W", "indecisive": "U", "ruthless": "B", "reckless": "R", "stuck in their ways": "G"}
LIMIT = dict(voice=25, aside=14, lesson=18)

# ---- what the engine replaces (explain.py v7)
# before(): one fills dict for the moment's key and its asides: N heart head x goal need what, and heart_why head_why
# only when the character weighs some option (not when the key is "stuck"; an aside can come with "stuck").
# {what} is empty except in the "lacks" aside (the raw say of the title or perk the best way needs).
# heart_why / head_why: explain.before merges the world's HEART_WHY / HEAD_WHY over its own ({**HEART_WHY, **L[...]}).
_BEFORE = {"N", "heart", "head", "x", "goal", "need", "what", "heart_why", "head_why"}
RECEIVES = {k: set(_BEFORE) for k in VOICE_KEYS}
RECEIVES["stuck"] = _BEFORE - {"heart_why", "head_why"}
RECEIVES.update({k: set() for k in SHADOW_KEYS})   # a state's voice line comes with no fills
RECEIVES.update({k: _BEFORE - {"heart_why", "head_why"} for k in ASIDE_KEYS})   # {what}: set only with "lacks"
# after(): lesson(key, weight, **kw) with N always
_LESSON_KW = dict(practice="c", hard_win="", self_control_up="", self_control_down="", surprise_teaches="c dir",
                  fail_own_ways="", defended="", habit="", door="c", binding="", backfire="kind", need_met="need",
                  duty_kept="kind kind_ref", commit_start="kind kind_ref c", commit_end="kind kind_ref",
                  goal_step="goal", goal_setback="goal", sealed="goal", goal_end="goal what", loss="", stress_up="",
                  regret="", rite="stage", rite_quiet="stage", turning_point="c", breakthrough="",
                  closer_to="guild guild_name", drifting_from="guild guild_name lost", title_gain="what", title_loss="what", status_gain="what",
                  perk_gain="what perk", perk_loss="what perk", perk_helped="what perk")
LRECEIVES = {k: {"N"} | set(v.split()) for k, v in _LESSON_KW.items()}

# ---- among those, what is always filled and fits the line's voice
_OPT = {"heart", "head", "x"}            # agree and the agreeing keys: heart = head = x
_WHY = {"heart_why", "head_why"}
WHY_KEYS = ("torn", "heart_over_head", "head_over_heart")            # the only keys whose lines may give the reasons
USABLE = {k: set(_OPT) for k in VOICE_KEYS}
USABLE.update(heart_over_head={"heart", "head"} | _WHY, head_over_heart={"heart", "head"} | _WHY,
              torn={"heart", "head"} | _WHY, dream_calls=_OPT | {"goal"}, need_first=_OPT | {"need"}, stuck=set())
USABLE.update({k: {"N"} for k in ASIDE_KEYS})
USABLE.update({k: set() for k in SHADOW_KEYS})
USABLE["lacks"] = {"N", "what"}
TITLE_WHAT = {"title_gain", "title_loss", "status_gain"}            # {what} is a title's say: follows is / being / no longer
PRED_WHAT = {"perk_gain", "perk_loss", "perk_helped"}               # a perk's say as a predicate: after "{N} " / "someone who "
COLON_WHAT = {"lacks"}                                              # the raw say, a title's or a perk's: after a colon
LUSABLE = {k: v - {"perk", "guild_name"} for k, v in LRECEIVES.items()}
WHY_NOT = {"heart_why": "only in torn, heart_over_head and head_over_heart", "head_why": "only in torn, heart_over_head "
           "and head_over_heart", "goal": "empty unless the key is dream_calls", "need": "can be empty outside need_first",
           "N": "voice lines are first person", "x": "is the head's option here, say {head}",
           "heart": "empty when stuck", "head": "empty when stuck", "what": "empty outside the lacks aside",
           "perk": "the perk's catalogue name; the lines use {what}", "guild_name": "the guild's game name, a Magic term"}
C_KEYS = {"practice", "surprise_teaches", "door", "commit_start", "turning_point"}   # where the default uses {c}
ALL_FILLS = _BEFORE | {"c", "dir", "kind", "kind_ref", "stage", "guild", "guild_name", "perk", "lost"}
HEART_KEYS = ["motives", "habit", "needs", "role", "goals", "horizon", "exit"]           # explain.HEART_WHY's drivers
HEAD_KEYS = ["values", "becoming", "odds", "needs", "role", "goals", "horizon", "exit", "exit_out"]  # explain.HEAD_WHY's drivers (exit_out: leaving, engine 15:00)
WHY_MAX = 8   # words: under 9

# ---- the engine's fill values, copied from explain.py (nothing is imported)
KIND_NOUN = {"career": "job", "partner": "relationship", "children": "family", "community": "community", "faith": "faith"}
KIND_REF = {"career": "their work", "partner": "their relationship", "children": "family life", "community": "the community",
            "faith": "their faith"}
KIND_GOAL = {"career": "a working life", "partner": "a life together", "children": "a family",
             "community": "a place among others", "faith": "a faith to live by"}
GOAL_LEAD = {"dream": "the dream of", "passion": "the passion for", "plan": "the plan for"}
COLOR_NOUN = {"W": "doing right", "U": "understanding", "B": "getting ahead", "R": "freedom", "G": "belonging"}
COLOR_ADJ = {"W": "principled", "U": "thoughtful", "B": "driven", "R": "passionate", "G": "grounded"}
STAGES = ["juvenile", "young adult", "adult", "mature", "elder"]   # the stages a rite leads into (library.STAGES)


def _and(ws):
    return " and ".join([", ".join(ws[:-1]), ws[-1]] if len(ws) > 1 else ws)


def predicate(say):
    """explain.predicate, copied: a perk's say as something the character does or is."""
    return ("is " + say) if say.split(" ", 1)[0] in ("a", "an", "the", "in", "on", "known", "good", "from", "someone") else say


_ENDS = [KIND_GOAL[k] for k in KIND_GOAL] + [COLOR_NOUN[c] for c in COLOR_NOUN] + \
        [_and([COLOR_NOUN[a], COLOR_NOUN[b]]) for a in COLOR_NOUN for b in COLOR_NOUN if a != b]
GOALS = [f"{lead} {end}" for lead in GOAL_LEAD.values() for end in _ENDS]          # plain_goal, every shape it builds
GOAL_FALLBACK = [f"{lead} something of their own" for lead in GOAL_LEAD.values()]  # plain_goal with no mix (see notes)
SEALED = [f"the dream of {end}" for end in _ENDS]                                  # after(): "the passion for" -> "the dream of"
GOAL_ENDS = [g[0].upper() + g[1:] for g in GOALS]
GOAL_END_WHAT = ["achieved", "let go", "faded", "drifted away", "pushed aside", "not reached in time"]
GUILDS = []
for _m in range(1, 32):
    _cs = [c for i, c in enumerate("WUBRG") if _m >> i & 1]
    GUILDS.append(_and([COLOR_ADJ[c] for c in _cs]))                               # plain_identity

# sample values, for the filled length and the engine fill test
SAMPLE = dict(N="Ada", heart="shout back", head="walk away and cool off", x="walk away and cool off",
              goal="the dream of a working life", need="belonging", c="Red", dir="more", kind="family",
              kind_ref="family life", stage="young adult", guild="principled and thoughtful", what="not reached in time",
              heart_why="it feels right to me", head_why="it is what I believe in", perk="driving licence",
              guild_name="Azorius", lost="driven")
SAMPLE_KEY = dict(backfire=dict(kind="approval of others"), goal_end=dict(goal="The dream of a working life"),
                  sealed=dict(goal="the dream of freedom"), commit_start=dict(c="Red and Green"),
                  title_gain=dict(what="a nurse"), title_loss=dict(what="married"), status_gain=dict(what="a graduate"),
                  goal_step=dict(goal="the passion for freedom"), goal_setback=dict(goal="the plan for doing right and freedom"),
                  perk_gain=dict(what="can drive"), perk_loss=dict(what="is a landlord"),
                  perk_helped=dict(what="knows first aid"), lacks=dict(what="can drive"))
SAMPLE_TEXT = ("{N} = Ada; {heart} = shout back; {head} = {x} = walk away and cool off; {goal} = the dream of a working "
               "life (goal_step: the passion for freedom; goal_setback: the plan for doing right and freedom; sealed: the "
               "dream of freedom; goal_end: The dream of a working life); {need} = belonging; {c} = Red (commit_start: Red "
               "and Green); {dir} = more; {kind} = family (backfire: approval of others); {kind_ref} = family life; "
               "{stage} = young adult; {guild} = principled and thoughtful; {what} = not reached in time (title_gain: a "
               "nurse; title_loss: married; status_gain: a graduate; perk_gain: can drive; perk_loss: is a landlord; "
               "perk_helped: knows first aid; lacks: can drive); {heart_why} and {head_why}: the file's motives and "
               "values phrases")
PERKS_PATH = os.path.join(os.path.dirname(os.path.abspath(PATH)), "earth_perks_titles.py")


def present_tense(pred):
    """A perk predicate must start with a present-tense verb ("can", "is", "has", "knows", "always has")."""
    ws = pred.split()
    w = ws[1] if ws[0] == "always" and len(ws) > 1 else ws[0]
    return w in ("can", "is", "has", "does", "will") or (w.endswith("s") and not w.endswith("ss"))

COLOR_WORDS = re.compile(r"\b(white[s]?|whiter|whitest|blue[s]?|bluer|bluest|black[s]?|blacker|blackest|blackened|"
                         r"red[s]?|redder|reddest|reddish|reddened|green[s]?|greener|greenest|greenish)\b", re.I)
MAGIC_WORDS = re.compile(r"\b(colou?rs?|mana|planeswalker\w*|azorius|dimir|rakdos|gruul|selesnya|orzhov|izzet|golgari|"
                         r"boros|simic|bant|esper|grixis|jund|naya|abzan|jeskai|sultai|mardu|temur|mono)\b", re.I)
FIRST = re.compile(r"\b(I|I'm|I've|I'd|I'll|me|my|mine|myself|we|we're|us|our|ours|ourselves)\b")
FIRST_LOWER = re.compile(r"\b(me|my|mine|myself|we|we're|us|our|ours|ourselves)\b", re.I)
SECOND = re.compile(r"\b(you|your|yours|yourself|you're|you've)\b", re.I)
NUMBER_WORDS = re.compile(r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|"
                          r"hundred|thousand|million|half|twice|double|triple|percent|second|third)\b", re.I)
VERDICT = re.compile(r"\b(should|must|ought|evil|wicked|sinful|shameful|deserves?|virtuous|good person|bad person)\b", re.I)
REVIEW = re.compile(r"\b(right|wrong|good|bad|better|worse)\b", re.I)
SAFETY = re.compile(r"\b(blood\w*|kill\w*|murder\w*|guns?|knife|knives|stab\w*|sex\w*|naked|drunk\w*|drugs?|suicid\w*|"
                    r"die|dies|dying|corpse\w*|tortur\w*|rape\w*|abus\w*|weapon\w*)\b", re.I)
FILL = re.compile(r"\{([^{}]*)\}")


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load(path):
    return load_file(path, "earth_voice_under_check")


def words(line):
    return len(FILL.sub("X", line).split())


def engine_fill(line, **kw):
    """explain._fill, copied: two passes, since fills can carry fills."""
    out = line
    for _ in range(2):
        for k_, v_ in kw.items():
            out = out.replace("{" + k_ + "}", str(v_))
    return out


def sample_for(key, group):
    s = dict(SAMPLE)
    s.update(SAMPLE_KEY.get(key, {}) if group == "lesson" or key == "lacks" else {})
    return s


def main():
    mod = load(PATH)
    VOICE = getattr(mod, "VOICE", None)
    LESSONS = getattr(mod, "LESSONS", None)
    HW = getattr(mod, "HEART_WHY", None)
    RW = getattr(mod, "HEAD_WHY", None)
    fails = {}          # check name -> list of messages
    notes = []
    if isinstance(HW, dict) and isinstance(HW.get("motives"), str):
        SAMPLE["heart_why"] = HW["motives"]          # the phrase the engine falls back on
    if isinstance(RW, dict) and isinstance(RW.get("values"), str):
        SAMPLE["head_why"] = RW["values"]

    def fail(check, msg):
        fails.setdefault(check, []).append(msg)

    for name, d in (("VOICE", VOICE), ("LESSONS", LESSONS)):
        if not isinstance(d, dict):
            fail("1 coverage", f"{name} is missing or not a dict")
    if "1 coverage" in fails:
        print("\n".join(fails["1 coverage"]))
        return 1

    rows = []           # (group, key, tag, line)
    groups = [("voice", VOICE, VOICE_KEYS), ("aside", VOICE, ASIDE_KEYS), ("lesson", LESSONS, LESSON_KEYS)]
    for name, d, known in (("VOICE", VOICE, VOICE_KEYS + ASIDE_KEYS + list(SHADOW_KEYS)), ("LESSONS", LESSONS, LESSON_KEYS)):
        for k in d:
            if k not in known:
                fail("1 coverage", f"{name} has an unknown key: {k}")
    table = []
    for group, d, keys in groups:
        for k in keys:
            vs = d.get(k)
            if not isinstance(vs, list):
                fail("1 coverage", f"{group} key missing: {k}")
                table.append((group, k, None))
                continue
            counts = {t: 0 for t in TAGS}
            for v in vs:
                if not (isinstance(v, tuple) and len(v) == 2 and all(isinstance(x, str) for x in v)):
                    fail("1 coverage", f"{k}: a variant is not a (color, line) tuple of strings: {v!r}")
                    continue
                tag, line = v
                if tag not in TAGS:
                    fail("1 coverage", f"{k}: unknown color tag {tag!r} (use \"\" or one of W U B R G)")
                    continue
                counts[tag] += 1
                rows.append((group, k, tag, line))
            if counts[""] != 2:
                fail("1 coverage", f"{k}: {counts['']} any-color variants, expected 2")
            for t in COLORS:
                if counts[t] < 2:
                    fail("1 coverage", f"{k}: {counts[t]} variants for {t}, expected 2 or more")
            if len({counts[t] for t in COLORS}) > 1:
                fail("1 coverage", f"{k}: colors have different numbers of variants: "
                                   + " ".join(f"{t} {counts[t]}" for t in COLORS))
            table.append((group, k, counts))
    for k, own in SHADOW_KEYS.items():   # optional: only in a batch written for the shadows
        vs = VOICE.get(k)
        if vs is None:
            continue
        counts = {t: 0 for t in TAGS}
        for v in vs if isinstance(vs, list) else []:
            if not (isinstance(v, tuple) and len(v) == 2 and all(isinstance(x, str) for x in v)) or v[0] not in ("", own):
                fail("1 coverage", f"{k}: a variant must be a (color, line) tuple tagged \"\" or {own}: {v!r}")
                continue
            counts[v[0]] += 1
            rows.append(("voice", k, v[0], v[1]))
        if counts[""] != 4 or counts[own] != 2:
            fail("1 coverage", f"{k}: {counts['']} any-color and {counts[own]} {own} variants, expected 4 and 2")
        table.append(("voice", k, counts))

    # ---- per line
    seen = {}
    c_use = {}
    maxw = {}
    for group, k, tag, line in rows:
        where = f"{k} [{tag or 'any'}]: {line}"
        used = FILL.findall(line)
        rec = LRECEIVES[k] if group == "lesson" else RECEIVES[k]
        use = LUSABLE[k] if group == "lesson" else USABLE[k]
        for f in used:
            if f not in ALL_FILLS:
                fail("2 fills", f"unknown placeholder {{{f}}}: {where}")
            elif f not in rec:
                fail("2 fills", f"{{{f}}} is not filled for this key, it would show as is: {where}")
            elif f not in use:
                fail("2 fills", f"{{{f}}} is filled but not usable here ({WHY_NOT.get(f, 'see header')}): {where}")
        # grammar the fill values need
        for m in re.finditer(r"\{(goal|need|kind|kind_ref|stage|dir|what|guild|heart_why|head_why)\}", line):
            pre = line[:m.start()]
            if (pre.strip() == "" or re.search(r"[.!?]\s*$", pre)) and not (k == "goal_end" and m.group(1) == "goal"):
                fail("2 fills", f"lower-case fill {{{m.group(1)}}} at a sentence start: {where}")
        for m in re.finditer(r"\{what\}", line):
            pre, post = line[:m.start()], line[m.end():]
            if k in TITLE_WHAT and not re.search(r"(\bis|\bbeing|no longer) $", pre, re.I):
                fail("2 fills", f"{{what}} (a title's say) must follow \"is\", \"being\" or \"no longer\": {where}")
            if k in PRED_WHAT and not (pre.endswith("{N} ") or pre.endswith("someone who ")):
                fail("2 fills", f"{{what}} (a perk's say as a predicate, \"can drive\", \"is a landlord\") must follow "
                                f"\"{{N}} \" or \"someone who \": {where}")
            if k in COLON_WHAT and not (pre.endswith(": ") and post.startswith(".")):
                fail("2 fills", f"{{what}} (the raw say, some are nouns) must come after a colon and end a sentence: {where}")
            if k == "goal_end" and not pre.endswith("{goal}: "):
                fail("2 fills", f"goal_end's {{what}} follows \"{{goal}}: \": {where}")
        if k == "goal_end" and not line.startswith("{goal}: {what}."):
            fail("2 fills", f"goal_end must start with \"{{goal}}: {{what}}.\" ({{goal}} is capitalised): {where}")
        for m in re.finditer(r"\{kind\}", line):
            pre = line[:m.start()]
            ok = pre.endswith("the ") or (k == "backfire" and pre.endswith("no "))
            if not ok:
                fail("2 fills", f"{{kind}} must read \"the {{kind}}\" (\"no {{kind}}\" in backfire): {where}")
        for m in re.finditer(r"\{kind_ref\}", line):
            pre = line[:m.start()]
            if re.search(r"(\b(the|a|an|their|his|her|its|our|my|this|that|no)|'s) $", pre, re.I):
                fail("2 fills", f"{{kind_ref}} brings its own article (\"their work\", \"the community\"): {where}")
        for m in re.finditer(r"\{(heart_why|head_why)\}", line):
            if not line[:m.start()].endswith("because "):
                fail("2 fills", f"{{{m.group(1)}}} is written to follow \"because \": {where}")
        lead_ = "being" if k == "drifting_from" else "becoming"   # drifting_from: what stays ("being {guild}", or "no one in particular")
        if "{guild}" in line and f"{lead_} {{guild}}" not in line:
            fail("2 fills", f"{{guild}} must read \"{lead_} {{guild}}\" (plain words, \"principled and thoughtful\"): {where}")
        if "{stage}" in line and not re.search(r"\b[Tt]he \{stage\} years", line):
            fail("2 fills", f"{{stage}} must read \"the {{stage}} years\": {where}")
        if "{dir}" in line and "{dir} {c}" not in line:
            fail("2 fills", f"{{dir}} only as \"{{dir}} {{c}}\": {where}")
        if "{c}" in line:
            if k not in C_KEYS or tag != "" or group != "lesson":
                fail("2 fills", f"{{c}} only in a \"\" lesson variant of {', '.join(sorted(C_KEYS))}: {where}")
            c_use[k] = c_use.get(k, 0) + 1
        for f in ("heart", "head", "x"):
            for m in re.finditer(r"\{" + f + r"\}", line):
                if line[m.start() - 1:m.start()] != "“" or line[m.end():m.end() + 1] != "”":
                    fail("7 style", f"{{{f}}} not in curly quotes: {where}")
        # length
        n = words(line)
        filled = engine_fill(line, **sample_for(k, group))
        nf = len(filled.split())
        mw = maxw.setdefault((group, k), [0, 0])
        mw[0] = max(mw[0], n); mw[1] = max(mw[1], nf)
        if n > LIMIT[group]:
            fail("3 length", f"{n} words (limit {LIMIT[group]}): {where}")
        # duplicates
        norm = re.sub(r"\s+", " ", line.strip().lower())
        if norm in seen:
            fail("4 duplicates", f"also in {seen[norm]}: {where}")
        else:
            seen[norm] = f"{k} [{tag or 'any'}]"
        # color words and Magic terms
        text = FILL.sub(" ", line)
        for m in COLOR_WORDS.finditer(text):
            fail("5 color words", f"\"{m.group(0)}\": {where}")
        for m in MAGIC_WORDS.finditer(text):
            fail("5 color words", f"Magic term \"{m.group(0)}\": {where}")
        # person and voice
        if group == "voice":
            if not (FIRST.search(text) or FIRST_LOWER.search(text)):
                fail("6 person", f"voice line without a first-person word: {where}")
            if "{N}" in line:
                fail("6 person", f"voice line names {{N}} (the inner voice is first person): {where}")
        else:
            if FIRST.search(text) or FIRST_LOWER.search(text):
                fail("6 person", f"{group} in the first person: {where}")
            if SECOND.search(text):
                fail("6 person", f"{group} in the second person: {where}")
            if group == "aside" and "{N}" not in line:
                fail("6 person", f"aside without {{N}}: {where}")
        # style
        if '"' in line:
            fail("7 style", f"straight double quote: {where}")
        if "’" in line or "‘" in line:
            fail("7 style", f"curly apostrophe (the defaults use '): {where}")
        if line.count("“") != line.count("”"):
            fail("7 style", f"unbalanced curly quotes: {where}")
        if line != line.strip() or "  " in line:
            fail("7 style", f"stray spaces: {where}")
        if not line.rstrip("”")[-1:] in ".!?":
            fail("7 style", f"does not end a sentence: {where}")
        if re.search(r"\d", text):
            fail("8 numbers and verdicts", f"digit: {where}")
        if group == "lesson":
            for m in NUMBER_WORDS.finditer(text):
                fail("8 numbers and verdicts", f"number word \"{m.group(0)}\" in a lesson: {where}")
            for m in VERDICT.finditer(text):
                fail("8 numbers and verdicts", f"verdict word \"{m.group(0)}\" in a lesson: {where}")
            for m in REVIEW.finditer(text):
                notes.append(f"lesson word \"{m.group(0)}\" (read as outcome or comparison, not as a verdict?): {where}")
        for m in SAFETY.finditer(text):
            fail("9 safety", f"\"{m.group(0)}\": {where}")
        # the engine's fill routine, with what the engine passes for this key (stuck and asides may get empty labels)
        kw = {f: SAMPLE[f] for f in rec}
        kw.update({f: v for f, v in sample_for(k, group).items() if f in rec})
        out = engine_fill(line, **kw)
        if FILL.sub("", out.replace("{N}", "")) != out.replace("{N}", ""):
            fail("2 fills", f"placeholder left after the engine's fill: {out}")
    for k, n in c_use.items():
        if n > 1:
            fail("2 fills", f"{k}: {{c}} used {n} times, at most once a key")

    # ---- 10 why phrases: HEART_WHY and HEAD_WHY, and every why filled into every line that uses it
    W10 = "10 why phrases"
    why_rows = []        # (side, driver, phrase, words)
    for side, d, keys in (("HEART_WHY", HW, HEART_KEYS), ("HEAD_WHY", RW, HEAD_KEYS)):
        if not isinstance(d, dict):
            fail(W10, f"{side} is missing or not a dict (explain.before would use the engine's third-person phrases)")
            continue
        if set(d) != set(keys):
            fail(W10, f"{side} keys differ from the engine's ({', '.join(keys)}): missing "
                      f"{', '.join(k_ for k_ in keys if k_ not in d) or 'none'}; unknown {', '.join(k_ for k_ in d if k_ not in keys) or 'none'}")
        for drv, ph in d.items():
            w_ = f"{side}[{drv!r}] = {ph!r}"
            if not isinstance(ph, str) or not ph.strip():
                fail(W10, f"not a phrase: {w_}")
                continue
            n_ = len(ph.split())
            why_rows.append((side, drv, ph, n_))
            if "{" in ph or "}" in ph:
                fail(W10, f"a fill inside a why ({{goal}} and {{need}} can be empty when it is drawn; {{N}} is third person): {w_}")
            if not (FIRST.search(ph) or FIRST_LOWER.search(ph)):
                fail(W10, f"no first-person word (the voice lines are the character's own): {w_}")
            if re.search(r"\b(they|them|their|theirs|themselves|themself|they're|they've|they'd)\b", ph, re.I):
                fail(W10, f"third person for the character: {w_}")
            if SECOND.search(ph):
                fail(W10, f"second person: {w_}")
            if n_ > WHY_MAX:
                fail(W10, f"{n_} words (under 9): {w_}")
            if not (ph[0].islower() or ph.startswith("I ")):
                fail(W10, f"must start lower case (or with \"I\") to follow \"because\": {w_}")
            if ph.rstrip()[-1:] in ".!?,;:":
                fail(W10, f"end punctuation (the line ends the sentence): {w_}")
            if ph != ph.strip() or "  " in ph or '"' in ph or "’" in ph or "‘" in ph:
                fail(W10, f"stray spaces, straight double quotes or curly apostrophes: {w_}")
            for m in COLOR_WORDS.finditer(ph):
                fail(W10, f"color word \"{m.group(0)}\": {w_}")
            for m in MAGIC_WORDS.finditer(ph):
                fail(W10, f"Magic term \"{m.group(0)}\": {w_}")
            if re.search(r"\d", ph):
                fail(W10, f"digit: {w_}")
            for m in SAFETY.finditer(ph):
                fail(W10, f"safety word \"{m.group(0)}\": {w_}")
    if isinstance(HW, dict) and isinstance(RW, dict):
        for drv in sorted(set(HW) & set(RW)):
            if HW[drv] == RW[drv]:
                fail(W10, f"heart and head give the same reason for {drv!r}, so a torn line could repeat it: {HW[drv]!r}")
    hw = [v for v in (HW or {}).values() if isinstance(v, str)] if isinstance(HW, dict) else []
    rw = [v for v in (RW or {}).values() if isinstance(v, str)] if isinstance(RW, dict) else []
    why_lines = []       # (key, tag, line, words, min filled, max filled, pairs)
    for group, k, tag, line in rows:
        if "{heart_why}" not in line and "{head_why}" not in line:
            continue
        hs = (hw or [SAMPLE["heart_why"]]) if "{heart_why}" in line else [SAMPLE["heart_why"]]
        rs = (rw or [SAMPLE["head_why"]]) if "{head_why}" in line else [SAMPLE["head_why"]]
        lens = []
        bad = set()
        for h in hs:
            for r in rs:
                # explain.before's fills, in its order; goal, need and what are empty when the reason is drawn
                kw = dict(N="{N}", heart=SAMPLE["heart"], head=SAMPLE["head"], x=SAMPLE["x"], goal="", need="", what="",
                          heart_why=h, head_why=r)
                o_ = engine_fill(line, **kw)
                lens.append(len(o_.split()))
                if FILL.search(o_):
                    bad.add(f"a placeholder is left (or {{N}}, third person): {o_}")
                if re.search(r"[.!?]”? [a-z]", o_) or re.search(r"\s[.,;:!?]", o_) or re.search(r"[.,;:]{2}", o_):
                    bad.add(f"does not read as whole sentences: {o_}")
                if re.search(r"\bbecause (?![a-z]|I\b)", o_):
                    bad.add(f"\"because\" is not followed by a clause: {o_}")
                if re.search(r"\b(\w+) \1\b", o_, re.I):
                    bad.add(f"a doubled word: {o_}")
        for m_ in sorted(bad):
            fail(W10, f"{k} [{tag or 'any'}]: {m_}")
        why_lines.append((k, tag, line, words(line), min(lens), max(lens), len(lens)))
        mw = maxw.setdefault((group, k), [0, 0])
        mw[1] = max(mw[1], max(lens))
    for k in WHY_KEYS:
        if not any(kk == k for kk, *_ in why_lines):
            fail(W10, f"{k}: no line gives the reasons ({{heart_why}} / {{head_why}}); one \"\" line should")

    # ---- 11 engine values: every value the engine can give a variable fill, in every line that uses it
    W11 = "11 engine values"
    perk_says = []
    perk_lost = {}       # predicate -> the catalogue's "lost" words
    if os.path.exists(PERKS_PATH):
        try:
            pm = load_file(PERKS_PATH, "earth_perks_titles_under_check")
            perk_says = [p_["say"] for p_ in getattr(pm, "PERKS", []) if isinstance(p_, dict) and isinstance(p_.get("say"), str)]
            perk_lost = {predicate(p_["say"]): str(p_.get("lost", "")) for p_ in getattr(pm, "PERKS", [])
                         if isinstance(p_, dict) and isinstance(p_.get("say"), str)}
        except Exception as e_:          # a broken catalogue is check_perks_titles.py's business; say so here
            fail(W11, f"earth_perks_titles.py could not be loaded: {e_!r}")
    preds = [predicate(x_) for x_ in perk_says]
    for x_, p_ in zip(perk_says, preds):
        if not present_tense(p_):
            fail(W11, f"perk say {x_!r} is not in the present tense: \"{{N}} {p_}\" reads wrongly (say \"has ...\", \"can ...\")")
    KINDS = [dict(kind=KIND_NOUN[k_], kind_ref=KIND_REF[k_]) for k_ in KIND_NOUN]
    NEEDS = ["safety", "belonging", "autonomy", "competence", "meaning"]
    VALUES = dict(dream_calls=[dict(goal=g_) for g_ in GOALS], need_first=[dict(need=n_) for n_ in NEEDS],
                  need_met=[dict(need=n_) for n_ in NEEDS],
                  goal_step=[dict(goal=g_) for g_ in GOALS + GOAL_FALLBACK],
                  goal_setback=[dict(goal=g_) for g_ in GOALS + GOAL_FALLBACK],
                  sealed=[dict(goal=g_) for g_ in SEALED],
                  goal_end=[dict(goal=g_, what=w_) for g_ in GOAL_ENDS for w_ in GOAL_END_WHAT],
                  duty_kept=KINDS, commit_start=KINDS, commit_end=KINDS,
                  rite=[dict(stage=x_) for x_ in STAGES], rite_quiet=[dict(stage=x_) for x_ in STAGES],
                  closer_to=[dict(guild=g_) for g_ in GUILDS],
                  drifting_from=[dict(guild=g_, lost=l_) for g_ in GUILDS + ["no one in particular"] for l_ in COLOR_ADJ.values()],
                  perk_gain=[dict(what=p_) for p_ in preds], perk_loss=[dict(what=p_) for p_ in preds],
                  perk_helped=[dict(what=p_) for p_ in preds])
    tried = {}
    try_keys = {("voice", "dream_calls"), ("voice", "need_first")} | {("lesson", k) for k in VALUES if k in LESSON_KEYS}
    for group, k, tag, line in rows:
        if (group, k) not in try_keys:
            continue
        rec = LRECEIVES[k] if group == "lesson" else RECEIVES[k]
        top = 0
        for v_ in VALUES[k]:
            kw = {f: SAMPLE[f] for f in rec if f in SAMPLE}
            kw.update({f: v for f, v in sample_for(k, group).items() if f in rec})
            kw.update(v_)
            kw["N"] = "Ada"
            o_ = engine_fill(line, **kw)
            top = max(top, len(o_.split()))
            where = f"{k} [{tag or 'any'}] with {', '.join(f'{a}={b!r}' for a, b in v_.items())}: {o_}"
            if FILL.search(o_):
                fail(W11, f"placeholder left: {where}")
            m_ = re.search(r"\b(\w+) \1\b", o_, re.I)
            if m_:
                fail(W11, f"doubled word \"{m_.group(0)}\": {where}")
            m_ = re.search(r"\b(the|a|an|their|its)\s+(the|a|an|their|its)\b", o_, re.I)
            if m_:
                fail(W11, f"two articles \"{m_.group(0)}\": {where}")
        tried[k] = (len(VALUES[k]), max(tried.get(k, (0, 0))[1], top))
        mw = maxw.setdefault((group, k), [0, 0])
        mw[1] = max(mw[1], top)

    # ---- engine notes
    notes_engine = []
    pooled = sum(1 for _, d, keys in groups for k in keys if isinstance(d.get(k), list))
    notes_engine.append(f"explain._pick pools the strongest color's lines with the \"\" lines (all {pooled} keys have "
                        "both), so the any-color lines are in play: with two of them beside n lines for the color, each "
                        "turns up about once in 2 + n draws. That is also how often a {c} line or a line that gives "
                        "the reasons ({heart_why} / {head_why}, all \"\" variants) is seen.")
    lost_ = lambda p_: f" (lost: {perk_lost[p_]})" if perk_lost.get(p_) else ""
    awk = [p_ for p_ in preds if p_.startswith("is someone")]
    if awk:
        notes_engine.append("explain.predicate keeps the say's own \"someone\", so after \"someone who\" (perk_loss) it "
                            "reads twice: " + "; ".join(f"\"{{N}} is no longer someone who {p_}\"{lost_(p_)}" for p_ in awk) +
                            ". A say without \"someone\" (\"not to be crossed\") would read in every shape.")
    perf = [p_ for p_ in preds if re.match(r"^has (\w+ed|come|gone|done|been|become|grown|taken|given)\b", p_)]
    if perf:
        notes_engine.append("Perfect-tense says read well after \"{N} \" and \"It helped that\", less well once lost "
                            "(perk_loss): " + "; ".join(f"\"{{N}} is no longer someone who {p_}\"{lost_(p_)}" for p_ in perf) + ".")
    last = [p_ for p_ in preds if "at last" in p_]
    if last:
        notes_engine.append("A say with \"at last\" reads oddly once the perk is gone (perk_loss): " +
                            "; ".join(f"\"{{N}} is no longer someone who {p_}\"{lost_(p_)}" for p_ in last) + ".")
    if any(g == "voice" and "{goal}" in ln for g, _, _, ln in rows):
        notes_engine.append("plain_goal's fallback for a goal with no mix, \"" + GOAL_FALLBACK[0] + "\", is third "
                            "person; in the inner voice (dream_calls) it would read \"I ... " + GOAL_FALLBACK[0] +
                            "\". \"something of my own\" there, or \"something of one's own\" everywhere, would fit.")
    if not perk_says:
        notes_engine.append("earth_perks_titles.py was not found next to the data file: the perk says were not tried.")

    # ---- report
    out = ["# Checks: the inner voice and the lessons (earth_voice.py)", "",
           f"File: `{os.path.relpath(PATH, HERE)}` (run from `chroma-library/drafts/`: `python3 check_voice.py > checks_voice.md`).", "",
           f"{len(rows)} lines in {len(table)} keys: {len(VOICE_KEYS)} voice keys, {len(ASIDE_KEYS)} asides, "
           f"{len(LESSON_KEYS)} lessons; {len(why_rows)} why phrases (HEART_WHY {len(HW or {}) if isinstance(HW, dict) else 0}, "
           f"HEAD_WHY {len(RW or {}) if isinstance(RW, dict) else 0}).", ""]
    names = ["1 coverage", "2 fills", "3 length", "4 duplicates", "5 color words", "6 person", "7 style",
             "8 numbers and verdicts", "9 safety", W10, W11]
    out += ["## Results", "", "| Check | Result |", "| --- | --- |"]
    for nm in names:
        out.append(f"| {nm} | {'FAIL (' + str(len(fails[nm])) + ')' if nm in fails else 'pass'} |")
    for nm in names:
        if nm in fails:
            out += ["", f"### {nm}: failures", ""] + [f"- {m}" for m in fails[nm]]
    out += ["", "## Per key", "",
            "Counts per color tag, the longest line in words (a fill counts as one word; limit in brackets), the longest "
            "once filled (with the sample fills, every why pair and every engine value tried in check 11), and the fills "
            "used.", "",
            "| Group | Key | any | W | U | B | R | G | Total | Longest | With fills | Fills used |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for group, k, counts in table:
        if counts is None:
            out.append(f"| {group} | {k} | missing | | | | | | | | | |")
            continue
        used = sorted({f for g, kk, _, ln in rows if g == group and kk == k for f in FILL.findall(ln)})
        mw = maxw.get((group, k), [0, 0])
        out.append(f"| {group} | {k} | " + " | ".join(str(counts[t]) for t in TAGS) +
                   f" | {sum(counts.values())} | {mw[0]} ({LIMIT[group]}) | {mw[1]} | "
                   + (" ".join("{" + f + "}" for f in used) or "none") + " |")
    out += ["", "Sample fills: " + SAMPLE_TEXT + "."]
    out += ["", "## Why phrases", "",
            "HEART_WHY and HEAD_WHY, as the inner voice says them after \"because\", with their length in words (under 9).", "",
            "| Side | Driver | Phrase | Words |", "| --- | --- | --- | --- |"]
    out += [f"| {sd} | {dv} | {ph} | {n_} |" for sd, dv, ph, n_ in why_rows]
    out += ["", "Lines that give the reasons, filled with every phrase they can draw (explain._fill, both passes) and the "
                "sample options: words with a fill counted as one, and the shortest and longest filled.", "",
            "| Key | Color | Line | Words | Filled | Pairs tried |", "| --- | --- | --- | --- | --- | --- |"]
    out += [f"| {k} | {t or 'any'} | {ln} | {n_} | {lo}-{hi} | {pr} |" for k, t, ln, n_, lo, hi, pr in why_lines]
    out += ["", "## Engine values tried", "",
            f"{len(GOALS)} goal names (plain_goal: dream, passion, plan of every domain, color and pair; the lessons "
            f"also get its {len(GOAL_FALLBACK)} fallbacks), "
            f"{len(SEALED)} sealed dream names, {len(GOAL_ENDS) * len(GOAL_END_WHAT)} goal endings, "
            f"{len(KINDS)} kinds (noun and reference), {len(GUILDS)} plain identities, {len(STAGES)} stages, "
            f"{len(preds)} perk says through explain.predicate (earth_perks_titles.py).", "",
            "| Key | Values | Longest filled |", "| --- | --- | --- |"]
    out += [f"| {k} | {n_} | {top} |" for k, (n_, top) in tried.items()]
    out += ["", "## Notes for the engine", ""] + [f"- {m}" for m in notes_engine]
    out += ["", "## For review (not failures)", "",
            "Lesson lines with right, wrong, good, bad, better or worse, to confirm each reads as an outcome or a comparison "
            "and not as a moral verdict:", ""] + ([f"- {m}" for m in notes] or ["- none"])
    print("\n".join(out))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
