# Game ideas

Open ideas for the game thread, newest first. Each says what is wrong, why it matters and what could be done.

## The inner voice: how the character comes to know the player (Emren, 2026-10-09)

**Goal.** Make the player-character relationship richer without making the character depend on the player. The
character lives their own life first. Only over time may they notice that the voice inside them can be talked to,
negotiated with, and leaned on, or argued with and ignored.

### Discovering the voice

The character does not start out knowing the player is there.
- **At first** the player's steers feel like the character's own hunches. Nothing talks back, and the character does
  not ask for anything.
- **Over time** the character may notice the voice. A hidden awareness grows with age and with how the player's steers
  turned out (see "Color inertia and trust" below), and stages unlock in order:
  1. **Noticing:** the story marks it once ("*That wasn't quite my own thought.*").
  2. **Asking for help:** at hard moments, when the heart and head disagree or the odds are poor, the character may
     turn to the voice. A steer they asked for costs less and builds trust. What they ask for follows their colors:
     Blue asks for information, White for guidance, Red for permission, Black only when cornered, Green when the world
     feels too big.
  3. **Negotiating:** when the player steers strongly, the character can answer with a counter-offer, an option that
     mixes the player's color with theirs ("*I'll take the job, but not in another city.*").
  4. **Opening up:** parts of the inner life stay hidden from the player until trust grows (secret dreams, fears,
     something they hide from the world; the engine already models hiding and coming out). The character sheet fills
     in as they open up.
- **It can go the other way.** A character the voice has hurt may stop listening, argue back, or refuse light steers.
  Some characters never discover the voice at all.

### Inner support

Actions on how the character feels, not on which option they take. Cheaper than a steer, and they never cause a
rebellion. Each acts on a value the engine already has:

| Action | What it does | Engine value |
|---|---|---|
| Encourage | raises belief in a color before a hard try | belief per color (`SE`) |
| Calm | lowers strain after a blow | `stress` |
| Remind | brings back a dream or value they are drifting from | goal strength (dreams, passions, plans) |
| Tell the truth | moves felt odds toward the real odds when hope or gloom distorts them | `outlook` and the felt odds |
| Stay with them | the player watches a grief or crisis instead of skipping it | `support` (being cared for) |

How it could work:
- **Small and temporary.** Each action is a nudge that fades back over weeks, unless the character's own life
  confirms it (encouragement before a try that succeeds sticks, because success raises belief anyway).
- **Received according to who they are.** The effect is scaled by awareness and trust, and by color: Blue takes the
  truth, Red takes encouragement and company, White takes reminders of duty, Black accepts little that is not useful,
  Green takes calm. Before the character notices the voice, support works only weakly, as a passing feeling.
- **A limited budget.** A few actions per year, so the player chooses when it matters.
- **No dependence.** Leaning on the voice too often slows the character's own coping: their discipline and steadiness
  grow less than they would have. A character who was supported well but sparingly ends up stronger than one who was
  carried.

### Who the player is to them

How the character understands the voice depends on the setting and on who they are:
- Modern Earth: intuition, an inner voice, a conscience.
- Tribal world: a spirit, an ancestor.
- World of magic: a patron, a familiar.

That understanding changes how they respond. A believer may obey a spirit; a sceptic may distrust a voice; a Blue
character may want to understand it; a Black one may try to use it. Their faith and colors decide which reading they
take, and it can change over the life.

### A last conversation

At the end of a life, the character speaks to the voice: what it gave them, what it cost them, and whether they were
glad of it. The words come from the relationship as it ended (awareness, trust per color, the steers they came to
accept or resented) and become part of the end-of-life reading. A character who never noticed the voice has no
conversation; the reading says so in a line.

### Not taken for now

- The character knowing things the player does not (how others really feel, rumors). Not now.
- Promises between player and character, shared memories of past steers, and making amends. Not in that form.
- Life stages that make the player a parent in childhood: it would make the character depend on the player early.

Related: "Character, player and outer world" and "Player intervention that helps" below.

## Character, player and outer world: three forces that shape a life (Emren, 2026-10-09)

**Goal.** Make choices matter and give the game more variety by letting three elements act on each other:

- **The character** is where the game is played: their colors, needs, means, habits, satisfaction and peace.
- **The player** steers: they can bend the character's course at moments, within limits.
- **The outer world** is the largest force: setting, era, culture, the people around them and outer events.

A moment is where the three meet. The world sets the situation, the character's colors make some responses easy and
others hard, and the player decides how far to bend the response. (Emren's image: the character is a car moving
through the world, and the player can make it drift. The image explains the idea; the game itself does not need to
use driving words.)

Most of the parts exist in the engine already. What is missing is that the player's control has only two settings:
let the character choose, or push them to another option.

### The character

- Colors now: what they naturally do.
- What holds them (deep nature 40%, habit 30%, roles 30% on the character sheet): how hard they are to change. Young
  characters change easily; older ones slowly (the sheet's "Speed").
- Needs: what must be fed. Satisfaction: how good life feels. Peace: how much room they have to bend before something
  gives. Strain and pent-up wanting: pressure that can break through.
- Skill and belief per color: how well they act in each color's ways.

### The outer world

- Era norms: a pull toward some colors that everyone feels.
- How the world sets colors against each other: holding both sides at once creates inner tension.
- Surroundings (family, place, culture): what is normal and easy where they live.
- Outer events (war, crisis, festivals, news): moments the world brings to them.
- Open and closed options: some opportunities close for good once passed.

### The player: bending instead of pushing

Replace the single push with a steer of chosen strength toward a color:
- **A light steer** tilts the character's own pick toward that color. Cheap, usually accepted, autonomy kept.
- **A strong steer** takes another option. It costs peace, adds strain and builds pent-up wanting.
- **Too much** backfires: stress, failure, or a rebellion where the pent-up wanting breaks out toward the opposite
  color.

How far the player can steer safely depends on:
- **The character:** their peace, and how strongly they hold their current colors.
- **The world:** steering with the era's pull is cheap; steering against it is expensive.
- **The bond with the player:** see "Trust" below.

The world can also open windows. A big event in a color makes a move toward that color nearly free if the player
times it well: during a war, a Black or White steer costs little and a Green one costs a lot.

### How each pair interacts

**Character and world: fit.** A Red character in a Red era is carried along; a White character in the same era works
against it. The screen could show the world's colors over the coming years and where the character fits or clashes.
This is also where "the same world, different people" belongs (see "Colors and needs" below): the world is the same
for everyone, but each character's own color-to-need table decides which need an event threatens and which colors they
reach for.

**Player and character: trust per color.** The character learns the player. Steers in a color that turned out well
(see "Hindsight" in the entry below) build trust in that color, and later steers there meet less resistance. Steers
that hurt them build resentment, and later steers there backfire sooner. The heart and the head are already two
voices in the inner voice; the player becomes a third one the character comes to trust or resist ("*Last time you
were right.*"). Over a life the player gets colors of their own, from how they tend to steer; the end-of-life reading
can say how the player's style and the character got along.

**Player and world: foresight.** The player sees a little further than the character: a few half-hidden signs of what
is coming (an era turning, a war likely, an opportunity about to close). Good play is acting early: getting into
position before an option closes, or building up a need before a hard stretch (belonging before a long loss, safety
before a likely crash).

### Making choices matter

- **Closed options stay closed.** A missed opportunity is gone, and the life remembers the paths taken. Closed
  options and lost dreams exist in the engine; show them as paths not taken.
- **Momentum.** Each act in a color makes the next one easier (habit, skill) and the opposite one harder, so early
  steers shape the rest of the life.
- **Quiet years for building.** Between moments the player could invest instead of steering: practise a color's
  skill, raise belief, set a plan, feed a need. Slow, but with no backfire risk.
- **People as a safety net.** With friends and family close, a backfire becomes a recovery (the engine's heal loop);
  without them it becomes a crisis that hardens them.
- **Lives in a line.** A grandchild inherits the world as it was left and the player's reputation with the family.

### The five colors as ways of steering

Steering is itself a color choice:

| | Way of steering | Strong in | Weak in |
|---|---|---|---|
| White | steady, by the rules | duties, crises (safety) | sudden opportunities |
| Blue | plan ahead | foresight, long plans | emotional moments (grief, love) |
| Black | take the opening | windows, power moves | trust (it is lost fast) |
| Red | follow the feeling | passion, belonging | peace (it adds strain) |
| Green | go with the world | riding the era's pull | going against the era |

How the player tends to steer becomes the player's own colors. A character whose colors match finds them easier to
trust.

### Color inertia and trust: two separate things

They answer different questions and should stay apart:

- **Color inertia: how hard is the character to change?** Their own resistance to changing color, whoever or
  whatever pushes. Built from deep nature, habit and roles. Moved by every act, the world, age and commitments. Its
  cost is **effort**: lower odds, strain, slower change.
- **Trust (hindsight): how do they feel about the one who pushed?** Their relationship with the player, per color.
  Built only from how the player's steers turned out. Its cost is **resentment**: pent-up backlash, lost autonomy, a
  lower "their own" score.

Splitting the costs keeps them clear:
- High inertia, high trust: "I trust you, but this is hard for me." They go along willingly, and it still takes effort.
- Low inertia, low trust: "This would be easy, but not because you say so." Cheap to do, but they resent it.
- A world event with no player steer moves inertia only; trust does not change.

They meet at one point, so nothing is counted twice:
- **A steer they came to accept becomes their own.** It counts fully toward habit, like their own pick (today a
  reluctant act keeps only part of its learning). So trust lowers inertia over time, but only through the existing
  habit path.
- **A steer they resented stays foreign.** It adds less to habit, and the pent-up wanting pulls back toward their old
  colors, so inertia toward those colors stays or grows.

Trust lowers resentment at once; once a steer is accepted, it slowly lowers inertia too.

### Where to start

1. Steer instead of push: a light or strong steer toward a color, with a visible limit.
2. Trust per color, built by steers that paid off (the hindsight idea below).
3. The world's pull over the coming years: steering with the era is cheap, against it expensive. Shown on the existing
   life timeline.

Related: "Player intervention that helps", "Colors and needs" (the living table) and "Make needs visible and learnable"
below.

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
- **Not the same as color inertia.** Hindsight builds trust in the player; inertia is the character's own resistance
  to change. See "Color inertia and trust" in the entry above for how they differ and where they meet.
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
