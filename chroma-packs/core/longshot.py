# Chroma content packs, shared core: the long shot that missed (the anti-story).
# Pathways and packs thread, 2026-10-06. Emren (packs thread, 06:06): "everything can be possible to push, but
# probability to not happen can be so low. But maybe for individuals, this fact would not stop them to try their chance
# and want to be failed anyways: this may create another story (anti-story maybe?)". Fields as in
# chroma-library/earth_perks_titles.py; batch.py reads every core/*.py after reach.py (engine, 06:07).
#
# How the packs use it: every pack title has at least one long shot, an attempt open to anyone, with tiny odds written
# into chance: (or lacking: when the act requires what the person does not have). Its option carries
# `grants_if_fails: a long shot that missed`. Each pack has echoes anchored on the perk: a second try years later, or
# making peace with it. The game stars a failed long shot in the Book of Moments like a rare success and names it in
# the peace reading, because the attempt is a story of its own.
#
# All five colors as ways: rules-keeper, scholar, climber, firebrand and the rooted can each try for the impossible in
# their own way. A small lift (odds .02) for the nerve it leaves behind; it never fades (skill_half None).

PERKS = [
  dict(name="a long shot that missed", kind="standing", ways="W U B R G", odds=.02, skill_half=None, retires=None,
       ages=(12, 110), share=.05,   # estimate: people who once went for a part, a seat or a discovery far beyond their
                                    # odds and missed it; many people try one such thing in a life
       say="once went for something far out of reach, and missed",
       gained="a long shot in any pack: the lead from the open queue, a seat with no party behind you, a discovery "
              "nobody believed; the attempt fails",
       lost="never; a second try that lands keeps it as part of the story",
       needs="the nerve to try"),
]
