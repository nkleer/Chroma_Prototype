"""Chroma library, modern Earth: aims as fields (v25, decision 9; chroma-engine/notes/v25/aims-shape.md sections 3 to 8).
Plain data, hand-written from the Library's v25 drafts (poured 10-23 by tools in the Library thread; the drafts stay in
the shared folder's chroma-ideas/v25-prep/library/fields/). Nothing reads this file until the Engine's aims refit
(aims_v2) is on, so no life changes. Checked by tests/check_fields.py.
- FIELDS_EARTH {field: dict}: the 60 v1 aims in earth_aims.py's order, then the new dream fields. Each keeps v1's
  face, sphere, domain, calling, dreams, below, tribal, magic, area, spark and, step for step, say, any, req, height.
- FIELDS_EARTH_LAND {way: dict}: the land's 30 ways as fields of the land shape (their numbers stay in land.json).
- TITLES_V25 [dict]: the new titles the rungs name, in the catalogue's format (perks_titles/00-head.py) plus `doors`.
  They stay out of earth_perks_titles.py until the Engine reads them with the refit on.
`prep` tags are one shared set across the parts (the writers' synonyms merged at the pour). All demand, window,
upkeep, share and year numbers are estimates unless a comment names a source.
"""



# ==== part a: from v25-prep/library/fields/fields-a.py, its header:
# Chroma library, modern Earth: v25 prep, fields part a, the competition, craft, art and knowledge shapes (Library
# writer a, 10-23). DRAFT, nothing reads it: the Library pours FIELDS into chroma-library/earth_fields.py
# (FIELDS_EARTH) on Friday 10-23 21:00 (Emren's time), and NEW_TITLES into earth_perks_titles.py with their doors.
# Format: chroma-engine/notes/v25/aims-shape.md sections 3 and 8 (the chess entry, key for key, plus the keys frozen
# later in section 3: prep, meets, demand, window, upkeep); brief: chroma-ideas/v25-prep/library/briefs/FIELDS.md and
# V25-DECISIONS.md ("Aims").
#
# Holds the 11 v1 Earth aims of these four shapes (areas body, craft, art, knowledge) and the 7 new dream fields of
# them (chess, football, racing, the ring, the martial-arts belt, video games, a band). v1's name, face, sphere,
# domain, calling, dreams, below, tribal, magic, area and spark are as v1 has them (the Engine reads sparks), and each
# step's say, any, req and height unchanged. The new dream fields have no v1 area or spark. A v1 aim with fewer steps
# than its shape's 5 rungs names the rungs it leaves out in `skip`, so its rungs map onto the shape in order.
#
# Clocks: `years` is (median, 10th, 90th percentile) of steady effort from the rung below; `share` is of those who
# keep at it, the share who reach that rung, so the shares multiply down the ladder. Sources are named in the comment
# above each field; "estimate" where no count is known. Ways in (V25-DECISIONS "Aims"): each field's places, people,
# contest and `round` give at least three ways in, and the last `round` entry is the recurring one (a weekly, monthly
# or yearly thing). A `time=True` rung comes with age alone (retiring): no forks, no contests, shown as "comes with
# time"; its `years` is the usual wait from the rung below, for the track only.
#
# Demands, windows and upkeep (aims-shape.md sections 3 and 5): ALL ESTIMATES, from what such pursuits usually ask.
# - `demand` = dict(hours a week at steady intensity, money a year as a share of a year's free money, entry as a
#   one-time share of a year's free money, energy 0 to 1). For a paid rung (a contract, a trade, a class of one's own)
#   the paid work week is the job's, not the aim's: `hours` is what the aim asks beyond it (study, extra practice,
#   building a name), and `money` is 0 where the rung pays its own way.
# - `window` = dict(every (years), open_weeks, deadline_age, deadline_years, pause_stops), only where real outside
#   timing exists (a yearly trial or audition season, an age limit for an academy or a junior series, a foraging
#   season); None elsewhere.
# - `upkeep` = dict(of ("proficiency", "access" or "credential"), years without use before it fades, kept_by (tags of
#   the uses that keep it)), only where something truly fades (fitness at the top of a sport, a licence, a coaching
#   badge, a clientele); None on most rungs. The reached title stays recorded either way.
# - `prep` tags (shared preparation counted once across two active aims) use a small common set: strength, endurance,
#   a team, reading, study, strategy, the workshop, the kitchen, writing code, drawing, music practice, a stage,
#   the outdoors, plants, listening, explaining, discipline. `meets` names needs from belonging, meaning, competence.
#
# Shape rungs (core labels): competition = taking part, regular, winning, master, summit; craft = learner, journeyman,
# trusted hand, master, a name in the craft; art = trying, showing, a following, recognised, a body of work;
# knowledge = student, practitioner, contributor, authority, a finding that lasts.
#
# Words: the field "to earn a black belt" and its dream "a black belt" keep the names fields-by-shape.txt and dreams.py
# give them (they are keys); every word a player reads says "the first-degree belt" instead, so no colour word shows.

_FIELDS_A = {

    # ================================================================ competition

    # Clock: estimate from sport-development pathways (a first club at 6 to 10, a first senior trophy in the mid-teens,
    # a first paid contract at 18 to 22, peaks in the mid to late twenties); professional athletes are about 1 in 1,000
    # people (the catalogue's share), a few in 100 of those who compete seriously as juniors. Shares: estimate.
    # Demands, windows (paid careers mostly begin by 30, top careers end in the mid-thirties) and upkeep: estimate.
    "to win at the highest level": dict(
        shape="competition", face="B", sphere="gather", domain="", calling=True,
        dreams=["a champion of the tournament", "a record nobody has beaten", "the champion wrestler of the gatherings",
                "the fastest runner in the clans"],
        thing="the sport", doing="training", contest="a competition",
        places=["gather.games"],
        people=dict(coach="a coach who sees something in them", rival="a rival from the next town",
                    peer="the rest of the squad", patron="a sponsor"),
        round=["the club across town", "a coach outside the family's circle", "the open trials held every spring"],
        prep=["strength", "endurance"], meets=["competence", "belonging"],
        below="{N} cannot lose a race to the bus stop without demanding a rematch",
        tribal="to win the races and the wrestling at every great gathering of the clans",
        magic="to take the champion's laurel at the realm's great games, year after year",
        area="body", spark="the first time winning is the only thing in the room",
        rungs=[
            dict(say="training every day", any=["on the team", "keeping fit", "boxing or martial arts", "swimming"],
                 years=(1, 0.5, 2), share=0.9, start=(6, 10, 16), contests_y=0, forks=["go_on"],
                 demand=dict(hours=6, money=0.05, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="trophies on the shelf", any=["trophies won", "team captain"],
                 years=(3, 1, 6), share=0.5, contests_y=6, forks=["pay"],
                 demand=dict(hours=12, money=0.15, entry=0.05, energy=0.7), window=None, upkeep=None),
            dict(say="paid to compete", any=["professional athlete"], height="Known",
                 years=(5, 2, 9), share=0.06, contests_y=8, forks=["take"],
                 demand=dict(hours=25, money=0, entry=0, energy=0.8),
                 window=dict(every=1, open_weeks=8, deadline_age=30, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="proficiency", years=1, kept_by=["training", "competing"])),
            dict(say="a champion the country knows", any=["known across the country", "a household name"],
                 req="was('professional athlete') | has('trophies won')", height="Notable",
                 years=(4, 2, 8), share=0.15, contests_y=6, forks=["go_on", "take"],
                 demand=dict(hours=25, money=0, entry=0, energy=0.8),
                 window=dict(every=1, open_weeks=52, deadline_age=36, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a record that stands", any=["a work that outlives you"],
                 req="was('professional athlete') | has('trophies won')", height="Historic",
                 years=(4, 1, 10), share=0.1, contests_y=4, forks=["take"],
                 demand=dict(hours=25, money=0, entry=0, energy=0.8), window=None, upkeep=None),
        ]),

    # Clock: estimate (endurance builds over years: a first long event after about a year of regular training, real
    # toughness after five or so; the last rung is the end of working life, in the sixties). Shares: estimate.
    # Demands and upkeep (toughness fades after a couple of idle years): estimate.
    "to outlast them all": dict(
        shape="competition", face="B G", sphere="", domain="", calling=False,
        dreams=["the champion wrestler of the gatherings", "to climb the highest mountains"],
        thing="endurance", doing="going the distance", contest="a long-distance race",
        places=["gather.games", "prod.wild"],
        people=dict(coach="an old hand who has done it for decades", rival="a runner who never drops back",
                    peer="the early-morning regulars"),
        round=["the hill path on the edge of town", "a quiet stretch of river to swim in",
               "the long walk the ramblers' group makes every Sunday"],
        prep=["endurance", "the outdoors"], meets=["competence", "meaning"],
        below="{N} keeps walking long after the others have sat down, and does not say how much it hurts",
        tribal="to be the hunter still on the trail when the young ones have turned back for camp",
        magic="to be the old ranger who has seen three wardens come and go, and still walks the bounds",
        area="body", spark="the long walk the others give up on",
        skip=[2, 3],   # 3 steps: taking part, regular, (winning and master left out), summit
        rungs=[
            dict(say="a body you look after", any=["keeping fit", "swimming", "growing food"],
                 years=(1, 0.5, 3), share=0.9, start=(10, 30, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.4), window=None, upkeep=None),
            dict(say="tough as old roots", any=["strong stomach", "knowing the woods", "hunting and fishing"],
                 years=(5, 2, 10), share=0.5, contests_y=2, forks=["pay"],
                 demand=dict(hours=6, money=0.03, entry=0.05, energy=0.6), window=None,
                 upkeep=dict(of="proficiency", years=2, kept_by=["long walks", "outdoor work"])),
            dict(say="still on your feet when the rest have stopped", any=["retiree", "grandparent"],
                 req="has('keeping fit') | has('knowing the woods') | has('swimming')",
                 years=(25, 10, 40), share=0.7, contests_y=0, forks=[], time=True,
                 demand=dict(hours=2, money=0, entry=0, energy=0.2), window=None, upkeep=None),
        ]),

    # Clock: estimate (a daily habit forms in months; a weekly team or walk in a year or two; a coaching badge after
    # several years of it; the last rung is retiring, in the sixties). Shares: estimate. Demands and upkeep (weekly
    # fitness fades within a year idle; coaching badges are renewed every few years): estimate.
    "to stay strong and well for life": dict(
        shape="competition", face="G", sphere="", domain="", calling=False,
        dreams=[],
        thing="fitness", doing="keeping fit", contest="a fun run",
        places=["gather.games", "prod.wild"],
        people=dict(coach="the trainer at the gym", rival="a friend who always gets up the hill first",
                    peer="the walking group"),
        round=["the pool before work", "the hills at the edge of town", "the walking group that meets every Saturday"],
        prep=["strength", "endurance", "the outdoors"], meets=["belonging", "competence"],
        below="{N} takes the stairs, walks the long way round, and is restless after a day indoors",
        tribal="to stay strong enough to walk with the herds into old age",
        magic="to keep the body as sound as the old wardens who walk the walls at ninety",
        area="body", spark="the hill that wins every morning",
        skip=[2],   # 4 steps: taking part, regular, (winning left out), master (showing others how), summit
        rungs=[
            dict(say="moving every day", any=["keeping fit", "swimming", "dancing", "boxing or martial arts"],
                 years=(0.5, 0.25, 1.5), share=0.9, start=(6, 25, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.4), window=None, upkeep=None),
            dict(say="a team or a hill each week", any=["on the team", "club member", "knowing the woods"],
                 years=(2, 1, 4), share=0.65, contests_y=1, forks=["pay"],
                 demand=dict(hours=4, money=0.04, entry=0.03, energy=0.5), window=None,
                 upkeep=dict(of="proficiency", years=1, kept_by=["training", "a weekly team or walk"])),
            dict(say="showing others how", any=["youth coach", "coaching badge", "outdoor instructor"],
                 years=(6, 3, 12), share=0.25, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0.02, entry=0.05, energy=0.4), window=None,
                 upkeep=dict(of="credential", years=3, kept_by=["coaching", "a refresher course"])),
            dict(say="still strong at the end of working life", any=["retiree"],
                 req="has('keeping fit') | has('swimming') | has('dancing') | has('knowing the woods')",
                 years=(25, 10, 40), share=0.6, contests_y=0, forks=[], time=True,
                 demand=dict(hours=3, money=0, entry=0, energy=0.3), window=None, upkeep=None),
        ]),

    # Clock: aims-shape.md section 8 and aims-coverage.md [1] (Gobet and Campitelli 2007: masters about 11,000 hours of
    # deliberate practice, spread 3,000 to 23,600; titled players nearly all started serious play by 12). The template,
    # with the dream named as dreams.py has it ("a chess grandmaster"). Demands: estimate (club fees and a board are
    # cheap; coaching and travel to opens cost more; ratings and titles do not lapse, so no upkeep).
    "to master chess": dict(
        shape="competition", face="U B", sphere="gather", domain="", calling=True,
        dreams=["a chess grandmaster"],
        thing="chess", doing="playing chess", contest="a tournament",
        places=["gather.games", "learn.keeping"],
        people=dict(coach="a chess coach", rival="a rival from the club", peer="the club's regulars",
                    patron="a sponsor"),
        round=["games online", "a teacher outside the family", "the chess club across town, every week"],
        prep=["strategy", "study"], meets=["competence", "belonging"],
        below="{N} sets up the board again after everyone else has gone to bed",
        tribal="to be the best at the stone game the elders play by the fire",
        magic="to master the game of towers that the court plays",
        rungs=[
            dict(say="a club player", any=["club chess player"],
                 years=(1.5, 0.5, 3), share=0.9, start=(8, 12, 18), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="a rated player", any=["rated chess player"],
                 years=(2.5, 1, 5), share=0.6, contests_y=5, forks=["pay"],
                 demand=dict(hours=6, money=0.08, entry=0.05, energy=0.4), window=None, upkeep=None),
            dict(say="a tournament winner", any=["chess tournament winner"],
                 years=(3, 1.5, 6), share=0.35, contests_y=6, forks=["take"],
                 demand=dict(hours=10, money=0.12, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="a master", any=["chess master"], height="Known",
                 years=(4, 2, 9), share=0.12, contests_y=6, forks=["go_on", "take"],
                 demand=dict(hours=20, money=0.2, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a grandmaster", any=["chess grandmaster"], height="Notable",
                 years=(4, 2, 10), share=0.15, contests_y=5, forks=["take"],
                 demand=dict(hours=25, money=0.1, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # Clock: estimate from youth-academy pathways (a junior side at 5 to 8; academy places from about 9 to 12; a first
    # professional contract at 17 to 19; under 1 in 100 of academy entrants at 9 make a professional career, about a
    # third of those kept at 16 get a first contract; a top-division debut in the early twenties, a first national cap
    # at 21 to 25). Shares: estimate. Windows (summer trials; academies sign by about 16; first contracts rare after
    # 23; top-flight and national careers mostly end in the mid-thirties), demands and upkeep: estimate.
    "to play football at the top": dict(
        shape="competition", face="B R", sphere="gather", domain="career", calling=True,
        dreams=["a star footballer"],
        thing="football", doing="playing football", contest="a match",
        places=["gather.games"],
        people=dict(coach="a youth coach", rival="a rival for the same shirt", peer="the squad",
                    patron="a scout from a big club"),
        round=["a club in the next town that is short of players", "a coach outside the family's circle",
               "the open trials every summer"],
        prep=["strength", "endurance", "a team"], meets=["belonging", "competence"],
        below="{N} kicks a ball against the garden wall until it is too dark to see it",
        tribal="to be the best at the ball game the young hunters play between the camps",
        magic="to be the star of the ball games the guilds play on feast days before the whole court",
        rungs=[
            dict(say="a place in a junior side", any=["on the team"],
                 years=(1, 0.5, 3), share=0.9, start=(5, 8, 14), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="picked for an academy", any=["academy footballer"],
                 years=(3, 1, 6), share=0.12, contests_y=4, forks=["pay"],
                 demand=dict(hours=10, money=0.1, entry=0.05, energy=0.7),
                 window=dict(every=1, open_weeks=6, deadline_age=16, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a first contract", any=["professional athlete"], height="Known",
                 years=(6, 3, 9), share=0.2, contests_y=6, forks=["take"],
                 demand=dict(hours=20, money=0.02, entry=0, energy=0.8),
                 window=dict(every=1, open_weeks=10, deadline_age=23, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="proficiency", years=1, kept_by=["training", "matches"])),
            dict(say="a regular in the top division", any=["top-flight footballer"], height="Known",
                 years=(3, 1, 7), share=0.3, contests_y=8, forks=["go_on", "take"],
                 demand=dict(hours=25, money=0, entry=0, energy=0.8),
                 window=dict(every=1, open_weeks=52, deadline_age=33, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="proficiency", years=1, kept_by=["training", "matches"])),
            dict(say="picked for the national side", any=["international footballer", "known across the country"],
                 height="Notable",
                 years=(3, 1, 8), share=0.15, contests_y=6, forks=["take"],
                 demand=dict(hours=25, money=0, entry=0, energy=0.8),
                 window=dict(every=1, open_weeks=52, deadline_age=35, deadline_years=None, pause_stops=False),
                 upkeep=None),
        ]),

    # Clock: estimate from the karting-to-cars path (karting from 6 to 10, a full junior season after a year or two,
    # junior titles in the mid-teens, a paid seat at 18 to 25 for very few; money gates every step, so the early
    # forks are costs). Shares: estimate. Demands (the costliest field here: a season can take most of a family's
    # free money), windows (junior series end at about 19; paid seats rarely after 30; season entries yearly) and
    # upkeep (racing licences are renewed each year; a seat needs a sponsor each season): estimate.
    "to race cars": dict(
        shape="competition", face="B R", sphere="gather", domain="career", calling=True,
        dreams=["a racing driver"],
        thing="racing", doing="racing", contest="a race weekend",
        places=["gather.games", "prod.craft"],
        people=dict(coach="a driver coach", rival="the driver on the next row of the grid",
                    peer="the families in the paddock", patron="a sponsor who pays for a season"),
        round=["a cheaper series in the next town", "a mechanic's workshop that trades track time for help",
               "the kart club's practice night every week"],
        prep=["the workshop", "strength"], meets=["competence", "belonging"],
        below="{N} knows every corner of the kart track by heart, and takes each one a little faster",
        tribal="to be the fastest in the canoe races down the river at every gathering of the clans",
        magic="to drive the fastest chariot at the realm's great games",
        rungs=[
            dict(say="a kart and a club track", any=["club kart racer"],
                 years=(1, 0.5, 2), share=0.85, start=(6, 10, 16), contests_y=0, forks=["pay"],
                 demand=dict(hours=5, money=0.3, entry=0.4, energy=0.5), window=None, upkeep=None),
            dict(say="a licence and a full season", any=["licensed racing driver"],
                 years=(2, 1, 4), share=0.5, contests_y=6, forks=["pay", "round"],
                 demand=dict(hours=8, money=0.6, entry=0.3, energy=0.6),
                 window=dict(every=1, open_weeks=8, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=1, kept_by=["racing", "renewing the licence"])),
            dict(say="a junior championship", any=["junior racing champion", "trophies won"],
                 years=(3, 1, 5), share=0.2, contests_y=8, forks=["take"],
                 demand=dict(hours=12, money=0.9, entry=0.2, energy=0.7),
                 window=dict(every=1, open_weeks=26, deadline_age=19, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a paid seat in a team", any=["professional athlete"], height="Known",
                 years=(4, 2, 8), share=0.1, contests_y=8, forks=["go_on", "take"],
                 demand=dict(hours=25, money=0.2, entry=0, energy=0.8),
                 window=dict(every=1, open_weeks=12, deadline_age=30, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="access", years=1, kept_by=["racing", "a sponsor"])),
            dict(say="a championship title", any=["racing champion", "known across the country"], height="Notable",
                 years=(4, 1, 10), share=0.1, contests_y=6, forks=["take"],
                 demand=dict(hours=25, money=0, entry=0, energy=0.8), window=None, upkeep=None),
        ]),

    # Clock: estimate from amateur boxing and ring sports (a first amateur bout after 6 to 18 months in a gym; amateur
    # titles after a few years and some 20 to 40 bouts; turning professional in the early twenties; a title shot
    # after some years as a professional, for few). The ladder is bouts and titles only. Shares: estimate. Windows
    # (amateur championships yearly; professional licences rarely first granted after the mid-thirties), demands and
    # upkeep (a professional licence needs a yearly medical): estimate.
    "to fight in the ring": dict(
        shape="competition", face="R B G", sphere="gather", domain="career", calling=True,
        dreams=["a prize fighter"],
        thing="the ring", doing="training for the ring", contest="a bout",
        places=["gather.games"],
        people=dict(coach="a trainer at the gym", rival="a fighter in the same weight", peer="the others at the gym",
                    patron="a promoter"),
        round=["a trainer who coaches fighters in a garage", "the amateur shows in the next town",
               "the fight gym across town, open every evening"],
        prep=["strength", "endurance", "discipline"], meets=["competence", "belonging"],
        below="{N} skips rope in the yard every morning and shadow-boxes the washing line",
        tribal="to be the wrestler no clan can throw at the great gathering",
        magic="to win the belt in the guild halls' prize ring, where the realm's best meet",
        rungs=[
            dict(say="a gym and gloves of your own", any=["boxing or martial arts"],
                 years=(0.5, 0.25, 1.5), share=0.9, start=(8, 14, 24), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.04, entry=0.05, energy=0.7), window=None, upkeep=None),
            dict(say="amateur bouts", any=["amateur fighter"],
                 years=(1.5, 0.5, 3), share=0.55, contests_y=4, forks=["pay"],
                 demand=dict(hours=10, money=0.06, entry=0.05, energy=0.8), window=None, upkeep=None),
            dict(say="an amateur title", any=["amateur ring champion", "trophies won"],
                 years=(3, 1.5, 6), share=0.3, contests_y=6, forks=["take"],
                 demand=dict(hours=15, money=0.08, entry=0, energy=0.8),
                 window=dict(every=1, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="paid to fight", any=["professional athlete"], height="Known",
                 years=(3, 1, 6), share=0.15, contests_y=3, forks=["go_on", "take"],
                 demand=dict(hours=25, money=0.05, entry=0.05, energy=0.9),
                 window=dict(every=1, open_weeks=52, deadline_age=35, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=1, kept_by=["bouts", "the yearly medical"])),
            dict(say="a title belt", any=["ring title holder", "known across the country"], height="Notable",
                 years=(5, 2, 10), share=0.1, contests_y=3, forks=["take"],
                 demand=dict(hours=25, money=0, entry=0, energy=0.9), window=None, upkeep=None),
        ]),

    # Clock: estimate from martial-arts schools (first gradings within a year; the first-degree belt usually 4 to 6
    # years from the start, reached by about 1 in 10 of those who start; a school of one's own some years after that).
    # Shares: estimate. Gradings are the contests; open competitions stay optional, so `winning` is left out. Windows
    # (gradings a few times a year; the first-degree grading yearly), demands (an instructor's entry is the hall and
    # the insurance) and upkeep (an instructor's licence and background check are renewed every few years): estimate.
    "to earn a black belt": dict(
        shape="competition", face="R U W", sphere="gather", domain="", calling=True,
        dreams=["a black belt"],
        thing="martial arts", doing="training", contest="a grading",
        places=["gather.games", "gather.hall"],
        people=dict(coach="an instructor", rival="a training partner who grades first", peer="the others in the class",
                    patron="the head of the school"),
        round=["a club across town with another style", "a summer training camp",
               "the class at the training hall twice a week"],
        prep=["strength", "discipline"], meets=["competence", "belonging"],
        below="{N} practises the same kick in the hallway until the family stops noticing",
        tribal="to master the old fighting dance the hunters teach the young",
        magic="to earn the master's sash of the order that trains the tower guards",
        skip=[2],   # 4 rungs: taking part, regular, (winning left out), master (the belt), summit (a school)
        rungs=[
            dict(say="a place in a training hall", any=["boxing or martial arts"],
                 years=(0.5, 0.25, 1), share=0.9, start=(5, 8, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.06, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="the first gradings passed", any=["graded martial artist"],
                 years=(1.5, 0.5, 3), share=0.6, contests_y=3, forks=["pay"],
                 demand=dict(hours=4, money=0.08, entry=0.03, energy=0.6),
                 window=dict(every=0.33, open_weeks=1, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="the first-degree belt", any=["first-degree belt holder"],
                 years=(3, 2, 5), share=0.3, contests_y=2, forks=["go_on"],
                 demand=dict(hours=6, money=0.08, entry=0.05, energy=0.6),
                 window=dict(every=1, open_weeks=1, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a school of your own", any=["martial arts instructor"],
                 req="was('first-degree belt holder')", height="Known",
                 years=(6, 3, 12), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=12, money=0.1, entry=0.4, energy=0.6), window=None,
                 upkeep=dict(of="credential", years=3, kept_by=["teaching classes", "a refresher course"])),
        ]),

    # ================================================================ craft

    # Clock: apprenticeships take 3 to 4 years to a trade ticket; a name for good work some 5 to 10 years after; a
    # master or chartered title commonly 10 or more years into the trade; the last rungs are for very few. Shares:
    # estimate. Demands (hours beyond the paid week: college, a portfolio, own jobs; tools are the big entry) and
    # upkeep (site safety cards are renewed every five years): estimate. Trade tests sit twice a year: estimate.
    "to build things that last": dict(
        shape="craft", face="W U", sphere="prod", domain="career", calling=True,
        dreams=["an architect", "a master of one's guild"],
        thing="building", doing="building", contest="an inspection",
        places=["prod.craft", "learn.higher"],
        people=dict(coach="a master builder", rival="another apprentice on the site", peer="the crew on site",
                    patron="a client with a big job"),
        round=["a firm across town that takes apprentices", "a cousin's building firm",
               "the college's trade course, one evening every week of term"],
        prep=["the workshop", "study"], meets=["competence", "meaning"],
        below="{N} checks every shelf they put up twice with a spirit level, and it never comes down",
        tribal="to build shelters, boats and fish-traps the clan still uses long after you are gone",
        magic="to raise walls and bridges in the guild's way, made to stand for centuries",
        area="craft", spark="the first wall laid true",
        rungs=[
            dict(say="a trade in your hands",
                 any=["apprentice", "building trade", "carpenter", "builder", "machinist", "welder"],
                 years=(1, 0.5, 2), share=0.9, start=(15, 18, 30), contests_y=0, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="a ticket and tools of your own",
                 any=["trade ticket", "tools of one's own", "site safety card", "welding certificate", "civil engineer"],
                 years=(3, 2, 5), share=0.7, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.05, entry=0.15, energy=0.5),
                 window=dict(every=0.5, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=5, kept_by=["site work", "a refresher course"])),
            dict(say="a name for work that holds",
                 any=["chartered status", "a maker's hallmark", "master craftsperson", "apprentice of one's own"],
                 height="Known",
                 years=(6, 3, 12), share=0.35, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="work people travel to see", any=["known across the country"],
                 req="was('master craftsperson') | has('chartered status') | was('architect') | was('civil engineer') | was('builder') | was('carpenter')", height="Notable",
                 years=(10, 5, 20), share=0.08, contests_y=1, forks=["go_on", "take"],
                 demand=dict(hours=10, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a building that stands for generations", any=["a work that outlives you"],
                 req="was('master craftsperson') | has('chartered status') | was('architect') | was('civil engineer') | was('builder') | was('carpenter')", height="Historic",
                 years=(10, 5, 25), share=0.1, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: kitchens: a commis or line cook after months; head chef usually 7 to 12 years in, sooner in a small
    # place; a name in town a few years after; a name across the country for few. Shares: estimate. Demands (kitchens
    # are long and tiring; premises of one's own are the big entry) and upkeep (a clientele drifts within a couple of
    # years without the kitchen): estimate.
    "to cook like nobody else": dict(
        shape="craft", face="U R", sphere="gather", domain="career", calling=True,
        dreams=["a chef"],
        thing="cooking", doing="cooking", contest="a night the critics come",
        places=["gather.house", "comm.market", "learn.higher"],
        people=dict(coach="a head chef who takes them on", rival="the cook at the place across the road",
                    peer="the kitchen brigade", patron="a backer for the restaurant"),
        round=["a supper club at home", "a kitchen across town that will take a beginner",
               "a market stall every Saturday"],
        prep=["cooking"], meets=["competence", "belonging"],
        below="{N} never makes the same dish twice, and the kitchen smells of something new every night",
        tribal="to cook the feast meat so that every clan at the gathering asks how it was done",
        magic="to be the cook whose table the travellers cross the realm to sit at",
        area="craft", spark="the dish that has never been made before",
        rungs=[
            dict(say="cooking for strangers",
                 any=["cooking for a crowd", "baking", "food hygiene certificate", "cook", "baker", "community-kitchen volunteer"],
                 years=(1, 0.5, 2), share=0.9, start=(14, 18, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=6, money=0.03, entry=0.03, energy=0.5), window=None, upkeep=None),
            dict(say="a kitchen of your own to run", any=["head chef", "café or bar owner", "premises of one's own"],
                 years=(7, 4, 12), share=0.3, contests_y=1, forks=["pay"],
                 demand=dict(hours=10, money=0.05, entry=0.6, energy=0.8), window=None, upkeep=None),
            dict(say="the place people cross town for",
                 any=["loyal clientele", "good name in town", "name on the local scene"],
                 height="Known",
                 years=(3, 1, 6), share=0.4, contests_y=2, forks=["take"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.7), window=None,
                 upkeep=dict(of="access", years=2, kept_by=["running the kitchen"])),
            dict(say="a cook the country talks about", any=["known across the country"],
                 req="was('head chef') | was('cook') | was('café or bar owner') | was('baker')", height="Notable",
                 years=(5, 2, 10), share=0.08, contests_y=2, forks=["go_on", "take"],
                 demand=dict(hours=10, money=0.02, entry=0, energy=0.7), window=None, upkeep=None),
            dict(say="a dish the country still cooks", any=["a work that outlives you"],
                 req="was('head chef') | was('cook') | was('café or bar owner') | was('baker')", height="Historic",
                 years=(10, 5, 25), share=0.06, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # Clock: estimate from game makers' paths (a first small game finished within a year of starting; a first studio
    # job after a degree or a portfolio, 3 to 5 years; leading a game some 5 years in; a game people talk about, then
    # one millions play, for few). Shares: estimate. Demands (a computer is the entry; a course the second) and upkeep
    # (the tools move on, so a developer's skill dates after a few idle years): estimate.
    "to make video games": dict(
        shape="craft", face="U R", sphere="arts", domain="career", calling=True,
        dreams=["to make video games"],
        thing="games", doing="making games", contest="a game jam",
        places=["arts.screen", "learn.higher", "gather.circle"],
        people=dict(coach="a developer who reviews their work", rival="a friend making a better game",
                    peer="the game-jam crowd", patron="a publisher"),
        round=["making games online with people met there", "the college's evening course",
               "the game jam held every month"],
        prep=["writing code", "drawing"], meets=["competence", "meaning"],
        below="{N} pulls apart every game to see how it works, then builds a worse one, then a better one",
        tribal="to make the games of pebbles and sticks that the children of every camp play",
        magic="to make the enchanted puzzle-boxes the court's children play with for hours",
        rungs=[
            dict(say="a first game finished", any=["hobby game maker"],
                 years=(1, 0.5, 3), share=0.9, start=(10, 14, 35), contests_y=2, forks=["go_on"],
                 demand=dict(hours=8, money=0.03, entry=0.1, energy=0.4), window=None, upkeep=None),
            dict(say="paid to make games", any=["video-game developer"],
                 years=(4, 2, 7), share=0.25, contests_y=2, forks=["pay"],
                 demand=dict(hours=10, money=0.1, entry=0.1, energy=0.5), window=None,
                 upkeep=dict(of="proficiency", years=3, kept_by=["making games", "writing code"])),
            dict(say="a game with your name on it", any=["lead game designer", "founder of a firm"],
                 years=(5, 3, 10), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a game people talk about", any=["a cult following", "name in the field"], height="Known",
                 years=(4, 2, 8), share=0.2, contests_y=1, forks=["go_on", "take"],
                 demand=dict(hours=10, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a game millions play", any=["known across the country", "a household name"],
                 req="was('video-game developer') | was('lead game designer') | was('founder of a firm')",
                 height="Notable",
                 years=(5, 2, 12), share=0.1, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # ================================================================ art

    # Clock: aims-coverage.md [2] (Ericsson, Krampe and Tesch-Romer 1993: the best student violinists had about
    # 10,000 hours by 20, from starts at 5 to 8); playing in a group after 2 to 4 years; paid work in the twenties;
    # a name some years after. Shares: estimate. Demands (the instrument is the entry; lessons the yearly cost), the
    # window (paid posts and conservatory places go through a yearly audition season) and upkeep (playing at a paid
    # standard slips after a couple of idle years): estimate.
    "to master an instrument": dict(
        shape="art", face="U", sphere="arts", domain="", calling=True,
        dreams=["to master the piano"],
        thing="the instrument", doing="playing", contest="a recital",
        places=["arts.song", "learn.higher"],
        people=dict(coach="a music teacher", rival="the other player who wants the same chair",
                    peer="the others they play with", patron="a patron who lends a fine instrument"),
        round=["a teacher across town", "lessons online", "the community orchestra that rehearses every week"],
        prep=["music practice", "a stage"], meets=["competence", "meaning"],
        below="{N} practises the same four bars until the neighbours know them by heart, and then a little longer",
        tribal="to play the bone flute so well that every fire falls quiet to listen",
        magic="to master an instrument the guild of players counts among its finest",
        area="art", spark="the piece that finally plays itself",
        rungs=[
            dict(say="an instrument in your hands", any=["musical instrument", "instrument of one's own"],
                 years=(1, 0.5, 2), share=0.9, start=(5, 9, 20), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0.15, energy=0.3), window=None, upkeep=None),
            dict(say="playing with others", any=["amateur band member", "folk musician", "congregation musician",
                                                 "choir member"],
                 years=(3, 1, 6), share=0.6, contests_y=2, forks=["pay"],
                 demand=dict(hours=8, money=0.1, entry=0.05, energy=0.4), window=None, upkeep=None),
            dict(say="paid to play", any=["session player", "music teacher", "touring musician"],
                 years=(6, 3, 10), share=0.15, contests_y=3, forks=["take"],
                 demand=dict(hours=20, money=0.1, entry=0.1, energy=0.5),
                 window=dict(every=1, open_weeks=8, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="proficiency", years=2, kept_by=["practice", "playing work"])),
            dict(say="a name for the playing", any=["name on the local scene", "good notices", "name in the field"],
                 height="Known",
                 years=(5, 2, 10), share=0.3, contests_y=3, forks=["go_on", "take"],
                 demand=dict(hours=20, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="heard across the country", any=["known across the country"],
                 req="was('session player') | was('touring musician') | was('music teacher') | has('name on the local scene')",
                 height="Notable",
                 years=(5, 2, 12), share=0.12, contests_y=2, forks=["take"],
                 demand=dict(hours=20, money=0.03, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: estimate from dance training (vocational training from about 10 to 18; a company place at 18 to 22 for
    # a minority; a company or a name of one's own some years after; dance careers are short, so the later rungs lean
    # on teaching and making dances). Shares: estimate. The window (company auditions each year, rarely a first place
    # after about 28), demands and upkeep (a company dancer's form fades within a year out of class): estimate.
    "to dance": dict(
        shape="art", face="R G", sphere="arts", domain="", calling=True,
        dreams=[],
        thing="dance", doing="dancing", contest="a showcase",
        places=["arts.stage", "gather.hall", "gather.great"],
        people=dict(coach="a dance teacher", rival="a dancer who always gets the front line",
                    peer="the dancers at the studio", patron="a choreographer who keeps casting them"),
        round=["a street-dance crew in the park", "a company across town",
               "the open class at the community hall every week"],
        prep=["a stage", "strength"], meets=["belonging", "meaning"],
        below="{N} cannot sit still once the music starts, at a wedding, in a kitchen or at a bus stop",
        tribal="to lead the dances round the fire at every gathering",
        magic="to dance in the great halls where the old steps still hold power",
        area="art", spark="the empty floor at the wedding",
        rungs=[
            dict(say="dancing whenever the music plays", any=["dancing", "youth theatre member"],
                 years=(0.5, 0.25, 1.5), share=0.9, start=(4, 10, 25), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.03, entry=0.02, energy=0.5), window=None, upkeep=None),
            dict(say="a company to dance with",
                 any=["a company that feels like family", "amateur actor", "a fringe slot"],
                 years=(3, 1, 6), share=0.45, contests_y=2, forks=["pay"],
                 demand=dict(hours=10, money=0.1, entry=0.05, energy=0.7),
                 window=dict(every=1, open_weeks=8, deadline_age=28, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="proficiency", years=1, kept_by=["class", "performing"])),
            dict(say="a floor of your own and a name on it",
                 any=["a company of your own", "name on the local scene", "a lead role to remember"],
                 req="has('dancing') | was('youth theatre member')", height="Known",
                 years=(6, 3, 12), share=0.2, contests_y=2, forks=["take"],
                 demand=dict(hours=15, money=0.1, entry=0.3, energy=0.7), window=None, upkeep=None),
            dict(say="danced for the whole country", any=["known across the country", "a cult following"],
                 req="has('dancing')", height="Notable",
                 years=(5, 2, 10), share=0.1, contests_y=2, forks=["go_on", "take"],
                 demand=dict(hours=20, money=0.05, entry=0, energy=0.8), window=None, upkeep=None),
            dict(say="a dance still taught", any=["a work that outlives you"],
                 req="has('dancing')", height="Historic",
                 years=(10, 5, 25), share=0.08, contests_y=1, forks=["take"],
                 demand=dict(hours=15, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # Clock: estimate from local music scenes (a first band within a year of picking up an instrument with friends;
    # a first gig to strangers in a year or two; a crowd that comes back after a few years of gigs; a record and a
    # first tour out of town for a few; most bands split within five years). Shares: estimate. Demands (gear is the
    # entry) and upkeep (a local crowd drifts after a couple of years without gigs): estimate. Gigs have no window.
    "to play in a band": dict(
        shape="art", face="R", sphere="arts", domain="", calling=True,
        dreams=["to play in a band"],
        thing="the band", doing="playing with the band", contest="a gig",
        places=["arts.song", "gather.hall", "gather.great"],
        people=dict(coach="an older musician who shows them the ropes", rival="the other band on the local scene",
                    peer="the rest of the band", patron="a promoter who books them"),
        round=["a rehearsal room across town", "putting the songs online",
               "the open-mic night at the community hall every week"],
        prep=["music practice", "a stage"], meets=["belonging", "meaning"],
        below="{N} drums on every table and knows the bass line of every song on the radio",
        tribal="to drum with the others until every fire in the camp is dancing",
        magic="to play in a troupe of travelling minstrels the whole realm waits for",
        rungs=[
            dict(say="a band of your own", any=["amateur band member"],
                 years=(1, 0.25, 3), share=0.9, start=(12, 16, 30), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0.15, energy=0.4), window=None, upkeep=None),
            dict(say="gigs to real crowds", any=["gigging musician"],
                 years=(1.5, 0.5, 3), share=0.6, contests_y=4, forks=["pay"],
                 demand=dict(hours=6, money=0.08, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="a crowd that comes back", any=["name on the local scene", "a cult following"],
                 years=(3, 1, 6), share=0.3, contests_y=6, forks=["go_on", "round"],
                 demand=dict(hours=8, money=0.06, entry=0, energy=0.6), window=None,
                 upkeep=dict(of="access", years=2, kept_by=["gigs"])),
            dict(say="a record out and a tour", any=["touring musician", "royalties"], height="Known",
                 years=(3, 1, 6), share=0.2, contests_y=6, forks=["take"],
                 demand=dict(hours=15, money=0.05, entry=0.1, energy=0.7), window=None, upkeep=None),
            dict(say="songs the country sings along to", any=["known across the country", "a household name"],
                 req="was('touring musician') | has('name on the local scene')", height="Notable",
                 years=(5, 2, 10), share=0.08, contests_y=4, forks=["take"],
                 demand=dict(hours=15, money=0, entry=0, energy=0.7), window=None, upkeep=None),
        ]),

    # ================================================================ knowledge

    # Clock: estimate (a listener's name among friends comes early; being sought out by strangers after some years of
    # volunteering or a counselling course; the one everyone asks usually in mid-life; a voice beyond the town for
    # few). Shares: estimate. Demands: estimate (cheap in money, a few evenings a week). No window, no upkeep.
    "to be the one people come to for advice": dict(
        shape="knowledge", face="W U", sphere="", domain="community", calling=True,
        dreams=["an elder whose counsel the clans seek", "the one the elders ask"],
        thing="advice", doing="listening and advising", contest="a hard question with no easy answer",
        places=["gather.talk", "gather.circle", "care.houses"],
        people=dict(coach="an older counsellor", rival="the one whose word the street used to follow",
                    peer="the other volunteers on the listening line",
                    patron="a community leader who sends people their way"),
        round=["a listening line answered from home", "a counselling course at the college",
               "the drop-in advice evening every week"],
        prep=["listening"], meets=["belonging", "meaning"],
        below="{N} is the friend the others ring at midnight, and somehow always has a sensible answer",
        tribal="to be the elder whose counsel the clans seek",
        magic="to be the counsellor every guild-hall sends for",
        area="knowledge", spark="a friend at the kitchen table at midnight",
        skip=[4],   # 4 steps: student, practitioner, contributor (the one everyone asks), authority; (a finding that lasts left out)
        rungs=[
            dict(say="a good listener", any=["calming people down", "finding things out", "counselling",
                                              "book-club organiser"],
                 years=(1, 0.5, 3), share=0.9, start=(14, 25, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=2, money=0, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="people bring their troubles", any=["community-mediation volunteer", "hospice volunteer",
                                                          "lay religious teacher", "private tutor", "teaching"],
                 years=(4, 2, 8), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=4, money=0.02, entry=0.05, energy=0.4), window=None, upkeep=None),
            dict(say="the one everyone asks", any=["the one everyone asks", "good name in town"], height="Known",
                 years=(8, 4, 15), share=0.35, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="advice heard far beyond the street", any=["known across the country"],
                 req="has('the one everyone asks') | was('the one everyone asks')", height="Notable",
                 years=(8, 4, 20), share=0.1, contests_y=1, forks=["go_on", "take"],
                 demand=dict(hours=6, money=0, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: a doctorate takes 4 to 6 years after a first degree; a name in the field 5 to 10 years after; for amateur
    # scholars the same steps take longer. Shares: estimate (a few in 100 of those who start reach a national name).
    # Demands: estimate (study fees or books in the long middle). Amateur and university roads both run all year, so
    # no window; knowledge kept by a name does not fade, so no upkeep.
    "to know one thing better than anyone": dict(
        shape="knowledge", face="U", sphere="learn", domain="", calling=True,
        dreams=["to know every bird by its song", "to know the name of every star", "to read every book in the great library"],
        thing="the subject", doing="studying", contest="a paper sent for review",
        places=["learn.keeping", "learn.higher"],
        people=dict(coach="a professor who answers their letters", rival="a scholar with a rival theory",
                    peer="the other regulars in the reading room", patron="a funder"),
        round=["the university's open lectures", "letters to the people who know the subject",
               "the library's reading room, open every evening"],
        prep=["study"], meets=["competence", "meaning"],
        below="{N} has read everything the library holds on one odd subject, and keeps asking for more",
        tribal="to know one thing, the stars or the herds or the stones, better than any elder of the clans",
        magic="to master one corner of the archives so well that the tower's scholars come asking",
        area="knowledge", spark="the question nobody at the library could answer",
        rungs=[
            dict(say="a question that will not let go",
                 any=["finding things out", "reader's ticket", "amateur astronomer in a club", "citizen scientist"],
                 years=(1, 0.5, 3), share=0.9, start=(8, 16, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="years of patient study",
                 any=["archive research", "fieldwork", "collection of one's own", "a research project under way"],
                 years=(5, 3, 10), share=0.5, contests_y=1, forks=["pay"],
                 demand=dict(hours=10, money=0.1, entry=0.1, energy=0.4), window=None, upkeep=None),
            dict(say="the one everyone asks",
                 any=["the one everyone asks", "name in the field", "published research"],
                 height="Known",
                 years=(6, 3, 12), share=0.3, contests_y=2, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="known across the country for it", any=["known across the country", "a finding that held up"],
                 req="has('name in the field') | has('published research') | has('the one everyone asks')", height="Notable",
                 years=(8, 4, 15), share=0.15, contests_y=2, forks=["go_on", "take"],
                 demand=dict(hours=12, money=0.03, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="the book on the subject", any=["a work that outlives you"],
                 req="has('name in the field') | has('published research') | has('the one everyone asks')", height="Historic",
                 years=(8, 4, 20), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=12, money=0, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: teacher training takes 1 to 4 years after school or a degree; former pupils coming back to say thanks
    # usually after 5 to 10 years in post; a teacher known nationally is rare. Shares: estimate (many new teachers
    # leave within five years). The window (training courses take one intake a year, applied for over a term),
    # demands (training fees are the entry) and upkeep (the background check for working with children is renewed
    # every few years): estimate.
    "to teach well": dict(
        shape="knowledge", face="U", sphere="learn", domain="career", calling=True,
        dreams=["a teacher"],
        thing="teaching", doing="teaching", contest="an observed lesson",
        places=["learn.higher", "learn.keeping"],
        people=dict(coach="an old teacher who mentors them", rival="a colleague who wants the same post",
                    peer="the staff room", patron="a head teacher who backs them"),
        round=["a school across town", "evening classes for adults", "tutoring after school every week"],
        prep=["teaching", "study"], meets=["meaning", "belonging"],
        below="{N} is the one the younger ones come to with their homework, and is quietly pleased when it clicks",
        tribal="to teach the young ones the tracks, the plants and the old ways so that they never forget",
        magic="to be a master at the academy whose pupils carry the lessons all their lives",
        area="knowledge", spark="the lesson that finally lands",
        skip=[4],   # 4 steps: student, practitioner, contributor (pupils who come back), authority; (a finding that lasts left out)
        rungs=[
            dict(say="explaining things to others", any=["teaching", "private tutor", "teaching assistant",
                                                          "youth coach"],
                 years=(1, 0.5, 3), share=0.9, start=(14, 20, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="a class of your own", any=["teacher", "music teacher", "drama teacher", "art teacher",
                                                 "lay religious teacher", "community language teacher"],
                 years=(4, 2, 6), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.1, entry=0.3, energy=0.6),
                 window=dict(every=1, open_weeks=12, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=3, kept_by=["teaching", "a background check"])),
            dict(say="pupils who come back to say thank you", any=["pupils who remember you", "former students",
                                                                     "good name in town"], height="Known",
                 years=(8, 4, 15), share=0.5, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a teacher the country knows of", any=["known across the country", "professor"],
                 req="was('teacher') | was('professor') | was('private tutor') | was('music teacher') | was('drama teacher')",
                 height="Notable",
                 years=(10, 5, 20), share=0.05, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: estimate (safe identification of the common edible species takes a few seasons with someone who knows;
    # selling to a market or a kitchen a few years after; a local name after some years; a field guide in print for
    # few). Shares: estimate. The window (selling comes in the gathering season, about three months a year) and
    # demands: estimate. Knowing the woods does not fade quickly, so no upkeep.
    "to know every root and mushroom": dict(
        shape="knowledge", face="B G", sphere="prod", domain="", calling=True,
        dreams=["to find every rare herb in the deep woods", "a garden of one's own"],
        thing="foraging", doing="foraging", contest="a basket checked by an expert",
        places=["prod.wild", "comm.market"],
        people=dict(coach="an old forager who knows the woods", rival="a forager who works the same woods",
                    peer="the foraging group", patron="a chef who buys all they bring"),
        round=["woods further out of town", "the field guides at the library",
               "the foraging walk every autumn weekend"],
        prep=["the outdoors", "naturalist"], meets=["competence", "meaning"],
        below="{N} comes home from every walk with pockets full of things that might be good to eat",
        tribal="to know every root, berry and fungus of the clan's woods, and which ones heal",
        magic="to know every herb and toadstool of the old forest, and what each one is worth to the potion-makers",
        area="knowledge", spark="the first basket that sells",
        rungs=[
            dict(say="eyes on the ground", any=["knowing the woods", "growing food"],
                 years=(1, 0.5, 3), share=0.9, start=(6, 20, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.01, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="what the woods give, sold", any=["market trader", "contact in the trade", "field permit"],
                 years=(3, 1, 6), share=0.4, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.02, entry=0.05, energy=0.4),
                 window=dict(every=1, open_weeks=12, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="the one everyone asks", any=["the one everyone asks", "name on the local scene"],
                 height="Known",
                 years=(6, 3, 12), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.01, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="the guide the country reads", any=["book in print", "known across the country"],
                 req="has('knowing the woods')", height="Notable",
                 years=(8, 4, 15), share=0.1, contests_y=1, forks=["go_on", "take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="a field guide still in every pocket", any=["a work that outlives you"],
                 req="has('knowing the woods')", height="Historic",
                 years=(10, 5, 25), share=0.08, contests_y=0, forks=["take"],
                 demand=dict(hours=6, money=0, entry=0, energy=0.4), window=None, upkeep=None),
        ]),
}


# ==== part b: from v25-prep/library/fields/fields-b.py, its header:
# Chroma library, modern Earth: v25 prep, fields part b, the career shape (Library writer b, 10-23). DRAFT, nothing
# reads it: the Library pours it into chroma-library/earth_fields.py (FIELDS_EARTH) on Friday 10-23 21:00 (Emren's
# time), and NEW_TITLES into earth_perks_titles.py with their doors. Format: chroma-engine/notes/v25/aims-shape.md
# sections 3 and 8 (the chess entry, key for key, plus the keys frozen later in section 3: prep, meets, and per rung
# demand, window, upkeep); brief: chroma-ideas/v25-prep/library/briefs/FIELDS.md and V25-DECISIONS.md ("Aims").
#
# Holds the 11 v1 Earth aims of the career shape (areas standing, wealth, care) and the one new dream field of that
# shape ("to be famous"). v1's name, face, sphere, domain, calling, dreams, below, tribal, magic, spark and area are as
# v1 has them, and each step's say, any, req and height unchanged. A v1 aim with 4 steps maps onto the shape's 5 rungs
# (a foot in, established, senior, leading, the top) with `skip` naming the one rung it leaves out.
#
# Clocks: `years` is (median, 10th, 90th percentile) of steady effort from the rung below; `share` is of those who
# keep at it, the share who reach that rung, so the shares multiply down the ladder. Sources are named in the comment
# above each field; "estimate" where no count is known. Ways in (V25-DECISIONS "Aims"): each field's places, people
# and `round` give at least three ways in, and the last `round` entry is the recurring one (a weekly, monthly or yearly
# thing).
#
# Demands (all estimates): `hours` a week at steady intensity are what the aim asks ON TOP OF the paid job's own hours
# (evening study, extra shifts, committee nights, drill nights), because a career rung's work hours are already the
# job title's; once a rung's title is the job itself (a founder, a full-time creator) only the extra is counted.
# `money` is the share of a year's free money it costs each year, `entry` a one-time cost (fees, tools, a deposit,
# stock), `energy` how tiring (0 to 1). `window` only where real outside timing decides most of the rung's routes (a
# yearly promotion round, exam sittings, committee elections, recruitment rounds); `upkeep` only where the named part
# truly fades without use (a first-aid certificate, a professional registration, fitness, an online following).
# `meets` names needs from the catalogue's set (autonomy, belonging, competence, meaning, safety).

_FIELDS_B = {

    # Clock: about 24 years from a first job to chief executive in executive-search firms' studies of large firms (the
    # average new chief executive is in their mid-fifties); first management post about 3 to 5 years in; executives
    # are a few in 100 of the workforce. Shares: estimate. Demands: estimate; promotions mostly come in a yearly round.
    "to rise to the top of the firm": dict(
        shape="career", face="W B", sphere="comm", domain="career", calling=True, area="standing",
        spark="the day the boss is off sick",
        dreams=["to reach the top of a big firm", "a merchant prince"],
        thing="the firm", doing="working your way up the firm", contest="a promotion round",
        places=["comm.market", "learn.higher", "rule.counsel"],
        people=dict(coach="a manager who takes you under their wing", rival="a colleague up for the same job",
                    peer="the people on your floor", patron="a director who speaks up for you"),
        round=["a move to another firm", "the evening management course", "the yearly appraisal, asked for in writing"],
        below="{N} is first in the door at the Saturday job, watching how the manager does it",
        tribal="to rise to the head of the clan's traders, first among those who barter",
        magic="to rise to the head of the merchants' guild",
        prep=["people skills", "numbers", "business"], meets=["competence", "belonging"],
        skip=[2],   # 4 steps: a foot in, established, (senior left out), leading, the top
        rungs=[
            dict(say="a foot on the ladder", any=["office clerk", "salesperson", "shop assistant", "accountant"],
                 years=(1, 0.3, 3), share=0.9, start=(16, 21, 35), contests_y=1, forks=["go_on"],
                 demand=dict(hours=4, money=0, entry=0.02, energy=0.4), window=None, upkeep=None),
            dict(say="people to manage", any=["shift manager", "inner circle at work", "organising people"],
                 years=(4, 2, 9), share=0.55, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.5),
                 window=dict(every=1, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a seat at the top table", any=["stake in the firm", "name in the field", "friend in power"],
                 height="Known",
                 years=(13, 7, 22), share=0.08, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=10, money=0.05, entry=0.2, energy=0.7), window=None, upkeep=None),
            dict(say="the head of the firm, known well beyond it", any=["known across the country"],
                 req="was('stake in the firm') | was('inner circle at work') | was('shift manager')",
                 height="Notable",
                 years=(7, 3, 14), share=0.1, contests_y=0.5, forks=["take"],
                 demand=dict(hours=12, money=0, entry=0, energy=0.8), window=None, upkeep=None),
        ]),

    # Clock: apprenticeships and trade training take 3 to 4 years; expert-level work about ten years of deliberate
    # practice beyond that (Ericsson and others); the best in a country is a handful per trade. Shares: estimate.
    # Demands: estimate; apprenticeships and college places start once a year; a registration lapses without practice
    # and its yearly training, and a name in the field fades after years away.
    "to be the best at what I do": dict(
        shape="career", face="U B", sphere="", domain="career", calling=True, area="standing",
        spark="the job only the best could finish",
        dreams=["to reach the top of a big firm"],
        thing="the work", doing="getting better at the work", contest="a skills competition",
        places=["prod.craft", "learn.higher"],
        people=dict(coach="an old hand who shows you how", rival="the best one in the next workshop",
                    peer="the others on the job", patron="a client who sends the hard jobs your way"),
        round=["a better shop across town", "a course in the hardest part of the trade",
               "the yearly skills competition"],
        below="{N} redoes the work nobody would check, because it was only nearly right",
        tribal="to be the best hunter, carver or tracker of the clans, and have every band know it",
        magic="to be the finest of the guild, the one whose mark the masters envy",
        prep=["the trade"], meets=["competence", "meaning"],
        skip=[2],   # 4 steps: a foot in, established, (senior left out), leading, the top
        rungs=[
            dict(say="a trade to get good at", any=["apprentice", "trade ticket", "professional registration",
                                                    "school-leaving certificate"],
                 years=(3, 1, 5), share=0.9, start=(15, 18, 30), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=6, money=0.05, entry=0.1, energy=0.5),
                 window=dict(every=1, open_weeks=8, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=5, kept_by=["work in the trade", "refresher course"])),
            dict(say="better than the people beside you", any=["reliable record", "inner circle at work", "rank"],
                 years=(4, 2, 8), share=0.5, contests_y=1, forks=["round"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a name in the field", any=["name in the field", "chartered status"], height="Known",
                 years=(8, 4, 15), share=0.15, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=8, money=0.05, entry=0.1, energy=0.6), window=None,
                 upkeep=dict(of="proficiency", years=8, kept_by=["work in the trade", "teaching the trade"])),
            dict(say="the best in the country", any=["known across the country"],
                 req="has('name in the field') | has('chartered status') | has('inner circle at work')",
                 height="Notable",
                 years=(8, 3, 18), share=0.06, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.7), window=None, upkeep=None),
        ]),

    # Clock: an accounting degree or trainee post 3 to 4 years; professional (chartered) qualification about 3 more
    # years of exams beside work, with pass rates near half per sitting; a first investment usually comes some years
    # into working life. A national name in money is a few in 1,000 of those qualified. Shares: estimate. Demands:
    # estimate; professional exams sit about twice a year and must usually be finished within some years; the
    # qualification needs yearly training hours to stay current.
    "to keep a sharp eye on money": dict(
        shape="career", face="U B", sphere="comm", domain="career", calling=True, area="wealth",
        spark="the accounts that do not add up",
        dreams=["a keeper of the treasure vaults", "a business of one's own"],
        thing="money", doing="keeping the books", contest="the professional exams",
        places=["comm.credit", "learn.higher", "learn.keeping"],
        people=dict(coach="an old bookkeeper who checks your sums", rival="the sharp one in the next office",
                    peer="the others studying for the exams", patron="a partner at the firm"),
        round=["night school in accounts", "a small firm that needs its books done",
               "the club's books, kept every month"],
        below="{N} keeps a little book of every coin that comes and goes, and it always adds up",
        tribal="to keep the tally of the clan's stores, so that no winter finds them short",
        magic="to keep the vault-books of a great house, where every coin is counted twice",
        prep=["numbers", "saving money"], meets=["competence", "safety"],
        rungs=[
            dict(say="every coin counted", any=["bookkeeping", "savings"],
                 years=(1, 0.3, 3), share=0.9, start=(10, 16, 30), contests_y=0, forks=["go_on"],
                 demand=dict(hours=2, money=0, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="the books in your hands", any=["accountant", "club treasurer", "data analyst"],
                 years=(4, 2, 7), share=0.5, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.1, entry=0.15, energy=0.5), window=None, upkeep=None),
            dict(say="money that works for you", any=["shares", "flat to rent out", "stake in the firm",
                                                      "good credit"],
                 years=(5, 2, 12), share=0.5, contests_y=0.5, forks=["take"],
                 demand=dict(hours=2, money=0.15, entry=0.1, energy=0.2), window=None, upkeep=None),
            dict(say="the one trusted with the money", any=["chartered status", "name in the field"],
                 height="Known",
                 years=(5, 3, 10), share=0.25, contests_y=2, forks=["pay", "go_on"],
                 demand=dict(hours=10, money=0.08, entry=0.1, energy=0.7),
                 window=dict(every=0.5, open_weeks=2, deadline_age=None, deadline_years=7, pause_stops=False),
                 upkeep=dict(of="credential", years=3, kept_by=["professional practice", "yearly training hours"])),
            dict(say="a name in money across the country", any=["known across the country"],
                 req="was('accountant') | has('chartered status') | has('shares') | has('stake in the firm')",
                 height="Notable",
                 years=(12, 5, 25), share=0.04, contests_y=0.5, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # Clock: local committee seats usually come after a few years of turning up; local councillors are mostly in
    # their fifties and sixties, with several years in local groups first; council elections every few years.
    # Shares: estimate. Demands: estimate; committee seats are mostly filled at a yearly general meeting (the town
    # hall rung has routes besides elections, so it has no window).
    "to be somebody in this town": dict(
        shape="career", face="B", sphere="", domain="community", calling=True, area="standing",
        spark="the evening the room turns to listen",
        dreams=["to run the town", "a seat on the city council"],
        thing="the town", doing="getting known in town", contest="a vote at the annual meeting",
        places=["gather.hall", "rule.counsel", "rule.voice"],
        people=dict(coach="an old councillor who knows how it works", rival="the one who wants the same seat",
                    peer="the committee regulars", patron="a local business owner who backs you"),
        round=["another club with an empty seat", "the residents' group in the next street",
               "the monthly open meeting at the town hall"],
        below="{N} always knows who sits where at every do, and minds which table they were given",
        tribal="to sit near the fire's heart when the clan gathers, where every word is heard",
        magic="to have a name the whole market town bows to, and a seat on the guildhall bench",
        prep=["people skills", "public speaking"], meets=["belonging", "meaning"],
        skip=[2],   # 4 steps: a foot in, established, (senior left out), leading, the top
        rungs=[
            dict(say="a face people know", any=["club member", "regular at the local", "on the team"],
                 years=(2, 0.5, 4), share=0.9, start=(14, 20, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.03, entry=0.02, energy=0.2), window=None, upkeep=None),
            dict(say="a seat at the table", any=["residents' committee member", "club treasurer",
                                                 "school-governance board member"],
                 years=(4, 1, 10), share=0.45, contests_y=1, forks=["pay"],
                 demand=dict(hours=4, money=0.02, entry=0, energy=0.3),
                 window=dict(every=1, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a voice the town hall hears", any=["voice at the town hall", "local councillor",
                                                          "friend in power"],
                 years=(6, 2, 15), share=0.2, contests_y=0.5, forks=["take", "round"],
                 demand=dict(hours=8, money=0.05, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="a name the whole town knows", any=["good name in town", "mayor"], height="Known",
                 years=(6, 2, 15), share=0.3, contests_y=0.3, forks=["go_on"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: a savings habit takes a year or so; a credit record that banks trust 2 to 7 years; a first holding of
    # shares a few years more; income from property or a paid-off home usually 10 to 25 years (loan terms near 25
    # years). Shares: estimate. Demands: estimate; the money is what is set aside or put in each year, the top rung's
    # entry a deposit.
    "to make money work for me": dict(
        shape="career", face="B", sphere="comm", domain="", calling=False, area="wealth",
        spark="the first money that grows on its own",
        dreams=["a fortune of one's own", "to cross the mountains and come back rich"],
        thing="money", doing="putting money to work", contest="a bad year in the markets",
        places=["comm.credit", "comm.market", "learn.keeping"],
        people=dict(coach="an uncle who explains interest", rival="a friend who brags about returns",
                    peer="the others at the investment club", patron="a bank manager who trusts you"),
        round=["a different bank", "a cheaper flat to buy into", "the monthly investment club"],
        below="{N} counts the coins in the jar every week, and asks what interest means before anyone explains",
        tribal="to own the herd that grows while others sleep, and lend out its calves for a share",
        magic="to hold shares in the caravans and let the guild's gold do the travelling",
        prep=["saving money", "numbers"], meets=["safety", "autonomy"],
        skip=[3],   # 4 steps: a foot in, established, senior, (leading left out), the top
        rungs=[
            dict(say="money set aside", any=["savings", "bookkeeping"],
                 years=(1, 0.5, 3), share=0.9, start=(12, 20, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=1, money=0.1, entry=0, energy=0.1), window=None, upkeep=None),
            dict(say="a name the bank trusts", any=["good credit", "striking a deal"],
                 years=(3, 1, 6), share=0.75, contests_y=0, forks=["pay"],
                 demand=dict(hours=1, money=0.05, entry=0, energy=0.1), window=None, upkeep=None),
            dict(say="money in something that grows", any=["shares", "stake in the firm"],
                 years=(3, 1, 8), share=0.6, contests_y=0.5, forks=["take"],
                 demand=dict(hours=2, money=0.2, entry=0.1, energy=0.2), window=None, upkeep=None),
            dict(say="income that comes in while you sleep", any=["flat to rent out", "paid-off home", "inheritance"],
                 years=(12, 6, 25), share=0.25, contests_y=0.5, forks=["pay", "go_on"],
                 demand=dict(hours=3, money=0.25, entry=0.5, energy=0.3), window=None, upkeep=None),
        ]),

    # Clock: about one new firm in five closes in its first year and about half within five years (small-business
    # survival counts); firms that become widely known are a few in 100 of survivors; about a third of those still
    # run well after the founder leaves (estimate). Shares beyond survival: estimate. Demands: estimate; the venture
    # rung is the side venture before it pays (once it is the job, its hours are the job's).
    "to make it big, and fast": dict(
        shape="career", face="B R", sphere="", domain="career", calling=True, area="wealth",
        spark="the deal that doubles overnight",
        dreams=["a merchant prince", "an alchemist's venture of one's own", "to reach the top of a big firm"],
        thing="the business", doing="chasing the next deal", contest="a pitch to investors",
        places=["comm.market", "comm.credit", "gather.night"],
        people=dict(coach="a founder who has done it before", rival="a competitor who copies everything",
                    peer="the others hustling in the market", patron="an investor"),
        round=["a different market", "a partner with money", "the monthly pitch night for new firms"],
        below="{N} sells sweets at a profit in the playground, and already talks about the first million",
        tribal="to come back from the far trading grounds with more than the whole clan owns",
        magic="to turn one lucky cargo into a fleet before the guilds can stop it",
        prep=["business", "trading", "people skills"], meets=["autonomy", "competence"],
        rungs=[
            dict(say="a hustle that pays", any=["selling", "salesperson", "estate agent", "market trader"],
                 years=(1, 0.3, 3), share=0.9, start=(12, 18, 35), contests_y=1, forks=["go_on"],
                 demand=dict(hours=8, money=0.02, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="a venture of your own", any=["founder of a firm", "business partner", "events promoter"],
                 years=(3, 1, 8), share=0.5, contests_y=2, forks=["pay", "take"],
                 demand=dict(hours=20, money=0.3, entry=0.5, energy=0.9), window=None, upkeep=None),
            dict(say="a name in the business", any=["name in the field", "stake in the firm", "inner circle at work"],
                 height="Known",
                 years=(5, 2, 10), share=0.25, contests_y=2, forks=["go_on", "round"],
                 demand=dict(hours=10, money=0.1, entry=0, energy=0.8), window=None, upkeep=None),
            dict(say="the one everyone has heard of", any=["known across the country", "a household name"],
                 req="was('founder of a firm') | has('stake in the firm') | was('events promoter')", height="Notable",
                 years=(6, 2, 15), share=0.05, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0, energy=0.8), window=None, upkeep=None),
            dict(say="a firm that outlasts its founder", any=["a work that outlives you"],
                 req="was('founder of a firm') | has('stake in the firm') | was('events promoter')", height="Historic",
                 years=(15, 8, 30), share=0.3, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=6, money=0, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: a year of regular training builds confidence and the basics of self-defence; union and workplace reps
    # are usually elected after a few years in the job; a public voice locally takes years more. Shares: estimate.
    # Demands: estimate; fitness and the skill to hold your own fade within a couple of years without training.
    "to never be pushed around again": dict(
        shape="career", face="B R", sphere="", domain="community", calling=True, area="standing",
        spark="the day the bully backs down",
        dreams=["to speak for the clan at the gatherings"],
        thing="standing your ground", doing="standing your ground", contest="a face-off at the meeting",
        places=["gather.games", "rule.voice", "gather.circle"],
        people=dict(coach="a trainer at the boxing club", rival="the one who used to lean on you",
                    peer="the ones who have your back", patron="an old union hand"),
        round=["another gym across town", "the union instead of going it alone", "the weekly training night"],
        below="{N} flinches at a raised voice, then stands a little straighter every time",
        tribal="to stand so strong among the hunters that no one takes the best cut of the kill from you again",
        magic="to win such a name in the market town that no guild bully dares lean on you twice",
        prep=["fitness", "people skills"], meets=["safety", "belonging"],
        skip=[3],   # 4 steps: a foot in, established, senior, (leading left out), the top
        rungs=[
            dict(say="able to hold your own", any=["boxing or martial arts", "keeping fit"],
                 years=(1, 0.3, 3), share=0.9, start=(10, 14, 40), contests_y=2, forks=["go_on"],
                 demand=dict(hours=4, money=0.04, entry=0.03, energy=0.6), window=None,
                 upkeep=dict(of="proficiency", years=2, kept_by=["training", "keeping fit"])),
            dict(say="people who stand with you", any=["crew that has your back", "union member", "old comrades"],
                 years=(2, 0.5, 5), share=0.7, contests_y=1, forks=["round"],
                 demand=dict(hours=3, money=0.01, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="someone not to be crossed", any=["not to be crossed", "union rep", "door staff"],
                 years=(5, 2, 10), share=0.35, contests_y=1, forks=["take"],
                 demand=dict(hours=4, money=0, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a voice nobody talks over", any=["voice at the town hall", "local councillor",
                                                        "a name for straight talk"], height="Known",
                 years=(8, 3, 15), share=0.2, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: children of shop families often help from their early teens; about 3 in 10 family firms pass to the
    # second generation and about 1 in 8 to the third (family-business succession studies); handover usually comes
    # in the successor's thirties or forties. Later shares: estimate. Demands: estimate; the handover's entry is a
    # buy-in or the stock and debts taken on.
    "to run the family business": dict(
        shape="career", face="B G", sphere="comm", domain="career", calling=True, area="wealth",
        spark="the day the shop is left in your hands",
        dreams=["to build up the family firm", "to carry on the family holding"],
        thing="the family business", doing="minding the family business", contest="a lean season",
        places=["comm.shop", "comm.market"],
        people=dict(coach="the parent who runs the shop", rival="the new shop down the road",
                    peer="the other traders on the street", patron="a supplier who gives you credit"),
        round=["a job at another shop to learn the trade", "a course in running a business",
               "the weekly market stall"],
        below="{N} does homework at the end of the shop counter, and knows the regulars' orders by heart",
        tribal="to keep the clan's trading post and its old bargains with the river folk",
        magic="to take over the family's apothecary shop and its standing with the guild",
        prep=["the trade", "trading", "numbers"], meets=["belonging", "meaning"],
        skip=[2],   # 4 steps: a foot in, established, (senior left out), leading, the top
        rungs=[
            dict(say="behind the family counter", any=["shop assistant", "market porter", "bookkeeping"],
                 years=(1, 0.3, 3), share=0.9, start=(8, 14, 30), contests_y=0, forks=["go_on"],
                 demand=dict(hours=6, money=0, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="learning the trade", any=["striking a deal", "contact in the trade", "selling"],
                 years=(4, 2, 8), share=0.7, contests_y=0.5, forks=["round"],
                 demand=dict(hours=8, money=0, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="the keys handed over", any=["family business", "shop owner", "premises of one's own"],
                 years=(8, 3, 20), share=0.3, contests_y=1, forks=["take", "pay"],
                 demand=dict(hours=10, money=0.1, entry=0.4, energy=0.7), window=None, upkeep=None),
            dict(say="the business the town trusts", any=["loyal clientele", "good name in town", "old family name"],
                 height="Known",
                 years=(8, 3, 15), share=0.5, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # Clock: a first-aid course takes days, being the one who acts takes longer; rescue and lifeboat volunteers train
    # 1 to 2 years before going out; firefighter recruitment takes many applicants per post, and a paramedic degree 3
    # years; bravery awards and national notice are rare. Shares: estimate. Demands: estimate; first-aid certificates
    # usually run three years; volunteers stood down after a long gap retrain; crews recruit in rounds; paramedics
    # keep their registration through work and training days.
    "to be there when it counts": dict(
        shape="career", face="R W", sphere="prot", domain="career", calling=True, area="care",
        spark="the car in the ditch on the bend",
        dreams=["a firefighter"],
        thing="rescue work", doing="going out on call", contest="a hard call-out",
        places=["prot.rescue", "care.houses", "prot.watch"],
        people=dict(coach="a crew manager", rival="a recruit who always beats your times",
                    peer="the crew on your watch", patron="the station's old hand who puts your name forward"),
        round=["the lifeboat crew down the coast", "a paramedic course instead", "the weekly drill night"],
        below="{N} is always first to the scraped knee in the playground, and never the one who freezes",
        tribal="to be the one who goes down the ravine when a hunter falls",
        magic="to ride with the fire wardens when the lanes burn",
        prep=["fitness", "first aid"], meets=["meaning", "belonging"],
        rungs=[
            dict(say="first on the scene", any=["first-aid certificate", "lifeguard qualification", "swimming"],
                 years=(0.5, 0.2, 2), share=0.9, start=(12, 18, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=1, money=0.01, entry=0.03, energy=0.3), window=None,
                 upkeep=dict(of="credential", years=3, kept_by=["refresher course", "first aid used"])),
            dict(say="trained to go in", any=["search-and-rescue volunteer", "lifeboat volunteer", "emergency care",
                                              "sea survival certificate"],
                 years=(2, 1, 4), share=0.65, contests_y=2, forks=["pay"],
                 demand=dict(hours=4, money=0.02, entry=0.05, energy=0.7), window=None,
                 upkeep=dict(of="proficiency", years=2, kept_by=["drill nights", "call-outs"])),
            dict(say="it is your job now", any=["firefighter", "paramedic"],
                 years=(3, 1, 7), share=0.4, contests_y=4, forks=["take", "round"],
                 demand=dict(hours=6, money=0.05, entry=0.2, energy=0.8),
                 window=dict(every=1, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=2, kept_by=["work on the crew", "training days"])),
            dict(say="the one the town thanks", any=["award for bravery", "local hero"],
                 req="was('firefighter') | was('paramedic') | was('search-and-rescue volunteer')"
                     " | was('lifeboat volunteer')", height="Known",
                 years=(8, 3, 20), share=0.15, contests_y=4, forks=["go_on"],
                 demand=dict(hours=2, money=0, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a rescue the whole country saw", any=["known across the country"],
                 req="was('firefighter') | was('paramedic') | was('lifeboat volunteer')", height="Notable",
                 years=(10, 4, 25), share=0.05, contests_y=3, forks=["go_on"],
                 demand=dict(hours=2, money=0, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # Clock: care work starts with a short induction course and often comes later in life; a few years make a steady
    # senior carer; being asked for by name takes most of a decade; national voices for carers are very few, and a
    # way of caring that others follow fewer still. Shares: estimate. Demands: estimate; the hours are the extra
    # beyond paid care (courses, the carers' group, the visits nobody pays for); the work itself is tiring.
    "to care for those who cannot manage alone": dict(
        shape="career", face="G W", sphere="care", domain="career", calling=True, area="care",
        spark="a week of looking in on someone",
        dreams=[],
        thing="care work", doing="caring for people", contest="an inspection",
        places=["care.houses", "gather.talk"],
        people=dict(coach="a senior carer who shows you the ropes", rival="a colleague who cuts corners",
                    peer="the others on the round", patron="a family who recommends you"),
        round=["a care home across town", "a nursing course at night", "the carers' group that meets each week"],
        below="{N} is the one who notices the old man at the bus stop who cannot manage the step",
        tribal="to tend the old, the hurt and the slow, so the clan leaves no one behind",
        magic="to keep the house of rest where the old and the spent are looked after",
        prep=["people skills", "first aid", "care"], meets=["meaning", "belonging"],
        rungs=[
            dict(say="care as one's work",
                 any=["carer for a parent", "home nursing", "hospice volunteer", "minding small children",
                      "care worker", "alms visitor"],
                 years=(0.5, 0.2, 2), share=0.9, start=(14, 18, 50), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0, entry=0.02, energy=0.6), window=None, upkeep=None),
            dict(say="the calm others lean on", any=["calming people down", "counselling", "carers' group"],
                 years=(3, 1, 6), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=3, money=0.02, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="the one families ask for by name", any=["good name in town", "trusted with the keys"],
                 req="was('care worker') | was('alms visitor') | was('carer for a parent')", height="Known",
                 years=(6, 3, 12), share=0.35, contests_y=1, forks=["go_on", "round"],
                 demand=dict(hours=3, money=0, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a voice for carers across the country", any=["known across the country"],
                 req="was('care worker') | was('carer for a parent')", height="Notable",
                 years=(10, 5, 20), share=0.04, contests_y=0.5, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a way of caring others still follow", any=["a work that outlives you"],
                 req="was('care worker') | was('carer for a parent')", height="Historic",
                 years=(10, 5, 25), share=0.2, contests_y=0.3, forks=["go_on"],
                 demand=dict(hours=5, money=0.01, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: animal care courses 1 to 2 years and paid animal work is sought after; a herd, a farm or hives of one's
    # own usually come years into the work; being the one people bring their animals to takes most of a decade.
    # Shares: estimate. Demands: estimate; the first rung's money is an animal's keep, the third rung's entry the
    # stock, hives or land rent.
    "to work with animals": dict(
        shape="career", face="G U", sphere="prod", domain="career", calling=True, area="care",
        spark="the dog nobody can handle",
        dreams=["a zookeeper", "a beast-tamer of the menagerie"],
        thing="animals", doing="working with animals", contest="the agricultural show",
        places=["prod.land", "care.houses", "prod.wild"],
        people=dict(coach="a stockkeeper who has seen everything", rival="the one whose dogs always win at the show",
                    peer="the others at the shelter", patron="a farmer who lends you a field"),
        round=["a farm across the valley", "a course in animal care", "volunteering at the shelter every weekend"],
        below="{N} is always on the floor with the dog at other people's houses, and the dog always comes",
        tribal="to keep and know the clan's beasts, the herds, the dogs and the birds",
        magic="to keep the guild's beasts, from the plough horses to the old creatures of the towers",
        prep=["animals", "the outdoors"], meets=["meaning", "competence"],
        rungs=[
            dict(say="a way with animals", any=["handling animals", "dog of one's own", "horse of one's own",
                                               "cat of one's own"],
                 years=(1, 0.3, 3), share=0.9, start=(5, 12, 30), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.08, entry=0.1, energy=0.3), window=None, upkeep=None),
            dict(say="animals as one's work", any=["animal care worker", "farm hand", "park ranger"],
                 years=(3, 1, 6), share=0.55, contests_y=0.5, forks=["round"],
                 demand=dict(hours=4, money=0.03, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="beasts of one's own to keep", any=["farmer", "hives of one's own", "professional beekeeper"],
                 years=(6, 2, 15), share=0.35, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=15, money=0.25, entry=0.6, energy=0.8), window=None, upkeep=None),
            dict(say="the one people bring their animals to", any=["good name in town", "loyal clientele",
                                                                  "the one everyone asks"],
                 req="was('animal care worker') | was('farm hand') | has('handling animals')", height="Known",
                 years=(8, 3, 15), share=0.35, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="known across the country for the work", any=["known across the country"],
                 req="has('handling animals')", height="Notable",
                 years=(12, 5, 25), share=0.04, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # New dream field ("to be famous", dreams.py: means B1, stages child and juvenile, plan "build a following that
    # grows every year"). Clock: creator-economy surveys count tens of millions who post for an audience and a few
    # in 100 of them who earn a living from it; most who reach tens of thousands of followers took 2 to 5 years of
    # regular posting; national recognition and a household name are a few in 1,000 of those. Shares: estimate.
    # calling False: a wish to be seen, not a line of work (estimate of the Library's intent; change if wrong). No v1
    # aim, so no v1 spark or area. Demands: estimate; a following fades within a year or so of silence (the
    # catalogue's "following online" is lost to "a year of silence").
    "to be famous": dict(
        shape="career", face="B", sphere="arts", domain="", calling=False,
        dreams=["to be famous"],
        thing="the spotlight", doing="building a following", contest="a live show",
        places=["arts.screen", "arts.stage", "gather.great"],
        people=dict(coach="an older creator who shows you the ropes", rival="someone who makes the same kind of show",
                    peer="the others making things for an audience", patron="a sponsor"),
        round=["a new kind of show", "the local radio's trial slot", "the open-mic night every week"],
        below="{N} turns every family dinner into a show, and asks for one more take",
        tribal="to have a name every clan repeats at the great gathering, long after the fire is out",
        magic="to be the name the bards sing in every hall of the realm",
        prep=["a stage", "public speaking", "making videos"], meets=["belonging", "competence"],
        rungs=[
            dict(say="an audience of your own", any=["online creator", "community-radio presenter",
                                                     "amateur band member"],
                 years=(1, 0.3, 2.5), share=0.9, start=(10, 15, 30), contests_y=1, forks=["go_on"],
                 demand=dict(hours=5, money=0.03, entry=0.05, energy=0.4), window=None, upkeep=None),
            dict(say="a following that grows", any=["following online"],
                 years=(3, 1, 7), share=0.2, contests_y=2, forks=["pay", "round"],
                 demand=dict(hours=10, money=0.05, entry=0.05, energy=0.6), window=None,
                 upkeep=dict(of="access", years=1, kept_by=["posting regularly", "live shows"])),
            dict(say="paid to be seen", any=["full-time creator", "DJ", "touring musician"],
                 req="has('following online') | was('touring musician') | was('DJ')", height="Known",
                 years=(2, 1, 5), share=0.3, contests_y=3, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0.1, energy=0.7), window=None,
                 upkeep=dict(of="access", years=1, kept_by=["posting regularly", "live shows"])),
            dict(say="a face the country knows", any=["known across the country"],
                 req="was('full-time creator') | was('touring musician') | was('DJ') | has('following online')",
                 height="Notable",
                 years=(4, 1, 10), share=0.15, contests_y=3, forks=["go_on", "take"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.7), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["new work", "public appearances"])),
            dict(say="a household name", any=["a household name"],
                 req="was('full-time creator') | was('touring musician') | was('DJ') | has('known across the country')",
                 height="Notable",
                 years=(5, 2, 15), share=0.1, contests_y=2, forks=["go_on"],
                 demand=dict(hours=8, money=0, entry=0, energy=0.6), window=None, upkeep=None),
        ]),
}


# ==== part c: from v25-prep/library/fields/fields-c.py, its header:
# Chroma library, modern Earth: v25 prep, fields part c, the cause and home shapes (Library writer c, 10-23). DRAFT,
# nothing reads it: the Library pours it into chroma-library/earth_fields.py (FIELDS_EARTH) on Friday 10-23 21:00
# (Emren's time), and NEW_TITLES into earth_perks_titles.py with their doors. Format: chroma-engine/notes/v25/
# aims-shape.md sections 3, 5 and 8 (the chess entry, key for key, plus the keys frozen in section 3 on 10-23);
# brief: chroma-ideas/v25-prep/library/briefs/FIELDS.md and V25-DECISIONS.md ("Aims").
#
# Holds the 10 v1 Earth aims of the cause shape (areas justice, cause, community, freedom), the 15 v1 Earth aims of the
# home shape (areas line, love, home) and the one new dream field of the home shape ("to take in a child who has no
# one"). v1's name, face, sphere, domain, area, calling, dreams, spark, below, tribal, magic are as v1 has them (spark
# and area kept on the Engine's word, 10-23: the Engine reads sparks), and each step's say, any, req and height
# unchanged. The new field has area "line" (its domain is children) and no spark: it is born from its dream.
#
# Rungs onto the shapes. cause: caring, joining, organising, leading, a change that lasts (5). home: a bond, a
# household, the household holds, the centre of the line (4). A field with fewer steps names the shape rungs it leaves
# out in `skip`. Two home aims have 5 v1 steps for the shape's 4 rungs; each drops one middle step without a height,
# named in its comment ("to grow old among many grandchildren", "to know where we come from").
#
# Clocks: `years` is (median, 10th, 90th percentile) of steady effort from the rung below; `share` is of those who
# keep at it, the share who reach that rung, so the shares multiply down the ladder. Sources are named in the comment
# above each field; "estimate" where no count is known. For home and cause the `contest` is the hard test (a vote, a
# hearing, a hard year for the family), and `contests_y` stays low (0.5 to 1 a year for home). `time=True` marks a
# rung that comes with age alone (children grown and gone, grandchildren): no forks, no contests, effort does not
# bring it, and its demand is an hour a week at most. Ways in (V25-DECISIONS "Aims"): each field's places, people and
# `round` give at least three ways in, and the last `round` entry is the recurring one (weekly, monthly or yearly).
#
# Section 3's keys of 10-23, all estimates:
# - `prep`: shared preparation tags, from one small set so that fields share them: organising, public speaking,
#   committee work, campaigning, the law, paperwork, trading, bookkeeping, saving money, the household, cooking,
#   hosting, caring for children, courting, reading, records and archives, storytelling, calming disputes, travel,
#   fixing things, outdoor work, first aid.
# - `meets`: the needs the practice restores, from the catalogue's five (autonomy, belonging, competence, meaning,
#   safety).
# - `demand` per rung, at steady intensity: hours a week on top of work and the relationships' ordinary time (the
#   capacity already counts those), money a year and a one-time entry, each as a share of a year's free money (a
#   wedding about .4 to .5, a home's deposit 1), and energy 0 to 1.
# - `window`: only where outside timing is real: committee and council elections, a public-service recruitment round,
#   the bar's exam sittings, a rep's election, the festival season, the fostering panel. `every` is in years.
# - `upkeep`: only where the rung truly fades: a credential that lapses (a practising certificate, a mediator's
#   accreditation, a foster carer's yearly review) or access that is lost (a seat not re-won, a clientele or a scene
#   left for years). Every other rung says None.

_FIELDS_C = {

    # ======================================================================== cause

    # Clock: community-mediation training is a course of a few weeks plus about a year of supervised cases before
    # accreditation (re-accredited every few years on a record of cases); residents' volunteers are many, trusted
    # keepers of a street few. Shares and demands: estimate.
    "to keep the peace in the street": dict(
        shape="cause", face="W", sphere="prot", domain="community", area="community", calling=True,
        dreams=["a lasting peace between the town and the forest folk"],
        spark="two neighbours squaring up on the pavement",
        thing="keeping the peace", doing="keeping an eye on the street", contest="a row between neighbours",
        places=["prot.watch", "gather.hall", "rule.counsel"],
        people=dict(coach="an old mediator from the community centre", rival="a neighbour who enjoys the trouble",
                    peer="the residents' group", patron="the local community officer"),
        round=["the mediation service's training course", "a residents' group on the next street",
               "the residents' meeting each month"],
        prep=["listening", "organising"],
        meets=["belonging", "meaning"],
        below="{N} is the one who steps between the two lads squaring up at the bus stop, before anyone else has moved",
        tribal="to keep the peace between the families of the camp",
        magic="to keep the peace in the lanes below the towers",
        skip=[4],   # 4 steps: caring, joining, organising, leading, (a change that lasts left out)
        rungs=[
            dict(say="an eye on the street", any=["neighbourhood volunteer", "residents' committee member",
                                                   "neighbour who has your back"],
                 years=(0.5, 0.2, 2), share=0.9, start=(16, 25, 60), contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.02, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="stepping in before it turns", any=["calming people down", "settling disputes",
                                                          "community-mediation volunteer"],
                 years=(1.5, 0.5, 4), share=0.6, contests_y=2, forks=["pay"],
                 demand=dict(hours=3, money=0.03, entry=0.05, energy=0.3), window=None, upkeep=None),
            dict(say="the street's keeper", any=["neighbourhood-watch coordinator", "mediator", "police officer",
                                                  "mediation accreditation"],
                 years=(2.5, 1, 6), share=0.4, contests_y=3, forks=["take"],
                 demand=dict(hours=5, money=0.03, entry=0.05, energy=0.4), window=None,
                 upkeep=dict(of="credential", years=3, kept_by=["mediating cases", "refresher training"])),
            dict(say="the name every door trusts", any=["good name in town", "local hero", "trusted with the keys",
                                                         "award for bravery"], height="Known",
                 years=(6, 3, 15), share=0.2, contests_y=2, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0, energy=0.35), window=None, upkeep=None),
        ]),

    # Clock: a law degree takes 3 to 4 years and the vocational training and pupillage or traineeship 1 to 2 more; the
    # qualifying exams sit about twice a year and a practising certificate lapses without work and courses; a name for
    # fairness comes after about a decade in practice; cases that change the law are a few in a career at most, and
    # few lawyers have one. Shares and demands: estimate.
    "to see justice done": dict(
        shape="cause", face="W", sphere="rule", domain="career", area="justice", calling=True,
        dreams=["a police officer"],
        spark="the evening at the free advice desk",
        thing="the law", doing="working for justice", contest="a case in court",
        places=["learn.higher", "learn.keeping", "rule.counsel"],
        people=dict(coach="a senior lawyer who takes them on", rival="a sharp opponent across the courtroom",
                    peer="the other trainees", patron="a judge who notices their work"),
        round=["evening law classes", "a clerk's job at the courts first",
               "the free advice desk on Thursday evenings"],
        prep=["the law", "public speaking", "study"],
        meets=["meaning", "competence"],
        below="{N} cannot let an unfair thing pass, and keeps arguing it long after the others have shrugged",
        tribal="to see that the elders judge fairly and every wrong is put right",
        magic="to see the realm's laws kept fairly, by the high and the low alike",
        rungs=[
            dict(say="a foot in the courts", any=["court clerk", "paralegal", "court interpreter", "police officer"],
                 years=(2, 1, 4), share=0.85, start=(16, 20, 35), contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.1, entry=0.2, energy=0.4), window=None, upkeep=None),
            dict(say="the right to stand up in court",
                 any=["lawyer", "lay judge", "detective", "professional registration"],
                 years=(5, 3, 9), share=0.5, contests_y=4, forks=["pay"],
                 demand=dict(hours=15, money=0.4, entry=0.5, energy=0.6),
                 window=dict(every=0.5, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=3, kept_by=["legal work", "professional courses"])),
            dict(say="a name for fairness",
                 any=["name in the field", "good name in town", "a name for straight talk"],
                 height="Known",
                 years=(8, 4, 15), share=0.35, contests_y=6, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="a case that changes the law", any=["a reform with your name on it", "known across the country"],
                 req="was('lawyer') | was('lay judge') | was('detective') | was('police officer') | was('court clerk') | was('paralegal')", height="Notable",
                 years=(8, 4, 20), share=0.08, contests_y=6, forks=["take", "round"],
                 demand=dict(hours=10, money=0.1, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="a ruling still cited", any=["a work that outlives you"],
                 req="was('lawyer') | was('lay judge') | was('detective') | was('police officer') | was('court clerk') | was('paralegal')", height="Historic",
                 years=(10, 5, 25), share=0.15, contests_y=4, forks=["go_on"],
                 demand=dict(hours=8, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: public services commonly recruit in a yearly round with an entrance test; grades usually take a few years
    # each (about 3 to 5 from a first desk to a post of trust); a name in the town hall after about a decade; a
    # national reform is rare. Shares and demands: estimate.
    "to serve the public well": dict(
        shape="cause", face="W U", sphere="rule", domain="career", area="community", calling=True,
        dreams=["a town warden"],
        spark="the claim that went missing",
        thing="public service", doing="working for the public", contest="an audit of the office's work",
        places=["rule.counsel", "rule.voice", "learn.keeping"],
        people=dict(coach="an old hand in the office", rival="a colleague after the same post",
                    peer="the others on the office floor", patron="a department head who rates them"),
        round=["a temporary post at the town hall", "volunteering at the polling station",
               "the public-service entrance exam held each spring"],
        prep=["paperwork", "organising"],
        meets=["meaning", "competence"],
        below="{N} reads every notice on the library board, and writes in when the bin round is missed",
        tribal="to serve the camp well as keeper of its stores and counts",
        magic="to serve the realm well in the clerks' halls of the high council",
        skip=[0],   # 4 steps: (caring left out), joining, organising, leading, a change that lasts
        rungs=[
            dict(say="a desk in public service", any=["office clerk", "postal worker", "court clerk",
                                                       "polling-station volunteer"],
                 years=(1, 0.3, 3), share=0.9, start=(17, 22, 45), contests_y=1, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.05, energy=0.2),
                 window=dict(every=1, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="trusted with the public's business", any=["standards inspector", "urban planner",
                                                                 "handling red tape", "constituency caseworker",
                                                                 "reliable record"],
                 years=(4, 2, 8), share=0.55, contests_y=1, forks=["pay"],
                 demand=dict(hours=5, money=0.05, entry=0.05, energy=0.35), window=None, upkeep=None),
            dict(say="a name in the town hall", any=["officials who trust you", "voice at the town hall",
                                                      "good name in town"], height="Known",
                 years=(7, 3, 15), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="a change the whole country uses", any=["a reform with your name on it",
                                                              "known across the country"],
                 req="was('office clerk') | was('court clerk') | was('standards inspector') | "
                     "was('urban planner') | was('constituency caseworker') | was('postal worker')", height="Notable",
                 years=(10, 5, 20), share=0.07, contests_y=1, forks=["go_on", "round"],
                 demand=dict(hours=6, money=0.03, entry=0, energy=0.45), window=None, upkeep=None),
        ]),

    # Clock: committees elect at a yearly meeting; councils sit about four years between elections and national
    # assemblies about five, and a seat not re-won is lost; local councillors are mostly first elected in their
    # forties or fifties after years on committees; most national legislators held local office first; a law that
    # outlasts its maker is rare. Shares and demands: estimate.
    "to make the rules everyone lives by": dict(
        shape="cause", face="W B", sphere="rule", domain="community", area="justice", calling=True,
        dreams=["a seat on the city council", "to speak for the clan at the gatherings"],
        spark="the yard that needs new rules",
        thing="making the rules", doing="sitting on committees", contest="a vote",
        places=["rule.counsel", "rule.voice", "gather.hall"],
        people=dict(coach="an old councillor who knows every rule of procedure", rival="the chair of the other side",
                    peer="the rest of the committee", patron="a backer who already holds a seat"),
        round=["a school board seat instead", "a committee across town", "the residents' meeting each month"],
        prep=["organising", "public speaking"],
        meets=["meaning", "belonging"],
        below="{N} writes out the rules for every game in the playground, and makes the others sign them",
        tribal="to set the laws of the camp with the council of elders",
        magic="to write the laws the city's guilds and towers all must keep",
        rungs=[
            dict(say="a seat on a committee",
                 any=["residents' committee member", "club treasurer", "school-governance board member", "prefect"],
                 years=(1, 0.3, 3), share=0.9, start=(12, 25, 55), contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.01, entry=0, energy=0.2),
                 window=dict(every=1, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a hand in the rules",
                 any=["local councillor", "lay judge", "knowing the rules of the house", "drafting policy"],
                 years=(3, 1, 8), share=0.45, contests_y=2, forks=["pay"],
                 demand=dict(hours=8, money=0.05, entry=0.1, energy=0.45),
                 window=dict(every=4, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="access", years=4, kept_by=["council work", "standing for election"])),
            dict(say="a voice the town hall heeds",
                 any=["voice at the town hall", "mayor", "officials who trust you"],
                 height="Known",
                 years=(5, 2, 12), share=0.35, contests_y=2, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0.1, energy=0.5),
                 window=dict(every=4, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="laws with your name on them", any=["a reform with your name on it", "member of parliament"],
                 height="Notable",
                 years=(6, 3, 15), share=0.12, contests_y=2, forks=["take", "round"],
                 demand=dict(hours=15, money=0.1, entry=0.2, energy=0.6),
                 window=dict(every=5, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="access", years=5, kept_by=["work in the assembly", "standing for election"])),
            dict(say="a charter still in force", any=["a work that outlives you"],
                 req="has('a reform with your name on it') | was('member of parliament')", height="Historic",
                 years=(10, 4, 25), share=0.1, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: about half of new small firms survive five years (business-survival counts, widely reported); a loyal
    # clientele takes a few years more and drifts away within a couple of years of not trading; a name far beyond the
    # town is a few in 100 of traders. Shares and demands: estimate.
    "to answer to no one": dict(
        shape="cause", face="B", sphere="comm", domain="career", area="freedom", calling=True,
        dreams=["a business of one's own", "a shop of one's own, with a till that rings",
                "a sellsword who answers to no one"],
        spark="the first money earned with no one over you",
        thing="a trade of one's own", doing="trading on your own account", contest="a bad month for trade",
        places=["comm.market", "comm.shop", "comm.credit"],
        people=dict(coach="an old trader who started the same way", rival="the stall across the way",
                    peer="the other traders", patron="a lender who believes in them"),
        round=["selling online", "a stall on the fair circuit", "the weekly market"],
        prep=["trading", "numbers"],
        meets=["autonomy", "competence"],
        below="{N} bristles at every rota and every manager, and keeps a list of things that could be sold",
        tribal="to hunt and trade on one's own, owing no headman a share of the catch",
        magic="to keep a free stall at the crossroads, sworn to no guild and paying no master",
        skip=[4],   # 4 steps: caring, joining, organising, leading, (a change that lasts left out)
        rungs=[
            dict(say="a little trade on the side", any=["market trader", "selling", "striking a deal"],
                 years=(0.5, 0.2, 2), share=0.9, start=(14, 20, 50), contests_y=2, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0.1, energy=0.3), window=None, upkeep=None),
            dict(say="your own name over the door", any=["shop owner", "founder of a firm", "premises of one's own"],
                 years=(3, 1, 7), share=0.45, contests_y=2, forks=["pay"],
                 demand=dict(hours=15, money=0.3, entry=0.8, energy=0.6), window=None, upkeep=None),
            dict(say="customers who come back for you", any=["loyal clientele", "good name in town"],
                 height="Known",
                 years=(4, 2, 8), share=0.5, contests_y=2, forks=["take"],
                 demand=dict(hours=12, money=0.2, entry=0, energy=0.55), window=None,
                 upkeep=dict(of="access", years=2, kept_by=["trading"])),
            dict(say="a name in the trade far beyond the town", any=["name in the field", "known across the country"],
                 req="was('shop owner') | was('founder of a firm') | was('market trader')", height="Notable",
                 years=(8, 4, 18), share=0.1, contests_y=1, forks=["take"],
                 demand=dict(hours=12, money=0.2, entry=0.1, energy=0.55), window=None, upkeep=None),
        ]),

    # Clock: a licence takes months; a skill that travels (a trade, a stall, decks or needles) a few years; living
    # full-time on the road is a small minority even of those who try it, many coming back within a few years.
    # Shares and demands: estimate.
    "to live by my own rules": dict(
        shape="cause", face="B R", sphere="", domain="", area="freedom", calling=False,
        dreams=["to live off the land, owing nothing to anyone", "a tower of one's own, answering to no Order",
                "an adventurer"],
        spark="the first door walked out of for good",
        thing="freedom", doing="living on your own terms", contest="a lean season on the road",
        places=["prod.wild", "comm.market"],
        people=dict(coach="an old traveller who has lived this way for years", rival="another drifter after the same pitch",
                    peer="the people met on the road", patron="a grower who always has seasonal work"),
        round=["a boat instead of a van", "a skill that travels anywhere", "the harvest work each summer"],
        prep=["travel", "trading", "the workshop"],
        meets=["autonomy"],
        below="{N} reads every rule as a dare, and keeps a bag packed under the bed",
        tribal="to roam beyond the clan's paths, following no elder's word but one's own",
        magic="to wander the roads between the towers, bound by no oath and no Order",
        skip=[3, 4],   # 3 steps: caring, joining, organising, (leading and a change that lasts left out)
        rungs=[
            dict(say="a way out of town", any=["driving licence", "motorbike licence", "passport"],
                 years=(1, 0.3, 3), share=0.9, start=(16, 18, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=2, money=0.1, entry=0.2, energy=0.15), window=None, upkeep=None),
            dict(say="a living no boss can take", any=["van and tools", "market trader", "tattoo artist", "DJ"],
                 years=(3, 1, 7), share=0.5, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.1, entry=0.4, energy=0.4), window=None, upkeep=None),
            dict(say="a life that fits in a van", any=["camper van", "boat of one's own", "place by the sea"],
                 years=(3, 1, 8), share=0.45, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=4, money=0.1, entry=0.6, energy=0.35), window=None, upkeep=None),
        ]),

    # Clock: advocacy and prison-visiting roles take training and a year or two of cases; a known local advocate about
    # a decade; national cases are few. Shares and demands: estimate.
    "to stand up for the underdog": dict(
        shape="cause", face="R", sphere="rule", domain="community", area="justice", calling=True,
        dreams=[],
        spark="the shouting in the queue",
        thing="the underdog's cause", doing="standing up for people", contest="a hearing",
        places=["rule.voice", "gather.talk", "rule.counsel"],
        people=dict(coach="an old campaigner who has seen it all", rival="the official who keeps saying no",
                    peer="the volunteers at the advice centre", patron="a lawyer who works for nothing"),
        round=["a petition with the neighbours", "a charity that takes such cases",
               "the advice centre's weekly drop-in"],
        prep=["campaigning", "public speaking", "the law"],
        meets=["meaning", "belonging"],
        below="{N} cannot stand by when someone smaller is pushed about, and never could",
        tribal="to speak for the ones the strong hunters push aside",
        magic="to stand for the commons when the guilds and the towers lean on them",
        rungs=[
            dict(say="speaking up when nobody else will", any=["local hero", "debating", "campaigning"],
                 years=(0.5, 0.2, 2), share=0.9, start=(12, 20, 60), contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.01, entry=0, energy=0.25), window=None, upkeep=None),
            dict(say="taking on other people's fights",
                 any=["prison visitor", "disability-rights organiser", "constituency caseworker", "restorative-justice advocate"],
                 years=(3, 1, 7), share=0.5, contests_y=2, forks=["pay"],
                 demand=dict(hours=5, money=0.02, entry=0.05, energy=0.4), window=None, upkeep=None),
            dict(say="the one people bring their trouble to",
                 any=["lawyer", "a name for straight talk", "good name in town"],
                 req="was('prison visitor') | was('disability-rights organiser') | was('constituency caseworker') | was('restorative-justice advocate') | was('lawyer')", height="Known",
                 years=(5, 2, 12), share=0.35, contests_y=3, forks=["take", "round"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="the whole country hears the case you took up", any=["known across the country"],
                 req="was('lawyer') | was('disability-rights organiser') | was('restorative-justice advocate')", height="Notable",
                 years=(7, 3, 18), share=0.1, contests_y=3, forks=["take"],
                 demand=dict(hours=8, money=0.05, entry=0.05, energy=0.55), window=None, upkeep=None),
            dict(say="a case still cited for others", any=["a work that outlives you"],
                 req="was('lawyer') | was('disability-rights organiser') | was('restorative-justice advocate')", height="Historic",
                 years=(10, 5, 25), share=0.12, contests_y=2, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.45), window=None, upkeep=None),
        ]),

    # Clock: local conservation campaigns over a wood or a field commonly run 2 to 10 years from first objection to
    # a decision; volunteers are many, leaders of a won campaign few, a national cause fewer. Shares and demands:
    # estimate. No window: planning consultations come irregularly, so the hearings are the field's contests.
    "to save the wild places": dict(
        shape="cause", face="R G", sphere="", domain="community", area="cause", calling=True,
        dreams=[],
        spark="the diggers at the edge of the wood",
        thing="the wild places", doing="campaigning for the wild", contest="a planning hearing",
        places=["prod.wild", "rule.voice", "gather.talk"],
        people=dict(coach="an old naturalist who counts the birds every spring", rival="the developer's spokesperson",
                    peer="the other volunteers", patron="a local trust that funds the work"),
        round=["a survey of the birds and plants for the record", "a petition to the council",
               "the monthly work party in the wood"],
        prep=["campaigning", "the outdoors", "organising"],
        meets=["meaning", "belonging"],
        below="{N} takes every felled tree on the way to school as a personal insult",
        tribal="to keep the old groves and the hunting grounds from the strangers' fires",
        magic="to keep the old woods from the lords' foresters and the guilds' axes",
        skip=[0],   # 4 steps: (caring left out), joining, organising, leading, a change that lasts
        rungs=[
            dict(say="out with the litter-pickers", any=["neighbourhood volunteer", "community observer",
                                                         "campaign volunteer"],
                 years=(0.5, 0.2, 2), share=0.9, start=(12, 25, 65), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=2, money=0.01, entry=0, energy=0.25), window=None, upkeep=None),
            dict(say="a cause of your own", any=["activist in a cause", "animal-shelter campaigner",
                                                 "citizen scientist"],
                 years=(2, 1, 5), share=0.5, contests_y=1, forks=["pay"],
                 demand=dict(hours=4, money=0.03, entry=0.02, energy=0.35), window=None, upkeep=None),
            dict(say="the one who saved the wood", any=["a list of supporters", "a movement behind you",
                                                        "good name in town"],
                 req="was('activist in a cause') | was('animal-shelter campaigner') | was('citizen scientist')",
                 height="Known",
                 years=(4, 2, 10), share=0.25, contests_y=2, forks=["take", "round"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="the country takes up the fight", any=["known across the country"],
                 req="was('activist in a cause') | was('animal-shelter campaigner')", height="Notable",
                 years=(8, 3, 20), share=0.1, contests_y=2, forks=["go_on"],
                 demand=dict(hours=8, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: a workplace rep is usually elected for about two years at a time after a few years as a member; a
    # campaign that wins a national right commonly takes one to several decades. Shares and demands: estimate.
    "to fight for what is right": dict(
        shape="cause", face="R W", sphere="rule", domain="community", area="cause", calling=True,
        dreams=[],
        spark="the sacking nobody would talk about",
        thing="the fight", doing="campaigning", contest="a ballot",
        places=["rule.voice", "gather.hall", "gather.talk"],
        people=dict(coach="an old organiser from the union hall", rival="a manager who will not budge",
                    peer="the campaign's volunteers", patron="a well-known campaigner who backs them"),
        round=["a petition with the neighbours", "a campaign group across town", "the branch meeting each month"],
        prep=["campaigning", "public speaking", "organising"],
        meets=["meaning", "belonging"],
        below="{N} says 'that is not fair' louder than anyone in the room, and means it every time",
        tribal="to stand against the headman when he breaks the camp's own ways",
        magic="to stand against the guildmasters when they break their own charters",
        rungs=[
            dict(say="refusing to look away", any=["campaigning", "canvassing", "union member"],
                 years=(0.5, 0.2, 2), share=0.9, start=(14, 25, 60), contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.02, entry=0, energy=0.25), window=None, upkeep=None),
            dict(say="a fight worth having", any=["union rep", "civil-liberties campaigner", "campaign organiser"],
                 years=(3, 1, 7), share=0.45, contests_y=2, forks=["pay"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.45),
                 window=dict(every=2, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="access", years=2, kept_by=["union work", "standing for election"])),
            dict(say="the one they cannot ignore", any=["voice at the town hall", "a name for straight talk"],
                 req="was('union member') | was('union rep') | was('civil-liberties campaigner') | was('campaign organiser')", height="Known",
                 years=(5, 2, 12), share=0.3, contests_y=2, forks=["take"],
                 demand=dict(hours=6, money=0.03, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="the whole country hears it", any=["known across the country"],
                 req="was('union rep') | was('civil-liberties campaigner') | was('campaign organiser')", height="Notable",
                 years=(7, 3, 18), share=0.12, contests_y=2, forks=["take", "round"],
                 demand=dict(hours=10, money=0.05, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a right the country still keeps", any=["a work that outlives you"],
                 req="was('union rep') | was('civil-liberties campaigner') | was('campaign organiser')", height="Historic",
                 years=(12, 5, 30), share=0.12, contests_y=1, forks=["go_on"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: a promoter's or organiser's name on a local scene in about 3 to 5 years of regular nights, fading within
    # a few years of stopping; a festival with national draw usually takes 5 to 10 editions in the summer season and
    # is rare. Shares and demands: estimate.
    "to throw the parties the town remembers": dict(
        shape="cause", face="R W", sphere="gather", domain="community", area="community", calling=True,
        dreams=["to start a festival the whole town comes to", "to lead the songs at every feast"],
        spark="the street party nobody else would organise",
        thing="a good party", doing="throwing parties", contest="a big night",
        places=["gather.house", "gather.great", "gather.hall"],
        people=dict(coach="an old hand who has run the town fair for years", rival="a rival promoter",
                    peer="the regulars who always help set up", patron="a venue owner who gives them a date"),
        round=["a hall hired across town", "a night in a borrowed space", "the street party each summer"],
        prep=["hosting", "organising", "cooking"],
        meets=["belonging", "competence"],
        below="{N} is the one who turns a quiet evening into twenty people in the kitchen",
        tribal="to call the feasts that the bands still talk about a season later",
        magic="to throw the harvest feasts the whole realm hears of",
        skip=[1],   # 4 steps: caring, (joining left out), organising, leading, a change that lasts
        rungs=[
            dict(say="the house everyone ends up at", any=["cooking for a crowd", "club member",
                                                           "neighbourhood volunteer"],
                 years=(1, 0.3, 3), share=0.9, start=(16, 22, 50), contests_y=2, forks=["go_on"],
                 demand=dict(hours=3, money=0.05, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="the one who runs the night", any=["festival organiser", "events promoter",
                                                        "parent-association organiser"],
                 years=(2, 1, 5), share=0.5, contests_y=4, forks=["pay"],
                 demand=dict(hours=6, money=0.1, entry=0.1, energy=0.5), window=None, upkeep=None),
            dict(say="a name for a good time", any=["good name in town", "name on the local scene"],
                 req="was('festival organiser') | was('events promoter') | was('parent-association organiser')",
                 height="Known",
                 years=(3, 1, 8), share=0.4, contests_y=6, forks=["take"],
                 demand=dict(hours=8, money=0.1, entry=0, energy=0.55), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["running nights", "organising events"])),
            dict(say="a festival the whole country comes to", any=["known across the country"],
                 req="was('festival organiser') | was('events promoter')", height="Notable",
                 years=(8, 4, 18), share=0.06, contests_y=4, forks=["take", "round"],
                 demand=dict(hours=15, money=0.2, entry=0.4, energy=0.7),
                 window=dict(every=1, open_weeks=14, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
        ]),

    # ======================================================================== home

    # Clock: the average age at a first birth is near 30 in many places, with a spread of about 22 to 38; children
    # leave home at about 18 to 25; the first grandchild comes at about 50 to 60 (demographic counts; estimate for the
    # spreads). Shares and demands: estimate.
    "to raise a family that holds together": dict(
        shape="home", face="W", sphere="", domain="children", area="line", calling=False,
        dreams=["a family of one's own", "to raise children well and teach them all one knows"],
        spark="the whole family round one table",
        thing="the family", doing="bringing up the family", contest="a hard year for the family",
        places=["gather.house", "gather.hall"],
        people=dict(coach="an aunt who raised five", rival="a friend raising children the opposite way",
                    peer="the other parents at the school gate", patron="grandparents who help"),
        round=["a family counsellor", "the grandparents' help", "the parents' group each week"],
        prep=["caring for children", "the household", "cooking"],
        meets=["belonging", "meaning"],
        below="{N} is the one who remembers every cousin's birthday and sets the extra places at the table",
        tribal="to raise a family that stays one hearth through every hard season",
        magic="to raise a household that holds together under one roof, whatever the towers ask of it",
        rungs=[
            dict(say="a home with children in it", any=["mother or father", "stepparent", "foster parent",
                                                         "adoptive parent", "guardian of an unrelated child"],
                 years=(3, 1, 8), share=0.85, start=(20, 28, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.1, entry=0.2, energy=0.4), window=None, upkeep=None),
            dict(say="a table the family gathers at", any=["cooking for a crowd", "minding small children",
                                                           "partner in a multigenerational household",
                                                           "parent of three or more"],
                 years=(3, 1, 8), share=0.75, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.2, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="children grown and still close", any=["parent of independent adult children",
                                                             "parent with a child living abroad"],
                 years=(17, 12, 22), share=0.8, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
            dict(say="the still centre of the family", any=["grandparent", "grandparent raising a grandchild"],
                 years=(8, 2, 20), share=0.7, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
        ]),

    # Clock: a first partner in the late teens or twenties, marriage after about 2 to 4 years together; about 4 in 10
    # first marriages end in divorce in many places, most within 15 years (demographic counts). Shares and demands:
    # estimate.
    "to keep one promise for life": dict(
        shape="home", face="W", sphere="", domain="partner", area="love", calling=False,
        dreams=["a marriage that lasts a lifetime"],
        spark="the year the promise gets heavy",
        thing="the promise", doing="keeping the promise", contest="a hard year together",
        places=["gather.house", "gather.circle"],
        people=dict(coach="a couple married fifty years", rival="an old flame who comes back",
                    peer="friends who married the same summer", patron="parents who back the match"),
        round=["a counsellor for couples", "a weekend away, just the two of them", "the same night out every week"],
        prep=["courting", "the household"],
        meets=["belonging", "safety"],
        below="{N} still keeps the note from the first date in a drawer, folded small",
        tribal="to keep the bond sworn at the fire through every season of life",
        magic="to keep the oath sworn at the hearth-stone for a whole life",
        skip=[3],   # 3 steps: a bond, a household, the household holds, (the centre of the line left out)
        rungs=[
            dict(say="someone to keep a promise to", any=["girlfriend or boyfriend", "living together"],
                 years=(2, 0.5, 6), share=0.9, start=(16, 22, 35), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="the promise made", any=["engaged", "wife or husband", "newlywed", "nonromantic life partner",
                                               "spouse in a family-arranged marriage"],
                 years=(3, 1, 7), share=0.7, contests_y=0.5, forks=["take"],
                 demand=dict(hours=3, money=0.05, entry=0.4, energy=0.2), window=None, upkeep=None),
            dict(say="kept through the hard years", any=["partner of many years", "caregiving partner"],
                 years=(15, 8, 25), share=0.6, contests_y=1, forks=["go_on", "pay"],
                 demand=dict(hours=3, money=0.03, entry=0, energy=0.3), window=None, upkeep=None),
        ]),

    # Clock: households commonly take a few years to build savings of a few months' pay; a home is bought after about
    # 3 to 6 years of saving and paid off over a 25 to 30 year loan, often early (estimate). Shares and demands:
    # estimate.
    "to make a home that runs well": dict(
        shape="home", face="W U", sphere="", domain="partner", area="home", calling=False,
        dreams=["a partner to think with"],
        spark="a kitchen table covered in bills",
        thing="the household", doing="running the household", contest="a month the money will not stretch",
        places=["comm.credit", "comm.shop", "gather.house"],
        people=dict(coach="a parent who never once missed a bill", rival="a sibling whose house is always in better order",
                    peer="neighbours on the same tight budget", patron="a money adviser at the advice centre"),
        round=["a budgeting class at the library", "a cheaper place to live",
               "the money talk at the kitchen table each month"],
        prep=["the household", "numbers", "saving money"],
        meets=["safety", "competence"],
        below="{N} keeps a list on the fridge and a jar for the bills, and the flat never once runs out of milk",
        tribal="to keep a shelter where the fire never goes out and the stores last the winter",
        magic="to keep a household in good order, every ward and pantry in its place",
        rungs=[
            dict(say="a home shared", any=["living together", "wife or husband", "nonromantic life partner"],
                 years=(2, 0.5, 6), share=0.9, start=(18, 25, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=2, money=0.05, entry=0.2, energy=0.15), window=None, upkeep=None),
            dict(say="the household in order", any=["bookkeeping", "fixing things", "cooking for a crowd",
                                                     "secure tenancy"],
                 years=(2, 1, 5), share=0.8, contests_y=1, forks=["pay"],
                 demand=dict(hours=3, money=0.02, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="money set by", any=["savings", "good credit", "workplace pension"],
                 years=(4, 2, 10), share=0.6, contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.2, entry=0, energy=0.15), window=None, upkeep=None),
            dict(say="a home that all but runs itself", any=["paid-off home", "homeowner"],
                 years=(12, 5, 25), share=0.45, contests_y=0.5, forks=["take"],
                 demand=dict(hours=2, money=0.3, entry=0.8, energy=0.2), window=None, upkeep=None),
        ]),

    # Clock: carrying the name begins with a first child or with being the eldest; a respected household after a
    # decade or so of work and saving; children grown with time; a name that opens doors is a few families in a town.
    # Shares and demands: estimate.
    "to keep the family name high": dict(
        shape="home", face="W B", sphere="", domain="children", area="line", calling=True,
        dreams=["a family name that counts for something", "to found a clan of one's own"],
        spark="the speech at the great-aunt's ninetieth",
        thing="the family name", doing="keeping up the family name", contest="talk in the town about the family",
        places=["gather.great", "gather.house", "rule.counsel"],
        people=dict(coach="the great-aunt who keeps the family history", rival="a cousin who wants the standing for themselves",
                    peer="the other old families in town", patron="the head of the family"),
        round=["a family business to carry the name", "a seat on a local board", "the family's yearly gathering"],
        prep=["the household", "hosting", "organising"],
        meets=["belonging", "meaning"],
        below="{N} sits up straight when the old aunts talk about who married whom, and remembers every word",
        tribal="to keep the clan's name honoured at every gathering",
        magic="to keep the house's name and crest honoured in the high halls",
        rungs=[
            dict(say="the one who carries the name", any=["mother or father", "adoptive parent", "eldest child"],
                 years=(5, 1, 12), share=0.85, start=(16, 25, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=3, money=0.05, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="a household others respect", any=["homeowner", "family business", "savings"],
                 years=(6, 2, 12), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=4, money=0.2, entry=0.5, energy=0.35), window=None, upkeep=None),
            dict(say="children who do it proud", any=["parent of independent adult children", "grandparent",
                                                       "inheritance"],
                 years=(18, 10, 25), share=0.75, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
            dict(say="a name that opens doors", any=["old family name", "good name in town"], height="Known",
                 years=(8, 3, 20), share=0.25, contests_y=1, forks=["take"],
                 demand=dict(hours=4, money=0.1, entry=0.05, energy=0.35), window=None, upkeep=None),
        ]),

    # Clock: first-time buyers commonly save a deposit over 3 to 6 years and buy in their early thirties; home loans
    # usually run 25 to 30 years, many repaid a few years early (estimate). Shares and demands: estimate (the deposit
    # is the one entry of a whole year's free money).
    "to own the roof over our heads": dict(
        shape="home", face="W B", sphere="", domain="", area="home", calling=False,
        dreams=["a manor with orchards", "to hold the family's waterhole for the generations"],
        spark="the small house at the end of the road",
        thing="a home of our own", doing="saving for a home", contest="a sale that falls through",
        places=["comm.credit", "comm.shop"],
        people=dict(coach="a parent who bought late and never regretted it", rival="a friend who bought first",
                    peer="the others in the savings club", patron="a relative who lends part of the deposit"),
        round=["a housing cooperative", "a smaller place further out", "the savings club that meets each month"],
        prep=["saving money", "the household"],
        meets=["safety", "autonomy"],
        below="{N} walks home the long way, past the houses with their own front doors, counting windows",
        tribal="to raise a lodge of our own that no one can turn us out of",
        magic="to hold a house of our own within the city walls, the deed sealed and signed",
        skip=[3],   # 3 steps: a bond, a household, the household holds, (the centre of the line left out)
        rungs=[
            dict(say="money set aside", any=["savings", "good credit", "reliable record"],
                 years=(3, 1, 8), share=0.85, start=(20, 27, 45), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=1, money=0.25, entry=0, energy=0.15), window=None, upkeep=None),
            dict(say="a front door that is ours", any=["homeowner", "housing-cooperative member"],
                 years=(4, 1, 10), share=0.65, contests_y=1, forks=["take"],
                 demand=dict(hours=3, money=0.3, entry=1.0, energy=0.35), window=None, upkeep=None),
            dict(say="the roof paid off", any=["paid-off home", "flat to rent out"],
                 years=(22, 12, 30), share=0.7, contests_y=0.5, forks=["pay"],
                 demand=dict(hours=1, money=0.3, entry=0, energy=0.15), window=None, upkeep=None),
        ]),

    # Clock: courtship to engagement commonly 1 to 3 years, engagement to wedding about 1 to 2; a household of standing
    # after about a decade of marriage (estimate). Shares and demands: estimate.
    "to marry well": dict(
        shape="home", face="U B", sphere="", domain="partner", area="love", calling=False,
        dreams=["to marry well", "a partner to think with"],
        spark="the dinner with the family who matters",
        thing="a good match", doing="looking for a good match", contest="a family dinner that decides things",
        places=["gather.great", "gather.circle", "gather.house"],
        people=dict(coach="an aunt who arranged half the family's matches", rival="another suitor",
                    peer="friends comparing prospects", patron="a matchmaker"),
        round=["introductions through family friends", "a matchmaker",
               "the season's weddings, where people meet each summer"],
        prep=["courting", "hosting"],
        meets=["belonging", "safety"],
        below="{N} listens closely when the grown-ups talk about who married whom, and why it worked",
        tribal="to be joined to a strong family of another clan, with gifts that are remembered",
        magic="to make a match the great houses speak well of, sealed with a fair contract",
        rungs=[
            dict(say="courting with a clear head", any=["girlfriend or boyfriend"],
                 years=(2, 0.5, 6), share=0.9, start=(17, 22, 35), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.1, entry=0, energy=0.25), window=None, upkeep=None),
            dict(say="a promise made", any=["engaged", "living together"],
                 years=(2, 1, 5), share=0.7, contests_y=0.5, forks=["take"],
                 demand=dict(hours=3, money=0.05, entry=0.1, energy=0.2), window=None, upkeep=None),
            dict(say="married, and well", any=["wife or husband", "spouse in a family-arranged marriage",
                                               "in-laws who took you in"],
                 years=(1.5, 0.5, 4), share=0.8, contests_y=0.5, forks=["pay"],
                 demand=dict(hours=3, money=0.05, entry=0.5, energy=0.3), window=None, upkeep=None),
            dict(say="a household that stands well", any=["homeowner", "paid-off home", "good credit",
                                                          "old family name"],
                 years=(8, 3, 18), share=0.5, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=3, money=0.1, entry=0.1, energy=0.25), window=None, upkeep=None),
        ]),

    # Clock: as for any partnership (a first partner in the twenties, moving in after 1 to 3 years, marriage a few
    # years on); about 4 in 10 first marriages end (demographic counts). Shares and demands: estimate.
    "to fall for a mind as quick as mine": dict(
        shape="home", face="U R", sphere="", domain="partner", area="love", calling=False,
        dreams=["a partner to think with", "a great love"],
        spark="the argument that turns into something else",
        thing="a meeting of minds", doing="looking for a mind to match", contest="a row that could go either way",
        places=["gather.talk", "learn.higher", "gather.circle"],
        people=dict(coach="a friend who married their sparring partner", rival="a clever rival for their attention",
                    peer="the crowd from the debating nights", patron="a host whose dinners mix the right people"),
        round=["evening classes", "a friend's dinner party", "the discussion night each week"],
        prep=["courting", "study", "public speaking"],
        meets=["belonging", "meaning"],
        below="{N} goes quiet around dull charm and lights up at anyone who argues back",
        tribal="to be joined to the one at the fire who answers every riddle with a better one",
        magic="to love a mind that keeps pace, a fellow student or a rival at the tower",
        rungs=[
            dict(say="a spark across the table", any=["girlfriend or boyfriend"],
                 years=(2, 0.5, 7), share=0.85, start=(17, 22, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="arguing till dawn, and loving it", any=["living together", "engaged"],
                 years=(2, 0.5, 5), share=0.7, contests_y=0.5, forks=["take"],
                 demand=dict(hours=4, money=0.05, entry=0.1, energy=0.2), window=None, upkeep=None),
            dict(say="a life of talk", any=["wife or husband", "married again", "nonromantic life partner"],
                 years=(3, 1, 7), share=0.7, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=3, money=0.03, entry=0.2, energy=0.2), window=None, upkeep=None),
            dict(say="still talking after all these years", any=["partner of many years"],
                 years=(12, 6, 25), share=0.6, contests_y=0.5, forks=["go_on", "pay"],
                 demand=dict(hours=3, money=0.02, entry=0, energy=0.15), window=None, upkeep=None),
        ]),

    # Clock: a first child at about 30 on average; the curious-house years while the children are small (a few
    # years to make it a habit); children grown at about 18 to 25; grandchildren some 25 to 35 years after one's own
    # first child (demographic counts; estimate for the spreads). Shares and demands: estimate.
    "to raise children who question everything": dict(
        shape="home", face="U R", sphere="", domain="children", area="line", calling=False,
        dreams=["to raise children well and teach them all one knows"],
        spark="the night of a hundred whys",
        thing="the children's questions", doing="raising curious children", contest="a hard term at school",
        places=["learn.keeping", "gather.house"],
        people=dict(coach="a teacher who loves a hard question", rival="a parent who thinks questions are cheek",
                    peer="other parents who teach at home", patron="a librarian who saves books for them"),
        round=["home-teaching for a year", "a school that welcomes questions", "the library's Saturday club"],
        prep=["caring for children", "study", "the household"],
        meets=["meaning", "belonging"],
        below="{N} answers a child's why with another why, and watches the little face light up",
        tribal="to raise children who ask the elders why, and are never afraid of the answer",
        magic="to raise children who question even the tower's masters, kindly and without fear",
        rungs=[
            dict(say="a child of your own", any=["mother or father", "stepparent", "adoptive parent",
                                                 "foster parent"],
                 years=(3, 1, 8), share=0.85, start=(20, 28, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.1, entry=0.2, energy=0.4), window=None, upkeep=None),
            dict(say="a house full of questions", any=["home-educating parent", "parent raising a child across languages",
                                                       "reader's ticket", "good telescope"],
                 years=(3, 1, 7), share=0.75, contests_y=0.5, forks=["pay"],
                 demand=dict(hours=6, money=0.1, entry=0.05, energy=0.45), window=None, upkeep=None),
            dict(say="children grown into their own minds", any=["parent of independent adult children",
                                                                 "parent with a child living abroad"],
                 years=(17, 12, 22), share=0.8, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
            dict(say="grandchildren asking why", any=["grandparent"],
                 years=(10, 3, 22), share=0.65, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
        ]),

    # Clock: first love in the late teens; moving in or engaged after 1 to 3 years; a wedding about a year or two
    # later; still in love after more than a decade is about half of couples who marry (estimate). Shares and
    # demands: estimate.
    "to love with everything": dict(
        shape="home", face="R", sphere="", domain="partner", area="love", calling=False,
        dreams=["a great love"],
        spark="saying it first",
        thing="love", doing="loving with everything", contest="a fight that might be the end",
        places=["gather.circle", "gather.great"],
        people=dict(coach="a grandparent still in love after fifty years", rival="a rival for their love",
                    peer="friends who hear every twist", patron="a friend who keeps setting them up"),
        round=["a friend's introduction", "a trip far from home", "the dance on Friday nights"],
        prep=["courting"],
        meets=["belonging", "meaning"],
        below="{N} falls hard and fast, and never once has kept a feeling to themselves",
        tribal="to love one person across every season and every camp",
        magic="to love as the old ballads love, whatever the towers say",
        rungs=[
            dict(say="falling hard", any=["girlfriend or boyfriend"],
                 years=(1.5, 0.3, 6), share=0.9, start=(16, 20, 35), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=5, money=0.08, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="all in, with no way back", any=["engaged", "living together"],
                 years=(1.5, 0.5, 4), share=0.65, contests_y=0.5, forks=["take"],
                 demand=dict(hours=4, money=0.05, entry=0.1, energy=0.3), window=None, upkeep=None),
            dict(say="the wedding of a lifetime", any=["newlywed", "wife or husband"],
                 years=(1.5, 0.5, 4), share=0.75, contests_y=0.5, forks=["pay"],
                 demand=dict(hours=3, money=0.05, entry=0.5, energy=0.35), window=None, upkeep=None),
            dict(say="still in love, years on", any=["partner of many years", "married again"],
                 years=(12, 6, 25), share=0.5, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=3, money=0.03, entry=0, energy=0.2), window=None, upkeep=None),
        ]),

    # Clock: a first child at about 26 to 30; a third child some 4 to 6 years later (families of three or more
    # children are about 1 in 6 to 1 in 5 of families with children in many places); children grown at 18 to 25;
    # grandchildren in the parents' fifties (demographic counts; estimate for the spreads). Shares and demands:
    # estimate.
    "to raise a big, loud family": dict(
        shape="home", face="R G", sphere="", domain="children", area="line", calling=False,
        dreams=["a big, noisy family"],
        spark="a whole weekend of other people's children",
        thing="a big family", doing="raising a houseful", contest="a winter with everyone ill at once",
        places=["gather.house", "gather.games", "gather.great"],
        people=dict(coach="a parent of six who makes it look easy", rival="a sibling with an even bigger brood",
                    peer="the other big families on the street", patron="grandparents who take the children on Sundays"),
        round=["fostering to fill the house", "a bigger house further out", "Sunday lunch with everyone, every week"],
        prep=["caring for children", "the household", "cooking"],
        meets=["belonging"],
        below="{N} is always the one at the big family meals with a cousin's baby on one knee",
        tribal="to fill the camp with children who run with the dogs",
        magic="to raise a houseful that the whole lane knows by its noise",
        rungs=[
            dict(say="a houseful in the making", any=["mother or father", "stepparent"],
                 years=(3, 1, 8), share=0.85, start=(18, 26, 36), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.1, entry=0.2, energy=0.45), window=None, upkeep=None),
            dict(say="more chairs round the table", any=["parent of three or more", "foster parent"],
                 years=(5, 2, 10), share=0.45, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.3, entry=0.2, energy=0.6), window=None, upkeep=None),
            dict(say="grown children who still come home", any=["parent of independent adult children",
                                                                "parent with a child living abroad"],
                 years=(18, 12, 24), share=0.8, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
            dict(say="grandchildren underfoot", any=["grandparent", "grandparent raising a grandchild"],
                 years=(8, 2, 20), share=0.8, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
        ]),

    # Clock: as for any partnership (a first partner in the twenties, a promise after about 2 to 4 years); a safe
    # home after a few years of saving or a secure tenancy; staying beside a partner through serious illness or
    # hardship is most couples who last (estimate). Shares and demands: estimate.
    "to protect the ones I love": dict(
        shape="home", face="R W", sphere="", domain="partner", area="love", calling=False,
        dreams=["a great love", "a marriage that lasts a lifetime"],
        spark="the man who followed them home",
        thing="the ones they love", doing="looking after the ones they love", contest="a crisis at home",
        places=["gather.house", "prot.rescue", "care.houses"],
        people=dict(coach="an old first-aider who taught them what to do", rival="a relative who thinks they fuss too much",
                    peer="friends who look out for each other", patron="a neighbour who has their back"),
        round=["a move to a safer street", "a family friend who can help", "the first-aid course each spring"],
        prep=["courting", "the household", "first aid"],
        meets=["belonging", "safety"],
        below="{N} walks on the road side of the pavement without ever being asked to",
        tribal="to stand between the one I love and every danger of the wild",
        magic="to be the shield of the one I love against every curse and blade",
        rungs=[
            dict(say="someone to stand beside", any=["girlfriend or boyfriend", "engaged"],
                 years=(2, 0.5, 6), share=0.9, start=(16, 22, 35), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0, energy=0.25), window=None, upkeep=None),
            dict(say="a promise made", any=["wife or husband", "living together", "nonromantic life partner"],
                 years=(2.5, 1, 6), share=0.75, contests_y=0.5, forks=["take"],
                 demand=dict(hours=3, money=0.05, entry=0.2, energy=0.25), window=None, upkeep=None),
            dict(say="a home where they are safe", any=["homeowner", "secure tenancy", "savings"],
                 years=(4, 1, 10), share=0.7, contests_y=1, forks=["pay"],
                 demand=dict(hours=3, money=0.15, entry=0.3, energy=0.3), window=None, upkeep=None),
            dict(say="beside them through the worst", any=["caregiving partner", "partner of many years"],
                 years=(12, 5, 30), share=0.6, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.1, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: family recipes and crafts are learned over childhood and youth; the gathering house usually passes in
    # one's forties or fifties; handing the ways on comes with grandchildren or teaching; the one the whole family asks
    # is one or two in a wide family (estimate). Shares and demands: estimate.
    "to keep the family's ways": dict(
        shape="home", face="G", sphere="", domain="community", area="line", calling=False,
        dreams=["the one the elders ask", "an elder whose counsel the clans seek",
                "to keep the band together through the hard seasons"],
        spark="the old dish made with nobody watching",
        thing="the family's ways", doing="keeping the old ways", contest="a feast day with half the family missing",
        places=["gather.house", "gather.great", "learn.keeping"],
        people=dict(coach="a grandmother who knows every recipe by heart", rival="a cousin who wants it all done the new way",
                    peer="the aunts in the kitchen", patron="the oldest uncle"),
        round=["the recipes written down and shared", "a community class in the old language",
               "the yearly feast at the old house"],
        prep=["cooking", "storytelling", "hosting"],
        meets=["belonging", "meaning"],
        below="{N} is the one in the kitchen at every family gathering, asking how the old dishes were made",
        tribal="to keep the clan's songs, foods and ways of the seasons, and hand them to the young",
        magic="to keep the house's old customs and charms, as the family has kept them for generations",
        rungs=[
            dict(say="the old ways learned by heart", any=["cooking for a crowd", "baking", "sewing and mending",
                                                           "telling a story aloud"],
                 years=(3, 1, 8), share=0.9, start=(8, 15, 50), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=2, money=0.02, entry=0, energy=0.15), window=None, upkeep=None),
            dict(say="the house where the family gathers", any=["partner in a multigenerational household",
                                                                "family who will always take you in", "paid-off home"],
                 years=(10, 4, 20), share=0.55, contests_y=1, forks=["pay"],
                 demand=dict(hours=4, money=0.1, entry=0.2, energy=0.35), window=None, upkeep=None),
            dict(say="the ways handed to the young", any=["grandparent", "community language teacher",
                                                         "grandparent raising a grandchild"],
                 years=(10, 4, 20), share=0.7, contests_y=1, forks=["take"],
                 demand=dict(hours=3, money=0.03, entry=0, energy=0.25), window=None, upkeep=None),
            dict(say="the one the whole family asks", any=["the one everyone asks", "old family name"],
                 req="was('grandparent') | has('cooking for a crowd') | has('telling a story aloud')", height="Known",
                 years=(8, 3, 18), share=0.4, contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.02, entry=0, energy=0.2), window=None, upkeep=None),
        ]),

    # Clock: a first child at about 27; a third child or a fostered one some 5 years later; the first grandchild
    # about 25 to 35 years after one's own first child; heading a wide family in one's sixties or seventies
    # (demographic counts; estimate for the spreads). Shares and demands: estimate.
    # v1 has 5 steps for the home shape's 4 rungs: "the children grown and still close" (no height, any: "parent of
    # independent adult children", "in-laws who took you in") is left out; its time passes inside the grandchild rung.
    "to grow old among many grandchildren": dict(
        shape="home", face="G", sphere="", domain="children", area="line", calling=False,
        dreams=["a big, noisy family", "a family of one's own", "a grandmother or grandfather to the whole camp"],
        spark="the cousins all under one roof",
        thing="a big family", doing="growing a big family", contest="a winter when the family is stretched",
        places=["gather.house", "gather.great"],
        people=dict(coach="an old grandmother with a crowd of grandchildren", rival="the other grandparents",
                    peer="the other grandparents at the school gate", patron="the eldest child"),
        round=["fostering", "moving closer to the children", "Sunday dinner for everyone, every week"],
        prep=["caring for children", "the household", "hosting"],
        meets=["belonging"],
        below="{N} always ends up holding the babies at weddings, and never minds a crowded table",
        tribal="to grow old by the fire with the clan's children and their children around",
        magic="to be the old head of a great house, its halls loud with grandchildren",
        rungs=[
            dict(say="a family of one's own", any=["mother or father", "stepparent", "adoptive parent"],
                 years=(3, 1, 8), share=0.85, start=(18, 27, 38), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.1, entry=0.2, energy=0.45), window=None, upkeep=None),
            dict(say="a house full of children", any=["parent of three or more", "foster parent",
                                                     "guardian of an unrelated child"],
                 years=(5, 2, 10), share=0.45, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.3, entry=0.2, energy=0.6), window=None, upkeep=None),
            dict(say="the first grandchild", any=["grandparent", "grandparent raising a grandchild"],
                 years=(25, 18, 35), share=0.75, contests_y=0, forks=[], time=True,
                 demand=dict(hours=1, money=0, entry=0, energy=0.05), window=None, upkeep=None),
            dict(say="the head of a big family", any=["the one everyone asks", "family who will always take you in"],
                 req="was('grandparent')", height="Known",
                 years=(8, 3, 20), share=0.5, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0, energy=0.3), window=None, upkeep=None),
        ]),

    # Clock: a shared home in the mid-twenties; a roof of one's own a few years later (a tenancy or a purchase); an
    # open table within a few years; fostering or a door that never shuts after about a decade (estimate). Shares
    # and demands: estimate.
    "to make a home everyone is welcome in": dict(
        shape="home", face="G W", sphere="", domain="partner", area="home", calling=False,
        dreams=["a marriage that lasts a lifetime"],
        spark="dinner for nine and four chairs",
        thing="an open home", doing="keeping an open house", contest="a full house in a lean month",
        places=["gather.house", "gather.hall"],
        people=dict(coach="a neighbour whose door is always open", rival="a neighbour who minds the comings and goings",
                    peer="the friends who always drop in", patron="in-laws who took them in"),
        round=["the shared supper at the community hall", "a spare room for whoever needs it",
               "the open table every Sunday"],
        prep=["hosting", "cooking", "the household"],
        meets=["belonging", "meaning"],
        below="{N} keeps an extra plate warm and a spare blanket on the sofa, just in case",
        tribal="to keep a hearth where any of the clan can sit down and eat",
        magic="to keep a house whose door the old wards open to any friend",
        rungs=[
            dict(say="someone to make a home with", any=["living together", "wife or husband",
                                                        "nonromantic life partner"],
                 years=(2, 0.5, 6), share=0.9, start=(18, 24, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=2, money=0.05, entry=0.2, energy=0.15), window=None, upkeep=None),
            dict(say="a roof of one's own", any=["homeowner", "secure tenancy", "paid-off home"],
                 years=(4, 1, 10), share=0.7, contests_y=0.5, forks=["pay"],
                 demand=dict(hours=3, money=0.2, entry=0.6, energy=0.3), window=None, upkeep=None),
            dict(say="a table that always has room", any=["cooking for a crowd", "in-laws who took you in",
                                                         "neighbour who has your back"],
                 years=(3, 1, 8), share=0.75, contests_y=1, forks=["go_on"],
                 demand=dict(hours=4, money=0.1, entry=0, energy=0.35), window=None, upkeep=None),
            dict(say="a door that never shuts", any=["foster parent", "guardian of an unrelated child",
                                                    "partner of many years"],
                 years=(8, 3, 20), share=0.5, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.1, entry=0.05, energy=0.45), window=None, upkeep=None),
        ]),

    # Clock: a family tree of a few generations takes amateur researchers about 1 to 3 years of evenings; a local
    # history in print most often comes after a decade of archive work, and most such researchers start after 40;
    # a history read nationally is rare (estimate). Shares and demands: estimate.
    # v1 has 5 steps for the home shape's 4 rungs: "the town's past as well" (no height, any: "historical reenactment
    # member", "archivist", "museum curator", "community language teacher") is left out, so every v1 height stays.
    "to know where we come from": dict(
        shape="home", face="G U", sphere="learn", domain="", area="line", calling=True,
        dreams=["to walk the lands of the ancestors"],
        spark="a box of photographs nobody can name",
        thing="the family's past", doing="tracing the family's past", contest="a record that may not exist",
        places=["learn.keeping", "learn.higher", "gather.talk"],
        people=dict(coach="the archivist at the record office", rival="a distant cousin with a different family tree",
                    peer="the local history society", patron="a publisher of local history"),
        round=["old records in another town's archive", "the old relatives' memories, written down",
               "the history society's monthly meeting"],
        prep=["records and archives", "study", "storytelling"],
        meets=["meaning", "competence"],
        below="{N} asks the old relatives about the faces in the photographs until they tire of it",
        tribal="to know the names of the clan's dead back to the first fire, and where each one walked",
        magic="to read the house's long rolls back to its founding, and know every name in them",
        rungs=[
            dict(say="the family tree on the wall",
                 any=["finding things out", "second language", "reader's ticket", "archive research"],
                 years=(2, 0.5, 5), share=0.9, start=(12, 40, 75), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=3, money=0.03, entry=0.02, energy=0.15), window=None, upkeep=None),
            dict(say="the one who knows the old stories",
                 any=["book in print", "the one everyone asks", "name in the field"],
                 req="has('archive research')", height="Known",
                 years=(6, 2, 15), share=0.4, contests_y=1, forks=["pay"],
                 demand=dict(hours=5, money=0.05, entry=0.05, energy=0.3), window=None, upkeep=None),
            dict(say="a history read across the country", any=["known across the country"],
                 req="has('archive research')", height="Notable",
                 years=(8, 3, 20), share=0.08, contests_y=0.5, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0.05, energy=0.35), window=None, upkeep=None),
            dict(say="the town's history, still read", any=["a work that outlives you"],
                 req="has('archive research')", height="Historic",
                 years=(10, 5, 25), share=0.15, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=6, money=0.03, entry=0, energy=0.35), window=None, upkeep=None),
        ]),

    # New field for the dream "to take in a child who has no one" (dreams.py: means W1, domain children, stages
    # young_adult to mature).
    # Clock: foster-carer assessment usually takes about 4 to 8 months after a first enquiry, and only a minority of
    # those who enquire go on to apply; approval panels sit about monthly, and an approved carer is reviewed every
    # year; a first placement often follows within months of approval; about 1 in 4 to 1 in 3 long-term placements
    # end early (placement-stability counts, estimate); a child placed young is grown about 10 to 15 years later.
    # Shares and demands: estimate (allowances cover much of a foster child's keep, so the yearly money is low).
    "to take in a child who has no one": dict(
        shape="home", face="W", sphere="", domain="children", area="line", calling=False,
        dreams=["to take in a child who has no one"],
        thing="fostering", doing="giving a child a home", contest="a hard stretch with a child who will not settle",
        places=["gather.talk", "care.houses"],
        people=dict(coach="an experienced foster carer", peer="the foster carers' support group",
                    patron="a social worker who believes in them"),
        round=["short breaks for another family's foster child first", "a different fostering agency",
               "the carers' support group each month"],
        prep=["caring for children", "the household"],
        meets=["meaning", "belonging"],
        below="{N} always notices the child left at the school gate after everyone else has been collected, and waits with them",
        tribal="to bring a child of the camp who has lost their kin to one's own fire, and raise them as one's own",
        magic="to take a foundling of the city into one's own house and raise them under its roof",
        rungs=[
            dict(say="checked, trained and approved", any=["approved foster carer"],
                 years=(1, 0.5, 2.5), share=0.85, start=(24, 30, 55), contests_y=1, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.1, energy=0.3),
                 window=dict(every=0.083, open_weeks=1, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=1, kept_by=["fostering", "carers' training"])),
            dict(say="a child who had no one, at home", any=["foster parent", "adoptive parent",
                                                             "guardian of an unrelated child",
                                                             "grandparent raising a grandchild"],
                 years=(0.5, 0.1, 2), share=0.9, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.1, entry=0.1, energy=0.65), window=None, upkeep=None),
            dict(say="a home that held", any=["long-term foster parent", "adoptive parent",
                                              "guardian of an unrelated child"],
                 years=(3, 1, 7), share=0.6, contests_y=1, forks=["go_on", "pay"],
                 demand=dict(hours=10, money=0.1, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a child who had no one, grown up and at home",
                 any=["parent of independent adult children", "foster parent to many"],
                 req="was('foster parent') | was('adoptive parent') | was('guardian of an unrelated child')",
                 years=(10, 4, 16), share=0.6, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.4), window=None, upkeep=None),
        ]),
}


# ==== part d: from v25-prep/library/fields/fields-d.py, its header:
# Chroma Library, modern Earth: aims as fields, part D (v25 prep, Library, 10-23). DRAFT: nothing here is built,
# run or merged before Friday 10-23 21:00 (Emren's time); the Library pours it into earth_fields.py (FIELDS_EARTH),
# and NEW_TITLES into earth_perks_titles.py with their doors.
#
# Holds the shapes land, faith and venture (briefs/fields-by-shape.txt): v1's 5 land aims, 5 faith aims and 3
# adventure aims (earth_aims.py, keys kept exactly, with v1's `area` and `spark`), and the new dream fields "to run an
# animal sanctuary", "to breed champion horses" and "to explore the far places". Not here: the land's 30 ways
# (land-ways.py) and the packs' fields. Template: chroma-engine/notes/v25/aims-shape.md section 8 (chess), key for
# key, with the keys section 3 froze later (prep, meets; per rung demand, window, upkeep).
#
# Read with the brief (briefs/FIELDS.md) and Emren's v25 decisions (briefs/V25-DECISIONS.md, "Aims"):
# - `share` is per rung: of those who keep at it from the rung below, the share who reach this one (as chess). The
#   comment above each field gives the medians' sum and the share of starters who reach the top (the product).
# - `years` are (median, 10th, 90th percentile) of steady effort from the rung below. Sources are named where known;
#   the rest are "estimate".
# - `demand` is at steady intensity: hours a week, money a year and a one-time entry cost (each 0 to 1 of a year's
#   free money) and energy (0 to 1, how tiring). All estimates. A paid rung's hours are the pursuit's own hours beyond
#   the job's.
# - `window` only where outside timing is real (a show season, an expedition season, an exam sitting); `upkeep` only
#   where something truly fades without use (a tongue, a ticket, a place in a congregation). Most are None.
# - `prep` tags name shared preparation (two aims sharing a tag count those hours once); `meets` names the needs the
#   practice restores (belonging, meaning, competence).
# - Every rung's ways in are the field's `places` (one to three haunts), its `people` and its `round` (three ways
#   round a block, the first of them recurring: a weekly club, a monthly meeting, a yearly show), and its contest.
# - `spark` is kept from v1 beside the field keys (the spark moments in earth_aim_moments-*.lib read it).
# - `land` takes 3 to 5 rungs (tending, keeping, stewarding, guarding, a land kept for good): the v1 land aims keep
#   all of v1's steps; the two new land fields use rungs 0 to 2. `faith` has 5 rungs (seeking, belonging, serving,
#   guiding, a teacher remembered) and `venture` 4 (first steps out, a seasoned hand, known for it, a legend of it);
#   `skip` names the shape rungs a shorter faith or venture field leaves out.
# - Contests: land's is a show or a fair (or, out of doors, a hard trek); faith's is a rite or a trial of faith;
#   venture's is a hard crossing or an exam. None comes with age alone, so no rung here has `time=True`.

_FIELDS_D = {

    # ================================================================ land (5 rungs)

    # B G. All four v1 steps (rungs 0 to 3). Estimate: farm successors usually take over in their thirties or forties
    # after a long wait, and hand on in their sixties; many farms have no named successor, so few hand the land on whole
    # (farm succession surveys, read loosely). Sum 50 years; top .9 x .45 x .7 x .5 = about 14 in 100 of those who start.
    "to keep the family land": dict(
        shape="land", area="land", face="B G", sphere="prod", domain="children", calling=False,
        dreams=["a family name that counts for something", "to found a clan of one's own"],
        below="{N} walks the boundary of the family's field on Sundays, and knows every post by name",
        tribal="to hold the clan's grazing grounds whole for the children's children",
        magic="to keep the family's charter lands from the baron's surveyors and the guild's buyers",
        spark="the season the land is yours to keep",
        thing="the family land", doing="working the family land", contest="the harvest fair",
        places=["prod.land", "gather.hall"],
        people=dict(coach="the old farmer next door", rival="a cousin with a claim on the land",
                    peer="the farming families round about", patron="a land agent who knows the family"),
        round=["the young farmers' club on a weeknight", "a lease on a neighbour's field",
               "a share-farming deal with an older farmer"],
        prep=["growing", "animals", "farm work"], meets=["belonging", "meaning"],
        rungs=[
            dict(say="hands on the family ground", any=["farm hand", "growing food", "handling animals"],
                 years=(2, 0.5, 5), share=0.9, start=(8, 18, 40), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="the land in your own name", any=["farmer", "plot of land", "inheritance"],
                 years=(20, 8, 35), share=0.45, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=20, money=0.15, entry=0.3, energy=0.7), window=None, upkeep=None),
            dict(say="the old name held", any=["old family name", "paid-off home", "family business"],
                 years=(8, 3, 15), share=0.7, contests_y=1, forks=["go_on"],
                 demand=dict(hours=20, money=0.1, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="the land handed on whole", any=["parent of independent adult children", "grandparent"],
                 req="has('plot of land') | was('farmer') | has('old family name')",
                 years=(20, 10, 35), share=0.5, contests_y=1, forks=["pay"],
                 demand=dict(hours=12, money=0.1, entry=0.2, energy=0.4), window=None, upkeep=None),
        ]),

    # R G. All four v1 steps (rungs 0 to 3). Estimate: wild skills (navigation, water, ropes) take a few seasons;
    # outdoor-instructor and ranger awards two to five years of logged days, revalidated every few years, and posts are
    # few; owning a patch of wild ground is mostly a matter of saving. Sum 18 years; top .9 x .6 x .45 x .3 = about 7
    # in 100.
    "to live wild and free outdoors": dict(
        shape="land", area="land", face="R G", sphere="prod", domain="", calling=False,
        dreams=["to climb the highest mountains", "to raise a wolf cub"],
        below="{N} is out of the door at the first break in the rain and the last one in at dusk",
        tribal="to live by the hunt and the river, far from the camp's fires",
        magic="to range the deep forests past the last of the towers",
        spark="the first night alone on the hill",
        thing="the outdoors", doing="living out of doors", contest="a long trek in hard weather",
        places=["prod.wild", "prot.rescue"],
        people=dict(coach="an old hand on the hills", rival="a climber who always goes further",
                    peer="the people who are always out", patron="a landowner who lets them camp"),
        round=["the walking club's Sunday outing", "a season's work on a trail crew", "a friend's hut in the hills"],
        prep=["the outdoors", "fitness", "navigation"], meets=["competence", "meaning"],
        rungs=[
            dict(say="out in all weathers", any=["knowing the woods", "swimming", "fishing licence"],
                 years=(1, 0.3, 3), share=0.9, start=(8, 16, 30), contests_y=1, forks=["go_on"],
                 demand=dict(hours=5, money=0.02, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="the skills of the wild", any=["hunting and fishing", "boat handling", "head for heights",
                                                    "chainsaw ticket"],
                 years=(3, 1, 6), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.05, entry=0.1, energy=0.6), window=None,
                 upkeep=dict(of="proficiency", years=5, kept_by=["time out of doors"])),
            dict(say="a living out of doors", any=["outdoor instructor", "forester", "park ranger"],
                 years=(4, 2, 8), share=0.45, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.03, entry=0.15, energy=0.7), window=None,
                 upkeep=dict(of="credential", years=3, kept_by=["instructing", "a refresher course"])),
            dict(say="a patch of the wild to call your own", any=["plot of land", "place by the sea",
                                                                  "horse of one's own"],
                 years=(10, 4, 20), share=0.3, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.1, entry=0.5, energy=0.4), window=None, upkeep=None),
        ]),

    # G. All five v1 steps. Estimate: a new farmer usually needs a few seasons as a hand before land of their own, some
    # years of shows and markets before a name for produce, and fifteen years or more before others come to learn; a
    # seed or a method that outlives the farm is very rare. The harvest show is yearly. Sum 34 years; top .9 x .45 x .4
    # x .15 x .2 = about 5 in 1,000.
    "to work the land": dict(
        shape="land", area="land", face="G", sphere="prod", domain="career", calling=True,
        dreams=["a farmer", "the biggest farm in the valley", "to carry on the family holding"],
        below="{N} slows at every field on the road out of town, reading what is growing and how well",
        tribal="to keep the clan's fields and herds through every season",
        magic="to tend the tower's growing gardens, where the old herbs still answer",
        spark="a first crop from a borrowed field",
        thing="farming", doing="working the land", contest="the harvest show",
        places=["prod.land", "comm.market"],
        people=dict(coach="an old farmer who takes them on", rival="the farm across the valley",
                    peer="the growers at the market", patron="a buyer who takes the whole crop"),
        round=["the weekly farmers' market", "a rented field on the edge of town",
               "a season on someone else's farm"],
        prep=["growing", "farm work", "animals"], meets=["competence", "meaning"],
        rungs=[
            dict(say="land of one's own to work",
                 any=["farm hand", "growing food", "gardener or groundskeeper", "farmer", "plot of land"],
                 years=(3, 1, 7), share=0.9, start=(10, 20, 40), contests_y=1, forks=["go_on"],
                 demand=dict(hours=10, money=0.05, entry=0.1, energy=0.7), window=None, upkeep=None),
            dict(say="a name for good produce", any=["good name in town", "contact in the trade", "loyal clientele"],
                 req="was('farmer') | was('farm hand') | has('plot of land')", height="Known",
                 years=(5, 2, 10), share=0.45, contests_y=1, forks=["pay"],
                 demand=dict(hours=15, money=0.1, entry=0.3, energy=0.7),
                 window=dict(every=1, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="the farm others learn from", any=["apprentice of one's own", "the one everyone asks"],
                 req="was('farmer')",
                 years=(8, 4, 15), share=0.4, contests_y=2, forks=["take"],
                 demand=dict(hours=12, money=0.05, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a farm known across the country", any=["known across the country"],
                 req="was('farmer')", height="Notable",
                 years=(8, 4, 20), share=0.15, contests_y=2, forks=["take"],
                 demand=dict(hours=12, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a farm and a seed others still grow", any=["a work that outlives you"],
                 req="was('farmer')", height="Historic",
                 years=(10, 5, 25), share=0.2, contests_y=1, forks=["go_on"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # G W. All five v1 steps. Estimate: neighbours share within a season or two of a first crop; community gardens are
    # often set up and run by one or two people within a few years; few become a model copied far away. Sum 18 years;
    # top .9 x .8 x .35 x .4 x .1 = about 1 in 100.
    "to feed the street from my garden": dict(
        shape="land", area="land", face="G W", sphere="prod", domain="community", calling=True,
        dreams=["to make one's town a green and fair place to live"],
        below="{N} leaves bags of beans on the neighbours' steps every summer and says nothing about it",
        tribal="to fill the clan's baskets from one's own patch in the hungry months",
        magic="to keep the guild garden whose fruit feeds the lane",
        spark="more beans than one house can eat",
        thing="the street garden", doing="growing food for the street", contest="the street's harvest fair",
        places=["prod.land", "gather.hall"],
        people=dict(coach="an old allotment hand", rival="a neighbour who wants the plot for parking",
                    peer="the neighbours who lend a hand", patron="a council officer who can lend land"),
        round=["the allotment society's monthly meeting", "a corner of the school field",
               "a patch of waste ground the council lends"],
        prep=["growing", "organising"], meets=["belonging", "meaning"],
        rungs=[
            dict(say="a few rows of one's own", any=["growing food", "plot of land"],
                 years=(1, 0.5, 3), share=0.9, start=(10, 45, 65), contests_y=1, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0.03, energy=0.3), window=None, upkeep=None),
            dict(say="sharing over the fence", any=["neighbour who has your back", "neighbourhood volunteer",
                                                   "community-kitchen volunteer"],
                 years=(1, 0.5, 3), share=0.8, contests_y=1, forks=["pay"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="the street's own garden", any=["community-garden coordinator", "housing-cooperative member"],
                 years=(3, 1, 8), share=0.35, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0.05, energy=0.4), window=None,
                 upkeep=dict(of="access", years=2, kept_by=["tending the plot"])),
            dict(say="the one the street thanks", any=["good name in town", "trusted with the keys"],
                 req="was('community-garden coordinator') | has('growing food')", height="Known",
                 years=(5, 2, 12), share=0.4, contests_y=1, forks=["go_on"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="a street garden others copy across the country", any=["known across the country"],
                 req="was('community-garden coordinator')", height="Notable",
                 years=(8, 4, 20), share=0.1, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # G U. All five v1 steps. Estimate: horticultural certificates take one to three years beside work, and a
    # plant-lover's knowledge of hundreds of plants most of a decade; gardens open to visitors in a yearly season; a
    # garden known across the country takes decades. Sum 25 years; top .9 x .6 x .5 x .25 x .08 = about 5 in 1,000.
    "to grow the perfect garden": dict(
        shape="land", area="land", face="G U", sphere="", domain="", calling=True,
        dreams=["a garden of one's own", "the finest garden in the street", "a manor with orchards",
                "to find every rare herb in the deep woods"],
        below="{N} reads seed packets like letters and knows every plant on the walk to the shops",
        tribal="to tend the finest herb patch in the clan, where every plant is known",
        magic="to grow the walled garden where every rare root of the old books will take",
        spark="the bed that will not take",
        thing="gardening", doing="gardening", contest="the flower show",
        places=["prod.land", "learn.keeping"],
        people=dict(coach="a head gardener", rival="the prize-winner two doors down", peer="the garden club",
                    patron="the owner of a big garden who wants help"),
        round=["the garden club's monthly talk", "an allotment across town",
               "a walled garden that needs a volunteer"],
        prep=["growing", "naturalist"], meets=["competence"],
        rungs=[
            dict(say="seeds on the windowsill", any=["growing food", "beekeeping"],
                 years=(1, 0.3, 3), share=0.9, start=(8, 40, 70), contests_y=1, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.2), window=None, upkeep=None),
            dict(say="a garden of one's own", any=["plot of land", "homeowner", "gardener or groundskeeper"],
                 years=(4, 1, 10), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.05, entry=0.3, energy=0.3), window=None, upkeep=None),
            dict(say="every plant known by name", any=["knowing the woods", "hives of one's own", "community observer"],
                 years=(6, 3, 12), share=0.5, contests_y=2, forks=["go_on"],
                 demand=dict(hours=8, money=0.05, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="the garden people come to see", any=["good name in town", "trophies won"],
                 req="has('growing food')", height="Known",
                 years=(6, 3, 15), share=0.25, contests_y=3, forks=["take"],
                 demand=dict(hours=10, money=0.06, entry=0.05, energy=0.4),
                 window=dict(every=1, open_weeks=16, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a garden known across the country", any=["known across the country"],
                 req="has('growing food')", height="Notable",
                 years=(8, 4, 20), share=0.08, contests_y=3, forks=["take"],
                 demand=dict(hours=10, money=0.06, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # G W (dream means G.4 W.3 R.3). New field, rungs 0 to 2. Estimate: shelter volunteers who foster often start
    # within a year or three; a sanctuary of one's own needs land, a charity's paperwork and years of fundraising, and
    # is close to full-time work. Sum 12 years; top .9 x .45 x .1 = about 4 in 100.
    "to run an animal sanctuary": dict(
        shape="land", face="G W", sphere="prod", domain="", calling=True,
        dreams=["an animal sanctuary"],
        thing="rescued animals", doing="caring for rescued animals", contest="the yearly open day",
        places=["prod.land", "gather.hall"],
        people=dict(coach="the old hand who runs the rescue yard", rival="a neighbour who complains about the noise",
                    peer="the volunteers at the yard", patron="a donor who pays the feed bill"),
        round=["the rescue yard's Saturday shift", "fostering for a shelter in the next town",
               "a farmer with a spare barn"],
        below="{N} brings home every stray that follows them and has a name for it by teatime",
        tribal="to keep a fold where every lame beast the hunters spare can mend",
        magic="to keep a refuge where every hurt creature of the forest, plain or strange, finds a stall",
        prep=["animals", "farm work", "fundraising"], meets=["meaning", "belonging"],
        rungs=[
            dict(say="a hand at the rescue yard", any=["handling animals", "animal care worker",
                                                      "animal-shelter campaigner"],
                 years=(1, 0.3, 3), share=0.9, start=(8, 25, 60), contests_y=1, forks=["go_on"],
                 demand=dict(hours=4, money=0.01, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="rescued animals at home", any=["animal fosterer"],
                 years=(3, 1, 8), share=0.45, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.08, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="a sanctuary where no animal is turned away", any=["sanctuary keeper"],
                 req="has('plot of land') | was('farmer')", height="Known",
                 years=(8, 3, 20), share=0.1, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=30, money=0.3, entry=0.6, energy=0.8), window=None, upkeep=None),
        ]),

    # G U (dream means G.4 U.3 B.3). New field, rungs 0 to 2. Estimate: a mare carries for about eleven months and a
    # foal competes at three to five, in a yearly show season, so a breeder sees only a few generations in a working
    # life; a winning foal usually comes after several, and a known bloodline after decades. Horses are dear to keep.
    # Sum 25 years; top .9 x .3 x .05 = about 1 in 100.
    "to breed champion horses": dict(
        shape="land", face="G U", sphere="prod", domain="", calling=True,
        dreams=["to breed champion horses"],
        thing="horse breeding", doing="breeding horses", contest="the horse show",
        places=["prod.land", "gather.games"],
        people=dict(coach="an old horse breeder", rival="a rival breeder at the shows", peer="the people at the yard",
                    patron="an owner who backs a foal"),
        round=["the riding school's weekly lessons", "a yard that swaps work for rides",
               "a breeder who sells a share in a mare"],
        below="{N} knows every horse in the next field by its walk, and which mare's foal will be the fast one",
        tribal="to raise the herd's swiftest runners, the ones the clans trade for",
        magic="to breed the steeds the court's riders ask for by name",
        prep=["animals", "riding"], meets=["competence"],
        rungs=[
            dict(say="a horse to look after", any=["horse of one's own", "stable groom"],
                 years=(2, 0.5, 5), share=0.9, start=(6, 14, 35), contests_y=2, forks=["pay"],
                 demand=dict(hours=6, money=0.2, entry=0.3, energy=0.5), window=None, upkeep=None),
            dict(say="a first foal that wins", any=["horse breeder"],
                 req="has('horse of one's own') | was('stable groom') | has('plot of land')",
                 years=(8, 4, 15), share=0.3, contests_y=4, forks=["go_on", "take"],
                 demand=dict(hours=12, money=0.3, entry=0.3, energy=0.6),
                 window=dict(every=1, open_weeks=20, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a line of horses known everywhere", any=["breeder of champions"],
                 req="was('horse breeder')", height="Notable",
                 years=(15, 8, 30), share=0.05, contests_y=5, forks=["take"],
                 demand=dict(hours=15, money=0.3, entry=0.2, energy=0.6), window=None, upkeep=None),
        ]),

    # ================================================================ faith (5 rungs)

    # U. skip the fifth rung (a teacher remembered): v1's four steps are seeking, belonging (reading every side, among
    # other readers), serving (an answer lived by) and guiding. Estimate: most people who seek settle on an answer,
    # a faith or none, within a few years of serious reading; fewer become the one others bring doubts to. Sum 19
    # years; top .9 x .6 x .5 x .2 = about 5 in 100.
    "to find out what is true": dict(
        shape="faith", area="faith", face="U", sphere="", domain="faith", calling=False,
        dreams=["to know what the old stories really mean", "to learn the secrets the old gods keep"],
        below="{N} asks the questions nobody at the table wants asked, and listens hard to every answer",
        tribal="to find out what the old stories really mean, and whether the spirits truly hear",
        magic="to learn what the old powers truly are, beneath the tales the temples tell",
        spark="the argument with the old believer",
        thing="the big questions", doing="searching for what is true", contest="a trial of faith",
        places=["faith.seeking", "learn.keeping", "gather.talk"],
        people=dict(coach="a patient teacher of the faiths", rival="a believer who argues back",
                    peer="the people at the discussion group", patron="an old scholar who lends books"),
        round=["the weekly discussion group at the library", "a different house of worship",
               "a teacher outside the family"],
        prep=["study", "public speaking"], meets=["meaning", "competence"],
        skip=[4],
        rungs=[
            dict(say="the big questions, asked out loud", any=["seeker", "finding things out"],
                 years=(1, 0.3, 3), share=0.9, start=(12, 30, 60), contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0, entry=0, energy=0.1), window=None, upkeep=None),
            dict(say="reading every side", any=["reader's ticket", "interfaith-dialogue participant",
                                                "archive research"],
                 years=(3, 1, 8), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=4, money=0.02, entry=0.02, energy=0.2), window=None, upkeep=None),
            dict(say="an answer to live by", any=["convert", "left the faith", "member of a monastic community",
                                                  "regular worshipper"],
                 years=(5, 2, 15), share=0.5, contests_y=1, forks=["take"],
                 demand=dict(hours=3, money=0.01, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="the one others bring their doubts to", any=["the one everyone asks", "lay religious teacher"],
                 height="Known",
                 years=(10, 4, 25), share=0.2, contests_y=1, forks=["go_on"],
                 demand=dict(hours=3, money=0, entry=0, energy=0.3), window=None, upkeep=None),
        ]),

    # U B. 5 rungs, none skipped. Estimate, from the study of ancient languages: two to four years of classes to read
    # a classical text with a dictionary (and it fades without reading), a teaching or archive post some years after,
    # and a reading or a translation that lasts only after decades of work. Sum 36 years; top .9 x .4 x .3 x .08 x .1 =
    # about 1 in 1,000.
    "to study the old texts": dict(
        shape="faith", area="faith", face="U B", sphere="learn", domain="faith", calling=True,
        dreams=["to learn the secrets the old gods keep", "to know what the old stories really mean"],
        below="{N} reads the old book with a pencil, and the margins fill with questions",
        tribal="to learn every word of the old tellings and what each one meant to the first people",
        magic="to read the first scrolls of the temple in their own tongue, and know what they hide",
        spark="the page in the old tongue",
        thing="the old texts", doing="reading the old texts", contest="a public disputation over a passage",
        places=["learn.keeping", "faith.orders", "learn.higher"],
        people=dict(coach="a teacher of the old tongue", rival="a scholar with another reading",
                    peer="the reading circle", patron="the keeper of a library's rare books"),
        round=["the weekly reading circle", "an evening class in the old tongue",
               "a teacher of the texts in another town"],
        prep=["study", "a second tongue"], meets=["competence", "meaning"],
        rungs=[
            dict(say="the tongue they were written in",
                 any=["scripture", "reader's ticket", "second language", "archive research", "interpreting"],
                 years=(3, 1, 6), share=0.9, start=(14, 25, 50), contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.05, entry=0.05, energy=0.4), window=None,
                 upkeep=dict(of="proficiency", years=5, kept_by=["reading the texts", "teaching"])),
            dict(say="a teacher of the texts",
                 any=["lay religious teacher", "archivist", "ordained religious minister"],
                 years=(5, 2, 10), share=0.4, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0.05, energy=0.4), window=None, upkeep=None),
            dict(say="the one others bring their questions to",
                 any=["the one everyone asks", "published research", "name in the field"],
                 height="Known",
                 years=(8, 4, 15), share=0.3, contests_y=2, forks=["go_on"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="a reading the whole country argues over", any=["known across the country"],
                 req="was('lay religious teacher') | was('archivist') | was('ordained religious minister') | has('published research')", height="Notable",
                 years=(10, 5, 20), share=0.08, contests_y=2, forks=["take"],
                 demand=dict(hours=10, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a translation still read", any=["a work that outlives you"],
                 req="was('lay religious teacher') | was('archivist') | was('ordained religious minister') | has('published research')", height="Historic",
                 years=(10, 5, 25), share=0.1, contests_y=1, forks=["go_on"],
                 demand=dict(hours=10, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # R. skip the fifth rung (a teacher remembered): singing is seeking, the music of worship belonging, leading the
    # song serving, the music people come for guiding. Estimate: choir members usually join within a year of singing
    # often; leading the singing for a house of worship takes some years of practice and a vacancy. Sum 16 years; top
    # .9 x .6 x .35 x .15 = about 3 in 100.
    "to feel something greater in the music": dict(
        shape="faith", area="faith", face="R", sphere="", domain="faith", calling=True,
        dreams=["a trance-dancer who heals"],
        below="{N} goes quiet and strange whenever a room full of people starts to sing",
        tribal="to dance with the drums until the spirits come close",
        magic="to sing the old chants until the temple stones hum",
        spark="the night the singing lifts the roof",
        thing="sacred song", doing="singing in worship", contest="the great feast-day service",
        places=["faith.congregation", "arts.song"],
        people=dict(coach="the choir leader", rival="a soloist who wants the same part", peer="the choir",
                    patron="an elder who wants more music"),
        round=["the choir's weekly practice", "a house of worship across town with a bigger choir",
               "a singing circle outside any one faith"],
        prep=["music practice", "worship"], meets=["belonging", "meaning"],
        skip=[4],
        rungs=[
            dict(say="singing until it lifts you", any=["singing", "choir member", "musical instrument"],
                 years=(1, 0.3, 3), share=0.9, start=(6, 20, 60), contests_y=2, forks=["go_on"],
                 demand=dict(hours=2, money=0, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="music at the heart of worship", any=["congregation musician", "regular worshipper",
                                                           "seeker"],
                 years=(2, 1, 5), share=0.6, contests_y=3, forks=["pay"],
                 demand=dict(hours=4, money=0.01, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="leading the room in song", any=["leading a ceremony", "folk musician",
                                                      "known face at worship"],
                 years=(5, 2, 12), share=0.35, contests_y=4, forks=["take"],
                 demand=dict(hours=5, money=0.01, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="the music people come for", any=["name on the local scene", "known face at worship"],
                 req="was('congregation musician') | was('folk musician') | was('choir member')", height="Known",
                 years=(8, 3, 20), share=0.15, contests_y=4, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # G W. skip the fifth rung (a teacher remembered): the weekly seat is seeking (a newcomer finding their place),
    # a known face belonging, a hand in its work serving, an elder guiding. Estimate: congregations' own counts put a
    # newcomer's welcome at months to two years (and a face not seen for a couple of years is soon a stranger again),
    # and lay leadership or eldership after ten to twenty years of service. Sum 20 years; top .9 x .75 x .45 x .3 =
    # about 9 in 100.
    "to belong to a congregation for life": dict(
        shape="faith", area="faith", face="G W", sphere="faith", domain="faith", calling=False,
        dreams=["to keep the family's old faith and hand it on", "to keep the clan's rites"],
        below="{N} drifts towards the singing whenever a door of a house of worship stands open",
        tribal="to stand in the clan's circle at every rite, from first naming to last",
        magic="to belong to the old shrine's fellowship, one voice among many",
        spark="missed at worship for the first time",
        thing="the congregation", doing="worshipping with the congregation",
        contest="a hard year for the congregation",
        places=["faith.congregation", "gather.hall"],
        people=dict(coach="an elder of the congregation", rival="a member who wants things done differently",
                    peer="the regulars", patron="the minister"),
        round=["the weekly service", "a smaller congregation nearer home", "the midweek study group"],
        prep=["worship", "volunteering"], meets=["belonging", "meaning"],
        skip=[4],
        rungs=[
            dict(say="a seat in the same place each week", any=["regular worshipper", "believer on the big days"],
                 years=(1, 0.2, 3), share=0.9, start=(6, 30, 70), contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.01, entry=0, energy=0.1), window=None, upkeep=None),
            dict(say="a known face", any=["known face at worship", "choir member", "congregation musician"],
                 years=(2, 1, 5), share=0.75, contests_y=1, forks=["pay"],
                 demand=dict(hours=3, money=0.02, entry=0, energy=0.1), window=None,
                 upkeep=dict(of="access", years=2, kept_by=["weekly worship"])),
            dict(say="a hand in its work", any=["trusted with the keys", "community-kitchen volunteer",
                                               "lay religious teacher"],
                 years=(5, 2, 12), share=0.45, contests_y=1, forks=["take"],
                 demand=dict(hours=4, money=0.02, entry=0, energy=0.2), window=None, upkeep=None),
            dict(say="one of its elders", any=["deacon or elder", "the one everyone asks"],
                 req="was('regular worshipper') | has('known face at worship')", height="Known",
                 years=(12, 5, 25), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.3), window=None, upkeep=None),
        ]),

    # G U. skip the fifth rung (a teacher remembered): time outdoors is seeking, a path of one's own belonging, a calm
    # others lean on serving, the one people come to guiding. Estimate: a steady quiet practice takes a few years to
    # settle; counselling training takes two to four years more. Sum 21 years; top .9 x .55 x .4 x .2 = about 4 in 100.
    "to live in balance": dict(
        shape="faith", area="faith", face="G U", sphere="", domain="faith", calling=False,
        dreams=["a keeper of the old grove", "to know what the old stories really mean"],
        below="{N} goes quiet on long walks and comes back steadier, without being able to say why",
        tribal="to walk in step with the seasons and the spirits of the land",
        magic="to keep the old balance of the grove, where every power has its weight",
        spark="a week with nothing in the diary",
        thing="a balanced life", doing="keeping to a quiet practice", contest="a long silent retreat",
        places=["faith.seeking", "prod.wild"],
        people=dict(coach="a teacher of stillness", rival="a restless friend who mocks it", peer="the sitting group",
                    patron="an older friend who keeps a retreat house"),
        round=["the weekly sitting group", "a long walk every morning", "a retreat house in the hills"],
        prep=["stillness", "the outdoors"], meets=["meaning"],
        skip=[4],
        rungs=[
            dict(say="time alone outdoors", any=["knowing the woods", "growing food", "hunting and fishing"],
                 years=(1, 0.3, 2), share=0.9, start=(10, 35, 70), contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=3, money=0, entry=0, energy=0.1), window=None, upkeep=None),
            dict(say="a path of one's own", any=["seeker", "convert"],
                 years=(4, 1, 10), share=0.55, contests_y=0.5, forks=["pay"],
                 demand=dict(hours=4, money=0.02, entry=0.03, energy=0.1), window=None, upkeep=None),
            dict(say="a calm others lean on", any=["calming people down", "counselling"],
                 years=(6, 2, 15), share=0.4, contests_y=0.5, forks=["take"],
                 demand=dict(hours=4, money=0.02, entry=0.1, energy=0.2), window=None, upkeep=None),
            dict(say="the one people come to when life tips over", any=["the one everyone asks"],
                 req="was('seeker') | has('calming people down') | has('counselling')", height="Known",
                 years=(10, 4, 25), share=0.2, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0, entry=0, energy=0.3), window=None, upkeep=None),
        ]),

    # ================================================================ venture (4 rungs)

    # U R. 4 rungs, none skipped. Language schools for diplomats count about 600 to 2,200 class hours to working
    # proficiency, by how far the tongue is from one's own (one to two years beside other work), and an unused tongue
    # fades within years; interpreter training takes two to three years more, and court accreditation, sat at a yearly
    # exam and renewed every few years, some years of practice. Sum 17 years; top .9 x .4 x .35 x .2 = about 3 in 100.
    "to speak every language I meet": dict(
        shape="venture", area="adventure", face="U R", sphere="", domain="", calling=True,
        dreams=["to speak five languages", "to travel the world"],
        below="{N} picks up the shopkeeper's greeting on the first day, and is chatting by the end of the week",
        tribal="to learn the speech of every clan the trading paths reach, and the far ones beyond",
        magic="to speak the tongues of every land in the realm, and a few the scholars call dead",
        spark="lost for words in a strange town",
        thing="languages", doing="learning languages", contest="a language exam",
        places=["learn.higher", "gather.talk"],
        people=dict(coach="a language teacher", rival="a classmate who learns faster", peer="the conversation group",
                    patron="an employer who needs a speaker"),
        round=["the weekly conversation evening", "a pen friend abroad",
               "a summer's work where nobody speaks your tongue"],
        prep=["a second tongue", "travel"], meets=["competence", "belonging"],
        rungs=[
            dict(say="a second tongue", any=["second language", "passport"],
                 years=(2, 1, 4), share=0.9, start=(6, 18, 40), contests_y=1, forks=["go_on"],
                 demand=dict(hours=4, money=0.03, entry=0.03, energy=0.3), window=None,
                 upkeep=dict(of="proficiency", years=5, kept_by=["speaking it", "reading it", "travel"])),
            dict(say="living among other speakers", any=["immigrant", "returned migrant", "family abroad"],
                 years=(3, 1, 8), share=0.4, contests_y=1, forks=["take"],
                 demand=dict(hours=4, money=0.05, entry=0.3, energy=0.4), window=None, upkeep=None),
            dict(say="words for a living", any=["translator", "interpreting", "community language teacher"],
                 years=(4, 2, 8), share=0.35, contests_y=1, forks=["pay"],
                 demand=dict(hours=10, money=0.03, entry=0.15, energy=0.5), window=None, upkeep=None),
            dict(say="the one they call when nobody understands", any=["court interpreter accreditation",
                                                                       "court interpreter", "the one everyone asks"],
                 height="Known",
                 years=(8, 3, 15), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.02, entry=0.05, energy=0.5),
                 window=dict(every=1, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=dict(of="credential", years=5, kept_by=["court work", "requalifying"])),
        ]),

    # B R. skip the fourth rung (a legend of it): v1's three steps are first steps out, a seasoned hand and known for
    # it. Estimate: a diving or rigging ticket takes weeks of training but most come after a few years of growing
    # risks, and the skill goes rusty within a couple of years off; a local name for daring takes years more, and few
    # want it or get it. Sum 8.5 years; top .9 x .5 x .15 = about 7 in 100.
    "to chase the next thrill": dict(
        shape="venture", area="adventure", face="B R", sphere="", domain="", calling=False,
        dreams=["an adventurer", "the boldest rider in the town", "to climb the highest mountains",
                "the boldest of the young hunters"],
        below="{N} climbs the highest tree in the park and stays up there long after the others go home",
        tribal="to be first across the river in flood and first up the cliff for the eagles' eggs",
        magic="to ride the storm-roads and climb the haunted towers just to see the view",
        spark="the jump that nobody else will take",
        thing="thrills", doing="chasing thrills", contest="a race or a big jump",
        places=["gather.games", "prod.wild"],
        people=dict(coach="an instructor who insists on the checks", rival="a friend who always goes one further",
                    peer="the crowd at the climbing wall", patron="a sponsor"),
        round=["the climbing wall's weekly night", "a club that trains people properly",
               "a new sport nobody in town does yet"],
        prep=["fitness", "risk sports"], meets=["competence"],
        skip=[3],
        rungs=[
            dict(say="the first rush", any=["motorbike licence", "head for heights", "swimming"],
                 years=(0.5, 0.2, 2), share=0.9, start=(10, 20, 35), contests_y=2, forks=["go_on"],
                 demand=dict(hours=3, money=0.05, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="bigger risks, more often", any=["diving certificate", "rigging ticket", "cards for money"],
                 years=(3, 1, 7), share=0.5, contests_y=4, forks=["pay"],
                 demand=dict(hours=5, money=0.1, entry=0.15, energy=0.7), window=None,
                 upkeep=dict(of="proficiency", years=2, kept_by=["regular dives or climbs"])),
            dict(say="a name for daring", any=["following online", "local hero", "name on the local scene"],
                 years=(5, 2, 12), share=0.15, contests_y=4, forks=["take"],
                 demand=dict(hours=5, money=0.1, entry=0.05, energy=0.7), window=None, upkeep=None),
        ]),

    # R. 4 rungs, none skipped. Estimate: most long-term travellers save a year or so for a first trip; a life on the
    # move (seafaring, a van) takes some years of short trips first; settling in a second country takes years of
    # residence (residence rules often ask about five). Sum 14 years; top .9 x .55 x .3 x .35 = about 5 in 100.
    "to see the world": dict(
        shape="venture", area="adventure", face="R", sphere="", domain="", calling=False,
        dreams=["to travel the world", "to see the great sea", "an adventurer"],
        below="{N} keeps a map on the bedroom wall and knows the departure board by heart",
        tribal="to walk past the far hills and see what the traders have seen",
        magic="to ride with the caravans to every realm on the old maps",
        spark="a ticket bought on a whim",
        thing="travel", doing="travelling", contest="a long journey overland",
        places=["gather.talk", "gather.great"],
        people=dict(coach="an old traveller", rival="a friend who has been further", peer="the people met on the road",
                    patron="an employer who sends staff abroad"),
        round=["the travellers' meet-up each month", "a working holiday", "a job on a ship"],
        prep=["travel", "a second tongue"], meets=["meaning"],
        rungs=[
            dict(say="a bag packed and a way out", any=["passport", "driving licence", "motorbike licence"],
                 years=(1, 0.3, 3), share=0.9, start=(14, 25, 60), contests_y=1, forks=["pay"],
                 demand=dict(hours=1, money=0.15, entry=0.2, energy=0.2), window=None, upkeep=None),
            dict(say="at home in strange places", any=["second language", "navigation", "sea legs",
                                                       "diving certificate"],
                 years=(3, 1, 7), share=0.55, contests_y=1, forks=["go_on"],
                 demand=dict(hours=2, money=0.2, entry=0.1, energy=0.4), window=None, upkeep=None),
            dict(say="a life on the move", any=["seafarer's papers", "merchant seafarer", "camper van",
                                                "boat of one's own"],
                 years=(4, 2, 10), share=0.3, contests_y=2, forks=["take"],
                 demand=dict(hours=4, money=0.1, entry=0.3, energy=0.5), window=None, upkeep=None),
            dict(say="a home in more than one country", any=["immigrant", "returned migrant", "family abroad",
                                                             "permanent residence"],
                 years=(6, 2, 15), share=0.35, contests_y=1, forks=["take"],
                 demand=dict(hours=2, money=0.05, entry=0.3, energy=0.5), window=None, upkeep=None),
        ]),

    # U R (dream means U.4 R.3 G.3). New field. Estimate: expedition members usually have years of mountain, polar or
    # field experience before a first place on a team, and expeditions leave in a short yearly season; leaders a few
    # expeditions more; a first map of a place nobody has mapped (a cave system, a range's far side) is rare. Sum 21
    # years; top .9 x .25 x .3 x .15 = about 1 in 100.
    "to explore the far places": dict(
        shape="venture", face="U R", sphere="", domain="", calling=True,
        dreams=["an explorer"],
        thing="exploring", doing="exploring far places", contest="a hard crossing",
        places=["prod.wild", "learn.higher", "prot.rescue"],
        people=dict(coach="an old explorer", rival="another team after the same place", peer="the expedition team",
                    patron="a society that funds expeditions"),
        round=["the walking club's weekly meet", "a field trip with a university team",
               "a season with a mountain rescue team"],
        below="{N} draws maps of the woods behind the house and marks the parts nobody has been yet",
        tribal="to walk past the last known valley and come back with its name",
        magic="to chart the lands past the edge of the old maps, where the guild's surveyors never went",
        prep=["the outdoors", "navigation", "fitness"], meets=["competence", "meaning"],
        rungs=[
            dict(say="nights out with a map and a compass", any=["navigation", "scout or guide", "knowing the woods"],
                 years=(2, 0.5, 4), share=0.9, start=(8, 22, 40), contests_y=1, forks=["go_on"],
                 demand=dict(hours=5, money=0.03, entry=0.05, energy=0.5), window=None,
                 upkeep=dict(of="proficiency", years=5, kept_by=["time on the hills"])),
            dict(say="a place on an expedition", any=["expedition member"],
                 years=(5, 2, 10), share=0.25, contests_y=1, forks=["pay"],
                 demand=dict(hours=6, money=0.2, entry=0.3, energy=0.8),
                 window=dict(every=1, open_weeks=10, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="leading an expedition", any=["expedition leader"],
                 req="was('expedition member')", height="Known",
                 years=(6, 3, 12), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.1, entry=0.2, energy=0.8),
                 window=dict(every=1, open_weeks=10, deadline_age=None, deadline_years=None, pause_stops=False),
                 upkeep=None),
            dict(say="a place nobody had mapped, mapped", any=["known across the country"],
                 req="was('expedition leader')", height="Notable",
                 years=(8, 4, 20), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0.1, energy=0.7), window=None, upkeep=None),
        ]),
}


FIELDS_EARTH = {k: {**_FIELDS_A, **_FIELDS_B, **_FIELDS_C, **_FIELDS_D}[k] for k in (
    'to raise a family that holds together',
    'to keep the peace in the street',
    'to see justice done',
    'to keep one promise for life',
    'to build things that last',
    'to serve the public well',
    'to be the one people come to for advice',
    'to make a home that runs well',
    'to rise to the top of the firm',
    'to keep the family name high',
    'to own the roof over our heads',
    'to make the rules everyone lives by',
    'to know one thing better than anyone',
    'to master an instrument',
    'to teach well',
    'to find out what is true',
    'to be the best at what I do',
    'to marry well',
    'to keep a sharp eye on money',
    'to study the old texts',
    'to cook like nobody else',
    'to speak every language I meet',
    'to fall for a mind as quick as mine',
    'to raise children who question everything',
    'to answer to no one',
    'to be somebody in this town',
    'to win at the highest level',
    'to make money work for me',
    'to live by my own rules',
    'to make it big, and fast',
    'to never be pushed around again',
    'to chase the next thrill',
    'to outlast them all',
    'to keep the family land',
    'to know every root and mushroom',
    'to run the family business',
    'to see the world',
    'to love with everything',
    'to stand up for the underdog',
    'to feel something greater in the music',
    'to live wild and free outdoors',
    'to raise a big, loud family',
    'to dance',
    'to save the wild places',
    'to be there when it counts',
    'to fight for what is right',
    'to throw the parties the town remembers',
    'to protect the ones I love',
    'to work the land',
    "to keep the family's ways",
    'to grow old among many grandchildren',
    'to stay strong and well for life',
    'to care for those who cannot manage alone',
    'to feed the street from my garden',
    'to belong to a congregation for life',
    'to make a home everyone is welcome in',
    'to grow the perfect garden',
    'to work with animals',
    'to know where we come from',
    'to live in balance',
    'to master chess',
    'to play football at the top',
    'to race cars',
    'to fight in the ring',
    'to earn a black belt',
    'to make video games',
    'to play in a band',
    'to be famous',
    'to take in a child who has no one',
    'to run an animal sanctuary',
    'to breed champion horses',
    'to explore the far places',
)}


# The land's 30 ways as aims fields of the land shape, and their 90 ladder titles (Library, v25 prep, draft 10-23).
#
# A plain data file: nothing here runs. The Library pours it in after Friday 10-23 21:00.
#
# Sources:
# - chroma-world/spheres/data/land.json `uses.ways.list` (key, lead, standing_in, ladder, ladder_years,
#   ladder_titles) and `uses.ways.bridges`; spec chroma-world/spheres/land-moments-v1.md ("Ways to use the land").
# - The field format: chroma-engine/notes/v25/aims-shape.md sections 3, 7 and 8 (chess, key for key) and
#   other-shapes.md section 4; the writer brief library/briefs/FIELDS.md; V25-DECISIONS.md ("Aims").
#
# How the fields are read from land.json (nothing in land.json is changed):
# - `face` is the way's `lead` written as v1 writes faces ("WG" -> "W G"), first colour first.
# - `sphere` is the way's `standing_in`.
# - Each rung's `say` is the ladder step's words without the years in brackets; its `any` is the step's
#   `ladder_titles` name (or, in five places, an existing catalogue title, noted on the rung); its `years` is the
#   step's `ladder_years` unchanged, as (median, low, high).
# - `dreams` is empty: every dream in dreams.py that fits a land way already turns into a v1 aim or a new field.
#   A way is opened by a moment's `opens`, by the people met, or by the player's aim (land.json).
# - `domain`: "career" for the ways that earn a living, "community" for the civic ones, "" for the rest.
#   `calling`: True for the six ways that grow into a life's work out of care for the land itself (soil, wild land,
#   river, records, wood, teaching outdoors); False for pastimes, trades and businesses.
# - `req` names catalogue perks and titles that stand for the way's `needs` where those are hard (money, land,
#   a permit, clearance to work with children). Soft needs (a course, a kit, a field guide) are left to the rung.
# - `height`: "Known" where the top rung is standing across the town ("the town's ..."), "" for a club's or a
#   society's own seat. No land rung is Notable or Historic: the land shape's tops are local.
# - No rung comes with time alone (`time` is never set).
#
# Clocks and shares:
# - All `years` are land.json's (taken there from the ladder's own text). All `share` values are estimates:
#   the share of those who keep at the way who reach that rung from the one below; rung 1 is about .9 (lower,
#   .8 to .85, where the first step needs money or land); the top is rare (.08 to .2), since there is one chair,
#   one recorder, one commodore for many members. Multiplied, about 1 to 4 in 100 who start reach the top.
# - `start` (from, best_to, late_from) is an estimate from who takes the way up (children keep hens and fish;
#   land dealing and building wait on savings); after late_from the odds fall, never shut.
# - `contests_y` is how often a contest moment comes at that rung: often for matches and markets (4 to 8),
#   once or twice a year for a show, a count or a hearing, 0 where the first rung has none.
#
# Demands, windows and upkeep (aims-shape.md section 3, Engine update 10-23); all estimates:
# - `demand` = dict(hours, money, entry, energy) on every rung, at steady intensity. Rung 1's hours are the way's
#   `hours` from land.json; later rungs add the hours the step asks (a stall becomes a shop, a member becomes a chair).
#   money (a year) and entry (once) are outlay only, as shares of a year's free money (0 to 1; 1.0 means at least a
#   year's, as for a field, a build or a boat); what a way earns comes from its land.json `effect`, not from here.
#   energy is how tiring the step is (0 to 1): high for the field and water trades and for matches, low for counts.
# - `window` only where the timing is outside the person: a yearly show or count, a season (cutting, hunting, fishing,
#   sailing, summer trade), a course run once a year, a club's yearly meeting that elects its chair, a selection for
#   the first team with an age limit. Every window recurs (`every`=1); a missed one waits a year. A rung with no
#   `window` key has none (None).
# - `upkeep` only where something really lapses: a licence or permit renewed each year (rod licence, hunting permit,
#   fishing and trading licences), safety training renewed (flood warden, swim lead, forest school, instructor,
#   chainsaw ticket), access lost through non-use (an allotment plot not worked is taken back; a water share unused
#   for years can be lost), and match or race fitness. The title itself is kept for life. No `upkeep` key means None.
# - Field `prep` tags (shared preparation, counted once across two aims): growing, animals, dealing, fitness,
#   organising, woodcraft, naturalist, teaching, making, the river, boats, the shore. Field `meets`: the needs the
#   practice restores, of belonging, meaning and competence.
#
# Ways in (V25-DECISIONS, "Aims"): every field names at least three ways in through `places`, `people` and
# `round`, and each `round` holds one that recurs (a weekly night, a monthly work day, a yearly show).
#
# Titles (LAND_TITLES, after the fields): 85 new status titles, one per ladder step, plus 5 steps that reuse a
# catalogue title (comments in the list). `ways` is the way's lead, as asked; note that the v24 catalogue's status
# titles carry ways="" (out of the colour balance), so the Library decides on pouring which to keep. `share` there
# is the share of all people who ever hold the title (estimate). `doors` names what the title opens: a setting, a
# person, a seat, or a bridge's opening from land.json `bridges` (a bridge needs both ways held).
#
# Flags for the pour:
# - land.json's wood_guardian step 3 reads "the town's voice for green land" and its title is "the town's green
#   voice": a colour word. The rung's `say` here drops it ("the town's voice for its land"); the title keeps
#   land.json's name so the keys match, and land.json's owner may rename it ("the town's land voice").
#   Two bridges' openings also carry the word ("the green street", "the council's green board"); the doors here
#   say them without it.
# - "stage manager" (field_events step 2) is land.json's name and already a catalogue career (theatre, W U);
#   it is reused, not written twice.
#
# Rules kept: no colour words in the text, no game terms, no year, brand, country, currency, real place, real
# person, real faith or real event; nothing graphic; children only in safe roles.

FIELDS_EARTH_LAND = {

    # ------------------------------------------------------------------ the field (ten ways)

    # clocks: land.json ladder_years; shares estimate (about 1 allotment society chair per 80 to 150 plots)
    "allotment": dict(
        shape="land", face="W G", sphere="gather", domain="community", calling=False, dreams=[],
        thing="the allotment", doing="growing on the allotment", contest="the society's summer show",
        places=["prod.land", "gather.circle", "gather.hall"],
        people=dict(coach="an old hand on the next plot", rival="the grower who always takes the onion prize",
                    peer="the Saturday-morning plot holders", patron="the society's secretary"),
        round=["a half plot shared with a neighbour while the list moves", "the community garden's weekly work morning",
               "a corner of a friend's garden"],
        below="{N} checks the weather twice before bed, thinking of the beans",
        prep=["growing"], meets=["belonging", "competence"],
        tribal="to keep a family's patch in the clan's tilled ground, and bring the best of it to the harvest gathering",
        magic="to hold a bed in the guild's walled garden, where the members swap seeds at the turn of each season",
        rungs=[
            dict(say="a plot", demand=dict(hours=4, money=.05, entry=.05, energy=.3),
                 window=dict(every=1, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),  # plots re-let at the yearly tenancy round
                 upkeep=dict(of="access", years=1, kept_by=["growing"]),  # a plot left unworked is taken back
                 any=["plot holder"],
                 years=(2.0, 1, 3), share=0.9, start=(18, 40, 70), contests_y=0, forks=["round"]),
            dict(say="prizes and seed swaps", demand=dict(hours=6, money=.08, entry=.1, energy=.35),
                 window=dict(every=1, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),  # the society's summer show
                 any=["prize grower"],
                 years=(4.5, 3, 6), share=0.55, contests_y=2, forks=["pay"]),
            dict(say="chairs the society", demand=dict(hours=8, money=.03, entry=0, energy=.3),
                 window=dict(every=1, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),  # the yearly meeting elects the chair
                 any=["allotment society chair"],
                 years=(13.0, 10, 20), share=0.12, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (most small growers stop within five years)
    "market_garden": dict(
        shape="land", face="B G", sphere="prod", domain="career", calling=False, dreams=[],
        thing="the market garden", doing="growing to sell", contest="a busy market day",
        places=["prod.land", "comm.market"],
        people=dict(coach="a grower who has done it for thirty years", rival="the stall across the aisle",
                    peer="the other growers at the market", patron="a restaurant that buys by the crate"),
        round=["a field rented from a farmer who has slowed down", "the weekly growers' market",
               "selling by the box to the street"],
        below="{N} is up before the light, washing roots in the yard with cold hands",
        prep=["growing", "trading"], meets=["competence", "meaning"],
        tribal="to grow more than the family eats and trade the rest at the gathering",
        magic="to grow the herbs and roots the tower kitchens send for",
        rungs=[
            dict(say="a stall", demand=dict(hours=20, money=.3, entry=.5, energy=.6),
                 any=["market stallholder"],
                 req="has('plot of land') | has('savings') | was('farmer') | has('inheritance')",
                 years=(1.5, 1, 2), share=0.85, start=(18, 35, 55), contests_y=4, forks=["pay"]),
            dict(say="regular buyers", demand=dict(hours=30, money=.3, entry=.3, energy=.7),
                 any=["market gardener"],
                 years=(4.0, 3, 5), share=0.5, contests_y=6, forks=["go_on"]),
            dict(say="a farm shop", demand=dict(hours=40, money=.4, entry=.8, energy=.7),
                 any=["farm shop owner"],
                 years=(10.4, 8, 16), share=0.25, contests_y=4, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (many first-year keepers lose a colony and stop)
    "beekeeping": dict(
        shape="land", face="G U", sphere="prod", domain="", calling=False, dreams=[],
        thing="bees", doing="keeping bees", contest="the honey show",
        places=["prod.land", "gather.hall"],
        people=dict(coach="the club's old beekeeper", rival="the member whose honey always wins",
                    peer="the beekeepers' club", patron="a farmer who wants hives in the orchard"),
        round=["the club's teaching hives on a Sunday morning", "a swarm collected from a neighbour's hedge",
               "a share in a friend's hives"],
        below="{N} sits by the hives in the evening and listens to the hum change",
        prep=["naturalist"], meets=["competence", "meaning"],
        tribal="to find the wild hives and take the honey without losing the bees",
        magic="to keep the tower's bees, whose wax the scribes and the candle-makers prize",
        rungs=[
            dict(say="first hive", demand=dict(hours=2, money=.05, entry=.25, energy=.2),
                 window=dict(every=1, open_weeks=10, deadline_age=None, deadline_years=None, pause_stops=False),  # colonies and the course start in spring
                 any=["beekeeper"],
                 years=(1, 1, 2), share=0.9, start=(14, 45, 70), contests_y=0, forks=["pay"]),
            dict(say="own honey", demand=dict(hours=3, money=.06, entry=.1, energy=.25),
                 window=dict(every=1, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),  # the late-summer honey harvest
                 any=["honey maker"],
                 years=(3.0, 2, 4), share=0.7, contests_y=1, forks=["go_on"]),
            dict(say="teaches the course", demand=dict(hours=4, money=.03, entry=0, energy=.25),
                 any=["beekeeping teacher"],
                 years=(10.4, 8, 16), share=0.2, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (show judges are few and chosen by the show)
    "keeping_animals": dict(
        shape="land", face="G W", sphere="prod", domain="", calling=False, dreams=[],
        thing="the animals", doing="keeping hens, goats and sheep", contest="the agricultural show",
        places=["prod.land", "gather.great"],
        people=dict(coach="the vet", rival="a breeder who wins every class",
                    peer="the neighbours who keep animals too", patron="a farmer with a spare field"),
        round=["a corner of a neighbour's field", "the poultry club's monthly meeting", "a share in a friend's flock"],
        below="{N} goes out in the dark with a torch to count the hens in",
        prep=["animals", "growing"], meets=["competence", "belonging"],
        tribal="to keep the clan's goats and sheep through the lean months",
        magic="to raise the tower's beasts, the goats that climb where no path goes",
        rungs=[
            dict(say="a few hens", demand=dict(hours=6, money=.06, entry=.1, energy=.3),
                 any=["hen keeper"],
                 years=(1, 1, 2), share=0.9, start=(8, 40, 65), contests_y=0, forks=["go_on"]),
            dict(say="a flock", demand=dict(hours=10, money=.15, entry=.3, energy=.45),
                 any=["smallholder"],
                 req="has('plot of land') | was('farmer') | has('inheritance')",
                 years=(4.5, 3, 6), share=0.5, contests_y=1, forks=["pay"]),
            dict(say="judges at the show", demand=dict(hours=6, money=.05, entry=0, energy=.3),
                 window=dict(every=1, open_weeks=1, deadline_age=None, deadline_years=None, pause_stops=False),  # the show's one week
                 any=["show judge"],
                 years=(13.0, 10, 20), share=0.12, contests_y=2, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (the soil takes years to turn; many go back to the old way)
    "regen_farming": dict(
        shape="land", face="U G", sphere="learn", domain="career", calling=True, dreams=[],
        thing="the soil", doing="farming to rebuild the soil", contest="the year's yield count",
        places=["prod.land", "learn.higher"],
        people=dict(coach="an old farmer who stopped ploughing years ago",
                    rival="the neighbour who says it will never pay", peer="the farmers' discussion group",
                    patron="the college's field researcher"),
        round=["the farmers' monthly field walk", "a trial strip on a borrowed field", "the college's short course"],
        below="{N} kneels in the field with a spade and counts the worms in a square of soil",
        prep=["growing"], meets=["meaning", "competence"],
        tribal="to learn which ground must rest and which can grow, and move the planting so the earth stays rich",
        magic="to work the tower's tired fields back to life, as the oldest books say they once were",
        rungs=[
            dict(say="a trial field", demand=dict(hours=30, money=.3, entry=.4, energy=.7),
                 any=["trial farmer"],
                 req="was('farmer') | has('plot of land') | has('inheritance')",
                 years=(2.5, 2, 3), share=0.85, start=(20, 40, 55), contests_y=1, forks=["pay"]),
            dict(say="yields hold", demand=dict(hours=35, money=.3, entry=.3, energy=.7),
                 window=dict(every=1, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),  # yields are shown at harvest
                 any=["soil farmer"],
                 years=(6.5, 5, 8), share=0.5, contests_y=1, forks=["go_on"]),
            dict(say="others copy it", demand=dict(hours=35, money=.25, entry=.1, energy=.6),
                 any=["model farmer"], height="Known",
                 years=(13.0, 10, 20), share=0.2, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (one or two big landowners a town)
    "land_dealing": dict(
        shape="land", face="B U", sphere="comm", domain="career", calling=False, dreams=[],
        thing="land", doing="buying and renting out land", contest="a land auction",
        places=["comm.credit", "rule.counsel", "prod.land"],
        people=dict(coach="an old land agent", rival="a buyer from out of town",
                    peer="the landowners at the auction rooms", patron="the bank's lending manager"),
        round=["the monthly land auctions", "a field bought with a partner", "renting land in before buying it"],
        below="{N} drives the back roads and notes every field with a sign at the gate",
        prep=["trading"], meets=["competence"],
        tribal="to hold the best grazing and trade its use to other families for a share of their herds",
        magic="to buy up charter lands from failing houses and let them to the guilds",
        rungs=[
            dict(say="a first field", demand=dict(hours=3, money=.1, entry=1.0, energy=.2),
                 any=["landholder"],
                 req="has('savings') | has('inheritance') | has('family business')",
                 years=(2, 0, 5), share=0.8, start=(25, 50, 65), contests_y=1, forks=["pay"]),
            dict(say="rents", demand=dict(hours=4, money=.1, entry=.8, energy=.2),
                 any=["landlord of fields"],
                 years=(4.0, 3, 5), share=0.5, contests_y=1, forks=["go_on"]),
            dict(say="the town's big landowner", demand=dict(hours=8, money=.1, entry=1.0, energy=.3),
                 any=["the town's big landowner"], height="Known",
                 years=(19.5, 15, 30), share=0.08, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (most self-builders build once)
    "building_on_land": dict(
        shape="land", face="B R", sphere="comm", domain="career", calling=False, dreams=[],
        thing="building", doing="building on land", contest="a planning hearing",
        places=["prod.land", "rule.counsel", "comm.credit"],
        people=dict(coach="a builder who has done self-builds", rival="a bigger firm after the same plot",
                    peer="the self-builders' group", patron="a lender who backs small schemes"),
        round=["the self-builders' monthly meeting", "a plot shared with another family",
               "an old barn to convert instead of a field"],
        below="{N} sketches floor plans on the back of every envelope in the house",
        prep=["trading"], meets=["competence", "meaning"],
        tribal="to raise the clan's new shelters where the ground is dry and the wind is kind",
        magic="to raise new halls on the old charter lands, if the council of the guilds allows it",
        rungs=[
            dict(say="a self-build", demand=dict(hours=10, money=.2, entry=1.0, energy=.6),
                 any=["self-builder"],
                 req="has('plot of land') | has('savings') | has('inheritance')",
                 years=(3.0, 2, 4), share=0.8, start=(25, 45, 60), contests_y=1, forks=["pay"]),
            dict(say="a small scheme", demand=dict(hours=20, money=.2, entry=1.0, energy=.6),
                 any=["small builder"],
                 years=(7.5, 5, 10), share=0.35, contests_y=1, forks=["take"]),
            dict(say="a developer", demand=dict(hours=40, money=.2, entry=1.0, energy=.7),
                 any=["developer"], height="Known",
                 years=(19.5, 15, 30), share=0.15, contests_y=2, forks=["go_on"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a first team holds about fifteen of a club's many players)
    "field_sports": dict(
        shape="land", face="R B", sphere="gather", domain="", calling=False, dreams=[],
        thing="the club's game", doing="playing for the town's club", contest="a league match",
        places=["gather.games", "gather.hall"],
        people=dict(coach="the club's coach", rival="a player from the next town's club",
                    peer="the club's regulars", patron="the local firm that pays for the kit"),
        round=["the Tuesday training night", "the club across town", "the veterans' side"],
        below="{N} still has mud on the boots from Saturday and is already thinking about next Saturday",
        prep=["fitness"], meets=["belonging", "competence"],
        tribal="to win the throwing and running games at the gathering of the clans",
        magic="to play for the town in the field games the guilds wager on",
        rungs=[
            dict(say="plays", demand=dict(hours=5, money=.05, entry=.03, energy=.6),
                 window=dict(every=1, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),  # signing on before the season
                 any=["club player"],
                 years=(2, 0, 5), share=0.9, start=(6, 16, 30), contests_y=6, forks=["go_on"]),
            dict(say="the first team", demand=dict(hours=7, money=.06, entry=.03, energy=.75),
                 window=dict(every=1, open_weeks=4, deadline_age=40, deadline_years=None, pause_stops=False),  # selection at the season's start
                 upkeep=dict(of="proficiency", years=1, kept_by=["training", "matches"]),  # match fitness
                 any=["first-team player"],
                 years=(5.5, 3, 8), share=0.4, contests_y=8, forks=["take"]),
            # land.json's "club captain" reuses the catalogue's [team captain] (community, R B, "picked by the coach
            # or voted in by the team")
            dict(say="captain or coach", demand=dict(hours=8, money=.05, entry=.05, energy=.6),
                 any=["team captain"],
                 years=(13.0, 10, 20), share=0.15, contests_y=8, forks=["go_on"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a festival has one director and dozens of volunteers)
    "field_events": dict(
        shape="land", face="R B", sphere="arts", domain="community", calling=False, dreams=[],
        thing="the fair", doing="putting on fairs and festivals", contest="the festival weekend",
        places=["gather.great", "arts.stage", "rule.counsel"],
        people=dict(coach="the committee's old hand", rival="the promoter who wants the same weekend",
                    peer="the committee and the volunteers", patron="a trader who sponsors the main stage"),
        round=["the committee's monthly meeting", "the fair in the next valley", "a street party to run first"],
        below="{N} keeps a notebook of acts, stalls and who owes whom a favour",
        prep=["organising"], meets=["belonging", "meaning"],
        tribal="to call the clans to the summer gathering and see the feasting go well",
        magic="to stage the midsummer fair where the guilds show their wonders",
        rungs=[
            dict(say="helps out", demand=dict(hours=6, money=.02, entry=0, energy=.5),
                 window=dict(every=1, open_weeks=4, deadline_age=None, deadline_years=None, pause_stops=False),  # the festival's weeks
                 any=["fair volunteer"],
                 years=(1, 1, 2), share=0.9, start=(14, 35, 65), contests_y=1, forks=["go_on"]),
            # land.json's "stage manager" is already a catalogue career (W U, theatre): reused, not written twice
            dict(say="runs a stage", demand=dict(hours=8, money=.03, entry=.02, energy=.6),
                 any=["stage manager"],
                 years=(4.0, 3, 5), share=0.45, contests_y=2, forks=["pay"]),
            dict(say="the festival is theirs", demand=dict(hours=12, money=.05, entry=.1, energy=.7),
                 any=["festival director"], height="Known",
                 years=(10.4, 8, 16), share=0.15, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (verges need the council's say; few lead the whole town's)
    "wildflower_meadow": dict(
        shape="land", face="G R", sphere="gather", domain="community", calling=False, dreams=[],
        thing="the meadow", doing="turning grass into meadow", contest="the summer flower count",
        places=["prod.wild", "gather.circle", "rule.counsel"],
        people=dict(coach="a botanist from the bee people", rival="a neighbour who likes a short lawn",
                    peer="the neighbours who sow the verges", patron="a councillor who will sign off the verges"),
        round=["the autumn seed-sowing day", "a corner of the school field", "the edge of the park"],
        below="{N} stops mowing one corner of the garden and watches what comes up",
        prep=["growing", "naturalist"], meets=["meaning", "belonging"],
        tribal="to rest the old meadow in turn so the flowers and the grazing both come back",
        magic="to sow the meadow whose flowers the herb-wives say still remember the old spells",
        rungs=[
            dict(say="a corner", demand=dict(hours=2, money=.02, entry=.03, energy=.2),
                 window=dict(every=1, open_weeks=8, deadline_age=None, deadline_years=None, pause_stops=False),  # autumn sowing
                 any=["meadow maker"],
                 years=(1, 1, 2), share=0.9, start=(10, 50, 75), contests_y=0, forks=["go_on"]),
            dict(say="the street's verges", demand=dict(hours=3, money=.02, entry=.03, energy=.25),
                 any=["verge keeper"],
                 years=(4.0, 3, 5), share=0.45, contests_y=1, forks=["round"]),
            dict(say="the town's meadows", demand=dict(hours=5, money=.02, entry=0, energy=.3),
                 any=["town meadow lead"], height="Known",
                 years=(10.4, 8, 16), share=0.15, contests_y=1, forks=["take"]),
        ]),

    # ------------------------------------------------------------------ the wood (ten ways)

    # clocks: land.json ladder_years; shares estimate (about half of new trail runners enter a race)
    "trail_running": dict(
        shape="land", face="R G", sphere="gather", domain="", calling=False, dreams=[],
        thing="the trails", doing="running and riding the wood's trails", contest="a trail race",
        places=["prod.wild", "gather.games"],
        people=dict(coach="the club's oldest runner", rival="a runner who is always ten seconds ahead",
                    peer="the Sunday trail group", patron="an outdoor shop that backs the club"),
        round=["the club's weekly night run", "the hill trails over the ridge", "a riding stable's rides out"],
        below="{N} knows every root on the long loop and runs it in the dark",
        prep=["fitness"], meets=["competence", "meaning"],
        tribal="to run the hunting trails faster than any of the young hunters",
        magic="to ride the old forest paths where the towers' messengers run",
        rungs=[
            dict(say="own routes", demand=dict(hours=5, money=.04, entry=.05, energy=.6),
                 any=["trail runner"],
                 years=(1, 1, 2), share=0.9, start=(12, 30, 50), contests_y=0, forks=["go_on"]),
            dict(say="races", demand=dict(hours=7, money=.08, entry=.05, energy=.75),
                 upkeep=dict(of="proficiency", years=1, kept_by=["running"]),  # race fitness
                 any=["trail racer"],
                 years=(3.5, 2, 5), share=0.55, contests_y=5, forks=["pay"]),
            dict(say="builds the trails", demand=dict(hours=6, money=.04, entry=.05, energy=.6),
                 any=["trail builder"],
                 years=(10.4, 8, 16), share=0.2, contests_y=2, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a wood is managed by one hand at a time)
    "timber": dict(
        shape="land", face="W B", sphere="prod", domain="career", calling=False, dreams=[],
        thing="the wood", doing="coppicing and cutting firewood", contest="the winter's orders",
        places=["prod.wild", "prod.craft", "comm.market"],
        people=dict(coach="an old woodsman who knows the rota", rival="a contractor who clears whole stands",
                    peer="the woodsmen at the timber yard", patron="the wood's owner"),
        round=["the coppice group's winter work days", "a neighbour's overgrown hedge line",
               "a licence on the council's wood"],
        below="{N} stacks the log pile in the yard by the winter each row was cut",
        prep=["woodcraft"], meets=["competence", "meaning"],
        tribal="to cut the clan's firewood by the old turns of the wood, so the trees grow back",
        magic="to cut the tower's wood by the old rota the foresters' guild keeps in its book",
        rungs=[
            dict(say="firewood for the house", demand=dict(hours=12, money=.05, entry=.25, energy=.7),
                 window=dict(every=1, open_weeks=16, deadline_age=None, deadline_years=None, pause_stops=False),  # the winter cutting season
                 any=["woodcutter"],
                 years=(1, 1, 2), share=0.9, start=(16, 40, 60), contests_y=0, forks=["pay"]),
            dict(say="sells cords", demand=dict(hours=15, money=.1, entry=.2, energy=.75),
                 upkeep=dict(of="credential", years=5, kept_by=["cutting"]),  # the saw ticket's refresher
                 any=["firewood seller"],
                 years=(4.0, 3, 5), share=0.5, contests_y=1, forks=["go_on"]),
            dict(say="manages the wood", demand=dict(hours=20, money=.08, entry=.1, energy=.7),
                 any=["woodland manager"],
                 years=(13.0, 10, 20), share=0.2, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a ranger post per wood or estate)
    "deer_management": dict(
        shape="land", face="W R", sphere="prot", domain="", calling=False, dreams=[],
        thing="the hunt", doing="hunting by season and permit", contest="the season's count",
        places=["prod.wild", "gather.hall"],
        people=dict(coach="the club's senior stalker", rival="a hunter who takes more than the plan allows",
                    peer="the hunting club", patron="a landowner who needs the deer kept down"),
        round=["the club's monthly meeting and range day", "a permit on an estate across the valley",
               "a plan shared with the neighbouring landowners"],
        below="{N} sits still at the edge of the wood before dawn, long before anything moves",
        prep=["woodcraft", "fitness"], meets=["belonging", "competence"],
        tribal="to hunt by the clan's rules: the right season, the right animal, a fair share for every fire",
        magic="to hunt the old forest by the lord's warrant and the wood's old rules",
        rungs=[
            dict(say="goes out with the club", demand=dict(hours=4, money=.08, entry=.2, energy=.5),
                 window=dict(every=1, open_weeks=20, deadline_age=None, deadline_years=None, pause_stops=False),  # the open season
                 any=["club stalker"],
                 years=(1.5, 1, 2), share=0.9, start=(16, 35, 55), contests_y=0, forks=["go_on"]),
            dict(say="own permit", demand=dict(hours=5, money=.1, entry=.15, energy=.5),
                 window=dict(every=1, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),  # permits are granted before each season
                 upkeep=dict(of="credential", years=1, kept_by=["hunting"]),  # the permit is renewed each season
                 any=["permit holder"], req="has('hunting licence')",
                 years=(4.0, 3, 5), share=0.55, contests_y=1, forks=["pay"]),
            dict(say="the wood's ranger", demand=dict(hours=10, money=.05, entry=.05, energy=.55),
                 any=["wood ranger"],
                 years=(13.0, 10, 20), share=0.15, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (guiding needs sure knowledge of what is safe)
    "forage_guide": dict(
        shape="land", face="G B", sphere="comm", domain="", calling=False, dreams=[],
        thing="foraging", doing="foraging and guiding walks", contest="the autumn foray",
        places=["prod.wild", "comm.market"],
        people=dict(coach="an old forager who knows what is safe", rival="a guide who takes too much",
                    peer="the cooks and walkers on the walks", patron="a restaurant cook who buys the basket"),
        round=["the society's monthly foray", "the hedgerows along the old rail line", "the shore at low tide"],
        below="{N} keeps a book of every patch, with the month it is ready",
        prep=["woodcraft", "naturalist"], meets=["competence", "meaning"],
        tribal="to lead the gatherers to the good patches each season, and teach which ones are safe",
        magic="to gather the old forest's herbs and caps for the potion-makers, and know which ones are safe",
        rungs=[
            dict(say="own baskets", demand=dict(hours=3, money=.01, entry=.02, energy=.3),
                 any=["forager"],
                 years=(1.5, 1, 2), share=0.9, start=(14, 40, 65), contests_y=0, forks=["go_on"]),
            dict(say="leads walks", demand=dict(hours=5, money=.03, entry=.1, energy=.4),
                 any=["foraging guide"], req="has('knowing the woods')",
                 years=(4.0, 3, 5), share=0.45, contests_y=1, forks=["take"]),
            dict(say="the restaurants' supplier", demand=dict(hours=10, money=.05, entry=.05, energy=.5),
                 any=["wild food supplier"],
                 years=(10.4, 8, 16), share=0.2, contests_y=1, forks=["go_on"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (leader training is a year or two; one head per town)
    "forest_school": dict(
        shape="land", face="U W", sphere="learn", domain="career", calling=True, dreams=[],
        thing="the forest school", doing="teaching children outdoors", contest="an inspection",
        places=["prod.wild", "learn.higher", "gather.circle"],
        people=dict(coach="the forest school leader who trained them",
                    rival="a head teacher who wants the children indoors",
                    peer="the teachers and parents who come out", patron="a school that pays for a term"),
        round=["the weekly session in the school's wood", "a holiday club in the park",
               "the training course run each spring"],
        below="{N} packs the tarp, the kettle and the spare boots, and checks the wind",
        prep=["teaching", "woodcraft"], meets=["meaning", "belonging"],
        tribal="to take the clan's children into the woods and teach them the paths, the plants and the fire",
        magic="to teach the tower's young apprentices out under the old trees, where the lessons stick",
        rungs=[
            dict(say="helps a session", demand=dict(hours=15, money=.02, entry=.05, energy=.5),
                 upkeep=dict(of="credential", years=3, kept_by=["working with children"]),  # the clearance is renewed
                 any=["forest school helper"], req="has('cleared to work with children')",
                 years=(1, 1, 2), share=0.9, start=(18, 35, 55), contests_y=0, forks=["go_on"]),
            dict(say="runs a group", demand=dict(hours=20, money=.05, entry=.3, energy=.6),
                 window=dict(every=1, open_weeks=6, deadline_age=None, deadline_years=None, pause_stops=False),  # the leader course runs each spring
                 upkeep=dict(of="credential", years=3, kept_by=["teaching outdoors"]),  # outdoor first aid renewed
                 any=["forest school leader"],
                 years=(4.0, 3, 5), share=0.5, contests_y=1, forks=["pay"]),
            dict(say="the town's forest school", demand=dict(hours=30, money=.05, entry=.1, energy=.6),
                 any=["forest school head"], height="Known",
                 years=(10.4, 8, 16), share=0.2, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (one recorder per group of animals in a whole county)
    "wildlife_survey": dict(
        shape="land", face="U W", sphere="learn", domain="", calling=True, dreams=[],
        thing="the counts", doing="counting wildlife for the record", contest="the yearly bird count",
        places=["prod.wild", "learn.keeping", "gather.hall"],
        people=dict(coach="the society's old recorder", rival="a counter who disputes every sighting",
                    peer="the naturalists' society", patron="the trust that needs the records"),
        round=["the society's monthly field meeting", "a square in the next valley", "the moth trap in the back garden"],
        below="{N} writes the date, the weather and every bird in a notebook before breakfast",
        prep=["naturalist"], meets=["competence", "meaning"],
        tribal="to know which birds come back with which season, and read the year by them",
        magic="to keep the tower's book of every creature in the wood, as the old masters did",
        rungs=[
            # land.json's "wildlife counter" reuses the catalogue's [community observer] (community, G W:
            # "volunteers wanted to count what lives here", kept up for years)
            dict(say="first counts", demand=dict(hours=3, money=.02, entry=.05, energy=.2),
                 window=dict(every=1, open_weeks=12, deadline_age=None, deadline_years=None, pause_stops=False),  # the breeding-season counts
                 any=["community observer"],
                 years=(1, 1, 2), share=0.9, start=(12, 50, 75), contests_y=1, forks=["go_on"]),
            dict(say="a square of their own", demand=dict(hours=4, money=.03, entry=.05, energy=.3),
                 upkeep=dict(of="proficiency", years=3, kept_by=["counting"]),  # calls and marks are forgotten unused
                 any=["survey square holder"],
                 years=(4.0, 3, 5), share=0.55, contests_y=2, forks=["round"]),
            dict(say="the county's recorder", demand=dict(hours=6, money=.02, entry=0, energy=.25),
                 any=["county recorder"], height="Known",
                 years=(13.0, 10, 20), share=0.1, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (cabins need a lender and a licence)
    "campsite": dict(
        shape="land", face="B R", sphere="comm", domain="career", calling=False, dreams=[],
        thing="the campsite", doing="running a campsite in the wood", contest="the summer season",
        places=["prod.wild", "comm.shop"],
        people=dict(coach="a site owner who has done it for years", rival="the big holiday park up the road",
                    peer="the visitors who come back every summer", patron="a lender who backs the cabins"),
        round=["a field rented each summer from a farmer", "the yearly holiday-trade fair", "pitches on a friend's land"],
        below="{N} walks the pitches at dusk and counts the tents and the campfires",
        prep=["trading"], meets=["competence"],
        tribal="to keep the camping ground where the travelling families stop, and have a share of what they bring",
        magic="to keep the waystation in the wood where travellers to the towers rest",
        rungs=[
            dict(say="a field of tents", demand=dict(hours=15, money=.2, entry=.8, energy=.5),
                 window=dict(every=1, open_weeks=16, deadline_age=None, deadline_years=None, pause_stops=False),  # the summer season
                 any=["campsite keeper"],
                 req="has('plot of land') | has('savings') | has('inheritance') | has('family business')",
                 years=(2.5, 2, 3), share=0.8, start=(25, 45, 60), contests_y=1, forks=["go_on"]),
            dict(say="cabins", demand=dict(hours=25, money=.3, entry=1.0, energy=.6),
                 any=["cabin host"],
                 years=(6.5, 5, 8), share=0.4, contests_y=1, forks=["pay"]),
            dict(say="the outdoor centre", demand=dict(hours=40, money=.3, entry=1.0, energy=.7),
                 any=["outdoor centre owner"],
                 years=(13.0, 10, 20), share=0.15, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (few carvers take apprentices)
    "wood_crafts": dict(
        shape="land", face="U B", sphere="arts", domain="", calling=True, dreams=[],
        thing="wood", doing="carving and working wood", contest="the craft fair",
        places=["arts.craft", "prod.wild", "comm.market"],
        people=dict(coach="an old carver with a pole lathe", rival="the maker on the next stall",
                    peer="the carving group", patron="a buyer who orders a set of chairs"),
        round=["the carving group's weekly evening", "a course at a woodland workshop", "a corner of a friend's barn"],
        below="{N} has shavings in every pocket and a half-carved spoon by the bed",
        prep=["the workshop", "woodcraft"], meets=["competence", "meaning"],
        tribal="to carve the clan's bowls, handles and spear shafts so they last a lifetime",
        magic="to carve staves and wands from the old wood's fallen limbs for the guild's masters",
        rungs=[
            dict(say="spoons", demand=dict(hours=5, money=.03, entry=.1, energy=.3),
                 any=["spoon carver"],
                 years=(1, 1, 2), share=0.9, start=(10, 40, 65), contests_y=0, forks=["pay"]),
            # land.json's "craft fair maker" reuses the catalogue's [craft maker] (career, G U: "starts selling
            # what they make at fairs and markets")
            dict(say="sells at the fair", demand=dict(hours=8, money=.06, entry=.1, energy=.35),
                 any=["craft maker"],
                 years=(4.0, 3, 5), share=0.45, contests_y=3, forks=["go_on"]),
            # land.json's "master woodworker" reuses the catalogue's [master craftsperson] (career, G: "years as a
            # [craft maker], a waiting list and an apprentice of their own")
            dict(say="a workshop and apprentices", demand=dict(hours=20, money=.1, entry=.4, energy=.45),
                 any=["master craftsperson"],
                 years=(13.0, 10, 20), share=0.12, contests_y=2, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (most friends of a wood stay members; few lead)
    "wood_guardian": dict(
        shape="land", face="R W", sphere="rule", domain="community", calling=False, dreams=[],
        thing="the wood", doing="watching over the wood", contest="a planning hearing",
        places=["prod.wild", "rule.voice", "rule.counsel"],
        people=dict(coach="the friends' long-serving secretary", rival="a developer's planning agent",
                    peer="the friends of the wood", patron="a councillor who listens"),
        round=["the friends' monthly walk and meeting", "a written objection when the meeting is closed",
               "a petition stall at the market"],
        below="{N} walks the wood's edge every week and notes every new survey peg",
        prep=["organising"], meets=["meaning", "belonging"],
        tribal="to stand for the clan's wood when another band comes to cut it",
        magic="to speak for the old wood at the guild council when the axes are sent for",
        rungs=[
            dict(say="joins the friends", demand=dict(hours=3, money=.01, entry=0, energy=.25),
                 any=["friend of the wood"],
                 years=(1, 1, 2), share=0.9, start=(14, 45, 70), contests_y=1, forks=["go_on"]),
            dict(say="leads a campaign", demand=dict(hours=6, money=.03, entry=0, energy=.5),
                 any=["wood campaigner"],
                 years=(4.0, 3, 5), share=0.4, contests_y=2, forks=["pay"]),
            # land.json's step reads "the town's voice for green land" and its title "the town's green voice":
            # the say drops the colour word; the title keeps land.json's name so the keys match (flagged)
            dict(say="the town's voice for its land", demand=dict(hours=8, money=.02, entry=0, energy=.5),
                 any=["the town's land voice"], height="Known",
                 years=(10.4, 8, 16), share=0.1, contests_y=2, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a reserve needs land and a trust behind it)
    "rewilding": dict(
        shape="land", face="G U", sphere="learn", domain="", calling=True, dreams=[],
        thing="the wild land", doing="letting land go back to wild", contest="the yearly species count",
        places=["prod.wild", "gather.hall", "rule.counsel"],
        people=dict(coach="an ecologist from the wildlife trust", rival="a farmer who wants the field kept tidy",
                    peer="the trust's volunteers", patron="a landowner who gives a field"),
        round=["the trust's monthly volunteer day", "a corner of the school grounds", "a field lent by a landowner"],
        below="{N} leaves the far corner alone and goes back each month to see what has come",
        prep=["naturalist"], meets=["meaning"],
        tribal="to let the old camping ground go back to the wood so the game returns",
        magic="to give the old wood back the fields the towers took, and let the old powers settle in them",
        rungs=[
            dict(say="a corner", demand=dict(hours=6, money=.03, entry=.05, energy=.4),
                 any=["rewilder"],
                 years=(1.5, 1, 2), share=0.9, start=(25, 50, 70), contests_y=0, forks=["go_on"]),
            dict(say="a field returned", demand=dict(hours=8, money=.05, entry=.2, energy=.45),
                 any=["land restorer"],
                 years=(7.5, 5, 10), share=0.35, contests_y=1, forks=["round"]),
            dict(say="a reserve", demand=dict(hours=12, money=.1, entry=.5, energy=.5),
                 any=["reserve founder"], height="Known",
                 years=(19.5, 15, 30), share=0.1, contests_y=1, forks=["take"]),
        ]),

    # ------------------------------------------------------------------ the water (ten ways)

    # clocks: land.json ladder_years; shares estimate (a club has one bailiff and one chair)
    "angling_club": dict(
        shape="land", face="W G", sphere="gather", domain="", calling=False, dreams=[],
        thing="fishing", doing="fishing with the angling club", contest="a club match",
        places=["prod.wild", "gather.hall"],
        people=dict(coach="the club's oldest member", rival="the angler who always draws the best peg",
                    peer="the club's match regulars", patron="the landowner who leases the club its bank"),
        round=["the club's Sunday match", "the canal when the river is in flood", "a day ticket on a lake"],
        below="{N} ties floats at the kitchen table on winter nights",
        prep=["the river"], meets=["belonging", "competence"],
        tribal="to fish the clan's river by the old shares, each family to its own pools",
        magic="to fish the moon lake by the guild's licence and the water's old rules",
        rungs=[
            dict(say="a licence", demand=dict(hours=4, money=.05, entry=.1, energy=.2),
                 window=dict(every=1, open_weeks=36, deadline_age=None, deadline_years=None, pause_stops=False),  # the river's open season
                 upkeep=dict(of="credential", years=1, kept_by=["fishing"]),  # the rod licence is yearly
                 any=["angler"],
                 years=(1, 1, 2), share=0.9, start=(8, 30, 65), contests_y=1, forks=["go_on"]),
            dict(say="the club's matches", demand=dict(hours=6, money=.08, entry=.1, energy=.3),
                 any=["match angler"],
                 years=(3.5, 2, 5), share=0.55, contests_y=6, forks=["pay"]),
            dict(say="the club's bailiff or chair", demand=dict(hours=6, money=.03, entry=0, energy=.3),
                 window=dict(every=1, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),  # the club's yearly meeting
                 any=["club bailiff"],
                 years=(13.0, 10, 20), share=0.15, contests_y=4, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (many stop at the first cold winter)
    "wild_swimming": dict(
        shape="land", face="R W", sphere="gather", domain="", calling=False, dreams=[],
        thing="cold water", doing="swimming outdoors", contest="the midwinter swim",
        places=["prod.wild", "gather.circle"],
        people=dict(coach="the group's founder", rival="a swimmer who dares further out",
                    peer="the morning swimmers", patron="the cafe that opens early for the group"),
        round=["the group's dawn swim every Saturday", "the lake when the river runs high",
               "the tidal pool along the coast"],
        below="{N} checks the water's temperature before the weather forecast",
        prep=["fitness", "the river"], meets=["belonging", "meaning"],
        tribal="to swim the cold river with the young ones at the spring gathering",
        magic="to swim the moon lake at dawn, as the water's old customs ask",
        rungs=[
            dict(say="first cold swims", demand=dict(hours=3, money=.02, entry=.05, energy=.5),
                 any=["cold-water swimmer"],
                 years=(1, 1, 2), share=0.9, start=(16, 45, 70), contests_y=1, forks=["go_on"]),
            dict(say="every season", demand=dict(hours=3, money=.02, entry=.03, energy=.55),
                 window=dict(every=1, open_weeks=12, deadline_age=None, deadline_years=None, pause_stops=False),  # the winter swims
                 any=["all-season swimmer"],
                 years=(3.0, 2, 4), share=0.65, contests_y=1, forks=["round"]),
            dict(say="leads the group", demand=dict(hours=4, money=.02, entry=.02, energy=.45),
                 upkeep=dict(of="credential", years=3, kept_by=["leading swims"]),  # water safety and first aid renewed
                 any=["swim group lead"],
                 years=(7.8, 6, 12), share=0.2, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (one commodore at a time; instructors a few)
    "sailing": dict(
        shape="land", face="U R", sphere="gather", domain="", calling=False, dreams=[],
        thing="sailing", doing="sailing and rowing", contest="a regatta",
        places=["gather.games", "prod.wild"],
        people=dict(coach="the club's instructor", rival="the helm who always rounds the mark first",
                    peer="the club's crews", patron="a boat owner who needs a crew"),
        round=["the club's Wednesday evening races", "crewing for a boat owner", "the rowing club's boats"],
        below="{N} reads the wind in the trees from the window every morning",
        prep=["boats", "fitness"], meets=["belonging", "competence"],
        tribal="to take the dugout across the great lake and back before the wind turns",
        magic="to sail the tower's skiffs across the moon lake, reading the winds the weather-mages set",
        rungs=[
            dict(say="lessons", demand=dict(hours=5, money=.1, entry=.15, energy=.5),
                 window=dict(every=1, open_weeks=16, deadline_age=None, deadline_years=None, pause_stops=False),  # lessons run in the summer season
                 any=["learner sailor"],
                 years=(1, 1, 2), share=0.9, start=(8, 25, 55), contests_y=0, forks=["pay"]),
            dict(say="races", demand=dict(hours=7, money=.15, entry=.4, energy=.6),
                 window=dict(every=1, open_weeks=26, deadline_age=None, deadline_years=None, pause_stops=False),  # the racing season
                 any=["club racer"],
                 years=(4.5, 3, 6), share=0.5, contests_y=6, forks=["go_on"]),
            dict(say="commodore or instructor", demand=dict(hours=8, money=.1, entry=.05, energy=.5),
                 window=dict(every=1, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),  # the club's yearly meeting
                 upkeep=dict(of="credential", years=5, kept_by=["instructing"]),  # the instructor badge is revalidated
                 any=["commodore"],
                 years=(13.0, 10, 20), share=0.15, contests_y=4, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (finding a source takes a patient record)
    "water_testing": dict(
        shape="land", face="U W", sphere="learn", domain="", calling=False, dreams=[],
        thing="the river's water", doing="testing the water", contest="the trust's yearly report",
        places=["prod.wild", "learn.keeping", "rule.counsel"],
        people=dict(coach="the river trust's scientist", rival="a firm upstream that says its outfall is clean",
                    peer="the volunteer samplers", patron="a councillor who reads the record"),
        round=["the monthly sampling round", "a stream nobody has tested", "the trust's training day each spring"],
        below="{N} keeps a chart on the kitchen wall of every sample since the first",
        prep=["the river", "naturalist"], meets=["meaning", "competence"],
        tribal="to know which springs are good to drink and which make people sick, and keep the clan from the bad ones",
        magic="to test the springs and wells for the tower's healers, by the old tinctures and the new",
        rungs=[
            dict(say="monthly samples", demand=dict(hours=2, money=.01, entry=.03, energy=.2),
                 any=["water sampler"],
                 years=(1, 1, 2), share=0.9, start=(16, 50, 75), contests_y=0, forks=["go_on"]),
            dict(say="finds a source", demand=dict(hours=4, money=.02, entry=0, energy=.3),
                 any=["river detective"],
                 years=(3.5, 2, 5), share=0.4, contests_y=1, forks=["round"]),
            dict(say="the town's water expert", demand=dict(hours=5, money=.01, entry=0, energy=.3),
                 any=["water expert"], height="Known",
                 years=(10.4, 8, 16), share=0.2, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a town's flood board has a handful of seats)
    "flood_warden": dict(
        shape="land", face="W U", sphere="prot", domain="community", calling=False, dreams=[],
        thing="the flood watch", doing="keeping the street's flood watch", contest="a flood night",
        places=["prot.rescue", "rule.counsel"],
        people=dict(coach="the council's flood officer", rival="a neighbour who says the warnings are a fuss",
                    peer="the other wardens", patron="the ward councillor"),
        round=["the wardens' yearly flood exercise", "the residents' meeting", "a phone chain up the street"],
        below="{N} checks the river gauge on the way to work, every day of the wet months",
        prep=["the river", "organising"], meets=["belonging", "meaning"],
        tribal="to watch the river in the rains and wake the camp before it rises",
        magic="to watch the river spirit's moods in the wet season, and ring the bell in time",
        rungs=[
            dict(say="warden for the street", demand=dict(hours=2, money=0, entry=0, energy=.2),
                 upkeep=dict(of="credential", years=3, kept_by=["flood exercises"]),  # the warden training is refreshed
                 any=["street flood warden"],
                 years=(1, 1, 2), share=0.9, start=(25, 55, 75), contests_y=1, forks=["go_on"]),
            dict(say="for the ward", demand=dict(hours=3, money=0, entry=0, energy=.3),
                 any=["ward flood warden"],
                 years=(4.0, 3, 5), share=0.45, contests_y=1, forks=["pay"]),
            dict(say="on the town's flood board", demand=dict(hours=4, money=0, entry=0, energy=.35),
                 any=["flood board member"], height="Known",
                 years=(10.4, 8, 16), share=0.2, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a water board has one chair)
    "water_rights": dict(
        shape="land", face="W B", sphere="rule", domain="community", calling=False, dreams=[],
        thing="the water", doing="sharing out the water", contest="the water board's vote",
        places=["prod.land", "rule.counsel"],
        people=dict(coach="an old farmer who knows every right", rival="a neighbour who draws more than the share",
                    peer="the farmers on the rota", patron="the water board's clerk"),
        round=["the rota's monthly meeting", "a well shared with a neighbour", "an appeal to the board"],
        below="{N} knows the day and the hour of every turn on the ditch",
        prep=["trading", "the river"], meets=["competence", "belonging"],
        tribal="to keep the clan's turn at the waterhole fair in the dry season",
        magic="to hold a share of the guild's wells and sit at the table where the water is shared",
        rungs=[
            dict(say="a share", demand=dict(hours=3, money=.1, entry=.8, energy=.2),
                 upkeep=dict(of="access", years=5, kept_by=["drawing water"]),  # a share left unused for years can be lost
                 any=["water shareholder"],
                 req="has('plot of land') | was('farmer') | has('inheritance')",
                 years=(2, 0, 5), share=0.8, start=(25, 50, 70), contests_y=0, forks=["pay"]),
            dict(say="on the water rota", demand=dict(hours=4, money=.05, entry=0, energy=.3),
                 any=["water rota keeper"],
                 years=(4.0, 3, 5), share=0.45, contests_y=1, forks=["go_on"]),
            dict(say="chairs the water board", demand=dict(hours=6, money=.02, entry=0, energy=.35),
                 window=dict(every=1, open_weeks=2, deadline_age=None, deadline_years=None, pause_stops=False),  # the board's yearly vote
                 any=["water board chair"], height="Known",
                 years=(13.0, 10, 20), share=0.1, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a boat of one's own is the hard step)
    "catch_to_sell": dict(
        shape="land", face="B U", sphere="prod", domain="career", calling=False, dreams=[],
        thing="the catch", doing="fishing to sell", contest="the morning market",
        places=["prod.wild", "comm.market"],
        people=dict(coach="a skipper who takes them on", rival="the boat that always lands first",
                    peer="the fish market's traders", patron="a buyer who takes the whole catch"),
        round=["the early market every weekday", "ponds on a rented field", "crewing on another's boat"],
        below="{N} watches the tide tables the way others watch the news",
        prep=["boats", "the shore"], meets=["competence"],
        tribal="to bring in more fish than the camp eats, and trade the rest up the river",
        magic="to fish the deep lake for the scaled things the tower kitchens and the alchemists pay for",
        rungs=[
            dict(say="sells the catch", demand=dict(hours=25, money=.2, entry=.4, energy=.8),
                 upkeep=dict(of="credential", years=1, kept_by=["fishing to sell"]),  # the selling licence is yearly
                 any=["fish seller"],
                 req="has('fishing licence') | was('commercial fisher') | has('boat of one\\'s own')",
                 years=(1.5, 1, 2), share=0.85, start=(16, 30, 45), contests_y=4, forks=["go_on"]),
            dict(say="a boat or ponds of their own", demand=dict(hours=35, money=.3, entry=1.0, energy=.85),
                 any=["boat owner"],
                 years=(6.5, 5, 8), share=0.4, contests_y=4, forks=["pay"]),
            dict(say="the market's main supplier", demand=dict(hours=45, money=.35, entry=.5, energy=.85),
                 any=["chief fish supplier"],
                 years=(13.0, 10, 20), share=0.15, contests_y=4, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (most shore stalls stay seasonal)
    "shore_business": dict(
        shape="land", face="B R", sphere="comm", domain="career", calling=False, dreams=[],
        thing="the shore business", doing="trading by the water", contest="the summer season",
        places=["comm.shop", "prod.wild"],
        people=dict(coach="an old trader on the front", rival="the kiosk that undercuts them",
                    peer="the other traders on the shore", patron="the landlord of the lease"),
        round=["the yearly summer fair on the front", "a hire boat on the lake", "a van at the beach car park"],
        below="{N} counts the clouds over the water each morning and guesses the takings",
        prep=["trading", "the shore"], meets=["competence", "belonging"],
        tribal="to keep the landing place where the boats come in, and take a share of each trade",
        magic="to keep the ferry stall at the moon lake, where every traveller to the towers stops",
        rungs=[
            dict(say="a summer stall", demand=dict(hours=30, money=.3, entry=.5, energy=.7),
                 window=dict(every=1, open_weeks=14, deadline_age=None, deadline_years=None, pause_stops=False),  # the summer season
                 upkeep=dict(of="credential", years=1, kept_by=["trading"]),  # the trading licence is yearly
                 any=["summer stall keeper"],
                 req="has('savings') | has('family business') | has('inheritance')",
                 years=(1, 1, 2), share=0.85, start=(20, 40, 60), contests_y=1, forks=["pay"]),
            dict(say="a year-round place", demand=dict(hours=45, money=.4, entry=.8, energy=.8),
                 any=["shore cafe owner"],
                 years=(4.0, 3, 5), share=0.4, contests_y=1, forks=["take"]),
            dict(say="the shore's best-known business", demand=dict(hours=50, money=.4, entry=.5, energy=.75),
                 any=["the shore's best-known trader"], height="Known",
                 years=(13.0, 10, 20), share=0.15, contests_y=1, forks=["go_on"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a gallery shows a few of the many who collect)
    "beachcombing": dict(
        shape="land", face="R G", sphere="arts", domain="", calling=False, dreams=[],
        thing="the shore's finds", doing="beachcombing and making shore art", contest="the gallery's open show",
        places=["prod.wild", "arts.craft"],
        people=dict(coach="an old mudlark who knows the tides", rival="an artist who works the same beach",
                    peer="the shore people", patron="the gallery owner"),
        round=["the lowest tides each month", "the river's foreshore", "the craft market in the square"],
        below="{N} keeps a jar of sea glass on every windowsill",
        prep=["the workshop", "the shore"], meets=["meaning", "competence"],
        tribal="to find the shells and stones the traders want, and make them into things worth carrying",
        magic="to find what the lake gives up after storms and set it in the charms the guild sells",
        rungs=[
            dict(say="a shelf of finds", demand=dict(hours=2, money=.01, entry=0, energy=.3),
                 any=["beachcomber"],
                 years=(1, 1, 2), share=0.9, start=(8, 50, 75), contests_y=0, forks=["go_on"]),
            dict(say="shows the art", demand=dict(hours=4, money=.03, entry=.05, energy=.3),
                 window=dict(every=1, open_weeks=3, deadline_age=None, deadline_years=None, pause_stops=False),  # the gallery's yearly open show
                 any=["shore artist"],
                 years=(4.5, 3, 6), share=0.4, contests_y=2, forks=["pay"]),
            dict(say="the gallery's name", demand=dict(hours=8, money=.05, entry=.1, energy=.35),
                 any=["gallery name"], height="Known",
                 years=(13.0, 10, 20), share=0.12, contests_y=1, forks=["take"]),
        ]),

    # clocks: land.json ladder_years; shares estimate (a trust has one lead and many volunteers)
    "restore_river": dict(
        shape="land", face="G U", sphere="learn", domain="community", calling=True, dreams=[],
        thing="the river", doing="bringing the river back", contest="the fish count",
        places=["prod.wild", "gather.circle", "rule.counsel"],
        people=dict(coach="the trust's project officer", rival="a landowner who wants the banks kept straight",
                    peer="the volunteer day crew", patron="a landowner who gives the trust a stretch"),
        round=["the trust's monthly volunteer day", "a stream through the school grounds", "a stretch on a willing farm"],
        below="{N} stands on the bridge and watches for fish where the new bend was cut",
        prep=["the river", "naturalist"], meets=["meaning", "belonging"],
        tribal="to clear the clan's river of fallen trees and let the fish run up again",
        magic="to give the river back its old bends, and the river spirit back its home",
        rungs=[
            dict(say="volunteer days", demand=dict(hours=4, money=.01, entry=.02, energy=.5),
                 any=["river volunteer"],
                 years=(1, 1, 2), share=0.9, start=(16, 45, 70), contests_y=1, forks=["go_on"]),
            dict(say="a stretch restored", demand=dict(hours=6, money=.02, entry=0, energy=.55),
                 window=dict(every=1, open_weeks=10, deadline_age=None, deadline_years=None, pause_stops=False),  # in-river works only in late summer
                 any=["river restorer"],
                 years=(4.5, 3, 6), share=0.45, contests_y=1, forks=["round"]),
            dict(say="the trust's lead", demand=dict(hours=10, money=.02, entry=0, energy=.5),
                 any=["river trust lead"], height="Known",
                 years=(13.0, 10, 20), share=0.15, contests_y=1, forks=["take"]),
        ]),
}


# Chroma library, modern Earth: v25 prep, the 33 new titles the new fields name (Library, 10-23). DRAFT, nothing
# reads it: the Library pours TITLES_V25 into earth_perks_titles.py (a perks_titles/ part) on Friday 10-23 21:00
# (Emren's time), beside FIELDS_EARTH from fields-a.py to fields-d.py. Plain data: nothing is imported, nothing runs.
#
# Source: the NEW_TITLES lists of fields-a.py (21), fields-b.py (2), fields-c.py (3) and fields-d.py (7). Each draft's
# name, kind, ages, share (with its comment), say and gained are kept as drafted. Written to the catalogue's format
# (perks_titles/00-head.py): name, kind, sector (careers only), sphere, face, ways, profiles, meets, lasts (statuses
# only), ages, share, say, gained, lost, needs, and the new key `doors` (what holding the title opens: a setting, a
# person, a seat or the step after; aims-shape.md sections 7 and 9).
#
# One value changed from the drafts, everywhere it occurs: `ways` on the 28 statuses. The catalogue's rule is that
# every status has ways="" (a status is a fact about a life and works through meets alone; only commitment-kind
# titles become a commitment's profile and count in the colour balance), so a status with ways="U B" would enter the
# balance check. The drafts gave each status its field's face; that face is kept as the first of `profiles`, and its
# first letter in `face` (the catalogue's one-letter form: sphere.letter). `sphere` is the field's where it has one
# and fits; the foster titles (field has none) take care, the animal fosterer care (as [animal care worker]), the
# expedition titles (field has none) learn, and the martial arts instructor learn (as [youth coach]). The 5 careers
# keep their drafted ways, which are their first profile as usual.
#
# Statuses here are rung titles, kept for life once reached (aims-shape.md section 6), so lasts="life", except the
# three whose drafted ages end early (academy footballer, top-flight footballer, amateur fighter), which fade in the
# years given. Profiles: every title is open to more than one temperament; they are tendencies, never walls.
# The field "to earn a black belt" is named here by its key; every word a player reads says "the first-degree belt".

TITLES_V25 = [
  # field "to master chess", rung 1 (a club player)
  dict(name="club chess player", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U B", "Studies the openings at home and plays every game on the ladder to climb it."),
                 ("W G", "Comes for the club night itself: the same tables, the same faces, tea at the break."),
                 ("R", "Plays fast and bold, hates a draw, and is always up for one more game.")],
       meets="need:belonging+.05 need:competence+.03 res:time-.03", lasts="life",
       ages=(7, 110), share=0.01,      # estimate: about 1 in 100 people ever play regularly at a club
       say="a club chess player",
       gained="joining a chess club and playing its league or ladder through a season",
       lost="never as a record; the club nights stop with a move, a busier life or the club closing",
       needs="the moves learned at home or at school; a club within reach and an evening a week",
       doors="the club's regulars and its weekend tournaments; a coach at the club who sees something in them"),
  # field "to master chess", rung 2 (a rated player)
  dict(name="rated chess player", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U B", "Watches the rating after every event and works on the weak lines between them."),
                 ("W", "Plays every round of the club's team matches, win or lose, because the team needs a board."),
                 ("R G", "Travels to the weekend tournaments for the hall full of players as much as for the points.")],
       meets="need:competence+.05 res:time-.05 res:money-.02", lasts="life",
       ages=(8, 110), share=0.003,     # estimate: rated players are a few in 1,000 people
       say="a rated chess player",
       gained="enough rated games at weekend tournaments for an official rating",
       lost="never as a record; the rating goes quiet when they stop entering tournaments",
       needs="[club chess player]; entry fees and travel to weekend tournaments",
       doors="the open sections of tournaments further away; rivals at the same strength to measure against"),
  # field "to master chess", rung 3 (a tournament winner)
  dict(name="chess tournament winner", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U B", "Prepares for each opponent in the draw and takes the half point when it is enough."),
                 ("R", "Wins by attacking in every game and enjoys the last round more than any other."),
                 ("G W", "Plays the same steady game every round and is still there at the top on the last day.")],
       meets="need:competence+.05 need:meaning+.03", lasts="life",
       ages=(9, 110), share=0.001,     # estimate
       say="a chess tournament winner",
       gained="first place, alone or shared, in an open tournament",
       lost="never; the win stays in the tournament's records",
       needs="[rated chess player]",
       doors="invitations to stronger tournaments; a sponsor or a coach willing to back the next step"),
  # field "to master chess", rung 4 (a master)
  dict(name="chess master", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U", "Has spent thousands of hours on positions and knows the game's history by heart."),
                 ("B R", "Plays for prizes and reputation, and travels wherever the strongest field is."),
                 ("W", "Coaches juniors at the club on weekday evenings and keeps the club's team together.")],
       meets="need:competence+.08 need:meaning+.05 res:time-.05", lasts="life",
       ages=(12, 110), share=0.0001,   # estimate: titled and master-rated players are tens of thousands worldwide
       say="a chess master",
       gained="a master's rating held, or the results at strong tournaments that earn the title",
       lost="never; the title is kept once awarded",
       needs="[rated chess player] for years; [chess tournament winner] usually first",
       doors="paid coaching and simultaneous displays; the international tournaments where a grandmaster result is "
             "possible"),
  # field "to master chess", rung 5 (a grandmaster)
  dict(name="chess grandmaster", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U B", "Lives at the board, prepares lines for months and plays for the very top of the rankings."),
                 ("W G", "Teaches, writes and coaches the national juniors, handing the game on."),
                 ("R", "Is known for wild, fearless games that people replay for years.")],
       meets="need:competence+.08 need:meaning+.08 res:ties+.03", lasts="life",
       ages=(13, 110), share=0.0000003,  # about two thousand grandmasters have held the title, all told
       say="a chess grandmaster",
       gained="three grandmaster results at international tournaments and a rating above the grandmaster mark",
       lost="never; the title is for life",
       needs="[chess master]; strong international tournaments to play in",
       doors="a seat at the strongest invitation tournaments; pupils, books and a name in the game"),
  # field "to play football at the top", rung 2 (picked for an academy)
  dict(name="academy footballer", kind="status", sphere="gather", face="gather.B", ways="",
       profiles=[("B R", "Wants the contract more than anything and knows every other boy or girl after the same place."),
                 ("W", "Trains the way the coaches say, never misses a session and plays for the side."),
                 ("G", "Plays by instinct and joy, the way they played in the park.")],
       meets="need:competence+.05 need:meaning+.05 res:time-.08 res:ties-.03", lasts=6,   # a few seasons; ages end it
       ages=(8, 21), share=0.002,      # estimate: a few in 1,000 children ever hold an academy place
       say="an academy footballer",
       gained="a scout's eye at a junior match or the open trials, then a place in a club's youth academy",
       lost="being released at the end of a season, an injury, growing out of the age groups without a contract",
       needs="[on the team]; a family who gets them to training several evenings a week",
       doors="the academy's coaches and its matches against other clubs; the first contract, if the club keeps them"),
  # field "to play football at the top", rung 4 (a regular in the top division)
  dict(name="top-flight footballer", kind="status", sphere="gather", face="gather.B", ways="",
       profiles=[("B R", "Plays for the next contract and the bigger club, and lives for the big match."),
                 ("W", "Is the steady professional the manager can rely on, season after season."),
                 ("U", "Studies the opponents on film and keeps the body in order to last longer than most.")],
       meets="need:meaning+.05 need:competence+.05 res:freedom-.05", lasts=10,   # a top-division stretch; ages end it
       ages=(17, 40), share=0.0001,    # estimate
       say="a top-flight footballer",
       gained="a first-team debut in the top division and a season of games there after it",
       lost="relegation and a move down, losing the place in the side, an injury, retiring in their thirties",
       needs="[professional athlete] at a club in the top division; [academy footballer] or years in the lower "
             "divisions first",
       doors="the national side's selectors; agents, sponsors and a face people know in the street"),
  # field "to play football at the top", rung 5 (picked for the national side)
  dict(name="international footballer", kind="status", sphere="gather", face="gather.B", ways="",
       profiles=[("B R", "Takes the shirt as the proof they were the best, and wants every cap after it."),
                 ("W", "Plays for the people back home and carries the town's pride onto the pitch."),
                 ("G", "Remembers the park where it started and goes back there to coach the children.")],
       meets="need:meaning+.08 need:belonging+.03", lasts="life",
       ages=(17, 110), share=0.00003,  # estimate
       say="an international footballer",
       gained="a call-up to the national side and a first cap on the pitch",
       lost="never; a cap is kept for life",
       needs="[top-flight footballer] or [professional athlete] at a strong club; eligibility for the national side",
       doors="the biggest tournaments; a name the country knows"),
  # field "to race cars", rung 1 (a kart and a club track)
  dict(name="club kart racer", kind="status", sphere="gather", face="gather.B", ways="",
       profiles=[("B R", "Wants to win every heat and argues about the results after each race."),
                 ("U", "Spends as long on the kart in the paddock as on the track, tuning it race by race."),
                 ("W G", "Comes for the family weekend at the track, with a parent as the whole pit crew.")],
       meets="need:competence+.03 need:autonomy+.03 res:money-.05 res:time-.05", lasts="life",
       ages=(6, 80), share=0.003,      # estimate
       say="a club kart racer",
       gained="a kart, second-hand or hired, and a first season of races at the club track",
       lost="never as a record; the racing stops when the money or the weekends run out",
       needs="a family or [savings] to pay for the kart, the fuel and the track days",
       doors="the club track's paddock and its regulars; the racing licence course"),
  # field "to race cars", rung 2 (a licence and a full season)
  dict(name="licensed racing driver", kind="status", sphere="gather", face="gather.B", ways="",
       profiles=[("B R", "Chases a paid seat and looks for a backer at every race weekend."),
                 ("U", "Learns every corner of every circuit and reads the timing sheets late into the night."),
                 ("W", "Keeps to the rules and the team's plan and finishes every race in one piece.")],
       meets="need:competence+.05 need:autonomy+.03 res:money-.08 res:time-.05", lasts="life",
       ages=(8, 80), share=0.0005,     # estimate
       say="a licensed racing driver",
       gained="the racing licence test passed and a full season entered in a junior series",
       lost="never as a record; the season's entry lapses when the money for it runs out",
       needs="[club kart racer]; the licence course and a season's entry, paid by the family, [savings], the "
             "[family business] or a backer",
       doors="a junior series and its teams; sponsors who watch the results"),
  # field "to race cars", rung 3 (a junior championship)
  dict(name="junior racing champion", kind="status", sphere="gather", face="gather.B", ways="",
       profiles=[("B R", "Took the title by being faster and harder in every race of the season."),
                 ("U W", "Took it by finishing in the points every weekend while others crashed out.")],
       meets="need:competence+.05 need:meaning+.05", lasts="life",
       ages=(10, 110), share=0.00005,  # estimate
       say="a junior racing champion",
       gained="the most points over a season of a junior series",
       lost="never; the championship stays in the records",
       needs="[licensed racing driver]",
       doors="tests with senior teams; a sponsor ready to pay for a seat"),
  # field "to race cars", rung 5 (a championship title)
  dict(name="racing champion", kind="status", sphere="gather", face="gather.B", ways="",
       profiles=[("B R", "Won it on the edge, race after race, and wants the next one."),
                 ("U", "Won it with the team's engineers, one tenth of a second at a time."),
                 ("W", "Won it by never giving the stewards a reason and never letting the team down.")],
       meets="need:meaning+.08 need:competence+.05", lasts="life",
       ages=(17, 110), share=0.000005,  # estimate
       say="a racing champion",
       gained="a senior championship won over a full season with a team",
       lost="never; the championship stays in the records",
       needs="[professional athlete] with a seat in a senior team; [licensed racing driver]",
       doors="the top teams' offers; a name the country knows"),
  # field "to fight in the ring", rung 2 (amateur bouts)
  dict(name="amateur fighter", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R B G", "Loves the nerves before the bell and wants to know how far they can go."),
                 ("W", "Fights for the gym and the coach who took them off the street, and follows every rule."),
                 ("U", "Studies footwork and distance in the mirror until the body does it alone.")],
       meets="need:competence+.05 need:autonomy+.03 res:health-.02 res:time-.05", lasts=10,   # active years; ages end it
       ages=(10, 40), share=0.003,     # estimate
       say="an amateur fighter",
       gained="a medical, a first amateur bout at a club show, and more bouts after it",
       lost="stopping after a bad defeat, a medical that is not passed, a job or a family, age",
       needs="[boxing or martial arts]; a gym and a coach; a medical passed",
       doors="the club shows and the amateur championships; a coach who takes them seriously"),
  # field "to fight in the ring", rung 3 (an amateur title)
  dict(name="amateur ring champion", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R B", "Won it by wanting it more than anyone in the draw."),
                 ("U W", "Won it by doing exactly what the coach planned for each opponent."),
                 ("G", "Won it on toughness, the one still strong in the last round.")],
       meets="need:competence+.05 need:meaning+.05", lasts="life",
       ages=(12, 110), share=0.0003,   # estimate
       say="an amateur ring champion",
       gained="an amateur championship won at the weight, after a run of bouts",
       lost="never; the title stays in the records",
       needs="[amateur fighter]",
       doors="a place in a national squad; promoters offering a first paid fight"),
  # field "to fight in the ring", rung 5 (a title belt)
  dict(name="ring title holder", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R B", "Holds the title as the proof of who they are, and wants every challenger."),
                 ("W G", "Brings the title home to the old gym and puts it on the wall for the children."),
                 ("U", "Chooses each defence with care and plans the end of the career long before it comes.")],
       meets="need:meaning+.08 need:competence+.05 res:health-.03", lasts="life",
       ages=(18, 110), share=0.00002,  # estimate
       say="a title holder in the ring",
       gained="a professional title bout won on the scorecards or the referee's call",
       lost="never as a record; the title itself passes on in a lost defence or when it is given up",
       needs="[professional athlete] in the ring; [amateur fighter] years first",
       doors="the biggest fights and purses; a name the country knows"),
  # field "to earn a black belt" (a key; players read "the first-degree belt"), rung 2 (the first gradings passed)
  dict(name="graded martial artist", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R U W", "Trains for the next grading and loves the moment the instructor ties on a new belt."),
                 ("G", "Comes for the calm of the training hall and what it does for the body."),
                 ("B", "Trains to be able to look after themselves, and keeps at it because it works.")],
       meets="need:competence+.03 need:belonging+.03 res:health+.02 res:time-.03", lasts="life",
       ages=(5, 100), share=0.03,      # estimate: a few in 100 people ever pass a grading
       say="a graded martial artist",
       gained="the first gradings passed in front of the school's instructors",
       lost="never as a record; the training stops with a move, an injury or a busier life",
       needs="[boxing or martial arts] classes at a training hall",
       doors="the senior class and its instructors; the gradings above"),
  # field "to earn a black belt", rung 3 (the first-degree belt)
  dict(name="first-degree belt holder", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R U W", "Earned it through years of discipline and wears it as a promise to keep training."),
                 ("U", "Knows the forms in detail and the reasons behind each one."),
                 ("G R", "Earned it through stubborn effort, after injuries and long breaks, at their own pace.")],
       meets="need:competence+.05 need:meaning+.05", lasts="life",
       ages=(10, 110), share=0.008,    # estimate: about 1 in 10 of those who start a martial art reach it
       say="a first-degree belt holder",
       gained="years of classes and every grading below it, then the first-degree grading passed before a panel",
       lost="never; the grade is kept for life",
       needs="[graded martial artist] for years",
       doors="helping teach the junior classes; an instructor's course"),
  # field "to earn a black belt", rung 4 (a school of your own)
  dict(name="martial arts instructor", kind="career", sector="services", sphere="learn", face="learn.R",
       ways="R U W",
       profiles=[("R U W", "Runs a strict, warm class, and grades every pupil on what they can really do."),
                 ("G", "Teaches as it was taught to them, with patience for slow learners and the old ways kept."),
                 ("B", "Builds the hall into a business, with classes every evening and a waiting list.")],
       meets="need:competence+.05 need:meaning+.05 need:belonging+.03 res:money+.02 res:time-.08",
       ages=(18, 80), share=0.002,     # estimate
       say="a martial arts instructor",
       gained="the first-degree belt, an instructor's course and a hall rented for a class of one's own",
       lost="too few pupils to pay the rent, an injury, the hall closing, handing the class to a senior pupil",
       needs="[first-degree belt holder]; an instructor's course or [coaching badge]; [cleared to work with "
             "children] for children's classes; age 18 or more",
       doors="a hall and a class of pupils; their own pupils' gradings, and a name in the town's training halls"),
  # field "to make video games", rung 1 (a first game finished)
  dict(name="hobby game maker", kind="status", sphere="arts", face="arts.U", ways="",
       profiles=[("U R", "Builds odd little worlds to see what happens, and finishes one in a weekend."),
                 ("W G", "Makes games with friends for the group, and plays every one of theirs."),
                 ("B", "Keeps every player's comment and wants the next game to be the one people pay for.")],
       meets="need:competence+.05 need:autonomy+.03 res:time-.05", lasts="life",
       ages=(10, 100), share=0.01,     # estimate
       say="a hobby game maker",
       gained="a small game finished and shared, at a game jam or online, that other people play",
       lost="never as a record; the making stops when other things take the evenings",
       needs="[writing code] or [drawing and painting]; a computer and the evenings to use it",
       doors="other makers online and at the game jams; a portfolio for a first studio job"),
  # field "to make video games", rung 3 (a game with your name on it)
  dict(name="lead game designer", kind="career", sector="knowledge", sphere="arts", face="arts.U", ways="U R",
       profiles=[("U R", "Holds the whole game in their head and tries every idea before keeping one."),
                 ("W B", "Keeps the team on the plan and the budget, and gets the game out on time."),
                 ("G", "Designs from the feel of play, testing with real players until it plays right.")],
       meets="need:meaning+.08 need:competence+.05 res:money+.1 res:time-.12 need:safety-.03",
       ages=(22, 75), share=0.0003,    # estimate
       say="a lead game designer",
       gained="years as a [video-game developer], then charge of a game's design from start to release",
       lost="the studio closing or 'a wave of layoffs at work', a game that fails, 'burnout', a studio of their own",
       needs="[video-game developer] for years, or [founder of a firm] with a game of its own",
       doors="a team that builds what they design; a game with their name on it"),
  # field "to play in a band", rung 2 (gigs to real crowds)
  dict(name="gigging musician", kind="status", sphere="arts", face="arts.R", ways="",
       profiles=[("R", "Lives for the gig itself, loud and late, and the crowd singing back."),
                 ("U", "Works the set over at every rehearsal and knows every venue's sound."),
                 ("B", "Books the dates, chases the fees and builds the mailing list.")],
       meets="need:meaning+.05 need:belonging+.03 res:time-.05 res:health-.02", lasts="life",
       ages=(14, 90), share=0.02,      # estimate: a few in 100 people ever play gigs to paying or passing crowds
       say="a gigging musician",
       gained="a first booked gig to people who are not friends or family, and more booked after it",
       lost="never as a record; the gigs stop with the band splitting, a move or a child at home",
       needs="[musical instrument] or [singing]; [amateur band member] usually first",
       doors="the venues and promoters in town; a crowd that comes back"),
  # field "to be famous", rung 1 (an audience of your own)
  dict(name="online creator", kind="status", sphere="arts", face="arts.B", ways="",
       profiles=[("B", "Watches the numbers after every post and shapes the show to grow them."),
                 ("R", "Posts whatever they feel that day, and the audience comes for the person."),
                 ("U G", "Makes patient shows on one subject they love, and the people who share it find them.")],
       meets="need:autonomy+.03 need:meaning+.03 res:time-.05", lasts="life",
       ages=(12, 100), share=0.08,     # estimate: people who ever post regularly for an audience of a few hundred or more
       say="an online creator",
       gained="months of posting the same kind of show every week, until a few hundred people come back for each new "
              "one",
       lost="never as a record; the audience drifts away when the posting stops",
       needs="a phone or camera, somewhere to post and the weeks to keep at it",
       doors="other creators who share each other's work; a following that can grow"),
  # field "to be famous", rung 3 (paid to be seen)
  dict(name="full-time creator", kind="career", sector="services", sphere="arts", face="arts.B", ways="B",
       profiles=[("B", "Runs the channel as a business: sponsors, schedules, and every number watched."),
                 ("R", "Is the show, on camera every day, and the audience pays for the person."),
                 ("U", "Makes careful, researched work, slowly, for viewers who pay to keep it going.")],
       meets="need:autonomy+.08 need:meaning+.05 res:money+.03 res:time-.12 need:safety-.05",
       ages=(16, 80), share=0.003,     # estimate from creator-economy surveys: a few million earn a living from it worldwide
       say="a full-time creator",
       gained="a [following online] that brings in enough from sponsors and viewers to leave the day job",
       lost="the audience moving on, a sponsor pulling out, 'burnout', a return to a day job",
       needs="[online creator] and [following online]",
       doors="sponsors and the studios that court creators; a face the country might come to know"),
  # field "to take in a child who has no one", rung 1 (checked, trained and approved)
  dict(name="approved foster carer", kind="status", sphere="care", face="care.W", ways="",
       profiles=[("W", "Applies because a child should not be without a home, and does every course offered."),
                 ("G", "Has always had a full house and a spare chair, and sees no reason to stop."),
                 ("U", "Reads everything about children who have been through hard things, and asks every question.")],
       meets="need:meaning+.05 res:time-.05", lasts="life",
       ages=(21, 75), share=0.02,      # estimate: somewhat more than the foster parents (.015 in the catalogue), as some
                                       # approved carers stop before a long placement
       say="an approved foster carer",
       gained="a first enquiry, months of training, home checks and references, then a panel's approval to foster",
       lost="never as a record; the approval lapses when they stop fostering or the agency withdraws it",
       needs="age 21 or more; a spare room; [cleared to work with children]",
       doors="a social worker's call about a child who needs a bed tonight; the foster carers' support group"),
  # field "to take in a child who has no one", rung 3 (a home that held)
  dict(name="long-term foster parent", kind="status", sphere="care", face="care.W", ways="",
       profiles=[("W", "Keeps every promise made to the child, especially the small ones."),
                 ("G", "Lets the child grow at their own pace, and makes them part of the whole family."),
                 ("B R", "Fights the system for the child's school place, therapy and rights, and does not let go.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.05", lasts="life",
       ages=(25, 85), share=0.006,     # estimate: a minority of foster parents keep one child for years
       say="a long-term foster parent",
       gained="a foster placement agreed as a child's home until they are grown, kept through the first hard years",
       lost="never as a record; the placement can end in a breakdown, a return home or an adoption",
       needs="[approved foster carer] and [foster parent]",
       doors="a child who stays, and who may call them family when grown; guardianship or adoption, if it comes"),
  # field "to take in a child who has no one", rung 4 (a child who had no one, grown up and at home)
  dict(name="foster parent to many", kind="status", sphere="care", face="care.W", ways="",
       profiles=[("W", "Has a house rule for everything and a bed made up for whoever comes next."),
                 ("G", "Runs a big, warm, untidy home where the grown ones bring their own children back."),
                 ("U", "Trains new carers, because after so many children they know what works.")],
       meets="need:meaning+.08 res:ties+.05", lasts="life",
       ages=(30, 90), share=0.003,     # estimate: carers who foster for a decade or more and take in many children
       say="a foster parent to many children",
       gained="a decade or more of fostering, with many children through the door and some still in touch",
       lost="never; the years and the children are part of their history",
       needs="[foster parent] for a decade or more; [approved foster carer]",
       doors="grown foster children who come back with their own; a voice in how the town's fostering is run"),
  # field "to run an animal sanctuary", rung 2 (rescued animals at home)
  dict(name="animal fosterer", kind="status", sphere="care", face="care.G", ways="",
       profiles=[("G W", "Takes in the frightened ones and lets them settle in their own time."),
                 ("U", "Keeps notes on each animal's habits for the shelter and the new owners."),
                 ("R", "Falls for every one and cries at every goodbye, then takes the next.")],
       meets="need:meaning+.05 res:time-.05 res:money-.02", lasts="life",
       ages=(18, 90), share=0.01,      # estimate: a small share of households foster for a shelter at some point
       say="an animal fosterer",
       gained="a shelter's home check, then a first rescued dog or cat living with them until a new home is found",
       lost="never as a record; the fostering stops with a move, a landlord, or keeping one for good",
       needs="a home where animals are allowed; [handling animals] helps",
       doors="the shelter's staff and other fosterers; the animals no one else will take"),
  # field "to run an animal sanctuary", rung 3 (a sanctuary where no animal is turned away)
  dict(name="sanctuary keeper", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G W", "Keeps every animal for the rest of its days, whatever the cost."),
                 ("B U", "Runs the charity with care: the donors, the vet's bills, the accounts."),
                 ("R", "Takes the cases that make the news and talks about them to anyone who will listen.")],
       meets="need:meaning+.1 need:autonomy+.05 res:time-.12 res:money-.08 res:health-.03", lasts="life",
       ages=(25, 90), share=0.0005,    # estimate: sanctuaries are few, a handful to a region
       say="the keeper of an animal sanctuary",
       gained="land of their own, a registered charity and the first animals no one else would take",
       lost="never as a record; the sanctuary can close when the money or the keeper's strength runs out",
       needs="[plot of land] or [farmer]; [animal fosterer] or [animal care worker] first; [savings] or donors",
       doors="volunteers, donors and the local vet; the yearly open day the town comes to"),
  # field "to breed champion horses", rung 1 (a horse to look after)
  dict(name="stable groom", kind="career", sector="farm", sphere="prod", face="prod.G", ways="G U",
       profiles=[("G U", "Knows each horse by its moods and notices a limp before anyone else."),
                 ("W", "Keeps the yard in order, every stall and every feed on time, before dawn."),
                 ("R", "Rides out the young horses nobody else will get on.")],
       meets="need:meaning+.05 need:belonging+.03 res:money+.01 res:time-.1 res:health-.03",
       ages=(16, 70), share=0.005,     # estimate
       say="a stable groom",
       gained="weekends mucking out at a yard, then a paid place looking after other people's horses",
       lost="low pay, a bad back or a kick, the yard closing, a horse and a yard of their own",
       needs="age 16 or more; [handling animals] or years around horses",
       doors="the yard's owners and riders; a horse to ride and, one day, a mare of their own"),
  # field "to breed champion horses", rung 2 (a first foal that wins)
  dict(name="horse breeder", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G U", "Matches mares and stallions by eye and by the records, and waits years to see if it worked."),
                 ("B", "Breeds to sell, and knows what every foal is worth at the sales."),
                 ("W", "Keeps the old line going as the family always has.")],
       meets="need:meaning+.05 need:competence+.05 res:money-.05 res:time-.08", lasts="life",
       ages=(20, 90), share=0.002,     # estimate
       say="a horse breeder",
       gained="a mare put to a good stallion, a foal raised for three years, and a first win at a show",
       lost="never as a record; the breeding stops when the land, the mares or the money go",
       needs="[horse of one's own], [stable groom] or [plot of land]; money for the stud fee",
       doors="the horse shows and the other breeders there; owners who want a foal from the mare"),
  # field "to breed champion horses", rung 3 (a bloodline known everywhere)
  dict(name="breeder of champions", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G U", "Has watched the line for generations and knows what each cross will give."),
                 ("B", "Sells the line's foals to the highest bidders across the horse world."),
                 ("W", "Holds the line in trust, and hands it to the next generation in good order.")],
       meets="need:meaning+.08 need:competence+.05 res:money+.05", lasts="life",
       ages=(30, 95), share=0.0001,    # estimate: a few breeders in a generation have a line the whole horse world names
       say="a breeder of champions",
       gained="decades of foals and shows, until riders everywhere ask for horses of that line",
       lost="never; the line keeps their name",
       needs="[horse breeder] for decades",
       doors="buyers from far away; young breeders who want to learn from them"),
  # field "to explore the far places", rung 2 (a place on an expedition)
  dict(name="expedition member", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U R", "Goes to see what no one has seen, and fills notebooks with what they find."),
                 ("W G", "Carries the heavy loads and looks after the others when the weather turns."),
                 ("B", "Goes for the summit or the crossing that will make their name.")],
       meets="need:competence+.05 need:meaning+.05 res:time-.08 res:money-.05 res:health-.03 res:ties-.03",
       lasts="life",
       ages=(18, 70), share=0.002,     # estimate
       say="a member of an expedition",
       gained="years on the hills or in the field, then a place on a team going somewhere hard to reach",
       lost="never as a record; the trips stop with an injury, a family or the money",
       needs="[navigation] or [knowing the woods]; [keeping fit]; [first-aid certificate] helps; [passport] for "
             "far places",
       doors="the team and the people who fund such trips; the far places themselves"),
  # field "to explore the far places", rung 3 (leading an expedition)
  dict(name="expedition leader", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U R", "Plans the route to a place nobody has mapped, and goes first."),
                 ("W", "Brings everyone home, and turns back when the risk is too high."),
                 ("B G", "Raises the money, picks the team and talks the funders round.")],
       meets="need:meaning+.08 need:autonomy+.05 res:time-.1 res:money-.05 res:health-.03", lasts="life",
       ages=(25, 75), share=0.0003,    # estimate
       say="an expedition leader",
       gained="a few expeditions as a member, then a plan, the money raised and a team that will follow",
       lost="never as a record; the leading stops after an accident, a failed trip or age",
       needs="[expedition member] several times; [navigation]; money raised from funders",
       doors="societies that fund expeditions; a place nobody had mapped, and talks about it afterwards"),
]

# Chroma library, modern Earth: v25 prep, the 85 land ladder titles in the catalogue format (Library, 10-23).
# DRAFT, nothing reads it: the Library pours TITLES_V25_LAND into a perks_titles/ part beside TITLES_V25
# (titles-v25.py) and the land fields. Plain data: nothing is imported, nothing runs.
#
# Source: LAND_TITLES in land-ways.py (85 status titles, one per ladder step of the 30 land ways, in the same order;
# the 5 steps that reuse an existing title are not repeated here). Each draft's name, kind, ages, share (with its
# comment), say, gained and doors are kept as drafted; doors stay lists, as in the draft. Written to the
# catalogue's format (perks_titles/00-head.py) as titles-v25.py does: name, kind, sphere, face, ways, profiles,
# meets, lasts, ages, share, say, gained, lost, needs, doors.
#
# Changed from the drafts, everywhere: `ways`. The catalogue's rule is that every status has ways="" (a status works
# through meets alone and stays out of the colour balance). The drafted ways (the way's lead) is kept as the first of
# `profiles`, and its first letter in `face` (sphere.letter). `sphere` is the field's own (its standing_in) for every
# title: each one fits. One name changed: "the town's green voice" holds a colour word and is written "the town's
# land voice" (land.json's ladder_titles still says the old name; see the comment on it).
#
# Statuses here are rung titles, kept for life once reached, so lasts="life", except the first-team player, whose
# drafted ages end at 50 and whose place in the side fades in the years given. Profiles: every title is open to more
# than one temperament; they are tendencies, never walls. `needs` brackets only names that are catalogue titles or
# perks (perks_titles/) or titles of this file. Three of the five steps land-ways.py reuses are not in perks_titles/
# but in the packs' catalogues ("stage manager", "community observer", "master craftsperson"), so the needs that
# follow them say the step in words, unbracketed.

_TITLES_LAND = [
  # ---- way "allotment" (W G), sphere gather
  # way "allotment", rung 1 (a plot)
  dict(name="plot holder", kind="status", sphere="gather", face="gather.W", ways="",
       profiles=[("W G", "Works the plot every weekend, keeps the paths tidy and shares the surplus over the fence."),
                 ("U", "Keeps a notebook of sowing dates and yields, and tries a new variety every spring."),
                 ("R B", "Wants the biggest crop on the site and is down there at dawn after every frost.")],
       meets="need:belonging+.03 need:competence+.03 res:health+.02 res:time-.05", lasts="life",
       ages=(16, 100), share=0.03,   # estimate
       say="a plot holder on the allotments",
       gained="a name on the society's waiting list, then a plot that comes free after one to three years",
       lost="never as a record; the plot goes back to the society when it is left unworked, or with a move or failing "
            "knees",
       needs="a name on the allotment society's waiting list and the years to wait; [growing food] helps",
       doors=["the allotment society's meetings and its seed swap",
              "with a meadow of their own: the street's group and its say at the council"]),
  # way "allotment", rung 2 (prizes and seed swaps)
  dict(name="prize grower", kind="status", sphere="gather", face="gather.W", ways="",
       profiles=[("W G", "Grows the old varieties as the site's elders taught, and enters every class at the show."),
                 ("B R", "Grows to beat last year's winner and keeps the secret of the feed."),
                 ("U", "Measures, selects and saves seed from the best plants, year on year.")],
       meets="need:competence+.05 need:meaning+.03 res:time-.03", lasts="life",
       ages=(18, 100), share=0.008,   # estimate
       say="a prize grower",
       gained="a first prize at the society's summer show, won with produce from their own plot",
       lost="never; the show's records keep the win",
       needs="[plot holder]; a season's produce good enough for the show bench",
       doors=["the show's judging table and the growers who keep the old seed"]),
  # way "allotment", rung 3 (chairs the society)
  dict(name="allotment society chair", kind="status", sphere="gather", face="gather.W", ways="",
       profiles=[("W G", "Keeps the waiting list fair, the rent low and the site open to everyone."),
                 ("U B", "Knows the lease, the rules and the council's budget, and argues the site's case on paper."),
                 ("R", "Rallies the members when the site is threatened and leads the work days from the front.")],
       meets="need:meaning+.05 need:belonging+.05 res:ties+.03 res:time-.05", lasts="life",
       ages=(28, 100), share=0.001,   # estimate
       say="the chair of the allotment society",
       gained="a vote of the society's members at the yearly meeting, after years on the plots",
       lost="never as a record; the chair passes on at a yearly meeting or when they step down",
       needs="[plot holder] for years; [prize grower] or long service on the committee; the members' vote",
       doors=["the council's parks and land officer",
              "a say on who gets the next plot"]),

  # ---- way "market_garden" (B G), sphere prod
  # way "market_garden", rung 1 (a stall)
  dict(name="market stallholder", kind="status", sphere="prod", face="prod.B", ways="",
       profiles=[("B G", "Grows what sells, prices it right and sells out before the market packs up."),
                 ("W", "Comes every week whatever the weather, and the regulars count on it."),
                 ("R", "Calls out the prices, chats with everyone and sells as much on charm as on produce.")],
       meets="need:autonomy+.03 need:competence+.03 res:money+.02 res:time-.05", lasts="life",
       ages=(18, 90), share=0.01,   # estimate
       say="a stallholder at the market",
       gained="a pitch at the weekly market and produce that sells out by noon",
       lost="never as a record; the pitch goes when the produce or the early mornings stop",
       needs="[plot of land], [farmer], [savings] or [inheritance] to grow on; [growing food]; the market's pitch fee",
       doors=["the market's regular buyers",
              "with keeping bees: a honey and produce stall, and the market's ear"]),
  # way "market_garden", rung 2 (regular buyers)
  dict(name="market gardener", kind="status", sphere="prod", face="prod.B", ways="",
       profiles=[("B G", "Plans every bed around what the buyers will want, and grows it well."),
                 ("U", "Rotates the beds, keeps the records and stretches the season at both ends."),
                 ("W", "Supplies the same households and kitchens for years and never lets an order fall short.")],
       meets="need:competence+.05 need:autonomy+.03 res:money+.03 res:time-.08 res:health-.02", lasts="life",
       ages=(20, 90), share=0.005,   # estimate
       say="a market gardener",
       gained="buyers who come back every week, and a restaurant or two ordering by the crate",
       lost="never as a record; the buyers drift off when the beds go untended or the land is lost",
       needs="[market stallholder]; land enough for beds that feed a market",
       doors=["the growers' co-operative",
              "a cook who buys the whole harvest"]),
  # way "market_garden", rung 3 (a farm shop)
  dict(name="farm shop owner", kind="status", sphere="prod", face="prod.B", ways="",
       profiles=[("B G", "Runs the shop as a business and fills it from the fields behind it."),
                 ("W", "Keeps the shop a fixture of the town, with fair prices and the same faces behind the till."),
                 ("R U", "Tries something new each season: a field to pick from, a harvest evening, a coffee corner.")],
       meets="need:autonomy+.05 need:meaning+.03 res:money+.05 res:time-.1", lasts="life",
       ages=(28, 90), share=0.001,   # estimate
       say="the owner of a farm shop",
       gained="a shop at the farm gate that the town drives out to on a Saturday",
       lost="never as a record; the shop can close after a bad run of years, a sale or a retirement",
       needs="[market gardener]; [premises of one's own] at the farm gate; [savings] or a loan for the fit-out",
       doors=["the town's food trade",
              "staff of their own"]),

  # ---- way "beekeeping" (G U), sphere prod
  # way "beekeeping", rung 1 (first hive)
  dict(name="beekeeper", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G U", "Watches the bees for hours and learns what each sound from the hive means."),
                 ("W", "Follows the course to the letter, checks the hives every week and never skips a winter feed."),
                 ("R", "Lifts the frames without gloves and loves the roar of a swarm.")],
       meets="need:competence+.03 need:meaning+.03 res:time-.03 res:money-.02", lasts="life",
       ages=(14, 100), share=0.01,   # estimate
       say="a beekeeper",
       gained="the club's course and a first colony that comes through its first winter",
       lost="never as a record; the hives go with a move, a hard winter or an allergy",
       needs="the club's course or [beekeeping]; [hives of one's own], or a hive kept at the club's apiary",
       doors=["the beekeepers' club",
              "with a market garden: a honey and produce stall, and the market's ear"]),
  # way "beekeeping", rung 2 (own honey)
  dict(name="honey maker", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G U", "Moves the hives to the heather and the lime trees, and knows each harvest by its taste."),
                 ("B", "Labels the jars well, prices them right and sells out at the gate."),
                 ("W", "Gives the first jars to the neighbours and the helpers, as the old beekeepers did.")],
       meets="need:competence+.05 need:meaning+.03 res:money+.02 res:time-.03", lasts="life",
       ages=(15, 100), share=0.006,   # estimate
       say="a maker of their own honey",
       gained="a first harvest of honey from their own hives, jarred and given or sold",
       lost="never as a record; the harvests stop when the colonies are lost or given up",
       needs="[beekeeper]; colonies strong enough to give a surplus; an extractor, borrowed or bought",
       doors=["the honey show",
              "orchards and farms that ask for hives"]),
  # way "beekeeping", rung 3 (teaches the course)
  dict(name="beekeeping teacher", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G U", "Teaches the bees' year as it comes, opening a hive in front of every class."),
                 ("W", "Runs the course the same careful way each spring and checks on each new keeper's first winter."),
                 ("R", "Talks bees to anyone who will listen and turns out for every swarm call.")],
       meets="need:meaning+.05 need:belonging+.03 res:ties+.03 res:time-.03", lasts="life",
       ages=(25, 100), share=0.0005,   # estimate
       say="the one who teaches the beekeeping course",
       gained="the club asking them to run the course after years of strong colonies",
       lost="never as a record; the course passes to someone else when they step back",
       needs="[honey maker]; years of colonies that came through; [teaching] helps",
       doors=["every new beekeeper in town",
              "the swarm calls in spring"]),

  # ---- way "keeping_animals" (G W), sphere prod
  # way "keeping_animals", rung 1 (a few hens)
  dict(name="hen keeper", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G W", "Lets the hens out at first light, shuts them in at dusk and knows each one by name."),
                 ("U", "Reads up on breeds and feeds, and keeps a chart of who lays what."),
                 ("B", "Sells the spare eggs at the gate and pays for the feed with them.")],
       meets="need:competence+.02 need:meaning+.02 res:time-.02", lasts="life",
       ages=(8, 100), share=0.08,   # estimate
       say="a keeper of hens",
       gained="a few hens in the yard, fed and shut in every night, and eggs on the table",
       lost="never as a record; the hens go with a move, a fox or old age",
       needs="a yard or garden where hens are allowed, and a coop",
       doors=["the neighbours who keep animals",
              "the vet"]),
  # way "keeping_animals", rung 2 (a flock)
  dict(name="smallholder", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G W", "Works the field through every season and stays up all night in the lambing shed."),
                 ("B", "Sells the lambs and the fleeces and keeps the books so the field pays its way."),
                 ("U", "Learns everything about the breed and keeps a flock book back to the first ewe.")],
       meets="need:competence+.05 need:meaning+.05 need:autonomy+.03 res:time-.08 res:health-.02", lasts="life",
       ages=(18, 100), share=0.01,   # estimate
       say="a smallholder",
       gained="a flock of goats or sheep on a field of their own, through the lambing and the winters",
       lost="never as a record; the flock goes when the field, the money or the strength runs out",
       needs="[hen keeper] or [handling animals]; [plot of land], [farmer] or [inheritance] for a field; [savings] for "
             "the first flock",
       doors=["the agricultural show",
              "with the sports field: the town's show and field day"]),
  # way "keeping_animals", rung 3 (judges at the show)
  dict(name="show judge", kind="status", sphere="prod", face="prod.G", ways="",
       profiles=[("G W", "Judges by the old standard of the breed, slowly, with a hand on every animal."),
                 ("U", "Knows the breed standards by heart and can explain every placing."),
                 ("B", "Is courted by breeders who want the prize, and gives it only to the best animal.")],
       meets="need:meaning+.05 need:competence+.05 res:ties+.03", lasts="life",
       ages=(30, 100), share=0.001,   # estimate
       say="a judge at the show",
       gained="the show committee's invitation, after years of their animals placing at the show",
       lost="never as a record; the invitations stop when they step down or the show ends",
       needs="[smallholder] for years, with animals that placed at the show; the show committee's invitation",
       doors=["the show committee",
              "breeders who ask their eye"]),

  # ---- way "regen_farming" (U G), sphere learn
  # way "regen_farming", rung 1 (a trial field)
  dict(name="trial farmer", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U G", "Digs soil pits, counts worms and measures the trial field against the old ones."),
                 ("B", "Wants to know if it cuts the cost of inputs, and keeps the figures to prove it."),
                 ("W", "Runs the trial with the farmers' group, so everyone can learn from the results.")],
       meets="need:competence+.05 need:meaning+.03 res:money-.03 res:time-.05", lasts="life",
       ages=(20, 90), share=0.002,   # estimate
       say="a farmer trying a new way with the soil",
       gained="a field taken off the old rotation and measured for two or three years",
       lost="never as a record; the trial ends if the field goes back to the old rotation",
       needs="[farmer], [plot of land] or [inheritance]; a field that can be spared for a few years",
       doors=["the farmers' discussion group",
              "the college's field researcher"]),
  # way "regen_farming", rung 2 (yields hold)
  dict(name="soil farmer", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U G", "Reads the soil like a book, and five years of records show the change."),
                 ("W", "Holds to the new way through two dry years when the neighbours went back."),
                 ("B", "Farms the whole place the new way because the margins are better.")],
       meets="need:competence+.05 need:meaning+.05 need:autonomy+.03 res:time-.05", lasts="life",
       ages=(24, 90), share=0.001,   # estimate
       say="a farmer of the soil",
       gained="yields that hold for five years or more without the old inputs, shown in the record",
       lost="never as a record; the change can fade if the land is sold or let to someone else",
       needs="[trial farmer]; years of records on the trial field",
       doors=["the college's trials",
              "with animals kept: a farm others visit to learn from"]),
  # way "regen_farming", rung 3 (others copy it)
  dict(name="model farmer", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U G", "Opens the gate to anyone who asks and shows them the pits, the records and the hedges."),
                 ("W", "Hosts the farm walks, feeds the visitors and answers every question twice."),
                 ("R", "Takes the story to every meeting in the region, with a spade and a jar of soil.")],
       meets="need:meaning+.08 need:belonging+.03 res:ties+.05 res:time-.05", lasts="life",
       ages=(32, 95), share=0.0002,   # estimate
       say="a farmer others copy",
       gained="neighbours and visitors who change their own fields after walking theirs",
       lost="never; the farm stays the one others learned from",
       needs="[soil farmer] for years; neighbours willing to walk the fields",
       doors=["farm walks that fill a bus",
              "the college's lecture hall"]),

  # ---- way "land_dealing" (B U), sphere comm
  # way "land_dealing", rung 1 (a first field)
  dict(name="landholder", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B U", "Studies the auction lists for months and buys the field that others overlooked."),
                 ("W", "Buys back a field that once belonged to the family and means to keep it."),
                 ("G", "Buys a field to have land of their own underfoot, and walks it every week.")],
       meets="need:safety+.03 need:autonomy+.03 res:money-.05", lasts="life",
       ages=(21, 110), share=0.02,   # estimate
       say="the owner of a field",
       gained="a first field bought at auction or from a neighbour, with savings or an inheritance",
       lost="never as a record; the field can be sold, or lost to a debt",
       needs="[savings], [inheritance] or the [family business] behind them; [good credit] for a loan",
       doors=["the land auctions",
              "the bank's lending manager"]),
  # way "land_dealing", rung 2 (rents)
  dict(name="landlord of fields", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B U", "Sets the rents by the market and reads every lease twice."),
                 ("W", "Lets to the same farming families for years at a fair rent."),
                 ("G", "Lets the fields to tenants who care for the hedges and the soil, and checks that they do.")],
       meets="need:safety+.03 need:autonomy+.03 res:money+.05", lasts="life",
       ages=(25, 110), share=0.005,   # estimate
       say="a landlord of fields",
       gained="tenants who rent their fields and pay on time, year after year",
       lost="never as a record; the rents stop when the fields are sold",
       needs="[landholder]; more than one field, and tenants who will take them",
       doors=["the farmers who rent",
              "with water shares: the valley's water and land, much power and much blame"]),
  # way "land_dealing", rung 3 (the town's big landowner)
  dict(name="the town's big landowner", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B U", "Has bought field by field for years and knows the value of every hedge."),
                 ("W", "Holds the land the way an old family holds it, as something to pass on whole."),
                 ("R", "Buys boldly whenever a field comes up, and the whole town talks about it.")],
       meets="need:autonomy+.05 need:safety+.05 res:money+.08 res:ties-.03", lasts="life",
       ages=(40, 110), share=0.0005,   # estimate
       say="the town's big landowner",
       gained="more of the town's land than anyone else, field by field over fifteen years or more",
       lost="never as a record; the standing goes with the land if it is sold off or split",
       needs="[landlord of fields] for years; [savings] or [good credit] enough to keep buying",
       doors=["the council's planning table",
              "every buyer who wants land in the town"]),

  # ---- way "building_on_land" (B R), sphere comm
  # way "building_on_land", rung 1 (a self-build)
  dict(name="self-builder", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Takes the risk, borrows the money and drives the build to finish on time."),
                 ("U", "Sketches the plans, learns each trade and checks every joist."),
                 ("G", "Builds a home that fits the plot, with wood and stone from close by.")],
       meets="need:autonomy+.05 need:competence+.05 res:money-.08 res:time-.1", lasts="life",
       ages=(22, 90), share=0.01,   # estimate
       say="someone who built their own house",
       gained="planning permission won and a house built on their own plot, lived in at the end",
       lost="never; the house stands as the record",
       needs="[plot of land], [savings] or [inheritance]; planning permission; [building trade] or builders to hire",
       doors=["the builders and the council's planners"]),
  # way "building_on_land", rung 2 (a small scheme)
  dict(name="small builder", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Finds the site, raises the money and sells the homes before the roofs are on."),
                 ("W", "Builds solid homes the street is glad of, and keeps the buyers' trust."),
                 ("U", "Works the numbers on every scheme and knows the planning rules better than the planners.")],
       meets="need:autonomy+.05 need:competence+.05 res:money+.03 res:time-.1 need:safety-.03", lasts="life",
       ages=(28, 85), share=0.002,   # estimate
       say="a small builder",
       gained="a small scheme of a few homes, built and sold or let",
       lost="never as a record; the building stops after a scheme that fails, a slump or retirement",
       needs="[self-builder]; [good credit] and a lender; [builder] or a builder to work with",
       doors=["lenders who back schemes",
              "with a meadow kept: homes in a meadow, the builder people thank"]),
  # way "building_on_land", rung 3 (a developer)
  dict(name="developer", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Takes on a bigger site each time and lives for the deal that closes."),
                 ("U", "Plans whole streets with the planners and gets each one through committee."),
                 ("W", "Builds the homes the town needs and keeps the promises made at the hearings.")],
       meets="need:autonomy+.05 need:meaning+.03 res:money+.08 res:time-.1 res:ties-.02", lasts="life",
       ages=(38, 90), share=0.0005,   # estimate
       say="a developer",
       gained="scheme after scheme built across the town over fifteen years or more",
       lost="never as a record; the schemes stop after a crash, a failed site or retirement",
       needs="[small builder] for years; lenders and land; [founder of a firm] helps",
       doors=["the council's planning committee",
              "the town's big landowners"]),

  # ---- way "field_sports" (R B), sphere gather
  # way "field_sports", rung 1 (plays)
  dict(name="club player", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R B", "Plays every match to win and hates being on the bench."),
                 ("W", "Turns up to every training night, plays where the coach says and helps put the nets up."),
                 ("G", "Plays for the fun of it and the friends in the changing room, whatever the score.")],
       meets="need:belonging+.05 need:competence+.03 res:health+.02 res:time-.05", lasts="life",
       ages=(6, 80), share=0.3,   # estimate
       say="a player for the town's club",
       gained="a place in the club's squad and a first match played",
       lost="never as a record; the playing stops with an injury, a move, a family or age",
       needs="a club within reach and the season's fees; [keeping fit] helps",
       doors=["the club's regulars and its coach"]),
  # way "field_sports", rung 2 (the first team)
  # lasts 12: a first-team stretch; the drafted ages end it
  dict(name="first-team player", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R B", "Fought for the place in the side and plays every match as if it might be taken away."),
                 ("W", "Is the reliable one the captain can put anywhere on the field."),
                 ("U", "Studies the other sides and the set pieces, and reads the game a step ahead.")],
       meets="need:competence+.05 need:meaning+.03 need:belonging+.03 res:time-.08 res:health-.02", lasts=12,
       ages=(15, 50), share=0.05,   # estimate
       say="a first-team player",
       gained="picked for the first team after seasons of matches and training",
       lost="losing the place to a younger player, an injury, a move, slowing down with age",
       needs="[club player] for seasons; [keeping fit]; picked before the first team's age limit",
       doors=["the league's matches",
              "with animals kept: the town's show and field day"]),

  # ---- way "field_events" (R B), sphere arts
  # way "field_events", rung 1 (helps out)
  dict(name="fair volunteer", kind="status", sphere="arts", face="arts.R", ways="",
       profiles=[("R B", "Loves the rush of the weekend, from the first tent peg to the last van out."),
                 ("W", "Signs up for the shifts no one else wants and stays till the field is clean."),
                 ("G", "Comes for the people and the music, and helps wherever a hand is needed.")],
       meets="need:belonging+.05 need:meaning+.02 res:time-.03", lasts="life",
       ages=(12, 95), share=0.1,   # estimate
       say="a volunteer at the fair",
       gained="a festival weekend worked from setting up to clearing the field",
       lost="never as a record; the weekends stop with a move or a busier life",
       needs="a fair or festival in town and a weekend free for it",
       doors=["the fair committee",
              "the traders and the acts"]),
  # way "field_events", rung 3 (the festival is theirs)
  dict(name="festival director", kind="status", sphere="arts", face="arts.R", ways="",
       profiles=[("R B", "Books the acts, takes the risk on the weather and makes the weekend the town's biggest."),
                 ("W", "Keeps the festival safe, licensed and open to every family in town."),
                 ("U G", "Builds the festival around the town's own land and makers, year after year.")],
       meets="need:meaning+.08 need:autonomy+.05 res:ties+.05 res:time-.1 need:safety-.03", lasts="life",
       ages=(25, 95), share=0.001,   # estimate
       say="the director of the town's festival",
       gained="a festival on the field that comes back year after year with their name on it",
       lost="never as a record; the festival passes on, or ends after a bad year or a lost licence",
       needs="years running a stage at the fair, or [festival organiser] or [events promoter]; [fair volunteer]; the "
             "field's owner and the council's licence",
       doors=["the council's licensing table",
              "the promoters and the sponsors"]),

  # ---- way "wildflower_meadow" (G R), sphere gather
  # way "wildflower_meadow", rung 1 (a corner)
  dict(name="meadow maker", kind="status", sphere="gather", face="gather.G", ways="",
       profiles=[("G R", "Lets a corner go wild and watches what comes up, with no plan but the seeds."),
                 ("U", "Sows a mix chosen for the soil and counts the flowers each summer."),
                 ("W", "Asks the neighbours first, then sows the corner and keeps a tidy edge mown.")],
       meets="need:meaning+.03 need:competence+.02 res:time-.02", lasts="life",
       ages=(10, 100), share=0.05,   # estimate
       say="the maker of a small meadow",
       gained="a corner left unmown and sown, and flowers coming back the next summer",
       lost="never as a record; the corner goes back to lawn with a move or a new owner",
       needs="a garden, a yard corner or a shared patch that can be left unmown",
       doors=["the bee people",
              "with an allotment plot: the street's group and its say at the council"]),
  # way "wildflower_meadow", rung 2 (the street's verges)
  dict(name="verge keeper", kind="status", sphere="gather", face="gather.G", ways="",
       profiles=[("G R", "Talks the council out of mowing and gets the whole street sowing."),
                 ("W", "Sets up a rota, writes to the council and keeps the verges safe at the corners."),
                 ("U", "Keeps the street's flower count and sends it to the council each year.")],
       meets="need:belonging+.05 need:meaning+.05 res:ties+.03 res:time-.03", lasts="life",
       ages=(14, 100), share=0.005,   # estimate
       say="the keeper of the street's verges",
       gained="the council's leave to stop mowing the verges, and the neighbours sowing them",
       lost="never as a record; the verges go back to mowing if the council changes its mind or the street loses "
            "interest",
       needs="[meadow maker]; the council's leave and neighbours who will sow; [organising people] helps",
       doors=["the council's parks officer",
              "with a builder's scheme: homes in a meadow, the builder people thank"]),
  # way "wildflower_meadow", rung 3 (the town's meadows)
  dict(name="town meadow lead", kind="status", sphere="gather", face="gather.G", ways="",
       profiles=[("G R", "Sees the whole town as one meadow waiting, and talks every park keeper into it."),
                 ("U W", "Writes the plan for the parks and verges and shows the counts at every meeting."),
                 ("B", "Wins the budget for it by showing how much the mowing costs.")],
       meets="need:meaning+.08 need:belonging+.03 res:ties+.05 res:time-.05", lasts="life",
       ages=(25, 100), share=0.0005,   # estimate
       say="the one who leads the town's meadows",
       gained="the town's parks and verges turned to meadow on their plan, with the flower count to show it",
       lost="never as a record; the role passes on when they step back or the council changes the plan",
       needs="[verge keeper] for years; the council's parks officer on side; [voice at the town hall] helps",
       doors=["the council's land board",
              "the schools that come to count"]),

  # ---- way "trail_running" (R G), sphere gather
  # way "trail_running", rung 1 (own routes)
  dict(name="trail runner", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R G", "Runs the wood in all weathers, off the paths whenever a new way looks good."),
                 ("U", "Maps every route and times each one, week after week."),
                 ("W", "Runs with the club's group on the same night each week and waits for the slowest.")],
       meets="need:autonomy+.03 need:competence+.03 res:health+.03 res:time-.03", lasts="life",
       ages=(12, 90), share=0.05,   # estimate
       say="a trail runner",
       gained="routes of their own through the wood, run or ridden every week through a year",
       lost="never as a record; the running stops with an injury, a move or age",
       needs="[keeping fit]; a wood within reach; shoes or a bike fit for the trails",
       doors=["the running or riding club",
              "with a campsite: the outdoor centre"]),
  # way "trail_running", rung 2 (races)
  dict(name="trail racer", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R G", "Races for the climbs and the mud, and chases whoever is just ahead."),
                 ("B", "Trains to a plan to move up the results, race by race."),
                 ("U", "Studies each course in advance and paces it to the minute.")],
       meets="need:competence+.05 need:meaning+.03 res:health+.02 res:time-.05 res:money-.02", lasts="life",
       ages=(14, 85), share=0.015,   # estimate
       say="a trail racer",
       gained="a first trail race finished, then a place in the club's results",
       lost="never as a record; the racing stops with an injury, a busier life or slowing with age",
       needs="[trail runner]; [keeping fit]; race entry fees",
       doors=["races in other woods",
              "the club's committee"]),
  # way "trail_running", rung 3 (builds the trails)
  dict(name="trail builder", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R G", "Cuts a new line through the wood where the ground says it should go."),
                 ("W", "Gets the landowner's leave, builds to the rules and runs the volunteer days."),
                 ("U", "Plans the drainage and the gradients so the trail lasts for years.")],
       meets="need:meaning+.05 need:competence+.05 res:ties+.03 res:time-.05", lasts="life",
       ages=(22, 85), share=0.001,   # estimate
       say="the one who builds the wood's trails",
       gained="the landowner's leave and trails of their own making that the club runs",
       lost="never; the trails stay as their work",
       needs="[trail racer] or years as a [trail runner]; the landowner's leave; [tools of one's own]",
       doors=["the wood's owner",
              "the trail volunteers"]),

  # ---- way "timber" (W B), sphere prod
  # way "timber", rung 1 (firewood for the house)
  dict(name="woodcutter", kind="status", sphere="prod", face="prod.W", ways="",
       profiles=[("W B", "Takes the turn on the rota, cuts the share and stacks it neatly to dry."),
                 ("G", "Coppices the old way and watches the stools grow back."),
                 ("R", "Loves the saw and the swing of the axe on a cold morning.")],
       meets="need:competence+.03 need:safety+.02 res:health+.02 res:time-.03", lasts="life",
       ages=(16, 90), share=0.03,   # estimate
       say="a woodcutter",
       gained="a winter's firewood cut by the wood's rota and stacked to dry",
       lost="never as a record; the cutting stops with a move, a bad back or a new way of heating the house",
       needs="a place on the wood's rota; [chainsaw ticket], or an axe and the strength for it",
       doors=["the woodsmen of the rota",
              "the wood's owner"]),
  # way "timber", rung 2 (sells cords)
  dict(name="firewood seller", kind="status", sphere="prod", face="prod.W", ways="",
       profiles=[("W B", "Sells honest cords, seasoned and full, to the same households every autumn."),
                 ("U", "Knows each kind of wood and how long it needs to dry, and sells it by the season."),
                 ("G", "Sells only what the wood can spare and plants back what is cut.")],
       meets="need:competence+.03 need:autonomy+.03 res:money+.02 res:time-.05", lasts="life",
       ages=(18, 90), share=0.005,   # estimate
       say="a seller of firewood",
       gained="cords sold to the same households every autumn",
       lost="never as a record; the selling stops when the wood or the buyers are lost",
       needs="[woodcutter]; [chainsaw ticket]; a van or trailer and somewhere to season the wood",
       doors=["the timber yard and its buyers"]),
  # way "timber", rung 3 (manages the wood)
  dict(name="woodland manager", kind="status", sphere="prod", face="prod.W", ways="",
       profiles=[("W B", "Keeps the rota fair, the licence in order and the books balanced."),
                 ("G", "Manages the wood for the next hundred years, not the next winter."),
                 ("U", "Plans the felling with the forester and keeps the record of every stand.")],
       meets="need:meaning+.05 need:competence+.05 res:ties+.03 res:time-.05", lasts="life",
       ages=(28, 90), share=0.001,   # estimate
       say="the manager of the wood",
       gained="the wood's owner handing them the rota and the licence after years of good cutting",
       lost="never as a record; the role passes on with a new owner of the wood or when they step back",
       needs="[firewood seller] or years as a [woodcutter]; the wood's owner's trust; [forester] helps",
       doors=["the foresters and the wood's owner",
              "the town's say over its woods"]),

  # ---- way "deer_management" (W R), sphere prot
  # way "deer_management", rung 1 (goes out with the club)
  dict(name="club stalker", kind="status", sphere="prot", face="prot.W", ways="",
       profiles=[("W R", "Follows the plan and the senior stalker's word, and takes only the shot that is right."),
                 ("G", "Goes for the dawn hours in the wood and the animals seen, more than for the shot."),
                 ("U", "Learns the herd's movements and keeps the count for the club.")],
       meets="need:belonging+.03 need:competence+.03 res:time-.05 res:money-.02", lasts="life",
       ages=(16, 85), share=0.01,   # estimate
       say="a member of the hunting club",
       gained="seasons out with the club under a senior stalker, by the plan and the permit",
       lost="never as a record; the seasons stop with a move, age or giving up the hunt",
       needs="[hunting licence]; a club that takes new members; a senior stalker to go out with",
       doors=["the hunting club and the landowners"]),
  # way "deer_management", rung 2 (own permit)
  dict(name="permit holder", kind="status", sphere="prot", face="prot.W", ways="",
       profiles=[("W R", "Keeps to the permit and the season, and reports every animal to the plan."),
                 ("B", "Takes the estates' paid work and sells the venison."),
                 ("G", "Goes out alone in the early hours, at home in the wood.")],
       meets="need:autonomy+.05 need:competence+.03 res:time-.05", lasts="life",
       ages=(18, 85), share=0.005,   # estimate
       say="a holder of their own hunting permit",
       gained="a permit of their own, granted after the club vouches for them",
       lost="never as a record; the permit lapses if it is not renewed, or is taken away",
       needs="[club stalker] for seasons; [hunting licence]; the club's word",
       doors=["the estates that need the deer kept down",
              "with foraging: the keeper of an estate's woods and what they give"]),
  # way "deer_management", rung 3 (the wood's ranger)
  dict(name="wood ranger", kind="status", sphere="prot", face="prot.W", ways="",
       profiles=[("W R", "Keeps the wood's plan for every landowner and turns away anyone who breaks it."),
                 ("G", "Watches over the whole wood: the deer, the young trees and the birds."),
                 ("U", "Counts the herd each spring and sets the season's numbers from the count.")],
       meets="need:meaning+.05 need:competence+.05 res:ties+.03 res:time-.08", lasts="life",
       ages=(28, 85), share=0.0005,   # estimate
       say="the wood's ranger",
       gained="the landowners asking them to keep the wood's plan, after years of fair seasons",
       lost="never as a record; the role passes on when they step back or the landowners choose another",
       needs="[permit holder] for years; the landowners' trust",
       doors=["the landowners' table",
              "the council's countryside officer"]),

  # ---- way "forage_guide" (G B), sphere comm
  # way "forage_guide", rung 1 (own baskets)
  dict(name="forager", kind="status", sphere="comm", face="comm.G", ways="",
       profiles=[("G B", "Knows where the best patches are and keeps them quiet."),
                 ("U", "Checks every find against the book and learns one new plant each month."),
                 ("W", "Takes only a little from each patch and leaves the rest.")],
       meets="need:competence+.03 need:autonomy+.02 res:health+.02 res:time-.02", lasts="life",
       ages=(12, 100), share=0.05,   # estimate
       say="a forager",
       gained="baskets of their own from the wood and the hedges, every season of a year",
       lost="never as a record; the baskets stop with a move or a busier life",
       needs="a wood and hedges within reach; a good field guide; [knowing the woods] helps",
       doors=["the foraging society's walks"]),
  # way "forage_guide", rung 2 (leads walks)
  dict(name="foraging guide", kind="status", sphere="comm", face="comm.G", ways="",
       profiles=[("G B", "Runs paid walks that end with a meal from what was found."),
                 ("W", "Teaches the safety rules first and never lets a doubtful find into a basket."),
                 ("U", "Explains every plant's story, its uses and its lookalikes.")],
       meets="need:meaning+.05 need:competence+.03 res:money+.02 res:time-.05", lasts="life",
       ages=(20, 95), share=0.002,   # estimate
       say="a foraging guide",
       gained="walks of their own that people book and pay for, with nobody sick from them",
       lost="never as a record; the walks stop with a move, a lost permission or a bad season",
       needs="[forager] for years; [knowing the woods]; [first-aid certificate] helps",
       doors=["the cooks and the walkers",
              "with forest school: the wood's teacher, paid by schools and visitors"]),
  # way "forage_guide", rung 3 (the restaurants' supplier)
  dict(name="wild food supplier", kind="status", sphere="comm", face="comm.G", ways="",
       profiles=[("G B", "Knows what each kitchen wants and brings it in the week it is best."),
                 ("W", "Supplies the same kitchens every week and never takes more than the woods can give."),
                 ("U", "Keeps a calendar of every patch and what it gives, week by week.")],
       meets="need:autonomy+.05 need:competence+.05 res:money+.03 res:time-.08", lasts="life",
       ages=(25, 95), share=0.0005,   # estimate
       say="the restaurants' wild food supplier",
       gained="kitchens that order from them every week of the season",
       lost="never as a record; the orders stop when a kitchen closes or the patches are lost",
       needs="[foraging guide]; [food hygiene certificate]; the landowners' leave to pick",
       doors=["the town's best kitchens",
              "with a hunting permit: the keeper of an estate's woods and what they give"]),

  # ---- way "forest_school" (U W), sphere learn
  # way "forest_school", rung 1 (helps a session)
  dict(name="forest school helper", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Follows the leader's plan, keeps the fire safe and answers the children's questions."),
                 ("G", "Lets the children dig, climb and get muddy, and joins in."),
                 ("R", "Brings the games, and the stories round the fire that the children ask for again.")],
       meets="need:meaning+.05 need:belonging+.03 res:time-.03", lasts="life",
       ages=(16, 80), share=0.01,   # estimate
       say="a helper at the forest school",
       gained="a year of sessions helped, with the check to work with children cleared",
       lost="never as a record; the helping stops when the clearance lapses or life gets busier",
       needs="[cleared to work with children]; a forest school that takes helpers; [first-aid certificate] helps",
       doors=["the teachers and the parents"]),
  # way "forest_school", rung 2 (runs a group)
  dict(name="forest school leader", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Plans each session around the season and keeps every child safe and busy."),
                 ("G", "Lets the wood lead the session, and the children find their own way into it."),
                 ("R", "Gets the shy ones climbing and the loud ones listening.")],
       meets="need:meaning+.08 need:competence+.05 res:money+.02 res:time-.05", lasts="life",
       ages=(20, 75), share=0.003,   # estimate
       say="a forest school leader",
       gained="the leader training passed and a group of their own that comes back every week",
       lost="never as a record; the group stops when the training lapses or they move on",
       needs="[forest school helper]; the leader training and [first-aid certificate]; [cleared to work with children]",
       doors=["schools that book a term",
              "with foraging: the wood's teacher, paid by schools and visitors"]),
  # way "forest_school", rung 3 (the town's forest school)
  dict(name="forest school head", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Writes the plans, trains the leaders and keeps every school's trust."),
                 ("B", "Builds the forest school into a business with a waiting list."),
                 ("G", "Keeps the wood itself at the heart of it, and plants as much as the children use.")],
       meets="need:meaning+.08 need:autonomy+.03 res:money+.03 res:ties+.03 res:time-.08", lasts="life",
       ages=(28, 75), share=0.0005,   # estimate
       say="the head of the town's forest school",
       gained="the forest school that the town's schools all use, run on their name",
       lost="never as a record; the role passes on when they step back or the wood is lost",
       needs="[forest school leader] for years; [cleared to work with children]; [teaching] or [outdoor instructor] "
             "helps",
       doors=["the town's head teachers",
              "the council's education office"]),

  # ---- way "wildlife_survey" (U W), sphere learn
  # way "wildlife_survey", rung 2 (a square of their own)
  dict(name="survey square holder", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Walks the same route at the same time each season and records everything."),
                 ("G", "Goes for the hours alone in the square, and the hare seen once in three years."),
                 ("R", "Treats each count as a hunt for the rare one, and is out at dawn for it.")],
       meets="need:competence+.05 need:meaning+.05 res:time-.03", lasts="life",
       ages=(14, 100), share=0.005,   # estimate
       say="the holder of a survey square",
       gained="a square of the map of their own, counted every season for three years or more",
       lost="never as a record; the square passes to someone else when the counts stop",
       needs="first counts with the society's observers; a field guide and the patience for it; [finding things out] "
             "helps",
       doors=["the naturalists' society's records",
              "with land rewilded: a nature reserve under their name"]),
  # way "wildlife_survey", rung 3 (the county's recorder)
  dict(name="county recorder", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Checks every record sent in and keeps the county's list true."),
                 ("G", "Knows the county's animals by place and season, from decades out among them."),
                 ("B", "Makes sure the planners and the trusts cannot overlook the record.")],
       meets="need:meaning+.08 need:competence+.05 res:ties+.03 res:time-.05", lasts="life",
       ages=(28, 100), share=0.0002,   # estimate
       say="the county's recorder",
       gained="the society naming them keeper of the county's record for one group of animals",
       lost="never as a record; the role passes to a younger recorder when they step back",
       needs="[survey square holder] for years; the society's trust; [working with data] helps",
       doors=["the trusts and the planners who need the record",
              "every counter in the county"]),

  # ---- way "campsite" (B R), sphere comm
  # way "campsite", rung 1 (a field of tents)
  dict(name="campsite keeper", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Takes the risk of a summer of bookings and fills the field every weekend."),
                 ("W", "Keeps the site clean, safe and quiet after ten."),
                 ("G", "Keeps the field half wild, with a fire pit and no lights.")],
       meets="need:autonomy+.05 res:money+.02 res:time-.08", lasts="life",
       ages=(21, 85), share=0.002,   # estimate
       say="the keeper of a campsite",
       gained="a field of tents licensed and full on the summer weekends",
       lost="never as a record; the site closes with a lost licence, a few wet summers or a sale",
       needs="[plot of land], [savings], [inheritance] or the [family business]; a licence for the field",
       doors=["the visitors and the council",
              "with trail running: the outdoor centre"]),
  # way "campsite", rung 2 (cabins)
  dict(name="cabin host", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Builds another cabin each year the bookings allow."),
                 ("U", "Designs the cabins to stay warm and dry in every season."),
                 ("G", "Builds the cabins from the wood's own timber and keeps them simple.")],
       meets="need:autonomy+.05 need:competence+.03 res:money+.05 res:time-.08", lasts="life",
       ages=(25, 85), share=0.001,   # estimate
       say="a host of cabins in the wood",
       gained="cabins built and booked through the year",
       lost="never as a record; the cabins close with a slump, a sale or retirement",
       needs="[campsite keeper]; [savings] or [good credit] for the build; planning permission",
       doors=["the lenders who back the next cabins"]),
  # way "campsite", rung 3 (the outdoor centre)
  dict(name="outdoor centre owner", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Runs it as a business, with schools booked a year ahead."),
                 ("W", "Keeps every group safe and every instructor trained."),
                 ("U G", "Builds the centre around what the wood and the water can teach.")],
       meets="need:autonomy+.05 need:meaning+.05 res:money+.05 res:time-.1 need:safety-.02", lasts="life",
       ages=(32, 85), share=0.0002,   # estimate
       say="the owner of the outdoor centre",
       gained="an outdoor centre that schools and groups come to every season",
       lost="never as a record; the centre closes after a slump, an accident or a sale",
       needs="[cabin host]; [outdoor instructor] or instructors to hire; [premises of one's own]",
       doors=["schools and youth groups",
              "instructors of their own"]),

  # ---- way "wood_crafts" (U B), sphere arts
  # way "wood_crafts", rung 1 (spoons)
  dict(name="spoon carver", kind="status", sphere="arts", face="arts.U", ways="",
       profiles=[("U B", "Studies the grain, makes each spoon better than the last and sells the best."),
                 ("G", "Carves by the fire from wood found on walks, slowly, for the feel of it."),
                 ("W", "Carves with the group each week and gives every spoon to someone.")],
       meets="need:competence+.05 need:autonomy+.02 res:time-.03", lasts="life",
       ages=(10, 100), share=0.02,   # estimate
       say="a spoon carver",
       gained="spoons and bowls of their own that are used in the kitchen",
       lost="never as a record; the carving stops with a hurt hand or a busier life",
       needs="a carving knife and fresh-cut wood; the carving group or [tools of one's own]",
       doors=["the carving group",
              "with shore finds: a gallery of the land's own things"]),

  # ---- way "wood_guardian" (R W), sphere rule
  # way "wood_guardian", rung 1 (joins the friends)
  dict(name="friend of the wood", kind="status", sphere="rule", face="rule.R", ways="",
       profiles=[("R W", "Turns up to every work day and every walk, and speaks up whenever the wood is threatened."),
                 ("G", "Comes for the wood itself and the first flowers of spring."),
                 ("U", "Learns the wood's history and its trees, and leads the walks on them.")],
       meets="need:belonging+.05 need:meaning+.03 res:time-.02", lasts="life",
       ages=(12, 100), share=0.03,   # estimate
       say="a friend of the wood",
       gained="a year of the friends' walks and work days",
       lost="never as a record; the walks stop with a move or a busier life",
       needs="a wood with a friends' group; a year of its walks and work days",
       doors=["the friends of the wood",
              "with flood watch: the town's voice for its land, a seat at the council's board for the land"]),
  # way "wood_guardian", rung 2 (leads a campaign)
  dict(name="wood campaigner", kind="status", sphere="rule", face="rule.R", ways="",
       profiles=[("R W", "Leads the campaign from the front, with the petition, the hearing and the local paper."),
                 ("U", "Builds the case from the records, the maps and the law, and wins it on paper."),
                 ("B", "Knows which councillor to ask and which deal to make.")],
       meets="need:meaning+.08 need:autonomy+.03 res:ties+.02 res:time-.08 need:safety-.02", lasts="life",
       ages=(16, 100), share=0.005,   # estimate
       say="a campaigner for the wood",
       gained="a campaign they led that brought people to a hearing or won an order to protect the wood",
       lost="never as a record; the campaigning stops when the fight is won or lost and life goes on",
       needs="[friend of the wood]; [campaigning] or [organising people]; [public speaking] helps",
       doors=["the council's planning hearings",
              "the local paper"]),
  # way "wood_guardian", rung 3 (the town's voice for its land)
  # renamed from "the town's green voice" (a colour word); land.json's ladder_titles still says the old name
  dict(name="the town's land voice", kind="status", sphere="rule", face="rule.R", ways="",
       profiles=[("R W", "Speaks for the town's land at every hearing, and is first called when a field is threatened."),
                 ("U", "Knows every plan, every protection and every map, and is asked because they are right."),
                 ("G", "Speaks for the land itself, the trees, the soil and the water, more than for any side.")],
       meets="need:meaning+.08 need:belonging+.03 res:ties+.05 res:time-.05", lasts="life",
       ages=(25, 100), share=0.0005,   # estimate
       say="the town's voice for its land",
       gained="the council and the town asking them first whenever its land is in question",
       lost="never as a record; the standing fades when they step back or the town stops asking",
       needs="[wood campaigner] for years; [voice at the town hall] or [good name in town]",
       doors=["the council's land board",
              "every campaign for a wood or a field"]),

  # ---- way "rewilding" (G U), sphere learn
  # way "rewilding", rung 1 (a corner)
  dict(name="rewilder", kind="status", sphere="learn", face="learn.G", ways="",
       profiles=[("G U", "Lets a corner go, plants only what is missing and counts what comes back."),
                 ("R", "Pulls out the fences and the tidy edges and lets it run wild."),
                 ("W", "Works to the trust's plan, with the neighbours' leave.")],
       meets="need:meaning+.05 need:competence+.02 res:time-.03", lasts="life",
       ages=(16, 100), share=0.02,   # estimate
       say="a rewilder",
       gained="a corner of land let go and planted where needed, with new life counted in it",
       lost="never as a record; the corner goes back to tidy with a move or a new owner",
       needs="a corner of land to let go; the wildlife trust's advice helps",
       doors=["the wildlife trust",
              "with a survey square: a nature reserve under their name"]),
  # way "rewilding", rung 2 (a field returned)
  dict(name="land restorer", kind="status", sphere="learn", face="learn.G", ways="",
       profiles=[("G U", "Returns a whole field to wild and keeps the record of what returns."),
                 ("B", "Finds the grants and the landowners, and makes each field pay its way."),
                 ("W", "Keeps the neighbours on side, the paths open and the plan agreed.")],
       meets="need:meaning+.05 need:competence+.05 res:time-.05", lasts="life",
       ages=(22, 100), share=0.002,   # estimate
       say="a restorer of land",
       gained="a whole field returned to wild, with the count to show what has come back",
       lost="never; the field and its record stay",
       needs="[rewilder]; a landowner who offers a field, or [plot of land]; the trust's grants",
       doors=["landowners who offer a field",
              "the trust's grants"]),
  # way "rewilding", rung 3 (a reserve)
  dict(name="reserve founder", kind="status", sphere="learn", face="learn.G", ways="",
       profiles=[("G U", "Watches the reserve come back to life over decades, and lets it lead."),
                 ("W", "Sets up the trust that will keep it safe after them."),
                 ("R", "Fought for every field of it, and opens the gate to everyone.")],
       meets="need:meaning+.1 need:autonomy+.03 res:ties+.05 res:time-.05", lasts="life",
       ages=(35, 100), share=0.0002,   # estimate
       say="the founder of a nature reserve",
       gained="a reserve declared on land they brought back, open to visitors",
       lost="never; the reserve keeps their name",
       needs="[land restorer] for years; land brought back, and the declaration of the council or a trust",
       doors=["the reserve's wardens and visitors",
              "the council's land board"]),

  # ---- way "angling_club" (W G), sphere gather
  # way "angling_club", rung 1 (a licence)
  dict(name="angler", kind="status", sphere="gather", face="gather.W", ways="",
       profiles=[("W G", "Fishes by the club's rules and the season, and puts most of the catch back."),
                 ("U", "Studies the water, the weather and the flies, and keeps a log of every trip."),
                 ("R", "Fishes for the big one and tells the story at the club for years.")],
       meets="need:autonomy+.03 need:belonging+.02 res:time-.03", lasts="life",
       ages=(8, 100), share=0.1,   # estimate
       say="an angler",
       gained="a rod licence and a season of fishing with the club",
       lost="never as a record; the fishing stops with a move or age",
       needs="[fishing licence]; a rod and the club's fees",
       doors=["the angling club",
              "with water samples: a seat on the river trust"]),
  # way "angling_club", rung 2 (the club's matches)
  dict(name="match angler", kind="status", sphere="gather", face="gather.W", ways="",
       profiles=[("W G", "Fishes every match on the club's calendar, rain or shine."),
                 ("B R", "Fishes to win the match on weight, and wants the best spot on the bank."),
                 ("U", "Plans the bait and the tactics for each water like a puzzle.")],
       meets="need:competence+.05 need:belonging+.03 res:time-.05", lasts="life",
       ages=(10, 100), share=0.02,   # estimate
       say="a match angler",
       gained="a place in the club's matches and a weight that counts in the results",
       lost="never as a record; the matches stop with a move, age or a busier life",
       needs="[angler]; [fishing licence]; the club's match fees",
       doors=["matches on other waters"]),
  # way "angling_club", rung 3 (the club's bailiff or chair)
  dict(name="club bailiff", kind="status", sphere="gather", face="gather.W", ways="",
       profiles=[("W G", "Walks the bank, checks the licences and keeps the water fair for every member."),
                 ("U", "Keeps the club's records of the fish and the water, and the lease up to date."),
                 ("B", "Runs the club's money and settles the lease with the landowners.")],
       meets="need:meaning+.05 need:belonging+.05 res:ties+.03 res:time-.05", lasts="life",
       ages=(25, 100), share=0.002,   # estimate
       say="the angling club's bailiff or chair",
       gained="the members' vote to keep the club's water or to chair the club",
       lost="never as a record; the post passes on at a yearly meeting or when they step down",
       needs="[angler] for years, often [match angler]; the members' vote",
       doors=["the landowners who lease the bank",
              "the river trust"]),

  # ---- way "wild_swimming" (R W), sphere gather
  # way "wild_swimming", rung 1 (first cold swims)
  dict(name="cold-water swimmer", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R W", "Gets in while the others hesitate, and comes every morning with the group."),
                 ("G", "Swims for the water, the mist and the birds, and floats as much as swims."),
                 ("U", "Reads up on the cold and the body, and times every swim.")],
       meets="need:belonging+.03 need:autonomy+.02 res:health+.03 res:time-.02", lasts="life",
       ages=(14, 100), share=0.05,   # estimate
       say="a cold-water swimmer",
       gained="a first season of swims with the morning group",
       lost="never as a record; the swims stop with a move, a health worry or a busier life",
       needs="[swimming]; a lake, river or shore with a morning group",
       doors=["the morning swimmers"]),
  # way "wild_swimming", rung 2 (every season)
  dict(name="all-season swimmer", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R W", "Swims right through midwinter, every week, because the group does."),
                 ("G", "Swims as the water changes, and knows every season by its feel."),
                 ("B", "Does it to be tough, and counts the coldest swim as a win.")],
       meets="need:competence+.03 need:belonging+.05 res:health+.03 res:time-.03", lasts="life",
       ages=(16, 100), share=0.015,   # estimate
       say="a swimmer in every season",
       gained="a whole year of swims, the midwinter one included",
       lost="never as a record; the winter swims stop with age or a health worry",
       needs="[cold-water swimmer]; a whole year in the water; good health",
       doors=["the midwinter swim",
              "with the river brought back: the swim the river came back for, the town's summer gathering"]),
  # way "wild_swimming", rung 3 (leads the group)
  dict(name="swim group lead", kind="status", sphere="gather", face="gather.R", ways="",
       profiles=[("R W", "Leads the swims, sets the rules and gets every newcomer safely in and out."),
                 ("U", "Checks the water, the weather and the flow before every swim."),
                 ("G", "Keeps the group open, with a hot drink after and room for anyone.")],
       meets="need:meaning+.05 need:belonging+.05 res:ties+.03 res:time-.03", lasts="life",
       ages=(22, 100), share=0.002,   # estimate
       say="the one who leads the swimming group",
       gained="the group asking them to keep the times, the safety rules and the newcomers",
       lost="never as a record; the lead passes on when they step back or the training lapses",
       needs="[all-season swimmer]; [lifeguard qualification] or water safety training; [first-aid certificate]",
       doors=["every newcomer to the water",
              "the cafe and the lifeguards"]),

  # ---- way "sailing" (U R), sphere gather
  # way "sailing", rung 1 (lessons)
  dict(name="learner sailor", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U R", "Learns the knots and the wind quickly, and wants to be out alone."),
                 ("W", "Follows the instructor exactly and passes every step of the course."),
                 ("G", "Loves the quiet of the water and the feel of the boat in the wind.")],
       meets="need:competence+.03 need:autonomy+.02 res:money-.02 res:time-.03", lasts="life",
       ages=(8, 90), share=0.05,   # estimate
       say="a learner sailor",
       gained="a course of lessons passed at the sailing club",
       lost="never as a record; the sailing stops with a move or when the lessons end",
       needs="[swimming]; a sailing club within reach and the course fees",
       doors=["the club's boats and crews"]),
  # way "sailing", rung 2 (races)
  dict(name="club racer", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U R", "Reads the wind shifts and tunes the boat for every race."),
                 ("B", "Sails to win the series and keeps track of every rival's points."),
                 ("W", "Crews for the same skipper every week and never misses a race.")],
       meets="need:competence+.05 need:belonging+.03 res:money-.03 res:time-.05", lasts="life",
       ages=(10, 90), share=0.01,   # estimate
       say="a club racer",
       gained="a season of the club's races sailed and a place in the results",
       lost="never as a record; the racing stops with a move, the boat sold or age",
       needs="[learner sailor]; [boat handling]; [boat of one's own] or a crew place",
       doors=["regattas on other waters",
              "with a shore business: the harbour's own business"]),
  # way "sailing", rung 3 (commodore or instructor)
  dict(name="commodore", kind="status", sphere="gather", face="gather.U", ways="",
       profiles=[("U R", "Leads the club and teaches the next sailors to race."),
                 ("W", "Keeps the club's rules, the safety boat and the yearly meeting in order."),
                 ("B", "Runs the club like a business and finds the money for the new pontoon.")],
       meets="need:meaning+.05 need:belonging+.05 res:ties+.05 res:time-.05", lasts="life",
       ages=(25, 95), share=0.001,   # estimate
       say="the club's commodore or instructor",
       gained="the members' vote, or the club's instructor badge, after years on the water",
       lost="never as a record; the post passes on at a yearly meeting, or the instructor's badge lapses",
       needs="[club racer] for years, or [boat handling] and the club's instructor course; the members' vote",
       doors=["the club's committee",
              "the harbour authority"]),

  # ---- way "water_testing" (U W), sphere learn
  # way "water_testing", rung 1 (monthly samples)
  dict(name="water sampler", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Takes the samples at the same place on the same day each month."),
                 ("G", "Walks the river for the samples and notices every change on the bank."),
                 ("R", "Wants to find the trouble, and samples every outflow.")],
       meets="need:meaning+.03 need:competence+.03 res:time-.02", lasts="life",
       ages=(14, 100), share=0.005,   # estimate
       say="a water sampler",
       gained="the trust's training and a year of monthly samples sent in",
       lost="never as a record; the samples stop with a move or a busier life",
       needs="the river trust's training and kit; a stretch of river within reach",
       doors=["the river trust",
              "with the angling club: a seat on the river trust"]),
  # way "water_testing", rung 2 (finds a source)
  dict(name="river detective", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Follows the readings upstream, sample by sample, until the source is clear."),
                 ("R", "Will not let it go, and takes the evidence to anyone who will act."),
                 ("B", "Knows whom to tell and when, and makes sure the firm upstream answers for it.")],
       meets="need:meaning+.08 need:competence+.05 res:ties-.02 res:time-.05", lasts="life",
       ages=(16, 100), share=0.001,   # estimate
       say="the one who found where the river was fouled",
       gained="a source of the trouble traced in their own record and confirmed by the trust",
       lost="never; the finding stays in the record",
       needs="[water sampler] for years; [finding things out] helps",
       doors=["the council's officers",
              "the firm upstream"]),
  # way "water_testing", rung 3 (the town's water expert)
  dict(name="water expert", kind="status", sphere="learn", face="learn.U", ways="",
       profiles=[("U W", "Knows the river's record better than anyone, and is asked because the facts are right."),
                 ("G", "Speaks for the river itself, its fish and its banks."),
                 ("R", "Speaks up at every hearing and in every paper when the river is at risk.")],
       meets="need:meaning+.08 need:belonging+.03 res:ties+.05 res:time-.03", lasts="life",
       ages=(25, 100), share=0.0003,   # estimate
       say="the town's water expert",
       gained="the town and its papers asking them first whenever the river is in question",
       lost="never as a record; the standing fades when they step back or the town stops asking",
       needs="[river detective]; years of the record; [public speaking] helps",
       doors=["the council's land board",
              "the river trust's board"]),

  # ---- way "flood_warden" (W U), sphere prot
  # way "flood_warden", rung 1 (warden for the street)
  dict(name="street flood warden", kind="status", sphere="prot", face="prot.W", ways="",
       profiles=[("W U", "Knows every door on the street, who needs help first and where the sandbags are."),
                 ("G", "Watches the river and the rain, and knows the street's water like a neighbour."),
                 ("R", "Is first out in the rain, knocking on doors when the alert comes.")],
       meets="need:meaning+.05 need:belonging+.05 res:time-.02", lasts="life",
       ages=(18, 95), share=0.01,   # estimate
       say="the street's flood warden",
       gained="the council's training and a street that knows to call them when the river rises",
       lost="never as a record; the role passes on with a move or when the training lapses",
       needs="the council's warden training; a street that floods; [first-aid certificate] helps",
       doors=["the council's flood officer",
              "with the friends of the wood: a seat at the council's board for the land"]),
  # way "flood_warden", rung 2 (for the ward)
  dict(name="ward flood warden", kind="status", sphere="prot", face="prot.W", ways="",
       profiles=[("W U", "Runs the ward's wardens with plans, drills and a phone list."),
                 ("R", "Took charge on the flood night, and the others followed."),
                 ("G", "Keeps the wardens together as neighbours, with a meal after every drill.")],
       meets="need:meaning+.05 need:competence+.05 res:ties+.03 res:time-.03", lasts="life",
       ages=(22, 95), share=0.002,   # estimate
       say="the ward's flood warden",
       gained="a flood night handled well and the wardens of the ward following their lead",
       lost="never as a record; the role passes on with a move or when the training lapses",
       needs="[street flood warden]; a flood night handled well; [organising people] helps",
       doors=["the ward councillor",
              "the rescue volunteers"]),
  # way "flood_warden", rung 3 (on the town's flood board)
  dict(name="flood board member", kind="status", sphere="prot", face="prot.W", ways="",
       profiles=[("W U", "Reads every plan and asks every question at the flood board."),
                 ("G", "Pushes for the fixes upstream: wetlands, ponds and old bends given back."),
                 ("B", "Wins the budget for the ward's defences.")],
       meets="need:meaning+.05 need:belonging+.03 res:ties+.05 res:time-.03", lasts="life",
       ages=(30, 95), share=0.0005,   # estimate
       say="a member of the town's flood board",
       gained="a seat on the flood board offered after years of the ward's watch",
       lost="never as a record; the seat passes on when the term ends or they step down",
       needs="[ward flood warden] for years; the board's offer of a seat",
       doors=["the town's flood plans",
              "the council's chamber"]),

  # ---- way "water_rights" (W B), sphere rule
  # way "water_rights", rung 1 (a share)
  dict(name="water shareholder", kind="status", sphere="rule", face="rule.W", ways="",
       profiles=[("W B", "Takes only the share, on the turn, and keeps the records straight."),
                 ("G", "Uses the water as the land needs it and leaves the stream alive."),
                 ("U", "Knows the old agreements and the measurements by heart.")],
       meets="need:safety+.03 need:belonging+.03", lasts="life",
       ages=(21, 110), share=0.01,   # estimate
       say="a holder of a share of the water",
       gained="land by the water and a share of its drawing written down",
       lost="never as a record; the share can be lost if unused for years, or goes with the land",
       needs="[plot of land], [farmer] or [inheritance]; land by the water",
       doors=["the farmers on the rota",
              "with fields to let: the valley's water and land, much power and much blame"]),
  # way "water_rights", rung 2 (on the water rota)
  dict(name="water rota keeper", kind="status", sphere="rule", face="rule.W", ways="",
       profiles=[("W B", "Keeps the turns fair and the book open for anyone to check."),
                 ("U", "Measures the flow and plans the turns around it."),
                 ("R", "Stands firm against the farmer who takes more than a turn.")],
       meets="need:meaning+.05 need:belonging+.03 res:ties+.03 res:time-.03", lasts="life",
       ages=(25, 110), share=0.002,   # estimate
       say="the keeper of the water rota",
       gained="the farmers trusting them to keep the turns fair through a dry summer",
       lost="never as a record; the rota passes on when they step down or lose the farmers' trust",
       needs="[water shareholder]; the farmers' trust; [settling disputes] helps",
       doors=["the water board"]),
  # way "water_rights", rung 3 (chairs the water board)
  dict(name="water board chair", kind="status", sphere="rule", face="rule.W", ways="",
       profiles=[("W B", "Chairs the board by the old agreements and the new rules alike."),
                 ("U", "Plans the valley's water for the dry years still to come."),
                 ("G", "Speaks for the river as one of the users, with a share of its own.")],
       meets="need:meaning+.05 need:autonomy+.03 res:ties+.05 res:time-.05", lasts="life",
       ages=(35, 110), share=0.0002,   # estimate
       say="the chair of the water board",
       gained="the board's vote, after years of fair rotas",
       lost="never as a record; the chair passes on at the board's vote",
       needs="[water rota keeper] for years; the board's vote",
       doors=["the council's chamber",
              "every farmer who draws water"]),

  # ---- way "catch_to_sell" (B U), sphere prod
  # way "catch_to_sell", rung 1 (sells the catch)
  dict(name="fish seller", kind="status", sphere="prod", face="prod.B", ways="",
       profiles=[("B U", "Knows what each day's market will pay, and fishes for it."),
                 ("W", "Keeps to the licence and the limits, and sells only fresh fish."),
                 ("R", "Goes out in weather others stay in, for the best price on the quay.")],
       meets="need:autonomy+.05 need:competence+.03 res:money+.02 res:time-.05 res:health-.02", lasts="life",
       ages=(16, 85), share=0.005,   # estimate
       say="a seller of their own catch",
       gained="a licence and a catch that sells at the morning market",
       lost="never as a record; the selling stops when the licence lapses or the catch fails",
       needs="[fishing licence], [commercial fisher] or [boat of one's own]; [food hygiene certificate] helps",
       doors=["the fish market's traders"]),
  # way "catch_to_sell", rung 2 (a boat or ponds of their own)
  dict(name="boat owner", kind="status", sphere="prod", face="prod.B", ways="",
       profiles=[("B U", "Paid for the boat from years of catches, and runs it to pay its way."),
                 ("W", "Keeps the boat safe, the crew paid and the licence clean."),
                 ("G", "Fishes the old grounds the old way, as the family did.")],
       meets="need:autonomy+.05 need:competence+.05 res:money+.03 res:time-.08 need:safety-.02", lasts="life",
       ages=(20, 90), share=0.002,   # estimate
       say="the owner of a fishing boat or ponds",
       gained="a boat or ponds of their own, paid for out of years of catches",
       lost="never as a record; the boat or the ponds are sold, lost to a debt or handed on",
       needs="[fish seller]; [savings] or [good credit]; [boat handling] or a [share in a fishing boat] first",
       doors=["crew of their own",
              "buyers who take the whole catch"]),
  # way "catch_to_sell", rung 3 (the market's main supplier)
  dict(name="chief fish supplier", kind="status", sphere="prod", face="prod.B", ways="",
       profiles=[("B U", "Lands the most fish in the market, and sets the price."),
                 ("W", "Keeps the kitchens supplied whatever the weather, and never gives short weight."),
                 ("G", "Fishes and farms with care so the stock lasts for the next generation.")],
       meets="need:autonomy+.05 need:meaning+.03 res:money+.08 res:time-.08", lasts="life",
       ages=(28, 90), share=0.0003,   # estimate
       say="the market's main supplier of fish",
       gained="more of the market's fish from their boats or ponds than anyone else's",
       lost="never as a record; the lead passes on when the boats or the ponds are sold",
       needs="[boat owner] for years; crew of their own",
       doors=["the town's kitchens and shops",
              "the harbour's own business"]),

  # ---- way "shore_business" (B R), sphere comm
  # way "shore_business", rung 1 (a summer stall)
  dict(name="summer stall keeper", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Takes the risk on the summer and sells whatever the crowds want."),
                 ("W", "Opens at the same hour every day of the season and knows the regulars."),
                 ("G", "Sells food and finds from the shore, simple and fresh.")],
       meets="need:autonomy+.05 res:money+.02 res:time-.08", lasts="life",
       ages=(16, 85), share=0.005,   # estimate
       say="the keeper of a summer stall by the water",
       gained="a summer stall licensed by the water and a season that pays its way",
       lost="never as a record; the stall stops with a wet summer, a lost licence or a move",
       needs="[savings], [inheritance] or the [family business]; a trading licence by the water",
       doors=["the visitors and the other traders"]),
  # way "shore_business", rung 2 (a year-round place)
  dict(name="shore cafe owner", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Turns the stall into a year-round business and bets on the winter."),
                 ("W", "Keeps it open through the winter for the swimmers and the walkers."),
                 ("U", "Keeps the books, the stock and the staff rota tight.")],
       meets="need:autonomy+.05 need:belonging+.03 res:money+.03 res:time-.1", lasts="life",
       ages=(21, 85), share=0.002,   # estimate
       say="the owner of a place by the water",
       gained="a year-round cafe, kiosk or boat hire that stays open through the winter",
       lost="never as a record; the place closes with a slump, a lost lease or a sale",
       needs="[summer stall keeper]; a lease by the water; [food hygiene certificate]",
       doors=["the lease and the landlord",
              "with sailing: the harbour's own business"]),
  # way "shore_business", rung 3 (the shore's best-known business)
  dict(name="the shore's best-known trader", kind="status", sphere="comm", face="comm.B", ways="",
       profiles=[("B R", "Built the busiest business on the shore, and enjoys it."),
                 ("W", "Keeps the shore's traders together and speaks for them."),
                 ("G", "Is part of the shore itself after so many years, open every season.")],
       meets="need:meaning+.05 need:autonomy+.05 res:money+.05 res:ties+.03 res:time-.08", lasts="life",
       ages=(30, 90), share=0.0003,   # estimate
       say="the shore's best-known trader",
       gained="the business everyone names when they talk of the shore",
       lost="never as a record; the name fades after the business is sold or closed",
       needs="[shore cafe owner] for years; [loyal clientele]",
       doors=["the traders' association",
              "the council's tourism officer"]),

  # ---- way "beachcombing" (R G), sphere arts
  # way "beachcombing", rung 1 (a shelf of finds)
  dict(name="beachcomber", kind="status", sphere="arts", face="arts.R", ways="",
       profiles=[("R G", "Walks the shore after every storm, and keeps whatever catches the eye."),
                 ("U", "Sorts and labels every find, and knows what each one is."),
                 ("W", "Picks up the litter as well as the treasures, every walk.")],
       meets="need:autonomy+.03 need:meaning+.02 res:time-.02", lasts="life",
       ages=(8, 100), share=0.05,   # estimate
       say="a beachcomber",
       gained="a shelf of their own finds from the shore and the foreshore",
       lost="never as a record; the walks stop with a move away from the shore",
       needs="a shore within reach and the tides to walk it; [place by the sea] helps",
       doors=["the shore people",
              "with wood carving: a gallery of the land's own things"]),
  # way "beachcombing", rung 2 (shows the art)
  dict(name="shore artist", kind="status", sphere="arts", face="arts.R", ways="",
       profiles=[("R G", "Makes bold pieces from the finds, whatever they suggest."),
                 ("U", "Works with care, piece by piece, until each one is right."),
                 ("B", "Makes what sells at the gallery and the market, and keeps making it.")],
       meets="need:meaning+.05 need:autonomy+.03 res:money+.02 res:time-.05", lasts="life",
       ages=(14, 100), share=0.003,   # estimate
       say="an artist of the shore",
       gained="work made from the shore's finds shown and sold at the gallery or the market",
       lost="never as a record; the making stops with a move or a busier life",
       needs="[beachcomber]; [drawing and painting] or a craft; a gallery or a market stall to show at",
       doors=["the gallery owner",
              "the craft market"]),
  # way "beachcombing", rung 3 (the gallery's name)
  dict(name="gallery name", kind="status", sphere="arts", face="arts.R", ways="",
       profiles=[("R G", "Makes the work people come for, and is never afraid to change it."),
                 ("B", "Builds the name and the price with every show."),
                 ("U", "Works slowly, and is collected for it.")],
       meets="need:meaning+.08 need:autonomy+.05 res:money+.03 res:time-.05", lasts="life",
       ages=(25, 100), share=0.0003,   # estimate
       say="the gallery's best-known name",
       gained="a show of their own and buyers who come for their work by name",
       lost="never as a record; the name fades if the work stops",
       needs="[shore artist] for years; a show of their own",
       doors=["galleries in other towns",
              "commissions"]),

  # ---- way "restore_river" (G U), sphere learn
  # way "restore_river", rung 1 (volunteer days)
  dict(name="river volunteer", kind="status", sphere="learn", face="learn.G", ways="",
       profiles=[("G U", "Comes to every work day and learns the river's plants and fish."),
                 ("W", "Turns up with the trust's crew every month, wades in and does the job."),
                 ("R", "Takes the hardest task, the deepest mud and the heaviest log.")],
       meets="need:belonging+.05 need:meaning+.03 res:time-.02", lasts="life",
       ages=(14, 100), share=0.03,   # estimate
       say="a river volunteer",
       gained="a year of the trust's volunteer days on the banks",
       lost="never as a record; the work days stop with a move or a busier life",
       needs="a river trust with volunteer days; waders and a willingness to get wet",
       doors=["the river trust"]),
  # way "restore_river", rung 2 (a stretch restored)
  dict(name="river restorer", kind="status", sphere="learn", face="learn.G", ways="",
       profiles=[("G U", "Plans each bend and pool, and counts the fish that come back."),
                 ("W", "Gets the landowners and the officials to agree, and keeps them agreeing."),
                 ("B", "Finds the grants and gets the works done before the season closes.")],
       meets="need:meaning+.08 need:competence+.05 res:time-.05", lasts="life",
       ages=(18, 100), share=0.003,   # estimate
       say="a restorer of the river",
       gained="a stretch restored on their plan, with fish counted back in it",
       lost="never; the stretch and its fish stay as the record",
       needs="[river volunteer]; a landowner who agrees; the trust's grant",
       doors=["landowners along the river",
              "with the swimming group: the swim the river came back for, the town's summer gathering"]),
  # way "restore_river", rung 3 (the trust's lead)
  dict(name="river trust lead", kind="status", sphere="learn", face="learn.G", ways="",
       profiles=[("G U", "Leads the trust for the whole river, from the springs to the sea."),
                 ("W", "Keeps the trust fair, open and run by its members."),
                 ("B", "Raises the money and widens the trust's reach every year.")],
       meets="need:meaning+.08 need:belonging+.03 res:ties+.05 res:time-.08", lasts="life",
       ages=(28, 100), share=0.0003,   # estimate
       say="the river trust's lead",
       gained="the trust's board asking them to lead, after years of stretches brought back",
       lost="never as a record; the lead passes on when they step back",
       needs="[river restorer] for years; the choice of the trust's board",
       doors=["the council's land board",
              "every landowner on the river"]),
]
TITLES_V25 = TITLES_V25 + _TITLES_LAND


# Rung steps for Earth's fields (v25 prep, Library).
# STEPS maps each field key of FIELDS_EARTH and FIELDS_EARTH_LAND (earth_fields.py) to one short gerund phrase
# per rung, in rung order: what the person does to reach that rung. The Library pours these into each rung as
# the optional key `step`, read into the slot {next} in lines like "the way into {next}" or
# "working toward {next}". Rungs with time=True get a phrase about the years themselves being lived well.

STEPS = {
    # FIELDS_EARTH
    "to raise a family that holds together": [
        "making a home with children in it",
        "gathering the family at one table",
        "living the years that keep them close",
        "seeing the long years through at its centre",
    ],
    "to keep the peace in the street": [
        "keeping an eye on the street",
        "learning to step in before it turns",
        "becoming the street's keeper",
        "earning the trust of every door",
    ],
    "to see justice done": [
        "getting a foot in the courts",
        "qualifying to stand up in court",
        "earning a name for fairness",
        "bringing a case that changes the law",
        "handing down a ruling still cited",
    ],
    "to keep one promise for life": [
        "finding someone to keep a promise to",
        "making the promise",
        "keeping it through the hard times",
    ],
    "to build things that last": [
        "learning a building trade",
        "earning a ticket and tools of their own",
        "earning a name for work that holds",
        "making work people travel to see",
        "raising a building that stands for generations",
    ],
    "to serve the public well": [
        "winning a desk in public service",
        "earning trust with the public's business",
        "making a name in the town hall",
        "bringing in a change the whole country uses",
    ],
    "to be the one people come to for advice": [
        "becoming a good listener",
        "earning the trust to hear troubles",
        "becoming the one everyone asks",
        "giving advice heard far beyond the street",
    ],
    "to make a home that runs well": [
        "sharing a home",
        "putting the household in order",
        "setting money by",
        "making a home that all but runs itself",
    ],
    "to rise to the top of the firm": [
        "getting a foot on the ladder",
        "taking on people to manage",
        "winning a seat at the top table",
        "rising to head the firm",
    ],
    "to keep the family name high": [
        "becoming the one who carries the name",
        "keeping a household others respect",
        "raising children through the years to do it proud",
        "making a name that opens doors",
    ],
    "to own the roof over our heads": [
        "setting money aside",
        "buying a front door of their own",
        "paying off the roof",
    ],
    "to make the rules everyone lives by": [
        "winning a seat on a committee",
        "having a say in the rules",
        "earning a voice the town hall heeds",
        "writing laws that carry their name",
        "drafting a charter still in force",
    ],
    "to know one thing better than anyone": [
        "finding a question that will not let go",
        "putting in years of patient study",
        "becoming the one everyone asks",
        "becoming known across the country for it",
        "writing the book on the subject",
    ],
    "to master an instrument": [
        "taking up an instrument",
        "learning to play with others",
        "getting paid to play",
        "earning a name for the playing",
        "playing to audiences across the country",
    ],
    "to teach well": [
        "learning to explain things to others",
        "taking a class of their own",
        "teaching pupils who come back to say thanks",
        "becoming a teacher the country knows of",
    ],
    "to find out what is true": [
        "asking the big questions out loud",
        "reading every side",
        "finding an answer to live by",
        "becoming the one others bring doubts to",
    ],
    "to be the best at what I do": [
        "taking up a trade to get good at",
        "getting better than those alongside them",
        "making a name in the field",
        "becoming the best in the country",
    ],
    "to marry well": [
        "courting with a clear head",
        "making a promise",
        "marrying well and wisely",
        "building a household that stands well",
    ],
    "to keep a sharp eye on money": [
        "counting every coin",
        "taking charge of the books",
        "putting money to work",
        "becoming the one trusted with the money",
        "making a name in money across the country",
    ],
    "to study the old texts": [
        "learning the tongue they were written in",
        "becoming a teacher of the texts",
        "becoming the one others bring questions to",
        "offering a reading the whole country argues over",
        "making a translation still read",
    ],
    "to cook like nobody else": [
        "cooking for strangers",
        "running a kitchen of their own",
        "making the place people cross town for",
        "becoming a cook the country talks about",
        "creating a dish the country still cooks",
    ],
    "to speak every language I meet": [
        "learning a second tongue",
        "living among other speakers",
        "earning a living with words",
        "becoming the one called when nobody understands",
    ],
    "to fall for a mind as quick as mine": [
        "finding a spark across the table",
        "arguing till dawn, and loving it",
        "building a life of talk",
        "keeping the talk going through the years",
    ],
    "to raise children who question everything": [
        "having a child of their own",
        "filling a house with questions",
        "raising them through the years into their own minds",
        "living on to hear grandchildren asking why",
    ],
    "to answer to no one": [
        "starting a little trade on the side",
        "putting their own name over the door",
        "winning customers who come back",
        "making a name in the trade beyond town",
    ],
    "to be somebody in this town": [
        "becoming a face people know",
        "winning a seat at the table",
        "earning a voice the town hall hears",
        "making a name the whole town knows",
    ],
    "to win at the highest level": [
        "training every day",
        "winning trophies for the shelf",
        "getting paid to compete",
        "becoming a champion the country knows",
        "setting a record that stands",
    ],
    "to make money work for me": [
        "setting money aside",
        "earning the bank's trust",
        "putting money into something that grows",
        "building an income that arrives while they sleep",
    ],
    "to live by my own rules": [
        "finding a way out of town",
        "earning a living no boss can take",
        "fitting a life into a van",
    ],
    "to make it big, and fast": [
        "making a side business pay",
        "starting a venture of their own",
        "making a name in the business",
        "becoming the one everyone has heard of",
        "building a firm that outlasts its founder",
    ],
    "to never be pushed around again": [
        "learning to hold their own",
        "finding people who stand with them",
        "becoming someone not to be crossed",
        "finding a voice nobody talks over",
    ],
    "to chase the next thrill": [
        "chasing the first rush",
        "taking bigger risks, more often",
        "earning a name for daring",
    ],
    "to outlast them all": [
        "looking after the body",
        "growing tough as old roots",
        "seeing the long years through on their feet",
    ],
    "to keep the family land": [
        "working the family ground",
        "getting the land in their own name",
        "holding on to the old name",
        "handing the land on whole",
    ],
    "to know every root and mushroom": [
        "learning to read the ground",
        "selling what the woods give",
        "becoming the one everyone asks",
        "writing the guide the country reads",
        "making a field guide for every pocket",
    ],
    "to run the family business": [
        "working behind the family counter",
        "learning the trade",
        "taking over the keys",
        "making it the business the town trusts",
    ],
    "to see the world": [
        "packing a bag and finding a way out",
        "growing at home in strange places",
        "making a life on the move",
        "making a home in more than one land",
    ],
    "to love with everything": [
        "falling hard",
        "going all in, with no way back",
        "making the wedding of a lifetime",
        "staying in love through the years",
    ],
    "to stand up for the underdog": [
        "speaking up when nobody else will",
        "taking on other people's fights",
        "becoming the one people bring trouble to",
        "taking up a case the whole country hears",
        "winning a case still cited for others",
    ],
    "to feel something greater in the music": [
        "singing until it lifts them",
        "bringing music to the heart of gatherings",
        "leading the room in song",
        "making the music people come for",
    ],
    "to live wild and free outdoors": [
        "getting out in all weathers",
        "learning the skills of the wild",
        "making a living out of doors",
        "finding a wild patch to call their own",
    ],
    "to raise a big, loud family": [
        "filling a house with children",
        "adding more chairs round the table",
        "living the years that keep them coming home",
        "living on to see grandchildren underfoot",
    ],
    "to dance": [
        "dancing whenever the music plays",
        "joining a company to dance with",
        "opening a floor of their own",
        "dancing for the whole country",
        "making a dance still taught",
    ],
    "to save the wild places": [
        "going out with the litter-pickers",
        "taking up a cause of their own",
        "saving the wood",
        "bringing the whole country into the fight",
    ],
    "to be there when it counts": [
        "getting first to the scene",
        "training to go in",
        "making it their job",
        "becoming the one the town thanks",
        "making a rescue the whole country saw",
    ],
    "to fight for what is right": [
        "refusing to look away",
        "finding a fight worth having",
        "becoming impossible to ignore",
        "making the whole country hear it",
        "winning a right the country still keeps",
    ],
    "to throw the parties the town remembers": [
        "making the house everyone ends up at",
        "running the night",
        "earning a name for a good time",
        "starting a festival the whole country comes to",
    ],
    "to protect the ones I love": [
        "finding someone to stand beside",
        "making a promise",
        "making a home where they are safe",
        "standing beside them through the worst",
    ],
    "to work the land": [
        "finding land of their own to work",
        "earning a name for good produce",
        "building the farm others learn from",
        "making a farm known across the country",
        "leaving a farm and a seed others grow",
    ],
    "to keep the family's ways": [
        "learning the old ways by heart",
        "keeping the house where the family gathers",
        "handing the ways down to the children",
        "becoming the one the whole family asks",
    ],
    "to grow old among many grandchildren": [
        "starting a family of their own",
        "filling a house with children",
        "living the years until the first grandchild",
        "becoming the head of a big family",
    ],
    "to stay strong and well for life": [
        "moving every day",
        "taking on a team or a hill weekly",
        "showing others how",
        "keeping strong through the working years",
    ],
    "to care for those who cannot manage alone": [
        "taking up care as their work",
        "becoming the calm others lean on",
        "becoming the carer families ask for",
        "speaking up for carers across the country",
        "shaping a way of caring others follow",
    ],
    "to feed the street from my garden": [
        "growing a few rows of their own",
        "sharing the harvest over the fence",
        "making the street's own garden",
        "becoming the one the street thanks",
        "making a street garden others copy",
    ],
    "to belong to a congregation for life": [
        "keeping the same seat each week",
        "becoming a known face",
        "taking a part in its work",
        "becoming one of its elders",
    ],
    "to make a home everyone is welcome in": [
        "finding someone to make a home with",
        "getting a roof of their own",
        "keeping a table that always has room",
        "keeping a door that never shuts",
    ],
    "to grow the perfect garden": [
        "sowing seeds on the windowsill",
        "making a garden of their own",
        "learning every plant by name",
        "making the garden people come to see",
        "growing a garden known across the country",
    ],
    "to work with animals": [
        "finding a way with animals",
        "making animals their work",
        "keeping animals of their own",
        "becoming the one people bring animals to",
        "becoming known across the country for the work",
    ],
    "to know where we come from": [
        "putting the family tree on the wall",
        "learning the old stories",
        "writing a history read across the country",
        "writing a town history that is still read",
    ],
    "to live in balance": [
        "taking time alone outdoors",
        "finding a path of their own",
        "becoming a calm others lean on",
        "becoming the one people turn to when life tips",
    ],
    "to master chess": [
        "becoming a club player",
        "becoming a rated player",
        "winning a tournament",
        "earning the master title",
        "earning the grandmaster title",
    ],
    "to play football at the top": [
        "winning a place in a junior side",
        "getting picked for an academy",
        "signing a first contract",
        "becoming a regular in the top division",
        "getting picked for the national side",
    ],
    "to race cars": [
        "getting a kart and a club track",
        "earning a licence and a full season",
        "winning a junior championship",
        "earning a paid seat in a team",
        "winning a championship title",
    ],
    "to fight in the ring": [
        "finding a gym and gloves of their own",
        "taking amateur bouts",
        "winning an amateur title",
        "getting paid to fight",
        "winning a title belt",
    ],
    "to earn a black belt": [
        "winning a place in a training hall",
        "passing the first gradings",
        "earning the first-degree belt",
        "opening a school of their own",
    ],
    "to make video games": [
        "finishing a first game",
        "getting paid to make games",
        "making a game with their name on it",
        "making a game people talk about",
        "making a game millions play",
    ],
    "to play in a band": [
        "starting a band of their own",
        "playing gigs to real crowds",
        "building a crowd that comes back",
        "putting a record out and touring",
        "writing songs the country sings along to",
    ],
    "to be famous": [
        "building an audience of their own",
        "growing a following",
        "getting paid to be seen",
        "becoming a face the country knows",
        "becoming a household name",
    ],
    "to take in a child who has no one": [
        "getting checked, trained and approved",
        "bringing a child who had no one home",
        "keeping a home that holds",
        "seeing a child who had no one grow up",
    ],
    "to run an animal sanctuary": [
        "helping out at the rescue yard",
        "taking rescued animals in at home",
        "opening a sanctuary that turns no animal away",
    ],
    "to breed champion horses": [
        "taking on a horse to look after",
        "breeding a first foal that wins",
        "building a line of horses known everywhere",
    ],
    "to explore the far places": [
        "spending nights out with map and compass",
        "winning a place on an expedition",
        "leading an expedition",
        "mapping a place nobody had mapped",
    ],

    # FIELDS_EARTH_LAND
    "allotment": ["taking on a plot", "winning prizes and swapping seed", "chairing the society"],
    "market_garden": ["running a stall", "winning regular buyers", "opening a farm shop"],
    "beekeeping": ["setting up a first hive", "bottling honey of their own", "teaching the course"],
    "keeping_animals": ["keeping a few hens", "building up a flock", "judging at the show"],
    "regen_farming": ["starting a trial field", "keeping the yields up", "getting others to copy it"],
    "land_dealing": ["buying a first field", "collecting rents", "becoming the town's big landowner"],
    "building_on_land": ["building a home of their own", "putting up a small scheme", "becoming a developer"],
    "field_sports": ["playing regularly", "making the first team", "becoming captain or coach"],
    "field_events": ["helping out at events", "running a stage", "making the festival their own"],
    "wildflower_meadow": ["sowing a wild corner", "sowing the street's verges", "tending the town's meadows"],
    "trail_running": ["mapping routes of their own", "running races", "building the trails"],
    "timber": ["cutting firewood for the house", "selling cords of wood", "managing the wood"],
    "deer_management": ["going out with the club", "earning a permit of their own", "becoming the wood's ranger"],
    "forage_guide": ["filling baskets of their own", "leading walks", "supplying the restaurants"],
    "forest_school": ["helping at a session", "running a group", "running the town's forest school"],
    "wildlife_survey": ["making first counts", "taking on a square of their own", "becoming the county's recorder"],
    "campsite": ["opening a field to tents", "building cabins", "running the outdoor centre"],
    "wood_crafts": ["carving spoons", "selling at the fair", "taking on a workshop and apprentices"],
    "wood_guardian": ["joining the friends of the wood", "leading a campaign", "becoming the town's voice for its land"],
    "rewilding": ["letting a corner go wild", "returning a field to the wild", "making a reserve"],
    "angling_club": ["getting a licence", "fishing the club's matches", "becoming the club's bailiff or chair"],
    "wild_swimming": ["taking first cold swims", "swimming through every season", "leading the group"],
    "sailing": ["taking lessons", "entering races", "becoming commodore or instructor"],
    "water_testing": ["taking monthly samples", "tracing a source", "becoming the town's water expert"],
    "flood_warden": ["becoming warden for the street", "serving as warden for the ward", "joining the town's flood board"],
    "water_rights": ["earning a share", "getting on the water rota", "chairing the water board"],
    "catch_to_sell": ["selling the catch", "getting a boat or ponds of their own", "becoming the market's main supplier"],
    "shore_business": ["running a summer stall", "opening a place that runs all seasons", "building the shore's best-known business"],
    "beachcombing": ["filling a shelf with finds", "showing the art", "making a name at the gallery"],
    "restore_river": ["joining volunteer days", "restoring a stretch", "leading the trust"],
}
for _k, _ss in STEPS.items():   # the optional rung key `step`, read into {next} (Engine 10-23)
    for _r, _s in zip((FIELDS_EARTH.get(_k) or FIELDS_EARTH_LAND[_k])["rungs"], _ss):
        _r["step"] = _s
