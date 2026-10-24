"""Timeless modern setting check (Emren 2026-10-06 10:42, outer world thread: "do not mention the year specifically, act
like setting is passing in modern days. Technology and availability may differ. I dont want players to fell lots of
tiktok videos, or war at Korea like interactions").

Scans what the player reads (moment names, scenes, options with their say lines, works, fails, world wordings) for a
calendar year or dated decade, a real country, nation, language or city, a currency name, a brand or platform, a real war
or historical event, one culture's festival, and a real person. Research notes (times, likelier, rarer, comments) may cite real sources and are
not scanned. Since 2026-10-06 23:10 (release check L8) it also reads every string in the Library's data files the
player sees: dreams.py, earth_voice.py and the titles and perks catalogue (names, say lines, and the gained, lost and
needs notes). Usage:
    python3 check_setting.py                      the next batch: the live main parts (with $NEXT over them when set), and the data files
    python3 check_setting.py <dir, .lib or .py> ...  any parts or data files, e.g. a pack folder (read only)
Prints each hit and exits 1 if there is any. A hit is a question, not always a fault: an idiom ("a cold war" between
siblings) or an age ("in the seventies" for a person's age) can stay; add it to ALLOW below with the reason.
"""
import os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.path.abspath(f"{HERE}/..")
W = lambda xs: r"\b(" + "|".join(xs) + r")\b"
PAT = {
    "year": r"\b(1[5-9]\d\d|20\d\d)s?\b|\b'\d0s\b|\b\d0s\b"
            r"|\b(built|made|opened|since|from|back|during)( in)? the (twenties|thirties|forties|fifties|sixties|seventies|eighties|nineties|noughties)\b",
    "country, nation, language or city": W([
        "afghan\w*", "africa\w*", "america\w*", "argentin\w*", "asia\w*", "australia\w*", "austria\w*", "bangladesh\w*",
        "belgi\w*", "brazil\w*", "brit\w*", "england", "english", "canad\w*", "chin(a|ese)", "danish", "denmark", "dutch",
        "egypt\w*", "europe\w*", "finland", "finnish", "france", "french", "german\w*", "greece", "greek", "india", "indian",
        "ireland", "irish", "israel\w*", "ital(y|ian)\w*", "japan\w*", "kenya\w*", "korea\w*", "mexic\w*", "nigeria\w*",
        "norw\w*", "pakistan\w*", "poland", "portug\w*", "russia\w*", "scotland", "scottish", "spain", "spanish",
        "swed\w*", "swiss", "switzerland", "turkey", "turkish", "ukrain\w*", "uk", "usa", "u\.s\.", "wales", "welsh",
        "vietnam\w*", "iraq\w*", "iran\w*", "syria\w*", "london", "paris", "new york", "berlin", "rome", "tokyo",
        "manchester", "glasgow", "edinburgh", "dublin", "sydney", "toronto", "chicago", "los angeles", "hollywood",
        "bollywood", "broadway", "west end", "las vegas", "ibiza", "alps", "himalaya\w*", "everest", "sahara",
        "mandarin", "arabic", "hindi", "urdu", "swahili", "latin america\w*", "scandinavia\w*"]),
    "currency": r"[£$€¥]|\b(quid|dollars?|euros?|pence|cents|yen|rupees?|fiver|tenner)\b"
                r"|\b(\d[\d,]*|a|an|one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|eighty|hundred|"
                r"thousand|million|extra|few) pounds?\b|\bpounds? (an|a|per) \w+",
    "brand or platform": W([
        "tik ?tok", "instagram", "facebook", "youtube\w*", "twitter", "tweet\w*", "whats ?app", "snapchat", "google\w*",
        "iphone", "ipad", "android", "netflix", "amazon", "uber", "tinder", "grindr", "spotify", "playstation", "xbox",
        "nintendo", "lego", "coca-cola", "pepsi", "mcdonald'?s", "starbucks", "ikea", "ebay", "reddit", "discord",
        "zoom call", "skype", "microsoft", "linkedin", "bitcoin", "nike", "adidas", "walmart", "airbnb", "paypal",
        "wikipedia", "chatgpt", "gmail", "kindle", "monopoly", "scrabble", "barbie", "pok[eé]mon", "minecraft",
        "fortnite", "disney", "marvel", "harry potter", "star wars", "beatles", "twitch stream\w*", "onlyfans",
        "olympic\w*", "world cup", "super bowl", "wimbledon", "glastonbury", "eurovision", "nobel", "oscars?",
        "grammys?", "nhs", "gcses?", "a-levels?", "bbc", "fbi", "cia", "red cross", "nato", "the eu", "the un"]),
    "real war or historical event": W([
        "world war\w*", "ww(1|2|i|ii)", "the cold war", "9/11", "brexit", "covid\w*", "coronavirus", "holocaust",
        "falklands", "gulf war", "berlin wall", "great depression", "the blitz", "d-day", "hiroshima", "chernobyl",
        "two metres apart", "six feet apart", "moon landing", "apartheid"]),
    "one culture's festival": W([
        "christmas\w*", "xmas", "easter", "ramadan", "eid", "diwali", "hanukkah", "passover", "yom kippur", "thanksgiving",
        "halloween", "bonfire night", "guy fawkes", "valentine'?s", "st\.? patrick'?s", "boxing day", "good friday"]),
    "real person": W([
        "shakespeare", "einstein", "darwin", "newton", "curie", "mozart", "beethoven", "picasso", "van gogh", "gandhi",
        "mandela", "churchill", "hitler", "stalin", "marx", "freud", "elvis", "madonna", "beyonc\w*", "taylor swift",
        "bowie", "lennon", "dickens", "tolkien", "austen", "hemingway", "orwell", "obama", "trump", "thatcher",
        "kennedy", "lincoln", "napoleon", "caesar", "cleopatra"]),
}
CASE = {"country, nation, language or city": r"\b(US|EU|UN|USSR|UAE|NYC)\b"}   # abbreviations, matched with their case (not "us")
ALLOW = [   # (part, start of the line, the hit, why it stays)
    ("earth-child-inner.lib", "- U>R | learn to juggle, or skip double-dutch", "dutch", "double-dutch is a skipping game"),
]
VIS = re.compile(r"^(== |scene( [WUBRG])?:|- |works:|fails:|earth:|tribal:|magic:)")

NEXT = os.environ.get("NEXT", "")   # a batch being prepared, whose parts and catalogue win over the main folder's:
# NEXT=<lib>/drafts/next4 for the paused v23 drafts. Default (2026-10-08): none, so a plain run checks the live v22
# batch, as the old default drafts/next3 did (it went live as v22, file for file)

def parts(args):
    if not args:
        fs = {os.path.basename(f): f for f in sorted(glob.glob(f"{LIB}/earth-*.lib"))}
        fs.update({os.path.basename(f): f for f in sorted(glob.glob(f"{NEXT}/earth-*.lib"))} if NEXT else {})
        cat = f"{NEXT}/earth_perks_titles.py" if NEXT and os.path.exists(f"{NEXT}/earth_perks_titles.py") else f"{LIB}/earth_perks_titles.py"
        voice = f"{NEXT}/earth_voice.py" if NEXT and os.path.exists(f"{NEXT}/earth_voice.py") else f"{LIB}/earth_voice.py"
        return list(fs.values()) + [f"{LIB}/dreams.py", voice, cat]
    out = []
    for a in args:
        out += sorted(glob.glob(f"{a}/*.lib")) if os.path.isdir(a) else [a]
    return out

def lines(p):
    """(where, text) of what the player can read: the visible lines of a part, or every string in a data file."""
    if p.endswith(".lib"):
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            s = line.rstrip("\n")
            if VIS.match(s):
                yield i, s
        return
    import importlib.util
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3] + "_setting", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    def walk(x, at):
        if isinstance(x, str):
            yield at, x
        elif isinstance(x, dict):
            for k, v in x.items():
                yield from walk(v, f"{at}.{k}")
        elif isinstance(x, (list, tuple, set)):
            for j, v in enumerate(x):
                yield from walk(v, f"{at}[{j}]")
    for name in dir(m):
        if name.isupper():
            yield from walk(getattr(m, name), name)

hits = 0
for p in parts(sys.argv[1:]):
    for i, s in lines(p):
        for kind, pat, fl in [(k, v, re.I) for k, v in PAT.items()] + [(k, v, 0) for k, v in CASE.items()]:
            for m in re.finditer(pat, s, fl):
                if any(os.path.basename(p) == a and s.startswith(b) and m.group(0).lower() == c.lower() for a, b, c, _ in ALLOW):
                    continue
                hits += 1
                print(f"{os.path.basename(p)}:{i}: {kind}: '{m.group(0)}' in: {s[:160]}")
print(f"{hits} setting hits in {len(parts(sys.argv[1:]))} parts" if hits else "setting: no year, real place, currency, brand, real event or real person in player text")
sys.exit(1 if hits else 0)
