# v25 round 0: v24's game half on, and where v25 replaces a v24 screen

Vision's call (10-23, from the baseline check `chroma-ideas/next-table-2026-10-19/v25-b1-baseline.md`): on head 10 the
engine's v24 switches were on but the game's were all off. game/v25 brings in game/v24-on, so feature/v25 now plays
with v24's game half on: `GAME V24` (arrows, foot, aims, steer_between, talk, world_answers, wa_phase2), save version
10 (11 once the agenda or fork cards are on).

## What changes in play, and why

These are v24's decisions, as made and checked for the v24 release (records under `chroma-release/records/`):
- **The hover arrows** show which way a choice moves needs, means, people and titles, in size words.
- **Footprints** show on screen.
- **The aims track** shows on the sheet and in the HUD. The player can take up an aim or let one go.
- **Steering between asks** lets the player lean them toward a colour until the next ask.
- **"Talk it over"** works once at a big moment.
- **The world's answers** come with their second phase for Known lives.
- **Asks that matter** are the player's choice, per life: key k, or the Table row "When it matters to them". The
  default stays 0, as Release's Q1 settled (Emren typed "Same play for the asks check", 10-19 22:01 UTC).
- **N3:** a setback's told line names its cause when the engine knows it ("at home", "after a disaster").

With these switched off (`CHROMA_GAME` setting the seven V24 keys false), presets 1 to 6 (seed 7) play the same as
feature/v25 step for step: same steps, ages, choices, colours and numbers. Three things differ, and all of them are
words:
- The setback lines carry N3's cause words.
- Because of those words, a few setback lines that were once identical now differ, which changes which ones a week's
  feed tells.
- The HUD carries the asks flag.

## Where v25 replaces a v24 screen

v24's game half goes on as it was. Where a v25 part takes over, the v24 screen stays until that part's switch is on.
At that point the v25 part replaces it, and the v24 screen is not developed further:

| v24 screen | v25 replacement (switch) | When the switch is on |
|---|---|---|
| The aims track (sheet and HUD) | The agenda (`agenda`): every held aim, pace, priority, decisions waiting, bottlenecks | The HUD shows the agenda strip in place of the aims track |
| Optional asks | Fork cards (`aim_forks` "every") and clash moments (Engine `clash`, game `clash_card`) | Each takes the place of the next optional ask (the Engine's protocol) |
| "Could start" and the aim choices | The preview before taking up an aim (with `agenda`) | Choosing an aim shows its preview first |
| The world panel's rings | Unchanged; "What this world prizes" (`prizes`) and the land line (`land_row`) are added beside them | |
