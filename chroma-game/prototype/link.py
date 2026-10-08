"""The game's link to the Chroma engine.

The engine (owned by the engine design thread) runs whole populations in one call and has no
pause points. For the game we load a pinned copy of it (engine_pin/) and, at import time, insert
six pause points into its weekly loop. That turns run() into a generator: every week it hands the
game a snapshot of its state and waits for an answer. Nothing in the engine's equations changes.

Pause points (each yields (kind, t, locals, value) and receives the possibly changed value back):
  "week"   start of each week, after the outside-world intervention     (value: None)
  "situation" after this week's situation is drawn                        (value: situation index array `s`)
  "choose" right after the character has picked an option               (value: chosen index array `a`)
  "odds"   just before the outcome is drawn                             (value: true chance array `p_true`)
  "learn"  right after the surprise of the outcome is computed          (value: prediction error `delta`)
  "end"    end of each week                                             (value: None)

If an anchor line is missing (the engine changed), loading fails loudly with the anchor's text,
so a re-pin never silently runs without the hooks. These are the hooks to move into the engine
itself later.
"""
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
PIN = os.path.join(HERE, "engine_pin")

# (anchor text, text inserted before it, text inserted after it)
PATCHES = [
    ("        e_i, e_p = era_i[t], era_p[t]\n",
     "        _ = yield (\"week\", t, locals(), None)\n", None),
    ("        s = (aff.cumsum(1) > rng.random((N, 1))).argmax(1)\n",
     None, "        s = yield (\"situation\", t, locals(), s)\n"),
    ("        a = (pr.cumsum(1) > rng.random((N, 1))).argmax(1)\n",
     None, "        a = yield (\"choose\", t, locals(), a)\n"),
    ("        succ = rng.random(N) < p_true\n",
     "        p_true = yield (\"odds\", t, locals(), p_true)\n", None),
    ("        delta = np.where(idle, 0.0, r - (ph - (1 - ph) * P[\"loss\"]) * stakes)\n",
     None, "        delta = yield (\"learn\", t, locals(), delta)\n"),
    ("    z = bound_logratios(z, P[\"min_color\"], P[\"max_color\"]); y = bound_logratios(y, P[\"min_color\"], P[\"max_color\"])\n    W_hist.append",
     "        _ = yield (\"end\", t, locals(), None)\n", None),
]


SIG = "def run(N=1000, years=80, seed=0, P=None, record_every=52, intervention=None, lib=None, log_lives=()):"


def _with_steps(src):
    """Return the engine source plus run_steps(): a copy of run() with the pause points inserted.
    The original run() is left exactly as it is."""
    if src.count(SIG) != 1:
        raise RuntimeError("engine changed: run() signature not found:\n" + SIG)
    body = src.split(SIG, 1)[1]
    end = body.find("\ndef ")
    run_text = SIG + (body[:end] if end >= 0 else body)
    for anchor, before, after in PATCHES:
        if run_text.count(anchor) != 1:
            raise RuntimeError(f"engine changed: anchor found {run_text.count(anchor)} times, expected once:\n{anchor}")
        run_text = run_text.replace(anchor, (before or "") + anchor + (after or ""))
    return src + "\n\n# ---- added by the game's link.py: the same weekly loop, pausing for the game\n" + \
        run_text.replace("def run(", "def run_steps(", 1) + "\n"


def load_engine(path=PIN):
    """Load the pinned engine as module `engine` with an extra generator run_steps()."""
    if path not in sys.path:
        sys.path.insert(0, path)
    with open(os.path.join(path, "engine.py"), encoding="utf-8") as f:
        src = f.read()
    mod = types.ModuleType("engine")
    mod.__file__ = os.path.join(path, "engine.py")
    sys.modules["engine"] = mod
    exec(compile(_with_steps(src), mod.__file__, "exec"), mod.__dict__)
    return mod


E = load_engine()
