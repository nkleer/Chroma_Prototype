"""Where each part of Chroma lives, named once (backend plan item 6, chroma-env/backend-plan.md).

Scripts import this instead of writing /mnt/project-files/... paths by hand, so a folder that moves is changed here once:

    import sys; sys.path.insert(0, "/mnt/project-files/chroma-env")
    from paths import P, path
    engine_dir = P["engine_live"]               # an absolute path
    pics = path("art_game", "pictures.json")    # joined under a named folder

The root is /mnt/project-files unless CHROMA_ROOT says otherwise, so a check can run on a copied work tree laid out the
same way (as chroma-release/v22_checks.py does) by setting CHROMA_ROOT instead of rewriting paths.

    python3 -B paths.py          lists every name, its path and whether it exists

Written 2026-10-08 by the "clean up the environment" thread. Owners change their own lines; MAP.md says the same in words.
"""
import os

ROOT = os.environ.get("CHROMA_ROOT", "/mnt/project-files")

# name: (path under ROOT, what it is)
NAMES = {
    # the live version (v22.1, published 10-08 13:10 UTC, artifact version 1791464842-7382)
    "engine_live":    ("chroma-engine/v22-speedpass", "the live v22.1 engine: the Engine's speed pass, same lives as v22 (MD5SUMS inside); the Engine changes this line if it freezes it elsewhere"),
    "live_manifest":  ("chroma-env/live-v22.1-manifest.txt", "MD5 of every file the live version is built from (chroma-env/check_live.py)"),
    "game_live":      ("chroma-game/prototype", "the live game: code, web/src, engine_pin, tests"),
    "library_live":   ("chroma-library", "the live Library: earth*.py, dreams.py and the .lib sources at its top level"),
    "packs_live":     ("chroma-packs", "the live packs: core, politics (Packs v7), science, stage"),
    "rarity_live":    ("chroma-engine/prototype/calib_v8/rarity.json", "the rarity table the live game's rarity.py came from"),
    "art_game":       ("chroma-art/game", "the pictures the page uses (pictures.json names them, pics/ holds them)"),
    "art":            ("chroma-art", "the visuals folder: kit/ drawing code, data/ scene texts, notes/"),
    "art_old_icons":  ("chroma-art/old", "the retired game-icons.net set (CC BY 3.0); the icon builder and review pages read it"),
    "build_helpers":  ("chroma-hud", "sync21.py builds a web folder, pubmap.py gives the publish file map"),
    # the v22.1 build record
    "game_v22p1":     ("chroma-game/staging-v22p1", "how v22.1 was built and checked (checks/, README); its tree/ became chroma-game/prototype"),
    "release":        ("chroma-release", "release records and check scripts (v22_checks.py runs every owner's checks)"),
    "release_out":    ("chroma-release/out", "check outputs, one folder or file per run"),
    # earlier versions kept as records
    "game_v22":       ("chroma-game/prototype-v22", "the v22 game, the only rollback (index.html 3114caa7f358)"),
    "engine_v22":     ("chroma-engine/archive/live-v22", "the v22 engine, frozen at its go-live (MD5SUMS inside)"),
    "live_manifest_v22": ("chroma-env/live-v22-manifest.txt", "MD5 of the v22 files (paths recorded as chroma-game/prototype; check_live.py reads them as prototype-v22)"),
    "game_v21":       ("_archive/2026-10-08/chroma-game/prototype-v21", "the v21 game, archived 10-08 13:15 UTC (check_identity reads its engine_pin/)"),
    "library_v21":    ("chroma-library/archive/live-2026-10-06-1625", "the Library batch live in v21"),
    # paused v23 drafts (paused 10-07 21:38 UTC)
    "engine_v23":     ("chroma-engine/prototype", "the paused v23 engine edits (engine.py, batch.py, world*.py) and calibration runs calib_v6 to calib_v11; backend item 7 splits it"),
    "game_v23":       ("chroma-game/staging-next/v23/prototype", "the single v23 game copy (paused)"),
    "library_v23":    ("chroma-library/staging/next4", "the v23 Library batch (paused)"),
    "library_v23_src": ("chroma-library/drafts/next4", "the v23 Library sources (paused): parts that win over the live ones"),
    "packs_v23":      ("chroma-packs/v23-drafts-paused", "the v23 pack drafts (paused)"),
    # the workspace itself
    "env":            ("chroma-env", "MAP.md, check_live.py, this file, the backend plan"),
    "archive":        ("_archive", "old outputs and versions moved out by date, under their old paths"),
}

P = {k: os.path.join(ROOT, v[0]) for k, v in NAMES.items()}


def path(name, *parts):
    """The absolute path of a named folder or file, with any further parts joined under it."""
    return os.path.join(P[name], *parts)


if __name__ == "__main__":
    print(f"CHROMA_ROOT = {ROOT}")
    for k, (rel, what) in NAMES.items():
        print(f"{'ok ' if os.path.exists(P[k]) else 'NO '} {k:17s} {rel:48s} {what}")
