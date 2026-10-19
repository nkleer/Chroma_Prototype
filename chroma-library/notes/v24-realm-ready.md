# v24 Library mechanics: how they read in a magic realm

Library thread, 2026-10-19. This is the design note that CONTRIBUTING.md ("New mechanics are realm-ready") asks for, covering the Library's v24
parts:

- footprints (#353, #357);
- aims and the world lines (#354, #357);
- the decision levers and the subvert ways (#361).

Each paragraph names what sits on the core and what is Earth's data, then says how the mechanic reads in a magic realm.

**Footprints.** Every option of a life event leaves one or two things the player can see, and every realm has the six
kinds: a person, a place, a means, a mark, a door or a lesson (`footprint_names.KINDS`). What is Earth's is only the
words. Today those are in `footprint_names.py`:

- the people's roles (`ROLE`);
- the haunts by sphere (`HAUNT`: "a sports club", "the bank");
- the means (`MEANS`);
- the marks' lines.

The table that says which option leaves which footprint (`<world>_foot.py`'s `FOOT`) is keyed by moment and option, so a
realm's own moments carry their own table. In a magic realm the same stacks hold "a master of the tower" (person), "the
guild hall" (place), "favour with the old powers" (means), "broke an oath" (mark), "a debt owed to the fair folk" (door,
told when it comes back), and a lesson in that realm's words. A realm file gives its own `HAUNT` and `ROLE` words for the
nine spheres; the engine reads only the kinds.

**Aims and the world lines.** An aim is defined on the core:

- a face (colours);
- a domain;
- a sphere;
- an area;
- a ladder of three to five steps, each reached by holding any one of a few named titles or perks;
- heights on the ladder, Known, Notable and Historic, read from standing (rung, a good name, reach across the country,
  a work that outlives you).

Every aim in `earth_aims.py` already carries its `tribal` and `magic` wording, and its 60 spark moments carry earth,
tribal and magic lines (`worlds`). In a magic realm "to work the land" reads "to tend the tower's growing gardens, where
the old herbs still answer". Its steps name that realm's titles in place of Earth's (an apprentice of the circle, a
keeper of the gardens), and its Historic height is a work the realm remembers. A realm file supplies `AIMS_<WORLD>` and
`LEGACY_<WORLD>` in the same format.

The told lines in `earth_world_lines.py` are keyed by world already:

- `BECAUSE`: the world moving because of the character;
- `NATION`: what a national push visibly did;
- `KEPT`: what the world kept at the end;
- `CAUSE`: how a line names its cause.

Each has earth, tribal and magic lines, and the units and rings they name (a person, a group, a place, a town's sphere,
the nation) are the core's. In a magic realm, "the order still teaches {N}'s way" stands where Earth says "the school
still teaches {N}'s way".

**Decision levers and subvert.** A decision for others is defined on the core:

- a sphere where the character is Known;
- two to four directions, each a colour mix;
- a scope (their place, the town's sphere, or the nation);
- a lever, the way the act works on the world: voice, loyalty, lead, found, fund, exit, neglect or subvert.

Every realm has people who argue, keep a thing going, take charge, start something new, pay for it, walk away, let it
slide, or quietly bend it. About one decision in four offers a subvert way (a quiet favour, a bent rule, loose books, a
held-back record), and it feeds the shadow of its colour (spec F6). What is Earth's is the 36 decision moments themselves:
the bylaw, the clinic's list, the credit union's loans. They carry Earth lines only, because a magic realm writes its own
moments on the same fields rather than retelling Earth's. A magic realm's council of the tower rules on who may enter
the library of spells (rule, voice or lead). Its healers' house decides who is seen first (care). A subvert way there is
a ward left unchecked one more season, a bargain kept off the guild's ledger, or a favour owed to a spirit and never
written down. The safety lines hold in every realm: no decision harms a child, none is violent or graphic, and a cover-up
is about money, safety, records or neglect, never a person hurt.
