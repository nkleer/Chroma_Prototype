"""v24 FP4 fp_titles and fp_alone_well (records/v24/scope.md) from the played heights lives (out/v24/heights/play_<sha7>/,
run.sh let, reader and none) against v23.1's (out/heights/play_e69b3bf/, the same presets 1 to 4 and seeds 1 to 6):

    python3 -B fp4.py <sha7> --rule today|band|plus1 [--out REPORT]

  fp_titles      catalogue titles a life (titles held that are in the Library's earth_perks_titles TITLES, as
                 cand_910fa57's judge67.py counts them) for the let and reader players. --rule is Emren's reading of the
                 Library's band (Rulings, "Titles a life"; their card): today = no higher than v23.1's, within twice the
                 paired standard error; band = 20 or fewer; plus1 = no more than one above v23.1's, within the same noise
  fp_alone_well  the review's well-being ('well') of the life left alone (none): not below v23.1's by more than twice the
                 paired standard error (v23.2 plays v23.1's lives)
fp_ties is read from the F9 tables (f9_parents, f9_partners, f9_means) in short-v24's `final`, not here."""
import argparse, glob, importlib.util, json, math, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
V24 = os.path.dirname(HERE)
BASE = os.path.join(os.path.dirname(V24), "heights", "play_e69b3bf")


def lives(d, pol, cat):
    out = {}
    for f in glob.glob(os.path.join(d, "*.json")):
        r = json.load(open(f))
        if r.get("policy") != pol or r.get("read_goals"):
            continue
        out[(str(r["preset"]), int(r["seed"]))] = dict(cat=sum(1 for nm, _ in r["titles"] if nm in cat), well=r.get("well"))
    return out


def paired(a, b, k):
    ks = sorted(set(a) & set(b))
    d = [a[x][k] - b[x][k] for x in ks if a[x][k] is not None and b[x][k] is not None]
    if len(d) < 2:
        return None, None, len(d)
    m = sum(d) / len(d); sd = math.sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return m, sd / math.sqrt(len(d)), len(d)


def catalogue(tree_lib):
    spec = importlib.util.spec_from_file_location("ept", os.path.join(tree_lib, "earth_perks_titles.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return {t["name"] for t in m.TITLES}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("sha7"); a.add_argument("--rule", required=True, choices=("today", "band", "plus1")); a.add_argument("--out")
    a.add_argument("--lib", help="the candidate's chroma-library (default: the worktree run.sh left in /tmp/h24_let/wt)")
    a.add_argument("--base-lib", default="/tmp/ept", help="v23.1's chroma-library/earth_perks_titles.py folder")
    a.add_argument("--play-dir", help="trials: another folder of played lives")
    a = a.parse_args()
    s7 = a.sha7[:7]; new = a.play_dir or os.path.join(V24, "heights", f"play_{s7}")
    lib = a.lib or "/tmp/h24_let/wt/chroma-library"
    cn, cb = catalogue(lib), catalogue(a.base_lib)
    rep = [f"v24 FP4 on {s7}, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC; rule {a.rule}; catalogue {lib} "
           f"({len(cn)} titles), v23.1's {a.base_lib} ({len(cb)})", ""]
    ok_t = True
    for pol in ("let", "reader"):
        N, B = lives(new, pol, cn), lives(BASE, pol, cb)
        if len(N) < 24 or len(B) < 24:
            rep.append(f"  {pol}: {len(N)} candidate and {len(B)} v23.1 lives: not read"); ok_t = False; continue
        mn = sum(x["cat"] for x in N.values()) / len(N); mb = sum(x["cat"] for x in B.values()) / len(B)
        d, se, n = paired(N, B, "cat")
        ok = {"today": d <= 2 * se, "band": mn <= 20, "plus1": d <= 1 + 2 * se}[a.rule]
        ok_t &= ok
        rep.append(f"  {pol}: catalogue titles a life {mn:.1f} (v23.1 {mb:.1f}; paired {d:+.2f} +- {se:.2f}, {n} lives): {'ok' if ok else 'OUT'}")
    rep.append(f"FP4 fp_titles: {'PASS' if ok_t else 'FAIL'} (rule {a.rule})")
    N, B = lives(new, "none", cn), lives(BASE, "none", cb)
    d, se, n = paired(N, B, "well")
    if d is None or n < 24:
        ok_w = False; rep.append(f"FP4 fp_alone_well: {n} paired lives left alone: not read")
    else:
        ok_w = d >= -2 * se
        rep.append(f"FP4 fp_alone_well: well-being left alone {sum(x['well'] for x in N.values()) / len(N):.3f} "
                   f"(v23.1 {sum(x['well'] for x in B.values()) / len(B):.3f}; paired {d:+.4f} +- {se:.4f}, floor {-2 * se:+.4f}): "
                   f"{'PASS' if ok_w else 'FAIL'}")
    txt = "\n".join(rep) + "\n"
    if a.out:
        open(a.out, "w").write(txt)
    print(txt)
    return 0 if ok_t and ok_w else 1


if __name__ == "__main__":
    sys.exit(main())
