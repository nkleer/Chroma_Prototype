"""The Book of Moments record and the peace reading (Emren chose "Book and peace", 21:44): play lives to the end with a mix
of own and pushed choices, check the record's keys against the catalogue and print the reading.
python3 test/book_check.py [lives] [push share]"""
import sys, os, random, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from console import Console
from game import book_catalog, PRESETS
n_lives = int(sys.argv[1]) if len(sys.argv) > 1 else 2
push = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
rnd = random.Random(11)
for trial in range(n_lives):
    t0 = time.time(); c = Console(); c.handle("")
    key = rnd.choice(list(PRESETS)); c.handle(key); c.handle("T" + str(trial))
    def send(x):
        text, busy = c.handle(x)
        while busy:
            _, busy = c.handle("")
    steps = 0; seen_book = 0
    while c.mode == "play" and steps < 4000:
        steps += 1
        if c.g.pending is not None and c.numbering and rnd.random() < push:
            send(str(rnd.choice(list(c.numbering))))
        else:
            send("")
        h = json.loads(json.dumps(c.hud(), default=str))
        if h.get("book"):
            seen_book += 1
    h = c.hud(); b = h.get("book"); r = c.g.review
    cat = book_catalog(c.g.setting)
    ck = {k for k, *_ in cat["moments"]}
    bad = [k for k in b["moments"] if k not in ck]
    print(f"life {trial} preset {key} {c.g.setting} age {r['age']} books {seen_book} moments {len(b['moments'])} deeds {len(b['deeds'])} "
          f"titles {len(b['titles'])} idents {len(b['idents'])} unknown keys {len(bad)} secs {time.time() - t0:.0f}")
    print("   ", {k: round(v, 2) for k, v in r.items() if k in ("fulfilment", "serenity", "integrity", "gifts")}, r["reading"])
    assert not bad, bad[:5]
print("catalogue sizes:", {w: (len(book_catalog(s)["moments"]), len(book_catalog(s)["titles"]), len(json.dumps(book_catalog(s)))) for w, s in (("earth", "earth"), ("base", "tribal"))})
