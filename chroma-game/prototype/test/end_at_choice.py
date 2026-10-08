"""A life that ends in the very week of a choice (the engine's run stops right after the pick): the review must still
come, in the terminal and in the HUD, and the console must reach "over" (seen once in 72 lives on 2026-10-06).
python3 test/end_at_choice.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from console import Console

for pick, season in (("", False), ("1", False), ("", True)):
    c = Console(); c.handle(""); c.handle("1"); c.handle("E")
    n = 0
    while c.mode == "play" and n < 2000 and not (c.job is None and c.g.pending is not None):
        n += 1; _, busy = c.handle("")
    assert c.g.pending is not None, "no checkpoint reached"
    def done():                                    # the engine's generator, finished: the next send ends the life
        return None
        yield
    gen = done(); next(gen, None); c.g._gen = gen
    if season:                                     # a season moment is a checkpoint whatever the pacing (point 6)
        real = c.g.season
        c.g.season = lambda *a, _r=real: dict(_r(*a) or {}, this_week=True)
    text, busy = c.handle(pick); k = 0
    while busy and k < 50:
        t2, busy = c.handle(""); text += t2; k += 1
    ok = c.mode == "over" and hasattr(c.g, "review") and "LIFE REVIEW" in text and "error" not in text.lower()
    hud = c.hud()
    print(f"pick {pick or 'theirs'}{' in a season' if season else ''}: mode {c.mode}, review {hasattr(c.g, 'review')}, hud mode {hud.get('mode')}, "
          f"after {k} calls -> {'OK' if ok else 'FAIL'}")
    if not ok:
        print(text[-600:]); sys.exit(1)
print("end at a choice: OK")
