# rules_callings.py: part 10 of 11 of earth_rules.py, the engine's reading of the Library's words.
# PACK_RULES: the Five Callings pack.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
# v24, the Five Callings (chroma-packs/callings/engine-conditions.py, Packs 10-19), pasted as the packs above at the
# joint refit, when callings joined batch.PACKS
# part callings BASE LIFE
PACK_RULES.setdefault('callings', {}).setdefault('LIFE', {}).update({'the congregation needs a senior minister': {'req': "~has('senior cleric') & (age >= 35) & ((yrs_has('ordained "
                                                     "religious minister') >= 6) | (yrs_has('member of a monastic "
                                                     "community') >= 8))"},
 'the order chooses its head': {'req': "~has('head of a faith order') & (age >= 45) & ((yrs_has('senior cleric') >= 6) "
                                       "| (yrs_has('member of a monastic community') >= 15))"},
 'the prototype works': {'req': "~has('inventor') & (has('prototyping') | has('fixing things')) & ((yrs_has('software "
                                "developer') >= 2) | (yrs_has('civil engineer') >= 2) | (yrs_has('machinist') >= 2) | "
                                "(yrs_has('electrician') >= 2) | (yrs_has('founder of a firm') >= 1) | "
                                "(yrs_has('apprentice') >= 2))"},
 'an invention in every home': {'req': "~has('celebrated inventor') & (yrs_has('inventor') >= 4)"},
 'the board needs a chief executive': {'req': "~has('chief executive') & (age >= 28) & ((yrs_has('founder of a firm') "
                                              ">= 3) | (yrs_has('shop owner') >= 4) | (yrs_has('café or bar owner') >= "
                                              "4) | (yrs_has('shift manager') >= 6))"},
 'a rival firm is for sale': {'req': "~has('magnate') & ((yrs_has('chief executive') >= 4) | (yrs_has('founder of a "
                                     "firm') >= 8))"},
 'officer selection': {'req': "~was('army officer') & (age >= 20) & (age <= 40) & ~has('someone with a record') & "
                              "((yrs_has('soldier') >= 2) | has('graduate') | has('national service done'))"},
 'the army needs a new general': {'req': "~has('general') & (yrs_has('army officer') >= 12)"},
 'the ward needs someone in charge': {'req': "~has('senior nurse or midwife') & ((yrs_has('nurse') >= 4) | "
                                             "(yrs_has('midwife') >= 4))"},
 'patients come from far away': {'req': "~has('renowned healer') & ((yrs_has('senior nurse or midwife') >= 4) | "
                                        "(yrs_has('midwife') >= 10) | (yrs_has('nurse') >= 12) | (yrs_has('physician') "
                                        ">= 10) | (yrs_has('complementary therapist') >= 12))"},
 'the god speaks in the temple': {'req': "~has('head of a faith order') & ((yrs_has('senior cleric') >= 3) | "
                                         "(yrs_has('ordained religious minister') >= 10))"},
 'the guild commissions a flying ship': {'req': "~has('celebrated inventor') & ((yrs_has('inventor') >= 3) | "
                                                "(yrs_has('civil engineer') >= 6) | (yrs_has('machinist') >= 6))"},
 'a seat among the merchant princes': {'req': "~has('magnate') & ((yrs_has('chief executive') >= 3) | "
                                              "(yrs_has('founder of a firm') >= 6))"},
 'the war leader is chosen at the gathering': {'req': "~has('general') & (((yrs_has('army officer') >= 6) & (age >= "
                                                      "40)) | (yrs_has('soldier') >= 12))"},
 'the sickness in the winter camp': {'req': "(yrs_has('nurse') >= 2) | (yrs_has('midwife') >= 2) | has('senior nurse "
                                            "or midwife')"}})
# part callings LONGSHOTS LIFE
PACK_RULES.setdefault('callings', {}).setdefault('LIFE', {}).update({'a sermon that goes round the country': {'req': "~has('senior cleric') & (((yrs_has('ordained religious minister') >= "
                                                 "3) & (age >= 35)) | (yrs_has('lay religious teacher') >= 5) | "
                                                 "(yrs_has('street preacher') >= 3))"},
 'the garage invention': {'req': "~was('inventor') & (has('fixing things') | has('prototyping')) & "
                                 "((yrs_has('apprentice') >= 1) | (yrs_has('machinist') >= 1) | "
                                 "(yrs_has('electrician') >= 1) | (yrs_has('software developer') >= 1) | "
                                 "(yrs_has('repair-cafe volunteer') >= 2) | has('workshop'))"},
 'the market stall that became a chain': {'req': "~has('chief executive') & ((((yrs_has('shop owner') >= 2) | "
                                                 "(yrs_has('café or bar owner') >= 2)) & (age >= 28)) | (yrs_has('shop "
                                                 "assistant') >= 4))"},
 'the field commission': {'req': "~was('army officer') & (yrs_has('soldier') >= 3) & (age <= 45)"},
 'the remedy that worked': {'req': "~has('renowned healer') & ((yrs_has('nurse') >= 3) | (yrs_has('midwife') >= 3) | "
                                   "(yrs_has('complementary therapist') >= 3) | has('senior nurse or midwife'))"}})
# part callings LONGSHOTS ECHO
PACK_RULES.setdefault('callings', {}).setdefault('ECHO', {}).update({'the calling, years later': {'anchor': "has('a long shot that missed') & had(['a sermon that goes round the country', "
                                        "'the garage invention', 'the market stall that became a chain', 'the field "
                                        "commission', 'the remedy that worked'], 0.08333333333333333) & (ago_fail_long "
                                        '< 0.08333333333333333)',
                              'req': "(age >= 20) & ~has('head of a faith order') & ~has('celebrated inventor') & "
                                     "~has('magnate') & ~has('general') & ~has('renowned healer')",
                              'more': ['(hR + hB) > .5',
                                       'time > .4',
                                       "has('mentor') | has('old comrades') | has('investors who back you')"],
                              'less': ['stress > 1.5', 'money < .15', 'health < .4']},
 'the long shot becomes a life of service': {'anchor': "has('a long shot that missed') & had(['a sermon that goes "
                                                       "round the country', 'the garage invention', 'the market stall "
                                                       "that became a chain', 'the field commission', 'the remedy that "
                                                       "worked'], 0.08333333333333333) & (ago_fail_long < "
                                                       '0.08333333333333333)',
                                             'req': "(age >= 25) & ~has('head of a faith order') & ~has('celebrated "
                                                    "inventor') & ~has('magnate') & ~has('general') & ~has('renowned "
                                                    "healer')",
                                             'more': ['sa > 10',
                                                      '(hW + hG) > .5',
                                                      'has(\'teaching\') | has(\'mentor\') | has("apprentice of one\'s '
                                                      'own")'],
                                             'less': ['stress > 1.5', 'health < .3']}})
# ---- end of pasted pack conditions
