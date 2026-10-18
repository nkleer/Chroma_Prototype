"""The game's tests play the owners' current engine, Library and packs: engine_pin/ is filled from their folders first
(chroma-game/tools/pin.py), unless the game folder holds a committed pin (PINNED.txt)."""
import os, sys

TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools")


def ensure(game=None):
    """Bring game/engine_pin/ (default: this test folder's game) in line with the owners' folders of its own tree."""
    game = os.path.abspath(game or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, TOOLS)
    try:
        import pin
    finally:
        sys.path.remove(TOOLS)
    return pin.ensure(game, say=lambda s: print(s, file=sys.stderr))
