# odds: optional (engine 08:55). Skill, standing and bond perks give better odds to acts in their ways; access perks
# (credentials and assets: a licence, a passport, a car, savings, a house) carry odds=0 and work only through
# requires: on specific acts, which the Library's act pass adds.
# Chroma Library: titles and perks for modern Earth (draft, Library thread, 2026-10-05).
# Asked for by Emren (08:05: "do we have enough perks and titles to increase the richness of one life's depth. Is it
# realistic numbers?"). Plan in chroma-library/perks-titles-plan.md. Written to the engine's format
# (chroma-engine/perks-titles-format.md, 08:15). Plain data: nothing is imported, nothing runs. Modern Earth only; the
# tribal and magic worlds get their own catalogues later, so there is no worlds field.
#
# The file is built as TITLES = [] and PERKS = [], with one "+= [...]" block per kind, so it stays valid at every step.
#
# TITLES: a role or status other people recognise, held for a stretch of life. A title of one of the five commitment
# kinds refines that commitment (holding "nurse" means holding a career with the nurse's colors as its profile); one
# title per commitment kind at a time. Statuses stand outside the commitments, and a person may hold any number.
#   name     the title as a short phrase, the key acts use (title:, drops:, requires:)
#   kind     career | partner | children | community | faith | status
#   ways     the colors the role expects of its holder and rewards, as letters ("W G"); it becomes the commitment's
#            profile. Each letter counts 1/len in the balance (a pair .5 each, a triad 1/3 each). Every status has
#            ways="": a status is a fact about a life (a record, a divorce, a degree), not a role with expectations,
#            and only commitment-kind titles become a commitment's profile. A status works through meets alone
#   meets    what holding it gives or costs while held, in the engine's base: syntax: need:<safety|belonging|autonomy|
#            competence|meaning>+.x and res:<money|time|health|ties|freedom>+.x; sizes .02 to .15. Written as the
#            title's own effect on top of what its commitment kind already meets (library.py COMMITMENTS). Since one
#            title per commitment kind is held at a time, a later title of the same kind (parent of three, team
#            captain, deacon) replaces the earlier one and carries its full effect; statuses add up
#   ages     (youngest, oldest) a person can hold it
#   share    the share of people in a modern rich country who ever hold it in their life, 0 to 1. The sum over TITLES
#            is the number of titles an average life holds over its course (target 10 to 20). A named source follows
#            where a well-known figure exists; anything else says "estimate"
#   say      how the story names the person ("a nurse")
#   lasts    statuses only: "life", or the years it lasts by itself before it fades (newcomer 2)
#   gained   plain words: how one comes to hold it. Situations from earth.md and the engine's history marks are in
#            single quotes ('a new job at last', 'learned a skill'); titles and perks of this file in brackets ([nurse])
#   lost     plain words: what ends it
#   cause    optional (every change has a cause, L2, 10-18): when the engine's rule names only an age, a stage, money
#            or nothing, the closing clause the game tells the gain with ("Ari can swim now, after lessons as a
#            child."): lower case, no end stop, true for the rule as it stands (chroma-library/notes/cause-audit.md)
#   needs    plain words: what must come first (a title, a perk, a history mark, an age, money)
#   profiles optional (engine 12:45): two or three equally valid ways to hold the title, [("W U", "words"), ...]; ways
#            is the first profile. A person holds the profile that fits them best and may move to another as their
#            colors drift ("reshaped", never a new title). In the balance each profile counts 1, split over its letters
#   refines  optional (engine 12:45): a facet, held on top of the title it names (newlywed on [wife or husband]); it
#            takes no slot of its kind and ends with that title. Several titles with ";" (engine 15:00): the facet sits
#            on any of them and ends when none is held
#   turning  optional: Emren's "ordinary turning point" for the title, the seed of a moment only its holders meet
#   sector   careers only (outer world, chroma-engine/world-fields.md, 2026-10-07): farm, industry, services, knowledge
#            or public. The economy and automation reach a job through its sector, and the state budget moves the
#            public ones. Jobs mostly paid from the public purse in a rich democracy (nurse, teacher, care worker,
#            physician, soldier, postal worker) are public; transport and retail are services; trades are industry
#
# PERKS: something a person can do or has access to that changes their odds or opens options. Emren's lifecycle:
# eligible, acquired, suspended, lost, retired, regained. Losing access keeps the skill, which then fades by
# skill_half: a struck-off nurse still knows nursing. Temperament and discipline are the engine's own learned traits,
# so they are not perks; a learned way that is a concrete skill (calming people down, public speaking) is a skill.
#   name       the perk as a short phrase, the key acts use (grants:, takes:, suspends:, requires:)
#   kind       skill | credential | standing | bond | asset
#   ways       the colors of the acts it helps, as letters ("R G"); counted 1/len each in the balance
#   odds       how much better acts in those ways go while the perk lasts, .02 to .1
#   skill_half years for what it taught to fade by half once access is gone or it goes unused; None when nothing is
#              left to fade (most assets: money spent is gone; a citizenship is never unlearned)
#   retires    an age at which it ends by itself, or None (body perks end when health makes them impossible)
#   ages       (youngest, oldest) a person can hold it
#   share      the share of people who ever hold it (target sum 15 to 30), sourced or "estimate" as for titles
#   say        a short phrase for the story ("can drive")
#   gained, lost, needs, cause   plain words, as for titles
#
# Balance (checked by check_perks_titles.py): over the commitment-kind TITLES (career, partner, children, community,
# faith; statuses carry no colors and stay out of it), and separately over PERKS, the ways letters summed per color
# (1/len each) are within 3% of each other, and every commitment kind and every perk kind holds all five colors.
# Singles, ally pairs, enemy pairs and triads all appear. Every color's entries hold discipline, care, ambition,
# curiosity and freedom in its own way: the boxer's training is Red discipline, the single parent's provision is Black
# care, the farmer's growing herd is Green ambition, the stepparent's slow patience is Blue care, the union rep's
# stand is White freedom.
#
# Realism groups (shares that interact):
#   - Nested titles: [veteran] and [has killed in war] come only after [soldier]; [ex-prisoner] only with
#     [someone with a record]; [parent of three or more], [single parent] and [grandparent] after [mother or father];
#     [partner of many years] after [living together] or [wife or husband]; [team captain] after [on the team]. Each is
#     its own recognised title, so its share counts again.
#   - One at a time: the career titles are held one after another (12.7 jobs from 18 to 56 for Americans born 1957 to
#     1964, US BLS NLSY79, 2023, many of them in the same few kinds of work), so their shares add up to about two
#     recognisable kinds of work per life, as listed here; the partner titles are a sequence (sweetheart, engaged,
#     living together, married, many years), so their shares add past 1.
#   - One per kind at a time: [on the team], [scout or guide] and [prefect] all take the child's one community slot,
#     and [regular worshipper], [activist in a cause] and [party member] the one faith slot (an engine question,
#     listed in perks_titles.md).
#   - Both at once: [newcomer] (new in town, fades in two years) and [immigrant] (for life).
# Statuses the engine grants itself (widowed, retiree, newcomer) are named here so the story uses these words; each
# carries the comment "granted by the engine".
#
# Safety (Emren's limits): dark statuses are named in plain words (a record, prison, a gang, homelessness, killing in
# war); nothing touches sexual violence, nothing makes harming children a role or a skill, nothing is graphic, and no
# entry moralises.

TITLES = []
PERKS = []

