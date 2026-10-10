# Pack: Art and Writing: Visual Art, Craft and Writing (modern Earth, with the tribal and magic worlds)

Status: built for v22.4 on 2026-10-10, held in a PR until v22.3 is live (coordinator relay 17:10 UTC: "Go with your
recommendation for v22.4... build the three green entry jobs and the Art and Writing slice now as PRs, held. Nothing
merges until I say v22.3 is live, then one at a time."). Not in batch.PACKS: merging this folder changes no life until
the Engine adds `art` at the v22.4 refit. Engine name: `art`. The plan: chroma-packs/notes/v22.4-lanes-sizing.md,
finding 2 (Emren 10-10: red-led choices lead to artist; each life sees richer lanes at different depths). The full pack
idea: chroma-pack-ideas/next-packs.md, "Art and Writing"; this is its visual-art, craft and writing slice. Music stays
with a later "Music, Dance and Comedy" pack.

## The roads

| Colour | Road | Rungs |
|---|---|---|
| R (deepest) | raw expression | taste [open-mic poet] or [life-drawing regular]; practice [street artist] or [illustrator for hire]; profession [painter or sculptor], or the base [novelist] for writing; summit [renowned artist] or [celebrated author] |
| W | form and service | [art school student], then [art teacher] (or a base [teacher] who takes the art room) |
| U | the experimenter | [art school student] or [life-drawing regular], then [illustrator for hire] (U R), then [painter or sculptor] |
| B | art as a career | [painter or sculptor], [art teacher], [shop owner] or [museum curator], then [gallery owner] |
| G | the folk maker | base [craft maker] or [carpenter], then [master craftsperson], then [renowned artist] |

- The two summits are facets (refines), like [lead actor or actress]: [renowned artist] on any of the four visual
  careers, [celebrated author] on [novelist]. The base [novelist] is every writer of books, poems included; the pack
  widens its rule for the open-mic poet with a book in print (EXTEND_ART).
- Every career and summit grows from the rung below (roles.py rungs=, LIFE_ART gates) and has a step at real odds and a
  long shot (art-longshots.lib, LONGSHOTS_ART).

## Files

| File | What it holds |
|---|---|
| catalogue.py | 11 titles (6 careers, 2 summit facets, 2 community, 1 status) and 15 perks, base catalogue format, every share with its source or marked as an estimate; sphere and face tags on careers and community titles |
| roles.py | ROLES_ART (how each title and perk comes and goes), EXTEND_ART (seven widenings of base rules), TARGET_ART (the one budget's tiers, perk multiples) |
| helps.py | HELPS_ART (earned odds), WINDOWS_ART (right place, right time), LIFT_ART (half lifts on the two summits) |
| engine-conditions.py | ECHO_ART and ECHO_ART_LONGSHOTS (four echoes), READ_ART (the reviews), LIFE_ART and LIFE_ART_LONGSHOTS (the rung below, in years), LONGSHOTS_ART |
| worlds.py | the tribal and magic form of every title and perk (WORLDS_ART) and the four world-only moments (WORLD_ONLY_ART) |
| art-doors.lib, -rungs.lib, -roads.lib, -steps.lib, -events.lib, -longshots.lib, -worlds.lib | the 51 moments (MOMENTS-BRIEF.md) |
| MOMENTS-BRIEF.md | the plan for every moment: tier, stages, holds, rates, the balance layout |

## Colour balance

- Titles: every title with colours has three profiles (one single colour and two pairs covering the other four), and
  each colour is the single of two titles: W 6.00, U 6.00, B 6.00, R 6.00, G 6.00 (check_pack.py, spread 0).
- Perks: every kind holds three perks (one single and two pairs), each colour the single of one kind: 3.00 each, and
  every kind holds all five colours.
- Red is deepest through its road (four depths), not through the counts, as every pack is even on its own.

## What the Engine and the Library need (v22.4, after v22.3 is live)

1. **Library:** build `chroma-library/earth_art.py` from art-*.lib (build.py reads the parts), and run check.py.
2. **Engine:** paste engine-conditions.py into earth_rules.PACK_RULES["art"] (calib_v7/paste_pack_rules.py); add `art`
   to batch.PACKS; fit TIER_LIFT for "art,politics,science,stage" (tier_fit with the floors), then roles_check.
3. **Engine, a decision:** TARGET_ART gives the base [novelist] a multiple of 20 (about 1 life in 100), so the writing
   summit has novelists to sit on (they are .0005 of lives today). A tier word instead put novelist under the pack
   careers' lift on its broad base rule: 57 lives in 100 in a scratch run. The Engine may change the multiple.
4. **Proof:** packs are always on, so this changes lives: the full proof with the v22.4 refit (tier_fit, roles_check,
   1,600 pooled lives, the steered rows, choice_check on the candidate). The pie gap against the run without the pack
   stays at .01 or less (the pack rule).

## Checks (2026-10-10, branch packs/art-writing)

- `PYTHONDONTWRITEBYTECODE=1 python3 -B chroma-packs/tools/check_pack.py art`: titles W U B R G 6.00 each, perks 3.00
  each (spread 0.000), every perk kind holds WUBRG; 11 titles, 15 perks, 7 .lib files with 51 moments, 511 catalogue
  names used; "All checks pass".
- The Library's build.py on `art.lib` (it reads the art-*.lib parts): art.py, 46 situations, 4 echoes, 1 read event,
  500 options, "no layout problems".
- lib_stats over the seven files: mean chance per means colour 60.1 to 60.3 overall, spread at most 0.3 points in every
  stage; tags close to even per colour.
- The Library's check.py on the compiled art.py: weight per colour even in every stage (largest spread 0%); the four
  echoes even on their own; choice share .200 for every colour in every stage; value-tag agreement 81% (W 86, U 70,
  B 83, R 79, G 86).
- check_setting.py on every file: no year, real place, currency, brand, real event or real person in player text.
- The engine loads it: `load_batch("earth", packs=["science", "politics", "stage", "art"], pack_moments={"art": <the
  compiled art.py>})` with engine-conditions.py in PACK_RULES["art"]: 285 titles, 272 perks, 1,346 moments (the four
  world-only moments stay out of an Earth life).
- A short scratch run (150 lives on each of seeds 11 and 12, with and without the pack; the three live packs' TIER_LIFT,
  no refit): the pie gap is .005 at most at 40 and at 70 (W U B R G at 40 .244 .153 .151 .230 .223 without, .248 .153
  .154 .225 .220 with). Ever held: street artist .023, illustrator for hire .030, painter or sculptor .013, art teacher
  .040, gallery owner .003, master craftsperson .003, open-mic poet .037, life-drawing regular .027, art school student
  .033, novelist .017; the two summits 0 in 300 lives, before the refit's tier fit with the floors.
- Merging this folder changes no life: nothing reads chroma-packs/art/ until `art` is in batch.PACKS.

Changes the writers made to the brief, kept: per_year is 0 for young_adult on moments whose stages begin at adult
(build.py rejects a rate for a stage a moment does not list); holder pairs carry no share: line (as stage-rungs.lib);
the read event has five readings and no cross cycle (build.py's rule for read events); options that only one holder
can take carry `requires: <title> | without: impossible`; the teacher doors carry no registration requirement, so
every colour's door to [art teacher] has the same chance.
