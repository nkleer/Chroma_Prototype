"""Everyday routine lines for the interlude between moments (game-side built-in lines)."""

import re
import string
from collections import Counter
from routine_text import ROUTINE  # noqa: E402,F401  the text tables (data only)


# Every slot name the lines may use.
SLOTS = {"N", "place", "partner", "child", "friend", "parent", "job", "circle"}

# Slots that may only appear when the matching need is part of the line's conditions.
SLOT_NEEDS = {
    "partner": "partner",
    "child": "children",
    "friend": "friend",
    "parent": "parent_alive",
    "job": "career",
    "circle": "community",
}

NEEDS = (
    "career", "student", "retired", "partner", "children", "no_partner", "faith",
    "community", "friend", "parent_alive", "poor", "wealthy", "stressed", "happy",
    "unhappy", "lonely", "calm", "restless", "in_poor_health",
)
# Needs that can never hold together.
CONFLICTS = (("partner", "no_partner"), ("poor", "wealthy"), ("happy", "unhappy"))

WORLDS = "ETM"
COLORS = "WUBRG"
SEASONS = ("spring", "summer", "autumn", "winter")
WHEN_KEYS = {"age", "world", "need", "color", "season"}
AGE_BANDS = (
    ("toddler", 0, 6), ("child", 6, 13), ("teen", 13, 18), ("young adult", 18, 30),
    ("adult", 30, 50), ("older adult", 50, 65), ("elder", 65, 110),
)

# Style guards.
MIN_WORDS, MAX_WORDS = 8, 22
CHARACTER_PRONOUNS = re.compile(r"\b(he|she|him|her|his|hers|himself|herself)\b", re.IGNORECASE)

# Coverage targets.
MIN_POOL = 10  # need-free lines for every world and age, worst case over leading color and season
MIN_EARTH_PER_NEED = 4
MIN_PER_COLOR = {"E": 12, "T": 3, "M": 3}
MIN_PER_SEASON = {"E": 6, "T": 2, "M": 2}


def slots_in(text):
    """Return the slot names used in text."""
    return {field for _, field, _, _ in string.Formatter().parse(text) if field is not None}


def worlds_of(when):
    return when.get("world", WORLDS)


def pool_size(entries, age, color, season):
    """Need-free lines open to a character of this age, leading color and current season."""
    return sum(
        1 for when in entries
        if when["age"][0] <= age < when["age"][1]
        and when.get("color") in (None, color)
        and when.get("season") in (None, season)
    )


def check():
    seen = set()
    for i, entry in enumerate(ROUTINE):
        assert isinstance(entry, tuple) and len(entry) == 2, f"entry {i} is not a (text, when) pair"
        text, when = entry
        where = f"line {i}: {text!r}"
        assert isinstance(text, str) and text and text == text.strip(), f"{where}: bad text"
        assert isinstance(when, dict), f"{where}: when must be a dict"
        assert set(when) <= WHEN_KEYS, f"{where}: unknown keys {sorted(set(when) - WHEN_KEYS)}"

        # Slots.
        for _, field, spec, conv in string.Formatter().parse(text):
            if field is None:
                continue
            assert field in SLOTS, f"{where}: unknown slot {{{field}}}"
            assert not spec and conv is None, f"{where}: slot {{{field}}} has a format spec"
        needs = when.get("need", ())
        assert isinstance(needs, tuple), f"{where}: need must be a tuple"
        for slot in slots_in(text):
            if slot in SLOT_NEEDS:
                assert SLOT_NEEDS[slot] in needs, f"{where}: {{{slot}}} needs need={SLOT_NEEDS[slot]!r}"

        # Age.
        assert "age" in when, f"{where}: missing age"
        age = when["age"]
        assert isinstance(age, tuple) and len(age) == 2 and all(type(a) is int for a in age), f"{where}: bad age {age!r}"
        assert 0 <= age[0] < age[1] <= 110, f"{where}: bad age range {age!r}"

        # World.
        world = worlds_of(when)
        assert isinstance(world, str) and world, f"{where}: bad world {world!r}"
        assert set(world) <= set(WORLDS) and len(set(world)) == len(world), f"{where}: bad world {world!r}"

        # Needs.
        for need in needs:
            assert need in NEEDS, f"{where}: unknown need {need!r}"
        assert len(set(needs)) == len(needs), f"{where}: repeated need"
        for a, b in CONFLICTS:
            assert not (a in needs and b in needs), f"{where}: {a} conflicts with {b}"

        # Color and season.
        if "color" in when:
            assert when["color"] in tuple(COLORS), f"{where}: bad color {when['color']!r}"
        if "season" in when:
            assert when["season"] in SEASONS, f"{where}: bad season {when['season']!r}"

        # Punctuation and style.
        assert "—" not in text, f"{where}: em dash"
        assert "!" not in text, f"{where}: exclamation mark"
        assert not CHARACTER_PRONOUNS.search(text), f"{where}: gendered pronoun"
        assert text.endswith(".") and ". " not in text and "?" not in text, f"{where}: not one sentence"
        words = len(text.split())
        assert MIN_WORDS <= words <= MAX_WORDS, f"{where}: {words} words"

        # Repeats.
        key = " ".join(text.lower().split())
        assert key not in seen, f"{where}: repeated line"
        seen.add(key)

    # ---- counts and coverage ----
    by_world = {w: [when for _, when in ROUTINE if w in worlds_of(when)] for w in WORLDS}
    total = len(ROUTINE)
    print(f"Routine lines: {total}")
    print("  " + "   ".join(f"{w}: {len(by_world[w])}" for w in WORLDS))
    young = sum(1 for when in by_world["E"] if when["age"][0] < 18 and when["age"][1] <= 20)
    print(f"  E lines written for ages 0-18: {young}")

    def table(title, keys, count):
        print(f"\n{title}")
        print(f"  {'':16}" + "".join(f"{w:>6}" for w in WORLDS))
        for key in keys:
            label = key if isinstance(key, str) else key[0]
            print(f"  {label:16}" + "".join(f"{count(w, key):>6}" for w in WORLDS))

    def band_count(w, band):
        _, lo, hi = band
        return sum(1 for when in by_world[w] if when["age"][0] < hi and when["age"][1] > lo)

    def min_pool(w, band):
        _, lo, hi = band
        free = [when for when in by_world[w] if not when.get("need")]
        return min(pool_size(free, a, c, s) for a in range(lo, hi) for c in COLORS for s in SEASONS)

    table("Per age band (lines whose range overlaps the band)", AGE_BANDS, band_count)
    table("Smallest need-free pool in band (worst age, color, season)", AGE_BANDS, min_pool)
    table("Per need", NEEDS, lambda w, n: sum(1 for when in by_world[w] if n in when.get("need", ())))
    table("Per color", tuple(COLORS), lambda w, c: sum(1 for when in by_world[w] if when.get("color") == c))
    table("Per season", SEASONS, lambda w, s: sum(1 for when in by_world[w] if when.get("season") == s))
    table("No need, no color, no season", ("unconditional",),
          lambda w, _: sum(1 for when in by_world[w] if not set(when) & {"need", "color", "season"}))

    openers = Counter(text.split()[0].strip(",") for text, _ in ROUTINE)
    print("\nMost common opening words: " + ", ".join(
        f"{word} {n} ({n * 100 // total}%)" for word, n in openers.most_common(6)))

    # Coverage targets.
    for w in WORLDS:
        for band in AGE_BANDS:
            assert band_count(w, band) > 0, f"no {w} lines for {band[0]}"
            assert min_pool(w, band) >= MIN_POOL, f"{w} {band[0]}: need-free pool below {MIN_POOL}"
        for c in COLORS:
            n = sum(1 for when in by_world[w] if when.get("color") == c)
            assert n >= MIN_PER_COLOR[w], f"{w} color {c}: only {n} lines"
        for s in SEASONS:
            n = sum(1 for when in by_world[w] if when.get("season") == s)
            assert n >= MIN_PER_SEASON[w], f"{w} season {s}: only {n} lines"
    for need in NEEDS:
        n = sum(1 for when in by_world["E"] if need in when.get("need", ()))
        assert n >= MIN_EARTH_PER_NEED, f"E need {need}: only {n} lines"
    print("\nAll checks passed.")


if __name__ == "__main__":
    check()
