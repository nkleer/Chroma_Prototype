# Proposal for the engine: needs, colors and steering

From the game thread, 2026-10-09, for the engine owner (and the Library for item 2). It covers the parts of the ideas in
`chroma-game/IDEAS.md` that the game cannot build on its own side, because they change rules inside the engine's week.
Line numbers refer to the game's pinned copy, `chroma-game/prototype/engine_pin/engine.py`.

What the game already does on its own side (no engine change):
- Shows needs: levels in the side panel, the needs a choice's week moved, which lacking need an option would feed, a
  one-time hint, a needs line on the terminal status.
- Hindsight and trust per color: after a push, the game judges it (accepted, resented or neither), undoes part of an
  accepted push's costs, and keeps the character's trust in the player per color. Trust spares some of a push's
  resentment; distrust adds to it. All through the existing pause points (`learn` and `end`), changing `stress`, `Q`
  and `need` in place, as the forced-pick costs already do.

Everything below needs the engine.

## 1. A living color-to-need table, one per person

**Why.** Today one fixed table (`NMAP`, from `library.NEED_MAP_V6`) says how much each color's ends feed safety,
belonging and meaning, the same for every person, age and setting. Emren (2026-10-09) wants it to be each character's
own and to change over the life, moved by moments, decisions, habits, dreams and the outer world. It also carries the
"same world, different people" idea: in a war one character reaches for safety through Black and White, another for
belonging through Red and Green.

**Where `NMAP` is used now:**
- line 931: chosen once per run (`NMAP_V6` or `NMAP_V5`).
- line 2384: `serves`, the needs each option would meet (the heart's "relief" pull).
- lines 2683 to 2699: the weekly need update (drain and niche supply, an act's ends on success, acting against an end,
  duty's meaning).
- line 3181: `felt`, which colors' ends could meet what is lacking (it shapes the want).
- line 3331: what a dream is about follows what its ways serve.
- `world.py` line 91 and 446: the world's own copy (`NEED_MAP`, `NEEDM`).
- `explain.py`: reads `NMAP` for its need words; `foresee.py` likewise where it scores plans.

**Proposal.**
- State: `NM`, shape (N, needs, colors), starting from the shared table (`NM[:] = NMAP`). Add it to `STATE` so
  `explain.py`, `foresee.py` and the game read the person's own table.
- Replace each use above with the person's table (`np.einsum("njc,nc->nj", NM, ends)` in place of `ends @ NMAP.T`).
- Weekly drift, small and bounded:
  - **Moments:** after an act, compare the need it fed with what the person's table expected. Where a color's end
    fed a need more than expected, that cell grows a little; where it let them down, it shrinks
    (`NM[n, j, c] += lr_m * stakes * ends[c] * (got[j] - expected[j])`).
  - **Habit and decisions:** a slow pull of each need's row toward the colors the person keeps using when that need
    is lacking (`lr_h`).
  - **Dreams, passions and plans:** a held goal ties its colors to the needs of its domain (`KPAY` of its kind),
    weighted by its strength (`lr_g`).
  - **The outer world:** an event that threatens a need (war: safety; a death: belonging) strengthens the cells of the
    colors the person turned to and that worked, through the same "moments" rule; an era's norms pull the table a
    little toward the era's colors for the needs its message speaks to (`lr_w`, times exposure and acceptance, as the
    era's pull on the want does now at line ~3202).
  - **Limits:** each cell stays within a band of the shared value (for example 0.5x to 2x), each color's column is
    renormalised to the shared total (0.6) so no color gets stronger overall, and the table drifts back toward the
    shared one slowly (`back`, a half-life of some years) unless kept up.
- Settings (new `P` keys, all 0 keeps today's behaviour exactly): `nm_lr_moment`, `nm_lr_habit`, `nm_lr_goal`,
  `nm_lr_world`, `nm_band`, `nm_back`.

**What to check.** With every rate at 0, `run_steps()` gives exactly the same lives (the game's `test/same_life.py`).
With rates on: the table's spread across people grows with age; characters with the same start diverge in which
colors they use for a lacking need; no column total changes; satisfaction and peace distributions stay within the
calibrated bands (`test/peace_bands.py`).

## 2. Sharper base table (Library)

**Why.** In `NEED_MAP_V6` safety is nearly flat (0.15 to 0.25), the biggest gap between two colors on one need is 0.2,
and Green feeds meaning least (0.10), an odd fit for "place in the whole". The color picked hardly changes which need
fills.

**Proposal.** Keep each column at 0.6 (the v6 fairness rule) but widen the rows. One example, for discussion:

| | White | Blue | Black | Red | Green |
|---|---|---|---|---|---|
| Safety | 0.30 | 0.20 | 0.30 | 0.05 | 0.15 |
| Belonging | 0.10 | 0.05 | 0.05 | 0.35 | 0.30 |
| Meaning | 0.20 | 0.35 | 0.25 | 0.20 | 0.15 |

**What to check.** Need levels stay in the calibrated range (v6: about 0.6 to 0.9), and no color's lives end with
lower fulfilment or serenity on average than today.

## 3. Means that feed needs

**Why.** Only an act's ends feed safety, belonging and meaning; its means (how it is done) feed none directly.

**Proposal.** In the weekly need update (line 2685), feed needs from a mix of ends and means:
`(1 - mean_w) * ends + mean_w * means` with a new `P["mean_w"]` (0 keeps today's rule; 0.25 to try). Apply the same
mix in `serves` (line 2384) so the heart's pull and the game's "meets" match.

## 4. Outer events land by need and by state

**Why.** An event should not land the same on everyone (IDEAS.md, "The same world, different people"). How content and
at peace the character is when it hits should shape the response.

**Proposal.**
- Give each read event and crisis a need it threatens (a `threat` vector over needs; war and disaster: safety; a
  death: belonging; a scandal or a lost faith: meaning). Library data, defaulting to none.
- When it lands (the read-event block around line 3140): the hit is scaled by how lacking that need already is, and
  the colors the person reaches for are drawn from their own row of `NM` for the threatened need (feeding the want, as
  `take_in` does now).
- State shapes the reaction: high peace and satisfaction damp the stress it adds and favour reaching out (belonging
  colors); low peace or high strain amplify it and favour self-protection (safety colors). A new `P["ev_state_k"]`
  (0 keeps today's rule).

## 5. A light steer (the player bends the choice instead of replacing it)

**Why.** IDEAS.md, "Character, player and outer world": the player should be able to tilt the character's own pick
toward a color with a chosen strength, not only replace it. The game cannot do this: the pick is drawn before the
`choose` pause, which can only replace it.

**Proposal.** A live setting the engine reads each week, as it already reads `P["self_death"]`:
`P["steer"]`, a vector over colors (0 = none). When set, the option utilities get `+ steer_k * (m[k] @ steer)` before
the pick is drawn, then the engine clears it. Report back, at the `choose` pause, how much the steer moved the chosen
option's probability (`steer_moved`), so the game can cost it: a light steer that only tipped a close call costs
little; one that overturned a clear preference costs like a push.

**Also useful:** the era's current pull as a color vector in `STATE` (it exists inside the week as the era's message,
`e_p`), so the game can show "steering with the times" as cheaper than against them, and the world object's schedule
of coming eras (if it has one) for a little foresight.

## 6. Trust and habit

**Why.** IDEAS.md, "Color inertia and trust": a push the character came to accept should become their own. The game
already lets trust soften the learning loss of a reluctant act (the `learn` pause's delta). But habit, the 30% of
what holds a person, grows inside the week (`habit += ... ma`) and the game cannot scale it.

**Proposal.** A live `P["habit_take"]` (default 1) the engine multiplies into this week's habit increment, which the
game sets at the `choose` pause for a pushed act (less than 1 when resented, 1 when trusted). Or: return a habit factor
alongside `delta` at the `learn` pause.

## Not in this proposal

The inner voice (the character discovering the player, asking for help, counter-offers, opening up) and inner support
actions are still being discussed (Emren, 2026-10-09) and are not proposed here.
