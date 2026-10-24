"""Checks for the played game's story words (earth_story.py): the song, the last conversation, the voice, the thread,
the world in their life and the disaster readings.

    python3 -B check_story.py [path/to/earth_story.py] [--setting path/to/check_setting.py]

Standard library only. The data file is loaded by path and no bytecode is written. Exit status 1 if a check fails.

What is checked:
  1. coverage: every key the game reads is there, with all five colors where a key goes by color, the same sub-keys
     for every color, the nine peace bands, all 24 history marks, two lines where a key has a light and a heavy (or a
     first and a later) form, and no keys the game does not read; SONG_WORLD only overrides keys SONG has, with the
     same shape; the thread covers all 24 marks; the world lines use only the kinds and channels the Engine reports,
     with both bands, and every one has its clause for the year's line; every channel has a fallback line; each
     hazard has a scene and five readings, near and at home, and the flood next door is earth.py's own text;
  2. fills: a line uses only the fills the game gives its key, and the ones it must use; a world's line uses the same
     fills as the line it replaces; no lower-case fill starts a sentence; filling every fill with sample words leaves no
     placeholder behind;
  3. length: at most 25 words for the voice's and the last conversation's lines (voice-mechanics.md section 9) and for
     the thread, world and disaster lines, 32 for a line of the song, 40 for a disaster scene, 16 for a reading's label,
     12 for a clause of the year's line and 8 for an option note, a fill counting as one word;
  4. duplicates: no line appears twice;
  5. color words: no white, blue, black, red or green (or their forms) and no Magic terms;
  6. person: the character's own words (answers, memories, the last conversation's quotes) never use {N}; narration
     lines that name the character start from {N} or {Ns}, or speak of "they";
  7. style: no straight double quotes and no curly apostrophes; the last conversation's quotes are in curly quotes;
     sentences end with . ? ! or a closing quote; clauses and phrases the game joins into a sentence do not;
  8. safety: no sexual violence, suicide, torture or gore words, nothing of harm to a child;
  9. setting (timeless modern days): check_setting.py's patterns, read from the same tree's
     chroma-library/drafts/check_setting.py or the path given with --setting; skipped with a note when neither is
     there (run check_setting.py on earth_story.py then).
"""
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.dirname(HERE)
args = [a for a in sys.argv[1:]]
SETTING = None
if "--setting" in args:
    i = args.index("--setting"); SETTING = args[i + 1]; del args[i:i + 2]
PATH = args[0] if args else os.path.join(LIB, "earth_story.py")
if SETTING is None and os.path.exists(os.path.join(LIB, "drafts", "check_setting.py")):
    SETTING = os.path.join(LIB, "drafts", "check_setting.py")

COLORS = "WUBRG"
MARKS = ["hid a wrong", "owned up", "kept your word", "broke your word", "learned a skill", "took a wild risk",
         "left home", "stayed home", "moved away", "turned down a chance", "helped someone in need",
         "refused someone in need", "made an enemy", "made a friend", "defied an authority", "gave in to pressure",
         "came home", "came out", "kept it hidden", "used drugs", "broke the law", "hurt someone badly", "took a life",
         "named their gender"]
BANDS = [(a, b) for a in ("high", "mid", "low") for b in ("high", "mid", "low")]
NAMES_READ = ("SONG", "SONG_WORLD", "MARK_SAY", "LAST_TALK", "VOICE", "THREAD", "THREAD_HOVER", "THREAD_DID", "WORLD",
              "WORLD_CHANNEL", "YEAR", "YEAR_WHAT", "YEAR_WHAT_CHANNEL", "OPTION_CAUSE", "DISASTER_READ")
# the Engine's world-effect report (STATE "wfx", stage 1 PR B): its kinds and channels
KINDS = ["recession", "prices", "housing", "welfare", "rights", "crime wave", "disaster", "war", "law", "unemployment",
         "hospital places", "university places"]
CHANNELS = ["money", "freedom", "safety", "job loss risk", "disaster risk", "crime risk", "option", "close person"]
HAZARDS = ["flood", "fire", "quake", "storm", "heat"]
SIDES = ["people", "themselves", "safety", "freedom", "head", "heart", "make", "already", "will", "meant"]

COLOR_WORDS = re.compile(r"\b(white[s]?|whiter|whitest|blue[s]?|bluer|bluest|black[s]?|blacker|blackest|blackened|"
                         r"red[s]?|redder|reddest|reddish|reddened|green[s]?|greener|greenest|greenish)\b", re.I)
MAGIC_WORDS = re.compile(r"\b(colou?rs?|mana|planeswalker\w*|azorius|dimir|rakdos|gruul|selesnya|orzhov|izzet|golgari|"
                         r"boros|simic|bant|esper|grixis|jund|naya|abzan|jeskai|sultai|mardu|temur|mono)\b", re.I)
SAFETY = re.compile(r"\b(rap(e|ed|es|ing|ist)|sexual\w*|sex|molest\w*|suicid\w*|kill (yourself|myself|themselves)|"
                    r"self-harm\w*|tortur\w*|gore|blood\w*|corpse\w*|mutilat\w*|abus\w*|naked|groom(ed|ing))\b", re.I)
FILL = re.compile(r"\{([^{}]*)\}")
UPPER_FILLS = {"N", "Ns", "Decade", "cheer", "toast"}       # fills whose values start with a capital letter

# kinds: "sentence" (one or more whole sentences), "clause" (the game joins it into a sentence: no end punctuation, may
# start lower case), "phrase" (a few words used inside a line), "quote" (the character's words in curly quotes),
# "own" (the character's words, unquoted: the answer to the voice). person: "song" (they), "first", "narration".
def rule(path):
    """(allowed fills, required fills, kind, person, word limit) for a line at path (a tuple of keys)."""
    top, k = path[0], path[1] if len(path) > 1 else None
    if top in ("SONG", "SONG_WORLD"):
        if top == "SONG_WORLD":
            path = ("SONG",) + path[2:]
            k = path[1]
        song = {
            "epithet": ((), (), "phrase"),
            "open": (("N", "ep", "age"), ("N", "ep", "age"), "clause"),
            "open_many": (("N", "ep", "age", "n"), ("N", "ep", "age", "n"), "clause"),
            "numbers": ((), (), "phrase"),
            "first_child": (("adjs",), ("adjs",), "sentence"),
            "first_later": (("adjs", "nth"), ("adjs", "nth"), "sentence"),
            "unsettled": ((), (), "phrase"),
            "swing": (("img", "span", "winds"), ("img", "span", "winds"), "clause+"),
            "span_all": ((), (), "phrase"),
            "span_years": (("n",), ("n",), "phrase"),
            "winds_both": (("adjs", "nouns"), ("adjs", "nouns"), "phrase"),
            "winds_apart": (("a", "b"), ("a", "b"), "phrase"),
            "flicker": ((), (), "phrase"),
            "harbour": (("age", "adjs"), ("age", "adjs"), "sentence"),
            "turn": (("cause", "gods"), ("cause",), "sentence"),
            "cause_death": ((), (), "phrase"),
            "cause_moment": (("moment",), ("moment",), "phrase"),
            "cause_title": (("becoming",), ("becoming",), "phrase"),
            "drift": (("Decade",), (), "sentence"),
            "rise": ((), (), "clause"),
            "fall": ((), (), "clause"),
            "home": ((), (), "sentence"),
            "longest": (("n", "ident"), ("n", "ident"), "sentence"),
            "rare_long": (("age", "title"), ("age", "title"), "sentence"),
            "rare_became": (("age", "title"), ("age", "title"), "sentence"),
            "rare_took": (("age", "doing"), ("age", "doing"), "sentence"),
            "rare_mark": (("age", "deed"), ("age", "deed"), "sentence"),
            "rare_moment": (("moment", "age", "nth"), ("moment",), "sentence"),
            "deeds_reach": (("noun",), ("noun",), "sentence"),
            "deeds_won": (("gods",), (), "sentence"),
            "deeds_pushed": (("n", "hand", "noun"), ("n", "hand", "noun"), "clause"),
            "deeds_pushed_end": ((), (), "tail"),
            "deeds_once": (("hand", "noun"), ("hand", "noun"), "clause"),
            "deeds_free": ((), (), "sentence"),
            "shape": (("hi", "lo"), (), "sentence"),
            "decade_youth": ((), (), "phrase"),
            "decade": (("d",), ("d",), "phrase"),
            "peace": (("decade",), ("decade",), "sentence"),
            "buried": (("n",), ("n",), "sentence"),
            "reached": (("n", "made"), ("n",), "sentence"),
            "death_early": (("age", "how"), ("age", "how"), "sentence"),
            "death_old": (("age",), ("age",), "sentence"),
            "close": (("hall", "N", "glad", "cheer", "toast"), ("hall", "N", "glad", "cheer", "toast"), "sentence"),
            "cheer": ((), (), "sentence"),
            "hall": ((), (), "phrase"),
            "gods": ((), (), "phrase"),
            "hand": ((), (), "phrase"),
            "glad": ((), (), "phrase"),
            "toast": ((), (), "sentence"),
        }[k]
        return song + ("song", 32)
    if top == "MARK_SAY":
        return ((), (), "phrase", "song", 32)
    if top == "LAST_TALK":
        return {"intro": (("N", "voice"), ("N", "voice"), "sentence", "narration", 25),
                "gave": ((), (), "quote", "first", 25),
                "cost": ((), (), "quote", "first", 25),
                "glad": ((), (), "quote", "first", 25),
                "none": (("N",), ("N",), "sentence", "narration", 25),
                "few": (("N",), ("N",), "sentence", "narration", 25)}[k]
    if top == "VOICE":
        p2 = path[2] if len(path) > 2 else None
        return {"noun": ((), (), "phrase", "narration", 25),
                "name": (("voice",), ("voice",), "phrase", "narration", 25),
                "none": (("voice",), ("voice",), "phrase", "narration", 25),
                "quiet": (("voice",), ("voice",), "phrase", "narration", 25),
                "answer": ((), (), "own", "first", 25),
                "memory": (("lost",), ("lost",) if p2 == "failed" else (), "own", "first", 25),
                "outcome": (("N",), (), "sentence", "narration", 25),
                "trust_turn": (("N",), ("N",), "sentence", "narration", 25),
                "became": (("N", "ident"), ("N", "ident"), "sentence", "narration", 25),
                "chapter": (("N", "Ns", "name"), ("name",) if p2 in ("won", "trust_up", "trust_down") else (),
                            "sentence", "narration", 25),
                "end": (("N", "Ns", "name", "adj", "share"),
                        ("N",) if p2 == "quiet" else ("Ns", "name", "adj"), "sentence", "narration", 25),
                "share": ((), (), "phrase", "narration", 25),
                "book": (("N", "start", "end", "lean"), ("N", "start", "end"), "sentence", "narration", 25),
                "lean": ((), (), "phrase", "narration", 25)}[k]
    if top == "THREAD":
        req = {"mark": ("N",), "title": ("title",), "commitment": ("who",) if path[-1] == "partner" else (),
               "plan": ("N",), "dream": ("N",), "road": ("N", "age"), "person": ("who",)}[k]
        return (("N", "Ns", "age", "title", "who"), req, "sentence", "narration", 25)
    if top == "THREAD_HOVER":
        req = {"mark": ("N", "did", "age"), "title": ("N", "title"), "commitment": ("Ns",), "plan": ("Ns", "plan"),
               "dream": ("Ns", "dream"), "road": ("N", "road", "age"), "person": ("who",)}[k]
        return (("N", "Ns", "age", "did", "title", "who", "plan", "dream", "road"), req, "sentence", "narration", 25)
    if top == "THREAD_DID":
        return ((), (), "phrase", "narration", 25)
    if top in ("WORLD", "WORLD_CHANNEL"):
        ch = path[2] if top == "WORLD" else path[1]
        return (("N", "Ns", "who"), ("who",) if ch == "close person" else (), "sentence", "narration", 25)
    if top == "YEAR":
        return (("N", "what"), ("N", "what"), "sentence", "narration", 25)
    if top in ("YEAR_WHAT", "YEAR_WHAT_CHANNEL"):
        ch = path[2] if top == "YEAR_WHAT" else path[1]
        return (("who",), ("who",) if ch == "close person" else (), "clause", "narration", 12)
    if top == "OPTION_CAUSE":
        return ((), (), "note", "narration", 8)
    if top == "DISASTER_READ":
        if path[3] == "scene":
            return (("N", "Ns"), (), "sentence", "narration", 40)
        if path[4] == 0:
            return ((), (), "label", "narration", 16)
        return (("N", "Ns"), ("N",), "sentence", "narration", 25)
    raise KeyError(path)


SAMPLE = dict(N="Deniz", Ns="Deniz's", ep="steadfast and fire-hearted", age="67", n="three", adjs="dutiful and rooted",
              nth="20th", img="like a flame in a gusting wind", span="for twelve years", winds="now curious, now rooted",
              nouns="curiosity and passion", a="curious", b="rooted", cause="when a friend was taken from them",
              gods="the gods", moment="“The long winter”", becoming="becoming a baker", Decade="In their 40s",
              ident="one of the Rooted", title="a judge", doing="the sea", deed="kept their word when it cost them",
              noun="sense of duty", hand="the gods' hand", hi="in their 50s", lo="in their 30s", d="40",
              decade="in their 60s", made="two", how="in a fall from a roof", hall="where the cups are filled",
              glad="who lived, and lost, and was glad", cheer="Raise the cup.", toast="To a heart that burned.",
              voice="voice", lost="“The band”", name="the careful voice", adj="passionate", share="a third",
              start="a Free Spirit", end="an Explorer", lean="caution", who="her sister", did="left home",
              plan="a home of their own", dream="the dream of a working life", road="the trades",
              what="prices outran their money and the downturn put jobs at risk")

fails = {}


def fail(check, msg):
    fails.setdefault(check, []).append(msg)


def load_as(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load(path):
    spec = importlib.util.spec_from_file_location("earth_story_checked", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def walk(x, at):
    if isinstance(x, str):
        yield at, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from walk(v, at + (k,))
    elif isinstance(x, (list, tuple)):
        for j, v in enumerate(x):
            if isinstance(v, (int, float)):
                continue
            yield from walk(v, at + (j,))


def words(text):
    return len(FILL.sub("X", text).split())


def where(path):
    return ".".join(str(p) for p in path)


M = load(PATH)
for name in NAMES_READ:
    if not hasattr(M, name):
        fail("1 coverage", f"{name} is missing")
extra = [n for n in dir(M) if n.isupper() and n not in NAMES_READ]
if extra:
    fail("1 coverage", f"names the game does not read: {extra}")
S, SW, MS, LT, V = M.SONG, M.SONG_WORLD, M.MARK_SAY, M.LAST_TALK, M.VOICE
TH, TH_H, TH_D = M.THREAD, M.THREAD_HOVER, M.THREAD_DID
WO, WO_C, YR, YW, YW_C, OC, DR = M.WORLD, M.WORLD_CHANNEL, M.YEAR, M.YEAR_WHAT, M.YEAR_WHAT_CHANNEL, M.OPTION_CAUSE, \
    M.DISASTER_READ


# ---------------------------------------------------------------------------------------------------- 1 coverage
def shape(x):
    """The key structure of x, without its words."""
    if isinstance(x, dict):
        return {k: shape(v) for k, v in x.items()}
    if isinstance(x, list):
        return ["list", len(x)]
    return type(x).__name__


def need_keys(at, d, keys):
    if not isinstance(d, dict):
        fail("1 coverage", f"{at} is not a dict"); return
    missing, extra = [k for k in keys if k not in d], [k for k in d if k not in keys]
    if missing or extra:
        fail("1 coverage", f"{at}: missing {missing}, not read by the game {extra}")


def per_color(at, d, sub=None, n=None):
    need_keys(at, d, list(COLORS))
    shapes = {c: shape(d.get(c)) for c in COLORS}
    if len({repr(v) for v in shapes.values()}) > 1:
        fail("1 coverage", f"{at}: the colors differ in shape")
    for c in COLORS:
        v = d.get(c)
        if sub is not None:
            need_keys(f"{at}.{c}", v, sub)
            if n is not None:
                for s_ in sub:
                    if not (isinstance(v.get(s_), list) and len(v[s_]) == n):
                        fail("1 coverage", f"{at}.{c}.{s_}: wanted {n} lines")
        elif not isinstance(v, str):
            fail("1 coverage", f"{at}.{c} is not a line")


SONG_KEYS = ["epithet", "open", "open_many", "numbers", "first_child", "first_later", "unsettled", "swing", "span_all",
             "span_years", "winds_both", "winds_apart", "flicker", "harbour", "turn", "cause_death", "cause_moment",
             "cause_title", "drift", "rise", "fall", "home", "longest", "rare_long", "rare_became", "rare_took",
             "rare_mark", "rare_moment", "deeds_reach", "deeds_won", "deeds_pushed", "deeds_pushed_end", "deeds_once",
             "deeds_free", "shape", "decade_youth", "decade", "peace", "buried", "reached", "death_early", "death_old",
             "close", "cheer", "hall", "gods", "hand", "glad", "toast"]
need_keys("SONG", S, SONG_KEYS)
per_color("SONG.epithet", S["epithet"])
per_color("SONG.open", S["open"], ["full", "short"])
if not (isinstance(S["numbers"], list) and len(S["numbers"]) >= 7 and S["numbers"][1] == "one"):
    fail("1 coverage", "SONG.numbers: wanted the words for 0 to 6 at least")
per_color("SONG.flicker", S["flicker"], ["first", "again"])
need_keys("SONG.turn", S["turn"], ["death", "title", "event"])
for k in S["turn"]:
    need_keys(f"SONG.turn.{k}", S["turn"][k], ["big", "small"])
need_keys("SONG.cause_death", S["cause_death"], ["parent", "sibling", "friend", "grandparent", "partner", "child", "other"])
need_keys("SONG.drift", S["drift"], ["big", "mid", "small"])
per_color("SONG.rise", S["rise"], ["first", "again"])
per_color("SONG.fall", S["fall"], ["first", "again"])
for key in ("rise", "fall"):    # "again" is a list the game takes in turn, so a song does not repeat a clause
    for c, d in S[key].items():
        ag = d.get("again")
        if not (isinstance(ag, list) and len(ag) >= 3 and len(set(ag)) == len(ag)):
            fail("1 coverage", f"SONG.{key}.{c}.again: wanted a list of 3 or more different clauses")
per_color("SONG.rare_moment", S["rare_moment"])
need_keys("SONG.deeds_reach", S["deeds_reach"], ["own", "other"])
need_keys("SONG.deeds_won", S["deeds_won"], ["often", "half", "seldom"])
need_keys("SONG.deeds_pushed_end", S["deeds_pushed_end"], ["willing", "bore", "against"])
need_keys("SONG.shape", S["shape"], ["rise", "fall", "valley", "fallen", "summit", "level"])
need_keys("SONG.reached", S["reached"], ["never", "once", "more"])
need_keys("SONG.glad", S["glad"], BANDS)
per_color("SONG.toast", S["toast"], ["glad", "hard"])

need_keys("SONG_WORLD", SW, ["tribal", "magic"])
for w, over in SW.items():
    for k, v in over.items():
        if k not in S:
            fail("1 coverage", f"SONG_WORLD.{w}.{k}: SONG has no such key"); continue
        base = shape(S[k])
        if isinstance(v, dict):
            for kk, vv in v.items():
                if not isinstance(base, dict) or kk not in base:
                    fail("1 coverage", f"SONG_WORLD.{w}.{k}.{kk}: SONG.{k} has no such key")
                elif shape(vv) != base[kk]:
                    fail("1 coverage", f"SONG_WORLD.{w}.{k}.{kk}: not the shape of SONG.{k}.{kk}")
        elif shape(v) != base:
            fail("1 coverage", f"SONG_WORLD.{w}.{k}: not the shape of SONG.{k}")

need_keys("MARK_SAY", MS, MARKS)

need_keys("LAST_TALK", LT, ["intro", "gave", "cost", "glad", "none", "few"])
per_color("LAST_TALK.gave", LT["gave"], ["own", "other"])
per_color("LAST_TALK.cost", LT["cost"], ["enemy", "other"])
need_keys("LAST_TALK.glad", LT["glad"], ["glad", "torn", "sorry"])
for k, v in LT["glad"].items():
    if not (isinstance(v, list) and len(v) == 2):
        fail("1 coverage", f"LAST_TALK.glad.{k}: wanted 2 lines (under a third, a third or more)")

need_keys("VOICE", V, ["noun", "name", "none", "quiet", "answer", "memory", "outcome", "trust_turn", "became", "chapter",
                       "end", "share", "book", "lean"])
need_keys("VOICE.noun", V["noun"], ["earth", "tribal", "magic"])
need_keys("VOICE.name", V["name"], SIDES)
for k in SIDES:
    need_keys(f"VOICE.name.{k}", V["name"].get(k, {}), ["trusted", "doubted"])
need_keys("VOICE.answer", V["answer"], list(COLORS))
n_answer = 0
for c in COLORS:
    need_keys(f"VOICE.answer.{c}", V["answer"][c], ["same", "ally", "enemy"])
    for dist, d in V["answer"][c].items():
        need_keys(f"VOICE.answer.{c}.{dist}", d, ["trust", "unsure", "doubt"])
        for t, lines in d.items():
            if not (isinstance(lines, list) and len(lines) == 2):
                fail("1 coverage", f"VOICE.answer.{c}.{dist}.{t}: wanted 2 lines (light, heavy)")
            n_answer += len(lines)
need_keys("VOICE.memory", V["memory"], ["worked", "failed", "failed_plain"])
need_keys("VOICE.outcome", V["outcome"], ["right", "wrong"])
per_color("VOICE.trust_turn", V["trust_turn"], ["up", "down"], 2)
need_keys("VOICE.became", V["became"], ["trusted", "unsure", "doubted"])
need_keys("VOICE.chapter", V["chapter"], ["first", "won", "trust_up", "trust_down", "quiet"])
for k in ("memory", "outcome", "chapter"):
    for kk, v in V[k].items():
        if not (isinstance(v, list) and len(v) == 2):
            fail("1 coverage", f"VOICE.{k}.{kk}: wanted 2 lines")
need_keys("VOICE.end", V["end"], ["trusted", "mixed", "doubted", "quiet"])
sh = V["share"]
if not (all(isinstance(a, float) and isinstance(b, str) for a, b in sh) and [a for a, _ in sh] == sorted(a for a, _ in sh)
        and sh[-1][0] > 1):
    fail("1 coverage", "VOICE.share: wanted (below, words) pairs in rising order, the last above 1")
need_keys("VOICE.book", V["book"], ["steered", "free"])
need_keys("VOICE.lean", V["lean"], list(COLORS))

need_keys("THREAD", TH, ["mark", "title", "commitment", "plan", "dream", "road", "person"])
need_keys("THREAD.mark", TH["mark"], MARKS)
need_keys("THREAD.title", TH["title"], ["held", "lost"])
need_keys("THREAD.commitment", TH["commitment"], ["career", "community", "faith", "partner", "children"])
need_keys("THREAD_HOVER", TH_H, ["mark", "title", "commitment", "plan", "dream", "road", "person"])
need_keys("THREAD_HOVER.title", TH_H["title"], ["held", "lost"])
need_keys("THREAD_HOVER.commitment", TH_H["commitment"], ["career", "community", "faith", "partner", "children"])
need_keys("THREAD_DID", TH_D, MARKS)
for k, d in WO.items():
    if k not in KINDS:
        fail("1 coverage", f"WORLD.{k}: not a kind the Engine reports")
    for ch, dd in d.items():
        if ch not in CHANNELS:
            fail("1 coverage", f"WORLD.{k}.{ch}: not a channel the Engine reports")
        for dr, b in dd.items():
            if dr not in ("up", "down"):
                fail("1 coverage", f"WORLD.{k}.{ch}.{dr}: dir is up or down")
            need_keys(f"WORLD.{k}.{ch}.{dr}", b, ["small", "big"])
            if not (isinstance(YW.get(k, {}).get(ch), dict) and dr in YW[k][ch]):
                fail("1 coverage", f"YEAR_WHAT.{k}.{ch}.{dr}: missing (WORLD has a line for it)")
missing_kinds = [k for k in KINDS if k not in WO]
if missing_kinds:
    fail("1 coverage", f"WORLD: no lines for the kinds {missing_kinds}")
for k, d in YW.items():
    for ch, dd in d.items():
        for dr in dd:
            if not (k in WO and ch in WO[k] and dr in WO[k][ch]):
                fail("1 coverage", f"YEAR_WHAT.{k}.{ch}.{dr}: WORLD has no line for it")
need_keys("WORLD_CHANNEL", WO_C, CHANNELS)
need_keys("YEAR_WHAT_CHANNEL", YW_C, CHANNELS)
for ch in CHANNELS:
    need_keys(f"WORLD_CHANNEL.{ch}", WO_C.get(ch, {}), ["up", "down"])
    need_keys(f"YEAR_WHAT_CHANNEL.{ch}", YW_C.get(ch, {}), ["up", "down"])
    for dr in ("up", "down"):
        need_keys(f"WORLD_CHANNEL.{ch}.{dr}", WO_C.get(ch, {}).get(dr, {}), ["small", "big"])
need_keys("YEAR", YR, ["lean", "easier", "uneasy", "calmer", "freer", "narrower", "close", "mixed"])
need_keys("OPTION_CAUSE", OC, ["law", "norm", "technology", "odds"])
for k in OC:
    need_keys(f"OPTION_CAUSE.{k}", OC[k], ["closed", "harder", "easier"])
need_keys("DISASTER_READ", DR, HAZARDS)
for hz in HAZARDS:
    need_keys(f"DISASTER_READ.{hz}", DR.get(hz, {}), ["near", "home"])
    for wh, d in DR.get(hz, {}).items():
        need_keys(f"DISASTER_READ.{hz}.{wh}", d, ["scene"] + list(COLORS))
        for c in COLORS:
            if not (isinstance(d.get(c), tuple) and len(d[c]) == 2):
                fail("1 coverage", f"DISASTER_READ.{hz}.{wh}.{c}: wanted (label, say)")
# the flood next door is earth.py's own text, so lives where the tag is missing read the same
EARTH = os.path.join(LIB, "earth.py")
if os.path.exists(EARTH):
    E_ = load_as(EARTH, "earth_checked")
    ev = [e for e in getattr(E_, "EVENTS_READ", []) if e.get("name") == "a disaster in the next town"]
    if not ev:
        fail("1 coverage", "earth.py has no 'a disaster in the next town' to match")
    else:
        e = ev[0]
        sc = e.get("scenes", {}).get("earth", [])
        sc0 = sc[0][1] if sc and isinstance(sc[0], tuple) else (sc[0] if sc else None)
        if sc0 is not None and sc0 != DR["flood"]["near"]["scene"]:
            fail("1 coverage", "DISASTER_READ.flood.near.scene differs from earth.py's scene")
        live = {}
        for r in e.get("readings", []):   # (label, tag, impact, also, color, say)
            if isinstance(r, tuple) and len(r) >= 6:
                live[r[4]] = (r[0], r[5])
        for c in COLORS:
            if c in live and live[c] != DR["flood"]["near"][c]:
                fail("1 coverage", f"DISASTER_READ.flood.near.{c} differs from earth.py's reading")
        flood_checked = bool(live) and sc0 is not None
else:
    flood_checked = False

# -------------------------------------------------------------------------------------------- lines, checks 2 to 9
ALL = []
for name in NAMES_READ:
    obj = getattr(M, name)
    if name == "SONG" or name == "SONG_WORLD":
        obj = {k: ({"|".join(b): t for b, t in v.items()} if k == "glad" else v) for k, v in obj.items()} \
            if name == "SONG" else {w: {k: ({"|".join(b): t for b, t in v.items()} if k == "glad" else v)
                                        for k, v in o.items()} for w, o in obj.items()}
    for path, text in walk(obj, (name,)):
        ALL.append((path, text))

FIRST = re.compile(r"\b(I|I'm|I've|I'd|I'll|me|my|mine|myself)\b")
seen = {}
longest = {"song": (0, ""), "voice": (0, "")}
for path, text in ALL:
    at = where(path)
    if path[0] == "VOICE" and path[1] == "share":
        continue
    allowed, required, kind, person, limit = rule(path)
    fills = FILL.findall(text)
    # 2 fills
    for f in fills:
        if f not in allowed:
            fail("2 fills", f"{{{f}}} is not a fill of this key: {at}: {text}")
    for f in required:
        if f not in fills:
            fail("2 fills", f"{{{f}}} is missing: {at}: {text}")
    if kind in ("sentence", "quote", "own"):
        for m in re.finditer(r"(?:^|[.?!]”? )\{([^{}]*)\}", text):
            if m.group(1) not in UPPER_FILLS:
                fail("2 fills", f"{{{m.group(1)}}} starts a sentence but its value is lower case: {at}")
    if path[0] in ("DISASTER_READ", "WORLD", "WORLD_CHANNEL") and kind == "sentence" and not ({"N", "Ns"} & set(fills)):
        fail("2 fills", f"the line does not name the character ({{N}} or {{Ns}}): {at}")
    filled = FILL.sub(lambda m: SAMPLE.get(m.group(1), "{" + m.group(1) + "}"), text)
    if FILL.search(filled) or "{" in filled or "}" in filled:
        fail("2 fills", f"a placeholder is left after filling: {at}: {filled}")
    if path[0] == "SONG_WORLD":
        base = S[path[2]]
        for p_ in path[3:]:
            key = tuple(p_.split("|")) if path[2] == "glad" else p_
            base = base.get(key) if isinstance(base, dict) else None
        if isinstance(base, str) and sorted(FILL.findall(base)) != sorted(fills):
            fail("2 fills", f"{at} uses other fills than the SONG line it replaces")
    # 3 length
    n = words(text)
    if n > limit:
        fail("3 length", f"{n} words (limit {limit}): {at}: {text}")
    grp = "song" if person == "song" else "voice"
    if n > longest[grp][0]:
        longest[grp] = (n, at)
    # 4 duplicates
    if kind != "phrase" and path[0] != "SONG_WORLD":
        if text in seen:
            fail("4 duplicates", f"{at} repeats {seen[text]}: {text}")
        seen[text] = at
    # 5 color words
    for m in COLOR_WORDS.finditer(text):
        fail("5 color words", f"\"{m.group(0)}\": {at}")
    for m in MAGIC_WORDS.finditer(text):
        fail("5 color words", f"Magic term \"{m.group(0)}\": {at}")
    # 6 person
    if person == "first":
        if "N" in fills or "Ns" in fills:
            fail("6 person", f"the character's own words name them: {at}")
        if kind == "quote" and not FIRST.search(text):
            fail("6 person", f"a quote with no first-person word: {at}: {text}")
    if person == "narration" and kind == "sentence" and FIRST.search(text.replace("“", "").replace("”", "")) \
            and "“" not in text:
        fail("6 person", f"narration in the first person: {at}: {text}")
    if person == "song" and ("N" in fills and path[1] not in ("open", "open_many", "close")):
        fail("6 person", f"the song names the character outside its opening and close: {at}")
    # 7 style
    if '"' in text:
        fail("7 style", f"straight double quote: {at}")
    if "’" in text or "‘" in text:
        fail("7 style", f"curly apostrophe (the Library uses '): {at}")
    if text.count("“") != text.count("”"):
        fail("7 style", f"unbalanced curly quotes: {at}")
    if kind == "quote" and not (text.startswith("“") and text.endswith("”")):
        fail("7 style", f"the last conversation's words are not in curly quotes: {at}")
    if kind in ("sentence", "quote", "own") and not re.search(r"([.?!]|[.?!]”|\{toast\})$", text):
        fail("7 style", f"does not end a sentence: {at}: {text}")
    if kind == "label" and re.search(r"[.!:;,]$", text):
        fail("7 style", f"a reading's label ends in punctuation other than a question mark: {at}: {text}")
    if kind == "note" and (re.search(r"[.?!:;,]$", text) or not text[:1].isupper()):
        fail("7 style", f"an option note starts upper case and has no end punctuation: {at}: {text}")
    if kind in ("clause", "phrase") and re.search(r"[.?!:;,]$", text):
        fail("7 style", f"a clause or phrase the game joins ends in punctuation: {at}: {text}")
    if kind == "tail" and not (text.startswith(", ") and text.endswith(".")):
        fail("7 style", f"an ending the game appends to a clause must start with \", \" and end with \".\": {at}")
    if kind in ("sentence", "quote", "own") and re.match(r"“?[a-z]", text) and path[1] not in ("swing",):
        fail("7 style", f"a sentence starts lower case: {at}: {text}")
    if re.search(r"\s{2,}|\s[,.?!]", text):
        fail("7 style", f"double space or space before punctuation: {at}")
    # 8 safety
    for m in SAFETY.finditer(filled):
        fail("8 safety", f"\"{m.group(0)}\": {at}")

if n_answer != 90:
    fail("1 coverage", f"VOICE.answer has {n_answer} lines, wanted 90 (5 colors x 3 distances x 3 trust levels x 2)")

# ---------------------------------------------------------------------------------------------------- 9 setting
setting_note = ""
if SETTING and os.path.exists(SETTING):
    spec = importlib.util.spec_from_file_location("check_setting_patterns", SETTING)
    src = open(SETTING, encoding="utf-8").read()
    head = src.split("\nNEXT = ")[0]            # the patterns and ALLOW, without the run at the bottom
    ns = {"__file__": SETTING}
    exec(compile(head, SETTING, "exec"), ns)
    pats = [(k, v, re.I) for k, v in ns["PAT"].items()] + [(k, v, 0) for k, v in ns["CASE"].items()]
    for path, text in ALL:
        for kind, pat, fl in pats:
            for m in re.finditer(pat, text, fl):
                fail("9 setting", f"{kind}: '{m.group(0)}' in {where(path)}: {text}")
    setting_note = "patterns from " + (os.path.relpath(SETTING, LIB) if os.path.abspath(SETTING).startswith(LIB) else SETTING)
else:
    setting_note = "skipped: no check_setting.py in this tree (give --setting, or run check_setting.py on earth_story.py)"

# ---------------------------------------------------------------------------------------------------- report
NAMES = ["1 coverage", "2 fills", "3 length", "4 duplicates", "5 color words", "6 person", "7 style", "8 safety",
         "9 setting"]
print(f"# check_story: {os.path.basename(PATH)}\n")
cnt = lambda *ns: sum(1 for p, _ in ALL if p[0] in ns)
print(f"{len(ALL)} lines: song {cnt('SONG', 'SONG_WORLD', 'MARK_SAY')}, last conversation {cnt('LAST_TALK')}, "
      f"voice {cnt('VOICE')} ({n_answer} answers), thread {cnt('THREAD', 'THREAD_HOVER', 'THREAD_DID')}, "
      f"world {cnt('WORLD', 'WORLD_CHANNEL')}, year {cnt('YEAR', 'YEAR_WHAT', 'YEAR_WHAT_CHANNEL')}, "
      f"option notes {cnt('OPTION_CAUSE')}, disaster readings {cnt('DISASTER_READ')}")
print("the flood next door matches earth.py: " + ("checked" if flood_checked else "not checked (no earth.py beside it)"))
print(f"longest: song {longest['song'][0]} words ({longest['song'][1]}), the other lines "
      f"{longest['voice'][0]} words ({longest['voice'][1]})\n")
for nm in NAMES:
    if nm == "9 setting" and not (SETTING and os.path.exists(SETTING)):
        print(f"- {nm}: {setting_note}")
        continue
    got = fails.get(nm, [])
    print(f"- {nm}: {'PASS' if not got else f'FAIL ({len(got)})'}" + (f", {setting_note}" if nm == "9 setting" else ""))
    for g in got[:40]:
        print(f"    {g}")
bad = sum(len(v) for v in fails.values())
print(f"\n{'PASS' if not bad else 'FAIL'}: {bad} problems")
sys.exit(1 if bad else 0)
