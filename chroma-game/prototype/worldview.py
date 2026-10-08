"""The outer world as the player sees it (the outer world package, chroma-world/, approved by Emren 2026-10-06 10:51):
the world panel of public facts and history, big public events in the story, the named cast by layer, reach by
standing, and the five levers on options.

The engine passes keys and numbers (chroma-game/world-hooks-for-engine.md); every word is written here, so the timeless
rule (Emren 10:42: no year, brand, real country, person or event on screen) and each world's flavour live in one place.
Hidden quantities (pressure, hazards, the odds of what comes next) are never shown (Emren 10:09). Everything is a no-op
until the engine's world lands: game.Game.world_source returns None and the panel, circle and reach stay hidden."""
import hashlib
import re

COLORS = "WUBRG"
CNAME = dict(W="White", U="Blue", B="Black", R="Red", G="Green")

# ---------------------------------------------------------------- names: by world seed and id, so a world always names the same people
FIRST = ["Ada", "Bran", "Cem", "Dara", "Elif", "Femi", "Gale", "Hana", "Idris", "Jun", "Kemal", "Lior", "Maren", "Nadia",
         "Oren", "Pia", "Quinn", "Rosa", "Sami", "Tove", "Umar", "Vera", "Wren", "Yara", "Zeki", "Aylin", "Bo", "Cyra", "Dov",
         "Emre", "Farah", "Galen", "Hugo", "Ines", "Jonah", "Kira", "Leto", "Mika", "Nils", "Odile", "Paz", "Rhea", "Selin",
         "Teo", "Una", "Vik", "Willa", "Yusuf", "Zora", "Alba", "Basil", "Cleo", "Dima", "Esme", "Fen", "Greta", "Hal",
         "Isak", "Joss", "Kaya", "Lenn", "Mona", "Nuri", "Otto", "Petra", "Rumi", "Sven", "Tamsin", "Ugo", "Vida", "Arlo",
         "Beren", "Cansu", "Dex", "Ebba", "Fikri", "Gus", "Hester", "Ilse", "Jory", "Kit", "Lale", "Milo", "Nell", "Oskar",
         "Pell", "Rafe", "Saba", "Tilde", "Ulla", "Vasco", "Wim", "Yuna", "Zev", "Amos", "Bea", "Cato", "Delia", "Eero",
         "Faye", "Gil", "Hedda", "Ivo", "Jana", "Kemi", "Lark", "Mirza", "Noor", "Olek", "Prue", "Remy", "Sanne", "Tarik",
         "Uri", "Valo", "Wilma", "Ximo", "Yves", "Zana", "Anouk", "Bertil", "Corin", "Dilan", "Edda", "Florin", "Gwen",
         "Haldis", "Iben", "Juno", "Koray", "Liv", "Malin", "Niko", "Ona", "Piet", "Riya", "Soren", "Thea", "Ulf", "Vesna"]
FAMILY = ["Ashdown", "Brenner", "Calloway", "Dunmore", "Ellery", "Farrow", "Galbraith", "Hollis", "Ingram", "Jessop",
          "Kestrel", "Lindqvist", "Marlow", "Norrell", "Okafor", "Pemberly", "Quaid", "Rowntree", "Sallow", "Thorne",
          "Underhill", "Varga", "Whitlock", "Yardley", "Zeller", "Amberly", "Blackwood", "Corran", "Delacroix", "Eastwick",
          "Fenwick", "Greaves", "Halloran", "Ivers", "Juniper", "Kalder", "Lorne", "Maddox", "Nesbit", "Orrin", "Pryor",
          "Redfern", "Stroud", "Tamsett", "Vane", "Wexley", "Arden", "Brook", "Castell", "Dorran"]
CLAN = ["of the River", "of the Hill", "of the Long Grass", "of the Ash Wood", "of the Salt Lake", "of the Red Cliff"]
HOUSE = ["of the Tower", "Brightwater", "Ashcombe", "of the Grey Order", "Silverhand", "Thornwall", "Ravensgate", "Duskmere"]
PLACE = {"earth": ["Ashford", "Brennick", "Calder", "Dunmere", "Eastfold", "Fallowfield", "Greystone", "Hollins", "Kingsmere",
                   "Larkhill", "Marbury", "Northwick", "Oakhaven", "Port Elver", "Redmouth", "Saltby", "Thornbury", "Westholm"],
         "tribal": ["the river camp", "the hill settlement", "the longhouses", "the valley camp", "the lake camp", "the forest camp"],
         "magic": ["Ravensgate", "Thornwall", "Brightwater", "Duskmere", "Spirehaven", "Ashcombe", "Greywater", "Highmoor"]}


def _h(*parts):
    return int(hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()[:8], 16)


def person_name(seed, pid, full=False, setting="earth"):
    """A cast member's or public figure's name: the same world seed and id always give the same name."""
    first = FIRST[_h(seed, "first", pid) % len(FIRST)]
    if not full:
        return first
    fam = {"tribal": CLAN, "magic": HOUSE}.get(setting, FAMILY)
    return f"{first} {fam[_h(seed, 'family', pid) % len(fam)]}"


# Earth's towns: each world's 15 localities take 15 different names from HOME (a seeded order), and a neighbour society
# the character emigrates to takes its own from ABROAD (W35-3), so no two places in one country share a name
HOME_EXTRA = ["Wrenhollow", "Pellbridge", "Ambervale", "Stonereach", "Hazelby", "Ferncombe", "Ollerby", "Rookhaven",
              "Millbeck", "Sallowford", "Tarnfield", "Whitlow"]
ABROAD = ["Kessby", "Varnholm", "Eskeby", "Tordal", "Lindmar", "Brekkadal", "Sollvik", "Askerholm", "Frostavik", "Gildmark",
          "Hallow Sound", "Isbern", "Jorvenby", "Kaldvik", "Lunmoor", "Merrowgate", "Nordhaven", "Orrin Bay", "Pellmar",
          "Quillon", "Rastholm", "Skarvik", "Tessmouth", "Ulmby", "Vallen Ford", "Wexmar", "Ystrand", "Zennick", "Amberlund",
          "Birkhaven", "Dravik", "Eldmoor", "Fjellby", "Grimsund", "Harrowmere", "Ivelholm", "Jarnby", "Korvik", "Lyssand",
          "Mornholt", "Nesslund", "Oskarby", "Pinehollow", "Rimby", "Selvaro"]
LOC_SOC = 100           # a locality key: loc + LOC_SOC * society (0 at home, k + 1 in neighbour k)
FIG_SOC = 100000        # a public figure's key, the same way


def loc_key(soc, loc):
    return int(loc) + LOC_SOC * int(soc or 0)


def _order(seed, tag, n):
    return sorted(range(n), key=lambda i: _h(seed, tag, i))


def place_name(seed, lid, setting="earth"):
    P = PLACE.get(setting, PLACE["earth"])
    if setting != "earth":
        return P[_h(seed, "place", lid) % len(P)]
    soc, l = divmod(int(lid), LOC_SOC)
    if soc == 0:
        H = P + HOME_EXTRA
        return H[_order(seed, "towns", len(H))[l % len(H)]]
    return ABROAD[_order(seed, "abroad", len(ABROAD))[(15 * (soc - 1) + l) % len(ABROAD)]]


# ---------------------------------------------------------------- color groups go by Chroma's own names (Emren 20:46, point 16)
def letters_of(mix, floor=0.24):
    """A mix of five shares (or letters) as its leading colors in WUBRG order: [.3,.3,.1,.1,.2] -> 'WU'."""
    if isinstance(mix, str):
        return "".join(c for c in COLORS if c in mix.upper())
    ls = "".join(c for c, x in zip(COLORS, mix) if x >= floor)
    return ls or COLORS[max(range(5), key=lambda i: mix[i])]


def group_name(ls):
    from game import ident_name
    return ident_name(ls)


def era_name(ls):
    """'WU' -> 'the Lawkeeper years' (spec 1: 'when you were 34, in the Lawkeeper years')."""
    n = group_name(ls)
    return "the " + re.sub(r"^The ", "", n) + " years" if n and n != "Still forming" else "these years"


def era_idea(ls):
    try:
        import combos
        return combos.IDEAS[ls][1]
    except Exception:
        return ""


def era_magic(ls):
    try:
        import combos
        return combos.IDEAS[ls][0]
    except Exception:
        return ""


def colors_words(ls):
    return " and ".join(CNAME[c] for c in ls)


# ---------------------------------------------------------------- ages: the panel and the story place everything by the character's age, never a year
def age_at(t, born_t):
    return (t - born_t) / 52


def when(t, born_t, name):
    a = age_at(t, born_t)
    if a < 0:
        y = int(round(-a))
        return f"{y} year{'s' if y != 1 else ''} before {name} was born" if y >= 1 else f"just before {name} was born"
    return f"when {name} was {int(a)}"


# ---------------------------------------------------------------- words for the public record
PHASE = dict(expansion="growing", recession="in recession", slowing="slowing")
SEVERITY = dict(mild="a mild recession", severe="a deep recession", crisis="a financial crisis")
WAR = dict(peace="at peace", abroad="troops abroad", home="war at home")
PANDEMIC_SAY = dict(rising="A new illness is spreading; it is all anyone talks about.", peak="The epidemic is at its height.",
                    waning="The epidemic is waning at last.", none="The epidemic is over.")
PANDEMIC_EVENT = dict(none="the epidemic is over", rising="a new illness spreading", peak="an epidemic at its height",
                      waning="an epidemic waning")      # as a moment on the timeline (a phase ending in none is its end)
PANDEMIC = dict(none="no epidemic", rising="a new illness spreading", peak="an epidemic at its height", waning="an epidemic waning")
LAW_STATE = dict(legal="allowed", restricted="restricted", banned="banned")
# a changed law in the story, in plain words per law and new state (legal, restricted, banned); world_keys.LAW_KEYS
LAW_SAY = {
    "drugs": ("drugs are now legal", "some drugs are now allowed under strict rules", "drugs are now banned"),
    "divorce": ("divorce is now open to anyone who asks", "divorce is now allowed, but hard to get", "divorce is now forbidden"),
    "abortion": ("abortion is now legal", "abortion is now allowed only in narrow cases", "abortion is now banned"),
    "same-sex marriage": ("two men or two women can now marry", "same-sex couples can now register, though not marry",
                          "same-sex unions are now forbidden"),
    "conscription": ("the draft now calls up all of the young", "the draft now calls up only some of the young",
                     "the draft is abolished"),
    "guns": ("guns can now be bought freely", "guns now need a licence", "guns are now banned"),
    "gambling": ("gambling is now legal", "gambling is now allowed in licensed places only", "gambling is now banned"),
    "alcohol": ("alcohol is now sold freely", "alcohol is now sold under strict rules", "alcohol is now banned"),
    "sex work": ("sex work is now legal", "sex work is now tolerated under strict rules", "sex work is now banned"),
    "euthanasia": ("assisted dying is now legal", "assisted dying is now allowed in narrow cases", "assisted dying is now banned"),
    "home schooling": ("families may now teach their children at home", "home schooling is now allowed, with inspections",
                       "home schooling is now banned"),
    "death penalty": ("courts may now sentence people to death", "the death penalty now applies only to the worst crimes",
                      "the death penalty is abolished"),
    "adoption": ("adoption is now open to all who can care for a child", "adoption is now allowed only under strict rules",
                 "adoption is now closed"),
}
KIND_WORD = dict(policy="led by the government", institutions="led by the great institutions", cosmology="led by belief")
# event kinds -> (icon, panel words); {x} are the record's values
EVENT = {
    "era": ("ci-domain-era", "{era} begin"),
    "era_end": ("ci-domain-era", "{era} end"),
    "recession": ("ci-chart-falling", "{severity} declared"),
    "recession_over": ("ci-chart", "the recession is over"),
    "election": ("ci-placard", "{a_gov} {gov} government is elected"),
    "gov_falls": ("ci-placard", "the government falls"),
    "law": ("ci-gavel", "{law}: {state}"),
    "right": ("ci-scales", "{right}: {change}"),
    "war": ("ci-swords", "{war}"),
    "war_end": ("ci-swords", "the war ends"),
    "disaster": ("ci-storm", "{disaster}{at}"),
    "pandemic": ("ci-first-aid", "{pandemic}"),
    "revolution": ("ci-fist", "a revolution"),
    "revival": ("ci-sparkle", "a revival of faith"),
    "tech": ("ci-lightbulb", "{tech} spreads"),
    "figure_rise": ("ci-figure-rising", "{figure} rises"),
    "figure_fall": ("ci-figure-falling", "{figure} falls"),
    "scandal": ("ci-newspaper", "a scandal around {figure}"),
    "figure_death": ("ci-candle", "{figure} dies"),
    "poll": ("ci-talk", "{share} in 100 accept {norm}"),
    "layoffs": ("ci-factory", "layoffs at {inst}"),
    "closure": ("ci-door-shut", "{inst} closes"),
    "inst_scandal": ("ci-newspaper", "a scandal at {inst}"),
    "local_election": ("ci-town-hall", "{place} elects {a_gov} {gov} council"),
    "crime_wave": ("ci-shield", "a wave of crime in {place}"),
    "local_disaster": ("ci-storm", "{disaster} in {place}"),
    "strike": ("ci-fist", "a strike at {inst}"),
    "budget_cut": ("ci-chart-falling", "budget cuts in the public services"),
    "welfare": ("ci-scales", "help for those in need is {up_down}"),
    "regime": ("ci-placard", "the way the country is governed changes"),
    "reform": ("ci-scales", "a time of reform"),
    "restoration": ("ci-placard", "the old ways are restored"),
    "refugees": ("ci-crowd", "people fleeing a war abroad arrive"),
    "price_shock": ("ci-chart-falling", "{price} prices jump"),
    "world_recession": ("ci-chart-falling", "a recession abroad"),
    "self_head": ("ci-sealed-scroll", "{name} becomes head of government"),
    "self_left": ("ci-placard", "{name} leaves office"),
}
# the timeline keeps what a person follows: big events, the country's own news (whatever its size), and local news only
# from the places the character has lived; the newest HIST_MAX entries
NATIONAL = {"era", "era_end", "recession", "recession_over", "election", "gov_falls", "law", "right", "war", "war_end",
            "pandemic", "revolution", "revival", "tech", "regime", "reform", "restoration", "welfare", "world_recession",
            "refugees", "price_shock", "budget_cut", "self_head", "self_left"}
HIST_MAX = 300
# a local event in the character's own place or institution, and one where their people live or work (WL.story)
PLACE_KINDS = {"disaster", "local_disaster", "crime_wave", "local_election"}
INST_KINDS_SEEN = {"inst_scandal", "strike", "closure", "layoffs"}
SELF_TAIL = {"disaster": " {N} lives through it.", "local_disaster": " {N} lives through it.",
             "crime_wave": " These are {N}'s own streets.", "local_election": "",
             "inst_scandal": " It is where {N} spends their days.", "strike": " It is where {N} spends their days.",
             "closure": " It is where {N} spends their days.", "layoffs": " It is where {N} spends their days."}
# an institution's news in the character's own place of school, work, service or faith, and where their people are
INST_SELF = {"school": " It is {N}'s own school.", "university": " It is {N}'s own university.", "army": " It is {N}'s own unit.",
             "prison": " {N} is held there.", "faith body": " It is {N}'s own congregation.", "party": " It is {N}'s own party.",
             "union": " It is {N}'s own union.",
             **{k_: " It is where {N} works." for k_ in ("employer", "bank", "media", "charity", "ministry", "council", "police", "court")}}
INST_TOUCH = {"school": "goes", "university": "studies", "army": "serves", "prison": "is held", "faith body": "worships",
              "party": "is a member", "union": "is a member"}
INST_WORD = dict(school="the school", university="the university", employer="the firm", factory="the factory", hospital="the hospital",
                 court="the court", party="the party", media="the paper", faith="the congregation", police="the police",
                 council="the council", bank="the bank", shop="the shop", office="the office",
                 **{"faith body": "the congregation", "army": "the army", "prison": "the prison", "union": "the union",
                    "charity": "the charity", "ministry": "the ministry"})
SOCIETY = ["Varnland", "Oster Reach", "the Southern Union", "Kaldmark", "the Isles of Merrow", "Tessary"]
STATUS_WORD = dict(citizen="a citizen", resident="a resident", migrant="a newcomer without papers yet")
# the same events told in the story (modern Earth; the other worlds share them until they get their own words)
STORY = {
    "era": ["The times are turning: {era} begin."],
    "election": ["Election night: {a_gov} {gov} government wins{led}."],
    "gov_falls": ["The government falls, and the country holds its breath."],
    "recession": ["It is official now: {severity}.", "The news says it plainly: {severity}."],
    "recession_over": ["The recession is over, the news says, though not everyone feels it yet."],
    "law": ["A new law: {law_say}."],
    "right": ["{right}: a right {change}."],
    "war": ["War: {war}."],
    "war_end": ["The war ends."],
    "disaster": ["{disaster} hits {where}."],
    "pandemic": ["{pandemic_say}"],
    "revolution": ["A revolution: the old order falls in the streets."],
    "revival": ["A revival of faith sweeps the country; the squares fill with the faithful."],
    "tech": ["{tech} is everywhere now."],
    "figure_death": ["{figure} dies, and the whole country talks of it."],
    "scandal": ["A scandal: {figure} is in every headline."],
}
ROLE_WORD = dict(head="head of government", opposition="leader of the opposition", **{"head of government": "head of government",
                 "opposition leader": "leader of the opposition"}, star="a star", athlete="an athlete",
                 preacher="a preacher", scientist="a scientist", magnate="a business magnate", activist="an activist")


def key_words(key, table=None):
    """A law, norm, right, technology or disaster key in words: from the engine's or the Library's table when it has
    one, else the key itself with spaces."""
    if table and key in table:
        return table[key]
    return str(key).replace("_", " ")


class WorldView:
    """Turns the engine's world data (see world-hooks-for-engine.md) into the panel, story lines, circle and reach."""

    def __init__(self, seed, setting, name, born_t=0, words=None):
        self.seed, self.setting, self.name, self.born_t = seed, setting, name, born_t
        self.words = words or {}                     # optional key -> words tables (laws, norms, rights, tech, disasters)
        self.figures = {}

    def fig(self, fid):
        """A public figure's name. The engine numbers figures 0, 1, 2... as they appear; each takes its seeded name unless
        an earlier figure has it, then the next seeded draw, so no two figures share a name whatever order they are asked in."""
        fid = int(fid)
        if fid < 0:
            return person_name(self.seed, f"fig{fid}", True, self.setting)
        soc, fid = divmod(fid, FIG_SOC)                 # a neighbour society's figures (W35-3) have names of their own
        names = self.__dict__.setdefault("_fig_names" + (str(soc) if soc else ""), [])
        used = self.__dict__.setdefault("_fig_used", set())
        while len(names) <= fid:
            j, k = len(names), 0
            tag = f"fig{j}" if not soc else f"fig{soc}.{j}"
            nm = person_name(self.seed, tag, True, self.setting)
            while nm in used and k < 50:
                k += 1; nm = person_name(self.seed, f"{tag}-{k}", True, self.setting)
            used.add(nm); names.append(nm)
        return names[fid]

    def inst_name(self, rec):
        """An institution in the record: its kind in words, at its place ("the factory in Redmouth")."""
        k = rec.get("inst_kind") or rec.get("inst")
        if k is None:
            return "a big employer"
        w = INST_WORD.get(str(k), "the " + str(k).replace("_", " "))
        return w + (f" in {place_name(self.seed, rec['locality'], self.setting)}" if rec.get("locality") is not None else "")

    def law_say(self, key, state):
        """A changed law as the story tells it: LAW_SAY on Earth, else the world's own word for the law and its state."""
        i = ("legal", "restricted", "banned").index(state) if state in ("legal", "restricted", "banned") else -1
        if not (self.words.get("laws") or {}).get(key) and key in LAW_SAY and i >= 0:
            return LAW_SAY[key][i]
        w = key_words(key, self.words.get("laws"))
        return f"{w} {'are' if w.endswith('s') and not w.endswith('ss') else 'is'} now {LAW_STATE.get(state, state)}"

    def society_name(self, sid):
        return SOCIETY[_h(self.seed, "society", sid) % len(SOCIETY)]

    def fill(self, kind, rec):
        icon, pat = EVENT.get(kind, ("ci-newspaper", kind.replace("_", " ")))
        if kind == "tech":
            icon = TECH_ICON.get(str(rec.get("tech", "")), icon)
        elif kind in ("disaster", "local_disaster"):
            hz = re.sub(r"^an? ", "", str(rec.get("hazard", rec.get("disaster", ""))))
            icon = HAZARD_ICON.get(hz, icon)
        pat = rec.get("_pat", pat)
        v = dict(rec)
        ls = letters_of(rec.get("colors", rec.get("letters", "")) or "W") if (rec.get("colors") or rec.get("letters")) else ""
        v.update(era=era_name(ls) if ls else "new times", gov=re.sub(r"^The ", "", group_name(ls)) if ls else "new",
                 leader=self.fig(rec["leader"]) if rec.get("leader") is not None else "",
                 a_gov="an" if ls and re.sub(r"^The ", "", group_name(ls))[:1] in "AEIOU" else "a",
                 severity=SEVERITY.get(rec.get("severity", ""), "a recession"),
                 law=key_words(rec.get("law", ""), self.words.get("laws")), state=LAW_STATE.get(rec.get("state", ""), rec.get("state", "")),
                 law_say=self.law_say(rec.get("law", ""), rec.get("state", "")),
                 right=key_words(rec.get("right", ""), self.words.get("rights")),
                 change="gained" if rec.get("gained", rec.get("level", 1) > 0.5) else "lost",
                 war=WAR.get(rec.get("war", ""), "war"), pandemic=PANDEMIC_EVENT.get(rec.get("phase", ""), "an epidemic"),
                 disaster=key_words(rec.get("disaster", "a disaster"), self.words.get("disasters")),
                 where=place_name(self.seed, rec["locality"], self.setting) if rec.get("locality") is not None else "the country",
                 pandemic_say=PANDEMIC_SAY.get(rec.get("phase", ""), "An epidemic."),
                 at=f" in {place_name(self.seed, rec['locality'], self.setting)}" if rec.get("locality") is not None else "",
                 tech=key_words(rec.get("tech", "a new kind of machine"), self.words.get("tech")),
                 figure=self.fig(rec.get("figure", -1)), led=f", led by {self.fig(rec['leader'])}" if rec.get("leader") is not None else "", share=int(round(100 * float(rec.get("share", 0)))),
                 norm=key_words(rec.get("norm", ""), self.words.get("norms")),
                 place=place_name(self.seed, rec["locality"], self.setting) if rec.get("locality") is not None else "the town",
                 inst=self.inst_name(rec), up_down="raised" if rec.get("up", True) else "cut",
                 price={"energy": "energy", "food": "food"}.get(str(rec.get("price", "")), "energy"), name=self.name)
        text = re.sub(r"\{(\w+)\}", lambda m: str(v.get(m.group(1), "")), pat)
        return icon, text[:1].upper() + text[1:]

    # ---------------------------------------------------------------- the world panel (spec 1 §8, spec 5 §4)
    def panel(self, snap, record, age_now):
        """What is publicly true now and what has happened, placed by the character's age and era."""
        for f in snap.get("figures", []):
            self.figures[f["id"]] = dict(f, name=self.fig(f["id"]))
        era = snap.get("era") or {}
        els = letters_of(era.get("colors", era.get("letters", ""))) if era else ""
        out = dict(name=self.name, age=round(age_now, 1))
        if els:
            out["era"] = dict(letters=els, name=era_name(els), idea=era_idea(els), magic=era_magic(els),
                              kind=KIND_WORD.get(era.get("kind", ""), ""), since=round(age_at(era.get("since_t", 0), self.born_t), 1))
        e = snap.get("econ") or snap.get("economy") or {}
        if e:
            out["econ"] = dict(phase=PHASE.get(e.get("phase_published", e.get("phase", "")), "steady"),
                               unemp=round(float(e.get("unemp") or 0), 1), infl=round(float(e.get("infl") or 0), 1),
                               housing=("homes dearer than ever" if (e.get("housing") or 0) > 0.4 else "homes dear" if (e.get("housing") or 0) > 0.1
                                        else "homes cheaper than they were" if (e.get("housing") or 0) < -0.2 else "homes about as dear as usual"))
        gv = snap.get("gov") or (snap.get("state") or {}).get("gov") or {}
        if gv:
            gl = letters_of(gv.get("colors", "W"))
            out["gov"] = dict(letters=gl, name=group_name(gl), leader=self.name if gv.get("leader_self") else
                              self.fig(gv.get("leader", -1)) if gv.get("leader") is not None else "",
                              support=int(round(100 * float(gv.get("support", 0)))),
                              next_age=round(age_at(gv["next_election_t"], self.born_t), 1) if gv.get("next_election_t") is not None else None)
        out["state"] = dict(war=WAR.get(snap.get("war", "peace"), ""), pandemic=PANDEMIC.get(snap.get("pandemic", "none"), ""))
        if snap.get("season"):
            out["season"] = snap["season"]
        pl = snap.get("place") or {}
        if pl:                                       # where they live; abroad, their standing there and the language
            home = pl.get("society", 0) in (None, pl.get("home_society", 0))
            out["place"] = dict(name=place_name(self.seed, pl.get("locality", 0), self.setting), kind=str(pl.get("kind", "")).replace("_", " "),
                                abroad=not home, society=None if home else self.society_name(pl["society"]),
                                status=STATUS_WORD.get(pl.get("status", ""), "") if not home else "",
                                language=("fluent" if pl.get("language", 1) > 0.8 else "getting by" if pl.get("language", 1) > 0.4 else "a few words") if not home else "")
        out["laws"] = [dict(word=key_words(k, self.words.get("laws")), state=LAW_STATE.get(s_, s_)) for k, s_ in sorted((snap.get("laws") or {}).items())]
        out["rights"] = [dict(word=key_words(k, self.words.get("rights")), level=float(v)) for k, v in sorted((snap.get("rights") or {}).items())]
        out["figures"] = [dict(id=f["id"], name=self.figures[f["id"]]["name"], role=ROLE_WORD.get(f.get("role", ""), f.get("role", "")),
                               letters=letters_of(f["read"]) if f.get("read") is not None else "", alive=bool(f.get("alive", True)),
                               standing=int(f.get("standing", 2))) for f in snap.get("figures", [])]
        # history: big events and public announcements, newest first; polls kept only as the latest per norm
        hist, polls, series, eras = [], {}, [], []
        pl0 = snap.get("place") or {}
        lived = set(pl0.get("lived") or ()) | {pl0.get("locality")}
        for r in sorted(record, key=lambda x: x["t"]):
            a = round(age_at(r["t"], self.born_t), 1)
            k = r["kind"]
            if k == "poll":
                polls[r.get("norm", "")] = dict(age=a, word=key_words(r.get("norm", ""), self.words.get("norms")), share=int(round(100 * float(r.get("share", 0)))))
                continue
            if k == "figures":                       # quarterly published figures: the unemployment line
                series.append([a, round(float(r.get("unemp", 0)), 1)])
                continue
            if k == "era":
                ls = letters_of(r.get("colors", r.get("letters", "W")))
                if eras:
                    eras[-1]["to"] = a
                eras.append(dict(letters=ls, name=era_name(ls), **{"from": a, "to": None}))
            if r.get("locality") is not None and r["locality"] not in lived:
                continue
            if not (r.get("big") or k in NATIONAL or r.get("locality") is not None):
                continue                             # someone else's town, a small institutional matter: not on the timeline
            icon, text = self.fill(k, r)
            hist.append(dict(age=a, kind=k, icon=icon, text=text, big=bool(r.get("big", False))))
        out["history"] = hist[::-1][:HIST_MAX]
        out["polls"] = sorted(polls.values(), key=lambda x: -x["age"])
        out["series"] = series[-400:]
        out["eras"] = eras
        return out

    # ---------------------------------------------------------------- the world in the story (spec 1 §8: big events always; the rest when they touch)
    def line(self, rec, cast_names=None):
        """A world event as a story line, or None when it neither is big nor touches the character or their people."""
        touches = [i for i in rec.get("touches", []) if cast_names and i in cast_names]
        if not (rec.get("big") or rec.get("self") or touches):
            return None
        icon, text = self.fill(rec["kind"], rec)
        pat = STORY.get(rec["kind"])
        if pat:
            _, text = self.fill(rec["kind"], dict(rec, _pat=pat[_h(self.seed, rec["t"], rec["kind"]) % len(pat)]))
        text = text.rstrip(".")
        tail, k = "", rec["kind"]
        ik = str(rec.get("inst_kind", ""))
        if rec.get("self"):
            tail = INST_SELF.get(ik, SELF_TAIL[k]) if k in INST_KINDS_SEEN else SELF_TAIL.get(k, " It reaches {N}'s own life.")
        elif touches:
            who = " and ".join(cast_names[i].rstrip(",") if j < len(touches[:2]) - 1 else cast_names[i] for j, i in enumerate(touches[:2]))
            one = len(touches[:2]) == 1
            if k in INST_KINDS_SEEN:
                v_ = INST_TOUCH.get(ik, "works")
                v_ = v_ if one else {"goes": "go", "studies": "study", "serves": "serve", "is held": "are held", "worships": "worship",
                                     "is a member": "are members", "works": "work"}[v_]
                tail = f" {who} {v_} there." if "member" not in v_ else f" {who} {v_}."
            else:
                tail = f" {who} {'lives' if one else 'live'} there." if k in PLACE_KINDS else f" It touches {who}."
        return icon, text + "." + (tail[:2].upper() + tail[2:] if tail[:1] == " " else tail)

    # ---------------------------------------------------------------- the named cast by layer (spec 2 §8)
    def circle(self, cast, t_now=None, names=None):
        LAYER = {1: "Support", 2: "Sympathy", 3: "Friends", 4: "Known"}
        out = []
        KIN = {"partner", "parent", "child", "sibling", "grandparent", "grandchild"}
        for p in cast:
            lay = int(p.get("layer", 4))
            dead_close = not p.get("alive", True) and (lay in (1, 2) or KIN & set(p.get("roles", [])))
            if not dead_close and (lay < 1 or lay > 4 or not p.get("alive", True)):
                continue                             # faces (layer 0) never; the dead only when they were close or kin
            c, tr = float(p.get("closeness", 0)), float(p.get("trust", 0))
            out.append(dict(id=p["id"], name=(names or {}).get(p["id"]) or person_name(self.seed, p["id"], False, self.setting), layer=int(p.get("layer", 4)),
                            layer_name=LAYER.get(int(p.get("layer", 4)), "Faces"), roles=list(p.get("roles", [])),
                            read=letters_of(p["read"]) if p.get("read") is not None else "",
                            close=("very close" if c > 0.75 else "close" if c > 0.5 else "friendly" if c > 0.25 else "distant"),
                            trust=("trusted completely" if tr > 0.8 else "trusted" if tr > 0.55 else "half trusted" if tr > 0.3 else "not trusted"),
                            want=p.get("want_word") or (str(p["want"]).replace("_", " ") if p.get("want") else ""),
                            alive=bool(p.get("alive", True)),
                            age=int(age_at(t_now, p["born_t"])) if t_now is not None and p.get("born_t") is not None else None))
        return sorted(out, key=lambda x: (x["layer"], x["name"]))

    # ---------------------------------------------------------------- reach by standing (spec 7 §2, §6): felt, reality only as a hint
    def reach(self, standing):
        """Standing and felt reach per ring (spec 7 §2). The engine's keys are its `pushes:` domains (close, group, place,
        institution, state, economy, culture, tech, ...); a ring shows the most the character has in any of its domains."""
        RING = [("close", "Close circle", "ci-hug", ("close",)), ("place", "Settings and place", "ci-cottage", ("group", "place")),
                ("inst", "Institutions", "ci-round-table", ("institution", "inst")),
                ("society", "State, economy, culture", "ci-crowd", ("state", "economy", "culture", "tech", "society"))]
        LEVEL = ["one of the crowd", "a little", "clearly", "strongly"]
        out = []
        for k, word, icon, keys in RING:
            have = [standing[x] for x in (k,) + keys if isinstance(standing.get(x), dict)]
            s_ = max(have, key=lambda d: (d.get("standing", 0), d.get("felt", 0))) if have else {}
            out.append(dict(ring=k, word=word, icon=icon, level=int(s_.get("standing", 0)), level_word=LEVEL[int(s_.get("standing", 0))],
                            felt=round(min(1.0, max(0.0, float(s_.get("felt", 0)))), 2), hint=s_.get("hint", "")))
        return out


# ---------------------------------------------------------------- who someone is to the character, for a story line
WHO_ROLE = dict(partner=("their partner",) * 3, ex=("their former partner",) * 3,
                parent=("their mother", "their father", "their parent"), child=("their daughter", "their son", "their child"),
                sibling=("their sister", "their brother", "their sibling"),
                grandparent=("their grandmother", "their grandfather", "their grandparent"),
                grandchild=("their granddaughter", "their grandson", "their grandchild"), inlaw=("their in-law",) * 3,
                kin=("their relative",) * 3, boss=("their boss",) * 3, teacher=("their teacher",) * 3,
                mentor=("their mentor",) * 3, rival=("their rival",) * 3, friend=("their friend",) * 3,
                colleague=("their colleague",) * 3, classmate=("their classmate",) * 3, neighbour=("their neighbour",) * 3)


def who_word(p, name):
    """A cast member as the story names them in a world line: "their friend Cato", or "Cato, someone they know"."""
    for r in p.get("roles", []):
        if r in WHO_ROLE:
            w = WHO_ROLE[r][0 if p.get("sex") == "female" else 1 if p.get("sex") == "male" else 2]
            return f"{w} {name}"
    return f"{name}, someone they know,"


# ---------------------------------------------------------------- the five levers on options (spec 7 §1)
# a technology's or a hazard's own glyph (Visuals, W42: ink-icons.json map.tech and map.hazard); unknown keys keep the
# record kind's glyph
TECH_ICON = {"phone": "ci-phone", "computer": "ci-laptop", "internet": "ci-signal", "video calls": "ci-screen",
             "online dating": "ci-phone-heart", "remote work": "ci-laptop", "ai helper": "ci-chat-spark",
             "modern medicine": "ci-pills", "car": "ci-car", "plane": "ci-plane"}
HAZARD_ICON = {"flood": "ci-flood", "fire": "ci-flame", "wildfire": "ci-flame", "quake": "ci-quake", "earthquake": "ci-quake",
               "storm": "ci-storm", "heat": "ci-sun", "heatwave": "ci-sun"}

LEVERS = dict(exit=("Exit", "leave it", "ci-door-open"), voice=("Voice", "speak up to change it", "ci-megaphone"),
              loyalty=("Loyalty", "stay and invest", "ci-anchor"), neglect=("Neglect", "let it go untended", "ci-shrug"),
              subvert=("Subvert", "work the system", "ci-domino-mask"))
PUSH = dict(none="nothing moves", small="it moves a little", clear="it moves", strong="it moves a great deal")


def lever_info(lever, target=None):
    if lever not in LEVERS:
        return None
    nm, what, icon = LEVERS[lever]
    return dict(lever=lever, name=nm, what=what, icon=icon, target=str(target).replace("_", " ") if target else "")


def push_words(push):
    if not push:
        return None
    return dict(size=push.get("size", "none"), word=PUSH.get(push.get("size", "none"), ""), backfire=bool(push.get("backfire")),
                target=str(push.get("target", "")).replace("_", " "))


# ---------------------------------------------------------------- the engine's outer world (chroma-engine/world.py, world_people.py)
HAZARD_WORD = dict(flood="a flood", fire="a wildfire", quake="an earthquake", storm="a storm", heat="a heatwave")
BREAK_KIND = dict(revolution="revolution", revival="revival", reform="reform", restoration="restoration")
INST_KIND = {"scandal": "inst_scandal", "closure": "closure", "strike": "strike"}      # the rest (rulings, new leaders...) stay off the timeline


def from_engine(e, t0=0, soc=0):
    """One entry of the engine's public record (dict(t, domain, kind, key, value, big), world weeks) as records in the
    panel's shape (test/mock_world.py), with t in the life's weeks (negative before the birth). A list: a norms poll is
    one entry per norm; entries the panel does not show give none."""
    d, k, key = e.get("domain"), e.get("kind"), e.get("key")
    v = e.get("value"); vd = v if isinstance(v, dict) else {}
    r = dict(t=int(e.get("t", 0)) - int(t0), big=bool(e.get("big", False)))
    if vd.get("loc") is not None:
        r["locality"] = loc_key(soc, vd["loc"])
    fk_ = lambda f_: (int(f_) + FIG_SOC * int(soc or 0)) if f_ is not None and int(f_) >= 0 else f_
    out = None
    if d == "era":
        if k == "era begins":
            out = dict(kind="era", letters=str(key or ""), kind_of=vd.get("kind"))
        elif k == "era ends":
            out = dict(kind="era_end", letters=str(key or ""))
        elif k == "breakthrough":
            out = dict(kind=BREAK_KIND.get(str(key), "reform"))
    elif d == "economy":
        if k == "recession declared":
            out = dict(kind="recession", severity=str(key))
        elif k == "recession over":
            out = dict(kind="recession_over")
        elif k == "published" and key == "unemployment":
            out = dict(kind="figures", unemp=float(v or 0))
    elif d == "state":
        if k == "election":
            out = dict(kind="election", colors=vd.get("colors"), leader=fk_(vd.get("leader")))
        elif k == "government falls":
            out = dict(kind="gov_falls")
        elif k == "law changed":
            out = dict(kind="law", law=str(key), state=vd.get("state", ""))
        elif k in ("right gained", "right lost"):
            out = dict(kind="right", right=str(key), gained=k == "right gained")
        elif k == "regime changes":
            out = dict(kind="regime")
        elif k == "head of government" and int(vd.get("life", 0)) == 0:      # W40: the character's own time in office
            out = dict(kind="self_head" if key == "self" else "self_left")
        elif k in ("welfare raised", "welfare cut"):
            out = dict(kind="welfare", up=k == "welfare raised")
    elif d == "culture" and k == "poll" and isinstance(v, dict):
        return [dict(r, kind="poll", norm=str(n_), share=float(s_)) for n_, s_ in v.items()]
    elif d == "abroad":
        if k == "war begins":
            out = dict(kind="war", war=str(key) if key in ("abroad", "home") else "abroad")
        elif k == "war comes home":
            out = dict(kind="war", war="home")
        elif k == "war ends":
            out = dict(kind="war_end")
        elif k == "world recession":
            out = dict(kind="world_recession")
        elif k == "refugees arrive":
            out = dict(kind="refugees")
    elif d == "nature":
        if k == "disaster":
            out = dict(kind="disaster", hazard=str(key), disaster=HAZARD_WORD.get(str(key), "a disaster"))
        elif k == "pandemic":
            out = dict(kind="pandemic", phase=str(key))
        elif k == "price shock":
            out = dict(kind="price_shock", price=str(key))
    elif d == "tech" and k == "arrives":
        out = dict(kind="tech", tech=re.sub(r" \d+$", "", str(key)))
    elif d == "figure":
        fk = {"rises": "figure_rise", "falls": "figure_fall", "scandal": "scandal", "death": "figure_death"}.get(k)
        if fk:
            out = dict(kind=fk, figure=fk_(vd.get("fig", -1)))
    elif d == "place":
        if k == "local election":
            out = dict(kind="local_election")
        elif k == "crime wave":
            out = dict(kind="crime_wave")
    elif d == "institution":
        if k == "budget cut":
            out = dict(kind="budget_cut")
        elif k in INST_KIND:
            out = dict(kind=INST_KIND[k], inst_kind=str(key))
    elif d == "belief" and k == "revival":
        out = dict(kind="revival")
    return [dict(r, **out)] if out else []


REACH_HINT = {0: "next to none", 1: "a little", 2: "some", 3: "a good deal", 4: "a great deal"}   # real reach, in quarters


class EngineWorld:
    """The engine's outer world, read from the week's state (world_link.WorldLink as `WL`, P["world"] on), in the shapes
    the panel, circle and reach read (the same as test/mock_world.py): (snapshot, record, cast, standing). The engine
    passes keys and numbers; every word is the game's (world-hooks-for-engine.md §1). Person 0 is the character."""

    def __init__(self, game):
        self.g = game
        self._rec, self._n = [], 0                      # the public record so far, converted once
        self._w = None                                  # the World read (a neighbour's after emigrating, W35-3)
        self.lived = set()                              # the localities the character has lived in (loc_key)

    @staticmethod
    def soc(WL):
        return int(getattr(WL.W, "society_id", 0) or 0)

    def link(self):
        loc = self.g.loc
        return loc.get("WL") if isinstance(loc, dict) else None

    def record(self, WL):
        R = WL.W.record
        if self._w is not None and WL.W is not self._w:
            self._n = len(R)                            # moved to another society, or back: its news from now on
        self._w = WL.W
        for e in R[self._n:]:
            self._rec.extend(from_engine(e, WL.t0, self.soc(WL)))
        self._n = len(R)
        return self._rec

    def __call__(self, t):
        WL = self.link()
        if WL is None:
            return None
        W, PP, t0 = WL.W, WL.PP, WL.t0
        sn = dict(W.snapshot())
        era = sn.get("era")
        if era:
            sn["era"] = dict(letters=str(era.get("key", "")), kind=era.get("kind"), since_t=int(era.get("since_t", t0)) - t0)
        sc = self.soc(WL); fk_ = lambda f_: int(f_) + FIG_SOC * sc if f_ is not None and int(f_) >= 0 else f_
        gv = sn.get("gov")
        if gv:
            sn["gov"] = dict(gv, next_election_t=int(gv["next_election_t"]) - t0 if gv.get("next_election_t") is not None else None,
                             leader=fk_(gv.get("leader")))
        sn["figures"] = [dict(f, id=fk_(f.get("id")), standing=int(round(3 * min(1.0, float(f.get("standing", 0))))),
                              born_t=int(f.get("born_t", t0)) - t0) for f in sn.get("figures", [])]
        try:
            pl = PP.place_view(0)
            lk = loc_key(pl.get("society", 0), pl.get("loc", 0))
            self.lived.add(lk)
            sn["place"] = dict(locality=lk, kind=pl.get("kind", ""), society=pl.get("society", 0), lived=sorted(self.lived),
                               home_society=pl.get("home_society", 0), status=pl.get("status", ""), language=pl.get("lang", 1))
        except Exception:
            pass
        cast = []
        try:
            for p in PP.cast_view(0, dead=True):
                cast.append(dict(p, born_t=int(t) - 52 * int(p.get("age", 0))))
        except Exception:
            pass
        standing = {}
        try:
            rv = PP.reach_view(0)
            hs = rv.get("hint") or [None] * len(rv["standing"])
            for key, s_, f_, h_ in zip(("close", "place", "inst", "society"), rv["standing"], rv["felt"], hs):
                standing[key] = dict(standing=int(s_), felt=float(f_), hint=REACH_HINT.get(round(float(h_) * 4)) if h_ is not None else "")
        except Exception:
            pass
        return sn, self.record(WL), cast, standing

    def news(self):
        """This week's big public events, as records for the story (spec 1 §8: big public events always)."""
        WL = self.link()
        if WL is None:
            return []
        try:
            pv_ = WL.PP.place_view(0); here = loc_key(pv_.get("society", 0), pv_.get("loc", 0))
        except Exception:
            here = None
        out = []
        for e in getattr(WL, "week_events", None) or []:
            if e.get("big"):
                out.extend(r_ for r_ in from_engine(e, WL.t0, self.soc(WL)) if (r_.get("locality") is None or r_["locality"] == here)
                           and r_["kind"] not in ("self_head", "self_left"))
        return out
