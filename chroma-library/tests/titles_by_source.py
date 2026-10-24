"""Lifetime title and perk shares, with where each first gain came from. 400 lives (4 x 100, seeds 11-14).
Usage: python3 titles_by_source.py <lib dir with earth.py, earth_perks_titles.py[, earth_<pack>.py]> <out.json> <engine copy dir> [packs]
  packs: comma-separated, e.g. science,politics,stage (default: none, the base batch only). Run it on a COPY of the engine
  (cp chroma-engine/prototype/*.py to a scratch dir): it imports the engine from that dir. Set PACK_DIR to chroma-packs.
Moved here from drafts/ for the release check (L7, 2026-10-06); the first version ran base only. Since 2026-10-07 (Emren's
point 4, "How age 5 person can have Eldest perk?") it also keeps the age of every first gain and lists the titles and
perks gained outside the catalogue's ages=."""
import sys, os, json, collections
sys.dont_write_bytecode = True
LIB = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); P = os.path.abspath(sys.argv[3])
PACKS = [x for x in (sys.argv[4] if len(sys.argv) > 4 else "").split(",") if x]
sys.path.insert(0, P); os.chdir(P)
from multiprocessing import Pool
import engine as E
import batch as B_
CAT = LIB + "/earth_perks_titles.py"
def one(seed):
    B_.LIB_DIR = LIB
    L = B_.load_batch("earth", roles=CAT, packs=PACKS)
    o = E.run(N=100, years=80, seed=seed, lib=L)
    R = o["roles"]; names = L["ROLES"]["names"]
    first = {}
    for (pn, t, i, what, how) in R["log"]:
        if what == "gained" and (pn, i) not in first:
            first[(pn, i)] = (str(how), t / 52)
    src = collections.defaultdict(collections.Counter); ages = collections.defaultdict(list)
    for (pn, i), (h, a) in first.items():
        src[names[i]][h] += 1; ages[names[i]].append((round(a, 1), h))
    return dict(ever={names[i]: int(v) for i, v in enumerate(R["ever"].sum(0))}, src={k: dict(v) for k, v in src.items()},
                ages={k: v for k, v in ages.items()},
                share={names[i]: float(L["ROLES"]["share"][i]) for i in range(len(names))})
if __name__ == "__main__":
    with Pool(4) as p: out = p.map(one, [11, 12, 13, 14])
    ever = collections.Counter(); src = collections.defaultdict(collections.Counter); ages = collections.defaultdict(list)
    for o in out:
        ever.update(o["ever"])
        for k, v in o["src"].items(): src[k].update(v)
        for k, v in o["ages"].items(): ages[k] += v
    sys.path.insert(0, LIB); import earth_perks_titles as C_
    CA = {x["name"]: (x["kind"], tuple(x.get("ages", (0, 110)))) for x in C_.TITLES + C_.PERKS}
    def q(xs, f):
        xs = sorted(xs); return xs[min(int(f * len(xs)), len(xs) - 1)] if xs else None
    res = {k: dict(cat=out[0]["share"][k], ever=ever[k] / 400, src=src[k].most_common(4),
                   age=dict(min=q([a for a, _ in ages[k]], 0), p5=q([a for a, _ in ages[k]], .05),
                            median=q([a for a, _ in ages[k]], .5), n=len(ages[k]))) for k in ever}
    json.dump(dict(packs=PACKS, lib=LIB, titles=res), open(OUT, "w"), indent=0)
    it = [(k, v) for k, v in res.items() if v["cat"] >= .01]
    me = sum(abs(v["ever"] - v["cat"]) for k, v in it) / len(it)
    over = sorted([(v["ever"] / v["cat"], k) for k, v in it if v["ever"] > 2 * v["cat"] and v["ever"] - v["cat"] > .03], reverse=True)
    under = [k for k, v in it if v["ever"] < .5 * v["cat"] and v["cat"] - v["ever"] > .03]
    print(f"packs {PACKS or 'none'}: {len(it)} titles and perks with a share of .01 or more; mean error {me:.3f}; "
          f"over 2x: {len(over)} ({', '.join(f'{k} {r:.1f}x' for r, k in over)}); under half: {under}")
    print("gained outside the catalogue's ages (age of first gain, how):")
    nage = 0
    for k in sorted(ages):
        kind, (lo, hi) = CA.get(k, ("?", (0, 110)))
        odd = [(a, h) for a, h in ages[k] if a < lo - .05 or a > hi + .05]
        if odd:
            nage += 1; hw = collections.Counter(h for _, h in odd).most_common(2)
            print(f"  {k} ({kind}, ages {lo}-{hi}): {len(odd)} of {len(ages[k])}, youngest {min(a for a, _ in odd)}, "
                  f"oldest {max(a for a, _ in odd)}; {'; '.join(f'{h[:50]} {c}' for h, c in hw)}")
    print(f"  {nage} titles and perks gained outside their ages" if nage else "  none")
    bad = sorted(res.items(), key=lambda kv: -(kv[1]["ever"] - kv[1]["cat"]))
    for k, r in bad[:45]:
        print("%-34s cat %.3f ever %.3f | %s" % (k[:34], r["cat"], r["ever"], "; ".join(f"{h[:38]} {c}" for h, c in r["src"][:3])))
