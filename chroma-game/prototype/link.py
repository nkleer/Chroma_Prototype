"""The game's link to the Chroma engine.

The engine (owned by the Engine thread) has its own pause points (backend plan item 2): engine.run_steps() is run() as
a generator that pauses six times a week and hands the game the run's state. engine.PAUSES lists the pauses,
run_steps()'s docstring says where each one is and what may be sent back, and engine.STATE names the run's variables
the game, explain.py and foresee.py may read at a pause. This file loads the pinned copy of the engine (engine_pin/)
as module `engine` and checks that it offers those pause points; it no longer changes the engine's text.

Pause points (each yields (kind, t, state, value) and receives the possibly changed value back):
  "week"   start of each week, after the outside-world intervention     (value: None)
  "situation" after this week's situation is drawn                        (value: situation index array `s`)
  "choose" right after the character has picked an option               (value: chosen index array `a`)
  "odds"   just before the outcome is drawn                             (value: true chance array `p_true`)
  "learn"  right after the surprise of the outcome is computed          (value: prediction error `delta`)
  "end"    end of each week                                             (value: None)

If the pinned engine lacks run_steps() or these pauses, loading fails loudly, so a re-pin never runs without them.
"""
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
PIN = os.path.join(HERE, "engine_pin")
PAUSES = ("week", "situation", "choose", "odds", "learn", "end")


def load_engine(path=PIN):
    """Load the pinned engine as module `engine`; its run_steps() is the generator the game drives."""
    if path not in sys.path:
        sys.path.insert(0, path)
    with open(os.path.join(path, "engine.py"), encoding="utf-8") as f:
        src = f.read()
    mod = types.ModuleType("engine")
    mod.__file__ = os.path.join(path, "engine.py")
    sys.modules["engine"] = mod
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    if not callable(getattr(mod, "run_steps", None)) or tuple(getattr(mod, "PAUSES", ())) != PAUSES:
        raise RuntimeError("engine changed: the pinned engine.py does not offer run_steps() with the pauses "
                           + ", ".join(PAUSES))
    return mod


E = load_engine()
