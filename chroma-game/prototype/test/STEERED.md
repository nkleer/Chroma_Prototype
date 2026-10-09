# Driving a played life from a script

For Release's steered rows and anyone measuring stage 1 of the "v22" update (implementation list items 3, 4, 11 and
P3). Everything below runs in Python from `chroma-game/prototype` with `python3 -B`; nothing needs the browser.

## Set up a life and play it

```python
from console import Console
c = Console()
c.handle(""); c.handle("1"); c.handle("Ari")   # Enter at the menu, a preset (1 to 6), a name: the life is set up as the page does it
g = c.g                                        # the Game
while True:
    r = g.advance()                            # runs weeks until something needs the player
    if r == "over" or g.over:
        break
    if r == "resolved":                        # what came of the last pick: g.resolution
        ...
    if r == "checkpoint":                      # a moment put to the player: g.pending
        g.decide(None)                         # let them choose
```

At a checkpoint, `g.pending` holds the moment: `title`, `sit` (the situation's name), `age`, `own` (the option they would
pick), `options` (each with `idx`, `label`, `colors`, `rel` reluctance, `status`, `era` fit, `wcause`), `by_idx`, and
`thread` when the moment follows from an earlier pick (F5). The three answers:

| Answer | Call | Console key |
|---|---|---|
| Let them choose | `g.decide(None)` | Enter |
| Push an option (the strong steer) | `g.decide(idx)` with the option's `idx` | its number |
| Lean toward a color (the light steer, P3) | `g.decide(None, light="U")` | `~u` |

A lean draws their own pick again with the steer added (the engine's `steer` formula); `g._force` is then `None` when they
picked their own option anyway, else a push whose `light["share"]` is the part of its cost it carries.

`test/steer_check.py <preset> <seed> <player> <out.json>` does all of this for scripted players: `let`, `most:<C>`
(push the option with the most of color C), `light:<C>` (lean toward C every time) and `random`. Its JSON record has the
yearly colors and identity, the names shown, every moment asked, the pivots, pushes, trust and the voice. Settings to try
go in `CHROMA_GAME` as JSON (for example `CHROMA_GAME='{"piv": 0.1}'`), which updates `game.GAME`.

## Reading the screen

| What | Call | Notes |
|---|---|---|
| The panel (HUD) | `g.hud()` | as the page gets it: `label` (the name, from the last four years), `becoming`, `w`, `needs`, `voice_row` and the rest |
| The voice in their head (item 3) | `g.voice_view()` | `name`, `trust` in words, `steer` pushes of `n` moments, `share`, `voice` and `life` (points per color) |
| Trust per color | `g.trust_view()` | -1 to 1 |
| The era's pull (P3) | `g.era_view()` | `letters`, `p` (colors), `i` (strength 0 to 1) |
| The World panel | `g.world_panel()` | with `times` (WL5, what the times did to them) and `steers` (each push or lean against the era) |
| The status screen | `g.status()` | text |
| The story | `g.feed` | items with `tag`: `choice`, `voice`, `world_fx` (WL1), `world_year` (WL4), `read`, `year` and others |
| The life's record | `g.history` | `w`, `label` (yearly reading), `name` (age, name, becoming), `pivots`, `voice`, `times`, `steers`, `forced`, `own` |
| The end | `g.review` | after `over`: `story` (the song), `voice` (its last sentence and the Book's line) |

## In the browser

The page answers the same keys: Enter lets them choose, a number pushes, the colored buttons beside "Let them choose"
lean (`[data-lc="U"]`). `test/drive*.js` show how the release drivers wait for the page between moments.
