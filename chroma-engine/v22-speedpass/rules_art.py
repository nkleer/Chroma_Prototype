# rules_art.py: part 9 of 11 of earth_rules.py, the engine's reading of the Library's words.
# PACK_RULES: the Art and Writing pack.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
# v22.4, the Art and Writing pack (chroma-packs/art/engine-conditions.py, Packs #154), pasted as the packs above
# part art BASE ECHO
PACK_RULES.setdefault('art', {}).setdefault('ECHO', {}).update({'the sketchbook in the attic': {'anchor': "had(['the "
                                                                                                          'urge to '
                                                                                                          'make '
                                                                                                          "something', "
                                                                                                          "'inspiration "
                                                                                                          "strikes'], "
                                                                                                          '0.08333333333333333) '
                                                                                                          '& '
                                                                                                          "has('drawing "
                                                                                                          'and '
                                                                                                          "painting') "
                                                                                                          '& (age >= '
                                                                                                          '30)',
                                                                                                'req': "~has('life-drawing "
                                                                                                       "regular') & "
                                                                                                       "~has('painter "
                                                                                                       "or sculptor') "
                                                                                                       "& ~has('street "
                                                                                                       "artist') & "
                                                                                                       "~has('illustrator "
                                                                                                       "for hire')",
                                                                                                'more': ['(hR + hU) > '
                                                                                                         '.5',
                                                                                                         'time > .5',
                                                                                                         'retired'],
                                                                                                'less': ['stress > 1.5',
                                                                                                         'kids_home > '
                                                                                                         '1',
                                                                                                         'money < .1']},
                                                                'the poems you never showed anyone': {'anchor': "had(['the "
                                                                                                                'first '
                                                                                                                'months '
                                                                                                                'of '
                                                                                                                "retirement', "
                                                                                                                "'your "
                                                                                                                'partner '
                                                                                                                "dies', "
                                                                                                                "'the "
                                                                                                                'notebooks '
                                                                                                                'come '
                                                                                                                "together'], "
                                                                                                                '0.08333333333333333) '
                                                                                                                '& '
                                                                                                                "(has('writing "
                                                                                                                "poems') "
                                                                                                                '| '
                                                                                                                "has('writing "
                                                                                                                "stories'))",
                                                                                                      'req': '(age >= '
                                                                                                             '25) & '
                                                                                                             "~has('open-mic "
                                                                                                             "poet') & "
                                                                                                             "~has('novelist')",
                                                                                                      'more': ['(hR + '
                                                                                                               'hW) > '
                                                                                                               '.5',
                                                                                                               'time > '
                                                                                                               '.4'],
                                                                                                      'less': ['stress '
                                                                                                               '> 1.8',
                                                                                                               'health '
                                                                                                               '< .3']}})
# part art BASE LIFE
PACK_RULES.setdefault('art', {}).setdefault('LIFE', {}).update({'art school applications': {'req': "~was('art school "
                                                                                                   "student') & (age "
                                                                                                   '<= 35)'},
                                                                'a wall that needs a mural': {'req': "(yrs_has('life-drawing "
                                                                                                     "regular') >= 1) "
                                                                                                     "| has('art "
                                                                                                     "school student') "
                                                                                                     "| has('art "
                                                                                                     "teacher')"},
                                                                'the first commission': {'req': "~has('illustrator for "
                                                                                                "hire') & "
                                                                                                "((yrs_has('life-drawing "
                                                                                                "regular') >= 2) | "
                                                                                                "has('art school "
                                                                                                "student') | "
                                                                                                "(yrs_has('street "
                                                                                                "artist') >= 1))"},
                                                                'the first show': {'req': "~has('painter or sculptor') "
                                                                                          "& ((yrs_has('life-drawing "
                                                                                          "regular') >= 4) | "
                                                                                          "(yrs_has('street artist') "
                                                                                          '>= 2) | '
                                                                                          "(yrs_has('illustrator for "
                                                                                          "hire') >= 3) | "
                                                                                          "(yrs_has('art school "
                                                                                          "student') >= 2))"},
                                                                'the school needs an art teacher': {'req': "~has('art "
                                                                                                           "teacher') "
                                                                                                           '& '
                                                                                                           "(has('teacher') "
                                                                                                           "| was('art "
                                                                                                           'school '
                                                                                                           "student') "
                                                                                                           '| '
                                                                                                           "(yrs_has('painter "
                                                                                                           'or '
                                                                                                           "sculptor') "
                                                                                                           '>= 2) | '
                                                                                                           "(yrs_has('illustrator "
                                                                                                           "for hire') "
                                                                                                           '>= 2) | '
                                                                                                           "(yrs_has('street "
                                                                                                           "artist') "
                                                                                                           '>= 2))'},
                                                                'an empty shop on the corner': {'req': "~has('gallery "
                                                                                                       "owner') & "
                                                                                                       "((yrs_has('painter "
                                                                                                       "or sculptor') "
                                                                                                       '>= 3) | '
                                                                                                       "(yrs_has('art "
                                                                                                       "teacher') >= "
                                                                                                       '5) | '
                                                                                                       "(yrs_has('shop "
                                                                                                       "owner') >= 3) "
                                                                                                       '| '
                                                                                                       "(yrs_has('museum "
                                                                                                       "curator') >= "
                                                                                                       '3) | '
                                                                                                       "(yrs_has('illustrator "
                                                                                                       "for hire') >= "
                                                                                                       '5))'},
                                                                'the guild judges your masterpiece': {'req': "~has('master "
                                                                                                             "craftsperson') "
                                                                                                             '& '
                                                                                                             "((yrs_has('craft "
                                                                                                             "maker') "
                                                                                                             '>= 4) | '
                                                                                                             "(yrs_has('carpenter') "
                                                                                                             '>= 6))'},
                                                                'a publisher reads the manuscript': {'req': "has('novelist') "
                                                                                                            '| '
                                                                                                            "(yrs_has('open-mic "
                                                                                                            "poet') >= "
                                                                                                            '2) | '
                                                                                                            "(yrs_has('illustrator "
                                                                                                            'for '
                                                                                                            "hire') >= "
                                                                                                            '2)'},
                                                                'a work in the national collection': {'req': "~has('renowned "
                                                                                                             "artist') "
                                                                                                             '& '
                                                                                                             "((yrs_has('painter "
                                                                                                             'or '
                                                                                                             "sculptor') "
                                                                                                             '>= 5) | '
                                                                                                             "(yrs_has('street "
                                                                                                             "artist') "
                                                                                                             '>= 5) | '
                                                                                                             "(yrs_has('illustrator "
                                                                                                             'for '
                                                                                                             "hire') "
                                                                                                             '>= 5) | '
                                                                                                             "(yrs_has('master "
                                                                                                             "craftsperson') "
                                                                                                             '>= 5))'},
                                                                'a national prize for writing': {'req': "~has('celebrated "
                                                                                                        "author') & "
                                                                                                        "(yrs_has('novelist') "
                                                                                                        '>= 3)'},
                                                                'the painted cave at the winter camp': {'req': "(yrs_has('painter "
                                                                                                               'or '
                                                                                                               "sculptor') "
                                                                                                               '>= 2) '
                                                                                                               '| '
                                                                                                               "(yrs_has('street "
                                                                                                               "artist') "
                                                                                                               '>= 2) '
                                                                                                               '| '
                                                                                                               "(yrs_has('life-drawing "
                                                                                                               "regular') "
                                                                                                               '>= 3) '
                                                                                                               '| '
                                                                                                               "has('art "
                                                                                                               'school '
                                                                                                               "student')"},
                                                                "the carver's mask for the dead": {'req': "(yrs_has('craft "
                                                                                                          "maker') >= "
                                                                                                          '4) | '
                                                                                                          "has('master "
                                                                                                          "craftsperson') "
                                                                                                          '| '
                                                                                                          "has('painter "
                                                                                                          'or '
                                                                                                          "sculptor')"},
                                                                "the queen's portrait sitting": {'req': "(yrs_has('painter "
                                                                                                        "or sculptor') "
                                                                                                        '>= 3) | '
                                                                                                        "(yrs_has('illustrator "
                                                                                                        "for hire') >= "
                                                                                                        '3)'},
                                                                'the illuminated book for the cathedral': {'req': "has('illustrator "
                                                                                                                  'for '
                                                                                                                  "hire') "
                                                                                                                  '| '
                                                                                                                  "has('art "
                                                                                                                  'school '
                                                                                                                  "student') "
                                                                                                                  '| '
                                                                                                                  "(yrs_has('life-drawing "
                                                                                                                  "regular') "
                                                                                                                  '>= '
                                                                                                                  '2)'}})
# part art BASE READ
PACK_RULES.setdefault('art', {}).setdefault('READ', {}).update({'the reviews of the show are in': {'req': "has('painter "
                                                                                                          'or '
                                                                                                          "sculptor') "
                                                                                                          '| '
                                                                                                          "has('renowned "
                                                                                                          "artist') | "
                                                                                                          "has('street "
                                                                                                          "artist') | "
                                                                                                          "has('illustrator "
                                                                                                          "for hire') "
                                                                                                          '| '
                                                                                                          "has('master "
                                                                                                          "craftsperson')",
                                                                                                   'more': ["has('renowned "
                                                                                                            "artist')",
                                                                                                            "has('a "
                                                                                                            'name in '
                                                                                                            'the art '
                                                                                                            "world')"],
                                                                                                   'less': ["~has('a "
                                                                                                            'name in '
                                                                                                            'the art '
                                                                                                            "world') & "
                                                                                                            "~has('a "
                                                                                                            'dealer '
                                                                                                            'who sells '
                                                                                                            'your '
                                                                                                            "work')"]}})
# part art LONGSHOTS ECHO
PACK_RULES.setdefault('art', {}).setdefault('ECHO', {}).update({'the same canvas, years later': {'anchor': "has('a "
                                                                                                           'long shot '
                                                                                                           'that '
                                                                                                           "missed') & "
                                                                                                           "had(['the "
                                                                                                           'sketch '
                                                                                                           'that went '
                                                                                                           'round the '
                                                                                                           "world', "
                                                                                                           "'the open "
                                                                                                           'submission '
                                                                                                           'to the '
                                                                                                           'great '
                                                                                                           'summer '
                                                                                                           "show', "
                                                                                                           "'the "
                                                                                                           'manuscript '
                                                                                                           'in the '
                                                                                                           'pile on '
                                                                                                           'the '
                                                                                                           "floor', "
                                                                                                           "'the late "
                                                                                                           'starter at '
                                                                                                           'the '
                                                                                                           "easel', "
                                                                                                           "'the other "
                                                                                                           'side of '
                                                                                                           'the '
                                                                                                           "easel', "
                                                                                                           "'the judge "
                                                                                                           'stops at '
                                                                                                           'your table '
                                                                                                           'at the '
                                                                                                           'craft '
                                                                                                           "fair'], "
                                                                                                           '0.08333333333333333) '
                                                                                                           '& '
                                                                                                           '(ago_fail_long '
                                                                                                           '< '
                                                                                                           '0.08333333333333333)',
                                                                                                 'req': '(age >= 18) & '
                                                                                                        "~has('renowned "
                                                                                                        "artist') & "
                                                                                                        "~has('celebrated "
                                                                                                        "author')",
                                                                                                 'more': ["has('drawing "
                                                                                                          'and '
                                                                                                          "painting') "
                                                                                                          '| '
                                                                                                          "has('writing "
                                                                                                          "poems') | "
                                                                                                          "has('writing "
                                                                                                          "stories')",
                                                                                                          '(hR + hB) > '
                                                                                                          '.5',
                                                                                                          'time > .4'],
                                                                                                 'less': ['stress > '
                                                                                                          '1.5',
                                                                                                          'money < .15',
                                                                                                          'health < '
                                                                                                          '.4']},
                                                                'the long shot becomes a class to teach': {'anchor': "has('a "
                                                                                                                     'long '
                                                                                                                     'shot '
                                                                                                                     'that '
                                                                                                                     "missed') "
                                                                                                                     '& '
                                                                                                                     "had(['the "
                                                                                                                     'sketch '
                                                                                                                     'that '
                                                                                                                     'went '
                                                                                                                     'round '
                                                                                                                     'the '
                                                                                                                     "world', "
                                                                                                                     "'the "
                                                                                                                     'open '
                                                                                                                     'submission '
                                                                                                                     'to '
                                                                                                                     'the '
                                                                                                                     'great '
                                                                                                                     'summer '
                                                                                                                     "show', "
                                                                                                                     "'the "
                                                                                                                     'manuscript '
                                                                                                                     'in '
                                                                                                                     'the '
                                                                                                                     'pile '
                                                                                                                     'on '
                                                                                                                     'the '
                                                                                                                     "floor', "
                                                                                                                     "'the "
                                                                                                                     'late '
                                                                                                                     'starter '
                                                                                                                     'at '
                                                                                                                     'the '
                                                                                                                     "easel', "
                                                                                                                     "'the "
                                                                                                                     'other '
                                                                                                                     'side '
                                                                                                                     'of '
                                                                                                                     'the '
                                                                                                                     "easel', "
                                                                                                                     "'the "
                                                                                                                     'judge '
                                                                                                                     'stops '
                                                                                                                     'at '
                                                                                                                     'your '
                                                                                                                     'table '
                                                                                                                     'at '
                                                                                                                     'the '
                                                                                                                     'craft '
                                                                                                                     "fair'], "
                                                                                                                     '0.08333333333333333) '
                                                                                                                     '& '
                                                                                                                     '(ago_fail_long '
                                                                                                                     '< '
                                                                                                                     '0.08333333333333333)',
                                                                                                           'req': '(age '
                                                                                                                  '>= '
                                                                                                                  '25) '
                                                                                                                  '& '
                                                                                                                  "~has('renowned "
                                                                                                                  "artist') "
                                                                                                                  '& '
                                                                                                                  "~has('celebrated "
                                                                                                                  "author')",
                                                                                                           'more': ['sa '
                                                                                                                    '> '
                                                                                                                    '10',
                                                                                                                    "has('teaching') "
                                                                                                                    '| '
                                                                                                                    "has('art "
                                                                                                                    "teacher') "
                                                                                                                    '| '
                                                                                                                    "has('pupils "
                                                                                                                    'who '
                                                                                                                    'remember '
                                                                                                                    "you')",
                                                                                                                    '(hW '
                                                                                                                    '+ '
                                                                                                                    'hG) '
                                                                                                                    '> '
                                                                                                                    '.5'],
                                                                                                           'less': ['stress '
                                                                                                                    '> '
                                                                                                                    '1.5',
                                                                                                                    'health '
                                                                                                                    '< '
                                                                                                                    '.3']}})
# part art LONGSHOTS LIFE
PACK_RULES.setdefault('art', {}).setdefault('LIFE', {}).update({'the sketch that went round the world': {'req': "~has('painter "
                                                                                                                'or '
                                                                                                                "sculptor') "
                                                                                                                '& '
                                                                                                                "((yrs_has('life-drawing "
                                                                                                                "regular') "
                                                                                                                '>= 2) '
                                                                                                                '| '
                                                                                                                "(yrs_has('street "
                                                                                                                "artist') "
                                                                                                                '>= 2) '
                                                                                                                '| '
                                                                                                                "(yrs_has('illustrator "
                                                                                                                'for '
                                                                                                                "hire') "
                                                                                                                '>= '
                                                                                                                '2))'},
                                                                'the open submission to the great summer show': {'req': "~has('renowned "
                                                                                                                        "artist') "
                                                                                                                        '& '
                                                                                                                        "((yrs_has('painter "
                                                                                                                        'or '
                                                                                                                        "sculptor') "
                                                                                                                        '>= '
                                                                                                                        '2) '
                                                                                                                        '| '
                                                                                                                        "(yrs_has('life-drawing "
                                                                                                                        "regular') "
                                                                                                                        '>= '
                                                                                                                        '5))'},
                                                                'the manuscript in the pile on the floor': {'req': "~has('celebrated "
                                                                                                                   "author') "
                                                                                                                   '& '
                                                                                                                   "((yrs_has('open-mic "
                                                                                                                   "poet') "
                                                                                                                   '>= '
                                                                                                                   '2) '
                                                                                                                   '| '
                                                                                                                   "(yrs_has('novelist') "
                                                                                                                   '>= '
                                                                                                                   '3))'},
                                                                'the late starter at the easel': {'req': "~was('painter "
                                                                                                         'or '
                                                                                                         "sculptor') & "
                                                                                                         "(yrs_has('life-drawing "
                                                                                                         "regular') >= "
                                                                                                         '2)'},
                                                                'the other side of the easel': {'req': "~has('gallery "
                                                                                                       "owner') & "
                                                                                                       "((yrs_has('painter "
                                                                                                       "or sculptor') "
                                                                                                       '>= 3) | '
                                                                                                       "(yrs_has('illustrator "
                                                                                                       "for hire') >= "
                                                                                                       '3) | '
                                                                                                       "(yrs_has('art "
                                                                                                       "teacher') >= "
                                                                                                       '3))'},
                                                                'the judge stops at your table at the craft fair': {'req': "~has('renowned "
                                                                                                                           "artist') "
                                                                                                                           '& '
                                                                                                                           "((yrs_has('craft "
                                                                                                                           "maker') "
                                                                                                                           '>= '
                                                                                                                           '3) '
                                                                                                                           '| '
                                                                                                                           "(yrs_has('master "
                                                                                                                           "craftsperson') "
                                                                                                                           '>= '
                                                                                                                           '5))'}})
# ---- end of pasted pack conditions


