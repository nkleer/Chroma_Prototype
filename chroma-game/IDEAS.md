# Game ideas

Open ideas for the game thread, newest first. Each says what is wrong, why it matters and what could be done.

## Player intervention that helps: pushing toward what they need (Emren, 2026-10-09)

**Problem.** The player should be able to help a character meet their needs, and through them raise satisfaction and
peace, even by pushing them to an option they are less than okay with. Today a push almost always costs and rarely
pays back.

What a push does now (`game.py`, GAME settings; the reluctance words come from explain.before's accept levels):
- Reluctance ("would go with it", "okay with it", "reluctant", "against it") lowers the true odds (half-hearted
  effort), adds stress (peace falls), adds pent-up pressure toward what they wanted, and keeps only part of the
  learning (40% at full reluctance). Forcing an out-of-reach option can backfire (stress, money).
- Acting outside their own strongest colors drains autonomy a little.
- Every push counts against "their own" in the end-of-life reading.
- What a push can give: if the option succeeds, its ends meet needs the same way as their own pick would. Nothing
  rewards a push that met a need they lacked, and nothing changes how they feel about the push afterwards.

What it could do:
- **Hindsight.** When a pushed act works and meets a need they lacked, part of the reluctance turns into acceptance
  ("you were right"): the stress and the pent-up pressure ease, the autonomy cost shrinks, and the end-of-life reading
  counts it as a push they came to own rather than one they resented. When it fails or meets nothing they lacked,
  the resentment stays or grows.
- **Ties to the living table** (see "Colors and needs" below). A push that met a need through a color they did not
  trust for it shifts their own color-to-need table: the next time, that option feels less foreign and the reluctance
  is lower. Repeated good pushes become their own way; repeated bad ones make them resist the player more.
- **Show the trade before the push.** At a choice: which lacking need the option would meet, how much that could lift
  satisfaction, against what the push will cost in peace and in "their own". After it: whether the push paid off
  ("They didn't want this, but it gave them the belonging they were missing").
- **Gentler interventions than a push.** Ways to steer without forcing, for example a nudge that lowers reluctance a
  little at a smaller cost, or helping them make a plan aimed at a lacking need (plans are adults only now).
- **A goal for the player.** The end-of-life reading could praise a life where the player's pushes were few, well
  timed and later accepted, so a good guardian differs from a controlling one.

Things to settle: how much hindsight can undo (never all of it, or forcing becomes free); whether acceptance depends
on how content and at peace they are at the time; and how it fits the "their own" score, which now only counts the
reluctance at the moment of the push.

Related: "Colors and needs" (the living table) and "Make needs visible and learnable" below.

## Colors and needs: a shallow, weak, uniform link (Emren, 2026-10-09)

**Problem.** The link between a color's means and ends and the five needs is shallow, weak per act and not very
different from color to color, so which color the player picks hardly changes which need fills. Engine and Library
change (their owners decide); the game would show the result.

How it works now:
- Only an act's **ends** feed needs, and only three of them: safety, belonging and meaning, through one fixed matrix
  (`engine_pin/library.py`, `NEED_MAP_V6`). **Means** feed no need directly; they count only for autonomy (whether the
  act fits the character's own colors) and for odds and access.
- Autonomy and competence are colorless: autonomy comes from acting as oneself, competence from succeeding at
  something hard.

| | White | Blue | Black | Red | Green |
|---|---|---|---|---|---|
| Safety | 0.25 | 0.20 | 0.20 | 0.15 | 0.20 |
| Belonging | 0.15 | 0.10 | 0.15 | 0.30 | 0.30 |
| Meaning | 0.20 | 0.30 | 0.25 | 0.15 | 0.10 |

Every column adds up to 0.6, by design (version 5 had made Black and Blue too strong).

Strength:
- One successful act with pure Red ends adds about 3 points of belonging, less the fuller the need already is
  (`engine.py`, the need update). Safety moves 1.5 to 2.5 points, whatever the color.
- The colorless parts are bigger per act: up to 8 points of autonomy, up to about 7 of competence.
- Needs drain 0.5 points a week, and the surroundings refill about 0.35 of that.
- Ongoing sources dominate over time: commitments (career, partner, children, community, faith; `library.py`
  COMMITMENTS) and resources (money, health, ties, freedom, time) feed needs every week while held.
- A failed act meets nothing and drains only competence. Acting against a color's ends drains its needs at half rate.

Depth: one linear layer, the same for every person, age, culture and setting (`world.py` reuses the matrix). A
White-leaning and a Red-leaning character get the same belonging from a Red act. Age changes only how much each need
counts toward satisfaction. Needs do steer choices: lacking needs make the character want the colors that meet them,
and options that would fill a lacking need get a heart pull.

Diversity:
- Safety is nearly flat (0.15 to 0.25).
- Belonging splits into Red and Green (0.30) against the rest (0.10 to 0.15).
- Meaning leans Blue (0.30) and is weakest for Green (0.10), an odd fit for Green's "place in the whole".
- No color is the only way to any need; the biggest gap on one need is 0.2.

Effect on the player: success, fit with who they are and what they hold long-term matter far more than the color
picked. The "meets X and Y" on options reflects small differences, so it feels weak.

Possible directions:
1. Sharper rows: for example, a clear safety lead for White and Black, a clear meaning lead for White and Blue.
2. A personal layer: let the character's own colors change how much an end satisfies them.
3. Let means count: have means meet some needs too.
4. A living table (Emren, 2026-10-09): instead of one fixed color-to-need table, each character carries their own
   copy that starts from the shared one and changes over the life. Its numbers could be moved by:
   - **Moments:** what came of an act. When a Green act brought real safety, Green counts a little more for safety
     for this person from then on; when it let them down, a little less.
   - **Decisions:** the choices they make and keep making, including forced picks they came to accept or resent.
   - **Habits:** ways of acting used often feel more and more like the way to meet a need ("work is how I feel safe").
   - **Dreams, passions and plans:** what they hope for ties a need to a color (a dream of a big family makes Green
     and Red count more for belonging and meaning).
   - **The outer world:** setting, era, culture and the people around them. A world in war or crisis, a faith, a
     community or a time of plenty changes which colors seem to bring safety, belonging or meaning.
   **The same world, different people** (Emren, 2026-10-09). An outer event should not land the same on everyone. When
   a war breaks out, one character finds a gun and stocks up on pasta (safety through Black and White ways), another
   cries and looks for touch and a hug (belonging through Red and Green ways). The difference comes from each
   character's own color-to-need table: which need the event threatens most for them, and which colors they reach for
   to meet it. The event in turn moves that table (whatever got them through the war counts more afterwards).
   **Where they stand matters too.** How content and at peace the character is when the event hits should shape the
   response: someone settled may take it calmly or reach out to others, while someone already strained or unhappy may
   panic, freeze or harden. So the reaction depends on both the personal table and the state they are in at that moment.
   Things to settle: how fast the numbers drift and how far from the shared table they may go; whether each color's
   total stays at 0.6 or can grow or shrink; whether drift fades back over time; and how the game shows it (a line in
   "What came of it", the character sheet, the end-of-life review). It would also make the personal layer in 2 a
   natural part of the engine rather than a fixed rule.

Related: "Make needs visible and learnable" below.

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
