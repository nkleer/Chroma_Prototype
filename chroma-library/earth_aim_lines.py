"""Aims v2 (Emren's decision #9 with its three selected parts; chroma-engine/notes/v25/aims-shape.md sections 3, 5
and 6; contracts.md sections 5 and 6, 10-23): the words the Game fills in for an aim's forks, previews, agenda states,
bottlenecks, funding and upkeep.

DRAFT for v25 (Library). Plain data, hand-written, no imports. Read only with the Engine's aims_v2 switch on; the Game
shows these in the agenda, the fork card, the preview and the agenda review. Third person, present tense, with {N}
(the character) and {Ns} (their possessive), or impersonal. Every entry that holds lines is a list; the Game picks one
(by the life's seed, as elsewhere) unless the table says the order means something. The Game capitalises the first
letter of a line, so a line may start with a lower-case slot.

Every line is filled from the life's actual state (S["aim2"], S["capacity"], S["aim_forks"], foresee's F.preview),
never from a simulated future: a part of a preview is shown only when its fact is true of this character now.

Slots (all filled by the Game in words, never numbers or percentages):

    {N}, {Ns}        the character's name and possessive
    {thing}          this aim's field thing (the field's `thing`: "chess", "medicine")
    {next}           the step being decided: the next rung's `say` ("a rated player", "a place at a medical school")
    {rung}           the rung already reached, as a noun phrase that reads after "became" ("a rated player");
                     UPKEEP only
    {other}          the other claim in play: another aim's thing ("the community project"); in BOTTLENECK time and
                     WHY_NOW over it may also be the largest non-aim claim on the hours, in words ("work",
                     "caring for {child}")
    {who}            the person whose time or care is affected, or who gives support, by name or role
    {partner}        the partner, by name (PREVIEW overlap_partner only)
    {parent}, {child}  a parent or a child by name, when the Game words {who} more exactly (optional)
    {hours_words}    the step's hours at the chosen intensity: "two evenings a week", "most weekends", "an hour a day"
    {money_words}    the yearly money, as a noun phrase: "a fee each term", "a small sum each month",
                     "more than the household spends on anything else"
    {entry_words}    the one-time way in, as a noun phrase: "an audition and a fee to enter",
                     "a year's spare money up front", "a recommendation from a teacher"
    {energy_words}   how tiring, as an adjective: "light", "steady", "tiring", "draining"
    {closes}         when a way in closes, as a phrase that reads after "closes": "at the end of the spring",
                     "before {N} turns thirty", "in about two years"
    {opens}          when a way in next opens, as a phrase that reads after "opens": "next autumn",
                     "once a year, in the summer" (BOTTLENECK window only)
    {door}           what the step could open, as a noun phrase: "specialist work", "a place on the first team"
    {kept_by}        what keeps a part from fading, from the rung's upkeep `kept_by`, as a noun phrase:
                     "regular play or teaching", "work in the field"

Tables:

    WHY_NOW[kind]          one sentence on why this choice matters now, per fork kind: commit (taking on a step),
                           cost, chance, window (closing), over (competing demands), changed (what a step needs, or
                           whether it is open, changed). Slots: N, Ns, thing, next, other, hours_words, money_words,
                           closes, door, who.
    PREVIEW[part]          the preview's parts, each one sentence; the Game shows the parts that apply, in the order of
                           PREVIEW_ORDER, joined by a space. Two templates each. Where the two differ by condition the
                           table says so (overlap_partner, unknown_admission). Slots as named in each line.
    PREVIEW_ORDER          the order the parts are joined in.
    STATE_WORDS[state]     the agenda's states (contracts.md section 6): dict(label, say); label is a short word or
                           two, say a list of one line. Slots: N, Ns, thing, next.
    BOTTLENECK[key]        what holds the aim now (S["aim2"] bottleneck: "time", "money", "a window" -> window,
                           "a fork" -> fork, "a door" -> door, "" -> nothing). One line each, naming the actual limit.
    FUNDED[level]          the share of its demand the capacity funds (`funded`): full (all), most (over about two
                           thirds), half (about a third to two thirds), little (under about a third). One line each,
                           honest about the slower pace, never "stalled" or "lost". Slot: thing.
    UPKEEP[of]             proficiency, access, credential: dict(fading (two lines: what faded, the achievement kept),
                           refresh (two lines: feasible ways back, none promised), kept (one line: what keeps it)).
                           Slots: N, Ns, thing, rung, kept_by.
    EXPIRY                 two lines, told once, when a way in closes before the step was reached. Slots: N, thing,
                           next.
    REVIEW                 two header lines for an agenda review that groups linked choices. Slots: N, Ns.
    LINKED[reason]         capacity, window, relationship: one line each on why these choices are linked.
                           Slots: closes, who.
    INTEGRATE              dict(earned (two lines: the rare integrated asset earned when two pursuits are shown used
                           together), why (two lines: it comes from showing them together, not from holding both)).
                           Slots: N, Ns, thing, other.
    TRIBAL[table][key], MAGIC[table][key]
                           the same keys, two lines each, only where the words differ by world (time between the hunts,
                           the band's stores, the elders' leave; duties in the tower, coin, the guild's seal). A key
                           not given there reuses Earth's. Nested the same way as the Earth table.

Writing rules kept here, for whoever adds lines:
- Amounts only through the word slots; no percentages, no counts of chance, no promised outcome, no hidden future
  event, no named reaction of a person beyond what the state already shows (overlap_partner's first line is used only
  when the partner's want for time is already up).
- Overcommitment slows or strains; it never collapses, ruins or ends anything by itself.
- A paused or set-aside pursuit keeps its learning and its people; a reached step is never taken away, only the named
  part of an upkeep fades.
- No colour words, no game terms (aim, rung, fork, agenda, capacity, perk, title, window, upkeep, funded), never "you";
  timeless (no year, brand, country, currency, real place, person, faith or event); nothing preaches.

Worlds: earth (timeless modern towns), tribal (bands and circles, the fire, the camp, the hunting grounds, the turning
seasons, before cities), magic (towers, guilds and old powers; circles and orders, halls and the tower).
"""

WHY_NOW = {
    "commit": [
        "{next} is the next step in {thing}, and it asks for a new promise of {hours_words}, not just more of the same.",
        "Saying yes to {next} would change what {thing} asks of {N} from here on, so it is put as a choice now.",
        "Earlier choices about {thing} do not decide this one: {next} is a fresh commitment, and it is {Ns} to make or not.",
    ],
    "cost": [
        "Going on with {thing} now means {money_words}, and money spent on it is not there for anything else.",
        "{thing} has come to a point where it costs {money_words}, before anyone knows what it will bring.",
    ],
    "chance": [
        "An opening has come up in {thing} that could lead to {door}; if it is let go, it will not come round again at this step.",
        "{N} has a chance at {next} sooner than the usual road would bring it, and chances like this do not wait long.",
    ],
    "window": [
        "The way into {next} closes {closes}, so the choice cannot sit for long.",
        "Time is short for {next}: the way in closes {closes}, whatever else is going on.",
    ],
    "over": [
        "As things stand, {thing} and {other} together ask more of {Ns} week than it holds, so one or both will go slower.",
        "{N} has taken on more than the free hours can carry: {thing} and {other} want the same time.",
        "Something in {Ns} week has to be set first, because {thing} and {other} cannot both have all they ask.",
    ],
    "changed": [
        "What {next} asks is not what it was when {N} took it on, so the earlier answer may not fit any more.",
        "Whether {next} is open to {N} has changed, and the plan made before needs another look.",
        "The terms of {next} have shifted since {N} said yes, so the choice is put again.",
    ],
}

PREVIEW = {
    "hours": [
        "This step asks {hours_words}.",
        "Going on with {thing} would take {hours_words}.",
    ],
    "money_year": [
        "The cost is {money_words}.",
        "Paying for it means {money_words}.",
    ],
    "entry": [
        "To begin, {N} needs {entry_words}.",
        "The way in asks {entry_words}, once.",
    ],
    "energy": [
        "Week to week it is {energy_words}.",
        "On top of everything else, it would be {energy_words}.",
    ],
    "overlap_aim": [
        "It overlaps with {other}.",
        "It wants the same free hours as {other}.",
    ],
    "overlap_care": [
        "It falls in hours {N} gives to caring for {who}.",
        "It would cut into the time {who} needs from {N}.",
    ],
    # [0] only when the partner's want for time is already up; [1] otherwise.
    "overlap_partner": [
        "{partner} has already asked for more time together.",
        "It comes out of evenings {N} and {partner} now spend together.",
    ],
    "overlap_work": [
        "It would have to fit around {Ns} work.",
        "Some of it falls in hours {Ns} work already claims.",
    ],
    "window": [
        "The way in closes {closes}.",
        "It has to be taken up soon: the way in closes {closes}.",
    ],
    # [0] when a place is decided by others (a selection, an audition); [1] when it depends on a test or a result.
    "unknown_admission": [
        "Whether {N} is taken on is not known.",
        "Getting in is not certain; it depends on more than effort.",
    ],
    "unknown_result": [
        "Finishing it could open {door}; what comes after is not known.",
        "It could lead to {door}, though nothing about the road after it is settled.",
    ],
    "exit_cost": [
        "If {N} stops later, what was paid to get in is not returned, though the learning stays.",
        "Leaving it later costs what was put in, not what was learned.",
    ],
    "pause_ok": [
        "It can be paused and picked up again without starting over.",
        "If the week gets too full, it can wait a while without being lost.",
    ],
    "pause_not": [
        "A pause will not hold its date: the way in still closes {closes}.",
        "Pausing it does not stop the clock on it.",
    ],
    "support": [
        "{who} can take on part of it, though the effort is still {Ns}.",
        "With {who}'s help part of the load is lighter; the work itself is still {Ns} to do.",
    ],
}

PREVIEW_ORDER = (
    "hours", "money_year", "entry", "energy",
    "overlap_aim", "overlap_care", "overlap_partner", "overlap_work",
    "support", "window", "unknown_result", "unknown_admission",
    "pause_ok", "pause_not", "exit_cost",
)

STATE_WORDS = {
    "holding": {
        "label": "holding",
        "say": ["{N} wants {thing}, but is not working at it yet."],
    },
    "pursuing": {
        "label": "pursuing",
        "say": ["{N} is working toward {next} and gives {thing} what it asks."],
    },
    "reduced": {
        "label": "going lightly",
        "say": ["{N} keeps at {thing}, but at a lighter pace than it asks, so the next step comes later."],
    },
    "keeping_up": {
        "label": "keeping up",
        "say": ["{N} has got where {N} meant to in {thing} and keeps it in use."],
    },
    "paused": {
        "label": "paused",
        "say": ["{thing} is on hold; what was learned waits with it, though outside dates do not."],
    },
    "set_aside": {
        "label": "set aside",
        "say": ["{N} has stopped pursuing {thing}; what was learned, and the people met through it, stay."],
    },
}

BOTTLENECK = {
    "time": ["There are not enough free evenings for {thing} and {other} both."],
    "money": ["{thing} costs more each year than the household has free after the essentials."],
    "window": ["The next step in {thing} waits for its way in, which opens {opens}."],
    "fork": ["{thing} waits on a choice that has not been made yet."],
    "door": ["{N} has done the work for {next}; what holds it now is the result itself, which effort alone does not bring."],
    "": ["Nothing holds {thing} back just now; it moves at its own pace."],
}

FUNDED = {
    "full": ["{thing} gets all the time it asks, so it moves at the usual pace."],
    "most": ["{thing} gets most of what it asks; the next step comes a little later than it otherwise would."],
    "half": ["{thing} gets about half of what it asks, so at this pace the next step is further off than usual."],
    "little": ["{thing} gets only what time is left over; at this pace the next step is far off, though not out of reach."],
}

UPKEEP = {
    "proficiency": {
        "fading": [
            "{N} became {rung}, and that stays on record; it is the everyday sharpness at {thing} that has slipped.",
            "Time away from {thing} shows in {Ns} hand, though nothing takes away that {N} became {rung}.",
        ],
        "refresh": [
            "A spell of {kept_by} could bring the sharpness back; how quickly depends on how things stand.",
            "Steady practice again, a refresher, or teaching it to someone could sharpen it, given the time.",
        ],
        "kept": ["As long as {N} keeps up {kept_by}, {Ns} hand at {thing} stays sharp."],
    },
    "access": {
        "fading": [
            "The people {thing} brought into {Ns} life have moved on; what {N} did is remembered, but the ready welcome has cooled.",
            "Doors that {thing} once opened for {N} are less open than they were, though {N} is still the one who became {rung}.",
        ],
        "refresh": [
            "Getting back in touch, or a return to {kept_by}, could reopen some of those doors; nothing is promised.",
            "An old contact, a visit, or a piece of new work could bring some of the welcome back, depending on who is still there.",
        ],
        "kept": ["As long as {N} keeps up {kept_by}, these doors stay open."],
    },
    "credential": {
        "fading": [
            "{Ns} papers for {thing} have lapsed; that {N} became {rung} stays on record, but it no longer counts as current.",
            "The standing that lets {N} practise {thing} needs renewing; the achievement itself stays.",
        ],
        "refresh": [
            "Renewing it means whatever the rules ask: a course, an exam, or proof of recent work.",
            "A return to {kept_by} could renew it; until then, the work that needs it stays closed to {N}.",
        ],
        "kept": ["As long as {N} keeps up {kept_by}, it stays current."],
    },
}

EXPIRY = [
    "The way into {next} has closed. What {N} learned along the way stays.",
    "The time for {next} has passed; {thing} goes on, but not by that way.",
]

REVIEW = [
    "Several of {Ns} plans need a decision at once, and they are tied together.",
    "{N} cannot settle one of these without touching the others, so they are put side by side.",
]

LINKED = {
    "capacity": ["They draw on the same free hours and money, and there is not enough for all of them at full pace."],
    "window": ["They run against the same date: the way in closes {closes}."],
    "relationship": ["Each of them takes time that {who} counts on."],
}

INTEGRATE = {
    "earned": [
        "{N} has brought {thing} and {other} together in one piece of work, and people have seen what it can do.",
        "What {N} knows of {thing} has gone into {other}, and the result is something neither alone could make.",
    ],
    "why": [
        "This comes from putting {thing} and {other} to work together, not from having both.",
        "Holding both was not enough; it was showing them together that counted.",
    ],
}

TRIBAL = {
    "WHY_NOW": {
        "cost": [
            "Going on with {thing} now asks {money_words}, and what the band gives to it is not there for the lean months.",
            "{thing} asks {money_words} now, before anyone at the fire knows what it will bring.",
        ],
        "over": [
            "{thing} and {other} both want the same days between the hunts, and there are not enough for both at full pace.",
            "{N} has taken on more than the seasons can carry: {thing} and {other} want the same days.",
        ],
    },
    "PREVIEW": {
        "money_year": [
            "It asks {money_words} from what the band shares.",
            "The band's stores would carry {money_words} for it.",
        ],
        "overlap_partner": [
            "{partner} has already asked for more time together at the fire.",
            "It comes out of days {N} and {partner} now spend together.",
        ],
        "overlap_work": [
            "It falls in days the hunt and the camp's work already take.",
            "It would have to fit around {Ns} share of the band's work.",
        ],
        "exit_cost": [
            "If {N} stops later, what was given to begin is not given back, though the learning stays.",
            "Leaving it later costs what was given, not what was learned.",
        ],
    },
    "BOTTLENECK": {
        "time": [
            "There are not enough free days between the hunts for {thing} and {other} both.",
            "{thing} waits for days that the camp's work and {other} already fill.",
        ],
        "money": [
            "{thing} asks more of the band's stores than can be spared.",
            "What {thing} needs in goods and trade is more than the hearth has to spare.",
        ],
        "window": [
            "The next step in {thing} waits for its season, which comes {opens}.",
            "{thing} waits for the turn of the seasons; its way in opens {opens}.",
        ],
    },
    "UPKEEP": {
        "access": {
            "fading": [
                "The bands {thing} brought {N} to have drifted onto other trails; what {N} did is still told, but the ready welcome has cooled.",
                "Fires that once made room for {N} because of {thing} make less room now, though the camp still knows {N} became {rung}.",
            ],
        },
        "credential": {
            "fading": [
                "The elders' leave for {N} to practise {thing} has lapsed with the seasons; that {N} became {rung} is still told at the fire.",
                "{N} would need the elders' word again before taking up {thing} for the band; what {N} did is not forgotten.",
            ],
            "refresh": [
                "Going before the elders again, and showing the skill, could win back their leave.",
                "A season of {kept_by}, seen by the elders, could restore their word.",
            ],
            "kept": [
                "As long as {N} keeps up {kept_by}, the elders' leave stands.",
                "While the band sees {N} at {kept_by}, no one asks for the elders' word again.",
            ],
        },
    },
    "INTEGRATE": {
        "earned": [
            "{N} has brought {thing} and {other} together in one work, and the whole camp has seen it.",
            "At the fire they speak of how {N} joined {thing} and {other}, and what came of it.",
        ],
    },
}

MAGIC = {
    "WHY_NOW": {
        "cost": [
            "Going on with {thing} now asks {money_words}, and coin spent on it will not be there for anything else.",
            "{thing} asks {money_words} now, before any master can say what it will bring.",
        ],
        "over": [
            "{thing} and {other} both want the hours left after {Ns} duties, and there are not enough for both at full pace.",
            "{N} has taken on more than the tower's hours allow: {thing} and {other} want the same time.",
        ],
    },
    "PREVIEW": {
        "overlap_work": [
            "It falls in hours {Ns} duties to the guild already claim.",
            "It would have to fit around {Ns} duties in the tower.",
        ],
        "money_year": [
            "The cost is {money_words}.",
            "The guild's dues for it come to {money_words}.",
        ],
    },
    "BOTTLENECK": {
        "time": [
            "There are not enough free hours between {Ns} duties for {thing} and {other} both.",
            "{thing} waits for hours that the tower's work and {other} already fill.",
        ],
        "money": [
            "{thing} asks more coin each year than {N} has once the household's needs are met.",
            "The dues and materials for {thing} are more than {Ns} purse can spare.",
        ],
    },
    "UPKEEP": {
        "access": {
            "fading": [
                "The halls {thing} opened to {N} have grown cooler; the order remembers {N}, but its doors are less ready.",
                "The circles {N} knew through {thing} have moved on, though the rolls still say {N} became {rung}.",
            ],
        },
        "credential": {
            "fading": [
                "The guild's seal on {Ns} {thing} has lapsed; that {N} became {rung} stays in the rolls, but it no longer counts as current.",
                "{N} would need the guild to renew its seal before practising {thing} for hire again; the achievement stays written.",
            ],
            "refresh": [
                "Sitting the guild's renewal, or showing recent work to its masters, could restore the seal.",
                "A season of {kept_by} under the guild's eye could renew it.",
            ],
            "kept": [
                "As long as {N} keeps up {kept_by}, the guild's seal holds.",
                "While the masters see {N} at {kept_by}, the seal stays current.",
            ],
        },
    },
    "INTEGRATE": {
        "earned": [
            "{N} has bound {thing} and {other} together in one working, and the order has seen it.",
            "In the halls they speak of what {N} made by joining {thing} and {other}.",
        ],
    },
}
