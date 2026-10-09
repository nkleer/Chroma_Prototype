# Game ideas

Open ideas for the game thread, newest first. Each says what is wrong, why it matters and what could be done.

## Make needs visible and learnable (Emren, 2026-10-09: "we need to do something about that")

**Problem.** New players cannot see how acts in moments change the character's needs (safety, belonging, autonomy,
competence, meaning) or how those needs change over time, so they cannot learn the mechanic.

What the game shows now:
- On an option: "meets X and Y", only the top two needs, only on success, with no size.
- In "What came of it": words such as "lonelier" or "more capable", only when a need moved by about 6 points or more
  and ranks among the week's top changes (`engine_pin/explain.py`, SCALE and the need words).
- The levels themselves: only on the character sheet (c, "The whole character": Inner life and Portrait tabs). The
  main panel has satisfaction, peace, strain, wanting and means, but no needs.
- Terminal: no needs on the status screen (s), only "meets ..." on options.

What stays hidden:
- Needs drain every week unless something feeds them (`engine.py`, `need_drain`), so a need going thin looks random.
- The other ways needs move: acting in one's strongest colors meets autonomy, succeeding at something hard meets
  competence (failing costs some), doing right by dependants meets meaning, deaths and losses cut belonging.
- Needs met is the biggest single driver of satisfaction, and the screen never says so.
- There is no history of which needs rose or fell, or why.

Possible fixes, from smallest to largest:
1. Need pips in the main panel: five icons (shield, people, feather, star, compass) that dim when thin and pulse when
   barely met.
2. Need changes after each choice: every need that moved, with an arrow and amount ("Belonging 42% → 51%").
3. Clearer option rows: "Meets belonging (you're low: big lift to satisfaction)", from how low the need is and how much
   the option meets it.
4. A tooltip per need: what drains it, what fills it, and its trend this year.
5. A one-time hint the first time a need turns thin: needs fade unless something feeds them, and unmet needs pull
   satisfaction down.
6. Terminal parity: a needs line on the status screen (s).

Suggested first step: 1, 2 and 5 together (see the needs, see what changed them, learn the rule).
