"""Average fits made on different lives (10-09: three sessions, each with its own SEEDS, so the floors are fitted on about
2,400 lives instead of 600). ROLE_NORM fits (roles_check.py's json) are averaged in log space, TIER_LIFT fits
(tier_fit.py's json, {pack set: {career, summit, split}}) as plain means; an item missing from a fit counts at that fit's
default (norm 1, lift 0).

python3 -B chroma-engine/tools/fit_average.py norm <out.json> <fit1.json> <fit2.json> ...
python3 -B chroma-engine/tools/fit_average.py tier <out.json> <fit1.json> <fit2.json> ..."""
import json
import sys

import numpy as np


def norm(fits):
    keys = sorted(set().union(*fits))
    return {k: round(float(np.exp(np.mean([np.log(f.get(k, 1.0)) for f in fits]))), 3) for k in keys}


def tier(fits):
    out = {}
    for key in sorted(set().union(*fits)):
        fs = [f.get(key, {}) for f in fits]
        res = {t: round(float(np.mean([f.get(t, 0.0) for f in fs])), 4) for t in ("career", "summit")}
        names = sorted(set().union(*(f.get("split", {}) for f in fs)))
        res["split"] = {n: round(float(np.mean([f.get("split", {}).get(n, 0.0) for f in fs])), 4) for n in names}
        out[key] = res
    return out


if __name__ == "__main__":
    kind, dst, srcs = sys.argv[1], sys.argv[2], sys.argv[3:]
    fits = [json.load(open(p)) for p in srcs]
    res = {"norm": norm, "tier": tier}[kind](fits)
    json.dump(res, open(dst, "w"), indent=0 if kind == "norm" else 1)
    print(f"{kind}: {len(fits)} fits averaged into {dst} ({len(res)} entries)")
