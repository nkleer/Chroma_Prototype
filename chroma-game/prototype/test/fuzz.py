import sys, time, random, traceback
import os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from console import Console
rnd = random.Random(5)
keys_play = ["", "", "", "", "w", "m", "y", "d", "s", "f", "v", "h", "l", "i", "p", "1", "2", "3", "UR", "x", "d1"]
for trial in range(6):
    c = Console(); t0 = time.time()
    c.handle("")  # menu
    pick = rnd.choice(["1", "2", "3", "4", "5", "6", "7"])
    script = [pick]
    if pick == "7":
        script += ["Q" + str(trial), rnd.choice(["1", "2", ""]), rnd.choice(["1", "2", "3"]), rnd.choice(["1", "2", "3"]), rnd.choice(["", "W", "UB", "RG", "WUBRG"]), rnd.choice("1234"),
                   rnd.choice("123"), "BG", rnd.choice(["", "U", "WR"]), str(rnd.choice([0, 5, 12, 25, 40, 60])), ""]
    else:
        script += [""]
    errs = 0; n = 0; cps = 0; forced = 0
    def send(x):
        global errs
        text, busy = c.handle(x)
        while busy:
            text2, busy = c.handle(""); text += text2
        if "[error" in text:
            errs += 1; print("ERROR", text[-400:])
        return text
    for x in script:
        send(x)
    while c.mode == "play" and n < 3000:
        n += 1
        if c.g.pending is not None:
            cps += 1
            if rnd.random() < 0.5 and c.numbering:
                send(str(rnd.choice(list(c.numbering)))); forced += 1
            else:
                send("")
        else:
            send(rnd.choice(keys_play))
    r = c.g.review if c.g is not None and c.g.over else None
    print(f"trial {trial} preset {pick} mode {c.mode} steps {n} checkpoints {cps} errors {errs} secs {time.time()-t0:.0f}",
          (f"fulfil {r['fulfilment']:.2f} seren {r['serenity']:.2f} integ {r['integrity']:.2f} paths {r['paths']}" if r else ""))
