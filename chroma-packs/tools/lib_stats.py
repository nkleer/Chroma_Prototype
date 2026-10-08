"""Chance and tag balance of .lib moment files, per means color (Pathways and packs thread, 2026-10-05).

python3 lib_stats.py file.lib [more.lib ...]

Prints the mean chance per means color overall and per stage (Library rule: within 3 points of each other, so no
color is easier), and how many habit, door, identity, binds, self_control + and - tags each means color carries.
A combination option counts toward each of its means colors with weight 1/len. Standard library only.
"""
import re
import sys

COLORS = "WUBRG"
STAGES = ["child", "juvenile", "young_adult", "adult", "mature", "elder"]


def stages_of(s):
    s = s.strip()
    if s == "all":
        return STAGES
    if s.endswith("+"):
        return STAGES[STAGES.index(s[:-1].replace(" ", "_")):]
    return [x.replace(" ", "_") for x in re.split(r"[,\s]+", s) if x]


def read(paths):
    out = []
    for p in paths:
        cur = None
        for raw in open(p, encoding="utf-8"):
            line = raw.strip()
            if line.startswith("== "):
                cur = dict(name=line[3:], stages=STAGES, tier="", opts=[])
                out.append(cur)
            elif cur is not None and line.startswith("- "):
                parts = [x.strip() for x in line[1:].split(" | ")]
                code = parts[0].replace(" ", "")
                means = re.match(r"[WUBRG]+", code).group(0) if re.match(r"[WUBRG]+", code) else ""
                f = {}
                for x in parts[2:]:
                    if ":" in x:
                        k, v = [y.strip() for y in x.split(":", 1)]
                        f[k] = v
                    else:
                        f[x] = True
                cur["opts"].append((means, f))
            elif cur is not None and ":" in line and not line.startswith("#"):
                k, v = [y.strip() for y in line.split(":", 1)]
                if k == "stages":
                    cur["stages"] = stages_of(v)
                elif k == "tier":
                    cur["tier"] = v
    return out


def main(paths):
    sits = read(paths)
    tot = {c: [0.0, 0.0] for c in COLORS}
    per = {st: {c: [0.0, 0.0] for c in COLORS} for st in STAGES}
    tags = {c: {t: 0.0 for t in ("habit", "door", "identity", "binds", "sc+", "sc-")} for c in COLORS}
    n = 0
    for s in sits:
        if s["tier"] == "read":
            continue
        for means, f in s["opts"]:
            if not means:
                continue
            w = 1 / len(means)
            for c in means:
                for t in ("habit", "door", "identity", "binds"):
                    if t in f:
                        tags[c][t] += w
                if f.get("self_control") == "+":
                    tags[c]["sc+"] += w
                if f.get("self_control") == "-":
                    tags[c]["sc-"] += w
            if "chance" not in f:
                continue
            ch = float(f["chance"].rstrip("%"))
            n += 1
            for c in means:
                tot[c][0] += ch * w
                tot[c][1] += w
                for st in s["stages"]:
                    per[st][c][0] += ch * w
                    per[st][c][1] += w
    mean = lambda a: a[0] / a[1] if a[1] else float("nan")
    print(f"{len(sits)} moments, {n} options with chance")
    row = {c: mean(tot[c]) for c in COLORS}
    spread = max(row.values()) - min(row.values())
    print("overall  " + "  ".join(f"{c} {row[c]:5.1f}" for c in COLORS) + f"   spread {spread:.1f}" +
          ("" if spread <= 3 else "   <-- above 3"))
    for st in STAGES:
        if not any(per[st][c][1] for c in COLORS):
            continue
        r = {c: mean(per[st][c]) for c in COLORS}
        sp = max(r.values()) - min(r.values())
        print(f"{st:9s}" + "  ".join(f"{c} {r[c]:5.1f}" for c in COLORS) + f"   spread {sp:.1f}" +
              ("" if sp <= 3 else "   <-- above 3"))
    print("tags per means color (habit door identity binds sc+ sc-)")
    for c in COLORS:
        print(f"  {c}  " + "  ".join(f"{t} {tags[c][t]:4.1f}" for t in tags[c]))


if __name__ == "__main__":
    main(sys.argv[1:])
