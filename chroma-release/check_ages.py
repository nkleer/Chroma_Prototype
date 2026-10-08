"""Release check C-X4 (chroma-release/checklist.md, section 9): age and stage sense of every status, perk and title.

Over --lives simulated lives (default 1,000, birth to --years), as the game plays an Earth life (the outer world on,
pace 1, modern technology, middle warming; --world off for the world-off engine):
  FAIL  a title or perk gained outside its catalogue ages= (the engine's `title_ages`)
  FAIL  one held below its ages=, or more than a year past them (the engine drops outgrown ones once a year)
  FAIL  'eldest child' held by someone with an older sibling, or gained with no younger sibling (N4)
  FAIL  a career title held before 14 (no career title in childhood)
  FAIL  'retiree' gained by someone who never held a career title, or before the retiree's ages=
  REVIEW the catalogue's needs: for every item whose `needs` names other items in [brackets], how often it is gained
         by someone who never held any of them before (needs are prose: "or", "and", "makes it easier")
The weekly check reads the engine's own arrays (r_has, dead, older_sib, younger_sib) through the `intervention` hook,
which changes nothing in the lives. Read only: the engine and the Library are imported, nothing is written there.

    python3 -B chroma-release/check_ages.py [--proto DIR] [--lib DIR] [--roles FILE] [--packs a,b,c] [--lives 1000]
                                            [--years 95] [--jobs 4] [--seed 4001] [--world on|off]

Defaults: today's engine, the live Library batch and catalogue (top of chroma-library; was staging/next3), batch.PACKS.
Writes chroma-release/out/ages_<UTC time>.txt. Exit code 0 when nothing FAILs."""
import sys, os, re, argparse, time, collections
import multiprocessing as mp
import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py
ap = argparse.ArgumentParser()
ap.add_argument("--proto", default=P["engine_live"])   # the engine to check (v22_checks.py lays a candidate there)
ap.add_argument("--lib", default=P["library_live"])
ap.add_argument("--roles", default=path("library_live", "earth_perks_titles.py"))
ap.add_argument("--packs", default=None)
ap.add_argument("--lives", type=int, default=1000)
ap.add_argument("--years", type=int, default=95)
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--seed", type=int, default=4001)
ap.add_argument("--world", default="on", choices=("on", "off"))
a = ap.parse_args()
sys.path.insert(0, os.path.abspath(a.proto))
import engine as E, batch
batch.LIB_DIR = os.path.abspath(a.lib)
PACKS = list(batch.PACKS) if a.packs is None else [p for p in a.packs.split(",") if p]
EX = 4   # examples kept per kind of breach


def one(job):
    seed, n = job
    L = batch.load_batch("earth", roles=a.roles, packs=PACKS)
    G = L["ROLES"]; names = G["names"]; NT = G["NT"]; lo, hi = G["ages"][:, 0], G["ages"][:, 1]
    ID = G["ID"]; ELD = ID.get("eldest child", -1); RET = ID.get("retiree", -1)
    CAREER = np.zeros(len(names), bool); CAREER[:NT] = G["tkind"] == list(batch.TITLE_KINDS).index("career")
    P = dict(E.DEFAULT)
    if a.world == "on":
        P.update(world=True, world_seed=seed, world_cfg=dict(setting="earth", pace=1.0, tech_level="modern", climate="middle"))
    st = dict(held_low=collections.Counter(), held_high=collections.Counter(), career_child=collections.Counter(),
              eld_older=0, eld_noyounger=0, ex=collections.defaultdict(list), weeks=0)
    prev = {}

    def note(kind, s):
        if len(st["ex"][kind]) < EX:
            st["ex"][kind].append(s)

    def hook(t, P_, nic, y):
        f = sys._getframe(1).f_locals
        r_has = f.get("r_has")
        if r_has is None:
            return
        st["weeks"] += 1
        age = t / 52.0
        live = ~np.asarray(f.get("dead", np.zeros(len(r_has), bool)), bool)
        h = r_has & live[:, None]
        low = h & (age < lo)[None]
        high = h & (age > hi + 1 + 1 / 52)[None]
        for name_, m_ in (("held_low", low), ("held_high", high)):
            if m_.any():
                for n_, i_ in zip(*np.nonzero(m_)):
                    st[name_][names[i_]] += 1
                    note(name_, f"life {seed}:{n_} holds {names[i_]!r} at {age:.1f} (ages {lo[i_]:g} to {hi[i_]:g})")
        if age < 14:
            cc = h & CAREER[None]
            for n_, i_ in zip(*np.nonzero(cc)):
                st["career_child"][names[i_]] += 1
                note("career_child", f"life {seed}:{n_} holds career {names[i_]!r} at {age:.1f}")
        if ELD >= 0:
            older, younger = f.get("older_sib"), f.get("younger_sib")
            e_ = h[:, ELD]
            if older is not None:
                bad = e_ & (np.asarray(older) > 0)
                st["eld_older"] += int(bad.sum())
                for n_ in np.nonzero(bad)[0]:
                    note("eld_older", f"life {seed}:{n_} is 'eldest child' at {age:.1f} with {int(older[n_])} older sibling(s)")
            if younger is not None and "eld" in prev:
                new_ = e_ & ~prev["eld"]
                bad = new_ & (np.asarray(younger) <= 0)
                st["eld_noyounger"] += int(bad.sum())
                for n_ in np.nonzero(bad)[0]:
                    note("eld_noyounger", f"life {seed}:{n_} becomes 'eldest child' at {age:.1f} with no younger sibling")
            prev["eld"] = e_.copy()

    t0 = time.time()
    o = E.run(N=n, years=a.years, seed=seed, lib=L, P=P, intervention=hook)
    R = o.get("roles")
    gained_out = collections.Counter(); ret_nowork = 0; ret_young = 0
    needs_n = collections.Counter(); needs_miss = collections.Counter(); gains = collections.Counter()
    NEEDS = {}
    cat = {x["name"]: x for x in list(L.get("TITLES", [])) + list(L.get("PERKS", []))}
    if not cat:
        import importlib.util
        sp = importlib.util.spec_from_file_location("cat_checked", a.roles); m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m); cat = {x["name"]: x for x in list(m.TITLES) + list(m.PERKS)}
    for nm, x in cat.items():
        txt_ = str(x.get("needs") or "")   # a name after "not", "no", "without" or "distinct from" is not a need
        ref = [m_.group(1).strip() for m_ in re.finditer(r"\[([^\]]+)\]", txt_) if m_.group(1).strip() in ID
               and not re.search(r"\b(not|no|without|distinct from( being)?( an?)?)\s*$", txt_[:m_.start()])]
        if ref:
            NEEDS[nm] = set(ref)
    ever = collections.defaultdict(set)
    for (nn, t, i, what, how) in (R["log"] if R else []):
        nm = names[i]; age = t / 52.0
        if what == "gained":
            gains[nm] += 1
            if not (lo[i] <= age <= hi[i]):
                gained_out[nm] += 1
                note("gained_out", f"life {seed}:{nn} gains {nm!r} at {age:.2f} (ages {lo[i]:g} to {hi[i]:g}, {how})")
            if i == RET:
                if not any(CAREER[ID[e_]] for e_ in ever[nn]):
                    ret_nowork += 1
                    note("ret_nowork", f"life {seed}:{nn} gains 'retiree' at {age:.1f} never having held a career title ({how})")
                if age < lo[i]:
                    ret_young += 1
            if nm in NEEDS:
                needs_n[nm] += 1
                if not (NEEDS[nm] & ever[nn]):
                    needs_miss[nm] += 1
                    note("needs:" + nm, f"life {seed}:{nn} at {age:.1f} ({how})")
            ever[nn].add(nm)
    return dict(seed=seed, n=n, secs=time.time() - t0, weeks=st["weeks"], roles_on=R is not None,
                held_low=st["held_low"], held_high=st["held_high"], career_child=st["career_child"],
                eld_older=st["eld_older"], eld_noyounger=st["eld_noyounger"], gained_out=gained_out,
                ret_nowork=ret_nowork, ret_young=ret_young, needs_n=needs_n, needs_miss=needs_miss, gains=gains,
                ex={k: v for k, v in st["ex"].items()}, needs=NEEDS)


if __name__ == "__main__":
    os.makedirs(P["release_out"], exist_ok=True)
    REPORT = path("release_out", time.strftime("ages_%Y%m%d-%H%M.txt", time.gmtime()))
    jobs = []
    per = -(-a.lives // a.jobs)
    for j in range(a.jobs):
        n = min(per, a.lives - j * per)
        if n > 0:
            jobs.append((a.seed + j, n))
    t0 = time.time()
    with mp.get_context("fork").Pool(len(jobs)) as pool:
        res = pool.map(one, jobs)
    tot = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list); sums = collections.Counter()
    for r in res:
        for k in ("held_low", "held_high", "career_child", "gained_out", "needs_n", "needs_miss", "gains"):
            tot[k].update(r[k])
        for k in ("eld_older", "eld_noyounger", "ret_nowork", "ret_young"):
            sums[k] += r[k]
        for k, v in r["ex"].items():
            ex[k] += v[:EX]
    out = []
    say = out.append
    say(f"C-X4 age and stage sweep, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC")
    say(f"  engine {os.path.join(os.path.abspath(a.proto), 'engine.py')}; Library {batch.LIB_DIR}; catalogue {a.roles}; packs {PACKS}")
    say(f"  {sum(r['n'] for r in res)} lives x {a.years} years, world {a.world}, seeds {[r['seed'] for r in res]}, "
        f"{time.time() - t0:.0f} s; every week checked ({res[0]['weeks']} weeks a run)")
    if not all(r["roles_on"] for r in res):
        say("MISS titles and perks are off in this engine (P['roles'])")
    fails = []

    def row(label, n, kind, counter=None):
        if n:
            fails.append(label)
        say(f"{'MISS' if n else 'ok  '} {label}: {n}" + (f"  ({', '.join(f'{k} {v}' for k, v in counter.most_common(8))})" if counter else ""))
        for s in ex.get(kind, [])[:EX] if n else []:
            say(f"       e.g. {s}")
    row("gains outside the catalogue's ages=", sum(tot["gained_out"].values()), "gained_out", tot["gained_out"])
    row("person-weeks holding an item below its ages=", sum(tot["held_low"].values()), "held_low", tot["held_low"])
    row("person-weeks holding an item over a year past its ages=", sum(tot["held_high"].values()), "held_high", tot["held_high"])
    row("person-weeks holding a career title before 14", sum(tot["career_child"].values()), "career_child", tot["career_child"])
    row("person-weeks as 'eldest child' with an older sibling", sums["eld_older"], "eld_older")
    row("'eldest child' gained with no younger sibling", sums["eld_noyounger"], "eld_noyounger")
    row("'retiree' gained never having held a career title", sums["ret_nowork"], "ret_nowork")
    row("'retiree' gained before its ages=", sums["ret_young"], "ret_young")
    say(f"  info: {sum(tot['gains'].values())} gains of {len(tot['gains'])} items; eldest child {tot['gains'].get('eldest child', 0)}, "
        f"retiree {tot['gains'].get('retiree', 0)}")
    say("\nREVIEW the catalogue's needs: gains by someone who never held any item the needs name (needs are prose; a high "
        "share is worth a look, not a breach)")
    rows_ = sorted(((tot["needs_miss"][k] / tot["needs_n"][k], k) for k in tot["needs_n"] if tot["needs_miss"][k]), reverse=True)
    for sh, k in rows_[:30]:
        say(f"  {k!r}: {tot['needs_miss'][k]} of {tot['needs_n'][k]} gains ({sh:.0%}) without "
            f"{' / '.join(sorted(res[0]['needs'].get(k, [])))}" + (f"; e.g. {ex['needs:' + k][0]}" if ex.get("needs:" + k) else ""))
    if not rows_:
        say("  none")
    say("\nC-X4: " + ("PASS" if not fails else f"FAIL ({len(fails)}: {'; '.join(fails)})"))
    say(f"report: {REPORT}")
    txt = "\n".join(out)
    print(txt)
    open(REPORT, "w").write(txt + "\n")
    import results; results.done('ages', 1 if fails else 0, REPORT)   # backend plan item 4: the result in out/results.jsonl
    sys.exit(1 if fails else 0)
