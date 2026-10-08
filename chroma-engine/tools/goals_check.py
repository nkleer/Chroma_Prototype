"""v7 goal statistics for one population: python3 chroma-engine/tools/goals_check.py [N] [seed] [P json] [earth|seed].
Goals are switched on (goals=True) unless P says otherwise."""
import sys, collections, numpy as np
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E

def stats(o, N):
    G = o["goals"]
    byid = collections.defaultdict(list)
    for g in G:
        byid[g["id"]].append(g)
    out = {}
    # plans: outcome by source and horizon
    plans = collections.defaultdict(lambda: collections.Counter())
    felt = collections.defaultdict(list); ach = collections.defaultdict(list)
    dur = collections.defaultdict(list)
    for gid, ev in byid.items():
        b = [e for e in ev if e["what"] == "begins" and e["kind"] == "plan"]
        if not b:
            continue
        b = b[-1]
        endings = [e for e in ev if e["what"] in ("achieved", "let go", "not reached in time", "drifted away", "pushed aside")]
        fin = endings[-1]["what"] if endings else "open"
        ext = sum(e["what"] == "extended" for e in ev)
        key = (b["source"], b["horizon"], "domain" if b["domain"] != "a pursuit" else "pursuit")
        plans[key][fin] += 1
        plans[key]["extended"] += ext > 0
        if fin != "open":
            felt[key].append(b["felt"]); ach[key].append(fin == "achieved")
            ontime = fin == "achieved" and ext == 0
            felt[("all", b["horizon"])].append(b["felt"]); ach[("all", b["horizon"])].append(ontime)
        if fin == "achieved":
            dur[b["horizon"]].append(endings[-1]["age"] - b["age"])
    print("plans per life:", round(sum(sum(v[k] for k in v if k != "extended") for v in plans.values()) / N, 2))
    for key in sorted(plans):
        v = plans[key]; tot = sum(v[k] for k in v if k != "extended")
        print(f"  {key}: n {tot}  achieved {v['achieved'] / max(tot, 1):.2f}  let go {v['let go'] / max(tot, 1):.2f}  "
              f"late {v['not reached in time'] / max(tot, 1):.2f}  drifted {v['drifted away'] / max(tot, 1):.2f}  "
              f"open {v['open'] / max(tot, 1):.2f}  extended {v['extended'] / max(tot, 1):.2f}  felt {np.mean(felt[key]) if felt[key] else float('nan'):.2f}")
    for h in E.HORIZONS:
        if felt[("all", h)]:
            print(f"  horizon {h}: felt at start {np.mean(felt[('all', h)]):.2f}, reached on time {np.mean(ach[('all', h)]):.2f}, "
                  f"years to reach (median) {np.median(dur[h]) if dur[h] else float('nan'):.2f}")
    # dreams
    dreams = [ev for ev in byid.values() if ev[0]["kind"] == "dream" and ev[0]["what"] == "begins"]
    fates = collections.Counter()
    for ev in dreams:
        last = [e["what"] for e in ev[1:]]
        fates[last[0] if last else "open"] += 1
    print("dreams per life:", round(len(dreams) / N, 2), dict(fates))
    trig = collections.Counter(ev[0].get("trigger") for ev in dreams)
    print("  sparks:", trig.most_common())
    ages = [ev[0]["age"] for ev in dreams]
    print("  age at dream start: p10/50/90", np.percentile(ages, [10, 50, 90]).round(1))
    # passions
    pas = [g for g in G if g["what"] == "became a passion"]
    print("passions per life:", round(len(pas) / N, 2), "age p10/50/90", np.percentile([g["age"] for g in pas], [10, 50, 90]).round(1) if pas else "",
          collections.Counter(g["sealed_by"] for g in pas))
    V = o["V_hist"]
    for yr in (10, 15, 20, 30, 40, 50, 60, 70):
        nd, npa, npl = V["n_dream"][yr], V["n_passion"][yr], V["n_plan"][yr]
        hm = V["harmonious"][yr]
        print(f"  age {yr}: dreams {nd.mean():.2f} (any {np.mean(nd > 0):.2f})  passions {npa.mean():.2f} (any {np.mean(npa > 0):.2f})"
              f"  harmonious mean {np.nanmean(hm) if np.any(~np.isnan(hm)) else float('nan'):.2f} (share >.5 {np.nanmean(hm[~np.isnan(hm)] > 0.5) if np.any(~np.isnan(hm)) else float('nan'):.2f})"
              f"  plans {npl.mean():.2f}  regret {V['regret'][yr].mean():.3f}")

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    import json
    P = {"goals": True, "history": "calm", **(json.loads(sys.argv[3]) if len(sys.argv) > 3 else {})}
    L = None
    if len(sys.argv) <= 4 or sys.argv[4] == "earth":
        from batch import load_batch
        L = load_batch("earth")
    o = E.run(N=N, seed=seed, years=80, P=P, lib=L)
    stats(o, N)
