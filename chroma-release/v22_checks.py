"""Every owner's v22 checks in one command, side by side (Emren 10-08 13:47 Emren's time, item 3 of the v22 health list,
chroma-env/v22-health.md). Kept by the release thread ("What made it into v21").

The checks are the ones the v22 record ran (chroma-release/checklist.md section 9: C-E, C-L, C-P, C-G and C-X rows),
pointed at the live v22 files by default. Nothing in the project folder is written except the run folder in
chroma-release/out/: the script first copies what the checks read into a work tree laid out like /mnt/project-files
(engine, Library, packs, game, the check scripts; pictures are linked, read only), rewrites the absolute project paths in
the copied scripts to that tree, and runs every check there, up to --cores at a time.

    python3 -B chroma-release/v22_checks.py [--level fast|quick|full] [--only ID,ID] [--skip ID,ID] [--ref RUN]
        [--engine DIR] [--game DIR] [--lib DIR] [--packs DIR] [--repo DIR] [--commit REF] [--cores 4] [--work DIR] [--keep]
        [--list] [--no-reuse]

  --level   fast: each owner's check of about 2 minutes, to run after every edit (backend plan item 3; with
            --only @owner for one owner's). quick (default): static, content and build checks, the pin, the GOLIVE
            identity, a few game lives (about 7 minutes on 4 cores). full: also every statistical run of the v22 record
            (the Engine's C-E rows, C-L4, C-L6, C-X4, C-E16, the game's C-G1 set; a few hours on 4 cores).
  --engine, --game, --lib, --packs: a candidate in place of the live folder (default the live files as
            chroma-env/paths.py names them: engine_live, game_live, library_live, packs_live). With
            --engine, the same-lives check (check_speedpass.py) runs too; with --game, the old-saves check
            (check_saves.py). Pass --game with --engine for a v22.1 build, so the speed check plays the build's game.
  --repo, --commit: a candidate from the repository (CONTRIBUTING.md, "Publishing a version": a release is checked
            from a commit of main). --commit REF exports exactly that commit's files (git archive) from --repo (default
            /home/claude/chroma_prototype) and checks them; --repo DIR alone checks the checkout as it is. The commit is
            written in the summary and in every result line (results.jsonl), which record.py reads. The commit's own
            chroma-release/ scripts run; check scripts the repository does not hold yet (the Library's build.py and
            check.py, chroma-packs/tools, the Engine's calibration scripts) come from the shared folder. Run from a
            checkout, this script still works in the shared folder (or CHROMA_PROJECT) and writes its run folder there.
  --only, --skip: check ids, or @engine, @library, @packs, @game, @release for all of one owner's checks, so a run
            can be split over several machines (each writes its own run folder here).
  --ref     an earlier run folder (out/v22checks_...), or several separated by commas (a split run); a check's log is
            taken from the first that has it. Checks marked "same" must print the same as there, once times,
            dates and the work tree's path are taken out: the v22.1 bar of identical lives makes every statistical run
            print what it printed on live v22.
  --list    print the checks and stop.
  --rejudge RUN  judge a finished run's logs again against --ref (when a reference finished after it), no runs;
            the first summary is kept as SUMMARY-first.md.

Each check passes on its own rule: "rc" (exit code 0), "re" (exit 0 and its success line), "same" (ran to the end, and
with --ref equal to the reference; without --ref it records RAN). Run folder: out/v22checks_<UTC>/ with one log per
check, SUMMARY.md and summary.json; every result is also added to out/results.jsonl (results.py; record.py builds a
release record from it). Exit code 0 when no check fails.

Proofs reused (backend plan item 3): while a check runs, every file its Python processes read in the work tree, the
project folder or a candidate folder is noted (an audit hook loaded through PYTHONPATH, rec/sitecustomize.py in the work
folder), with every folder they listed. When a check passes, those files' hashes go in out/proofs/<id>.jsonl. A later
run reuses that pass, without running the check, when the command is the same and every noted file and folder listing
is byte for byte the same (the work tree's path taken out); its log is copied in and judged again (against --ref too).
A check that another check waits on runs whenever that one runs. --no-reuse runs everything. Reading a file through a
shell tool (cp, cmp, cat) is not seen by the hook; those checks name the files they read that way in EXTRA."""
import sys, os, argparse, ast, json, re, shutil, subprocess, time, glob, hashlib

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the project folder: where this script sits, unless that is a repository checkout (which holds the code and content, not
# every owner's check scripts, notes and outputs); then the shared folder, or CHROMA_PROJECT
REAL = os.environ.get("CHROMA_PROJECT") or ("/mnt/project-files" if os.path.isdir(os.path.join(HERE, ".git")) else HERE)
sys.path.insert(0, os.path.join(REAL, "chroma-env")); sys.path.insert(0, os.path.join(REAL, "chroma-release"))
os.environ.setdefault("CHROMA_ROOT", REAL)
from paths import NAMES   # backend plan item 6: the live folders are named once, in chroma-env/paths.py
import results
LIVE = dict(engine=NAMES["engine_live"][0], game=NAMES["game_live"][0], lib=NAMES["library_live"][0], packs=NAMES["packs_live"][0])
MANIFEST = NAMES.get("live_manifest", ("chroma-env/live-v22-manifest.txt",))[0]
GAME_V21 = NAMES["game_v21"][0]
PACKS3 = "science,politics,stage"

# (id, row, owner, level, cores, cwd in the tree, command, rule, after, what)
# {T} is the work tree; the commands run under bash with PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1.
CX2 = "FINAL_LIB={T}/chroma-library python3 -B calib_v10/cx2/cx2run.py"
EP = NAMES["engine_v23"][0]   # the Engine's calibration scripts (calib_v7, v8, v10); the candidate engine is laid over them
V21 = NAMES["library_v21"][0]   # the v21 batch: the go-live rules read it (check_identity --lib)
CHECKS = [
    # ---- across threads and the release thread's own checks
    ("pin", "C-X1", "Release", "quick", 1, ".", "python3 -B chroma-release/check_pin.py", "re:^C-X1: PASS", (),
     "every file the game pinned equals its owner's copy; rarity.py equals rarity.json"),
    ("live", "live files", "Release", "quick", 1, "@real", "python3 -B chroma-env/check_live.py check " + MANIFEST,
     "rc", (), "the live files are unchanged (live runs only; manifest from paths.py)"),
    ("speedpass", "v22.1 E", "Release", "quick", 4, ".", "python3 -B chroma-release/check_speedpass.py --new {ENGINE} --base {LIVEENGINE} --base-game {LIVEGAME} "
     "--scratch {W}/speedpass", "re:^Speed pass: PASS", (), "the build lives the same lives as live v22: engine runs and whole game lives (with --engine or --game)"),
    ("saves", "v22.1 B3", "Release", "full", 4, ".", "python3 -B chroma-release/check_saves.py --new-game {GAME} --base-game {LIVEGAME} "
     "--scratch {W}/saves", "re:^Old saves: PASS", (), "lives saved on live v22 load into the same life, for a build whose played "
     "lives must not change (with --game only)"),
    ("saves_note", "v22.2 S10", "Release", "quick", 4, ".", "python3 -B chroma-release/check_saves.py --new-game {GAME} --base-game {LIVEGAME} "
     "--play-on --note 'saved in an earlier version' --scratch {W}/saves_note", "re:^Old saves: PASS", (), "lives saved on live v22.1 "
     "load into the build with the game's old-save note (console.OLD_SAVE) and play on without error (Emren's card \"Replay with a "
     "note\", 10-09 19:40 UTC; with --game only)"),
    ("identity1", "C-E14", "Release", "quick", 1, ".", "python3 -B chroma-release/check_identity.py --lib " + V21 + " --lives 10 --years 60 "
     "--seeds 5", "re:^C-E14: PASS", (), "engine.GOLIVE lives the go-live engine's lives (engine_v9_golive.py), 10 lives, seed 5"),
    ("identity", "C-E14", "Release", "full", 1, ".", "python3 -B chroma-release/check_identity.py --lib " + V21 + " --lives 10 --years 60 "
     "--seeds 5,21", "re:^C-E14: PASS", (), "the same, seeds 5 and 21"),
    ("identity_full", "C-E14", "Release", "full", 1, ".", "python3 -B chroma-release/check_identity.py --lib " + V21, "re:^C-E14: PASS", (),
     "the same at the v22 record's size: 40 lives x 70 years, seeds 5, 21, 57"),
    ("content", "C-L5, C-L7 to C-L10", "Release", "quick", 1, ".", "python3 -B chroma-release/check_content.py", "rc", (),
     "safety, timeless, sex and gender marks, option chance, closed kinds"),
    ("packrules", "C-P3", "Release", "quick", 1, ".", "python3 -B chroma-release/check_pack_rules.py", "rc", (),
     "every pack's engine-conditions key is in earth_rules.PACK_RULES"),
    ("ages", "C-X4", "Release", "full", 4, ".", "python3 -B chroma-release/check_ages.py", "rc", (),
     "titles and perks only inside their ages, 1,000 lives, world on"),
    ("world", "C-E16", "Release", "full", 3, ".", "python3 -B chroma-release/check_world.py --work {W}/world", "same", (),
     "the outer world's targets (the Engine's world checks plus parts B1-B7); v22 passed with accepted misses"),
    # ---- Library
    ("build_earth", "C-L1", "Library", "quick", 1, "chroma-library",
     "cp earth.py {W}/earth.py.live && python3 -B build.py earth | tail -3 && cmp earth.py {W}/earth.py.live && echo REBUILT-SAME",
     "re:^REBUILT-SAME", (), "earth.py rebuilds byte for byte from its .lib sources"),
    ("build_packs", "C-L1", "Library", "quick", 1, "chroma-library",
     "for p in science politics stage; do rm -rf {W}/b_$p; mkdir -p {W}/b_$p; cp ../chroma-packs/$p/$p-*.lib build.py earth_voice.py {W}/b_$p/; "
     "(cd {W}/b_$p && python3 -B build.py $p | tail -2) && cmp {W}/b_$p/$p.py earth_$p.py && echo \"$p REBUILT-SAME\" || exit 1; done",
     "re:stage REBUILT-SAME", (), "each pack's compiled earth_<pack>.py rebuilds byte for byte from chroma-packs/<pack>/*.lib"),
    ("balance", "C-L1", "Library", "quick", 1, "chroma-library", "python3 -B check.py earth.py && cat checks_earth.md", "same", (),
     "balance per stage, drivers and echoes, chance per color, Schwartz agreement"),
    ("setting", "C-L2", "Library", "quick", 1, "chroma-library",
     "python3 -B drafts/check_setting.py && python3 -B drafts/check_setting.py ../chroma-packs/science ../chroma-packs/politics ../chroma-packs/stage",
     "re:^setting: no year", (), "timeless modern setting in every player string (Library parts, dreams, voice, catalogue, packs)"),
    ("voice", "C-L3", "Library", "quick", 1, "chroma-library", "python3 -B drafts/check_voice.py earth_voice.py", "rc", (),
     "the inner voice and lessons"),
    ("perks", "C-L3", "Library", "quick", 1, "chroma-library", "python3 -B drafts/check_perks_titles.py", "same", (),
     "the titles and perks catalogue: format, color balance, realism"),
    ("titles", "C-L4", "Library", "full", 4, "chroma-library",
     "PACK_DIR={T}/chroma-packs python3 -B tests/titles_by_source.py {T}/chroma-library {W}/titles.json {T}/" + EP + " " + PACKS3
     + " && python3 -c \"import json; d=json.load(open('{W}/titles.json')); print(json.dumps(d, sort_keys=True)[:200000])\"",
     "same", (), "lifetime title and perk shares against the catalogue, 400 lives, packs on"),
    ("reach", "C-L6", "Library", "full", 4, "chroma-library",
     "PACK_DIR={T}/chroma-packs python3 -B tests/reach.py {T}/chroma-library {W}/reach.json {T}/" + EP + " " + PACKS3
     + " && python3 -c \"import json; d=json.load(open('{W}/reach.json')); print(json.dumps(d, sort_keys=True)[:200000])\"",
     "same", (), "reach and repeats against each moment's gap, 400 lives"),
    # ---- Packs
    ("pack_check", "C-P1", "Packs", "quick", 1, "chroma-packs/tools",
     "for p in science politics stage; do python3 -B check_pack.py $p || exit 1; done", "rc", (),
     "catalogue fields, color balance, references, names"),
    ("pack_stats", "C-P2", "Packs", "quick", 1, "chroma-packs",
     "for p in science politics stage; do echo \"== $p\"; python3 -B tools/lib_stats.py $p/*.lib || exit 1; done", "same", (),
     "chance per means color per stage; tags"),
    ("pack_balance", "C-P4", "Packs", "quick", 1, "chroma-library",
     "for p in science politics stage; do python3 -B check.py earth_$p.py && cat checks_earth_$p.md || exit 1; done", "same", (),
     "the Library's balance check on each compiled pack"),
    # ---- Engine (the C-X2 share of the v22 record, calib_v10/cx2/jobs.txt, plus the rows that ran elsewhere)
    ("score21", "C-E1", "Engine", "full", 1, EP, "LIB={T}/chroma-library PACKS=" + PACKS3 + " python3 -B calib_v8/score_packs.py '{{}}' 600 21",
     "same", (), "the survey scorecard, seed 21 (v22: 8 of 11, accepted)"),
    ("score23", "C-E1", "Engine", "full", 1, EP, "LIB={T}/chroma-library PACKS=" + PACKS3 + " python3 -B calib_v8/score_packs.py '{{}}' 600 23",
     "same", (), "the survey scorecard, seed 23"),
    ("tier", "C-E3", "Engine", "full", 4, EP, "FIT_OUT={W}/tier.json PACKS=" + PACKS3 + " python3 -B calib_v8/tier_fit.py 500 0 "
     "{T}/chroma-library/earth_perks_titles.py",
     "same", (), "pack careers about 1 in 3, summits about 1 in 20 (2,000 lives, seeds 11 to 14)"),
    ("roles", "C-E4", "Engine", "full", 4, EP, "FIT_OUT={W}/role_norm.json python3 -B calib_v7/roles_check.py 150 0 {T}/chroma-library/earth_perks_titles.py",
     "same", (), "titles and perks a life against the catalogue"),
    ("death", "C-E5", "Engine", "full", 1, EP, CX2 + " calib_v8/death_check.py {T}/chroma-library 400 3", "same", (), "dead by 30, 50, 65, 80"),
    ("death_won", "C-E5", "Engine", "full", 1, EP, "PX='{{\"world\": true}}' " + CX2 + " calib_v8/death_check.py {T}/chroma-library 400 3", "same", (),
     "the same, world on"),
    ("lean41", "C-E6", "Engine", "full", 1, EP, "python3 -B calib_v10/lean_check.py {T}/chroma-library 400 41 {W}/lean_41.npz", "same", (), "packs on, seed 41"),
    ("lean42", "C-E6", "Engine", "full", 1, EP, "python3 -B calib_v10/lean_check.py {T}/chroma-library 400 42 {W}/lean_42.npz", "same", (), "seed 42"),
    ("lean43", "C-E6", "Engine", "full", 1, EP, "python3 -B calib_v10/lean_check.py {T}/chroma-library 400 43 {W}/lean_43.npz", "same", (), "seed 43"),
    ("lean44", "C-E6", "Engine", "full", 1, EP, "python3 -B calib_v10/lean_check.py {T}/chroma-library 400 44 {W}/lean_44.npz", "same", (), "seed 44"),
    ("nopack41", "C-E6", "Engine", "full", 1, EP, "NOPACKS=1 " + CX2 + " calib_v10/lean_check.py {T}/chroma-library 400 41 {W}/nopack_41.npz", "same", (), "no packs, seed 41"),
    ("nopack42", "C-E6", "Engine", "full", 1, EP, "NOPACKS=1 " + CX2 + " calib_v10/lean_check.py {T}/chroma-library 400 42 {W}/nopack_42.npz", "same", (), "seed 42"),
    ("nopack43", "C-E6", "Engine", "full", 1, EP, "NOPACKS=1 " + CX2 + " calib_v10/lean_check.py {T}/chroma-library 400 43 {W}/nopack_43.npz", "same", (), "seed 43"),
    ("nopack44", "C-E6", "Engine", "full", 1, EP, "NOPACKS=1 " + CX2 + " calib_v10/lean_check.py {T}/chroma-library 400 44 {W}/nopack_44.npz", "same", (), "seed 44"),
    ("lean", "C-E6, P12", "Engine", "full", 1, EP, "python3 -B calib_v10/lean_check.py sum {T}/chroma-library {W}/lean_41.npz {W}/lean_42.npz "
     "{W}/lean_43.npz {W}/lean_44.npz", "same", ("lean41", "lean42", "lean43", "lean44"), "pack roads' holders lean to their lead color"),
    ("pie", "C-E6", "Engine", "full", 1, EP, "python3 -B -c \"import numpy as np; W='{W}'\n"
     "a = sum(np.load(W + '/lean_%d.npz' % s)['pie'] * 400 for s in (41, 42, 43, 44)) / 1600\n"
     "b = sum(np.load(W + '/nopack_%d.npz' % s)['pie'] * 400 for s in (41, 42, 43, 44)) / 1600\n"
     "[print(age, 'packs', a[k].round(3), 'none', b[k].round(3), 'largest gap %.3f' % abs(a[k] - b[k]).max()) for k, age in enumerate((20, 40, 70))]\n"
     "g = abs(a - b).max(); print('C-E6', 'PASS' if g <= .015 else 'CHECK', 'largest gap %.3f (v22 .006)' % g)\"",
     "re:^C-E6 PASS", ("lean41", "lean42", "lean43", "lean44", "nopack41", "nopack42", "nopack43", "nopack44"),
     "packs against no packs within .015, 1,600 paired lives"),
    ("pie41", "C-E6", "Engine", "full", 1, EP, "python3 -B -c \"import numpy as np; W='{W}'\n"
     "a = np.load(W + '/lean_41.npz')['pie']; b = np.load(W + '/nopack_41.npz')['pie']\n"
     "[print(age, 'packs', a[k].round(3), 'none', b[k].round(3), 'largest gap %.3f' % abs(a[k] - b[k]).max()) for k, age in enumerate((20, 40, 70))]\n"
     "g = abs(a - b).max(); print('C-E6', 'PASS' if g <= .03 else 'CHECK', 'largest gap %.3f, 400 paired lives (seed 41)' % g)\"",
     "re:^C-E6 PASS", ("lean41", "nopack41"),
     "packs against no packs within .03, 400 paired lives (seed 41; v22.3's quick proof, Engine 10-10)"),
    ("pie_packs", "C-E6", "Engine", "full", 1, EP, CX2 + " calib_v8/pie_check.py {T}/chroma-library 200 11", "same", (), "the pie, packs on, 200 lives"),
    ("pie_nopacks", "C-E6", "Engine", "full", 1, EP, "NOPACKS=1 " + CX2 + " calib_v8/pie_check.py {T}/chroma-library 200 11", "same", (), "no packs"),
    ("pie_won", "C-E6", "Engine", "full", 1, EP, "PX='{{\"world\": true}}' " + CX2 + " calib_v8/pie_check.py {T}/chroma-library 200 11", "same", (), "world on"),
    ("season", "C-E7", "Engine", "full", 1, EP, CX2 + " calib_v8/season_check.py {T}/chroma-library 150 5 " + PACKS3, "same", (), "seasons open; steps"),
    ("repeat", "C-E7", "Engine", "full", 1, EP, CX2 + " calib_v8/repeat_check.py '{{}}' 300 11", "same", (), "births, childless"),
    ("chance", "C-E8", "Engine", "full", 1, EP, "PACKS=" + PACKS3 + " python3 -B calib_v7/chance_check.py check 100 {T}/chroma-library "
     "{T}/chroma-library/earth_perks_titles.py", "same", (), "written chance against true odds"),
    ("exits", "C-E9", "Engine", "full", 1, EP, CX2 + " calib_v7/exits_check.py '{{}}' 300 11", "same", (), "at work by age, retiring"),
    ("exits_won", "C-E9", "Engine", "full", 1, EP, "PX='{{\"world\": true}}' " + CX2 + " calib_v7/exits_check.py '{{}}' 300 11", "same", (), "world on"),
    ("satisf", "C-E10", "Engine", "full", 1, EP, CX2 + " calib_v8/t_satisf.py '{{}}' 150 5", "same", (), "satisfaction U-shape"),
    ("satisf_won", "C-E10", "Engine", "full", 1, EP, "PX='{{\"world\": true}}' " + CX2 + " calib_v8/t_satisf.py '{{}}' 150 5", "same", (), "world on"),
    ("inertia", "C-E10", "Engine", "full", 1, EP, CX2 + " calib_v8/inertia_check.py '{{}}' 300 11", "same", (), "turning years move more"),
    ("goals", "C-E11", "Engine", "full", 1, EP, CX2 + " calib_v7/goals_check.py 200 1 '{{}}' earth", "same", (), "dreams, harmony, passions"),
    ("goals_won", "C-E11", "Engine", "full", 1, EP, "PX='{{\"world\": true}}' " + CX2 + " calib_v7/goals_check.py 200 1 '{{}}' earth", "same", (), "world on"),
    ("felt_gap", "C-E12", "Engine", "full", 1, EP, CX2 + " calib_v7/felt_gap.py live", "same", (), "felt odds against true"),
    ("plan_felt", "C-E12", "Engine", "full", 1, EP, CX2 + " calib_v7/plan_felt.py '{{}}'", "same", (), "plans"),
    ("accept", "C-E12", "Engine", "full", 1, EP, CX2 + " calib_v7/accept_check.py 8 70", "same", (), "acceptance words"),
    ("foresee_off", "E5", "Engine", "full", 1, EP, CX2 + " calib_v7/foresee_table.py 400 3 earth '{{}}'", "same", (), "the foresee hint"),
    ("foresee_on", "E5", "Engine", "full", 1, EP, CX2 + " calib_v7/foresee_table.py 400 3 earth '{{\"world\": true, \"history\": \"random\"}}'",
     "same", (), "world on"),
    ("rarity", "C-E13", "Engine", "full", 4, EP, "OUT={W}/rarity.json python3 -B calib_v8/rarity_build.py && cmp {W}/rarity.json {RARITY} "
     "&& echo RARITY-SAME", "re:^RARITY-SAME", (), "the Book's rarity table rebuilds byte for byte (1,200 lives)"),
    ("rarity1000", "C-E13", "Engine", "full", 4, EP, "OUT={W}/rarity.json python3 -B calib_v8/rarity_build.py 1000 && cmp {W}/rarity.json {RARITY} "
     "&& echo RARITY-SAME", "re:^RARITY-SAME", (), "the same at 1,000 lives a seed (4,000 lives; v22.3's wider table, coordinator 10-10)"),
    ("speed", "C-E15", "Engine", "full", 1, EP, "python3 -B speed_check.py 1 80 5 off,on", "rc", (),
     "time per life, world off and on (the go-live v9 run is left out: it cannot read today's Library; C-E14 compares with it)"),
    ("child_deaths", "C-X5", "Engine", "full", 1, EP, "python3 -B calib_v10/child_deaths.py 400 90 5 {T}/chroma-library "
     "{T}/chroma-library/earth_perks_titles.py", "same", (), "a child's death and illness among parents"),
    # ---- Game (C-G1, staging-final/run_cg1G.sh; C-G2)
    ("icons", "C-G2", "Game", "quick", 1, "chroma-game/prototype", "python3 -B web/src/live_icons.py --check", "rc", (),
     "every option keeps its drawn icon"),
    ("build", "item 5", "Game", "quick", 1, ".", "python3 -B chroma-game/tools/build.py {W}/build --same-as game_live && echo BUILD-SAME",
     "re:^BUILD-SAME", (), "the one build command makes the game from the engine, Library and packs, file for file as the "
     "candidate's game (Library rebuild, pin C-X1, load); when chroma-game/tools/build.py is there"),
    # ---- Engine's own fast check (backend plan item 2): the engine's pause points
    ("t_steps", "item 2", "Engine", "quick", 1, ".", "python3 -B chroma-engine/tools/t_steps.py", "re:^ALL PASS", (),
     "run_steps() lives run()'s lives bit for bit, pauses in PAUSES order, every STATE name at every pause (3 short runs); "
     "when chroma-engine/tools/t_steps.py is there and the engine has run_steps()"),
    # ---- Visuals (its own fast check, chroma-art/kit/check_art.py; --full also rebuilds the icons with Node)
    ("art", "art", "Visuals", "quick", 1, ".", "python3 -B chroma-art/kit/check_art.py", "re:^art check: pass", (),
     "every picture the game names exists at its size and weight; every life event has a picture; one icon per option"),
]
G1 = [("peace_bands", "test/peace_bands.py 8"), ("fuzz", "test/fuzz.py 6"), ("acceptance", "test/acceptance.py 1 6"),
      ("longshot_check", "test/longshot_check.py 6"), ("event_rate", "test/event_rate.py 30"), ("season_rate", "test/season_rate.py 30"),
      ("roles2", "test/roles2.py 11"), ("roles_g", "test/roles.py 7"), ("book_check", "test/book_check.py 6"),
      ("timeless", "test/timeless.py 6"), ("next2_check", "test/next2_check.py 8"), ("markers", "test/markers.py 4"),
      ("saveload", "test/saveload.py 3"), ("life_ends", "test/life_ends.py 4"), ("end_at_choice", "test/end_at_choice.py"),
      ("season_ages", "test/season_ages.py"), ("identity_g", "test/identity_check.py 3"), ("kin", "test/kin_check.py 4 60"),
      ("saveload_world", "test/saveload_world.py"), ("abroad", "test/abroad_check.py")]
QUICK_G1 = {"fuzz", "saveload", "saveload_world", "end_at_choice", "markers", "identity_g"}
for gid, cmd in G1:
    CHECKS.append((gid, "C-G1", "Game", "quick" if gid in QUICK_G1 else "full", 1, "chroma-game/prototype", "python3 -B " + cmd, "rc", (),
                   "the game's own Python check " + cmd.split()[0]))
# The steered checks of the update's stage 1 (implementation-list.md, Build plan; gameplay-feel.md 5.2; voice-mechanics.md
# section 9): played lives from the game's scripted players, test/steer_check.py <target>, whose last line is
# "STEER <target>: PASS" (or MISS) under the numbers it measured. They wait (are left out) until the game holds the driver.
# --only @steered runs them all. The driver uses every core and keeps the lives it played in $STEER_CACHE, so the rows run
# one at a time (4 cores each) and share one cache in the run's work folder: targets that share lives (the "let" seeds)
# play them once. Split over machines as the Game suggests: steer_identity; steer_apart; the other eight together.
STEERED = [
    ("steer_identity", "identity", "steering one colour at most picks puts it in the identity at 40 in most lives (each colour)"),
    ("steer_apart", "apart", "the same life steered two ways ends further apart than two different lives left alone"),
    ("alone_names", "alone_names", "a life left alone changes its identity name at most 3 to 4 times after 18"),
    ("push_rare", "push_rare", "pushed lives meet more rare moments than the same lives left alone"),
    ("world_lines", "world_lines", "every world line names a change the engine made to the character that year (wfx)"),
    ("voice_quiet", "voice_quiet", "always letting them choose: \"a quiet voice\" and no voice lines"),
    ("voice_careful", "voice_careful", "always the careful pick: named \"the careful voice\" at the end and in two moments in three once "
     "named (a pure White pick sits at several poles, so an early name can go to a neighbour); no other side's voice lines"),
    ("voice_trust", "voice_trust", "trust per colour after steered picks: the mean change after ones that worked is above the mean after "
     "ones that failed, which is below 0 (P2: a push that worked but fed no need they lacked is still resented)"),
    ("voice_lines", "voice_lines", "every voice line first person or plain narration, at most 25 words, no colour named"),
    ("voice_year", "voice_year", "the chapter keeps at most one voice line a year"),
]
STEER = "test/steer_check.py"
for sid, target, what in STEERED:
    CHECKS.append((sid, "steered", "Game", "full", 4, "chroma-game/prototype", f"STEER_CACHE={{W}}/steer_cache python3 -B {STEER} {target}",
                   f"re:^STEER {target}: PASS", (), what))

# Backend plan item 3: each owner's fast check, about 2 minutes on 4 cores, run after every edit (--level fast). These are
# the release thread's proposals from the quick level's times (out/v22checks_20261008-122526); each owner confirms or
# names its own, and changes its own line here.
FAST = {
    "Release": ["pin", "content", "packrules", "build"],                                # 0.4 min
    "Library": ["build_earth", "build_packs", "balance", "setting", "voice", "perks"],    # 0.6 min
    "Packs": ["pack_check", "pack_stats", "pack_balance"],                               # 0.3 min
    "Game": ["icons", "end_at_choice", "saveload", "saveload_world"],                    # about 2 min on 4 cores
    "Engine": ["t_steps"],     # about 20 s; on an engine from before item 2 (no run_steps, e.g. live v22.1) identity1 (3 min) instead
    "Visuals": ["art"],                                                                  # a few seconds (its own check_art.py)
}
FAST_OWNER = {cid: o for o, l in FAST.items() for cid in l}
TSTEPS = "chroma-engine/tools/t_steps.py"
# Files a check reads through a shell tool (cp, cmp, cat), which the proof recorder cannot see (paths in the work tree)
EXTRA = {
    "build_earth": ["chroma-library/earth.py"],
    "build_packs": ["chroma-packs/science/*.lib", "chroma-packs/politics/*.lib", "chroma-packs/stage/*.lib", "chroma-library/build.py",
                    "chroma-library/earth_voice.py", "chroma-library/earth_science.py", "chroma-library/earth_politics.py",
                    "chroma-library/earth_stage.py"],
    "rarity": [NAMES["rarity_live"][0]],
    "rarity1000": [NAMES["rarity_live"][0]],
}
# A steered row whose lives are already in the run's cache reads only the driver and the cache, so its proof names the
# game and its pinned engine too: a later run reuses its pass only when they are unchanged.
for sid, _, _ in STEERED:
    EXTRA[sid] = ["chroma-game/prototype/*.py", "chroma-game/prototype/engine_pin/*.py", "chroma-game/prototype/" + STEER]

ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
ap.add_argument("--level", default="quick", choices=("fast", "quick", "full"))
ap.add_argument("--only", default="")
ap.add_argument("--skip", default="")
ap.add_argument("--ref", default=None)
for k in LIVE:
    ap.add_argument("--" + k, default=None)
ap.add_argument("--repo", default=None, help="a checkout of the repository: its engine, game, Library and packs are the candidate")
ap.add_argument("--commit", default=None, help="check exactly this commit of --repo (default /home/claude/chroma_prototype), e.g. origin/main")
ap.add_argument("--cores", type=int, default=4)
ap.add_argument("--work", default=None)
ap.add_argument("--keep", action="store_true")
ap.add_argument("--list", action="store_true")
ap.add_argument("--json", action="store_true", help="with --list: one JSON line per check (record.py reads it)")
ap.add_argument("--no-reuse", action="store_true", help="run every check, even when an earlier pass covered the same files")
ap.add_argument("--rejudge", default=None, help="a finished run folder: judge its logs again against --ref, no runs")
a = ap.parse_args()

if a.list:
    for c in CHECKS:
        lv = "fast" if c[0] in FAST_OWNER else c[3]
        if a.json:
            print(json.dumps(dict(id=c[0], row=c[1], owner=c[2], level=lv, fast_of=FAST_OWNER.get(c[0]), rule=c[7], what=c[9])))
            continue
        print(f"{c[0]:15s} {c[1]:20s} {c[2]:8s} {lv:5s} {c[7]:22s} {c[9]}" + (f"  (fast check of {FAST_OWNER[c[0]]})" if c[0] in FAST_OWNER and FAST_OWNER[c[0]] != c[2] else ""))
    sys.exit(0)

stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
if not a.rejudge:                # claim the run folder now: runs started in the same second (jobs side by side) get -2, -3, ...
    for n in range(2, 100):
        try:
            os.makedirs(os.path.join(REAL, "chroma-release", "out", "v22checks_" + stamp)); break
        except FileExistsError:
            stamp = stamp[:15] + f"-{n}"
COMMIT = None                    # the repository commit checked (repo workflow step 6: a release is checked from a commit of main)
CAND = None                      # its files' root: its own chroma-release/ scripts are the ones that run
if a.repo or a.commit:
    repo = os.path.abspath(a.repo or "/home/claude/chroma_prototype")
    git = lambda *x: subprocess.run(["git", "-C", repo] + list(x), capture_output=True, text=True, check=True).stdout.strip()
    if a.commit:                 # the commit's own files, exported by git archive into the work folder (nothing else of the checkout)
        sha = git("rev-parse", a.commit + "^{commit}")
        cand = os.path.join(os.path.abspath(a.work or os.path.join("/tmp", "v22checks_" + stamp)) + "-commit", sha[:12])
        shutil.rmtree(cand, ignore_errors=True); os.makedirs(cand)
        subprocess.run(f"git -C {repo} archive {sha} | tar -x -C {cand}", shell=True, check=True)
        COMMIT = dict(repo=repo, commit=sha, ref=a.commit, dirty=False)
    else:                        # the checkout as it is, uncommitted edits included (marked dirty)
        cand = repo
        COMMIT = dict(repo=repo, commit=git("rev-parse", "HEAD"), ref=git("rev-parse", "--abbrev-ref", "HEAD"),
                      dirty=bool(git("status", "--porcelain", "--untracked-files=no")))
    CAND = cand
    for k, v in LIVE.items():
        if getattr(a, k) is None and os.path.isdir(os.path.join(cand, v)):
            setattr(a, k, os.path.join(cand, v))
src = {k: os.path.abspath(getattr(a, k) or os.path.join(REAL, v)) for k, v in LIVE.items()}
is_live = all(getattr(a, k) is None for k in LIVE)
if a.rejudge:                    # judge a finished run again (its references may have finished after it)
    RUN = os.path.abspath(a.rejudge)
    WORK = next((ln[6:].split("/tree")[0] for f in sorted(glob.glob(os.path.join(RUN, "*.log")))
                 for ln in open(f, errors="replace").read().splitlines()[:3] if ln.startswith("# cwd ") and "/tree" in ln), "/nonexistent")
    T = os.path.join(WORK, "tree"); W = os.path.join(WORK, "w")
else:
    RUN = os.path.join(REAL, "chroma-release", "out", "v22checks_" + stamp)   # made above
    WORK = os.path.abspath(a.work or os.path.join("/tmp", "v22checks_" + stamp))
    T = os.path.join(WORK, "tree"); W = os.path.join(WORK, "w")
    shutil.rmtree(WORK, ignore_errors=True); os.makedirs(T); os.makedirs(W)
SKIPF = shutil.ignore_patterns("__pycache__", "*.pyc", "*.out", "*.npz", "*.done", "*.rc", "*.log")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()[:12]


def cp_files(s, d, pat="*"):
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(s, pat)):
        if os.path.isfile(f):
            shutil.copy2(f, d)


TOOLS_DIR = "chroma-engine/tools"   # the Engine's check scripts since backend plan item 7, without their calib_vN/ folders
TOOLS_MARK = TOOLS_DIR + "/cx2run.py"   # they are there when this is (tools/ began with _engine.py and t_steps.py alone)
TOOLS = False                       # set in main(): the candidate or the shared folder has them


def engine_row(c):
    """A check's cwd and command. The Engine's rows run in chroma-engine/tools once it is there (the calib_v7, calib_v8,
    calib_v10 and calib_v10/cx2 prefixes dropped; cx2run.py takes the short names); before that, in the calib layout."""
    if c[5] != EP or not TOOLS:
        return c[5], c[6]
    return TOOLS_DIR, re.sub(r"\bcalib_v(?:7|8|10)/(?:cx2/)?", "", c[6])


def fromcand(rel):
    """The root a shared file comes from: the candidate commit or checkout when it holds the file, else the project folder."""
    return CAND if CAND and os.path.exists(os.path.join(CAND, rel)) else REAL


def build_tree():
    """The work tree: the candidate (or live) folders where the checks expect them, plus the scripts that run them."""
    P = os.path.join(T, "chroma-engine", "prototype"); RP = os.path.join(REAL, "chroma-engine", "prototype")
    cp_files(RP, P, "*.py")                                   # check scripts at the prototype's top (speed_check, v9)
    for d in ("calib_v7", "calib_v8", "calib_v10"):           # the Engine's check scripts, without their outputs
        for r, ds, fs in os.walk(os.path.join(RP, d)):
            ds[:] = [x for x in ds if x not in ("__pycache__", "wasm", "fit_final_backup")]
            for f in fs:
                if f.endswith((".py", ".sh", ".json", ".csv", ".txt")) and os.path.getsize(os.path.join(r, f)) < 5e6:
                    o = os.path.join(P, os.path.relpath(r, RP)); os.makedirs(o, exist_ok=True); shutil.copy2(os.path.join(r, f), o)
    cp_files(src["engine"], P, "*.py")                        # the engine itself: live v22 or the candidate
    if os.path.exists(os.path.join(src["engine"], "rarity.json")):
        os.makedirs(os.path.join(P, "calib_v8"), exist_ok=True)
        shutil.copy2(os.path.join(src["engine"], "rarity.json"), os.path.join(P, "calib_v8", "rarity.json"))
    shutil.copytree(src["engine"], os.path.join(T, "chroma-engine", "archive", "live-v22"), ignore=SKIPF)   # owners' scripts name it
    if LIVE["engine"] != "chroma-engine/archive/live-v22":                    # and where paths.py names the live engine
        shutil.copytree(src["engine"], os.path.join(T, LIVE["engine"]), ignore=SKIPF, dirs_exist_ok=True)
    L = os.path.join(T, "chroma-library")
    cp_files(src["lib"], L)
    for f in glob.glob(os.path.join(REAL, LIVE["lib"], "*")):                 # the Library's scripts and notes a candidate lacks (the
        b = os.path.basename(f)                                                # repository holds its content only): build.py, check.py,
        if os.path.isfile(f) and not os.path.exists(os.path.join(L, b)) and not (b.endswith(".lib") or re.match(r"earth.*\.py$", b)):
            shutil.copy2(f, L)                                                 # earth.md; never a content file the candidate dropped
    if os.path.exists(os.path.join(L, "earth.py")) and os.path.exists(os.path.join(L, "render.py")):
        # earth.md, which the title and perk checks read for situation names, comes from the candidate's own earth.py: the
        # repository holds no earth.md, and the shared folder's is the live one, so a moment added after it went missing
        try:                                                                   # (10-09, Library #26's 'a following of your own')
            subprocess.run([sys.executable, "-B", "render.py", "earth.py"], cwd=L, check=True, capture_output=True, timeout=300)
        except (subprocess.SubprocessError, OSError):
            if os.path.exists(os.path.join(L, "earth.md")):                    # never the live one in its place: the checks that
                os.remove(os.path.join(L, "earth.md"))                         # read it then say they could not
    cp_files(os.path.join(REAL, "chroma-library", "drafts"), os.path.join(L, "drafts"), "*.py")
    for f in ("checks_perks_titles.md", "checks_voice.md", "earth_voice.md", "perks_titles.md"):
        if os.path.exists(os.path.join(REAL, "chroma-library", "drafts", f)):
            shutil.copy2(os.path.join(REAL, "chroma-library", "drafts", f), os.path.join(L, "drafts"))
    for pat in ("*.py", "*.sh"):
        cp_files(os.path.join(REAL, "chroma-library", "tests"), os.path.join(L, "tests"), pat)
    shutil.copytree(os.path.join(REAL, V21), os.path.join(T, V21), ignore=SKIPF)
    for sd in (os.path.join(src["lib"], "sources"), os.path.join(REAL, LIVE["lib"], "sources")):   # research notes, from the
        if os.path.isdir(sd):                                                                      # shared folder if need be
            shutil.copytree(sd, os.path.join(L, "sources"), ignore=SKIPF); break
    K = os.path.join(T, "chroma-packs")
    cp_files(src["packs"], K)
    for d in ("core", "politics", "science", "stage", "tools"):                # tools/ (the Packs' checks) from the shared folder if the
        sd = os.path.join(src["packs"], d)                                     # candidate lacks it
        shutil.copytree(sd if os.path.isdir(sd) else os.path.join(REAL, LIVE["packs"], d), os.path.join(K, d), ignore=SKIPF)
    shutil.copytree(src["game"], os.path.join(T, "chroma-game", "prototype"), ignore=SKIPF)
    v21 = os.path.join(REAL, GAME_V21, "engine_pin")                          # check_identity's go-live rules
    shutil.copytree(v21, os.path.join(T, GAME_V21, "engine_pin"), ignore=SKIPF)
    os.makedirs(os.path.join(T, "chroma-env"), exist_ok=True)                 # the folder names, read under CHROMA_ROOT=T
    shutil.copy2(os.path.join(fromcand("chroma-env/paths.py"), "chroma-env", "paths.py"), os.path.join(T, "chroma-env", "paths.py"))
    tools = fromcand(TOOLS_MARK) if TOOLS else fromcand(TSTEPS) if os.path.exists(os.path.join(fromcand(TSTEPS), TSTEPS)) else None
    if tools:                                                 # the Engine's tools, items 2 and 7 (they find the tree's engine_live
        shutil.copytree(os.path.join(tools, TOOLS_DIR), os.path.join(T, TOOLS_DIR), ignore=SKIPF)   # by _engine.py)
    if os.path.exists(os.path.join(fromcand("chroma-game/tools/build.py"), "chroma-game", "tools", "build.py")):   # the one build
        shutil.copytree(os.path.join(fromcand("chroma-game/tools/build.py"), "chroma-game", "tools"),      # command (item 5)
                        os.path.join(T, "chroma-game", "tools"), ignore=SKIPF)
    os.makedirs(os.path.join(T, "chroma-art"))
    art = fromcand("chroma-art/game/pictures.json")            # the candidate's own pictures when it holds them (a release
    os.symlink(os.path.join(art, "chroma-art", "game"), os.path.join(T, "chroma-art", "game"))   # ships its commit's art), read only
    cp_files(os.path.join(fromcand("chroma-art/kit/check_art.py"), "chroma-art", "kit"), os.path.join(T, "chroma-art", "kit"), "check_art.py")
    R = os.path.join(T, "chroma-release")
    for pat in ("*.py", "*.js"):
        cp_files(os.path.join(fromcand("chroma-release"), "chroma-release"), R, pat)
    n = 0                                                     # absolute project paths in the copies point at the tree
    for r, ds, fs in os.walk(T):
        if os.path.islink(r):
            continue
        ds[:] = [x for x in ds if not os.path.islink(os.path.join(r, x))]
        for f in fs:
            if f.endswith((".py", ".sh", ".js")):
                p = os.path.join(r, f); s = open(p, encoding="utf-8", errors="surrogateescape").read()
                s2 = s.replace("/mnt/attach/project-files", T).replace("/mnt/project-files", T)
                if s2 != s:
                    open(p, "w", encoding="utf-8", errors="surrogateescape").write(s2); n += 1
    return n


TIMES = re.compile(r"\d+(\.\d+)?\s*(ms|s|sec|secs|seconds|min|minutes|h)\b|\b\d\d:\d\d(:\d\d)?\b|\b20\d\d-\d\d-\d\d\b|\b\d{8}-\d{4,6}\b")


def norm(text):
    """A log as it should repeat on identical lives: no times, dates, run stamps or work paths."""
    out = []
    for ln in text.replace(T, "<T>").replace(W, "<W>").replace(WORK, "<WORK>").splitlines():
        if ln.startswith("# ") or ln.startswith("exit ") or "process_time" in ln:
            continue
        out.append(TIMES.sub("<t>", ln).rstrip())
    return out


SITE = r"""# v22_checks.py proof recorder (backend plan item 3): notes the files and folders this process reads under the
# watched roots, one line each, in $CHROMA_REC_OUT/<pid>.txt. Loaded as sitecustomize through PYTHONPATH.
import os, sys, hashlib
_out = os.environ.get("CHROMA_REC_OUT"); _roots = [r for r in os.environ.get("CHROMA_REC_ROOTS", "").split(os.pathsep) if r]
if _out and _roots:
    _st = {"pid": None, "f": None, "seen": set(), "wrote": set(), "busy": False}
    _WR = os.O_WRONLY | os.O_RDWR
    def _abs(p):
        return os.path.abspath(os.fsdecode(p))
    def _under(p):
        return any(p == r or p.startswith(r + os.sep) for r in _roots)
    def _write(line):
        if os.getpid() != _st["pid"]:
            _st["pid"] = os.getpid(); _st["f"] = None
        if _st["f"] is None:
            _st["f"] = open(os.path.join(_out, "%d.txt" % os.getpid()), "a", buffering=1)
        _st["f"].write(line + "\n")
    def _hook(ev, args):
        if _st["busy"] or ev not in ("open", "os.listdir", "os.scandir"):
            return
        _st["busy"] = True
        try:
            if ev == "open":
                p, mode, flags = (tuple(args) + (None, None, None))[:3]
                if p is None or isinstance(p, int):
                    return
                p = _abs(p)
                if (isinstance(mode, str) and any(c in mode for c in "wax+")) or (not isinstance(mode, str) and isinstance(flags, int) and flags & _WR):
                    _st["wrote"].add(p); return
                if p in _st["wrote"] or ("F" + p) in _st["seen"] or not _under(p):
                    return
                _st["seen"].add("F" + p); _write("F" + p)
            else:
                p = args[0] if args else "."
                if p is None:
                    p = "."
                if isinstance(p, int):
                    return
                p = _abs(p)
                if ("D" + p) in _st["seen"] or not _under(p):
                    return
                _st["seen"].add("D" + p)
                try:
                    h = hashlib.md5("\n".join(sorted(os.listdir(p))).encode()).hexdigest()[:16]
                except OSError:
                    h = "missing"
                _write("D" + p + "\t" + h)
        except Exception:
            pass
        finally:
            _st["busy"] = False
    sys.addaudithook(_hook)
"""
ALIASES = sorted({REAL, os.path.realpath(REAL), "/mnt/project-files", "/mnt/attach/project-files"}, key=len, reverse=True)
PROOFS = os.path.join(REAL, "chroma-release", "out", "proofs")


def keyof(p):
    """A path as a proof records it: in the work tree (T:), in the project folder (R:), in a candidate folder given on the
    command line (S<part>:, relative to it, so the same files pass wherever the candidate sits) or anywhere else (A:)."""
    for pre, root in (("T:", T),) + tuple(("R:", r) for r in ALIASES) + tuple(("S" + k + ":", v) for k, v in src.items()):
        if p == root or p.startswith(root + os.sep):
            return pre + os.path.relpath(p, root)
    return "A:" + p


def pathof(k):
    pre, rest = k.split(":", 1)
    return os.path.join(T, rest) if pre == "T" else os.path.join(REAL, rest) if pre == "R" else \
        os.path.join(src[pre[1:]], rest) if pre[1:] in src else rest


def fhash(k):
    p = pathof(k)
    if not os.path.isfile(p):
        return "dir" if os.path.isdir(p) else "missing"
    b = open(p, "rb").read()
    if k.endswith("chroma-env/paths.py"):      # only the folders it names count, not its descriptions (other owners edit those)
        try:
            tree = ast.parse(b)
            names = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                         and any(getattr(t, "id", "") == "NAMES" for t in n.targets))
            b = json.dumps({x: v[0] for x, v in names.items()}, sort_keys=True).encode()
        except (StopIteration, ValueError, SyntaxError):
            pass
    if k.startswith("T:"):                     # the copies' paths were rewritten to this run's tree: take them out
        b = b.replace(W.encode(), b"<W>").replace(T.encode(), b"<T>").replace(WORK.encode(), b"<WORK>")
    return hashlib.md5(b).hexdigest()[:16]


def dhash(k):
    p = pathof(k)
    return hashlib.md5("\n".join(sorted(os.listdir(p))).encode()).hexdigest()[:16] if os.path.isdir(p) else "missing"


def cmd_key(cmd):
    out = cmd
    for k, v in sorted(src.items(), key=lambda kv: -len(kv[1])):   # a candidate folder by its part, wherever it was laid out
        if not is_live and getattr(a, k):
            out = out.replace(v, "<S" + k + ">")
    out = out.replace(W, "<W>").replace(T, "<T>").replace(WORK, "<WORK>")
    for r in ALIASES:
        out = out.replace(r, "<R>")
    return out


def recorded(cid):
    """The files and folder listings a finished check's Python processes read, plus its EXTRA files, with hashes."""
    files, dirs = {}, {}
    for f in glob.glob(os.path.join(WORK, "rec", cid, "*.txt")):
        for ln in open(f, errors="replace").read().splitlines():
            if ln.startswith("F"):
                p = ln[1:]
                if p.endswith(".pyc") and os.sep + "__pycache__" + os.sep in p:   # a cached module stands for its source, which
                    d, b = os.path.split(p)                                         # the import then only stats, never opens
                    p = os.path.join(os.path.dirname(d), b.split(".")[0] + ".py")
                k = keyof(p)
                if not k.startswith("A:"):
                    files[k] = None
            elif ln.startswith("D") and "\t" in ln:
                p, h = ln[1:].split("\t", 1)
                dirs.setdefault(keyof(p), h)
    for pat in EXTRA.get(cid, ()):
        for p in sorted(glob.glob(os.path.join(T, pat))):
            files[keyof(p)] = None
        dirs.setdefault("G:" + pat, hashlib.md5("\n".join(os.path.relpath(p, T) for p in sorted(glob.glob(os.path.join(T, pat)))).encode()).hexdigest()[:16])
    return {k: fhash(k) for k in files}, dirs


def dirs_now(dirs):
    out = {}
    for k in dirs:
        if k.startswith("G:"):
            out[k] = hashlib.md5("\n".join(os.path.relpath(p, T) for p in sorted(glob.glob(os.path.join(T, k[2:])))).encode()).hexdigest()[:16]
        else:
            out[k] = dhash(k)
    return out


def save_proof(cid, cmd, secs):
    files, dirs = recorded(cid)
    if not files:
        return 0
    os.makedirs(PROOFS, exist_ok=True)
    with open(os.path.join(PROOFS, cid + ".jsonl"), "a") as f:
        f.write(json.dumps(dict(cmd=cmd_key(cmd), files=files, dirs=dirs, log=os.path.join(RUN, cid + ".log"), work=WORK, run=RUN,
                                time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), secs=round(secs)), sort_keys=True) + "\n")
    return len(files)


WHY = {}   # why a check could not reuse its newest proof, for the run log


def find_proof(cid, cmd):
    """The newest earlier run of this check, with the same command, whose every recorded file and listing is the same now."""
    fp = os.path.join(PROOFS, cid + ".jsonl")
    if not os.path.exists(fp):
        WHY[cid] = "no earlier proof"
        return None
    ck = cmd_key(cmd)
    for ln in reversed(open(fp).read().splitlines()):
        try:
            e = json.loads(ln)
        except ValueError:
            continue
        if e["cmd"] != ck or not os.path.exists(e["log"]):
            WHY.setdefault(cid, "the command changed" if e["cmd"] != ck else "the proof's log is gone")
            continue
        bad = [k for k, h in e["files"].items() if fhash(k) != h]
        now = dirs_now(e["dirs"]); badd = [k for k in e["dirs"] if now.get(k) != e["dirs"][k]]
        if not bad and not badd:
            return e
        WHY.setdefault(cid, "changed since " + os.path.basename(e["run"]) + ": " + ", ".join((bad + badd)[:4])
                       + (f" and {len(bad) + len(badd) - 4} more" if len(bad) + len(badd) > 4 else ""))
    return None


def main():
    t0 = time.time()
    def ids(spec):   # check ids, or @owner for every check of that owner (@engine, @library, @packs, @game, @release)
        out = set()
        for x in (y.strip() for y in spec.split(",")):
            if x.startswith("@"):
                out |= {c[0] for c in CHECKS if c[2].lower() == x[1:].lower() or c[1] == x[1:].lower()
                        or (a.level == "fast" and FAST_OWNER.get(c[0], "").lower() == x[1:].lower())}
            elif x:
                out.add(x)
        return out
    eng = os.path.join(src["engine"], "engine.py")   # t_steps needs its script and an engine with the pause points
    steps = os.path.exists(os.path.join(fromcand(TSTEPS), TSTEPS)) and os.path.exists(eng) \
        and "\ndef run_steps(" in open(eng, encoding="utf-8").read()
    if not steps and "t_steps" in FAST_OWNER:          # an engine from before item 2: the one-seed C-E14 stands in
        FAST_OWNER["identity1"] = FAST_OWNER.pop("t_steps")
    only = ids(a.only); skip = ids(a.skip)
    todo, waiting = [], []
    for c in CHECKS:
        cid, row, owner, level, cores, cwd, cmd, rule, after, what = c
        if only and cid not in only:
            continue
        if a.level == "fast" and cid not in FAST_OWNER:
            continue
        if cid in skip or (not only and a.level == "quick" and level == "full"):
            continue
        if cid == "live" and not is_live:
            continue
        if (cid == "speedpass" and a.engine is None and a.game is None) or (cid in ("saves", "saves_note") and a.game is None) \
                or (cid == "build" and not os.path.exists(os.path.join(fromcand("chroma-game/tools/build.py"), "chroma-game/tools/build.py"))) \
                or (cid == "t_steps" and not steps):
            continue
        if row == "steered" and not os.path.exists(os.path.join(src["game"], STEER)):
            waiting.append(cid); continue
        todo.append(c)
    say = open(os.path.join(RUN, "run.txt"), "w")

    def log(s):
        print(s, flush=True); say.write(s + "\n"); say.flush()
    log(f"v22 checks, {stamp} UTC, level {a.level}, {len(todo)} checks, up to {a.cores} cores; run folder {RUN}")
    if waiting:
        log(f"  left out, waiting for the game's {STEER}: {', '.join(waiting)}")
    for k in LIVE:
        log(f"  {k:6s} {src[k]}" + ("" if getattr(a, k) is None else "   (candidate)"))
    if a.ref:
        log(f"  reference run {a.ref}")
    if a.level == "fast" and FAST_OWNER.get("identity1") == "Engine" and any(c[0] == "identity1" for c in todo):
        log("  Engine: this engine has no run_steps() (from before backend item 2), so its fast check is identity1, not t_steps")
    global TOOLS
    TOOLS = os.path.exists(os.path.join(fromcand(TOOLS_MARK), TOOLS_MARK))
    n = build_tree()
    log(f"  the Engine's rows run from {TOOLS_DIR if TOOLS else EP + ' (calib_v7, calib_v8, calib_v10)'}")
    log(f"  work tree {T}: {n} copied scripts re-pointed to it; engine.py {md5(os.path.join(T, EP, 'engine.py'))}, "
        f"game.py {md5(os.path.join(T, 'chroma-game/prototype/game.py'))}, earth.py {md5(os.path.join(T, 'chroma-library/earth.py'))}")
    os.makedirs(os.path.join(WORK, "rec"), exist_ok=True)
    open(os.path.join(WORK, "rec", "sitecustomize.py"), "w").write(SITE)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1", MPLBACKEND="Agg")
    for k in ("PACK_DIR", "LIB", "PACKS", "PACK_MOMENTS", "TIER_LIFT", "FINAL_LIB", "PX", "NEXT", "RULES", "CHROMA_ROOT", "CHROMA_ENGINE",
              "OUT_DIR"):
        env.pop(k, None)
    fmt = lambda c: engine_row(c)[1].format(T=T, W=W, ENGINE=src["engine"], LIVEENGINE=os.path.join(REAL, LIVE["engine"]),
                                            GAME=src["game"], LIVEGAME=os.path.join(REAL, LIVE["game"]),
                                            RARITY=os.path.join(T, NAMES["rarity_live"][0]))
    # a proof's command names the folder it runs in when that is not the check's own (an Engine row run from tools/), so a
    # proof taken in one layout is never reused for the other
    pkey = lambda c: fmt(c) if engine_row(c)[0] == c[5] else "cd " + engine_row(c)[0] + " && " + fmt(c)
    # proofs reused: a check whose files are all as they were when it last ran; any check another one waits on runs with it
    reuse = {} if a.no_reuse else {c[0]: e for c in todo for e in [find_proof(c[0], pkey(c))] if e}
    names = {t[0] for t in todo}
    changed = True
    while changed:
        changed = False
        for c in todo:
            if c[0] not in reuse:
                for x in c[8]:
                    if x in reuse and x in names:
                        del reuse[x]; changed = True
    res = {}
    for c in todo:
        if c[0] in reuse:
            e = reuse[c[0]]
            text = open(e["log"], encoding="utf-8", errors="replace").read().replace(e["work"], WORK)
            open(os.path.join(RUN, c[0] + ".log"), "w").write(f"# reused from {e['run']} ({e['time']} UTC): {len(e['files'])} files read, "
                                                              f"every one the same now\n" + text)
            v = verdict(c, 0, 0)
            v["note"] = (f"reused from {os.path.basename(e['run'])} ({len(e['files'])} files the same); " + v["note"]).rstrip("; ")
            v["reused_from"] = e["run"]
            res[c[0]] = v
            log(f"  {v['result']:4s} {c[0]} ({c[1]}) reused: {len(e['files'])} files read then are the same now ({os.path.basename(e['run'])})")
    running = []; pending = [c for c in todo if c[0] not in reuse]; used = 0
    roots = os.pathsep.join([T] + ALIASES + sorted({os.path.abspath(v) for v in src.values()}))
    while pending or running:
        for c in list(pending):
            cid, cores = c[0], min(c[4], a.cores)
            if any(x not in res for x in c[8] if x in names):
                continue
            if used + cores > a.cores and running:
                continue
            cmd = fmt(c)
            cwd = REAL if c[5] == "@real" else os.path.join(T, engine_row(c)[0])
            rec = os.path.join(WORK, "rec", cid); os.makedirs(rec, exist_ok=True)
            e2 = dict(env, CHROMA_ROOT=REAL if c[5] == "@real" else T, CHROMA_REC_OUT=rec, CHROMA_REC_ROOTS=roots,
                      PYTHONPATH=os.pathsep.join([os.path.join(WORK, "rec")] + [x for x in [env.get("PYTHONPATH")] if x]))
            f = open(os.path.join(RUN, cid + ".log"), "w"); f.write(f"# {cmd}\n# cwd {cwd}\n"); f.flush()
            p = subprocess.Popen(["bash", "-c", cmd], cwd=cwd, env=e2, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
            running.append((p, c, time.time(), f, cores, cmd)); pending.remove(c); used += cores
            log(f"  start {cid} ({c[1]}, {c[2]})" + (f": {WHY[cid]}" if cid in WHY and not a.no_reuse else ""))
        time.sleep(3)
        for r in list(running):
            p, c, ts, f, cores, cmd = r
            limit = 3 * 3600 if c[3] == "full" else 3600
            if p.poll() is None and time.time() - ts > limit:
                os.killpg(p.pid, 9); p.wait()
            if p.poll() is not None:
                f.write(f"\nexit {p.returncode} in {time.time() - ts:.0f}s\n"); f.close()
                running.remove(r); used -= cores
                res[c[0]] = verdict(c, p.returncode, time.time() - ts)
                nf = save_proof(c[0], pkey(c), time.time() - ts) if p.returncode == 0 else 0
                log(f"  {res[c[0]]['result']:4s} {c[0]} ({c[1]}) in {res[c[0]]['secs']:.0f}s {res[c[0]]['note']}"
                    + (f" [proof: {nf} files]" if nf else ""))
    write_summary(todo, res, t0, log)
    if not a.keep:
        shutil.rmtree(WORK, ignore_errors=True)
        if a.commit and CAND:                    # the exported commit too
            shutil.rmtree(os.path.dirname(CAND), ignore_errors=True)
    bad = [k for k, v in res.items() if v["result"] in ("FAIL", "MISS")]
    sys.exit(1 if bad else 0)


def verdict(c, rc, secs):
    cid, rule = c[0], c[7]
    text = open(os.path.join(RUN, cid + ".log"), encoding="utf-8", errors="replace").read()
    last = [x for x in text.splitlines() if x.strip() and not x.startswith("exit ")][-1:] or [""]
    if rc != 0:
        return dict(result="FAIL", secs=secs, note=f"exit {rc}: {last[0][:160]}")
    if rule.startswith("re:"):
        ok = re.search(rule[3:], text, re.M) is not None
        return dict(result="PASS" if ok else "FAIL", secs=secs, note="" if ok else f"no line matching {rule[3:]!r}")
    if rule == "same":
        if not a.ref:
            return dict(result="RAN", secs=secs, note="(no reference given)")
        rp = next((os.path.join(r, cid + ".log") for r in a.ref.split(",") if os.path.exists(os.path.join(r, cid + ".log"))),
                  os.path.join(a.ref.split(",")[0], cid + ".log"))
        if not os.path.exists(rp):
            return dict(result="RAN", secs=secs, note="(not in the reference run)")
        rtext = open(rp, encoding="utf-8", errors="replace").read()
        rx = re.findall(r"^exit (-?\d+) in", rtext, re.M)
        if not rx:
            return dict(result="RAN", secs=secs, note="(the reference run of it has not finished; rejudge later)")
        if rx[-1] != "0":
            return dict(result="RAN", secs=secs, note=f"(the reference run of it ended with exit {rx[-1]})")
        x = norm(rtext.replace(ref_tree(rp)[:-len("/tree")], WORK))
        y = norm(text)
        if x == y:
            return dict(result="PASS", secs=secs, note=f"same as the reference ({len(y)} lines)")
        i = next((k for k, (u, v) in enumerate(zip(x, y)) if u != v), min(len(x), len(y)))
        return dict(result="MISS", secs=secs, note=f"differs from the reference at line {i + 1}: "
                    f"{(x[i] if i < len(x) else '<end>')[:120]!r} vs {(y[i] if i < len(y) else '<end>')[:120]!r}")
    return dict(result="PASS", secs=secs, note="")


def ref_tree(rp):
    """The reference run's work tree, from the cwd line its log starts with."""
    for ln in open(rp, encoding="utf-8", errors="replace").read().splitlines()[:3]:
        if ln.startswith("# cwd ") and "/tree" in ln:
            return ln[6:].split("/tree")[0] + "/tree"
    return "\0"


def write_summary(todo, res, t0, log):
    rows = [f"# v22 checks, {stamp} UTC", "",
            f"Level {a.level}; " + ("live files" if is_live else "candidate: " + ", ".join(f"{k} {src[k]}" for k in LIVE if getattr(a, k)))
            + (f"; commit {COMMIT['commit'][:12]} ({COMMIT['ref']}{', with uncommitted edits' if COMMIT['dirty'] else ''}) of {COMMIT['repo']}"
               if COMMIT else "")
            + (f"; reference {a.ref}" if a.ref else "") + f"; {(time.time() - t0) / 60:.0f} minutes on up to {a.cores} cores.", "",
            "| Check | Row | Owner | Result | Time | What | Note |", "|---|---|---|---|---|---|---|"]
    for c in todo:
        r = res.get(c[0], dict(result="NOT RUN", secs=0, note=""))
        rows.append(f"| {c[0]} | {c[1]} | {c[2]} | {r['result']}{' (reused)' if r.get('reused_from') else ''} | {r['secs'] / 60:.1f} min | {c[9]} | {r['note'].replace('|', '/')} |")
    cnt = {k: sum(1 for v in res.values() if v["result"] == k) for k in ("PASS", "RAN", "MISS", "FAIL")}
    rows += ["", f"PASS {cnt['PASS']}, RAN {cnt['RAN']} (no reference to compare), MISS {cnt['MISS']}, FAIL {cnt['FAIL']} of {len(todo)}"]
    open(os.path.join(RUN, "SUMMARY.md"), "w").write("\n".join(rows) + "\n")
    json.dump(dict(stamp=stamp, level=a.level, live=is_live, src=src, commit=COMMIT, ref=a.ref, results=res), open(os.path.join(RUN, "summary.json"), "w"), indent=1)
    for c in todo:                              # backend plan item 4: every result in out/results.jsonl, for record.py
        r = res.get(c[0])
        if r:
            cand = None if is_live else {k: src[k] for k in LIVE if getattr(a, k) or src[k] != os.path.join(REAL, LIVE[k])}
            if COMMIT:
                cand = dict(cand or {}, commit=COMMIT["commit"], dirty=COMMIT["dirty"])
            results.add(c[0], r["result"], os.path.join(RUN, c[0] + ".log"), r["note"], candidate=cand, run=RUN, secs=round(r["secs"]),
                        reused_from=r.get("reused_from"))
    log(rows[-1]); log(f"summary: {os.path.join(RUN, 'SUMMARY.md')}")


def rejudge():
    old = json.load(open(os.path.join(RUN, "summary.json")))
    global stamp, is_live, src, COMMIT
    stamp, is_live, src, COMMIT = old["stamp"], old["live"], old["src"], old.get("commit")
    a.level = old["level"]
    res = {}; todo = []
    for c in CHECKS:
        lp = os.path.join(RUN, c[0] + ".log")
        if c[0] not in old["results"] or not os.path.exists(lp):
            continue
        todo.append(c)
        m = re.findall(r"^exit (-?\d+) in (\d+)s", open(lp, errors="replace").read(), re.M)
        res[c[0]] = verdict(c, int(m[-1][0]), float(m[-1][1])) if m else dict(result="NOT RUN", secs=0, note="no exit line")
    if os.path.exists(os.path.join(RUN, "SUMMARY.md")) and not os.path.exists(os.path.join(RUN, "SUMMARY-first.md")):
        shutil.copy2(os.path.join(RUN, "SUMMARY.md"), os.path.join(RUN, "SUMMARY-first.md"))
    write_summary(todo, res, time.time(), print)
    sys.exit(1 if any(v["result"] in ("FAIL", "MISS") for v in res.values()) else 0)


rejudge() if a.rejudge else main()
