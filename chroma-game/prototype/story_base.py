"""The story layer's words, tables and helpers: everything story.py held before class Story, moved out verbatim.
story.py and the Story mixins import from here."""
import re
from collections import deque
import numpy as np
from story_text import WORLD_LEAKS, EPITHETS, GOAL_END, NAMED_END, SCENES, OUTCOMES, GONE_OUT, REACT, MOOD, WEEKS, OUTSIDE, HEALED, HARDENED, SNOUN, CAREER, ACT_FIX, STATUS_LINE  # noqa: E402,F401  the text tables (data only)

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


def _worlds():
    """v22.5, F12: the Library's words of the tribal and magic worlds (worlds.py, pinned next to the engine), or None."""
    try:
        import worlds
        return worlds
    except ImportError:
        return None


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
# Named dreams (the Library's dreams.py, Emren 2026-10-06 22:19): the engine names each dream by the nearest catalogue
# entry and passes the spark's say line, the dream's name and its passion, plan and life-goal phrases. {S} is the say
# line, {g} the dream ("becoming a police officer"), {p} its passion, {v} its plan, {l} its life goal.
DREAM_SAY = ["{S}. From that day {N} dreams of {g}.", "{S}. After that, {N} dreams of {g}.", "{S}. It leaves {N} dreaming of {g}."]
DREAM_AGAIN = ["{S}. It feeds an old dream of {N}'s: {g}.", "{S}. The dream of {g} burns brighter in {N}."]   # a dream they already hold
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


# ------------------------------------------------------------------ the character's thoughts
REASON = {   # why they lean toward an act: the act's own colors speak
    "W": ["It's the right thing to do.", "Someone has to do this properly.", "What would a decent person do here?", "There are rules for a reason."],
    "U": ["Think first. Then act.", "There's a smarter way through this.", "I want to understand it before I touch it.", "Let me see how it works."],
    "B": ["What do I get out of this?", "Nobody else is going to look out for me.", "Use what you have.", "Winning is what counts."],
    "R": ["Don't think. Go.", "I'm sick of waiting.", "My gut already knows.", "If it feels right, it is right."],
    "G": ["This is how it has always been done.", "Let things take their course.", "Stay close to your own.", "Don't fight what is meant to be."],
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

ROLL_KIN = ("mother", "father", "grandparent", "sibling", "partner", "child")   # F7: the people the engine keeps the roll of
TAKEN_IN = re.compile(r"adopt|foster|take (?:them |a child |the child )?in\b", re.I)   # F7: a child taken in, not born
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

SHIFT = ["Slowly, the {old} that used to drive {N} gives ground to {new}.",
         "{N} is not who they were a few years ago: less {old_adj}, more {new_adj}.",
         "Something has shifted in {N}: where {old} once led, {new} leads now."]

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
# item 6 (the game's lines_tied): the mark on an outside event that moved them little (|took| .45 or less), so every
# outside event shows the color it carried
TOOK_SMALL = dict(up="A little of it stays with {N}.", flat="It barely touches {N}.", down="{N} keeps it at arm's length.")

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
KINDREF = dict(career="their work", children="family life", community="the community", faith="their faith")
EPITAPH = dict(W="kept their word", U="never stopped asking why", B="made their own way, on their own terms",
               R="lived every day as if it mattered", G="kept faith with their people and the turning seasons")


# ---- story fields written by the Library (modern Earth batch, approved by Emren 2026-10-05 05:11): scenes per world
# with one variant per color (child/older as k/a), two works and two fails lines, and the act as the narrator says it.
# Filled by load_library_story() from whatever library the pinned engine compiles; the game's own lines above stay as
# the fallback for situations, worlds or stages the Library has not written yet.
LIB_SCENES, LIB_OUTCOMES, LIB_ACTS, LIB_READ = {}, {}, {}, {}
# F7 (one_roll): the moments that tell a funeral or what it leaves, so their {dead} died within DEAD_LATELY years (a
# friend's, a friend); with none lately gone, someone new has just died. Other moments of the dead remember the latest
DEAD_FRESH = {"a memorial service for a friend", "an old friend's funeral", "the funeral bill", "the funeral where everyone sings",
              "ten people at the graveside", "a dispute over an inheritance"}
DEAD_LATELY = 1.0
LIB_OUT_NOT = {}   # F11b (v22.4.1): per moment, (option labels, per works line and per fails line the options it does not fit)
LIB_GRIEF = set()          # moments in which someone dies (kills:)
LIB_ECHO = {}              # echo -> the mark it answers ("a promise you broke comes back" -> "broke your word")
LIB_GONE = {}              # Picks come back: an echo's or return's scenes for a seed person who died or moved far (scenes_gone)
WCODE = dict(earth="E", tribal="T", magic="M")
PERSON_SLOTS = ("friend", "rival", "partner", "prospect", "sibling", "colleague", "boss", "mentor", "parent", "child",
                "grandparent", "elder")


def load_library_story(situations, read_events=()):
    """Take the Library's story fields from its situation dicts (and its read outside events, when given).
    Called once per life: an empty call clears them (settings the Library has not written use the game's own lines)."""
    for d in (LIB_SCENES, LIB_OUTCOMES, LIB_ACTS, LIB_READ, LIB_ECHO, LIB_OUT_NOT, LIB_GONE):
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
        if x.get("scenes_gone"):
            LIB_GONE[x["name"]] = pool(x["scenes_gone"])
        if x.get("outcomes"):
            LIB_OUTCOMES[x["name"]] = (list(x["outcomes"][0]), list(x["outcomes"][1]))
            if x.get("outcomes_not") and any(any(n) for n in x["outcomes_not"]):
                LIB_OUT_NOT[x["name"]] = ({o[0]: i for i, o in reversed(list(enumerate(x.get("options", ()))))}, x["outcomes_not"])
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


ACT_WORLD = {}   # v22.5, F12 (the game's world_hold): the seed labels as the clan or the towers say them (worlds.py LABELS)


def act(label):
    """An option label as something the character does: 'put your own needs first' -> 'put their own needs first'."""
    label = ACT_WORLD.get(label, label)
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
