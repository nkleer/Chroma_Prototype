"""Text console for the Chroma game: one controller for both the terminal (play.py) and the browser page.

Console.handle(line) takes one line the player typed and returns (text, busy). When busy is True the
console still has work to do (simulating years takes time), and the caller should call handle("")
again after letting the screen refresh. Each call does a bounded amount of simulation.
"""
import json
import random
import time
import numpy as np
from game import Game, PRESETS, WORLDS, FREQ, COLORS, CNAME, letters, label_name, rel_word, accept_word, STAGES, base_word, adj_defs, AROUND_WORDS, AROUND_DEFAULT, book_catalog
from story import SETTINGS, WORLD, plain, NEED_SAY

CHUNK = 104           # weeks simulated per call before handing back to the screen
# a random name for the character: from their birth sex's list or either (chroma-identity/for-the-game.md §4); a start
# whose sex the engine draws takes one from either
CHAR_NAMES = {"female": ["Mira", "Lale", "Esra", "Ilse", "Nora"], "male": ["Tobin", "Iven", "Rafe", "Bram", "Cael"],
              "either": ["Ari", "Noor", "Kai", "Sol", "Juno", "Deniz", "Rowan", "Sasha"]}
NAMES = [n for v in CHAR_NAMES.values() for n in v]


def char_name(sex=None):
    return random.choice(CHAR_NAMES.get(sex, []) + CHAR_NAMES["either"])


def _fp(v):
    """Felt odds as a percent, never quite certain either way."""
    return f"{min(99, max(1, round(v * 100)))}%"

HELP = """Keys while watching
  Enter   live on until the next checkpoint
  w m y   one week, one month, one year
  d       ten years
  s       status: colors, the four color vectors, meta variables, titles
  f       how often checkpoints come (rare, normal, often, every)
  v       how much of daily life the story tells (quiet, normal, every week)
  l       ledger: show the numbers under the story (on or off)
  p       dreams, passions and plans; make a plan for them, or drop one
  n       start a new life
  h       this help
Keys at a checkpoint
  Enter   let them choose for themselves
  1, 2..  push them to that option. They always go through with it; the less they wanted it,
          the more it costs them (effort, stress, pent-up wanting).
  i       heart and head on each option, and what may follow
  s       status
  p f v l n h work here too
After each choice
  Enter   go on (what came of it stays in the story)"""

CUSTOM_STEPS = [
    ("name", "Name? (Enter for a random one)"),
    ("sex", "Sex at birth?  1 female  2 male  3 intersex  (Enter: let chance decide)"),
    ("setting", "Setting?\n" + "\n".join(f"  {i} {v['title']}: {v['blurb']}" for i, v in enumerate(SETTINGS.values(), 1))),
    ("earlier", "Which world?  1 a fresh world  2 the world {name} left behind  3 as {name}'s grandchild"),
    ("times", "The times?  1 calm  2 as in life  3 restless  4 turbulent  (Enter: as in life)"),
    ("tech", "Technology?  1 behind the times  2 modern  3 ahead  (Enter: modern)"),
    ("world", "How does their world frame the colors? (Enter for 1)\n  1 " + WORLDS["questions"][0] + "\n  2 " + WORLDS["neutral"][0] + "\n  3 " + WORLDS["pie"][0]),
    ("society", "What does their society reward? Color letters such as W, UB or RG (Enter for nothing in particular)"),
    ("wealth", "Family means?  1 poor  2 modest  3 comfortable  4 rich"),
    ("faith", "Family faith?  1 none  2 one at random  3 give its colors (letters)"),
    ("faith_cols", "The faith's colors? (letters, e.g. WG)"),
    ("upbringing", "Values the family raises them with? Color letters (Enter for none)"),
    ("start_age", "Age when you take over? (0 to 60; their past is simulated up to then)"),
    ("seed", "Seed? (a number to replay the same world; Enter for random)"),
]

# how the browser asks each step: (kind, choices as (what to send, title, detail))
STEP_FORM = {
    "name": ("text", "Their name", "Leave empty for a random one."),
    "sex": ("choice", "Sex at birth", "The body they are born with. Who they come to know themselves to be, and who they love, are not "
            "chosen here: they are found in play, at real rates. Their world decides what it expects of them, and how hard it is to be "
            "someone else.",
            (("1", "Female", "born a girl"), ("2", "Male", "born a boy"),
             ("3", "Intersex", "born with a body between the usual patterns; raised as a girl or a boy"),
             ("4", "Let chance decide", "about half and half; rarely intersex")),
            "Three things, kept apart. The body at birth is chosen here. The gender they know themselves to be is found in play: "
            "for about 98 in 100 it matches; for some it is the other, or neither, or both. The role their world expects of them "
            "comes from the world, the family's faith and the people around them; living outside it costs more where the world "
            "is strict."),
    "setting": ("choice", "The world they are born into", "",
                tuple((str(i), v["title"], v["blurb"]) for i, v in enumerate(SETTINGS.values(), 1))),
    # the outer world's setup (release row W41, world-build.md): an earlier world, the history dial, the technology level
    "earlier": ("choice", "Which world", "A world of its own, or the one an earlier life in this browser left behind.",
                (("1", "A fresh world", "its own history, drawn from the seed"),
                 ("2", "The world {name} left behind", "{name}'s eras, laws, figures and places go on"),
                 ("3", "As {name}'s grandchild", "born into {name}'s family line, in the same world")),
                "An earlier world keeps everything public that happened in it: its eras, laws, wars and the people who led them. "
                "As a grandchild, the birth is placed in that family; everything else about it is still drawn."),
    "times": ("choice", "The times", "How often the world is shaken. It never changes the character's own odds.",
              (("1", "Calm", "about half the real rate of crises, wars and disasters"),
               ("2", "As in life", "real rates: about a dozen recessions and one or two epidemics in 80 years"),
               ("3", "Restless", "half again as many"), ("4", "Turbulent", "twice the real rate"))),
    "tech": ("choice", "Technology", "What the world has when they are born, and how soon new things arrive.",
             (("1", "Behind the times", "the new things arrive late"), ("2", "Modern", "what a rich country has today"),
              ("3", "Ahead", "the newest things come early"))),
    "world": ("choice", "How their world frames the colors", "",
              (("1", "Neutral", WORLDS["neutral"][0]), ("2", "Mild tension", WORLDS["questions"][0]),
               ("3", "The pie, literally", WORLDS["pie"][0]))),
    "society": ("colors", "What their society rewards", "Pick colors, or none for nothing in particular."),
    "wealth": ("choice", "The family's means", "",
               (("1", "Poor", "every coin counted"), ("2", "Modest", "enough, most years"),
                ("3", "Comfortable", "room to choose"), ("4", "Rich", "doors open before they knock"))),
    "faith": ("choice", "The family's faith", "",
              (("1", "None", "no family faith"), ("2", "One at random", "a faith the world offers"),
               ("3", "Choose its colors", "you pick what it expects"))),
    "faith_cols": ("colors", "What the faith expects", "Pick its colors."),
    "upbringing": ("colors", "The values the family raises them with", "Pick colors, or none."),
    "start_age": ("number", "When you take over", "Age 0 to 60; the years before are lived without you."),
    "seed": ("text", "Seed", "A number replays the same world; leave empty for a random one."),
}


PLAN_HZ = [["1", "year", "a year"], ["2", "five years", "five years"], ["3", "life", "a lifetime"]]
PLAN_HZ_KEY = {"1": "year", "2": "five years", "3": "life", "year": "year", "five": "five years", "life": "life"}
PLAN_DOM = [["1", "career", "find work that is theirs"], ["2", "partner", "find a partner"], ["3", "children", "have a child"],
            ["4", "community", "find their people"], ["5", "faith", "find a faith"]]
PLAN_DOM_KEY = {"1": "career", "2": "partner", "3": "children", "4": "community", "5": "faith",
                "career": "career", "partner": "partner", "children": "children", "community": "community", "faith": "faith"}


def legacy_ok():
    """Whether the pinned engine places a birth in an earlier life's family line (world_cfg["legacy"])."""
    try:
        import inspect, world_link
        return "legacy" in inspect.getsource(world_link.WorldLink.__init__)
    except Exception:
        return False


def letters_to_spec(txt):
    cols = [c for c in txt.upper() if c in COLORS]
    if not cols:
        return ""
    return " ".join(f"{c}1" for c in dict.fromkeys(cols))


class Console:
    def __init__(self):
        self.g = None
        self.mode = "menu"
        self.custom = {}
        self.step = 0
        self.job = None           # long-running work: dict(kind, ...)
        self.numbering = {}       # displayed number -> option index at a checkpoint
        self.feed = []            # typed lines for the browser (the game's own feed is added on take_feed)
        self.note = ""            # a short answer to the last key, for the browser
        self.plan = None          # v7: a plan being made (key p): dict(step, horizon, domain, mix, preview)
        # point 9 (Emren 20:39): save a life to a file and load it again. A life is its setup (with the seed) and every line
        # the player typed since; loading replays them, so the life comes back exactly as it was (the engine, the story and
        # the voice all draw from seeded streams). A pause in the middle of a run is kept as "@stop <week>".
        self.inputs = []
        self.replay = None        # dict(lines, i, n) while a loaded life is being replayed
        self._cat_sent = set()    # worlds whose Book of Moments catalogue the page already has
        self.loaded = None        # a note for the page once a replay is done
        self.earlier_meta = None  # the world an earlier life left behind, as the page keeps it: dict(key, name, age)
        self.earlier_data = None  # ... and the world itself, once the player chose it (or a saved life needs it)

    # ------------------------------------------------------------------ entry point
    def start_text(self):
        return self._menu()

    def handle(self, line):
        """One line from the player; returns (text, busy). The text is plain: the browser's markers are stripped."""
        if self.job is None and self.replay is None and self.mode == "play" and (line or "").strip().lower() not in ("s", "h", "i"):
            self.inputs.append((line or "").strip())
        text, busy = self._handle(line)
        if self.replay is not None:
            busy = True                          # a loaded life is still being replayed
        return plain(text), busy

    # ------------------------------------------------------------------ saving and loading a life (point 9)
    def stop(self):
        """The player paused a run: kept as a stop at this week, so a replay pauses at the same place."""
        if self.job is not None and self.g is not None and self.replay is None:
            self.inputs.append(f"@stop {int(self.g.t)}")
        self.job = None

    def save(self):
        """The life so far as a small JSON text: its setup (seed included) and the player's lines."""
        if self.g is None or self.mode not in ("play", "over"):
            return ""
        g = self.g
        return json.dumps(dict(game="chroma", version=1, saved=time.strftime("%Y-%m-%d %H:%M"), name=g.name, age=round(g.age(), 1),
                               identity=g.hud().get("guild", ""), setup={k: v for k, v in self.custom.items()},
                               inputs=list(self.inputs)), separators=(",", ":"))

    def world_in(self, text):
        """The page hands over the world an earlier life left behind: its key, name and age, or the whole world."""
        try:
            d = json.loads(text) if text else None
        except Exception:
            d = None
        if not isinstance(d, dict) or not d.get("key"):
            self.earlier_meta = None; self.earlier_data = None
            return ""
        self.earlier_meta = dict(key=d["key"], name=d.get("name", ""), age=d.get("age"))
        if "world" in d:
            self.earlier_data = d
        return d["key"]

    def world_out(self):
        """The world a life leaves behind, as JSON for the page to keep ("" without one)."""
        if self.g is None:
            return ""
        d = self.g.world_save()
        return json.dumps(d, separators=(",", ":")) if d else ""

    def load(self, text):
        """Start replaying a saved life. Returns (text, busy) like handle()."""
        try:
            d = json.loads(text)
            assert d.get("game") == "chroma" and isinstance(d.get("setup"), dict) and isinstance(d.get("inputs"), list)
        except Exception:
            self.note = "That file is not a saved Chroma life"
            return "That file is not a saved Chroma life.", False
        self.custom = dict(d["setup"]); self.plan = None; self.job = None
        out, busy = self._begin()
        if self.mode != "play":                  # the life could not begin (an earlier world missing here)
            return out, False
        self.inputs = []
        self.replay = dict(lines=[str(x) for x in d["inputs"]], i=0, n=len(d["inputs"]), name=d.get("name", ""), age=d.get("age"))
        self._stop_next()                        # paused while the years before the start were lived
        return out, True

    def _replay_step(self):
        """One saved line, then the work it starts (the caller keeps calling while busy)."""
        r = self.replay
        if r["i"] >= r["n"]:
            self.replay = None
            self.loaded = dict(name=self.g.name, age=round(self.g.age(), 1))
            self.note = f"{self.g.name} is back, at {self.g.age():.0f}"
            return "", False
        line = r["lines"][r["i"]]; r["i"] += 1
        if line.startswith("@stop"):
            return "", True                      # already applied to the run before it
        self.inputs.append(line)
        out, busy = self._dispatch(line)
        self._stop_next()
        return out, True

    def _stop_next(self):
        """A run the player paused: the saved stop that follows it ends it at the same week."""
        r = self.replay
        nxt = r["lines"][r["i"]] if r["i"] < r["n"] else ""
        if nxt.startswith("@stop") and self.job is not None:
            self.job["stop"] = int(nxt.split()[1])
            self.inputs.append(nxt)

    def _handle(self, line):
        line = (line or "").strip()
        if self.job is not None:
            return self._work()
        if self.replay is not None:
            return self._replay_step()
        return self._dispatch(line)

    def _dispatch(self, line):
        try:
            if self.mode == "menu":
                return self._on_menu(line)
            if self.mode == "custom":
                return self._on_custom(line)
            if self.mode == "name":
                return self._on_name(line)
            if self.mode == "play":
                return self._on_play(line)
            if self.mode == "over":
                if line.lower() in ("n", ""):
                    self.mode = "menu"; return self._menu(), False
                return "Life over. Press Enter or n to start a new one.", False
        except Exception as e:  # keep the console alive and say what broke
            self.note = f"error: {type(e).__name__}: {e}"
            return f"[error: {type(e).__name__}: {e}]", False
        return "", False

    # ------------------------------------------------------------------ setup
    def _menu(self):
        L = ["CHROMA: one life, five colors (text prototype on engine v6)", "",
             "Choose where a life begins:"]
        for k, p in PRESETS.items():
            when = "at birth" if p["start_age"] == 0 else f"you take over at {p['start_age']:g}"
            L.append(f"  {k}  {p['title']} ({when})")
            L.append(f"     {p['blurb']}")
        L.append(f"  {len(PRESETS) + 1}  Build your own")
        L.append("")
        L.append("Type a number and press Enter.")
        return "\n".join(L)

    def _on_menu(self, line):
        if line in PRESETS:
            self.custom = dict(PRESETS[line]); self.mode = "name"
            return "Name? (Enter for a random one)", False
        if line == str(len(PRESETS) + 1):
            self.custom = dict(world="questions", society="", wealth=0.3, faith=None, upbringing="", start_age=0.0,
                               setting="earth", place="town")
            self.mode = "custom"; self.step = 0
            return CUSTOM_STEPS[0][1], False
        return self._menu(), False

    # ------------------------------------------------------------------ the browser's view
    def take_feed(self):
        out = self.feed
        if self.g is not None and self.g.feed:
            out = out + self.g.feed; self.g.feed = []
        self.feed = []
        return out

    def hud(self):
        """The whole screen state for the browser: menu, setup step, life, checkpoint or review."""
        d = dict(mode=self.mode, busy=self.job is not None, note=self.note, job=self.job["kind"] if self.job else None)
        self.note = ""
        if self.mode == "menu":
            d["menu"] = [dict(k=k, title=p["title"], blurb=p["blurb"], age=p["start_age"], setting=p["setting"],
                              colors=letters(np.array(_spec(p["society"] or p["upbringing"]))).split("+")
                              if (p["society"] or p["upbringing"]) else [])
                         for k, p in PRESETS.items()]
            d["menu"].append(dict(k=str(len(PRESETS) + 1), title="Build your own", age=None, setting="custom",
                                  blurb="Choose the world, the family, its means and faith, and when you take over."))
        elif self.mode in ("custom", "name"):
            key = "name" if self.mode == "name" else CUSTOM_STEPS[self.step][0]
            kind, q, hint, *ch = STEP_FORM[key]
            if key == "earlier":                     # name the earlier life in the choices
                nm = (self.earlier_meta or {}).get("name", "") or "an earlier life"
                ch = [tuple(tuple(x.replace("{name}", nm) for x in c_) for c_ in ch[0] if c_[0] != "3" or legacy_ok())] + list(ch[1:])
            d["step"] = dict(key=key, q=q, hint=hint, kind=kind, choices=[list(c) for c in (ch[0] if ch else ())], help=ch[1] if len(ch) > 1 else "",
                             i=0 if self.mode == "name" else self.step, n=1 if self.mode == "name" else len(CUSTOM_STEPS),
                             title=self.custom.get("title", "Build your own"))
        if self.replay is not None:
            r = self.replay
            d["replay"] = dict(i=r["i"], n=r["n"], name=r["name"], age=r["age"])
        if self.loaded is not None:
            d["loaded"] = self.loaded; self.loaded = None
        if self.g is not None and self.mode in ("play", "over"):
            d["life"] = self.g.hud()
            d["trace"] = self.g.take_trace()
            d["routine"] = self.g.routine()
            d["adj_defs"] = adj_defs()
            d["around_bands"] = {k: [[t, w] for t, w in v if t > -9] for k, v in AROUND_WORDS.items()}
            d["around_bands"]["*"] = [[t, w] for t, w in AROUND_DEFAULT if t > -9]
            d["around_floor"] = {k: v[-1][1] for k, v in list(AROUND_WORDS.items()) + [("*", AROUND_DEFAULT)]}
            if self.mode == "play" and self.g.pending is not None and self.job is None:
                d["cp"] = self.g.cp_hud(self.numbering)
            elif self.mode == "play" and self.g.resolution is not None and self.job is None:
                d["res"] = self.g.resolution
            if self.plan is not None:
                held = self.g.hud().get("titles", [])
                d["plan"] = dict(self.plan, horizons=PLAN_HZ, domains=PLAN_DOM, held=[t["kind"] for t in held])
            if self.mode == "over" and getattr(self.g, "review", None):
                d["review"] = self.g.review
            # the Book of Moments (Emren 21:44): the world's catalogue once per world, and this life's record at each
            # moment, resolution and the end, which the page merges into the Book it keeps across lives
            wk = "earth" if self.g.setting == "earth" else "base"
            if wk not in self._cat_sent:
                d["book_cat"] = book_catalog(self.g.setting); self._cat_sent.add(wk)
            if "cp" in d or "res" in d or "review" in d:
                d["book"] = self.g.book()
                wp = self.g.world_panel()
                if wp:                                  # the outer world's panel (spec 1 §8), when the engine has a world
                    d["world"] = wp
        return d

    def _on_name(self, line):
        self.custom["name"] = line[:24] or char_name()
        self.custom["seed"] = random.randrange(1, 10 ** 6)
        return self._begin()

    def _on_custom(self, line):
        key = CUSTOM_STEPS[self.step][0]
        c = self.custom
        if key == "name":
            c["name"] = line[:24] or None              # a random name waits for the sex at birth (N1d §4)
        elif key == "sex":
            c["sex"] = {"1": "female", "2": "male", "3": "intersex"}.get(line)
            if not c.get("name"):
                c["name"] = char_name(c["sex"])
        elif key == "setting":
            c["setting"] = {"1": "earth", "2": "tribal", "3": "magic"}.get(line, "earth")
            c["place"] = WORLD[c["setting"]]["places"][0]
            c["earlier"] = None
            if c["setting"] != "earth":
                self.step += 3                      # the outer world is Earth's: no world steps
            elif self.earlier_meta is None:
                self.step += 1                      # no earlier world in this browser
        elif key == "earlier":
            m = self.earlier_meta
            if line in ("2", "3") and m:
                c["earlier"] = dict(key=m.get("key"), name=m.get("name", ""), grandchild=line == "3" and legacy_ok())
                self.step += 2                      # an earlier world keeps its own times and technology
            else:
                c["earlier"] = None
        elif key == "times":
            c["pace"] = {"1": 0.5, "2": 1.0, "3": 1.5, "4": 2.0}.get(line, 1.0)
        elif key == "tech":
            c["tech"] = {"1": "behind", "2": "modern", "3": "ahead"}.get(line, "modern")
        elif key == "world":
            c["world"] = {"1": "questions", "2": "neutral", "3": "pie"}.get(line, "questions")
        elif key == "society":
            c["society"] = letters_to_spec(line)
        elif key == "wealth":
            c["wealth"] = {"1": 0.08, "2": 0.3, "3": 0.55, "4": 0.85}.get(line, 0.3)
        elif key == "faith":
            c["faith"] = {"1": "none", "2": None, "3": "ask"}.get(line, None)
            if c["faith"] != "ask":
                self.step += 1                      # skip the colors question
        elif key == "faith_cols":
            c["faith"] = letters_to_spec(line) or None
        elif key == "upbringing":
            c["upbringing"] = letters_to_spec(line)
        elif key == "start_age":
            try:
                c["start_age"] = float(min(60, max(0, float(line or 0))))
            except ValueError:
                self.note = "Please give an age from 0 to 60."
                return "Please type an age from 0 to 60.", False
        elif key == "seed":
            c["seed"] = int(line) if line.isdigit() else random.randrange(1, 10 ** 6)
        self.step += 1
        if self.step < len(CUSTOM_STEPS):
            return CUSTOM_STEPS[self.step][1].replace("{name}", (self.earlier_meta or {}).get("name", "") or "an earlier life"), False
        return self._begin()

    def _begin(self):
        c = self.custom
        self.inputs = []
        if c.get("faith") == "ask":
            c["faith"] = None
        try:
            self.g = Game(**c, earlier_data=self.earlier_data if c.get("earlier") else None)
        except ValueError as e:
            self.mode = "menu"; self.note = str(e)[:1].upper() + str(e)[1:]
            return self.note + ".", False
        self.mode = "play"
        world = WORLDS[c["world"]][0]
        head = [self.g.story.birth(c.get("blurb", "")), "",
                f"Setting: {SETTINGS[self.g.setting]['title']}. Outlook: {world}. Seed {c['seed']}."]
        self.feed.append(dict(tag="birth", text=head[0], age=0.0, setting=SETTINGS[self.g.setting]["title"], outlook=world,
                              seed=c["seed"], start=c["start_age"]))
        if c.get("society"):
            head.append(f"Their society rewards {letters(np.array(_spec(c['society'])))} ways of acting.")
        if c.get("upbringing"):
            head.append(f"The family raises them toward {letters(np.array(_spec(c['upbringing'])))}.")
        if c["start_age"] > 0:
            head.append(f"Their first {c['start_age']:g} years are lived without you; then you take over.")
            self.job = dict(kind="past")
        else:
            head.append("Press Enter to watch them grow. Type h for the keys.")
            return "\n".join(head), False
        return "\n".join(head), True

    # ------------------------------------------------------------------ play
    def _on_play(self, line):
        g = self.g
        k = line.lower()
        if self.plan is not None or k == "p" or k.startswith("plan "):
            return self._on_plan(line)
        if g.pending is not None:
            if k == "s":
                return g.status(), False
            if k == "h":
                return HELP, False
            if k in ("f", "v", "n", "l"):
                return self._keys(k)
            if k == "i":
                return self._foresee(), False
            if k == "":
                g.decide(None)
                self.job = dict(kind="run", until_cp=True)
                return "", True
            if k.isdigit() and int(k) in self.numbering:
                g.decide(self.numbering[int(k)])
                self.job = dict(kind="run", until_cp=True)
                return "", True
            return "Press Enter to let them choose, or a number to push them.", False
        if k.startswith("=") and isinstance(g.resolution, dict) and g.resolution.get("rename"):
            new = line.strip()[1:].strip() or g.resolution["rename"]["suggest"]   # N1d §4: a new name when they name their gender
            g.rename(new)
            return f"From now on, {g.name}.", False
        if k in ("", "w", "m", "y", "d"):
            g.resolution = None                     # going on: what came of the last choice stays in the story
        if k == "":
            self.job = dict(kind="run", until_cp=True); return "", True
        if k in ("w", "m", "y", "d"):
            weeks = dict(w=1, m=4, y=52, d=520)[k]
            self.job = dict(kind="run", until_cp=True, stop=g.t + weeks); return "", True
        if k == "s":
            return g.status(), False
        if k == "h":
            return HELP, False
        if k in ("f", "v", "n", "l"):
            return self._keys(k)
        return "Unknown key. Type h for help.", False

    def _on_plan(self, line):
        """Key p: the character's dreams, passions and plans, and a plan the player sets (engine v7 foresee.py).
        Browser shortcut: 'plan <horizon> <domain or letters>' previews in one line, 'plan ok' makes it."""
        g = self.g; k = line.strip().lower()
        if k in ("x", "q") or (k == "p" and self.plan is not None):
            self.plan = None; self.note = "No plan made."
            return "No plan made.", False
        if k.startswith("plan "):
            parts = k.split()
            if parts[1] == "ok" and self.plan and self.plan.get("preview"):
                k = ""
            elif parts[1] == "drop" and len(parts) > 2 and parts[2].isdigit():
                ok = g.plan_drop(int(parts[2])); self.plan = None
                self.note = "Plan dropped." if ok else "No such plan."
                return self.note, False
            elif parts[1] in PLAN_HZ_KEY:
                self.plan = dict(step="what", horizon=PLAN_HZ_KEY[parts[1]], domain=None, mix=None, preview=None)
                if len(parts) > 2:
                    return self._on_plan(parts[2])
                return self._plan_text(), False
        if self.plan is None:
            self.plan = dict(step="horizon", horizon=None, domain=None, mix=None, preview=None)
            return self._plan_text(), False
        p = self.plan
        if p["step"] == "horizon":
            if k.startswith("d") and k[1:].isdigit():
                gl = [x for x in g.goals() if x["kind"] == "plan"]
                i = int(k[1:]) - 1
                if 0 <= i < len(gl):
                    g.plan_drop(gl[i]["j"]); self.plan = None
                    self.note = f"{g.name} lets the plan go."
                    return f"{g.name} lets the plan to {gl[i]['name']} go. It costs what was put into it.", False
            hz = {"1": "year", "2": "five years", "3": "life"}.get(k)
            if hz is None:
                return self._plan_text(), False
            p.update(step="what", horizon=hz)
            return self._plan_text(), False
        if p["step"] == "what":
            dom = PLAN_DOM_KEY.get(k)
            mix = [1.0 if c in k.upper() else 0.0 for c in COLORS] if dom is None and any(c in k.upper() for c in COLORS) else None
            if dom is None and not mix:
                return self._plan_text(), False
            pv = g.plan_preview(p["horizon"], dom, mix or None)
            if pv is None:
                self.plan = None
                return "Plans come with engine v7.", False
            p.update(step="confirm", domain=dom, mix=mix or None, preview=pv)
            return self._plan_text(), False
        if p["step"] == "confirm":
            if k in ("", "y", "ok"):
                if p["preview"].get("blocked"):
                    self.plan = None
                    return p["preview"]["blocked"] + ".", False
                j, f = g.plan_add(p["horizon"], p["domain"], p["mix"])
                self.plan = None
                if j < 0:
                    self.note = f
                    return f"No plan made: {f}.", False
                self.note = "Plan made"
                return (f"{g.name} now holds the plan to {p['preview']['name']} ({p['horizon']}). "
                        f"They feel it will work {_fp(f['felt'])} of the time; plans like it come true {f['hint']}."), False
            return self._plan_text(), False
        return self._plan_text(), False

    def _plan_text(self):
        g = self.g; p = self.plan
        L = []
        if p["step"] == "horizon":
            gl = g.goals()
            if gl:
                L.append(f"What {g.name} holds now:")
                n_ = 0
                for x in gl:
                    if x["kind"] == "plan":
                        n_ += 1
                        L.append(f"  d{n_}  plan: {x['name']} ({x['horizon']}, due at {x['due']:.0f}; feels {_fp(x['felt'])}, "
                                 f"plans like it come true {x['hint']}; {x['progress'] * 100:.0f}% of the way)"
                                 + (" [yours]" if x["by_player"] else ""))
                    else:
                        L.append(f"      {x['kind']}: {x['name']} [{x['colors']}], strength {x['strength']:.2f}")
            else:
                L.append(f"{g.name} holds no dreams or plans yet.")
            L.append("Make a plan for them, within:  1 a year  2 five years  3 a lifetime" + ("  · d1, d2..: drop a plan" if any(x["kind"] == "plan" for x in gl) else "") + "  · x: cancel")
        elif p["step"] == "what":
            L.append("A plan to:  1 find work that is theirs  2 find a partner  3 have a child  4 find their people  5 find a faith")
            L.append("  or type color letters for a pursuit in those ways (e.g. U, RG)  · x: cancel")
        else:
            pv = p["preview"]
            if pv.get("blocked"):
                L.append(pv["blocked"] + ". Press x, or Enter.")
            else:
                L.append(f"The plan to {pv['name']}, {p['horizon']} (due at {pv['due_age']:.0f}).")
                L.append(f"{g.name} feels it would work {_fp(pv['felt'])} of the time. Plans like it come true {pv['hint']}.")
                if pv["left_out"]:
                    L.append("What the feeling leaves out: " + ", ".join(pv["left_out"]) + ".")
                L.append(f"Fit with who they are: {pv['fit']:+.2f}. Enter: make the plan · x: cancel")
        return "\n".join(L)

    def _keys(self, k):
        g = self.g
        if k == "n":
            self.mode = "menu"; self.g = None; return self._menu(), False
        if k == "f":
            order = list(FREQ)
            g.freq = order[(order.index(g.freq) + 1) % len(order)]
            self.note = f"Checkpoints: {g.freq}"
            return f"Checkpoints now come: {g.freq}.", False
        if k == "l":
            g.ledger = not g.ledger
            self.note = "Ledger " + ("on" if g.ledger else "off")
            return "Ledger " + ("on: the numbers follow the story." if g.ledger else "off: the story alone."), False
        g.detail = (g.detail + 1) % 3
        self.note = "Story: " + ["quiet", "normal", "every week"][g.detail]
        return "The story now tells: " + ["only checkpoints and life events (quiet)", "also big moments and notable events (normal)",
                                          "every week (everything)"][g.detail] + ".", False

    def _work(self):
        g = self.g; job = self.job
        if job["kind"] == "past":
            stop = job.get("stop")
            st = g.advance(weeks=CHUNK if stop is None else max(0, min(CHUNK, stop - g.t)), until_checkpoint=False, until_age=g.start_age)
            out = self._flush()
            if g.over:
                return out + "\n" + self._review(), self._end()
            if stop is not None and g.t >= stop:
                self.job = None
                return out, False
            if g.age() >= g.start_age:
                self.job = None
                return out + "\n\n" + g.status() + "\n\nPress Enter to go on. Type h for the keys.", False
            return out, True
        stop = job.get("stop")
        weeks = CHUNK if stop is None else max(0, min(CHUNK, stop - g.t))
        st = g.advance(weeks=weeks, until_checkpoint=True)
        out = self._flush()
        if st == "over":
            self.job = None
            return out + "\n" + self._review(), self._end()
        if st == "checkpoint":
            self.job = None
            return (out + "\n" if out else "") + self._checkpoint(), False
        if st == "resolved":
            self.job = None
            return (out + "\n" if out else "") + self._resolved(), False
        if stop is not None and g.t >= stop:
            self.job = None
            return out + f"\n(age {g.age():.1f})", False
        return out, True

    def _end(self):
        self.mode = "over"; self.job = None
        return False

    def _flush(self):
        g = self.g
        out = "\n".join(g.log); g.log.clear()
        return out

    # ------------------------------------------------------------------ rendering
    def _checkpoint(self):
        g = self.g; cp = g.pending
        stake = "very high" if cp["stakes"] >= 1.2 else "high" if cp["stakes"] >= 0.95 else "moderate"
        L = ["", f"== CHECKPOINT · age {cp['age']:.1f} · {cp['title']} (stakes {stake}) =="]
        if cp.get("scene"):
            L.append(cp["scene"])
        if cp["extra"]:
            L.append(cp["extra"])
        if cp.get("thought"):
            L.append(cp["thought"])
        v = cp.get("view")
        if v:
            L.append("Inner voice: " + v["line"])
            L.extend("  (" + a_ + ")" for a_ in v["asides"])
        self.numbering = {}
        own = cp["own"]
        for n, o in enumerate(cp["options"], 1):
            self.numbering[n] = o["idx"]
            star = "*" if o["idx"] == own else " "
            ways = f"  [{o['colors']}]" if o["colors"] != "-" else ""
            sides = (" ♥ heart" if v and o["idx"] == v["heart"] else "") + (" ◆ head" if v and o["idx"] == v["head"] else "")
            L.append(f" {n}{star} {o['label']}{ways}{sides}")
            bits = []
            if o["colors"] != "-" and o.get("reality"):
                r_ = o["reality"]
                bits.append(f"feels {_fp(o['felt'])}; reality: {r_['band']}"
                            + (f" ({r_['misread']}" + (f": {r_['why']})" if r_["why"] else ")") if r_["misread"] != "fair" else ""))
            elif o["colors"] != "-":
                bits.append(f"feels {_fp(o['felt'])}, reality looks {o['hint']}")
            if o["idx"] == own:
                bits.append(f"their pick this time ({o['lean'] * 100:.0f}% likely)")
            elif o["status"] == "considered":
                bits.append(f"{o.get('acc') or accept_word(o['rel'])} ({o['lean'] * 100:.0f}% likely to pick it)")
            elif o["status"] == "didn't think of it":
                bits.append(f"hadn't thought of it; {o.get('acc') or accept_word(o['rel'])}")
            else:
                bits.append(f"out of reach ({o['why']}): can be forced, at higher risk")
            if o["commit"]:
                bits.append(f"could start a {o['commit']}")
            if o.get("needs"):                  # titles and perks: what it needs, what helps, what it gives or takes
                bits.append(o["needs"]["line"])
            for x in o["follows"].get("lift", []):   # a lacking need it would feed if it works
                bits.append(f"meets {NEED_SAY[x['need']]} ({x['word']}, {x['level'] * 100:.0f}%): {x['lift']} to satisfaction")
            if o["idx"] != own and o.get("trust", 0.0) and abs(o["trust"]) >= 0.05:
                bits.append(("trusts you" if o["trust"] > 0 else "distrusts you") + " in these colors")
            L.append("     " + "; ".join(bits))
            for fx in o.get("roles_fx", []):
                L.append("     " + fx["line"])
        L.append(f"Enter: let {g.name} choose (*) · a number: push them to it · i: heart, head, what may follow · s: status")
        return "\n".join(L)

    def _resolved(self):
        """What came of the choice just made (engine v7 explain.after, in the story's words)."""
        r = self.g.resolution
        return "\n".join(["", "~ What came of it ~", r["say"], "Enter: go on"])

    def _foresee(self):
        """What may follow each option (key i at a checkpoint), as far as the character can foresee it."""
        g = self.g; cp = g.pending
        L = [f"Heart and head on each option (the share each would give it, choosing alone), and what may follow, as {g.name} sees it:"]
        for n, o in enumerate(cp["options"], 1):
            f = o["follows"]
            if o["colors"] == "-":
                L.append(f" {n}  {o['label']}: nothing changes now; wanting and pressure keep building.")
                continue
            good = f["win"] + ([("meets " + " and ".join(f["needs"]))] if f["needs"] else [])
            if f["commit_p"] > 0:
                good.append(f"{o['commit']} starts about {f['commit_p'] * 100:.0f}% of the time")
            good.append(f"draws them toward {o['colors']}")
            bad = f["lose"] + ["stress", f"doubts about {o['colors']} ways"]
            if o["status"] == "out of reach":
                bad.append("forcing it backfires: more stress, some money lost")
            L.append(f" {n}  {o['label']}" + (f"  (costs {' '.join(f['cost'])})" if f["cost"] else ""))
            if o.get("heart") is not None:
                dr = o.get("drivers") or {}
                def why(side):
                    return ", ".join(("for: " if x > 0 else "against: ") + nm for nm, x in dr.get(side, []))
                L.append(f"     heart {o['heart'] * 100:.0f}%" + (f" ({why('heart')})" if dr.get("heart") else "")
                         + f" · head {o['head'] * 100:.0f}%" + (f" ({why('head')})" if dr.get("head") else ""))
            if o.get("helped"):                 # perks that make it likelier to work (titles and perks, Emren 12:05)
                L.append(f"     helped by what {g.name} has: " + ", ".join(f"{h['pred']} (+{h['plus']}%)" for h in o["helped"]))
            if o.get("base") is not None:       # the Library's chance for an ordinary person of these ages
                L.append(f"     most people manage this {base_word(o['base'])}")
            L.append(f"     works (feels {_fp(o['felt'])}): " + ", ".join(good))
            L.append("     fails: " + ", ".join(bad))
            acc = o.get("acc") or accept_word(o["rel"])
            if acc in ("reluctant", "against it") and o["idx"] != cp["own"]:
                L.append(f"     if pushed: {acc}, so weaker effort, strain and pent-up wanting")
        return "\n".join(L)

    def _review(self):
        r = self.g.review
        L = ["", r["epitaph"], "", *([r["story"], ""] if r.get("story") else []), "== LIFE REVIEW ==",
             f"Fulfilment (satisfaction through adulthood): {r['fulfilment']:.2f}",
             f"Serenity (peace through adulthood):         {r['serenity']:.2f}",
             f"Integrity (lived by their own wants):       {r['integrity']:.2f}",
             f"Checkpoints: {r['own']} left to them, {r['forced']} pushed by you"
             + (f" ({r.get('accepted', 0)} they came to accept, {r.get('resented', 0)} they resented)" if r["forced"] else ""),
             f"Ended as: {r['final']}",
             f"Identities lived ({r['paths']}): " + " > ".join(r["path"]),
             "", "Press Enter for a new life."]
        return "\n".join(L)


def _spec(spec):
    from game import mix
    return mix(spec)
