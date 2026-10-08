# How the threads work in this repository

Backend plan item 1 (the shared folder's `chroma-env/backend-plan.md`, accepted by Emren 2026-10-08 11:14 UTC). Written
by the "clean up the environment" thread. The coordinator relays changes to this page.

## What goes where

| Here, in the repository | In the shared folder (`/mnt/project-files`) only |
|---|---|
| Code, content sources and compiled content, the built page, the pictures the page uses, check and build scripts | Notes, briefs, plans, specs, each owner's README, SPEC, INTERFACE and CHANGELOG, run outputs (`chroma-release/out/`, calibration runs), screenshots, Emren's uploads, `_archive/` |

Paths in the repository are the same as in the shared folder, so `chroma-engine/...` means the same file in both.
A file that is in the repository is changed only through the repository. The shared folder's copy is written from it
(see "Getting a change into the shared folder").

## Branches

- `release/<version>` (`release/v22`, `release/v22.1`): exactly the files that version was published from. Never
  committed to again and never deleted. The session's git proxy refuses tag pushes, so these branches stand in for tags.
- `main`: the newest live version plus finished work that has passed its owner's checks. It is the base for every
  change and for the next release.
- A work branch per change, named after the owner's folder: `engine/<topic>`, `game/<topic>`, `library/<topic>`,
  `packs/<topic>`, `art/<topic>`, `world/<topic>`, `identity/<topic>`, and `checks/<topic>` for the release thread
  (`release/` is taken by the version branches).

## Setting up in a thread

1. Attach the repository: `add_repo` with owner `nkleer`, repo `Chroma_Prototype`, access `push`.
2. Clone it once, shallow, with a long timeout: `git clone --depth 50 https://github.com/nkleer/chroma_prototype
   /home/claude/chroma_prototype`. Only one git operation at a time per session; the proxy allows two.
3. Set the commit author: `git config user.name "Claude"` and `git config user.email "noreply@anthropic.com"`. End every
   commit message with the attribution lines your own session gives you.

## Making a change

1. `git fetch origin main && git checkout -B <owner>/<topic> origin/main`.
2. If a file you will change is not in the repository yet, copy it in from the shared folder unchanged and commit that
   first ("Import <path> as it is in the shared folder"). Your own commit then shows only your change.
3. Change only your own folder. If the change needs another owner's files, ask the coordinator; that owner makes its
   part on its own branch.
4. Run your checks on the branch, in your own container, never in the shared folder.
5. Push the branch and open a pull request into `main`. Its title says what changes in plain words. Its body says why,
   who decided it (Emren's words and time where there are any), and which checks passed, with their output lines.
6. Merge it yourself once your checks pass, unless it touches another owner's folder. In that case the coordinator asks
   that owner to run its checks on the branch first. Use a merge commit, never a force-push. If `main` moved since you
   branched, merge `origin/main` into your branch, rerun the checks it affects, then merge.

## Changing a live part (engine, game, Library, packs, pictures)

Edit it at its live path on your branch, for example `chroma-engine/v22-speedpass/engine.py` on `engine/<topic>`.
There is one path per part in the repository, and the version is the branch, so no `work/` or `staging/` copy is made,
in the repository or in the shared folder. The shared folder's live folders stay exactly as published until the next
publish, so they double as the frozen baseline to prove a change against (or check out `release/<version>`). A thread
that needs your unmerged work fetches your branch. Renaming a version-named path (such as `v22-speedpass`) to a
neutral one is a commit like any other; the shared folder follows at the next publish, with one line in
`chroma-env/paths.py`.

## Getting a change into the shared folder

Other threads and the checks still read the shared folder, so a merged change is copied there:

    python3 -B tools/mirror.py <path> [<path> ...]            # from a clean checkout of main

It copies the tracked files under the paths you name to the same paths in `/mnt/project-files`, prints each file's
md5, and deletes nothing. It refuses any file of the live version (the files in `chroma-env/live-<version>-manifest.txt`),
because those change only at a publish.

## Publishing a version

1. Release runs the checks on a commit of `main` and records it in the version's checklist.
2. On the coordinator's word, the game publishes the page from that commit, using the same build as before for now
   (backend plan item 5 makes this one command).
3. Release pushes that commit as `release/<version>`. The game then writes the live folders from it with
   `python3 -B tools/mirror.py --publish <paths>`, and `chroma-env/check_live.py` gets a new manifest for the version.

## Never

- Force-push `main` or a `release/` branch, or rewrite their history.
- Commit run outputs, screenshots, calibration runs, caches (`__pycache__`), secrets or anything over 50 MB.
- Edit a file in the shared folder that is tracked here, except through `tools/mirror.py`.
- Make another full copy of the game, engine or Library. Use a branch.
