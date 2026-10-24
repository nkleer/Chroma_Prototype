# Checks chroma-library/earth_perks_titles.py against the engine's catalogue format (chroma-engine/perks-titles-format.md) and the
# Library's balance and realism rules (profiles, facets and turning points since volume 2, 13:20). The title color balance covers the five commitment kinds only: statuses carry
# no colors (ways="") and the checker makes sure of it. The share sum still counts every title, statuses included. Standard library only. Run: python3 check_earth_perks_titles.py
# Prints a markdown report; the Library keeps the last one in checks_perks_titles.md.
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True   # leave no __pycache__ in the shared folder
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "earth_perks_titles.py")   # the live catalogue since 2026-10-05 18:25
EARTH_MD = os.path.join(HERE, "..", "earth.md")
if len(sys.argv) > 2:   # a staged batch: python3 check_perks_titles.py <catalogue .py> <earth.md> (2026-10-07)
    DATA, EARTH_MD = sys.argv[1], sys.argv[2]
if False:   # 2026-10-06: the live earth.md is the one to check (staging/earth.md is the old batch)
    EARTH_MD = os.path.join(HERE, "..", "staging", "earth.md")

COLORS = "WUBRG"
ALLY = {"WU", "UB", "BR", "RG", "WG"}
ENEMY = {"WB", "UR", "BG", "WR", "UG"}
COMMITMENT_KINDS = ["career", "partner", "children", "community", "faith"]
TITLE_KINDS = COMMITMENT_KINDS + ["status"]   # statuses carry no colors (ways="") and stay out of the color balance
PERK_KINDS = ["skill", "credential", "standing", "bond", "asset"]
NEEDS = {"safety", "belonging", "autonomy", "competence", "meaning"}
RESOURCES = {"money", "time", "health", "ties", "freedom"}
MARKS = {"learned a skill", "made an enemy", "hid a wrong", "helped someone in need", "made a friend",
         "took a wild risk", "kept your word", "owned up", "turned down a chance", "defied an authority", "moved away",
         "broke your word", "stayed home", "left home", "refused someone in need", "gave in to pressure", "came home"}
TITLE_KEYS = {"name", "kind", "ways", "meets", "ages", "share", "say"}
PERK_KEYS = {"name", "kind", "ways", "odds", "skill_half", "retires", "ages", "share", "say"}
EXTRA_KEYS = {"gained", "lost", "needs", "cause"}   # cause: every change has a cause (L2, 10-18)
TITLE_EXTRA = {"profiles", "refines", "turning", "sphere", "face",   # sphere=, face=: item 15 (2026-10-09)
                 # engine 12:45 (profiles and facets) and Emren's turning points
               "sector", "role"}   # the outer world (world-fields.md, 2026-10-07) and sex and gender (chroma-identity)
SECTORS = {"farm", "industry", "services", "knowledge", "public"}
ROLES = {"women", "men"}
ENGINE_GRANTED = {"widowed", "retiree", "newcomer"}
SPREAD_MAX = 0.03
TITLE_SHARE = (10, 20)
PERK_SHARE = (15, 30)
ODDS = (0.02, 0.10)
MEETS_MAX = 0.15

problems = []


def problem(msg):
    problems.append(msg)


def load():
    spec = importlib.util.spec_from_file_location("perks_titles_draft", DATA)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TITLES, mod.PERKS


def situations():
    try:
        with open(EARTH_MD, encoding="utf-8") as f:
            sits = {line[4:].strip() for line in f if line.startswith("### ")}
    except OSError:
        problem("could not read earth.md, so situation names were not checked")
        return None
    return sits | lib_moments()


def lib_moments():
    """Moment names ('== name') in the Library's .lib files, which cause lines quote too (10-19). Their 'mark: x' values join
    MARKS, so a history mark the .lib files use (broke the law, used drugs, ...) is known without listing it by hand."""
    lib_dir, found = os.path.join(HERE, ".."), set()
    for fn in sorted(os.listdir(lib_dir)):
        if not fn.endswith(".lib"):
            continue
        with open(os.path.join(lib_dir, fn), encoding="utf-8") as f:
            for line in f:
                if line.startswith("== ") and not line.startswith("== bold:"):
                    found.add(line[3:].strip())
                for m in re.finditer(r"\bmark: ([a-z][a-z ]*[a-z])\s*(?:\||$)", line):
                    MARKS.add(m.group(1))
    return found


def ways_of(e):
    """The entry's ways as a list of letters, or None when malformed."""
    w = e.get("ways")
    if not isinstance(w, str):
        return None
    letters = w.split()
    if not letters or any(c not in COLORS for c in letters) or len(set(letters)) != len(letters):
        return None
    return letters


SPHERES = ["rule", "gather", "arts", "faith", "care", "learn", "prod", "comm", "prot"]   # item 15 (world-fields.md)


def check_entry(e, kinds, keys, where):
    name = e.get("name", "?")
    if "sphere" in e and e["sphere"] not in SPHERES:
        problem(f"{where} '{name}': sphere '{e['sphere']}' is not one of the nine")
    if "face" in e and not (isinstance(e["face"], str) and e["face"].count(".") == 1
                            and e["face"].split(".")[0] == e.get("sphere") and e["face"].split(".")[1] in COLORS):
        problem(f"{where} '{name}': face '{e.get('face')}' is not <its sphere>.<W|U|B|R|G>")
    missing = keys - set(e)
    if missing:
        problem(f"{where} '{name}': missing {', '.join(sorted(missing))}")
    allowed = keys | EXTRA_KEYS | ({"lasts"} | TITLE_EXTRA if where == "title" else set())
    extra = set(e) - allowed
    if extra:
        problem(f"{where} '{name}': unknown keys {', '.join(sorted(extra))}")
    if e.get("kind") not in kinds:
        problem(f"{where} '{name}': kind '{e.get('kind')}' is not one of {', '.join(kinds)}")
    ages = e.get("ages")
    if not (isinstance(ages, tuple) and len(ages) == 2 and all(isinstance(a, int) for a in ages)
            and 0 <= ages[0] < ages[1] <= 110):
        problem(f"{where} '{name}': ages {ages!r} is not (youngest, oldest) within 0 to 110")
    share = e.get("share")
    if not (isinstance(share, (int, float)) and 0 < share <= 1):
        problem(f"{where} '{name}': share {share!r} is not in (0, 1]")
    if not isinstance(e.get("say"), str) or not e.get("say").strip() or "{" in e.get("say", ""):
        problem(f"{where} '{name}': say should be a plain naming phrase")


def check_title(e):
    check_entry(e, TITLE_KINDS, TITLE_KEYS, "title")
    name = e.get("name", "?")
    if "sector" in e and (e["sector"] not in SECTORS or e.get("kind") != "career"):
        problem(f"title '{name}': sector {e['sector']!r} must be one of {', '.join(sorted(SECTORS))}, on a career")
    if "role" in e and e["role"] not in ROLES:
        problem(f"title '{name}': role {e['role']!r} must be women or men")
    for tok in str(e.get("meets", "")).split():
        m = re.fullmatch(r"(need|res):(\w+)([+-])(\d*\.\d+|\d+)", tok)
        if not m:
            problem(f"title '{name}': meets token '{tok}' is not in base: syntax")
            continue
        group, what, _, size = m.groups()
        if what not in (NEEDS if group == "need" else RESOURCES):
            problem(f"title '{name}': meets names unknown {group} '{what}'")
        if float(size) > MEETS_MAX:
            problem(f"title '{name}': meets token '{tok}' is larger than {MEETS_MAX}")
    toks = [t.split("+")[0].split("-")[0] for t in str(e.get("meets", "")).split()]
    if len(toks) != len(set(toks)):
        problem(f"title '{name}': meets names the same need or resource twice")
    if e.get("kind") == "status":
        if e.get("ways") != "":
            problem(f"title '{name}': a status carries no colors, so ways must be \"\" (it is {e.get('ways')!r})")
        lasts = e.get("lasts")
        if not (lasts == "life" or (isinstance(lasts, (int, float)) and lasts > 0)):
            problem(f"title '{name}': a status needs lasts = \"life\" or a number of years")
    elif "lasts" in e and not e.get("refines"):
        problem(f"title '{name}': lasts is for statuses and facets only")
    prof = e.get("profiles")
    if prof is not None:
        if e.get("kind") == "status":
            problem(f"title '{name}': a status carries no profiles")
        elif not (isinstance(prof, list) and 2 <= len(prof) <= 3 and all(isinstance(p_, tuple) and len(p_) == 2
                  and isinstance(p_[1], str) and p_[1].strip() for p_ in prof)):
            problem(f"title '{name}': profiles must be two or three (letters, words) pairs")
        else:
            for c_, _ in prof:
                if ways_of({"ways": c_}) is None:
                    problem(f"title '{name}': profile letters {c_!r} are malformed")
            if e.get("ways") != prof[0][0]:
                problem(f"title '{name}': ways {e.get('ways')!r} should be the first profile's letters {prof[0][0]!r}")
            if len({c_ for c_, _ in prof}) != len(prof):
                problem(f"title '{name}': two profiles have the same letters")
    if "turning" in e and not (isinstance(e["turning"], str) and e["turning"].strip()):
        problem(f"title '{name}': turning should be Emren's turning-point text")


def check_facets(titles):
    """refines= names a commitment-kind title of the same kind, and a facet refines no facet."""
    by = {e.get("name"): e for e in titles}
    n = 0
    for e in titles:
        r = e.get("refines")
        if not r:
            continue
        n += 1
        for r1 in ([x.strip() for x in r.split(";")] if isinstance(r, str) else list(r)):   # several with ";" (engine 15:00)
            t_ = by.get(r1)
            if t_ is None:
                problem(f"title '{e.get('name')}': refines '{r1}', which is not a title here")
            elif t_.get("kind") != e.get("kind") or e.get("kind") == "status":
                problem(f"title '{e.get('name')}': a facet must be of its refined title's kind ({t_.get('kind')}), not a status")
    return n


def check_perk(e):
    check_entry(e, PERK_KINDS, PERK_KEYS, "perk")
    name = e.get("name", "?")
    odds = e.get("odds")
    if e.get("kind") in ("credential", "asset"):   # access perks: no odds, they work through requires: on acts (engine 08:55)
        if odds not in (0, None):
            problem(f"perk '{name}': an access perk ({e.get('kind')}) should have odds 0, not {odds!r}")
    elif not (isinstance(odds, (int, float)) and ODDS[0] <= odds <= ODDS[1]):
        problem(f"perk '{name}': odds {odds!r} is outside {ODDS[0]} to {ODDS[1]}")
    sh = e.get("skill_half", 0)
    if not (sh is None or (isinstance(sh, (int, float)) and sh > 0)):
        problem(f"perk '{name}': skill_half {sh!r} is not None or a number of years")
    ret = e.get("retires", 0)
    ages = e.get("ages") or (0, 110)
    if not (ret is None or (isinstance(ret, int) and ages[0] < ret <= ages[1] + 1)):
        problem(f"perk '{name}': retires {ret!r} is not None or an age within its ages")


def color_table(entries, kinds, label):
    out = []
    total = dict.fromkeys(COLORS, 0.0)
    per_kind = {k: dict.fromkeys(COLORS, 0.0) for k in kinds}
    count = {k: 0 for k in kinds}
    shapes = {"single": 0, "ally pair": 0, "enemy pair": 0, "triad": 0, "other": 0}
    bad = []
    for e in entries:
        letters = ways_of(e)
        if letters is None:
            bad.append(e.get("name", "?"))
            continue
        k = e.get("kind")
        if k in count:
            count[k] += 1
        sets = [ways_of({"ways": c_}) or letters for c_, _ in e.get("profiles") or [(e.get("ways"), "")]]
        for ls in sets:
            for c in ls:
                total[c] += 1 / len(ls)
                if k in per_kind:
                    per_kind[k][c] += 1 / len(ls)
        for letters in sets:
            if len(letters) == 1:
                shapes["single"] += 1
            elif len(letters) == 2:
                pair = "".join(sorted(letters, key=COLORS.index))
                shapes["ally pair" if pair in ALLY else "enemy pair"] += 1
            elif len(letters) == 3:
                shapes["triad"] += 1
            else:
                shapes["other"] += 1
    mean = sum(total.values()) / 5
    spread = (max(total.values()) - min(total.values())) / mean if mean else 1.0
    ok = spread <= SPREAD_MAX
    out.append(f"### {label}: ways per color (each profile counts 1, split over its letters; an entry without profiles counts its ways once)\n")
    out.append("| " + " | ".join(COLORS) + " | spread | |")
    out.append("|" + "---|" * 7)
    out.append("| " + " | ".join(f"{total[c]:.2f}" for c in COLORS) +
               f" | {100 * spread:.1f}% | {'pass' if ok else 'FAIL'} (limit {100 * SPREAD_MAX:.0f}%) |")
    if not ok:
        problem(f"{label}: color spread {100 * spread:.1f}% is over {100 * SPREAD_MAX:.0f}%")
    out.append("")
    out.append("Shapes: " + ", ".join(f"{v} {k}" for k, v in shapes.items() if v or k != "other"))
    out.append("")
    out.append(f"### {label}: count and colors per kind\n")
    out.append("| kind | count | " + " | ".join(COLORS) + " | all five |")
    out.append("|" + "---|" * 8)
    for k in kinds:
        present = all(per_kind[k][c] > 0 for c in COLORS)
        if not present:
            problem(f"{label}: kind '{k}' lacks {''.join(c for c in COLORS if per_kind[k][c] == 0)}")
        out.append(f"| {k} | {count[k]} | " + " | ".join(f"{per_kind[k][c]:.2f}" for c in COLORS) +
                   f" | {'yes' if present else 'NO'} |")
    out.append(f"| all | {sum(count.values())} | " + " | ".join(f"{total[c]:.2f}" for c in COLORS) + " | |")
    out.append("")
    if bad:
        problem(f"{label}: malformed ways (must be distinct letters from WUBRG, so the weights sum to 1): {', '.join(bad)}")
    out.append("Ways entries that are malformed (weights not summing to 1): " + (", ".join(bad) if bad else "none"))
    out.append("")
    return out


def share_line(entries, label, target):
    total = sum(e.get("share", 0) for e in entries if isinstance(e.get("share"), (int, float)))
    ok = target[0] <= total <= target[1]
    if not ok:
        problem(f"{label}: share sums to {total:.2f}, outside {target[0]} to {target[1]}")
    by_kind = {}
    for e in entries:
        by_kind[e.get("kind")] = by_kind.get(e.get("kind"), 0) + e.get("share", 0)
    parts = ", ".join(f"{k} {v:.2f}" for k, v in by_kind.items())
    return [f"- {label}: sum of share {total:.2f} (target {target[0]} to {target[1]}): {'pass' if ok else 'FAIL'}",
            f"  - by kind: {parts}"]


def references(titles, perks, sits):
    """[name] must be a title or perk here; 'quoted' text must be an earth.md situation or a history mark."""
    names = {e.get("name") for e in titles + perks}
    known = (sits or set()) | MARKS
    known_sorted = sorted(known, key=len, reverse=True)
    bad_brackets, bad_quotes, used_sits, used_marks = [], [], set(), set()
    for e in titles + perks:
        for field in ("gained", "lost", "needs"):
            text = e.get(field, "")
            for ref in re.findall(r"\[([^\]]+)\]", text):
                if ref not in names:
                    bad_brackets.append(f"{e.get('name')}.{field}: [{ref}]")
            for m in re.finditer(r"(?:(?<=^)|(?<=[\s(]))'", text):
                rest = text[m.end():]
                hit = next((k for k in known_sorted if rest.startswith(k + "'")), None)
                if hit:
                    (used_marks if hit in MARKS else used_sits).add(hit)
                elif sits is not None:
                    end = re.search(r"'(?![a-z])", rest)
                    bad_quotes.append(f"{e.get('name')}.{field}: '{rest[:end.start()] if end else rest}'")
    for b in bad_brackets:
        problem(f"unknown bracketed title or perk: {b}")
    for b in bad_quotes:
        problem(f"quoted text is not an earth.md situation or a history mark: {b}")
    return [f"- bracketed titles and perks that do not exist: {len(bad_brackets)}",
            f"- quoted situations or marks that do not exist: {len(bad_quotes)}",
            f"- earth.md situations named: {len(used_sits)}; history marks named: {len(used_marks)} of {len(MARKS)}"]


def main():
    titles, perks = load()
    sits = situations()
    for e in titles:
        check_title(e)
    for e in perks:
        check_perk(e)
    out = ["# Checks: chroma-library/earth_perks_titles.py\n",
           f"{len(titles)} titles, {len(perks)} perks (modern Earth). Format: chroma-engine/perks-titles-format.md.\n"]
    commitment = [e for e in titles if e.get("kind") != "status"]
    statuses = [e for e in titles if e.get("kind") == "status"]
    out += color_table(commitment, COMMITMENT_KINDS, "TITLES (commitment kinds)")
    colored = [e.get("name") for e in statuses if e.get("ways") != ""]
    out.append(f"Statuses: {len(statuses)}, outside the color balance; with ways other than \"\": "
               + (", ".join(colored) if colored else "none") + "\n")
    n_fac = check_facets(titles)
    n_prof = sum(1 for e in titles if e.get("profiles"))
    out.append(f"Titles with profiles: {n_prof}; facets (refines=): {n_fac}; with Emren's turning point: "
               f"{sum(1 for e in titles if e.get('turning'))}\n")
    out += color_table(perks, PERK_KINDS, "PERKS")
    out.append("### Realism: expected number held over one life\n")
    out += share_line(titles, "TITLES", TITLE_SHARE)
    out += share_line(perks, "PERKS", PERK_SHARE)
    out.append("")
    out.append("### Names, fields and references\n")
    seen, dups = {}, []
    for where, lst in (("title", titles), ("perk", perks)):
        for e in lst:
            n = e.get("name")
            if n in seen:
                dups.append(f"{n} ({seen[n]} and {where})")
            seen[n] = where
    for d in dups:
        problem(f"duplicate name: {d}")
    out.append("- duplicate names: " + (", ".join(dups) if dups else "none"))
    granted = {e.get("name") for e in titles if e.get("kind") == "status"} & ENGINE_GRANTED
    if granted != ENGINE_GRANTED:
        problem(f"engine-granted statuses missing: {', '.join(sorted(ENGINE_GRANTED - granted))}")
    out.append(f"- statuses the engine grants, named here: {', '.join(sorted(granted))}")
    out += references(titles, perks, sits)
    out.append("")
    out.append("### Result\n")
    if problems:
        out.append(f"{len(problems)} problem(s):\n")
        out += [f"- {p}" for p in problems]
    else:
        out.append("All checks pass.")
    print("\n".join(out))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
