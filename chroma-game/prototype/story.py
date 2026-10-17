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
# Since the split (chroma-game/CLAUDE.md): the module code before class Story is in story_base.py and Story's methods
# are in the four mixin modules below; this file keeps the class and its core (__init__ to nm). Every name story.py
# had is still importable from story.
from story_base import *  # noqa: F401,F403
from story_base import _DREAMS, _worlds  # noqa: F401
from story_cast import CastMixin
from story_moments import MomentsMixin
from story_lines import LinesMixin
from story_goals import GoalsMixin


class Story(CastMixin, MomentsMixin, LinesMixin, GoalsMixin):
    birth_place = None      # the outer world's birthplace, in words (set by the game when the world is on)

    def __init__(self, name, seed, place="town", setting="earth"):
        self.name = name
        self.rng = np.random.default_rng(int(seed) + 4243)
        self.seed = int(seed)
        self.place = place
        self.setting = setting if setting in WORLD else "earth"
        self.W = WORLD[self.setting]
        self.wcode = SETTINGS[self.setting]["code"]
        self.hold = False                   # v22.5, F12: the game's world_hold (the world's own words)
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
        # v22.5 F7, one roll of the living (the engine's one_roll; the game sets it every week): the people the world has
        # lost and the story has not yet told, (engine role, person), told first by the next death of that role
        self.one_roll = False
        self.due = []
        self.kids_n = 0                     # F7: the engine's living children (the game sets it every week with one_roll)
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
        p = dict(id=1 + max((q["id"] for q in self.people), default=-1), name=n, role=role, ref=ref.format(n=n), alive=True, introduced=False, met=None, seen=0,
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
