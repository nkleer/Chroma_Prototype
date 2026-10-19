# rules_packs.py: part 8 of 11 of earth_rules.py, the engine's reading of the Library's words.
# PACK_RULES: the science, politics and stage packs.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
# ---- content packs (chroma-packs/, the pathways and packs thread): the engine's conditions for each pack's echoes, inner and
# read moments (batch._packs merges them over INNER, ECHO, LIFE and READ). A season's moments (threshold:) need none.
_RESEARCH = ("has('research assistant') | has('research scientist') | has('research project lead') | "
             "has('research group leader') | has('research facility lead') | has('independent investigator') | "
             "has('research software engineer') | has('research data steward') | has('evidence synthesis specialist')")
PACK_RULES = {
    "science": dict(
        ECHO={
            # a breakthrough at work outside research that keeps asking to be understood (the applied translator's door)
            "the finding will not leave you alone": dict(
                anchor=f"had(['a breakthrough in your work'], {JUST})", req=f"~({_RESEARCH}) & (age >= 18)",
                more=["has('graduate')", "(hU + hR) > .5", "time > .5"],
                less=["stress > 1.5", "money < .2", "held_children & (kids_home > 0) & (time < .3)"]),
            # a child's wonder, back decades later with time to spare (the late entrant's door)
            "a question from childhood comes back": dict(
                anchor=f"had(['a curiosity that will not let go', 'awe'], {JUST}) & (age < 20)",
                req="(age >= 27) & (time > .4)",
                more=["retired", "~held_career", "kids_home == 0"],
                less=["stress > 1.5", "money < .2", "health < .3"]),
        },
        ROLES={
            # the catalogue has a professor on a research scientist or a group leader; the proposed rule named only the first
            "professor": dict(refines="research scientist; research group leader"),
        },
        READ={
            # a year's results come back null: only to someone with a research project under way
            "the results are in": dict(req="has('a research project under way')"),
        },
    ),
    "politics": dict(
        ECHO={   # the packs thread's proposal (chroma-packs/politics/engine-conditions.py, 22:56), taken as written
            # a local fight, a protest or a bitter election that leaves the person wanting to stand (the door from the street)
            "the fight that made you want to stand": dict(
                anchor=f"had(['your town faces a change you could fight', 'a protest to save the local hospital', "
                       f"'a sense of injustice', 'a bitter election', 'they ask you to lead because you stood up once'], {JUST})",
                req="~(has('local councillor') | has('mayor') | has('member of parliament')) & (age >= 18)",
                more=["has('activist in a cause')", "has('party member')", "(hW + hR) > .5"],
                less=["stress > 1.5", "health < .3"]),
            # a school debate, or a young campaigner's stand, back years later with time to spare (the door from the past)
            "the debate you never forgot": dict(
                anchor=f"had(['a debate or contest at school', 'defending a speaker you cannot stand'], {JUST}) & (age < 30)",
                req="(age >= 19) & (time > .4)",
                more=["retired", "kids_home == 0", "has('public speaking')"],
                less=["stress > 1.5", "money < .2"]),
        },
    ),
}
# ---- pack conditions pasted from the packs' engine-conditions.py (calib_v7/paste_pack_rules.py; the engine may reword them here)
# part politics BASE ECHO
PACK_RULES.setdefault('politics', {}).setdefault('ECHO', {}).update({'the fight that made you want to stand': {'anchor': "had(['your town faces a change you could fight', 'a protest to "
                                                     "save the local hospital', 'a sense of injustice', 'a bitter "
                                                     "election', 'they ask you to lead because you stood up once'], "
                                                     '0.08333333333333333)',
                                           'req': "~(has('local councillor') | has('mayor') | has('member of "
                                                  "parliament')) & (age >= 18)",
                                           'more': ["has('activist in a cause')",
                                                    "has('party member')",
                                                    '(hW + hR) > .5'],
                                           'less': ['stress > 1.5', 'health < .3']},
 'the debate you never forgot': {'anchor': "had(['a debate or contest at school', 'defending a speaker you cannot "
                                           "stand'], 0.08333333333333333) & (age < 30)",
                                 'req': '(age >= 19) & (time > .4)',
                                 'more': ['retired', 'kids_home == 0', "has('public speaking')"],
                                 'less': ['stress > 1.5', 'money < .2']}})
# part politics LONGSHOTS ECHO
PACK_RULES.setdefault('politics', {}).setdefault('ECHO', {}).update({'the race comes round again': {'anchor': "has('a long shot that missed') & had(['election night', 'polling day for "
                                          "mayor', 'a challenge from the back benches', 'the campaign nobody gave a "
                                          "chance', 'the leadership falls vacant'], 0.08333333333333333) & "
                                          '(ago_fail_long < 0.08333333333333333)',
                                'req': "(age <= 80) & (health > .35) & (ago_fail_long >= sa) & (~had(['a challenge "
                                       "from the back benches', 'the leadership falls vacant'], 13) | has('member of "
                                       "parliament')) & (~had(['the campaign nobody gave a chance'], 13) | "
                                       "has('party leader'))",
                                'more': ["has('good name in town') | has('voice at the town hall') | has('a "
                                         "following in the party') | has('allies in the party')",
                                         "has('a loyal campaign team') | has('a list of supporters') | "
                                         "has('canvassing')",
                                         'time > .4'],
                                'less': ['stress > 1.5', 'money < .15', 'ago_move < sa']},
 'making peace with the long shot': {'anchor': "has('a long shot that missed') & had(['election night', 'a seat "
                                               "falls vacant', 'the leadership falls vacant', 'polling day for "
                                               "mayor', 'a challenge from the back benches', 'the campaign nobody "
                                               "gave a chance', 'writing in cold for a job in politics', 'the "
                                               "campaign loses its organiser'], 0.08333333333333333) & "
                                               '(ago_fail_long < 0.08333333333333333)',
                                     'req': 'age >= 25',
                                     'more': ['age >= 45', 'retired | (kids_home == 0)', 'ties > .5'],
                                     'less': ['stress > 1.5', 'health < .3']}})
# part politics LONGSHOTS LIFE
PACK_RULES.setdefault('politics', {}).setdefault('LIFE', {}).update({'standing with no party behind you': {'req': "~has('member of parliament') & ~has('parliamentary candidate') & "
                                              "((yrs_has('local councillor') >= 4) | (yrs_has('mayor') >= 2) | "
                                              "has('former member of parliament') | ((yrs_has('voice at the town "
                                              "hall') >= 6) & (has('activist in a cause') | has('union rep') | "
                                              "has('residents\\' committee member') | has('school-governance board "
                                              "member') | has('civil-liberties campaigner') | has('local hero'))))",
                                       'more': ["(yrs_has('local councillor') >= 8) | (yrs_has('mayor') >= 4)",
                                                "has('good name in town') | has('local hero') | has('a list of "
                                                "supporters') | has('a loyal campaign team')"],
                                       'less': ["has('party member')", 'stress > 1.5', 'money < .1']},
 'a run for mayor from outside the council': {'req': "~was('local councillor') & ~was('mayor') & ~has('mayoral "
                                                     "candidate') & ((yrs_has('local party officer') >= 4) | "
                                                     "(yrs_has('voice at the town hall') >= 5) | "
                                                     "(yrs_has('residents\\' committee member') >= 5) | "
                                                     "(yrs_has('school-governance board member') >= 4) | "
                                                     "(yrs_has('union rep') >= 5) | (yrs_has('local hero') >= 5) | "
                                                     "(yrs_has('good name in town') >= 10) | (yrs_has('founder of a "
                                                     "firm') >= 8) | (yrs_has('family business') >= 10) | "
                                                     "(yrs_has('party member') >= 6) | (yrs_has('activist in a "
                                                     "cause') >= 5))",
                                              'more': ["has('voice at the town hall') | has('local hero')",
                                                       'ago_move > 10'],
                                              'less': ['ago_move < 3', 'stress > 1.5']},
 'a challenge from the back benches': {'req': "(yrs_has('member of parliament') >= 4) & ~has('minister') & "
                                              "~has('party leader')",
                                       'more': ["yrs_has('member of parliament') >= 8",
                                                "has('a following in the party') | has('allies in the party')"],
                                       'less': ['stress > 1.5']},
 'the campaign nobody gave a chance': {'req': "(yrs_has('party leader') >= 2) & ~has('head of government')",
                                       'more': ["has('known across the country')"],
                                       'less': ['stress > 1.5']},
 'writing in cold for a job in politics': {'req': "~(has('political adviser') | has('party official') | "
                                                  "has('lobbyist') | has('policy analyst') | has('speechwriter') | "
                                                  "has('member of parliament')) & (age <= 70) & ((yrs_has('local "
                                                  "party officer') >= 1) | (has('graduate') & (yrs_has('data "
                                                  "analyst') >= 2)) | (yrs_has('salesperson') >= 3) | "
                                                  "(yrs_has('journalist') >= 3) | (yrs_has('constituency "
                                                  "caseworker') >= 1))",
                                           'more': ["has('graduate')",
                                                    "has('friend in power') | has('mentor')",
                                                    'time > .4'],
                                           'less': ['stress > 1.5']},
 'the campaign loses its organiser': {'req': "(age <= 75) & ~has('campaign organiser') & ~has('constituency "
                                             "caseworker') & ~has('pollster') & ~(has('political adviser') | "
                                             "has('party official') | has('lobbyist') | has('policy analyst') | "
                                             "has('speechwriter') | has('member of parliament'))",
                                      'more': ["(yrs_has('campaign volunteer') >= 3) | (yrs_has('local party "
                                               "officer') >= 3)",
                                               "has('canvassing')"],
                                      'less': ['stress > 1.5', 'time < .2']}})
# part science LONGSHOTS ECHO
PACK_RULES.setdefault('science', {}).setdefault('ECHO', {}).update({'the old door opens a crack': {'anchor': "has('a long shot that missed') & had(['a discovery nobody asked you for', "
                                          "'a group of your own, open to all comers', 'a facility looks outside for "
                                          "its next head', 'a search for a new voice for science', 'a chair falls "
                                          'vacant at another university\', "a scientist\'s post at a famous lab", '
                                          "'a named fellowship, one a year', 'a national centre opens its posts', "
                                          "'the survey wants a paid assistant'], 0.08333333333333333) & "
                                          '(ago_fail_long <= 0.08333333333333333)',
                                'req': "(age >= 28) & (age <= 85) & (health > .35) & ((had(['a discovery nobody "
                                       "asked you for'], 14) & ~has('independent investigator') & has('published "
                                       "research') & (has('research scientist') | has('research assistant') | "
                                       "has('citizen scientist') | has('community observer') | has('volunteer "
                                       "research organiser'))) | (had(['a group of your own, open to all comers'], "
                                       "14) & ~has('research group leader') & has('research grant') & (has('research "
                                       "scientist') | has('research project lead'))) | (had(['a facility looks "
                                       "outside for its next head'], 14) & ~has('research facility lead') & "
                                       "(has('lab work') | has('instrument troubleshooting')) & (has('laboratory "
                                       "technician') | has('research scientist'))) | (had(['a search for a new voice "
                                       "for science'], 14) & ~has('science communication specialist') & "
                                       "has('explaining science') & (has('research scientist') | has('research "
                                       "assistant') | has('journalist') | has('teacher'))) | (had(['a chair falls "
                                       "vacant at another university'], 14) & ~has('professor') & has('published "
                                       "research') & (has('research group leader') | has('research scientist'))) | "
                                       '(had(["a scientist\'s post at a famous lab"], 14) & ~has(\'research '
                                       "scientist') & (has('research assistant') | has('laboratory technician') | "
                                       "has('research data steward') | has('research software engineer'))) | "
                                       "(had(['a named fellowship, one a year'], 14) & ~has('postdoctoral "
                                       "researcher') & has('doctoral graduate') & has('research scientist') & "
                                       "(yrs_has('research scientist') <= 8)) | (had(['a national centre opens its "
                                       "posts'], 14) & has('research scientist')) | (had(['the survey wants a paid "
                                       "assistant'], 14) & ~has('research assistant') & (has('citizen scientist') | "
                                       "has('community observer'))))",
                                'more': ["has('mentor') | has('research collaborators')",
                                         "has('research grant') | has('savings') | has('patron')",
                                         "has('a finding that held up') | has('name in the field') | "
                                         "has('supervising researchers')"],
                                'less': ['stress > 1.5',
                                         'money < .15',
                                         'held_children & (kids_home > 0) & (time < .3)']},
 'the story of the long shot': {'anchor': "has('a long shot that missed') & had(['a discovery nobody asked you for', "
                                          "'a group of your own, open to all comers', 'a facility looks outside for "
                                          "its next head', 'a search for a new voice for science', 'a chair falls "
                                          'vacant at another university\', "a scientist\'s post at a famous lab", '
                                          "'a named fellowship, one a year', 'a national centre opens its posts', "
                                          "'the survey wants a paid assistant', 'the old door opens a crack'], "
                                          '0.08333333333333333) & (ago_fail_long <= 0.08333333333333333)',
                                'req': 'age >= 32',
                                'more': ['retired',
                                         'kids_home == 0',
                                         "has('teaching') | has('explaining science') | has('former students') | "
                                         "has('mentor')"],
                                'less': ['stress > 1.5', 'health < .25', 'ago_loss < 1']}})
# part science LONGSHOTS LIFE
PACK_RULES.setdefault('science', {}).setdefault('LIFE', {}).update({'a discovery nobody asked you for': {'req': "~has('independent investigator') & ((yrs_has('research scientist') >= "
                                             "2) | (yrs_has('research assistant') >= 3) | (has('published research') "
                                             "& ((yrs_has('citizen scientist') >= 5) | (yrs_has('community "
                                             "observer') >= 5) | (yrs_has('volunteer research organiser') >= 3))))"},
 'a group of your own, open to all comers': {'req': "~has('research group leader') & (yrs_has('research scientist') "
                                                    ">= 4) & has('research grant')"},
 'a facility looks outside for its next head': {'req': "~has('research facility lead') & ((yrs_has('laboratory "
                                                       "technician') >= 4) | (yrs_has('research scientist') >= 4)) & "
                                                       "(has('lab work') | has('instrument troubleshooting'))"},
 'a search for a new voice for science': {'req': "~has('science communication specialist') & (yrs_has('explaining "
                                                 "science') >= 3) & has('graduate') & (was('research scientist') | "
                                                 "was('research assistant') | was('journalist') | was('teacher'))"},
 'a chair falls vacant at another university': {'req': "~has('professor') & has('published research') & "
                                                       "((yrs_has('research group leader') >= 3) | "
                                                       "(yrs_has('research scientist') >= 8))"},
 "a scientist's post at a famous lab": {'req': "~has('research scientist') & has('graduate') & ((yrs_has('research "
                                               "assistant') >= 2) | (yrs_has('laboratory technician') >= 2) | "
                                               "(yrs_has('research data steward') >= 2) | (yrs_has('research "
                                               "software engineer') >= 2))"},
 'a named fellowship, one a year': {'req': "~has('postdoctoral researcher') & has('doctoral graduate') & "
                                           "(yrs_has('research scientist') <= 5) & (age <= 45)"},
 'a national centre opens its posts': {'req': "yrs_has('research scientist') >= 2"},
 'the survey wants a paid assistant': {'req': "~has('research assistant') & ((yrs_has('citizen scientist') >= 4) | "
                                              "(yrs_has('community observer') >= 4))"}})
# part stage BASE ECHO
PACK_RULES.setdefault('stage', {}).setdefault('ECHO', {}).update({'the part you never got to play': {'anchor': "had(['the school play'], 0.08333333333333333) & (age < 13)",
                                    'req': "(age >= 18) & ~has('amateur actor') & ~has('professional actor')",
                                    'more': ['(hR + hG) > .5', 'time > .5', "has('singing') | has('dancing')"],
                                    'less': ['stress > 1.5',
                                             'money < .15',
                                             'held_children & (kids_home > 0) & (time < .3)']},
 'never too late for the stage': {'anchor': "had(['the first months of retirement'], 0.08333333333333333)",
                                  'req': "retired & ~has('amateur actor') & (health > .4)",
                                  'more': ["was('amateur actor') | was('youth theatre member') | has('a lead role to "
                                           "remember')",
                                           'time > .5',
                                           '(hG + hR) > .45'],
                                  'less': ['health < .5', 'money < .15', 'held_partner & (support < .3)']},
 'the show you wrote to star in': {'anchor': "had(['inspiration strikes', 'wanting to be noticed'], "
                                             "0.08333333333333333) & has('acting')",
                                   'req': "(age >= 17) & ~has('lead actor or actress') & ~has('a fringe slot')",
                                   'more': ["has('writing stories') | has('writing scripts')",
                                            "has('improvisation')",
                                            '(hR + hU) > .5'],
                                   'less': ['stress > 1.5', 'money < .15', 'kids_home > 1']},
 'the part that came with the letter': {'anchor': "had(['an unexpected chance: a grant, a role, a stage'], "
                                                  "0.08333333333333333) & has('acting')",
                                        'req': "(age >= 17) & ~has('professional actor') & ((yrs_has('amateur "
                                               "actor') >= 2) | (yrs_has('background artist') >= 2) | "
                                               "(yrs_has('drama school student') >= 1))",
                                        'more': ["has('a lead role to remember')",
                                                 "has('amateur actor')",
                                                 "has('casting directory listing')"],
                                        'less': ['stress > 1.5', 'kids_home > 1', 'health < .4']}})
# part stage BASE LIFE
PACK_RULES.setdefault('stage', {}).setdefault('LIFE', {}).update({'the part of a lifetime is cast': {'req': "(yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2) | "
                                           "((yrs_has('amateur actor') >= 5) & has('a lead role to remember'))"},
 'chosen to wear the great mask': {'req': "(yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2) | "
                                          "((yrs_has('amateur actor') >= 5) & has('a lead role to remember'))"},
 'a glamour that makes the play real': {'req': "(yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2) "
                                               "| ((yrs_has('amateur actor') >= 5) & has('a lead role to "
                                               "remember'))"},
 'the understudy goes on': {'req': "has('understudy') & (yrs_has('professional actor') >= 1)"},
 'the director calls again': {'req': "has('a director who keeps casting you') & ((yrs_has('professional actor') >= "
                                     "2) | (yrs_has('voice actor') >= 2))"},
 'opening night at the fringe': {'req': "has('a fringe slot') & (has('professional actor') | has('voice actor') | "
                                        "(yrs_has('drama school student') >= 1) | (yrs_has('amateur actor') >= 2) | "
                                        "(yrs_has('background artist') >= 2))"},
 'a voice for the cartoon': {'req': "(yrs_has('professional actor') >= 1) | (has('accents and voices') & "
                                    "((yrs_has('amateur actor') >= 2) | (yrs_has('community-radio presenter') >= "
                                    '2)))'},
 'the stage management team is a person short': {'req': "(yrs_has('stage technician') >= 1) | (yrs_has('drama school "
                                                        "student') >= 1) | (yrs_has('amateur actor') >= 2) | "
                                                        "(yrs_has('community theatre director') >= 2)"},
 'a director is needed for the autumn play': {'req': "(~has('community theatre director') & ((yrs_has('amateur "
                                                     "actor') >= 3) | (yrs_has('drama teacher') >= 3))) | "
                                                     "(yrs_has('community theatre director') >= 3)"},
 'the script competition': {'req': "(yrs_has('novelist') >= 1) | (yrs_has('journalist') >= 1) | (((yrs_has('writing "
                                   "stories') >= 2) | (yrs_has('writing scripts') >= 2)) & (was('amateur actor') | "
                                   "was('community theatre director') | was('drama school student') | "
                                   "was('professional actor')))"},
 'the illusionist players come to town': {'req': "~has('amateur actor') | (yrs_has('amateur actor') >= 1)"},
 'the school needs someone to take drama': {'req': "has('acting') | was('amateur actor') | was('community theatre "
                                                   "director')"}})
# part stage BASE READ
PACK_RULES.setdefault('stage', {}).setdefault('READ', {}).update({'the reviews are in': {'req': "has('professional actor') | has('lead actor or actress') | has('director') | "
                               "has('playwright or screenwriter') | has('amateur actor') | has('community theatre "
                               "director')",
                        'more': ["has('lead actor or actress')", "has('a fringe slot')"],
                        'less': ["~has('lead actor or actress') & has('amateur actor')"]}})
# part stage LONGSHOTS ECHO
PACK_RULES.setdefault('stage', {}).setdefault('ECHO', {}).update({'the same door, years later': {'anchor': "has('a long shot that missed') & had(['the lead from the open queue', "
                                          "'filmed by chance in the street', 'the film you made with friends', 'the "
                                          "old theatre needs someone to save it', 'the late starter', 'the night "
                                          "both covers are off', 'the other side of the table', 'an open audition in "
                                          "the city', 'a voice for the cartoon', 'the stage management team is a "
                                          "person short', 'the old teller dies at midwinter', 'the illusionist "
                                          "players come to town'], 0.08333333333333333) & (ago_fail_long < "
                                          '0.08333333333333333)',
                                'req': "(age >= 21) & ~has('lead actor or actress') & ~has('artistic director')",
                                'more': ["has('acting') | has('writing scripts') | has('directing actors') | "
                                         "has('amateur actor')",
                                         '(hR + hB) > .5',
                                         'time > .4'],
                                'less': ['stress > 1.5', 'money < .15', 'health < .4']},
 'the long shot becomes a story to tell': {'anchor': "has('a long shot that missed') & had(['the lead from the open "
                                                     "queue', 'filmed by chance in the street', 'the film you made "
                                                     "with friends', 'the old theatre needs someone to save it', "
                                                     "'the late starter', 'the night both covers are off', 'the "
                                                     "other side of the table', 'an open audition in the city', 'a "
                                                     "voice for the cartoon', 'the stage management team is a person "
                                                     "short', 'the old teller dies at midwinter', 'the illusionist "
                                                     "players come to town'], 0.08333333333333333) & (ago_fail_long "
                                                     '< 0.08333333333333333)',
                                           'req': "(age >= 25) & ~has('lead actor or actress')",
                                           'more': ['sa > 10',
                                                    "has('teaching') | has('telling a story aloud') | has('acting')",
                                                    '(hW + hG) > .5'],
                                           'less': ['stress > 1.5', 'health < .3']}})
# part stage LONGSHOTS LIFE
PACK_RULES.setdefault('stage', {}).setdefault('LIFE', {}).update({'the lead from the open queue': {'req': "~has('lead actor or actress') & (has('professional actor') | has('voice "
                                         "actor') | has('understudy') | ((yrs_has('amateur actor') >= 5) & has('a "
                                         "lead role to remember')))"},
 'filmed by chance in the street': {'req': "~has('professional actor') & ~has('voice actor') & ((yrs_has('amateur "
                                           "actor') >= 3) | (yrs_has('background artist') >= 3))"},
 'the film you made with friends': {'req': "~has('playwright or screenwriter') & (has('novelist') | "
                                           "has('journalist') | was('amateur actor') | was('community theatre "
                                           "director') | was('professional actor') | was('drama school student'))"},
 'the old theatre needs someone to save it': {'req': "~has('artistic director') & ((yrs_has('director') >= 3) | "
                                                     "(yrs_has('community theatre director') >= 8))"},
 'the late starter': {'req': "~was('professional actor') & ~was('voice actor')"},
 'the night both covers are off': {'req': "~has('lead actor or actress')"},
 'the other side of the table': {'req': "~has('lead actor or actress')"}})
