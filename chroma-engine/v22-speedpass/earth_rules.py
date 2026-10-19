"""Engine-side reading of the Library's modern Earth batch (chroma-library/earth.py, approved by Emren 2026-10-05 05:11).

The Library writes when an inner moment, an echo or an outside event comes in plain words (trigger: requires / likelier /
rarer; after + delay_years; timing). The engine reads those words through the conditions below, written in the engine's
own vocabulary (see COND_VOCAB in batch.py). Parts the engine cannot see (a song on the radio, a friend's promotion this
week) stay in the situation's rate: the condition only says when the moment is possible at all.

Each entry: req (must hold), more (each true clause makes it likelier), less (each true clause makes it rarer).
Echoes also have an anchor: what starts the clock (a mark, a commitment, a stretch of life). The delay window is the
Library's delay_years. Expressions are numpy expressions over one row per person; use & | ~ and parentheses.
"""

# The tables live in the files of RULES_PARTS, one stretch each, unchanged; parts.join puts them back in order and
# they run here, in this module's own namespace, so every name, dict and key order is what it was.
RULES_PARTS = ('rules_moments', 'rules_drivers', 'rules_titles', 'rules_perks', 'rules_norms',
               'rules_chance', 'rules_more', 'rules_packs', 'rules_art', 'rules_callings', 'rules_world')
exec(compile(*__import__("parts").join(RULES_PARTS, __file__), "exec"), globals())   # no module-level name: see parts.py
