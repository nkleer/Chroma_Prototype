"""Chroma: the built-in story layer (text prototype).

Turns what the engine records into a story: scenes, the character's own thoughts, outcomes, a cast of named
people, and a short chapter for every year. Built-in lines only, so nothing waits on generated text (Emren,
2026-10-04).

Voice (Emren's pick, "Mixed"): a narrator in the third person and present tense, with the character's own
thoughts in the first person, in *italics*.

The narration follows the character's colors (Emren, 2026-10-04): almost every passage has variants written
through each color's eyes (a funeral is a duty to White, a riddle to Blue, a gap to fill to Black, a blow to
Red, the turning of a season to Green). The variant told is drawn by the character's VOICE: a blend of who
they are now (40%) and a memory of who they have been, which fades over about six years. As the identity
drifts, the emphasis of the telling drifts with it, slowly. Thoughts before an act speak for the act's own
colors (the motive); thoughts after an outcome speak through the voice (how the character reads it).

The story draws from its own random stream, so the text never changes the simulated life.
"""
import re
from collections import deque
import numpy as np

COLORS = "WUBRG"
CI = {c: i for i, c in enumerate(COLORS)}
STAGESETS = dict(k={0}, a={1, 2, 3, 4, 5}, y={0, 1, 2}, o={3, 4, 5})   # by phase of life: under 12, 12 and over, under 30, 30 and over
SHARP = 3.0           # how strongly the voice favours its leading colors when picking a variant
MEMORY_YEARS = 3.0    # how long past identities linger in the voice (Emren, 2026-10-04 23:02: 3 years)
NOW_SHARE = 0.4       # share of the present identity in the voice

# names by how they are usually heard (chroma-identity/for-the-game.md §4): feminine, masculine, and either. A mother or a
# grandmother takes a feminine or either name, a father a masculine or either one; anyone else any name. A partner takes
# their own sex's list or either once the engine says who the partner is (partner_same), and either until then.
NAMES_F = ["Ada", "Elif", "Hana", "Maren", "Nadia", "Pia", "Rosa", "Tove", "Vera", "Yara", "Aylin", "Cyra", "Farah",
           "Ines", "Kira", "Odile", "Rhea", "Selin", "Una", "Willa", "Zora", "Alba", "Cleo", "Esme", "Greta", "Mona",
           "Petra", "Tamsin", "Vida", "Cansu", "Ebba", "Hester"]
NAMES_M = ["Bran", "Cem", "Idris", "Kemal", "Oren", "Umar", "Zeki", "Dov", "Emre", "Galen", "Hugo", "Jonah", "Nils",
           "Teo", "Vik", "Yusuf", "Basil", "Dima", "Hal", "Isak", "Otto", "Sven", "Ugo", "Arlo", "Dex", "Fikri", "Gus"]
NAMES_X = ["Dara", "Femi", "Gale", "Jun", "Lior", "Quinn", "Sami", "Wren", "Bo", "Leto", "Mika", "Paz", "Fen", "Joss",
           "Kaya", "Lenn", "Nuri", "Rumi", "Beren"]
NAMES = NAMES_F + NAMES_M + NAMES_X
NAME_POOL = {"f": NAMES_F + NAMES_X, "m": NAMES_M + NAMES_X, "x": NAMES_X}
FEM_REF = re.compile(r"\b(mother|grandmother|sister|aunt|daughter|wife|girlfriend|niece|mum|stepmother|widow)\b")
MAS_REF = re.compile(r"\b(father|grandfather|brother|uncle|son|husband|boyfriend|nephew|dad|stepfather|widower)\b")
PLACES = ["town", "city", "village", "port town", "neighbourhood", "valley town", "market town"]
DISASTERS = ["a flood", "a fire", "a storm", "an earthquake", "an epidemic", "a drought", "a landslide"]
BRUSHES = ["a fall from a roof", "a fever that will not break", "a speeding car that misses them by a hand's width",
           "a night in freezing water", "a knife in a dark street", "a wrong step on a cliff path"]

# The setting the story is told in (Emren, 2026-10-04 23:02: chosen at the start, modern Earth by default, with
# fantasy and supernatural settings wanted too). The engine runs the same rules in each; only the telling differs
# until the library's tribal and magic worlds land. Pool entries carry world letters (E, T, M) when they belong
# to some settings only.
SETTINGS = {
    "earth": dict(code="E", title="Modern Earth", blurb="phones, offices, schools and cities; no magic"),
    "tribal": dict(code="T", title="Tribal", blurb="clans, hunts, elders and the turning seasons, before cities"),
    "magic": dict(code="M", title="A world of magic", blurb="towers, guilds and old powers; a gift may awaken"),
}
WORLD = {
    "earth": dict(places=PLACES, disasters=DISASTERS, brushes=BRUSHES,
                  classmate="their classmate {n}", teacher="their teacher {n}", elder_mentor="an older hand called {n}",
                  boss="their boss {n}", new_boss="their new boss {n}", colleague="their colleague {n}",
                  runs="{b} runs the place.", job="job", inst=("school", "work", "the town hall"),
                  era=dict(policy="New laws and new leaders arrive.", institutions="The great institutions change their ways.",
                           cosmology="A new way of seeing the world spreads.")),
    "tribal": dict(places=["river camp", "hill settlement", "longhouse village", "valley camp", "lakeside camp", "forest camp"],
                   disasters=["a flood", "a fire in the dry grass", "a drought", "a raid from across the hills", "a killing winter",
                              "a sickness", "a stampede"],
                   brushes=["a fall from the cliffs", "a fever that will not break", "a boar's charge", "a night in the freezing river",
                            "a spear thrown in a quarrel", "thin ice on the lake"],
                   classmate="their playmate {n}", teacher="the elder {n}", elder_mentor="the old hunter {n}",
                   boss="the hunt leader {n}", new_boss="an old hand called {n}", colleague="their work-mate {n}",
                   runs="{b} shows them the work.", job="work", inst=("the elders' teaching", "the hunt", "the council fire"),
                   era=dict(policy="A new chief rises, with new laws.", institutions="The councils of the clans change their ways.",
                            cosmology="The shamans speak of a new way of seeing the world.")),
    "magic": dict(places=["tower town", "walled city", "forest hamlet", "harbour of spires", "crossroads village", "river city"],
                  disasters=["a wild surge of magic", "a blight", "a storm of ash", "a plague of shadows", "a flood",
                             "a beast out of the deep woods", "a fire"],
                  brushes=["a spell that backfires", "a fever cast by a curse", "a fall from the tower stairs",
                           "a night lost in the haunted wood", "a blade in a dark alley", "a bargain with something in the river"],
                  classmate="their fellow pupil {n}", teacher="their tutor {n}", elder_mentor="the old mage {n}",
                  boss="their master {n}", new_boss="the master {n}", colleague="their fellow journeyman {n}",
                  runs="{b} takes them on.", job="post", inst=("the academy", "the guild", "the Order"),
                  era=dict(policy="A new Archmage takes the throne, with new decrees.", institutions="The great Orders change their ways.",
                           cosmology="The stars shift, and a new teaching about the powers beyond spreads.")),
}

# a short phrase for each identity, shown in the chapter header (Emren, 2026-10-04 23:02)
EPITHETS = {
    "W": ["keeper of the peace", "the dutiful one"], "U": ["the endless student", "mind before motion"],
    "B": ["the self-made", "hunger with a plan"], "R": ["the open flame", "heart on the sleeve"],
    "G": ["deep roots", "the patient grove"], "WU": ["rule and reason", "the careful lawgiver"],
    "UB": ["secrets in the shadows", "the quiet schemer"], "BR": ["the feast and the fire", "pleasure without apology"],
    "RG": ["wild and unbowed", "the storm in the hills"], "WG": ["many voices, one song", "the open hearth"],
    "WB": ["duty with a price", "the gilded ledger"], "UR": ["sparks before caution", "the restless inventor"],
    "BG": ["rot feeds the root", "nothing wasted"], "WR": ["justice with a raised fist", "the righteous charge"],
    "UG": ["growth by design", "the patient shaper"], "WUG": ["honour in all things", "the noble steward"],
    "WUB": ["polished and in control", "perfection by design"], "UBR": ["ambition off the leash", "the cold fire"],
    "BRG": ["only the strong", "teeth and appetite"], "WRG": ["life at full volume", "big heart, strong arms"],
    "WBG": ["hold the ground", "family before all"], "WUR": ["the disciplined spark", "the clever path"],
    "UBG": ["patience and plunder", "the coiled serpent"], "WBR": ["fast, fierce, unflinching", "the war-drum"],
    "URG": ["wisdom of the wild", "instinct and cunning"], "WUBR": ["everything but nature", "the made world"],
    "UBRG": ["no rules but their own", "the untamed"], "WBRG": ["act first, think later", "all muscle and will"],
    "WURG": ["for everyone but themselves", "the open hand"], "WUBG": ["slow and sure", "the steady climb"],
    "WUBRG": ["a little of everything", "the whole spectrum"],
}

# ------------------------------------------------------------------ what each color cares about, in words
VALUE = dict(W="doing right by others", U="understanding how things work", B="getting ahead on their own terms",
             R="feeling alive and free", G="staying true to their roots and their people")
VALUE2 = dict(W="fairness, and belonging to something bigger", U="learning, and getting things right",
              B="power, and what it can buy", R="freedom, and following the heart", G="kin, nature and the old ways")
NOUN = dict(W="sense of duty", U="curiosity", B="ambition", R="passion", G="rootedness")
ADJ = dict(W="dutiful", U="curious", B="ambitious", R="passionate", G="rooted")
FAITH_ADJ = dict(W="orderly, devout", U="questioning, learned", B="exclusive, power-promising",
                 R="fervent, ecstatic", G="old, earth-rooted")

# ------------------------------------------------------------------ v7 dreams, passions and plans, in words
# What a goal is about. A pursuit in some colors: (as a dream or passion, as a plan); the goal's id picks the variant, so
# the same goal keeps its words. A domain: (dream, passion, plan).
GOAL_C = dict(
    W=[("serving something bigger than themselves", "serve something bigger than themselves"),
       ("setting things right", "set something right that is wrong"),
       ("being someone others can count on", "become someone others can count on")],
    U=[("mastering a hard craft", "master a hard craft"), ("finding out how things really work", "find out how something really works"),
       ("making something clever", "make something clever")],
    B=[("making a name", "make a name for themselves"), ("getting rich", "get rich"), ("rising to the top", "rise to the top")],
    R=[("chasing adventure", "go on a real adventure"), ("making something that burns bright", "make something that burns bright"),
       ("living free", "live free, answering to no one")],
    G=[("building a home of their own", "build a home of their own"), ("living close to the land", "live close to the land"),
       ("keeping the family close", "keep the family close")])
GOAL_D = dict(career=("work that is truly theirs", "their work", "find work that is truly theirs"),
              partner=("finding the one", "the one they love", "find the one"),
              children=("children of their own", "raising their children", "have a child"),
              community=("a place among their people", "their people", "find a place among their people"),
              faith=("a faith to live by", "their faith", "find a faith to live by"))
HORIZON_WORD = {"week": "this week", "year": "within a year", "five years": "within five years", "life": "before their life is over"}
# where a dream comes from (the engine's DREAM_TRIGGERS), told per setting: (earth, tribal, magic); {x} are cast slots
TRIGGER = {
    "a parent or relative at their work": ("watching {parent} at work",) * 3,
    "an older sibling or cousin": ("watching {sibling}",) * 3,
    "a teacher or coach": ("{teacher}",) * 3,
    "a friend's family": ("a friend's family",) * 3,
    "someone they meet": ("someone they meet",) * 3,
    "a book": ("a book they read twice", "a story told by the fire", "an old book from the tower"),
    "a film or a show": ("a film", "a storyteller's tale", "a travelling show"),
    "a parade or a festival": ("a parade", "a festival", "a festival of lights"),
    "a match or a contest": ("a match", "a contest of strength", "a duel"),
    "a ceremony": ("a ceremony",) * 3,
    "a stranger passing through": ("a stranger passing through",) * 3,
}
DREAM_FROM = ["{T} plants something in {N}: the dream of {g}.", "After {T}, {N} cannot stop thinking about {g}.",
              "{N} catches a dream from {T}: {g}."]
DREAM_NEW = ["A dream takes hold of {N}: {g}.", "{N} starts to dream of {g}."]
PLAN_FROM = {"resolution": "{N} makes a resolution: to {v} {h}.",
             "need": "Something is missing, and {N} makes a plan: to {v} {h}.",
             "old dream": "An old dream comes back to {N}, now as a plan: to {v} {h}.",
             "passion": "{N}'s passion turns into a plan: to {v} {h}.",
             "player": "You set {N} a plan: to {v} {h}.",
             "": "{N} makes a plan: to {v} {h}."}
GOAL_END = {("plan", "achieved"): ["It is done: {N}'s plan to {v} has come true.", "{N} did it: the plan to {v} has come true."],
            ("plan", "not reached in time"): ["Time runs out on {N}'s plan to {v}.", "The plan to {v} runs out of time."],
            ("plan", "let go"): ["{N} gives up the plan to {v}.", "{N} lets the plan to {v} go."],
            ("plan", "extended"): ["{N} gives the plan to {v} more time."],
            ("dream", "let go"): ["{N} lets the dream of {g} go.", "The dream of {g} slips away from {N}."],
            ("dream", "pushed aside"): ["The dream of {g} fades, crowded out by others."],
            ("passion", "let go"): ["{N}'s passion for {g} fades away."],
            ("passion", "pushed aside"): ["{N}'s passion for {g} gives way to a stronger one."],
            ("dream", "became a passion"): ["The dream of {g} is no longer only a dream: it has become {N}'s passion.",
                                            "Tries that worked, and felt like {N}'s own, make {g} a passion."],
            ("dream", "became a plan"): ["{N} turns the dream of {g} into a plan: to {v} {h}."]}
# Named dreams (the Library's dreams.py, Emren 2026-10-06 22:19): the engine names each dream by the nearest catalogue
# entry and passes the spark's say line, the dream's name and its passion, plan and life-goal phrases. {S} is the say
# line, {g} the dream ("becoming a police officer"), {p} its passion, {v} its plan, {l} its life goal.
DREAM_SAY = ["{S}. From that day {N} dreams of {g}.", "{S}. After that, {N} dreams of {g}.", "{S}. It leaves {N} dreaming of {g}."]
DREAM_AGAIN = ["{S}. It feeds an old dream of {N}'s: {g}.", "{S}. The dream of {g} burns brighter in {N}."]   # a dream they already hold
NAMED_END = {("dream", "became a passion"): ["The dream of {g} is no longer only a dream. It has become {N}'s passion: {p}.",
                                             "Tries that worked, and felt like {N}'s own, make the dream of {g} a passion: {p}."],
             ("dream", "became a plan"): ["{N} turns the dream of {g} into a five-year plan: to {v}."],
             ("dream", "let go"): ["{N} lets a dream go: {g}.", "A dream slips away from {N}: {g}."],
             ("dream", "pushed aside"): ["A dream fades, crowded out by others: {g}."],
             ("passion", "let go"): ["{N}'s passion fades away: {p}."],
             ("passion", "pushed aside"): ["A stronger passion crowds out an old one: {p}."],
             ("plan", "achieved"): ["{N} did what they set out to do: {v}.", "It is done. {N} set out to {v}, and did."],
             ("plan", "not reached in time"): ["Time runs out on a plan: to {v}."],
             ("plan", "let go"): ["{N} gives up on a plan: to {v}."],
             ("plan", "extended"): ["{N} gives a plan more time: to {v}."]}
# when the dream's name is long, the line names it by "the dream" alone (the HUD and the hover still show it)
NAMED_SHORT = {("dream", "became a passion"): ["The dream is no longer only a dream. It has become {N}'s passion: {p}.",
                                               "Tries that worked, and felt like {N}'s own, make the dream a passion: {p}."],
               ("dream", "became a plan"): ["{N} turns the dream into a five-year plan: to {v}."]}
LIFE_FROM = {"passion": "{N}'s passion becomes a life goal: {l}.", "dream": "{N} makes the dream a life goal: {l}.",
             "old dream": "An old dream comes back to {N}, now as a life goal: {l}.", "player": "You set {N} a life goal: {l}.",
             "": "{N} sets a life goal: {l}."}
LIFE_END = {"achieved": "{N} has reached a life goal: {l}.", "not reached in time": "A life goal stays out of reach: {l}.",
            "let go": "{N} lets a life goal go: {l}.", "pushed aside": "A life goal gives way to another: {l}.",
            "extended": "{N} keeps faith with a life goal: {l}."}
# the catalogue speaks of "one's own"; the story speaks of the character
THEIR = [(r"\bone's\b", "their"), (r"\boneself\b", "themselves"), (r"\bone is\b", "they are"), (r"\bone has\b", "they have"), (r"\bone does\b", "they do"),
         (r"\bone (knows|gets|arrives|speaks|wants|needs|sees|lives|loves|makes|leaves|finds)\b", lambda m: "they " + m.group(1)[:-1]),
         (r"\bone (goes|dies)\b", lambda m: "they " + m.group(1)[:-2] + ("" if m.group(1) == "goes" else "e"))]
AND_VERB = {"teach", "hand", "come", "go", "make", "keep", "bring", "take", "give", "live", "grow", "see", "find", "win", "build",
            "lead", "raise", "learn", "become", "stay", "return", "settle", "save", "walk", "run", "sing", "write", "read", "play",
            "help", "share", "carry", "pass", "serve", "protect", "open", "start", "travel", "bring", "die"}
DOUBLE = {"run", "win", "get", "sit", "swim", "set", "cut", "put", "stop", "plan", "shop", "travel", "map", "dig", "rid",
          "beg", "hug", "jog", "chat", "trek"}
PERSON = {"spy", "vet", "nurse", "architect", "scout", "knight", "priest", "mage", "bard", "prince", "princess", "champion",
          "paladin", "sellsword", "elder", "general", "witch", "warden", "one", "chef", "pilot", "judge", "monk", "nun", "poet",
          "artist", "chief", "smith", "sage", "seer", "shaman", "druid", "hero", "heroine", "captain", "queen", "king",
          "lawyer", "pianist", "dentist", "cook", "guide", "monarch", "mayor", "saint", "star", "diplomat", "pharmacist"}
NOT_PERSON = {"partner", "tower", "order", "river", "water", "corner", "border", "number", "letter", "summer", "winter",
              "power", "honour", "honor", "harbour", "harbor", "manor", "mirror", "chamber", "theatre", "centre", "flower",
              "silver", "timber", "collar", "altar", "dollar", "pillar", "calendar", "sugar", "nectar", "career", "charter"}


def their(s):
    """The catalogue's generic "one's own" in the story's words ("a garden of their own")."""
    for a, b in THEIR:
        s = re.sub(a, b, s)
    return s


def gerund(v):
    """marry -> marrying, raise -> raising, run -> running, be -> being, see -> seeing."""
    if v in ("be", "see", "flee", "agree", "free"):
        return v + "ing"
    if v.endswith("ie"):
        return v[:-2] + "ying"
    if v in DOUBLE:
        return v + v[-1] + "ing"
    if v.endswith("e") and not v.endswith(("ee", "ye", "oe")) and len(v) > 2:
        return v[:-1] + "ing"
    return v + "ing"


def is_person(name):
    """Whether a dream's name is someone to become ("a police officer", "the keeper of the camp's fire")."""
    head = re.split(r",| of | who | whose | to | in | at | between | that | for | on | with ", name)[0].strip()
    w = head.split()[-1].split("-")[-1].lower() if head else ""
    return w in PERSON or (bool(re.search(r"(er|or|ist|ian|ar)$", w)) and w not in NOT_PERSON)


def dream_of(name, domain=""):
    """A dream's name as the object of "the dream of": "to marry well" -> "marrying well", "a police officer" -> "becoming
    a police officer", "as clever as the trickster" -> "being as clever as the trickster", "a great love" stays."""
    n = their(name.strip())
    if n.startswith("to "):
        verb, _, rest = n[3:].partition(" ")
        rest = re.sub(r"\b(and|or) (\w+)\b", lambda m: m.group(1) + " " + (gerund(m.group(2)) if m.group(2) in AND_VERB else m.group(2)), rest)
        return gerund(verb) + (" " + rest if rest else "")
    if n.startswith("as "):
        return "being " + n
    if domain != "partner" and re.match(r"(a|an|the) ", n) and is_person(n):
        return "becoming " + n
    return n


_DREAMS = {}


def dream_catalogue():
    """The Library's dreams.py from the pinned engine copy, when it is there: names to phrases, sparks to say lines."""
    if "ok" not in _DREAMS:
        try:
            import dreams as D_
            _DREAMS["by_name"] = {d["name"]: d for d in D_.DREAMS}
            _DREAMS["say"] = {w: {tr[0]: tr[4] for tr in T if len(tr) > 4} for w, T in D_.DREAM_TRIGGERS.items()}
            _DREAMS["ok"] = True
        except Exception:
            _DREAMS.update(by_name={}, say={}, ok=False)
    return _DREAMS
# the inner voice, the resolution and its lessons: what the engine's explain.py names, in the game's words
DRIVER_WORD = dict(motives="what moves them", habit="habit", needs="what they lack", role="what is expected", goals="a dream or plan",
                   horizon="time feeling short", exit="what leaving would cost", values="what they believe in",
                   becoming="who they want to become", odds="the odds")
NEED_SAY = dict(safety="safety", belonging="belonging", autonomy="room to choose", competence="a sense of skill", meaning="meaning")
# looking back on a push (IDEAS.md, "Player intervention that helps", Emren 2026-10-09)
HINDSIGHT = dict(
    accepted=["*I didn't want this. But it gave me {need}, and I needed that.*",
              "Looking back, {N} is glad of the push: it brought {need} they were missing.",
              "*Fine. You were right this time.* It gave {N} {need} they had gone without."],
    resented_fail=["*I knew it. I should never have listened.*",
                   "{N} holds it against the voice that pushed them: it went badly, and it was never theirs.",
                   "*That was not mine to do, and it failed.*"],
    resented_empty=["*It worked. So what? It was never what I needed.*",
                    "It worked, but it gave {N} nothing they were missing, and they resent being pushed.",
                    "*Someone else's win, in my life.*"],
)
SURPRISE = {(True, "better"): "It works, better than {N} expected.", (True, "as expected"): "It works, as {N} expected.",
            (True, "worse"): "It works, though less well than {N} hoped.", (False, "better"): "It goes badly, though not as badly as {N} feared.",
            (False, "as expected"): "It goes badly, as {N} half expected.", (False, "worse"): "It goes badly, worse than {N} feared."}

# ------------------------------------------------------------------ scenes: (colors, text[, stages])
SCENES = {
    "playground dispute": [
        ("W", "In the {place} schoolyard, {rival} snatches a toy out of a smaller child's hands. Everyone knows that is not allowed, and everyone looks at {N}.", "E"),
        ("U", "{rival} and {N} both want the same toy at break. {N} notices that {rival} wants it more, and starts wondering what that is worth."),
        ("B", "{rival} has the best toy in the yard, and {N} wants it. Nobody is watching."),
        ("R", "{rival} shoves {N} in the queue, hard, and laughs. {Ns} face goes hot.", "E"),
        ("G", "The children in the yard have old rules about whose turn it is, and {rival} has just broken them."),
        ("W", "By the river, {rival} snatches a carved toy from a smaller child. Everyone knows that is not done, and everyone looks at {N}.", "T"),
        ("R", "{rival} shoves {N} into the mud, hard, and laughs. {Ns} face goes hot.", "T"),
        ("W", "In the academy courtyard, {rival} snatches a charmed toy from a smaller child. Everyone knows that is not allowed, and everyone looks at {N}.", "M"),
        ("R", "{rival} shoves {N} into the courtyard fountain, hard, and laughs. {Ns} face goes hot.", "M"),
    ],
    "hard school task": [
        ("W", "The teacher sets a hard task and expects it done properly, by Monday. {N} stares at the page.", "E"),
        ("U", "A problem at school will not come apart, however {N} turns it. It is maddening, and a little thrilling.", "E"),
        ("B", "There is a test, and the marks will decide who gets ahead next year. {N} cannot do half of it.", "E"),
        ("R", "The school task is long, dull and hard, and the sun is out. {N} can hear the others playing.", "E"),
        ("G", "{N} is stuck on the same lesson {parent} once struggled with, at the same age, in the same school.", "E"),
        ("W", "{teacher} sets {N} to learn the clan's long chant by the next moon, every word in its place.", "T"),
        ("U", "{N} cannot work out how to read the tracks {teacher} showed them, and it gnaws at them.", "T"),
        ("B", "The children who learn the hunt fastest will go out with the hunters first. {N} is falling behind.", "T"),
        ("R", "Learning to mend nets is slow, dull work, and the river is calling.", "T"),
        ("G", "{N} is learning the plant-lore {parent} once learned at this age, at the same fire.", "T"),
        ("W", "{teacher} sets a hard lesson and expects it copied in a perfect hand by dawn.", "M"),
        ("U", "A riddle in the old grammar of runes will not come apart, however {N} turns it. It is maddening, and a little thrilling.", "M"),
        ("B", "There is a trial at the academy, and the best will be chosen for the high tower. {N} cannot do half of it.", "M"),
        ("R", "The lesson is long, dull and dusty, and the fair is in the square. {N} can hear the music.", "M"),
        ("G", "{N} is stuck on the same herb-lore {parent} once struggled with, in the same old academy.", "M"),
    ],
    "family rule you dislike": [
        ("W", "{parent} lays down a new rule at home. It seems fair enough to everyone except {N}."),
        ("U", "{parent} forbids something, and when {N} asks why, the only answer is “because I said so”."),
        ("B", "A house rule stands between {N} and something they want. Rules have gaps, if you look for them."),
        ("R", "{parent} says no. Again. {N} feels it in their fists."),
        ("G", "“In this family we don't,” says {parent}, the way {grandparent} once said it."),
    ],
    "peer pressure to take a risk": [
        ("W", "{friend} and the others plan to sneak somewhere forbidden tonight. It is plainly against the rules, and they want {N} along."),
        ("U", "{friend} dares {N} to do something risky. Without meaning to, {N} starts working out the odds."),
        ("B", "{friend} has a risky plan that would make anyone who joins look bold. Being seen with the right people matters."),
        ("R", "{friend} grins: “Are you in or not?” It is reckless, and {Ns} heart is already racing."),
        ("G", "The whole group is going, {friend} included. Staying behind means being on the outside."),
    ],
    "choosing a path": [
        ("W", "Everyone in the {place} has an opinion about what {N} should become. {parent} talks about being useful to others.", "y"),
        ("U", "{N} has to choose what to do with their life, and there are so many fields to master that it is dizzying.", "y"),
        ("B", "Some paths lead to money and standing, others don't. {N} has noticed which is which.", "y"),
        ("R", "{N} must choose a path, and only one of them makes their heart beat faster. It is not the sensible one.", "y"),
        ("G", "{parent} hopes {N} will carry on what the family has always done. The work is in their hands already.", "y"),
        ("W", "{N} wonders whether the work they do still serves anyone. There are other ways to be useful.", "o"),
        ("U", "{N} has mastered their work and is bored of it. Something harder is calling.", "o"),
        ("B", "A better position is opening up, if {N} is willing to change course to get it.", "o"),
        ("R", "Halfway through life, {N} feels the old itch: is this really all?", "o"),
        ("G", "{N} thinks of the work their family did for generations, and wonders whether to go back to it.", "o"),
    ],
    "witnessing an injustice": [
        ("W", "In the {place}, {N} watches someone being cheated in plain sight. It is wrong, and somebody should say so."),
        ("U", "{N} sees something that does not add up: a neighbour treated badly, and an official story that cannot be true.", "E"),
        ("B", "{N} witnesses something shameful done by someone powerful. Knowing it could be worth a great deal."),
        ("R", "Right in front of {N}, someone weaker is being pushed around. {Ns} blood boils."),
        ("G", "An old neighbour is being turned out of the home their family has had for generations. {N} sees it happen."),
        ("W", "At an office in the {place}, {N} watches a clerk refuse someone their rights.", "E"),
        ("W", "At the clan gathering, {N} watches a family cheated of its share of the hunt.", "T"),
        ("U", "{N} sees something that does not add up: a neighbour blamed for a theft, and a story that cannot be true.", "T"),
        ("W", "At the magistrate's hall, {N} watches a clerk refuse a poor family their rights.", "M"),
        ("U", "{N} sees a hedge-witch blamed for a blight that no hedge-witch could have cast.", "M"),
        ("U", "{N} reads something that does not add up: someone innocent has been punished."),
        ("B", "{N} sees a rich family's child walk free for something that would have ruined anyone else."),
        ("R", "Someone on the street is being beaten, and people are walking past.", "EM"),
        ("R", "Someone is being beaten behind the longhouses, and people look away.", "T"),
        ("G", "Strangers have fenced off the common land the {place} has used for generations."),
    ],
    "conflict at work": [
        ("W", "At work, {colleague} keeps cutting corners and leaving others to pay for it. There are procedures for this.", "E"),
        ("U", "A problem at work has everyone blaming each other. {N} suspects the real cause is something nobody has looked at.", "E"),
        ("B", "{colleague} wants the same promotion as {N}, and {boss} is watching them both.", "E"),
        ("R", "{boss} humiliates {N} in front of everyone. {N} can barely keep still.", "E"),
        ("G", "The workplace is splitting into camps, and {N} has old friends on both sides.", "E"),
        ("W", "{N} discovers that {colleague} has been bending the rules at work, and others are covering for it.", "E"),
        ("U", "{boss} has made a decision at work that {N} can prove is wrong.", "E"),
        ("B", "A fight is brewing at work, and whoever wins it will run the place.", "E"),
        ("R", "{colleague} takes credit for {Ns} work, again. {N} is seething.", "E"),
        ("G", "{N} has worked beside {colleague} for years. Now they are on opposite sides.", "E"),
        ("W", "On the hunt, {colleague} keeps cutting corners and leaving others to carry the cost. The clan has customs for this.", "T"),
        ("U", "The catch has been poor for weeks and everyone blames each other. {N} suspects the cause is somewhere nobody has looked.", "T"),
        ("B", "{colleague} wants to lead the next hunt, and so does {N}. {boss} is watching them both.", "T"),
        ("R", "{boss} shames {N} in front of the whole hunting party. {N} can barely keep still.", "T"),
        ("G", "The work-gangs are splitting into camps, and {N} has kin on both sides.", "T"),
        ("W", "In the guild workshop, {colleague} keeps cutting corners with the wards and leaving others to answer for it.", "M"),
        ("U", "An enchantment the workshop sold has failed, and everyone blames each other. {N} suspects the flaw is in the old formula.", "M"),
        ("B", "{colleague} wants the same seat on the guild council as {N}, and {boss} is watching them both.", "M"),
        ("R", "{boss} humiliates {N} in front of the whole workshop. {N} can barely keep still.", "M"),
        ("G", "The guild is splitting into factions, and {N} has old friends on both sides.", "M"),
    ],
    "relationship strain": [
        ("W", "{N} and {close} keep breaking the same promises to each other. Something has to be settled."),
        ("U", "Things have gone quiet between {N} and {close}, and {N} keeps going over where it started."),
        ("B", "{N} has given more to {close} than they ever got back, and has started keeping count."),
        ("R", "{N} and {close} fight late into the night, about everything and about nothing."),
        ("G", "{N} and {close} have drifted apart, slowly, the way roots drift in dry ground."),
        ("W", "{N} and {close} cannot agree on what they owe each other any more."),
        ("U", "{N} has started noticing patterns in the arguments with {close}, and doesn't like what they show."),
        ("B", "{close} wants more of {N} than {N} wants to give."),
        ("R", "One careless word from {close}, and {N} is shouting."),
        ("G", "{N} and {close} sit at the same table every night, further apart each time."),
    ],
    "money: windfall or squeeze": [
        ("W", "An unexpected sum arrives, and {N} feels at once that some of it is owed to others.", "E"),
        ("U", "Money gets tight. {N} sits down with the numbers to see where it all goes.", "E"),
        ("B", "A windfall lands in {Ns} lap, and with it a chance to make it grow.", "EM"),
        ("R", "There is money to spare, for once, and {N} can already taste what it could buy.", "E"),
        ("G", "A hard season empties the purse, and {N} thinks first of the household and the old folk.", "EM"),
        ("W", "A relative needs money, and {N} has a little put aside.", "EM"),
        ("U", "{N} is offered a deal that sounds good, and wants to understand it before signing.", "E"),
        ("B", "{N} hears of a chance to double their savings, if they move quickly.", "E"),
        ("R", "Payday, and the whole {place} is going out.", "E"),
        ("G", "The roof leaks, the bills pile up, and the family looks to {N}.", "E"),
        ("W", "The hunt brings more than the family needs, and {N} feels at once that some of it is owed to others.", "T"),
        ("U", "Stores run low before winter. {N} counts what is left, and what it must last.", "T"),
        ("B", "A trader from the coast offers {N} a bargain, if they move before the others hear of it.", "T"),
        ("R", "A good season: there is meat and mead to spare, and {N} wants a feast.", "T"),
        ("G", "The stores are thin, and {N} thinks first of the old ones and the children.", "T"),
        ("W", "A purse of silver comes to {N} unexpectedly, and they feel at once that some of it is owed to others.", "M"),
        ("U", "Coin runs short. {N} sits down with the ledger to see where it all goes.", "M"),
        ("B", "A merchant of the spice guild offers {N} a share in a voyage, if they move quickly.", "M"),
        ("R", "There is silver to spare, for once, and the fair is in town.", "M"),
    ],
    "community problem": [
        ("W", "A problem in the {place} has gone unsolved for months, and the neighbours are meeting about it."),
        ("U", "The {place}'s well keeps running dry, and {N} keeps sketching how it could be fixed."),
        ("B", "Something in the {place} is broken and nobody is fixing it. Someone could ask a price for the fix."),
        ("R", "The council has promised to fix the same problem for a year. {N} is sick of waiting.", "E"),
        ("R", "The elders have promised to deal with the same problem for a year of moons. {N} is sick of waiting.", "T"),
        ("R", "The wardens have promised to fix the same problem for a year. {N} is sick of waiting.", "M"),
        ("G", "In the old days neighbours fixed these things together. Now the {place} just waits."),
        ("W", "The {place} needs volunteers for a problem nobody owns. {N} is asked to help organise."),
        ("U", "The {place} keeps patching the same broken thing. {N} wonders why nobody looks at the cause."),
        ("B", "There is a gap in what the {place} provides, and gaps can be filled, for a price."),
        ("R", "Another winter with the same problem in the {place}. {N} has had enough."),
        ("G", "The {place} has forgotten how to look after itself. {N} remembers how it used to be done."),
    ],
    "tempting shortcut": [
        ("W", "There is an easy way around the rules, and everyone seems to use it. {N} would not have to lie, exactly."),
        ("U", "A shortcut is on offer. {N} can see what it saves now, and is less sure what it costs later."),
        ("B", "A shortcut is there for the taking: a quiet word, a small favour, a door that should have been locked."),
        ("R", "The shortcut is wrong and it would be thrilling. {Ns} pulse quickens."),
        ("G", "{elder} never took shortcuts, and {N} knows it. But this one is so easy."),
        ("W", "Someone offers to fix {Ns} paperwork, for a small fee and no questions.", "E"),
        ("U", "{N} spots a loophole nobody else has noticed.", "EM"),
        ("B", "A friend in the right office could make things easier for {N}, for a favour later.", "E"),
        ("W", "There is a way around the clan's customs that everyone pretends not to see.", "T"),
        ("U", "{N} notices that the elders never count the stores twice.", "T"),
        ("B", "A word with the chief's nephew could make things easier for {N}, for a favour later.", "T"),
        ("W", "A clerk of the magistrate offers to fix {Ns} papers, for a small fee and no questions.", "M"),
        ("B", "A friend in the Order could make things easier for {N}, for a favour later.", "M"),
        ("R", "A charm from the night market would do a month's work in an hour. It is forbidden, and nobody would know.", "M"),
        ("R", "A shortcut is there, right now, and nobody would ever know."),
        ("G", "{N} could skip the slow way their family has always done it."),
    ],
    "raising a child": [
        ("W", "{child} is testing every limit at home. {N} feels the weight of being the one who sets them."),
        ("U", "{child} asks why the sky is blue, why people die, why {N} said one thing and did another."),
        ("B", "{child} is falling behind the other children, and {N} cannot stand to see them lose."),
        ("R", "{child} is wild and restless and has {Ns} temper. They clash, and love each other fiercely."),
        ("G", "{child} is growing fast, and {N} wonders which of the old ways to hand down."),
    ],
    "chance to innovate": [
        ("W", "There is a better way to do the work, and {N} could make it the standard if they wrote it down."),
        ("U", "An idea takes hold of {N}: a new way to do the work, if it holds up."),
        ("B", "{N} has spotted something nobody else has, and it could be worth a great deal."),
        ("R", "{N} wakes up with an idea burning in their head and cannot think of anything else."),
        ("G", "Everyone says the old way can be improved. {N} isn't sure it should be."),
        ("W", "{N} sees how the work could be organised better for everyone."),
        ("U", "{N} has been tinkering for months, and something finally works."),
        ("B", "{N} notices a need nobody is meeting, and a profit nobody is taking."),
        ("R", "A wild idea seizes {N} in the middle of the night."),
        ("G", "{N} finds a forgotten old method that might work better than the new ones."),
    ],
    "crisis or disaster": [
        ("W", "{disaster} strikes the {place}, and people stand about, waiting for someone to take charge."),
        ("U", "{disaster} hits the {place}. Amid the panic, {N} tries to see what will happen next."),
        ("B", "{disaster} hits the {place}. In a crisis everything is suddenly up for grabs, food and safety first."),
        ("R", "{disaster} tears through the {place}. Someone is shouting for help two doors down.", "EM"),
        ("R", "{disaster} tears through the {place}. Someone is screaming for help in the smoke.", "T"),
        ("G", "{disaster} comes to the {place}, as it has before and will again. The old people know what to do."),
        ("W", "{disaster} leaves the {place} in chaos. Someone has to organise the shelters."),
        ("U", "When {disaster} comes, the warnings {N} read about turn out to be right."),
        ("B", "{disaster} wrecks the {place}, and suddenly food is worth more than friendship."),
        ("R", "{disaster}: smoke, sirens, and people running. {Ns} heart pounds."),
        ("G", "{disaster} sweeps through the {place}. Neighbours gather at the old meeting place."),
    ],
    "bereavement": [
        ("W", "{dead} dies. {N} is dressed in their best clothes and told how to behave at the funeral.", "k"),
        ("W", "{dead} dies. There is a funeral to arrange, and a family that looks to {N} to do it properly.", "a"),
        ("U", "{dead} is gone. {N} keeps returning to the how and the why, as if understanding could undo it."),
        ("B", "{dead} dies, and leaves a gap: in the house, in the will, in who decides things now.", "a"),
        ("B", "{dead} dies. {N} notices how the grown-ups start arguing over the things left behind.", "k"),
        ("R", "{dead} is gone, suddenly, and {N} feels it like a blow to the chest."),
        ("G", "{dead} dies in the autumn, as old things do. The garden goes on growing."),
        ("W", "Word comes that {dead} has died. {N} puts on dark clothes and goes to sit with the family.", "a"),
        ("U", "{dead} dies after a long illness. {N} had read everything about it, and still it comes as a shock.", "a"),
        ("B", "{dead} dies, and {N} is surprised by how much it costs them.", "a"),
        ("R", "The news about {dead} comes at night. {N} throws the phone across the room.", "aE"),
        ("R", "Word of {dead}'s death comes with a runner at dusk. {N} howls at the sky.", "aT"),
        ("G", "{dead} is given back to the earth on the hill where the old ones sleep.", "T"),
        ("R", "A raven brings word of {dead}'s death. {N} hurls the letter into the fire.", "aM"),
        ("G", "{dead}'s spirit lingers three nights by the hearth, then goes.", "M"),
        ("G", "{dead} goes quietly, in their sleep, the way the old ones hope to."),
    ],
    "thinking about legacy": [
        ("W", "{N} has started asking what they will leave the {place} when they are gone."),
        ("U", "{N} has learned a great deal in one life, and most of it will die with them unless they pass it on."),
        ("B", "{N} wants their name to outlast them, and their fortune to stay in the right hands."),
        ("R", "Time is running out, and {N} feels it every morning. There is still so much to feel."),
        ("G", "{N} walks the old paths and thinks about who will tend them afterwards."),
    ],
    "meeting someone": [
        ("W", "{prospect} comes from a good family in the {place}, and people are already saying what a fine match it would be."),
        ("U", "{N} meets {prospect}, who argues with them about everything and is usually right."),
        ("B", "{prospect} is well connected, admired, and interested in {N}."),
        ("R", "{N} meets {prospect} and forgets, for a while, everything else."),
        ("G", "{prospect} has been around for years, a friend of a friend. Lately it feels different."),
        ("W", "At a family gathering, {N} is introduced to {prospect}, with meaningful looks all round."),
        ("U", "{N} and {prospect} meet over a problem neither can solve alone, and talk until morning."),
        ("B", "{prospect} could open doors for {N}, and seems to know it."),
        ("R", "{prospect} laughs at something {N} says, and {N} is lost."),
        ("G", "{prospect} grew up three streets away. {N} has known them a little, all their life.", "EM"),
        ("G", "{prospect} grew up three fires away. {N} has known them a little, all their life.", "T"),
    ],
    "deciding about children": [
        ("W", "Everyone in the {place} seems to expect {N} to start a family, and asks when."),
        ("U", "{N} lists the reasons for and against having children, and the list keeps growing on both sides."),
        ("B", "{N} thinks about who will carry the family name and inherit what they have built."),
        ("R", "Some days {N} wants a house full of noise; other days, nothing but their freedom."),
        ("G", "{Ns} parents had children young, and their parents before them. {N} feels the old pull."),
        ("W", "{Ns} family has started asking, at every dinner, about grandchildren."),
        ("U", "{N} reads everything they can about raising children, and is no closer to a decision.", "EM"),
        ("U", "{N} watches how the other families manage, and still cannot decide.", "T"),
        ("B", "{N} wonders what a child would cost them, and what one would carry forward."),
        ("R", "{N} holds a friend's baby and feels something they did not expect."),
        ("G", "Spring comes, the trees flower, and {N} thinks about children."),
    ],
    "a search for meaning": [
        ("W", "{N} has started going to services in the {place} again, and is surprised how much the order of it helps.", "E"),
        ("U", "{N} lies awake asking what any of it is for, and cannot settle for an easy answer."),
        ("B", "{N} hears of a circle that promises its members strength, and the secrets of getting on."),
        ("R", "{N} wants to believe in something with their whole heart, and hasn't found it yet."),
        ("G", "{N} keeps thinking of the old ways of their grandparents, and the faith that came with them."),
        ("W", "{N} finds comfort in the old rituals, and wonders whether to take them more seriously."),
        ("U", "{N} reads philosophy late into the night, looking for something solid.", "E"),
        ("W", "{N} sits longer at the fire ceremonies, surprised how much the order of them helps.", "T"),
        ("U", "{N} keeps asking the old ones what the stars are for, and no answer satisfies them.", "T"),
        ("W", "{N} has started attending the temple rites again, and finds comfort in their order.", "M"),
        ("U", "{N} reads forbidden treatises in the archive late into the night, looking for something solid.", "M"),
        ("G", "{N} keeps returning to the standing stones, where the old gods are said to listen.", "M"),
        ("B", "{N} wants a creed that works: one that makes them stronger."),
        ("R", "{N} is overwhelmed by feeling at a gathering, and cannot forget it."),
        ("G", "{N} walks in the woods and feels, for a moment, part of something very old."),
    ],
    "your group must decide how to act": [
        ("W", "{Ns} group has to decide something together, and already everyone is talking over everyone else."),
        ("U", "The group has a decision to make, and {N} can see three ways it could go wrong."),
        ("B", "The group must decide what to do, and {friend} is quietly lining up votes."),
        ("R", "The group can't agree. {N} is ready to just do something."),
        ("G", "The group must decide, and {N} keeps glancing at {friend2}, who always gets left out."),
    ],
    "something is wrong where you live": [
        ("W", "Something has gone wrong in the {place}: rules ignored, rubbish piling up, officials looking away.", "E"),
        ("W", "Something has gone wrong in the {place}: customs ignored, quarrels unsettled, the elders looking away.", "T"),
        ("W", "Something has gone wrong in the {place}: wards left to fade, laws ignored, the wardens looking away.", "M"),
        ("U", "Something is souring the {place}'s wells, and the hedge-mages cannot say what.", "M"),
        ("U", "Something in the {place} is failing, and nobody seems to know why. {N} starts asking questions."),
        ("B", "The {place} is going to ruin, and somebody is profiting from it. {N} wonders who."),
        ("R", "The {place} is falling apart and the people in charge do nothing. {N} is furious."),
        ("G", "The {place} is not what it was. The old neighbours have gone, and the new ones keep to themselves."),
    ],
    "a crossroads in how you live": [
        ("W", "{N} looks at the life they have built and asks whether it is a good one."),
        ("U", "{N} sits with a question avoided for years: is this the life they would design, if they could start again?"),
        ("B", "{N} has power enough now to change course. The question is how far they are willing to go."),
        ("R", "{N} wakes up one morning knowing that something has to change, and soon."),
        ("G", "{N} feels the years settle on them, and asks what will last."),
        ("W", "{N} wonders whether they have lived as well as they could, for others."),
        ("U", "{N} drafts, in their head, a better version of their own life."),
        ("B", "{N} sees how far others have climbed, and measures themselves against them."),
        ("R", "{N} is bored, deeply, of the life they have, and the boredom is turning into something hotter."),
        ("G", "{N} visits the place they grew up and feels the pull of where they came from."),
    ],
    "reconsidering a commitment": [
        ("W", "{N} has been loyal to {kindref} for years. Lately, loyalty feels more like duty than love."),
        ("U", "{N} keeps turning {kindref} over in their mind, looking for the flaw."),
        ("B", "{N} wonders what {kindref} still does for them."),
        ("R", "{N} feels caged by {kindref}, and the feeling is getting louder."),
        ("G", "{N} has put down deep roots in {kindref}. Pulling them up would tear something."),
        ("W", "{N} still does everything {kindref} asks of them, and is no longer sure why."),
        ("U", "{N} has started to see {kindref} from the outside, as if it belonged to someone else."),
        ("B", "{N} is counting what {kindref} costs them, and what it pays."),
        ("R", "Some mornings {N} wants to burn {kindref} to the ground and start again."),
        ("G", "{kindref_cap} has been part of {N} so long that doubting it feels like doubting the weather."),
    ],
}

# ------------------------------------------------------------------ outcomes: (success lines, failure lines)
OUTCOMES = {
    "playground dispute": (["The grown-ups sort it out, and {N} goes home feeling taller.", "By the end of break the fight is forgotten, and {rival} is almost a friend."],
                           ["It ends in tears and a note sent home.", "{rival} wins this one, and the whole yard sees it."]),
    "hard school task": (["The answer comes, and for once it earns praise.", "{N} gets it done, and better than expected."],
                         ["The task comes back covered in red ink.", "{N} falls behind, and feels it."]),
    "family rule you dislike": (["It goes the way {N} wanted, more or less.", "Home is calm again by supper."],
                                ["{parent} is angry, and the house is cold for days.", "{N} is caught, and the rule only gets stricter."]),
    "peer pressure to take a risk": (["Nobody gets hurt, and the story improves each time it is told.", "{N} comes out of it with a little more standing among friends."],
                                     ["It goes wrong: someone is caught, and there is trouble at home.", "{N} ends up on the wrong side of the group, for a while."]),
    "choosing a path": (["The way opens.", "It feels, for once, like the right road."],
                        ["The door does not open, not this time.", "The first steps go badly, and doubt creeps in."]),
    "witnessing an injustice": (["Something is put right, in the end.", "The person who was harmed is not left alone with it."],
                                ["Nothing changes, and {N} carries it home.", "It backfires, and {N} is the one who pays."]),
    "conflict at work": (["The trouble at work settles, and {N} comes out of it well.", "{boss} notices how {N} handled it."],
                         ["The trouble at work gets worse before it gets better.", "{N} loses ground at work, and knows it."]),
    "relationship strain": (["{N} and {close} find their way back to each other.", "The air between {N} and {close} clears."],
                            ["The distance between {N} and {close} grows.", "Words are said that cannot be taken back."]),
    "money: windfall or squeeze": (["What there is goes where it should, and there is more security after.", "{N} comes out of it better off."],
                                   ["It slips through {Ns} fingers.", "It ends with less than before, and a lesson."]),
    "community problem": (["The {place} is a little better for it.", "Neighbours nod at {N} as they pass, now."],
                          ["Nothing gets fixed, and the meetings go on.", "{N} makes enemies in the {place} over it."]),
    "tempting shortcut": (["It works out, with no harm done that anyone can see.", "{N} sleeps well that night."],
                          ["It catches up with {N}.", "{N} gets burned, and others see it."]),
    "raising a child": (["{child} comes through it well.", "There is a good stretch at home after that."],
                        ["{child} pulls away for a while.", "It ends in slammed doors."]),
    "chance to innovate": (["The new way works.", "{N} has made something that did not exist before."],
                           ["The idea fails, expensively.", "It doesn't work, and people say they knew it wouldn't."]),
    "crisis or disaster": (["{N} comes through it, and so do the people near them.", "The {place} recovers, and {N} played a part."],
                           ["The disaster takes more than it should have.", "{N} comes out of it hurt and shaken."]),
    "bereavement": (["The grief finds somewhere to go.", "In time the loss becomes something {N} can carry."],
                    ["The grief stays raw for a long time.", "{N} closes up around the loss."]),
    "thinking about legacy": (["Something of {N} will outlast them.", "It feels like a life well spent."],
                              ["Nothing comes of it, and the years keep moving.", "The people {N} hoped to reach do not seem to care."]),
    "meeting someone": (["Something real starts between {N} and {prospect}.", "{prospect} becomes part of {Ns} life."],
                        ["It fizzles out before it begins.", "{prospect} moves on, and {N} is left wondering."]),
    "deciding about children": (["{N} feels at peace with the decision.", "The decision holds, and feels right."],
                                ["The decision brings more strain than {N} expected.", "It does not go as planned, and {N} feels it."]),
    "a search for meaning": (["{N} finds something to hold on to.", "Something in {N} settles."],
                             ["The search goes on, emptier than before.", "It doesn't answer the question after all."]),
    "your group must decide how to act": (["The group pulls together, and {N} had a hand in it.", "It works, and the group remembers who made it work."],
                                          ["The group splits, and some friendships with it.", "It goes badly, and the blame lands on {N}."]),
    "something is wrong where you live": (["Things in the {place} begin to turn around.", "Something gets fixed, and people notice."],
                                          ["The {place} goes on as before, only worse.", "{N} spends a great deal and changes little."]),
    "a crossroads in how you live": (["The new way of living holds.", "The choice feels like coming home to themselves."],
                                     ["The change goes badly, and the old life is harder to return to.", "{N} pays dearly for the turn."]),
    "reconsidering a commitment": (["{kindref_cap} feels like {Ns} own again.", "It feels settled now."],
                                   ["Nothing feels settled.", "The doubt doesn't leave."]),
    "an ordinary week": (["A good week."], ["A flat week."]),
}

# ------------------------------------------------------------------ the character's thoughts
REASON = {   # why they lean toward an act: the act's own colors speak
    "W": ["It's the right thing to do.", "Someone has to do this properly.", "What would a decent person do here?", "There are rules for a reason."],
    "U": ["Think first. Then act.", "There's a smarter way through this.", "I want to understand it before I touch it.", "Let me see how it works."],
    "B": ["What do I get out of this?", "Nobody else is going to look out for me.", "Use what you have.", "Winning is what counts."],
    "R": ["Don't think. Go.", "I'm sick of waiting.", "My gut already knows.", "If it feels right, it is right."],
    "G": ["This is how it has always been done.", "Let things take their course.", "Stay close to your own.", "Don't fight what is meant to be."],
}
REACT = {   # how they read an outcome: the voice speaks
    "W": (["That's how it should be done.", "We did right by each other.", "Doing it properly paid off."],
          ["I did what was right. It wasn't enough.", "Somebody broke faith, and it wasn't me.", "Rules only work if everyone keeps them."]),
    "U": (["Good. I understood it in time.", "So the plan holds up.", "Now I know how this works."],
          ["I missed something. I'll find out what.", "Where did my reasoning go wrong?", "Next time I'll know more."]),
    "B": (["Good. I came out ahead.", "One more thing I control.", "They'll remember who did that."],
          ["Next time I look after myself first.", "Nobody does me any favours.", "I won't be caught like that again."]),
    "R": (["Yes. That's how it should feel.", "I followed my heart, and it held.", "That felt alive."],
          ["Damn it. Damn all of it.", "Fine. At least I felt something.", "I'll do it differently, and louder."]),
    "G": (["Things settle when you let them.", "That's the way of it.", "We are still here. That's what matters."],
          ["Some things aren't meant to be.", "It will pass, like everything does.", "I pushed against the grain."]),
}
REACT_GRIEF = {
    "W": (["We did right by them."], ["I couldn't even do this properly."]),
    "U": (["I understand it a little better now."], ["No answer is good enough."]),
    "B": (["Life goes on, and so do I."], ["Nobody helped me through this."]),
    "R": (["I let it out. That was right."], ["It hurts. It just hurts."]),
    "G": (["Everything returns to the earth."], ["Some wounds stay open."]),
}
RELUCT = {   # a pick they did not want: who they are pushes back
    "W": ["It isn't right. But fine.", "This goes against everything I was taught."],
    "U": ["This makes no sense to me.", "I can already see how this goes wrong."],
    "B": ["And what's in this for me?", "I'm being used."],
    "R": ["Who decided this for me?", "Everything in me says no."],
    "G": ["This isn't our way.", "This goes against the grain of me."],
}
BIG_WIN_SOFT = [("", "It helps more than {N} expected."), ("W", "It brings the family closer than it has been in years."),
                ("U", "It makes a strange kind of sense, in the end."), ("B", "{N} comes out of it stronger."),
                ("R", "Something in {N} breaks open, and heals."), ("G", "It eases something deep in {N}.")]
SOMBER = {"bereavement", "crisis or disaster"}
NEW_KIN = dict(friend=("friend", "their closest friend {n}"), sibling=("sibling", "their sibling {n}"),
               grandparent=("grandparent", "their grandparent {n}"), partner=("partner", "their partner {n}"),
               parent=("mother", "their mother {n}"), child=("child", "their child {n}"))
LEFT_BEHIND = ("friend", "rival", "teacher", "neighbour", "old neighbour", "colleague", "boss")   # who stays when the family moves

KILLS = {"parent": ("mother", "father"), "grandparent": ("grandparent",), "sibling": ("sibling",), "friend": ("friend",),
         "partner": ("partner",), "child": ("child",), "mentor": ("mentor",)}   # library kills: role -> cast roles
BIG_WIN = [("", "It is better than {N} had dared to hope."), ("W", "It is more than {N} deserved, they think."),
           ("U", "It goes better than any of {Ns} calculations."), ("B", "{N} can hardly believe their luck."),
           ("R", "It is glorious."), ("G", "It feels like a gift.")]
BIG_LOSS = [("", "It hits {N} hard."), ("W", "It feels like a judgement."), ("U", "It is worse than anything {N} had foreseen."),
            ("B", "It costs {N} dearly."), ("R", "It hits {N} like a fist."), ("G", "It shakes {N} to the roots.")]
MISSED = (["Not what I wanted. But it worked.", "Funny how things turn out.", "Fine. It'll do."],
          ["I never wanted this anyway.", "I should have trusted myself.", "That's what I get for settling."])
RELUCT_LOW = ["Fine. Why not.", "All right, then.", "Could be worse."]
OUT_OF_REACH = ["I don't even have what this takes.", "This is beyond me, and I know it."]

# ------------------------------------------------------------------ yearly chapters
MOOD = {   # (content, peace) bands -> lines through each color's eyes; "k" lines are for children under 12
    "hh": [("W", "A good, orderly year: promises kept on all sides.", "a"), ("W", "A year of doing things well, and being thanked for it.", "a"),
           ("U", "A year of quiet progress; {N} understands a little more than before.", "a"), ("U", "A clear-headed year: problems come apart in {Ns} hands.", "a"),
           ("B", "A profitable year, by {Ns} own reckoning.", "a"), ("B", "A year of advantage: {N} ends it stronger than they began.", "a"),
           ("R", "A bright year, lived at full volume and without regret.", "a"), ("R", "A year that tastes of summer, start to finish.", "a"),
           ("G", "A year that ripens in its own time, like a good harvest.", "a"), ("G", "A year rooted in good soil: family close, days unhurried.", "a"),
           ("W", "A good year at home: {N} is praised for being good.", "k"), ("U", "A bright, curious year; {N} asks a thousand questions.", "k"),
           ("B", "A good year: {N} gets most of what they want.", "k"), ("R", "A happy, noisy year of games and scraped knees.", "k"),
           ("G", "A warm year, close to family.", "k")],
    "hl": [("W", "Things go well, yet {N} lies awake over what is still owed.", "a"), ("W", "A year of success, and of obligations that never end.", "a"),
           ("U", "Plenty of success, and a mind that will not stop turning.", "a"), ("U", "Good results, and no rest from the questions behind them.", "a"),
           ("B", "{N} is winning, and cannot afford to rest.", "a"), ("B", "A good year, spent looking over their shoulder.", "a"),
           ("R", "A year of highs, and no stillness anywhere in it.", "a"), ("R", "A blazing year that leaves {N} wired and sleepless.", "a"),
           ("G", "Plenty on the table, and a restlessness {N} cannot name.", "a"), ("G", "A full year that never quite settles.", "a"),
           ("", "A busy, overexcited year; {N} sleeps badly.", "k"), ("R", "A year of tantrums and big joys.", "k"),
           ("W", "{N} tries so hard to be good that they forget to rest.", "k")],
    "lh": [("W", "Not much goes {Ns} way, and still they keep their word, calmly.", "a"), ("W", "A thin year, met with patience and good manners.", "a"),
           ("U", "A lean year, met with patience: {N} watches and learns.", "a"), ("U", "Little goes right, and {N} takes notes.", "a"),
           ("B", "A poor year, which {N} bears coolly, waiting for a better hand.", "a"), ("B", "A lean year; {N} keeps their head down and their cards close.", "a"),
           ("R", "A dull year; even so, {N} is oddly at peace.", "a"), ("R", "A slow year, and for once {N} doesn't fight it.", "a"),
           ("G", "A thin year, borne the way winters are borne.", "a"), ("G", "A fallow year; {N} lets it be one.", "a"),
           ("", "A quiet year; {N} keeps to themselves and doesn't seem to mind.", "k"), ("G", "A slow year, mostly spent at home.", "k")],
    "ll": [("W", "A hard year: duties pile up, and nobody thanks {N} for them.", "a"), ("W", "A year of broken promises, some of them {Ns} own.", "a"),
           ("U", "A hard year, and no amount of thinking makes it make sense.", "a"), ("U", "A year of problems with no solutions in sight.", "a"),
           ("B", "A bitter year; {N} trusts nobody, and is right not to.", "a"), ("B", "A losing year, and {N} keeps count of every loss.", "a"),
           ("R", "A wretched year, full of fights and bad nights.", "a"), ("R", "A year {N} spends angry, at everything.", "a"),
           ("G", "A hard year; {N} feels cut off from everything that used to hold them.", "a"), ("G", "A year of drought, inside and out.", "a"),
           ("", "A hard year for a child: tears at night, trouble with the other children.", "k"), ("R", "A year of fights in the yard and sulks at home.", "k"),
           ("W", "A year of being told off, for things {N} doesn't understand.", "k"), ("U", "A lonely year; {N} retreats into their own head.", "k"),
           ("B", "A year of learning that nobody gives you anything for free.", "k"), ("G", "{N} misses something they cannot name, all year.", "k")],
    "mm": [("W", "An ordinary year of work and obligations.", "a"), ("W", "A year of keeping things in order.", "a"),
           ("U", "An unremarkable year, spent learning small things.", "a"), ("U", "A year of small puzzles and small answers.", "a"),
           ("B", "A year of small gains and small losses.", "a"), ("B", "A year of quiet positioning.", "a"),
           ("R", "A year that passes in fits and starts.", "a"), ("R", "A restless, ordinary year.", "a"),
           ("G", "A year like many others, and none the worse for it.", "a"), ("G", "A year that turns like the seasons do.", "a"),
           ("", "Another year of games, chores and growing.", "k"), ("U", "A year of learning to read the world.", "k"),
           ("R", "A year of running about.", "k"), ("G", "A year of family dinners and long summers.", "k"),
           ("W", "A year of chores, lessons and early nights.", "k"), ("B", "A year of small trades and secrets.", "k")],
}
WEEKS = {   # what the ordinary weeks went to
    "W": [("Most days go to lessons and chores, done the way {parent} asks.", "k"), ("{N} learns to keep their room tidy and their promises.", "k"),
          ("Most weeks go to routine and duty: chores done, promises kept.", "a"), ("{N} keeps a steady routine, week after week.", "a"),
          ("{Ns} weeks run like a good clock.", "a"),
          ("Most days go to the shared work of the camp: hides, nets, firewood.", "aT"), ("Most weeks go to duty: the guild's hours kept, the household wards renewed.", "aM")],
    "U": [("{N} spends spare hours taking things apart to see how they work.", "k"), ("{N} reads under the covers long after lights out.", "kE"), ("{N} spends hours watching how the beavers build.", "kT"),
          ("{N} sneaks into the archive to read about the old wars.", "kM"),
          ("Spare hours go to learning something on the side.", "a"), ("Evenings go to books and half-finished projects.", "aE"), ("Evenings go to carving and half-finished snares.", "aT"),
          ("Evenings go to old books and half-finished experiments.", "aM"),
          ("{N} teaches themselves something new, a little every week.", "a"),
          ("{N} spends spare hours learning the stars and the tracks.", "aT"), ("Spare hours go to the archive and its dusty grimoires.", "aM")],
    "B": [("{N} learns to trade, bargain and keep what is theirs.", "k"), ("{N} learns which grown-ups can be talked round.", "k"),
          ("Most weeks, {N} looks after their own interests first.", "a"), ("{N} spends the weeks quietly building their own position.", "a"),
          ("{N} spends the year making useful friends.", "a"),
          ("{N} spends the weeks trading favours and quietly gathering what is theirs.", "aT"), ("{N} spends the weeks courting patrons and collecting debts.", "aM")],
    "R": [("{N} spends the year running, climbing and shouting, never still.", "k"), ("{N} is always off somewhere, chasing something.", "k"),
          ("The weeks go by on impulse: whatever {N} feels like, when they feel like it.", "a"), ("{N} chases whatever excites them that week.", "a"),
          ("Late nights, sudden trips, new crazes: {N} lives on impulse.", "a"),
          ("{N} lives for the hunt, the dance and the night fires.", "aT"), ("{N} chases fairs, duels of wit and whatever the night market offers.", "aM")],
    "G": [("{N} spends long days outdoors and with family.", "k"), ("{N} follows {elder} around, learning the old ways of doing things.", "k"),
          ("Most weeks go to home, body and kin.", "a"), ("{N} tends the household and the people in it.", "a"),
          ("{N} spends the year close to home: meals, walks, visits to family.", "a"),
          ("{N} spends the year close to camp and kin, following the seasons.", "aT"), ("{N} tends a herb garden and the old shrine at the end of the lane.", "aM")],
}
SHIFT = ["Slowly, the {old} that used to drive {N} gives ground to {new}.",
         "{N} is not who they were a few years ago: less {old_adj}, more {new_adj}.",
         "Something has shifted in {N}: where {old} once led, {new} leads now."]

# ------------------------------------------------------------------ the outside world
OUTSIDE = {
    "new friends with a different way of life": [
        ("", "{N} falls in with {newfriend} and their crowd, who live very differently from anyone {N} grew up with.", "a"),
        ("W", "{N} makes new friends, {newfriend} among them, whose rules are not the family's rules.", "a"),
        ("R", "New friends, wild ones: {newfriend} and the rest pull {N} into a different kind of life.", "a"),
        ("", "At play {N} makes a new friend, {newfriend}, whose family does everything differently.", "k"),
        ("R", "{N} falls in with {newfriend}, the wildest child on the street.", "kEM"),
        ("R", "{N} falls in with {newfriend}, the wildest child in the camp.", "kT")],
    "your circle closes ranks around its norms": [
        ("", "{Ns} circle closes ranks: there is one right way to be, and everyone is watched.", "a"),
        ("G", "The old crowd closes ranks around how things have always been done.", "a"),
        ("U", "{N} notices how quickly their friends turn on anyone who is different.", "a"),
        ("", "The other children decide who belongs and who doesn't. {N} learns the rules fast.", "k")],
    "moving somewhere new": [
        ("", "{N} moves to a {newplace}. Everything familiar is left behind.", "a"),
        ("R", "A fresh start: {N} moves to a {newplace}, and feels lighter for it.", "a"),
        ("G", "{N} leaves the {oldplace} for a {newplace}, with a heavy heart.", "a"),
        ("", "The family moves to a {newplace}. {N} cries the whole way there.", "k"),
        ("U", "The family moves to a {newplace}, and {N} explores every corner of it.", "k")],
    "a mentor takes you under their wing": [
        ("", "{mentor} takes an interest in {N} and starts teaching them what they know."),
        ("U", "{mentor} sees something in {N}, and starts lending them books and hard questions."),
        ("W", "{mentor} takes {N} under their wing and shows them how things are properly done.")],
    "a friend's life choice makes you wonder": [
        ("", "{friend} makes a choice that surprises everyone, and {N} can't stop thinking about it."),
        ("R", "{friend} drops everything to chase something new. {N} is a little envious.")],
    "a new rule changes how things are done": [
        ("", "A new rule comes down from above, and everyday things are done differently now.", "aE"),
        ("W", "New regulations arrive, and {N} reads them closely.", "aE"),
        ("R", "Another new rule. {N} rolls their eyes.", "a"),
        ("", "A new headteacher arrives at school, with new rules for everything.", "kE"),
        ("", "A new elder takes charge of the children's lessons, with new rules for everything.", "kT"),
        ("", "The chief proclaims a new law, and everyday things are done differently now.", "aT"),
        ("", "A new master arrives at the academy, with new rules for everything.", "kM"),
        ("", "The Archmage's council decrees a new law, and everyday things are done differently now.", "aM"),
        ("W", "A new decree is read out in the square, and {N} listens to every word.", "aM")],
    "an institution rewards a kind of person": [
        ("", "{N} notices who gets ahead at {inst}, and what kind of person they are."),
        ("B", "{inst_cap} starts rewarding a certain kind of person. {N} takes note.")],
    "you are judged by an official process": [
        ("", "{N} sits an exam that will decide a great deal.", "kE"),
        ("", "{N} is judged by an official process: a hearing, a review, forms in triplicate.", "aE"),
        ("", "{N} must pass the elders' test before the first hunt.", "kT"),
        ("", "{N} is brought before the elders to answer for a quarrel.", "aT"),
        ("", "{N} sits the academy's entrance trial, which will decide a great deal.", "kM"),
        ("", "{N} is summoned before the magistrate's tribunal, scrolls and seals and all.", "aM")],
    "a book, film or idea grips you": [
        ("", "A book falls into {Ns} hands and will not let go of them.", "EM"),
        ("W", "A sermon, or a speech, stays with {N} for weeks.", "EM"),
        ("G", "An old story told by {elder} stays with {N} for weeks."),
        ("U", "An idea grips {N} for weeks: they fill notebooks with it.", "EM"),
        ("R", "A song, a film, a night of music: something sets {N} on fire.", "E"),
        ("U", "An idea grips {N} for a whole moon: they cannot stop scratching it into the dirt.", "T"),
        ("R", "A night of drums around the great fire sets {N} on fire.", "T"),
        ("W", "A speech by the chief at the gathering stays with {N} for many days.", "T"),
        ("R", "A troupe of travelling players comes through, and their music sets {N} on fire.", "M"),
        ("U", "A spellbook falls into {Ns} hands and will not let go of them.", "M")],
    "small daily frictions add up": [
        ("", "Small frictions pile up: a leaking roof, a quarrelsome neighbour, a hundred little chores."),
        ("R", "Everything grates this month: every chore, every neighbour.")],
    "an illness": [
        ("", "{N} falls ill and is laid up for weeks."),
        ("R", "A fever lays {N} low; being still is its own torment."),
        ("G", "{N} falls ill, and is looked after by {carer}.")],
    "an unexpected windfall or loss of money": [
        ("", "A bill nobody saw coming, and {Ns} savings are suddenly thinner.", "E"),
        ("B", "Money goes missing that {N} had counted on, and they take it personally.", "EM"),
        ("", "A store-pit floods, and half of what {N} put by is ruined.", "T"),
        ("B", "Someone has been taking from {Ns} stores, and they take it personally.", "T"),
        ("", "A debt nobody saw coming, and {Ns} purse is suddenly lighter.", "M")],
    "a natural disaster hits where you live": [
        ("", "{disaster} hits the {place}. Houses are damaged and people are hurt."),
        ("G", "{disaster} comes to the {place}, the worst the old people can remember.")],
    "a hard season of scarcity": [
        ("", "A lean season: prices climb, shelves empty, everyone tightens their belt.", "E"),
        ("G", "A bad harvest year. Everyone makes do with less."),
        ("W", "Hard times: rationing, queues, and neighbours sharing what they have.", "E"),
        ("B", "Hard times. {N} learns who hoards, and who shares."),
        ("", "A lean season: the game moves away, and everyone tightens their belt.", "T"),
        ("", "A lean season: the market stalls empty, and bread costs silver.", "M")],
    "a season of plenty": [
        ("", "A season of plenty: work is easy to find, and tables are full."),
        ("R", "A fat season, and the {place} celebrates it loudly."),
        ("B", "Good times: money moves, and {N} watches where it goes.", "EM"),
        ("G", "A generous year: full harvests, full tables, children everywhere."),
        ("B", "Good times: the traders come, and {N} watches who gets the best of them.", "T")],
    "an experience you cannot explain": [
        ("", "Something happens to {N} that they cannot explain, and they tell no one about it."),
        ("U", "Something happens that {N} cannot explain, however hard they try."),
        ("", "A spirit speaks to {N} at the edge of sleep, and they tell no one.", "M"),
        ("G", "Something uncanny follows {N} home from the woods, and stays a while.", "M"),
        ("", "{N} dreams of the dead, and wakes knowing things they should not.", "T")],
    "a sign or prophecy that seems to come true": [
        ("", "Something {elder} once predicted seems to come true, and {N} shivers."),
        ("G", "An old saying of {elder}'s comes true, just as they said it would."),
        ("", "A seer's prophecy about {N} begins, unmistakably, to come true.", "M"),
        ("", "The bones the old ones cast for {N} seem to have told the truth.", "T")],
    "a brush with death": [
        ("", "{N} nearly dies: {brush}. Afterwards everything looks sharper."),
        ("R", "{brush_cap}, and {N} is almost gone. Afterwards they laugh too loudly, for weeks.")],
}
NOTABLE = {"moving somewhere new", "a mentor takes you under their wing", "an illness", "a natural disaster hits where you live",
           "a hard season of scarcity", "a season of plenty", "an experience you cannot explain",
           "a sign or prophecy that seems to come true", "a brush with death", "new friends with a different way of life",
           "an unexpected windfall or loss of money"}
SEVERE = {"moving somewhere new", "an illness", "a natural disaster hits where you live", "a brush with death"}
TOOK = (["It stays with {N}, and leaves them thinking more about {value}.", "Something in it speaks to {N}: {value}.",
         "{N} finds themselves drawn to it: {value}.", "It sets {N} wondering whether {value} matters more than they thought.",
         "{N} can't shake it off. It is all about {value}, and it gets under their skin."],
        ["{N} wants none of it.", "{N} pushes back against it.", "{N} sets their face against it.",
         "{N} shrugs it off, a little too firmly.", "It only makes {N} more sure of their own ways."])

ERA_KIND = dict(policy="New laws and new leaders arrive.", institutions="The great institutions change their ways.",
                cosmology="A new way of seeing the world spreads.")
CLASH_HOW = {"doubled down": "{N} doubles down on it", "reshaped it": "{N} reshapes it to fit who they are now",
             "made peace": "{N} makes peace with it", "left": "{N} walks away from it", "ended otherwise": "it ends on its own"}
# ---- deaths the engine records outside a told scene (Earth batch)
DEATH_LINE = [
    ("", "{dead_cap} dies."),
    ("W", "{dead_cap} dies, and there is a funeral to arrange."),
    ("U", "{dead_cap} dies. {N} keeps turning the news over, looking for the sense in it."),
    ("B", "{dead_cap} dies. {N} feels the gap before they feel the grief."),
    ("R", "{dead_cap} dies, suddenly, and {N} takes it like a blow."),
    ("G", "{dead_cap} dies, as all living things do, and {N} grieves the way the old songs say to."),
]
# R15: a child's death, said plainly and never graphically (the Library's moment "your child dies" tells the scene; this
# line is only for a death the story has not told)
DEATH_CHILD = [
    ("", "{dead_cap} dies, far too young."),
    ("W", "{dead_cap} dies, far too young, and the family holds on to each other."),
    ("U", "{dead_cap} dies, far too young. {N} looks for a reason and there is none."),
    ("B", "{dead_cap} dies, far too young, and something in {N} closes."),
    ("R", "{dead_cap} dies, far too young, and {N} is broken by it."),
    ("G", "{dead_cap} dies, far too young, and {N} grieves with everything they are."),
]
DEATH_FAR = [
    ("", "{dead_cap} dies, at a great age."),
    ("W", "{dead_cap} dies at a great age, and the family gathers for the funeral."),
    ("G", "{dead_cap} dies, full of years, and the family tree loses one of its oldest branches."),
    ("U", "{dead_cap} dies, at a great age. {N} realises how many questions they never asked."),
]

# ---- engine v6 loops told in the story
# tension rebounds (Emren 22:46): an act that joins colors the world reads as opposed either fits or tears
REBOUND_FIT = [
    ("", "Two things {N} was told could not go together just did, and something in them settles."),
    ("W", "*There is a way to keep faith with both. I found it.*"),
    ("U", "*So the contradiction was only a failure of imagination.*"),
    ("B", "*Everyone said I had to choose. I didn't.*"),
    ("R", "*Both! Why did nobody tell me I could have both?*"),
    ("G", "Like two rivers meeting, the two halves of {N} run together for a while."),
]
REBOUND_SPLIT = [
    ("", "Pulled two ways at once, {N} ends up with neither, and feels torn down the middle."),
    ("W", "*I tried to serve two masters. That never ends well.*"),
    ("U", "*The two ideas do not fit. I should have seen that.*"),
    ("B", "*Half measures. I paid twice for them.*"),
    ("R", "The two pulls in {N} fight it out, and both lose."),
    ("G", "*You cannot be two things at once. Not yet, anyway.*"),
]
# after a hard blow: support brings people back to themselves; alone, the change hardens into them
HEALED = [
    ("", "Through the hard months, {close} stays near, and bit by bit {N} comes back to themselves."),
    ("W", "{N}'s people close ranks around them after the blow. Nobody lets them face it alone."),
    ("U", "{close_cap} asks the right questions and listens to the answers. It helps more than {N} expected."),
    ("B", "{N} would never ask for help, but {close} gives it anyway, and {N} lets them."),
    ("R", "{close_cap} turns up with food, noise and no advice, which is exactly what {N} needed."),
    ("G", "The people around {N} gather like a wall against the wind, and slowly {N} mends."),
    ("W", "There are meals left at the door and a rota of visitors. {N} is carried, and lets themselves be carried."),
    ("U", "Long talks with {close} help {N} make sense of it, and a sense they can live with."),
    ("B", "{N} finds out who their real friends are. There are more of them than {N} would have bet."),
    ("R", "{close_cap} drags {N} out of the house, again and again, until one day {N} goes willingly."),
    ("G", "{N} heals the way living things do, slowly, held by the people who were always there."),
]
HARDENED = [
    ("", "{N} carries the hard months alone, and something in them sets harder."),
    ("W", "{N} keeps every duty through the bad months and tells no one how bad they are. It sets into them."),
    ("U", "{N} reasons their way through the blow alone, and comes out colder and more certain."),
    ("B", "*Nobody is coming. Fine. I don't need anyone.* {N} comes out of the year harder."),
    ("R", "{N} rages through the bad months alone, and the anger cools into something hard."),
    ("G", "Like a tree after a storm, {N} grows back around the wound, alone, tougher and more set."),
    ("W", "{N} tells everyone they are fine, and keeps saying it until it hardens into something like the truth."),
    ("U", "{N} files the blow away with the other facts, and nobody is let close enough to see it."),
    ("B", "{N} learns the lesson the hard way, alone: count on yourself. It is not a lesson they will unlearn."),
    ("R", "{N} burns through the bad months on their own, and comes out scorched and stubborn."),
    ("G", "{N} goes to ground like a wounded animal, alone, and comes back warier than before."),
]
# loss and gain spirals: recent trouble brings more trouble, recent fortune more fortune
STREAK_BAD = [
    ("", "Trouble comes in a chain, each blow pulling the next one behind it."),
    ("W", "One hard thing after another. {N} keeps going, because someone has to."),
    ("U", "{N} starts to see the pattern: one trouble making room for the next."),
    ("B", "*When it rains, it pours. Remember who stayed dry.*"),
    ("R", "*Again? Fine. Bring it.*"),
    ("G", "A lean season. The roots will have to hold."),
]
STREAK_GOOD = [
    ("", "Good fortune seems to breed more of it."),
    ("W", "A blessed stretch. {N} tries not to take any of it for granted."),
    ("U", "Things keep working out, and {N} wonders, a little warily, why."),
    ("B", "*Everything I touch is working. Push while it lasts.*"),
    ("R", "A lucky streak, and {N} rides it with both hands."),
    ("G", "A rich season. {N} gathers what it brings and shares it round."),
]

RITE = {
    "juvenile": ["Somewhere around here, after {what}, {N} stops being a child.", "After {what}, {N} is not quite a child any more."],
    "young_adult": ["After {what}, {N} steps into adulthood.", "{what_cap} marks the end of {Ns} youth."],
    "adult": ["After {what}, {N} settles into full adulthood.", "{what_cap} leaves {N} a grown person, settled in themselves."],
    "mature": ["After {what}, {N} enters the middle of life.", "{what_cap} marks the start of {Ns} middle years."],
    "elder": ["After {what}, {N} enters old age.", "{what_cap} makes {N}, quite suddenly, old."],
}
RITE_QUIET = dict(juvenile="{N} is not a child any more, though nobody marks the day.", young_adult="{N} grows quietly into adulthood.",
                  adult="{N} settles quietly into adulthood.", mature="Middle age arrives quietly.", elder="Old age arrives quietly.")
SNOUN = {"playground dispute": "a fight among the children", "hard school task": "a hard lesson",
         "family rule you dislike": "a quarrel over a family rule", "peer pressure to take a risk": "a dare",
         "choosing a path": "choosing a path in life", "witnessing an injustice": "witnessing an injustice",
         "conflict at work": "a fight at work", "relationship strain": "a hard time with someone close",
         "money: windfall or squeeze": "a turn in their money", "community problem": "trouble in the community",
         "tempting shortcut": "a tempting shortcut", "raising a child": "a hard stretch with their child",
         "chance to innovate": "a chance to make something new", "crisis or disaster": "a disaster",
         "bereavement": "a death in the family", "thinking about legacy": "thinking about their legacy",
         "meeting someone": "meeting someone", "deciding about children": "deciding about children",
         "a search for meaning": "a search for meaning", "your group must decide how to act": "a hard call in their group",
         "something is wrong where you live": "trouble where they live", "a crossroads in how you live": "a crossroads",
         "reconsidering a commitment": "second thoughts", "an ordinary week": "an ordinary week"}
KINDREF = dict(career="their work", children="family life", community="the community", faith="their faith")
CAREER = {
    "earth": {"found new work": "a new job", "serve the community": "a job serving the {place}", "pursue a rigorous field": "a demanding apprenticeship in a rigorous field",
              "chase money and status": "a job that pays well and promises more", "follow your passion": "work that follows their passion",
              "continue the family craft": "the family craft", "join an institution's ranks": "a post in an institution's ranks",
              "build something wild and new": "a venture of their own"},
    "tribal": {"serve the community": "a place among those who serve the clan", "pursue a rigorous field": "the healer's craft",
               "chase money and status": "trading between the clans", "follow your passion": "the life of a wandering singer",
               "continue the family craft": "the family craft", "join an institution's ranks": "a place in the chief's circle",
               "build something wild and new": "a new way of hunting that nobody has tried"},
    "magic": {"serve the community": "service with the town wardens", "pursue a rigorous field": "an apprenticeship in the arcane archives",
              "chase money and status": "a place in the merchant guilds", "follow your passion": "the life of a travelling bard",
              "continue the family craft": "the family craft", "join an institution's ranks": "a post in the Order's ranks",
              "build something wild and new": "an alchemist's venture of their own"},
}
EPITAPH = dict(W="kept their word", U="never stopped asking why", B="made their own way, on their own terms",
               R="lived every day as if it mattered", G="kept faith with their people and the turning seasons")

# labels that read badly once spoken about the character
ACT_FIX = {"refuse, it breaks the rules": "refuse, because it breaks the rules",
           "refuse, it is not our way": "refuse, since it is not their way",
           "accept death, keep what remains useful": "accept death and keep what remains useful",
           "ignore the adults and do it our way": "ignore the adults and do it their own way",
           "accept it as how our family is": "accept it as the way their family is",
           "raise them in our traditions": "raise the child in the family's traditions",
           "let them adapt and find their nature": "let the child adapt and find their own nature",
           "push them to compete": "push the child to compete", "let them roam free": "let the child roam free",
           "set firm rules": "set firm rules for the child",
           "fight off whoever threatens you": "fight off whoever threatens them",
           "give yourself to a cause that sets your heart on fire": "give themselves to a cause that sets their heart on fire",
           "have children as expected of you": "have children, as expected of them",
           "take it": "take the shortcut", "take it for the rush": "take the shortcut for the rush",
           "reshape it toward who you want to be": "reshape it toward who they want to be",
           "live fully while you can": "live fully while they can",
           "have them to carry on your name": "have children to carry on their name", "choose someone who thinks like you": "choose someone who thinks like them"}


# ---- story fields written by the Library (modern Earth batch, approved by Emren 2026-10-05 05:11): scenes per world
# with one variant per color (child/older as k/a), two works and two fails lines, and the act as the narrator says it.
# Filled by load_library_story() from whatever library the pinned engine compiles; the game's own lines above stay as
# the fallback for situations, worlds or stages the Library has not written yet.
LIB_SCENES, LIB_OUTCOMES, LIB_ACTS, LIB_READ = {}, {}, {}, {}
LIB_GRIEF = set()          # moments in which someone dies (kills:)
LIB_ECHO = {}              # echo -> the mark it answers ("a promise you broke comes back" -> "broke your word")
WCODE = dict(earth="E", tribal="T", magic="M")
PERSON_SLOTS = ("friend", "rival", "partner", "prospect", "sibling", "colleague", "boss", "mentor", "parent", "child",
                "grandparent", "elder")


def load_library_story(situations, read_events=()):
    """Take the Library's story fields from its situation dicts (and its read outside events, when given).
    Called once per life: an empty call clears them (settings the Library has not written use the game's own lines)."""
    for d in (LIB_SCENES, LIB_OUTCOMES, LIB_ACTS, LIB_READ, LIB_ECHO):
        d.clear()
    LIB_GRIEF.clear()

    def pool(scenes):
        out = []
        for world, lst in scenes.items():
            for e in lst:
                code = (e[2] if len(e) > 2 else "") + WCODE.get(world, "")
                out.append((e[0], e[1], code))
        return out
    for x in situations:
        if x.get("scenes"):
            LIB_SCENES[x["name"]] = pool(x["scenes"])
        if x.get("outcomes"):
            LIB_OUTCOMES[x["name"]] = (list(x["outcomes"][0]), list(x["outcomes"][1]))
        if x.get("kills"):
            LIB_GRIEF.add(x["name"])
        mk = re.search(r"mark '([^']+)'", str(x.get("after", ""))) if x.get("tier") == "echo" else None
        if mk:
            LIB_ECHO[x["name"]] = mk.group(1)
        for o in x.get("options", ()):
            if len(o) > 5 and isinstance(o[5], dict) and o[5].get("act"):
                LIB_ACTS[o[0]] = o[5]["act"]
    for x in read_events:
        LIB_READ[x["name"]] = dict(scenes=pool(x.get("scenes", {})), readings=list(x.get("readings", ())))
    return len(LIB_SCENES)


def act(label):
    """An option label as something the character does: 'put your own needs first' -> 'put their own needs first'."""
    if label in LIB_ACTS:                       # the Library already wrote it in the third person
        return LIB_ACTS[label]
    s = ACT_FIX.get(label, label)
    s = re.sub(r"\byourself\b", "themselves", s)
    s = re.sub(r"\bwho you want\b", "who they want", s)
    s = re.sub(r"\b(of|for|to|with|like|at|on|about) you\b", r"\1 them", s)     # 'you' as an object
    s = re.sub(r"\byou\b(?=\s*[.,;:!?]|\s*$)", "them", s)
    s = re.sub(r"\byou\b", "they", s)
    s = re.sub(r"\byour\b", "their", s)
    return s


def chooses(a):
    """'choose someone who ...' -> 'someone who ...'; anything else -> 'to ...'."""
    return a[7:] if a.startswith("choose ") else "to " + a


def chooses_mk(a, payload, kind="a"):
    """chooses(), with the act itself marked for the browser."""
    return mk(kind, payload, a[7:]) if a.startswith("choose ") else "to " + mk(kind, payload, a)


# titles and perks (game.py: Emren 12:05). A status the engine gives, told in a line of its own: (template, the marked
# words); <o> is the hoverable title. Others: "{N} is <say> now." STATUS_WORD: how a status reads after "is no longer".
STATUS_LINE = {"graduate": ("{N} <o>.", "graduates"), "veteran": ("{N} comes home <o>.", "a veteran"),
               "widowed": ("{N} is <o>.", "widowed"), "homeowner": ("{N} <o> now.", "owns a home"),
               "newcomer": ("{N} is <o>.", "new in town"), "out of work": ("A year on, {N} is still <o>.", "out of work"),
               "homeless": ("{N} has <o>.", "nowhere to live"), "ex-prisoner": ("{N} is <o> now.", "out of prison"),
               "someone with a record": ("{N} has <o> now.", "a record"), "eldest child": ("{N} is <o>.", "the eldest"),
               "has killed in war": ("{N} <o>.", "has killed in war"), "carer for a parent": ("{N} becomes <o> for a parent.", "a carer"),
               "left the faith": ("{N} has <o>.", "left the faith they grew up in"), "retiree": ("{N} is <o> now.", "retired"),
               "doctoral graduate": ("{N} <o>.", "earns a doctorate"), "adopted person": ("{N} is <o>.", "adopted"),
               "bankruptcy or insolvency in their history": ("{N} is declared <o>.", "bankrupt"),
               "on probation or community supervision": ("{N} is <o>.", "on probation"),
               "living in residential care": ("{N} moves into <o>.", "a care home"),
               "returned migrant": ("{N} is <o>.", "back home after years abroad"),
               "displaced by a disaster": ("{N} is <o>.", "displaced by a disaster")}
# titles of the faith place that are causes, not a faith (earth_perks_titles.py, kind faith)
CAUSES = {"activist in a cause", "party member", "animal-shelter campaigner", "disability-rights organiser", "civil-liberties campaigner",
          "restorative-justice advocate", "digital-rights advocate"}
# the engine's own reasons for a loss (its rules' words), told before the line: "With the money gone, Ari no longer has a car."
LOSS_LEAD = {"financial ruin": "With the money gone, ", "missed payments": "After missed payments, ",
             "no money to keep it": "With no money to keep it, ", "spent while out of work": "Out of work, ",
             "spent in hard times": "In hard times, ",
             "the doctor says to stop driving": "On the doctor's advice, ", "a partner at home": "With a partner at home now, ",
             "the children grown": "With the children grown, "}
STATUS_WORD = {"widowed": "widowed", "left the faith": "outside the faith they grew up in", "newcomer": "new in town",
               "homeowner": "a homeowner", "carer for a parent": "caring for a parent"}


def neg_of(pred):
    """'can swim' -> 'can no longer swim'; 'is a landlord' -> 'is no longer a landlord'; 'has a car' -> 'no longer has a car'."""
    pred = pred[len("always "):] if pred.startswith("always ") else pred
    for lead in ("can ", "is "):
        if pred.startswith(lead):
            return lead + "no longer " + pred[len(lead):]
    return "no longer " + pred


def an(word):
    """'a' or 'an' by the sound: an hour, a university, a one-off, an honest man."""
    w = word.lower()
    vowel = w[:1] in "aeiou" and not re.match(r"(uni|use|usu|uti|eu|one\b|once)", w) or re.match(r"(hour|honest|honou?r|heir)", w)
    return ("an " if vowel else "a ") + word


def cap(s):
    """Capitalise the first letter of each sentence (looking past the browser's text markers)."""
    return re.sub(r"(^|[.!?]\s+|[.!?]” )((?:⟦[^⟧]*⟧)*)([a-z])", lambda m: m.group(1) + m.group(2) + m.group(3).upper(), s)


# Interactive text for the browser (Emren 2026-10-05 08:02: the story is the main text, and hovering its flavorful parts shows
# the mechanics behind them): ⟦kind:payload⟧text⟦/⟧. Markers can nest. The terminal shows plain() text.
#   p person (id)        a act (means>ends colors)     w act they wanted (gate)    t thought (color|kind)
#   v value (color)      m mood (content|peace)        d better/worse (change)     s voice shift (old|new)
#   k the year's weeks (color|W,U,B,R,G counts)        f frictions (count)         x how news landed (took|colors)
#   e an era's idea (kind)  r a reading of news (reading|impact)  c a title (kind|expects|what)  b rebound (fit|tear)
#   h after a blow (healed|wound|support)  q a streak (trouble|level)  T temperament (moved keys)  R a rite (stage)
#   B a breakthrough (color)  C a lost faith (old|new)
#   i the inner voice (key|heart driver|head driver|self-control)  j an aside (key)  g a dream, passion or plan
#   (kind|what|colors|domain|source|horizon)  z a change (what|delta|size)  y closer to (identity|guild|distance)
#   n a lesson (key)  o a title or perk (name|kind|ways|title 1 or 0|points it adds|state)
MARK = re.compile(r"⟦[^⟧]*⟧")


def mk(kind, payload, text):
    return f"⟦{kind}:{payload}⟧{text}⟦/⟧" if text else text


def plain(s):
    return MARK.sub("", s) if s and "⟦" in s else s


def phase(age):
    """The phase of life the text is written for: 0 under 12, 1 under 18, 2 under 30, 3 under 50, 4 under 70, 5 older."""
    return 0 if age < 12 else 1 if age < 18 else 2 if age < 30 else 3 if age < 50 else 4 if age < 70 else 5


def weights_of(letters):
    v = np.zeros(5)
    for c in letters:
        if c in CI:
            v[CI[c]] = 1.0
    return v if v.sum() else np.full(5, 0.2)


class Story:
    def __init__(self, name, seed, place="town", setting="earth"):
        self.name = name
        self.rng = np.random.default_rng(int(seed) + 4243)
        self.seed = int(seed)
        self.place = place
        self.setting = setting if setting in WORLD else "earth"
        self.W = WORLD[self.setting]
        self.wcode = SETTINGS[self.setting]["code"]
        self.mem = np.full(5, 0.2)          # memory of past identities
        self.voice = np.full(5, 0.2)        # the narrator's emphasis: present identity blended with the memory
        self._voice_top = None
        self._values_told = (None, -99)
        self._recent = deque(maxlen=60)
        self.people = []                    # dict(name, role, ref, alive, introduced)
        self.dreams = {}                    # goal id -> the Library dream the engine named it by (dream_info)
        self.dreams_held = {}               # goal id -> name, for the dreams held now (a new spark can feed one already held)
        self._used = set()                  # names given so far (no two people share one until the lists run out)
        self.partner_sex = None             # "f" or "m" once the engine says who the partner is (partner_same); else either
        self._moment = {}                   # week -> dict(sit, slots, scene)
        self.year = dict(weeks=np.zeros(5), frictions=0)
        self._last_c = None
        self._weeks_told = (None, -99)
        self._disaster = None
        self._dead = []                     # who has died, in order (a {dead} outside a death scene is the latest)
        self._moved_at = None               # age of the last move
        self.marks = {}                     # mark -> the person the marked act involved (for echoes)
        self._told_dead = set()             # names of those whose death a told scene already showed
        self._broke = None
        self._shift_age = -99
        self.age = 0.0                      # set by the game every week (when people are first met)
        self.last_tag = ""                  # color tag of the variant pick() drew last
        self.last_weeks = [0.0] * 5         # where the ordinary weeks of the last chapter's year went
        # the family the character is born into
        self.new("mother", "their mother {n}")
        self.new("father", "their father {n}")
        self.new("grandparent", "their grandmother {n}")
        if self.rng.random() < 0.7:
            self.new("grandparent", "their grandfather {n}")
        if self.rng.random() < 0.6:
            self.new("sibling", "their " + ("older" if self.rng.random() < 0.5 else "younger") + " sibling {n}")

    # ---------------------------------------------------------------- cast
    def _name(self, sex=None):
        """A name nobody in the story has yet: from the feminine, masculine or either list (sex "f", "m", "x"), else any."""
        pool = NAME_POOL.get(sex, NAMES)
        free = [n for n in pool if n not in self._used and n != self.name]
        if not free:
            self._used = set(); free = [n for n in pool if n != self.name]
        n = free[int(self.rng.integers(len(free)))]
        self._used.add(n)
        return n

    def new(self, role, ref, sex=None):
        if sex is None:
            r_ = ref.split("{n}")[0] + " " + role
            sex = ("f" if FEM_REF.search(r_) else "m" if MAS_REF.search(r_) else
                   (self.partner_sex or "x") if role in ("partner", "prospect", "companion", "former partner") else None)
        n = self._name(sex)
        p = dict(id=len(self.people), name=n, role=role, ref=ref.format(n=n), alive=True, introduced=False, met=None, seen=0,
                 made=getattr(self, "age", 0))
        self.people.append(p)
        return p

    def alive(self, role):
        return [p for p in self.people if p["role"] == role and p["alive"]]

    def get(self, role, ref=None):
        ps = self.alive(role)
        if ps:
            return ps[int(self.rng.integers(len(ps)))]
        return self.new(role, ref or ("their " + role + " {n}"))

    def say(self, p):
        """A person as the story names them: with who they are the first time, by name afterwards."""
        if p is None:
            return "someone"
        p["seen"] += 1
        if p["introduced"]:
            return mk("p", p["id"], p["name"])
        p["introduced"] = True; p["met"] = round(self.age, 1)
        return mk("p", p["id"], p["ref"])

    def nm(self, p):
        """A person already known, by name (marked for the browser)."""
        if p.get("met") is None:
            p["met"] = round(self.age, 1)
        p["introduced"] = True
        return mk("p", p["id"], p["name"])

    def role(self, slot, stage, ctx):
        """Fill a role slot with a person (created when the story first needs them)."""
        if "_p_" + slot in ctx:
            return self.say(ctx["_p_" + slot])
        if slot in ctx:
            return ctx[slot]
        p = None
        if slot == "parent":
            ps = self.alive("mother") + self.alive("father")
            p = ps[int(self.rng.integers(len(ps)))] if ps else self.get("aunt", "their aunt {n}")
        elif slot == "grandparent":
            ps = self.alive("grandparent")
            p = ps[0] if ps else None
            if p is None:
                ctx[slot] = "their late grandparents"
                return ctx[slot]
        elif slot == "elder":
            ps = self.alive("grandparent") or self.alive("mother") + self.alive("father") or self.alive("mentor")
            p = ps[0] if ps else self.get("old neighbour", "their old neighbour {n}")
        elif slot == "sibling":
            p = self.get("sibling") if self.alive("sibling") else self.get("cousin", "their cousin {n}")
        elif slot == "partner":
            p = self.get("partner") if self.alive("partner") else self.get("companion", "their companion {n}")
        elif slot == "friend":
            p = self.get("friend", "their friend {n}")
        elif slot == "friend2":
            fs = self.alive("friend")
            p = fs[1] if len(fs) > 1 else self.new("friend", "their friend {n}")
        elif slot == "newfriend":
            p = self.new("friend", "someone called {n}")
        elif slot == "rival":
            p = self.get("rival", self.W["classmate"] if stage <= 1 else "their rival {n}")
        elif slot == "mentor":
            p = self.new("mentor", (self.W["teacher"] if stage <= 1 else self.W["elder_mentor"]))
        elif slot == "teacher":
            p = self.get("teacher", self.W["teacher"])
        elif slot == "boss":
            p = self.get("boss", self.W["boss"])
        elif slot == "colleague":
            p = self.get("colleague", self.W["colleague"])
        elif slot == "child":
            p = self.get("child", "their child {n}")
        elif slot == "prospect":
            p = self.new("prospect", "someone called {n}")
        elif slot == "close":
            ps = self.alive("partner") or self.alive("friend") or self.alive("sibling")
            p = ps[0] if ps else self.get("friend", "their friend {n}")
        elif slot == "carer":
            ps = self.alive("partner") or self.alive("mother") + self.alive("father") or self.alive("child") or self.alive("friend")
            p = ps[0] if ps else self.get("neighbour", "their neighbour {n}")
        elif slot == "dead":
            if ctx.get("_dying"):                       # a death scene: someone alive is about to die
                p = self._who_dies(ctx.get("_age", 30), ctx["_dying"])
            elif self._dead:                            # otherwise the dead are those already gone
                p = self._dead[-1]
            else:
                p = self.new("late relative", "their late " + ("aunt" if self.rng.random() < 0.5 else "uncle") + " {n}")
                self.dies(p)
        elif slot == "disaster":
            age = ctx.get("_age", 0)
            if self._disaster is None or age - self._disaster[1] > 1.0:       # the same disaster, if one struck lately
                ds = self.W["disasters"]
                self._disaster = (ds[int(self.rng.integers(len(ds)))], age)
            ctx[slot] = self._disaster[0]
            return ctx[slot]
        elif slot == "brush":
            ctx[slot] = self.W["brushes"][int(self.rng.integers(len(self.W["brushes"])))]
            return ctx[slot]
        if p is None:
            ctx[slot] = "someone"
            return ctx[slot]
        ctx["_p_" + slot] = p
        ctx[slot] = self.say(p)
        return ctx[slot]

    def dies(self, p):
        if p is not None and p["alive"]:
            p["alive"] = False
            self._dead.append(p)

    def _who_dies(self, age, kills="anyone"):
        """Someone close dies. A library event can name the role (kills: parent, sibling, ...); otherwise
        grandparents first, then parents, later friends and siblings."""
        roles = KILLS.get(kills, ())
        named = [p for r in roles for p in self.alive(r)]
        if named:
            return named[0] if kills == "grandparent" else named[int(self.rng.integers(len(named)))]
        if kills in NEW_KIN:                        # the engine knows this person exists; the story meets them now
            return self.new(*NEW_KIN[kills])
        cands = []
        for p in self.people:
            if not p["alive"]:
                continue
            w = {"grandparent": 1.0 + age / 30, "mother": max(0.0, (age - 18) / 25), "father": max(0.0, (age - 18) / 25),
                 "sibling": max(0.0, (age - 45) / 60), "friend": max(0.0, (age - 40) / 80), "mentor": max(0.0, (age - 25) / 60),
                 "aunt": 0.3, "old neighbour": 0.3}.get(p["role"], 0.0)
            if w > 0:
                cands.append((w, p))
        cands.append((0.15, None))
        ws = np.array([w for w, _ in cands]); i = int(self.rng.choice(len(cands), p=ws / ws.sum()))
        p = cands[i][1]
        if p is None:
            p = self.new("old neighbour", "their old neighbour {n}" if age >= 25 else "their neighbour {n}")
        return p

    # ---------------------------------------------------------------- telling
    def pick(self, pool, stage=None, v=None):
        """One variant from a pool of (colors, text[, stages]), drawn by the voice (or by v)."""
        v = self.voice if v is None else v
        cands = []
        for e in pool:
            if isinstance(e, str):
                e = ("", e)
            if len(e) > 2:
                st = [c for c in e[2] if c.islower()]; wl = [c for c in e[2] if c.isupper()]
                if wl and self.wcode not in wl:
                    continue
                if st and stage is not None and not any(stage in STAGESETS[c] for c in st):
                    continue
            tag = e[0]
            w = float(np.mean([v[CI[c]] for c in tag])) if tag else 0.12
            cands.append((max(w, 1e-3) ** SHARP, e[1], tag))
        if not cands:
            self.last_tag = ""
            return ""
        fresh = [c for c in cands if c[1] not in self._recent] or cands
        ws = np.array([c[0] for c in fresh])
        _, text, self.last_tag = fresh[int(self.rng.choice(len(fresh), p=ws / ws.sum()))]
        self._recent.append(text)
        return text

    def fill(self, text, stage=0, ctx=None):
        ctx = {} if ctx is None else ctx
        def one(m):
            out = _one(m)
            if m.group(2):
                out = re.sub(r"^((?:⟦[^⟧]*⟧)*)someone called ", r"\1", out)
            return out + (m.group(2) or "")

        def _one(m):
            k = m.group(1)
            if k == "N":
                return self.name
            if k == "Ns":
                return self.name + "'s"
            if k == "place":                     # the town, or the place a moment is about (v22.4's caught, odd, lead)
                return str(ctx["place"]) if "place" in ctx else self.place
            if k == "seen_as":                   # N1d: girl or boy, young woman or young man, woman or man, as their world sees them
                f_ = getattr(self, "seen_as", None)
                return f_() if callable(f_) else "person"
            if k == "title":                     # the Library's {title}: the title that brought them here (engine next hand-off)
                return getattr(self, "title_now", None) or "their role"
            if "_p_" + k in ctx:
                return self.say(ctx["_p_" + k])
            if k in ctx:
                return str(ctx[k])
            if k.endswith("_cap"):
                return cap(self.role(k[:-4], stage, ctx))
            return self.role(k, stage, ctx)
        out = re.sub(r"\{(\w+)\}('s)?", one, text)
        # a {title} inside a filled-in act (an option's label in "{N} chooses {c}") is the held title too
        return cap(out.replace("{title}", getattr(self, "title_now", None) or "their role"))

    def thought(self, text, kind="", tag=None):
        """An italic thought; its color is the variant's (the voice's, or the act's for a reason)."""
        return mk("t", f"{self.last_tag if tag is None else tag}|{kind}", f"*{text}*")

    def val(self, c):
        """What a color values, in words (marked for the browser)."""
        return mk("v", c, VALUE[c])

    # ---------------------------------------------------------------- the voice
    def update_voice(self, w):
        """Once a year: the memory of past identities takes in the present one, slowly."""
        w = np.asarray(w, float)
        a = 1 - np.exp(-1 / MEMORY_YEARS)
        self.mem = (1 - a) * self.mem + a * w
        self.voice = NOW_SHARE * w + (1 - NOW_SHARE) * self.mem

    def leading(self, v=None, n=2, thr=0.215):
        v = self.voice if v is None else v
        order = [COLORS[i] for i in np.argsort(-v)]
        return [c for c in order[:n] if v[CI[c]] >= thr] or order[:1]

    # ---------------------------------------------------------------- birth
    def birth(self, blurb=""):
        ctx = {}
        fam = [self.say(p) for p in self.alive("mother") + self.alive("father")]
        g = self.alive("grandparent"); s = self.alive("sibling")
        L = [f"{self.name} is born in {self.birth_place or 'a ' + self.place}. " + (blurb + " " if blurb else "")
             + f"The family: {fam[0]} and {fam[1]}"
             + (", " + " and ".join(self.say(p) for p in g) if g else "")
             + (", and " + " and ".join(self.say(x) for x in s) if s else "") + "."]
        return cap(" ".join(L))

    # ---------------------------------------------------------------- moments
    def moment(self, t, sit, stage, age, kind=None, kills=None):
        """The scene of this week's situation, built once (a checkpoint and its outcome share it).
        kills: the role who dies in it (the library's kills: field); a bereavement without one takes anyone close."""
        m = self._moment.get(t)
        if m is not None and m["sit"] == sit:
            return m
        ph = phase(age)
        ctx = dict(_age=age)
        if kills or sit == "bereavement":
            ctx["_dying"] = kills or "anyone"
            if kills:
                p = self._who_dies(age, kills)
                ctx["_p_dead"] = p; ctx["_p_" + kills] = p
        if kind:
            ctx["kind"] = kind
            ps = self.alive("partner")
            ctx["kindref"] = (f"their life with {ps[0]['name']}" if ps else "their relationship") if kind == "partner" else KINDREF.get(kind, "their " + kind)
        tpl = self.pick(LIB_SCENES[sit], ph) if sit in LIB_SCENES else ""
        if not tpl and sit in SCENES:
            tpl = self.pick(SCENES[sit], ph)
        if not tpl and sit in LIB_SCENES:           # a Library moment not yet written for this world
            tpl = cap(act(sit)) + "."
        who = self.marks.get(LIB_ECHO.get(sit))
        if who is not None and who["alive"]:        # an echo: the same person as in the act it answers
            slot = next((x for x in re.findall(r"\{(\w+)\}", tpl) if x in PERSON_SLOTS), None)
            if slot:
                ctx["_p_" + slot] = who
        m = dict(sit=sit, ctx=ctx, tpl=tpl, text=None, stage=ph, age=age)
        self._moment = {t: m}
        return m

    def scene(self, m):
        """The scene's text, filled the first time it is told (people are introduced only when the player meets them)."""
        if m["text"] is None:
            m["text"] = self.fill(m["tpl"], m["stage"], m["ctx"]) if m["tpl"] else ""
            if m["sit"] == "a close friend moves away":
                if "_p_friend" not in m["ctx"]:         # the scene did not name them; the outcome may
                    m["ctx"]["_p_friend"] = self.get("friend", "their friend {n}")
                self.far(m["ctx"]["_p_friend"])
            elif m["sit"] == "the family moves to a new town":
                self.left_behind()
        return m["text"]

    def far(self, p):
        """Someone moves away: still alive and remembered by name, but no longer the one down the street."""
        if p is not None and p["alive"] and not p["role"].startswith("old "):
            p["role"] = "old " + p["role"]

    def left_behind(self):
        """A move: friends, rivals, teachers and neighbours stay in the old place; new ones come with the new one."""
        for p in self.people:
            if p["role"] in LEFT_BEHIND:
                self.far(p)

    def slots_in(self, text, m):
        """v22.4's moments (game.py _social_slots marks them): the slots in an option's label or act ({friend}, {place_a},
        {offer}...) as the moment's scene fills them, in plain words and lower case as written."""
        if not text or "{" not in text or not m:
            return text
        out = plain(self.fill(text, m["stage"], m["ctx"]))
        return out[:1].lower() + out[1:] if text[:1].islower() else out

    def act_in(self, m, label):
        """An option label as the character's act in this moment ('reshape it ...' names what is reshaped)."""
        a = act(label)
        if m and m["ctx"].get("_social"):
            a = self.slots_in(a, m)
        ref = m["ctx"].get("kindref") if m else None
        if ref:
            a = "walk away from " + ref if a == "walk away" else re.sub(r"\bit\b", ref, a)
        return a

    def recon_note(self, kind, years, asks, wants):
        """How long a commitment has been held, what it asks and what they want now, in words."""
        n = "a year" if years < 1.5 else f"{years:.0f} years"
        ps = self.alive("partner")
        held = dict(career="{N} has done this work for {n}.", partner="{N} has been with {p} for {n}.",
                    children="{N} has been raising a family for {n}.", community="{N} has belonged to the community for {n}.",
                    faith="{N} has kept the faith for {n}.").get(kind, "{N} has held their " + kind + " for {n}.")
        line = self.fill(held, ctx=dict(n=n, p=self.nm(ps[0]) if ps else "their partner"))
        if asks == wants:
            return line + " It still fits who they are, mostly; yet something nags."
        return line + f" It asks them to be {asks}; lately they want to be {wants}."

    def reason(self, colors):
        """Why they lean toward an act, in their own words: the act's colors speak."""
        return self.thought(self.pick([(c, x) for c in REASON for x in REASON[c]], v=weights_of(colors)), "reason")

    def confidence(self, felt):
        n = self.name
        return (f"{n} feels sure of it." if felt > 0.7 else f"{n} thinks it could work." if felt > 0.45 else
                f"{n} is not sure it will work." if felt > 0.25 else f"{n} doubts it will work at all.")

    def _result(self, m, ev):
        sit = m["sit"]; succ = bool(ev["success"]); d = float(ev.get("delta", 0.0))
        lines = (LIB_OUTCOMES.get(sit) or OUTCOMES.get(sit) or (["It works."], ["It goes badly."]))[0 if succ else 1]
        out = self.fill(lines[int(self.rng.integers(len(lines)))], m["stage"], m["ctx"])
        if succ and d > 0.6:
            out += " " + self.fill(self.pick(BIG_WIN_SOFT if sit in SOMBER or sit in LIB_GRIEF else BIG_WIN))
        elif not succ and d < -1.0:
            out += " " + self.fill(self.pick(BIG_LOSS))
        return out

    def react(self, succ, sit=None):
        src = REACT_GRIEF if sit == "bereavement" or sit in LIB_GRIEF else REACT
        pool = [(c, x) for c in src for x in src[c][0 if succ else 1]]
        return self.thought(self.pick(pool), "react")

    def outcome(self, m, ev, chosen_label, pushed, rel, closed, colors=""):
        """A checkpoint resolved: what they did, how it went, and how they read it."""
        a = self.act_in(m, chosen_label)
        if not pushed:
            first = self.fill(self.pick(["{N} chooses {c}.", "So {N} chooses {c}.", "In the end, {N} chooses {c}."]),
                              ctx=dict(c=chooses_mk(a, colors)))
        else:
            if closed:
                inner = self.pick(OUT_OF_REACH)
            elif rel < 0.3:
                inner = self.pick(RELUCT_LOW)
            else:
                inner = self.pick([(c, x) for c in RELUCT for x in RELUCT[c]])
            first = self.fill("You push, and {N} goes along: they {a}. ", ctx=dict(a=mk("a", colors, a))) + self.thought(inner, "reluct")
        L = [first, self._result(m, ev) + " " + self.react(ev["success"], m["sit"])]
        if pushed and rel >= 0.3:
            L.append(self.fill("It costs {N}: strain, and a wanting they swallow for now."))
        if pushed and closed and not ev["success"]:
            L.append("Forcing what was out of reach backfires: more stress, and money lost.")
        return "\n".join(L)

    def set_family(self, siblings, grandparents):
        """Match the family to the engine's (the Earth batch draws siblings and grandparents per person)."""
        for role, n, refs in (("sibling", siblings, None), ("grandparent", grandparents,
                              ["their grandmother {n}", "their grandfather {n}", "their other grandmother {n}", "their other grandfather {n}"])):
            have = self.alive(role)
            for p in have[n:]:
                self.people.remove(p)
            for i in range(len(have), n):
                ref = refs[i] if refs else "their " + ("older" if self.rng.random() < 0.5 else "younger") + " sibling {n}"
                self.new(role, ref)

    def death(self, d, m, age, alone=False):
        """The engine's record of a death (Earth batch). Returns a line, or None when a told scene already showed it.
        alone: a partner's death with no widowed commitment this week (with the world on it can come without one)."""
        role = d["role"]
        p = m["ctx"].get("_p_dead") if m is not None and m["ctx"].get("_dying") == role else None
        if p is None or not p["alive"]:
            p = self._who_dies(age, role)
        told = m is not None and m["text"] is not None and m["ctx"].get("_p_dead") is p
        self.dies(p)
        if told:
            self._told_dead.add(p["name"])
            return None
        if role == "partner" and not alone:         # the partnership's end tells it (commitment: widowed)
            return None
        if role == "partner":
            self._told_dead.add(p["name"])
        lines = DEATH_CHILD if role == "child" else DEATH_LINE
        return self.fill(self.pick(lines, phase(age)), phase(age), dict(_p_dead=p, _age=age))

    def settle(self, c):
        """A commitment's end that a moment already told: the people change as the line would have changed them."""
        kind, what = c["kind"], c["what"]
        if kind == "partner" and what in ("left", "broke up"):
            for q in self.alive("partner"):
                q["role"] = "ex"
        elif kind == "career" and what in ("left", "lost job"):
            for b in self.alive("boss"):
                b["role"] = "former boss"
        elif what == "widowed":
            ps = self.alive("partner")
            if ps:
                self.dies(ps[0])

    birth_place = None      # the outer world's birthplace, in words (set by the game when the world is on)

    def world_siblings(self, sexes):
        """With the outer world on, the siblings at the birth are the world's: older ones, in the world's sexes."""
        for p, sx in zip(self.alive("sibling"), list(sexes) + [None] * len(self.alive("sibling"))):
            if sx is not None:
                self._used.discard(p["name"]); p["name"] = self._name(sx)
            p["ref"] = "their older " + {"f": "sister", "m": "brother"}.get(sx, "sibling") + " " + p["name"]

    def new_kin(self, role, n, sexes=(), told=True):
        """The engine's family grew (with the outer world on, younger siblings are born into it): add the newcomers, in
        the world's sexes when known. Returns the line, or None when they were there all along (told False)."""
        out = []
        for i in range(n):
            sx = sexes[i] if i < len(sexes) else None
            word = {"f": "sister", "m": "brother"}.get(sx, "sibling")
            p = self.new(role, ("their younger " if told else "their older ") + word + " {n}", sex=sx)
            out.append(p)
        if not told or not out:
            return None
        if len(out) == 1:
            w_ = {"f": "sister", "m": "brother"}.get(sexes[0] if sexes else None, "sibling")
            return self.fill("{N} has a new baby " + w_ + ": " + self.nm(out[0]) + ".")
        return self.fill("New babies in the family: " + " and ".join(self.nm(p) for p in out) + ".")

    def later_child(self):
        """One more child (R15: a later child born or taken in while there are children already): a line."""
        ch = self.new("child", "a child, {n}"); ch["born"] = True
        line = self.fill("Another child is born to {N}: " + self.nm(ch) + ".")
        ch["ref"] = "their child " + ch["name"]
        return line

    def quiet_deaths(self, role, left, age):
        """Grandparents of grown-up grandchildren die outside the Library's moments: say so briefly."""
        out = []
        for p in self.alive(role)[left:] if left < len(self.alive(role)) else []:
            self.dies(p)
            out.append(self.fill(self.pick(DEATH_FAR), phase(age), dict(_p_dead=p, _age=age)))
        return " ".join(out) or None

    def mark(self, mk, m):
        """An act left a mark: remember who was in the scene, so an echo can bring them back."""
        if m is None:
            return
        for slot in PERSON_SLOTS:
            p = m["ctx"].get("_p_" + slot)
            if p is not None:
                self.marks[mk] = p
                return

    def read(self, r, stage):
        """An outside event read through the character's colors (Earth batch): the scene and how they take it."""
        ev = LIB_READ.get(r["name"])
        scene = self.fill(r["_scene"], phase(r["age"]), dict(_age=r["age"])) if r.get("_scene") else \
            self.fill(self.pick(ev["scenes"], phase(r["age"])), phase(r["age"]), dict(_age=r["age"])) if ev and ev["scenes"] else ""
        say = self.fill(r["say"], phase(r["age"]), dict(_age=r["age"])) if r.get("say") else \
            self.fill("{N} takes it as " + r["reading"] + ".")
        return (scene + " " + mk("r", f"{r.get('reading', '')}|{float(r.get('impact', 0)):.2f}", say)).strip()

    def tally(self, v):
        """An everyday week that was not told still counts toward the year's picture of how the weeks were spent."""
        v = np.maximum(np.asarray(v, float), 0)
        if v.sum() > 0:
            self.year["weeks"] += v / v.sum()

    def rebound(self, worked, span=0.0):
        """An act that joined colors the world sets against each other: it fit together, or it tore."""
        return mk("b", f"{'fit' if worked else 'tear'}|{span:.2f}", self.fill(self.pick(REBOUND_FIT if worked else REBOUND_SPLIT)))

    def aftermath(self, supported, age, wound=0.0, support=0.0):
        """After a hard blow (engine v6): with support a person comes back to their core; alone it hardens into them."""
        ctx = dict(_age=age)
        return mk("h", f"{'healed' if supported else 'hardened'}|{wound:.2f}|{support:.2f}",
                  self.fill(self.pick(HEALED if supported else HARDENED, phase(age)), phase(age), ctx))

    def streak(self, bad, level=0.0):
        return mk("q", f"{'trouble' if bad else 'fortune'}|{level:.2f}", self.fill(self.pick(STREAK_BAD if bad else STREAK_GOOD)))

    def told_moment(self, m, ev, colors=""):
        """A moment the player did not decide, told briefly: the scene, the act, the result."""
        a = self.act_in(m, ev["choice"])
        line = (self.scene(m) + " " + self.fill("{N} chooses {c}. ", ctx=dict(c=chooses_mk(a, colors)))).lstrip() + self._result(m, ev)
        gate = ev.get("gate"); wanted = ev.get("wanted")
        if gate and gate != "chosen" and wanted and wanted != ev["choice"]:
            w = self.act_in(m, wanted)
            why = {"pulled away": "{N} meant to {w}, but old habits won.",
                   "lacked the means": "{N} would rather have chosen {cw}, but could not manage it.",
                   "not offered": "{N} would rather have chosen {cw}, but nobody around them offered that."}.get(gate)
            if why:
                line += " " + self.fill(why, ctx=dict(w=mk("w", gate, w), cw=chooses_mk(w, gate, "w")))
            if why:
                line += " " + self.thought(self.pick(MISSED[0] if ev["success"] else MISSED[1]), "missed")
                return line
        if abs(float(ev.get("delta", 0))) > 0.25:
            line += " " + self.react(ev["success"], m["sit"])
        return line

    def ordinary(self, ev, k):
        """An ordinary week, told only at the most detailed level; always counted for the chapter."""
        if 0 <= k < 5:
            self.year["weeks"][k] += 1
        return self.fill("An ordinary week: {N} chooses to {a}.", ctx=dict(a=mk("a", COLORS[k] if 0 <= k < 5 else "", act(ev["choice"]))))

    # ---------------------------------------------------------------- the world and the life's turns
    def outside(self, o, stage, detail):
        """An outside event, or None when it is not worth telling at this level of detail."""
        name = o["name"]; took = o.get("took")
        moved = took is not None and abs(took) > 0.45
        stage = phase(o["age"])
        if name == "small daily frictions add up":
            self.year["frictions"] += 1
        if detail < 2:
            if detail == 0 and name not in SEVERE:
                return None
            if detail == 1 and name not in NOTABLE and not moved:
                return None
        ctx = dict(_age=o["age"])
        if name == "moving somewhere new":
            old = self.place
            pl = [p for p in self.W["places"] if p != old]
            self.place = pl[int(self.rng.integers(len(pl)))]
            ctx.update(oldplace=old, newplace=self.place)
            again = self._moved_at is not None and o["age"] - self._moved_at < 1.0
            self._moved_at = o["age"]
            self.left_behind()
            if again:                   # a second move in a row
                return self.fill("Before they have even settled in, {N} moves again, this time to " + an(self.place) + ".")
        if name == "an institution rewards a kind of person":
            ctx["inst"] = self.W["inst"][0 if stage <= 1 else 1 if stage <= 3 else 2]
            ctx["inst_cap"] = cap(ctx["inst"])
        if name == "a brush with death":
            bs = self.W["brushes"]
            ctx["brush"] = bs[int(self.rng.integers(len(bs)))]; ctx["brush_cap"] = cap(ctx["brush"])
        line = self.fill(self.pick(OUTSIDE.get(name, [("", name + ".")]), stage), stage, ctx)
        if moved and o.get("message"):
            v = np.asarray(o["message"], float)
            c = COLORS[int(np.argmax(v))]
            if took > 0:
                line += " " + mk("x", f"{took:+.2f}|{c}", self.fill(self.pick(TOOK[0]), ctx=dict(value=(VALUE, VALUE2)[int(self.rng.integers(2))][c])))
            else:
                line += " " + mk("x", f"{took:+.2f}|{c}", self.fill(self.pick(TOOK[1])))
        return line

    def era(self, e):
        took = e["took"]
        react = ("{N} takes to it." if took > 0.3 else "{N} sets their face against it." if took < -0.3 else "{N} barely notices.")
        return self.fill("The times are turning. " + self.W["era"].get(e["kind"], "") + " Everywhere, the talk is of "
                         + mk("e", e["kind"], e["idea"]) + ". " + mk("x", f"{took:+.2f}|era", react))

    def role_mark(self, d, text=None, state=""):
        """A title or perk as a hoverable phrase (marker o): the browser shows its kind, ways and what it does."""
        return mk("o", f"{d['name']}|{d['kind']}|{d['ways']}|{1 if d['title'] else 0}|{d.get('plus', 0)}|{state}",
                  d["say"] if text is None else text)

    def title_line(self, r, d, frm=None):
        """A title or perk gained, lost, suspended or restored (the engine's role event r, the catalogue's words d; frm: the
        title it grew from)."""
        what, how = r["what"], r["how"]
        lead = LOSS_LEAD.get(how, "") if what in ("lost", "suspended") else ""
        if what == "reshaped" and d["title"]:          # the same title, held another way now (the new profile's words)
            way = how.strip().rstrip(".")
            if not way or way == "in other ways":
                return self.fill("{N} is still " + self.role_mark(d) + ", but holds it differently now.")
            return self.fill("{N} is still " + self.role_mark(d) + ", and now " + way[0].lower() + way[1:] + ".")
        if d["title"]:
            if what == "gained":
                if d["kind"] == "status" and d["name"] in STATUS_LINE:
                    tpl, word = STATUS_LINE[d["name"]]
                    return self.fill(tpl.replace("<o>", self.role_mark(d, word)))
                if how == "changed jobs":
                    return self.fill("{N} changes jobs, and is " + self.role_mark(d) + " now.")
                if frm and d["kind"] in ("career", "community"):
                    return self.fill("{N} is " + self.role_mark(d) + " now, after being " + frm + ".")
                return self.fill("{N} is " + self.role_mark(d) + " now.")
            if what == "lost":
                if how == "gave it up":
                    return self.fill("{N} gives up being " + self.role_mark(d, state="lost") + ".")
                if how == "outgrew it" and d["kind"] in ("community", "career"):
                    return self.fill("{N} has outgrown being " + self.role_mark(d, state="lost") + ".")
                return self.fill(lead + "{N} is no longer " + self.role_mark(d, STATUS_WORD.get(d["name"], d["say"]), "lost") + ".")
            return ""
        pred = d["pred"]
        if what in ("gained", "regained", "restored"):
            again = what != "gained" or how == "regained"
            return self.fill("{N} " + self.role_mark(d, pred) + (" again." if again else "." if pred.startswith("always ") else " now."))
        if what == "suspended":
            return self.fill(lead + "{N} " + self.role_mark(d, neg_of(pred), "suspended") + ", for a while.")
        if what == "lost":
            lead = "Out of practice, " if how == "slipped away" and d["kind"] == "skill" else lead
            return self.fill(lead + "{N} " + self.role_mark(d, neg_of(pred), "lost") + ".")
        return ""

    def commitment(self, c, m=None, title=None):
        """A commitment starts, ends or changes. title: the catalogue's title that came with a start this week (role_info),
        told in the same line."""
        line = self._commitment(c, m, title)
        if title and c["what"] == "start" and c["kind"] != "career" and not (
                c["kind"] == "children" and title["name"] in ("mother or father", "adoptive parent", "foster parent", "stepparent")):
            line += " " + self.fill("{N} is " + self.role_mark(title) + " now.")
        return line

    def _commitment(self, c, m=None, title=None):
        kind, what = c["kind"], c["what"]
        prof = np.asarray(c["profile"], float) if c.get("profile") else None
        top = COLORS[int(np.argmax(prof))] if prof is not None else "W"
        if what == "inherited":
            return self.fill("{N} is raised in " + mk("c", f"faith|{top}|inherited", "the family faith") + ", " + an(FAITH_ADJ[top]) + " one.")
        if what == "start":
            through = c.get("through", "")
            if kind == "career":
                job = (mk("c", f"career|{top}|start", "work") + " as " + self.role_mark(title) if title else
                       mk("c", f"career|{top}|start", CAREER[self.setting].get(through, "work")))
                met = m["ctx"].get("_p_boss") if m else None     # the boss the scene already introduced
                if met is not None:
                    return self.fill("{N} takes up " + job + ".")
                boss = self.new("boss", self.W["new_boss"])
                return self.fill("{N} takes up " + job + ". " + cap(self.W["runs"].format(b=self.say(boss))))
            if kind == "partner":
                p = m["ctx"].get("_p_prospect") if m else None
                if p is None and m is not None and m["ctx"].get("_p_partner") is not None:
                    p = m["ctx"]["_p_partner"]                    # the companion the scene already named
                if p is None:
                    ps = self.alive("companion") + self.alive("prospect")
                    p = ps[-1] if ps else self.new("prospect", "someone called {n}")
                for q in self.alive("partner"):         # whoever was partner before is a former partner now
                    if q is not p:
                        q["role"] = "ex"
                p["role"] = "partner"
                return self.fill("{N} and " + self.say(p) + " make it official: " + mk("c", f"partner|{top}|start", "they are together now") + ".")
            if kind == "children" and title and title["name"] in ("adoptive parent", "foster parent", "stepparent"):
                if title["name"] == "stepparent":           # the engine counts the partner's child among theirs (R15)
                    ch = self.new("child", "a stepchild, {n}"); ch["born"] = True
                    ch["ref"] = "their stepchild " + ch["name"]
                    return self.fill("{N} becomes " + self.role_mark(title) + ": a partner's child, " + self.nm(ch) + ", is part of their life now.")
                ch = self.new("child", "a child, {n}" if title["name"] == "adoptive parent" else "a foster child, {n}")
                ch["ref"] = "their child " + ch["name"]
                if title["name"] == "adoptive parent":
                    return self.fill("{N} adopts " + self.nm(ch) + ": " + self.role_mark(title) + " now.")
                return self.fill("{N} takes in " + self.nm(ch) + ", a child who needs a home: " + self.role_mark(title) + " now.")
            if kind == "children":
                first = not self.alive("child")
                fresh = [q for q in self.alive("child") if not q.get("born") and getattr(self, "age", 0) - q.get("made", -99) < 0.1]
                if fresh:                               # a scene this week already held the newborn: the same child
                    ch = fresh[-1]; ch["born"] = True; first = len(self.alive("child")) == 1
                    return self.fill(("{N}'s first child is born: " if first else "Another child is born to {N}: ") + self.nm(ch) + ".")
                ch = self.new("child", "a child, {n}"); ch["born"] = True
                line = ("{N}'s first child is born: " if first else "Another child is born to {N}: ") + self.nm(ch) + "."
                ch["ref"] = "their child " + ch["name"]
                if through == "raise a big family":
                    more = [self.new("child", "their child {n}") for _ in range(2)]
                    for x in more:
                        x["introduced"] = True
                    line += " Then come " + self.nm(more[0]) + " and " + self.nm(more[1]) + "."
                return self.fill(line)
            by = "" if title and through == title["name"] else ", by choosing to " + act(through)    # a title that came in time
            if kind == "faith":
                if title and title["name"] in CAUSES:  # the engine's faith place also holds causes (the catalogue's campaigners)
                    return self.fill("{N} takes up " + mk("c", f"faith|{top}|start", "a cause") + by + ".")
                return self.fill("{N} takes up " + mk("c", f"faith|{top}|start", "a faith, " + an(FAITH_ADJ[top]) + " one") + by + ".")
            if kind == "community":
                return self.fill("{N} becomes part of " + mk("c", f"community|{top}|start", "a community in the {place}") + by + ".")
            return self.fill("{N} takes on a " + kind + ".")
        if what == "left":
            if kind == "partner":
                ps = self.alive("partner")
                if ps:
                    ps[0]["role"] = "ex"
                    return self.fill("{N} and " + self.nm(ps[0]) + " part ways.")
                return ""                               # already apart in the story: nothing to tell
            if kind == "career":
                for b in self.alive("boss"):
                    b["role"] = "former boss"
                return self.fill(self.pick([("R", "{N} walks out of their {job}, and does not look back."), ("", "{N} quits their {job}."),
                                            ("U", "{N} leaves their {job}, having learned what it had to teach.")]), ctx=dict(job=self.W["job"]))
            if kind == "faith":
                if c.get("drifted"):                    # no decision was made: it stopped mattering (the engine's drifted flag)
                    return self.fill(self.pick([("", "Somewhere along the way, what {N} believed in stops mattering to them."),
                                                ("U", "{N} stops believing without ever deciding to; the questions simply won."),
                                                ("R", "{N} stops showing up, and one day notices the belief is gone.")]))
                return self.fill("{N} leaves the faith.")
            if kind == "community":
                return self.fill("{N} drifts away from their community.")
            return self.fill("{N} walks away from their " + kind + ".")
        if what == "lost job":
            bs = self.alive("boss")
            for b in bs:
                b["role"] = "former boss"
            return self.fill("{N} loses their " + mk("c", "career||lost job", self.W["job"]) + "." + (f" {self.nm(bs[0])} does not meet their eye." if bs else ""))
        if what == "retired":
            return self.fill(self.pick([("", "{N} retires."), ("G", "{N} retires, and the days grow slower and wider."),
                                        ("B", "{N} retires, reluctantly, still counting what they are owed.")]))
        if what == "widowed":
            ps = self.alive("partner")
            if ps:
                self.dies(ps[0])
                return self.fill(self.nm(ps[0]) + " dies. {N} is " + mk("c", "partner||widowed", "widowed") + ".")
            gone = [p for p in self.people if p["role"] == "partner" and not p["alive"]]
            if gone and gone[-1]["name"] in self._told_dead:
                return self.fill("{N} is " + mk("c", "partner||widowed", "widowed") + ".")
            if gone:
                return self.fill(self.nm(gone[-1]) + " dies. {N} is " + mk("c", "partner||widowed", "widowed") + ".")
            return self.fill("{N}'s partner dies.")
        if what == "broke up" and kind == "partner":
            ps = self.alive("partner")
            if ps:
                ps[0]["role"] = "ex"
                return self.fill(self.pick([("", "{N} and {p} break up."), ("R", "{N} and {p} break up, loudly, and for good."),
                                            ("W", "{N} and {p} end it, as decently as they can."),
                                            ("G", "{N} and {p} let it go; whatever grew between them has run its course.")]),
                                 ctx=dict(p=self.nm(ps[0])))
            return ""
        if what == "outgrew it":                   # a title the person is too old for (a scout at nineteen): its own line tells it
            return ""
        return self.fill("{N} leaves their " + ("family years" if kind == "children" else kind) + " behind.")

    def clash(self, c):
        how = CLASH_HOW.get(c["how"], "it ends")
        return self.fill("The long quarrel between {N} and their own " + c["kind"] + " is over: " + how + ".")

    def rite(self, r, sit=None):
        to = r["to"]
        if r.get("quiet"):
            return mk("R", to, self.fill(RITE_QUIET.get(to, "{N} grows older.")))
        what = SNOUN.get(sit, "it")
        return mk("R", to, self.fill(self.pick(RITE.get(to, ["{N} grows older."])), ctx=dict(what=what, what_cap=cap(what))))

    def conversion(self, c):
        tow = np.asarray(c["toward"], float)
        new = COLORS[int(np.argmax(tow))]
        old = c["disowned"]
        return self.fill(mk("C", f"{old}|{new}", "Something gives way.") + " {N} loses faith in " + self.val(old) + ", and turns toward "
                         + self.val(new) + ". " + self.thought(self.pick(REASON[new]), "reason", new))

    def breakthrough(self, b):
        want = np.asarray(b["want"], float) - np.asarray(b["before"], float)
        new = COLORS[int(np.argmax(want))]
        age = float(b["age"]); last = self._broke
        self._broke = age
        if last is not None and age - last < 1.0:
            return None
        if last is not None and age - last < 4.0:
            return mk("B", new, self.fill(self.pick(["Once again {N} gives in to what they keep holding back: {v}.",
                                                   "The old wanting breaks through again: {v}."]), ctx=dict(v=self.val(new))))
        fresh = ("With a round birthday ahead, it feels like now or never. " if int(age) % 10 == 9 else
                 "New surroundings make it easier. " if self._moved_at is not None and age - self._moved_at < 1.0 else "")
        return self.fill(fresh + mk("B", new, "What {N} has held back for years breaks through.") + " They turn toward " + self.val(new) + ".")

    def temperament(self, moved, keys=()):
        return self.fill(self.pick(["People who know {N} say they have become {m}.", "Over the years {N} has become {m}."]),
                         ctx=dict(m=mk("T", ",".join(keys), ", and ".join(moved))))

    # ---------------------------------------------------------------- v7: dreams, passions and plans
    def goal_words(self, kind, domain, mix, gid=0):
        """What a goal is about: (as a dream, as a passion, as a plan's verb). The id keeps the same words for one goal;
        a dream the engine named from the Library's catalogue keeps its own words."""
        info = self.dreams.get(int(gid))
        if info:
            g_d = dream_of(info["name"], info.get("domain", ""))
            fb = self._generic_goal_words(domain, mix, gid)
            return g_d, their(info["passion"]) if info.get("passion") else fb[1], their(info["plan"]) if info.get("plan") else fb[2]
        return self._generic_goal_words(domain, mix, gid)

    def _generic_goal_words(self, domain, mix, gid=0):
        if domain in GOAL_D:
            return GOAL_D[domain]
        v = np.asarray(mix, float)
        c = COLORS[int(np.argmax(v))]
        g, verb = GOAL_C[c][int(gid) % len(GOAL_C[c])]
        return g, g, verb

    def life_words(self, gid):
        """A named dream's life-goal phrase ("a whole career keeping one town safe"), or None."""
        info = self.dreams.get(int(gid))
        return their(info["life"]) if info and info.get("life") else None

    def dream_info(self, rec):
        """The dream behind a goal record: the engine's names (name, passion, plan, life; flat on the record or under
        "dream"), completed from the Library's catalogue, kept by the goal's id for the HUD and the inner voice."""
        gid = int(rec.get("id", 0))
        d = rec["dream"] if isinstance(rec.get("dream"), dict) else rec
        name = next((d[k] for k in ("name", "dream") if isinstance(d.get(k), str) and d[k]), None)
        if name is None:
            return self.dreams.get(gid)
        cat = dream_catalogue()["by_name"].get(name, {})
        def f(*keys):
            for k in keys:
                if isinstance(d.get(k), str) and d[k]:
                    return d[k]
            return cat.get(keys[0]) if isinstance(cat.get(keys[0]), str) else None
        info = dict(name=name, domain=cat.get("domain") or (d.get("domain") if isinstance(d.get("domain"), str) else ""),
                    passion=f("passion"), plan=f("plan"), life=f("life", "life_goal", "life_phrase"))
        self.dreams[gid] = info
        return info

    def spark_say(self, rec):
        """The spark's narration line (the Library's say, with {N}), from the record or the catalogue."""
        d = rec["dream"] if isinstance(rec.get("dream"), dict) else rec
        say = d.get("say") if isinstance(d.get("say"), str) else rec.get("say") if isinstance(rec.get("say"), str) else None
        return say or dream_catalogue()["say"].get(self.setting, {}).get(rec.get("trigger", ""))

    def goal(self, rec):
        """A dream, passion or plan begins, turns into another, comes true or ends (engine v7 goal records)."""
        kind, what, src = rec["kind"], rec["what"], rec.get("source", "")
        info = self.dream_info(rec)
        if kind == "dream" and what != "begins":                           # no longer a dream: let go, pushed aside, a passion or a plan
            self.dreams_held.pop(int(rec.get("id", 0)), None)
        g_d, g_p, verb = self.goal_words(kind, rec.get("domain", ""), rec.get("mix", (0.2,) * 5), rec.get("id", 0))
        life = self.life_words(rec.get("id", 0)) if info else None
        hz = HORIZON_WORD.get(rec.get("horizon", ""), "")
        cols = "".join(c for c, x in zip(COLORS, rec.get("mix", ())) if x >= 0.24) or COLORS[int(np.argmax(rec.get("mix", (0.2,) * 5)))]
        ctx = dict(g=g_p if kind == "passion" else g_d, v=verb, h=hz, p=g_p, l=life or "")
        line = None
        if what == "begins" and kind == "dream":
            say = self.spark_say(rec) if info else None
            tr = TRIGGER.get(rec.get("trigger", ""))
            if say:                                     # the spark as the Library tells it, then the dream it left
                ctx["S"] = self.fill(say)
                again = info["name"] in {v for k, v in self.dreams_held.items() if k != int(rec.get("id", 0))}
                line = self.pick(DREAM_AGAIN if again else DREAM_SAY)
            elif tr:
                raw = tr[("earth", "tribal", "magic").index(self.setting)]
                ctx["T"] = self.fill(raw)
                lead = re.match(r"^((?:⟦[^⟧]*⟧)*)(Their|The|A|An|Someone|Watching) ", ctx["T"])
                if lead:                                # mid-sentence it stays lower case: "After their teacher Hester, ..."
                    ctx["T"] = lead.group(1) + lead.group(2).lower() + ctx["T"][lead.end(2):]
                line = self.pick(DREAM_FROM)
            else:
                line = self.pick(DREAM_NEW)
        elif what == "begins" and kind == "plan" and src != "dream":
            line = LIFE_FROM.get(src, LIFE_FROM[""]) if life and rec.get("horizon") == "life" else PLAN_FROM.get(src, PLAN_FROM[""])
        elif life and kind == "plan" and rec.get("horizon") == "life" and what in LIFE_END:
            line = LIFE_END[what]
        elif info and (kind, what) in NAMED_END:
            long_ = "," in g_d or len(g_d.split()) > 7
            line = self.pick((NAMED_SHORT if long_ and (kind, what) in NAMED_SHORT else NAMED_END)[(kind, what)])
        elif (kind, what) in GOAL_END:
            line = self.pick(GOAL_END[(kind, what)])
        if not line:
            return None
        if not hz:
            line = line.replace(" {h}", "")
        elif info:                                      # a named plan is a long phrase: the deadline after a comma
            line = line.replace(" {h}", ", {h}")
        if kind == "dream" and what == "begins" and info:
            self.dreams_held[int(rec.get("id", 0))] = info["name"]
        pay = f"{kind}|{what}|{cols}|{rec.get('domain', '')}|{src}|{rec.get('horizon', '')}"
        return mk("g", pay, self.fill(line, ctx=ctx))

    def name_goal(self, text, kind, domain, mix, gid, horizon=""):
        """The engine's default name for a goal ("the plan (B W)") in the story's words, for the inner voice and lessons."""
        g_d, g_p, verb = self.goal_words(kind, domain, mix, gid)
        life = self.life_words(gid) if kind == "plan" and horizon == "life" else None
        if life:
            return f"their life goal, {life}"
        return {"dream": f"the dream of {g_d}", "passion": f"the passion for {g_p}"}.get(kind, f"the plan to {verb}")

    # ---------------------------------------------------------------- v7: the inner voice before a choice, what came of it after
    def insight(self, key, line, heart_driver, head_driver, self_control):
        return mk("i", f"{key}|{heart_driver}|{head_driver}|{self_control:.2f}", self.fill(line))

    def aside(self, key, line):
        return mk("j", key, self.fill(line))

    def needs_line(self, needs):
        """The needs a choice's week moved, as one line (IDEAS.md, "Make needs visible"); empty when none moved."""
        if not needs:
            return ""
        bits = [f"{NEED_SAY.get(x['need'], x['need'])} {x['before'] * 100:.0f}% → {x['after'] * 100:.0f}%" for x in needs[:4]]
        return "Needs: " + ", ".join(bits) + "."

    def _hrng(self):
        """Its own random stream, so lives without pushes are told exactly as before."""
        if getattr(self, "_hr", None) is None:
            self._hr = np.random.default_rng(int(self.seed) + 9177)
        return self._hr

    def hindsight(self, kind, need, worked):
        """How the character judges a push, looking back (IDEAS.md, "Player intervention that helps")."""
        if kind == "accepted":
            return self.fill(self._hrng().choice(HINDSIGHT["accepted"]).replace("{need}", need or "what was missing"))
        if kind == "resented":
            return self.fill(self._hrng().choice(HINDSIGHT["resented_fail" if not worked else "resented_empty"]))
        return ""

    def resolution(self, r):
        """What came of a choice, as the terminal tells it (the browser draws the same dict as a panel)."""
        L = [self.fill(SURPRISE.get((r["worked"], r["surprise"]), "It is done."))]
        if r.get("pushed"):
            L.append(self.fill("You pushed {N} into it" + (", against everything in them." if not (r["with_heart"] or r["with_head"]) else
                                                          ", the way the head said." if r["with_head"] else ", the way the heart wanted.")))
        elif r.get("with_heart") and r.get("with_head"):
            L.append(self.fill("{N} followed both heart and head."))
        elif r.get("with_heart"):
            L.append(self.fill("{N} followed the heart over the head."))
        elif r.get("with_head"):
            L.append(self.fill("{N} followed the head over the heart."))
        elif "with_heart" in r:
            L.append(self.fill("{N} went a third way, neither the heart's first choice nor the head's."))
        if r.get("regret"):
            L.append(self.fill("It will be regretted: the heart won against the head, and lost."))
        bec = [mk("z", f"{c['what']}|{c['delta']}|{c['size']}", c["word"]) for c in r.get("became", [])]
        if bec:
            L.append(self.fill("{N} is " + (", ".join(bec[:-1]) + " and " + bec[-1] if len(bec) > 1 else bec[0]) + " now."))
        gained = [x["word"] for x in r.get("states", []) if x["what"] == "gained"]
        lost = [x["word"] for x in r.get("states", []) if x["what"] != "gained"]
        join = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]
        if gained:
            L.append(self.fill("{N} is " + join(gained) + " now."))
        if lost:
            L.append(self.fill("{N} is no longer " + join(lost) + "."))
        cl = r.get("closer")
        if cl:
            L.append(mk("y", f"{cl['identity']}|{cl['guild']}|{cl['distance']}",
                        self.fill(("A step closer to becoming " if cl["distance"] < 0.05 else "Slowly moving toward ") + cl["guild"] + ".")))
        for les in r.get("lessons", [])[:2]:
            L.append(mk("n", les["key"], self.fill(les["line"])))
        return "\n".join(L)

    # ---------------------------------------------------------------- the yearly chapter
    def chapter(self, age, stage, w, content, peace, ident=""):
        """The head of a new year: how life feels, what drives them, and where the ordinary weeks went."""
        w = np.asarray(w, float)
        stage = phase(age)
        band = ("h" if content >= 0.62 else "l" if content <= 0.30 else "m") + ("h" if peace >= 0.67 else "l" if peace <= 0.47 else "m")
        band = band if band in MOOD else "mm"
        L = [mk("m", f"{content:.2f}|{peace:.2f}", self.fill(self.pick(MOOD[band], stage), stage))]
        if self._last_c is not None and abs(content - self._last_c) > 0.15 and band != "mm":
            L.append(mk("d", f"{content - self._last_c:+.2f}", "Better than last year." if content > self._last_c else "Worse than last year."))
        self._last_c = content
        # a slow shift in emphasis, told once it has really happened
        top = COLORS[int(np.argmax(self.voice))]
        if (self._voice_top is not None and top != self._voice_top and self.voice[CI[top]] - self.voice[CI[self._voice_top]] > 0.025
                and age - self._shift_age >= 3):
            o = self._voice_top
            L.append(mk("s", f"{o}|{top}", self.fill(self.pick(SHIFT), ctx=dict(old=NOUN[o], new=NOUN[top], old_adj=ADJ[o], new_adj=ADJ[top]))))
            self._voice_top = top; self._shift_age = age
        elif self._voice_top is None and age >= 6:
            self._voice_top = top
        lead = tuple(self.leading())
        if age >= 6 and (lead[0] != self._values_told[0] or age - self._values_told[1] >= 6):
            self._values_told = (lead[0], age)
            s = "What drives {N} now is " + self.val(lead[0])
            s += (", and after that, " + self.val(lead[1]) + "." if len(lead) > 1 else ".")
            L.append(self.fill(s))
        wk = self.year["weeks"]
        if wk.sum() >= 3:
            c = COLORS[int(np.argmax(wk))]
            if c != self._weeks_told[0] or age - self._weeks_told[1] >= 3:      # told when it changes, or now and then
                self._weeks_told = (c, age)
                L.append(mk("k", c + "|" + ",".join(f"{x:.0f}" for x in wk), self.fill(self.pick([(c, x[0], x[1]) for x in WEEKS[c]], stage), stage)))
        if self.year["frictions"] >= 2:
            L.append(mk("f", self.year["frictions"], "Small frictions pile up all year."))
        self.last_weeks = [round(float(x), 1) for x in self.year["weeks"]]
        self.year = dict(weeks=np.zeros(5), frictions=0)
        head = f"── Age {int(round(age))}" + (f" · {ident}" if ident else "") + " ──"
        return head + "\n" + " ".join(L)

    def epitaph(self, w):
        lead = self.leading(np.asarray(w, float) * 0.5 + self.voice * 0.5)
        s = "Here the story of {N} ends. They are remembered as someone who " + mk("v", lead[0], EPITAPH[lead[0]])
        s += (", and " + mk("v", lead[1], EPITAPH[lead[1]]) + "." if len(lead) > 1 else ".")
        return self.fill(s)
