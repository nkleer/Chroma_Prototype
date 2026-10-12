"""Played lives for chroma-engine/tools/roll_once.py (v22.5 row K18: F7 one roll of the living, F10 once means once).
Plays one life of a preset to its end with the engine settings of CHROMA_ENGINE and the game settings of CHROMA_GAME
(both JSON) and writes what the checks count as JSON. RO_LAY names the row's game switches (line_wait, news_touch): one
that GAME still has off is laid on (line_wait 5 years) and listed under "laid".
    python3 -B test/roll_once_game.py <preset> <seed> <f7_roll|f10_once> <out.json>

f7_roll  dead      a line names a person after the week of their death (the story's), except where the story tells of
                   the dead (the death itself, the dead slot of grief and memory, the quiet deaths)
         world     a line names a person the outer world lost 13 weeks or more before (the story should have told it)
         unborn    a line names a child of theirs in a week the engine counts no living child (and the child was not
                   born or taken in that week)
         births    a child's birth told in two different weeks; a birth scene ("a child is born") with no newborn
         partners  a partner's death or split told in a week before which no line had named them
f10_once lines     a line of a kind line_wait holds said again word for word inside line_wait years
         news      national news (not their own place's, a war, a pandemic, a recession) before news_age; the same kind
                   (a government's fall with its election) twice inside news_gap years; a law twice for the same state
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import game, story   # noqa: E402

preset, seed, what, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
LAY_ON = dict(line_wait=5.0, news_touch=True)     # a row's game switch GAME still has off, laid on for the check (RO_LAY;
laid = []                                          # line_wait in years, until the refit sets its own)
for k_ in filter(None, os.environ.get("RO_LAY", "").split(",")):
    if not game.GAME.get(k_):
        game.GAME[k_] = LAY_ON[k_]; laid.append(k_)
PM = re.compile(r"⟦p:(\d+)⟧(.*?)⟦/⟧")
G = None


def now():
    """The week being played: the game's t (advance() plays many weeks before it returns)."""
    return G.t if G is not None else 0
pending = []                    # (week, marker, kind, detail): a naming to look for in the lines said that week
bad = {k: [] for k in ("dead", "world", "unborn", "births", "partners", "lines", "news")}
n = {k: 0 for k in bad}
births = {}                     # serial -> weeks their birth was told
scenes = []                     # weeks of a birth scene
wdead = {}                      # world cast id -> week first seen dead
news = []                       # (week, record) of the national news told
_serial = [0]


def _frames():
    f = sys._getframe(2)
    while f is not None:
        yield f
        f = f.f_back


def _new(self, role, ref, sex=None, _o=story.Story.new):
    p = _o(self, role, ref, sex)
    _serial[0] += 1; p["_k"] = _serial[0]; p["_w0"] = now()
    return p


def _dies(self, p, _o=story.Story.dies):
    if p is not None and p["alive"]:
        p["_wd"] = now()
    return _o(self, p)


def _naming(fn):
    orig = getattr(story.Story, fn)

    def w(self, p, _o=orig):
        mark = _o(self, p)
        if p is None or G is None:
            return mark
        legit = birth = False
        for f in _frames():
            co = f.f_code.co_name
            if co in ("death", "quiet_deaths", "_who_dies", "dies") or (co == "role" and f.f_locals.get("slot") == "dead"):
                legit = True
            if co == "role" and f.f_locals.get("slot") == "child" and (f.f_locals.get("ctx") or {}).get("_birth"):
                birth = True
        if not p["alive"] and p.get("_wd", now()) < now() and not legit:
            pending.append((now(), mark, "dead", f"{p['role']} {p['name']}, dead since {p['_wd'] / 52:.1f}"))
        if p["alive"] and wdead and not legit:
            cid = {v: k for k, v in (getattr(G, "_castname", None) or {}).items()}.get(p["name"])
            if cid in wdead and now() - wdead[cid] >= 13:
                pending.append((now(), mark, "world", f"{p['role']} {p['name']}, dead in the world since {wdead[cid] / 52:.1f}"))
        if p["role"] == "child" and p["alive"] and self.one_roll and self.kids_n == 0 and p.get("_w0") != now():
            pending.append((now(), mark, "unborn", f"child {p['name']} while the engine counts no living child"))
        if birth:
            births.setdefault(p["_k"], set()).add(now())
        return mark
    setattr(story.Story, fn, w)


story.Story.new = _new
story.Story.dies = _dies
_naming("say"); _naming("nm")

_later = story.Story.later_child


def _later_child(self, taken=False):
    line = _later(self, taken)
    if not taken:
        births.setdefault(self.people[-1]["_k"], set()).add(now())
    return line


story.Story.later_child = _later_child
_commit = story.Story._commitment


def _commitment(self, c, m=None, title=None):
    line = _commit(self, c, m, title)
    if line and c.get("kind") == "children" and c.get("what") == "start" and "is born" in story.plain(line):
        for pid, txt in PM.findall(line):
            for p in self.people:
                if p["id"] == int(pid) and p["role"] == "child" and p["name"] in txt:
                    births.setdefault(p["_k"], set()).add(now())
    return line


story.Story._commitment = _commitment
_moment = story.Story.moment


def _moment_w(self, t, sit, stage, age, kind=None, kills=None):
    if sit == "a child is born" and (not scenes or scenes[-1] != now()):
        scenes.append(now())
    return _moment(self, t, sit, stage, age, kind, kills)


story.Story.moment = _moment_w
_say = game.Game._say


def _say_w(self, line, level=0, tag="note", **meta):
    k0 = len(self.feed)
    _say(self, line, level, tag, **meta)
    if len(self.feed) > k0:
        e = self.feed[-1]; e["_t"] = self.t
        pending[:] = [x for x in pending if x[0] == self.t]
        for _, mark, kind, det in pending:
            if mark and mark in e["text"]:
                bad[kind].append(f"{self.t / 52:.1f}: {det}: {story.plain(e['text'])[:160]}")


game.Game._say = _say_w
_wn = game.Game._world_news


def _world_news(self, r):
    k0 = len(self.feed)
    _wn(self, r)
    if len(self.feed) > k0:
        news.append((self.t, dict(r)))


game.Game._world_news = _world_news

role_was = {}; splits = {}; ever_partner = set()
_week = game.Game._on_week


def _on_week(self, t, loc):
    """Each week: a partner who became a former partner (the split's week), and the outer world's dead."""
    for p in self.story.people:
        k = p.get("_k")
        if role_was.get(k) == "partner" and p["role"] in ("ex", "former partner"):
            splits.setdefault(k, t - 1)               # (changed during the week before)
        if p["role"] == "partner":
            ever_partner.add(k)
        role_was[k] = p["role"]
    if t % 4 == 0 and self.story.one_roll:
        wd = self.world_data()
        for c in (wd[2] if wd else []):
            if not c.get("alive") and c["id"] not in wdead:
                wdead[c["id"]] = t
    return _week(self, t, loc)


game.Game._on_week = _on_week
G = game.Game(name="Lale", seed=seed, **{k: v for k, v in game.PRESETS[preset].items() if k not in ("title", "blurb")})
steps = 0
while not G.over and steps < 40000:
    steps += 1
    if G.advance() == "checkpoint":
        G.decide(None)

# ---- after the life
P = G.story.people
by_mark = {}
first_named = {}
for e in G.feed:
    for pid, txt in PM.findall(e["text"]):
        for p in P:
            if p["id"] == int(pid) and p["name"] in txt:
                first_named.setdefault(p["_k"], e["_t"])
G_ = game.GAME
if what == "f7_roll":
    n["dead"] = n["world"] = n["unborn"] = sum(len(PM.findall(e["text"])) for e in G.feed)
    for k, ws in births.items():
        n["births"] += 1
        if max(ws) - min(ws) > 5:
            p = next(q for q in P if q.get("_k") == k)
            bad["births"].append(f"{p['name']}: birth told at {', '.join(f'{w / 52:.1f}' for w in sorted(ws))}")
    for w in scenes:
        n["births"] += 1
        if not any(p["role"] == "child" and w <= p.get("_w0", -1) <= w + 2 for p in P):
            bad["births"].append(f"{w / 52:.1f}: a birth scene with no newborn")
    for p in P:
        k = p.get("_k")
        if k not in ever_partner:
            continue
        n["partners"] += 1
        for ev, w in (("death", p.get("_wd")), ("split", splits.get(k))):
            fn = first_named.get(k)
            if w is not None and fn is not None and fn >= w:
                bad["partners"].append(f"{p['name']} ({p['role']}): {ev} at {w / 52:.1f}, first named {fn / 52:.1f}")
    checks = dict(dead=("lines that name a person after their death", "dead"),
                  world=("lines that name a person the world lost 13 or more weeks before", "world"),
                  unborn=("lines that name a child while the engine counts none", "unborn"),
                  births=("births told twice, or a birth scene with no newborn (births and scenes)", "births"),
                  partners=("partners whose death or split comes before any line named them (partners)", "partners"))
else:
    tags = game.LINE_WAIT_TAGS; lw = float(G_.get("line_wait") or 0) * 52
    said = {}
    for e in G.feed:
        if e["tag"] in tags and e["text"]:
            n["lines"] += 1
            k = story.plain(e["text"])
            if lw and k in said and e["_t"] - said[k] < lw:
                bad["lines"].append(f"{e['_t'] / 52:.1f}: said at {said[k] / 52:.1f} too: {k[:120]}")
            said[k] = e["_t"]
    last, laws = {}, {}
    gap = float(G_.get("news_gap") or 0) * 52; age0 = float(G_.get("news_age") or 0)
    for t, r in news:
        k_ = r["kind"]
        if r.get("locality") is not None or k_ in game.NEWS_ALL:
            continue
        n["news"] += 1
        if t / 52 < age0:
            bad["news"].append(f"{t / 52:.1f}: {k_} told before {age0:g}")
        if k_ == "law":
            key = (r.get("law"), r.get("state"))
            if key in laws:
                bad["news"].append(f"{t / 52:.1f}: the law {r.get('law')} told again for the same state (first {laws[key] / 52:.1f})")
            laws[key] = t
            continue
        g_ = "government" if k_ in ("gov_falls", "election") else k_
        if g_ in last and t - last[g_] < gap:
            bad["news"].append(f"{t / 52:.1f}: {g_} told again inside {gap / 52:g} years (last {last[g_] / 52:.1f})")
        last[g_] = t
    checks = dict(lines=(f"lines said again word for word inside line_wait ({G_.get('line_wait')} years; lines of its kinds)", "lines"),
                  news=(f"national news before news_age ({G_.get('news_age')}) or again inside news_gap "
                        f"({G_.get('news_gap')} years) (national news told)", "news"))
res = dict(preset=preset, seed=seed, age=round(G.age(), 1), lines=len(G.feed), one_roll=G.story.one_roll, laid=laid,
           game={k: G_.get(k) for k in ("line_wait", "news_touch", "news_age", "news_gap")},
           checks={k: dict(what=w, n=n[b], bad=bad[b][:20]) for k, (w, b) in checks.items()})
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res)[:2000])
