"""A release record that fills itself (backend plan item 4, chroma-env/backend-plan.md).

People write only the scope, Emren's rulings and the bar, in chroma-release/records/<version>/scope.md. The checks write
their results (out/results.jsonl, through results.py; v22_checks.py and the stand-alone check scripts do this). This
script joins the two into records/<version>/RECORD.md: one row per line of the bar, with the newest result of each of
its checks, when it ran, its report, and the verdict. Rerun it whenever a check finishes; never edit RECORD.md by hand.

    python3 -B chroma-release/record.py <version>          # writes records/<version>/RECORD.md and prints the verdict
    python3 -B chroma-release/record.py <version> --new    # writes a scope.md to fill in (the bar: every quick check)

scope.md holds three sections, written by people: "## Scope", "## Rulings" and "## Bar" (any other section, such as
notes before the record or the publish, is copied into RECORD.md in its place before the bar), plus two optional lines near
the top: "commit: <sha>" (only results of checks run on that repository commit count; repo workflow step 6: a release
is checked from a commit of main) and "since: YYYY-MM-DD HH:MM" in UTC (only results from then on count). The bar is a
table "| Row | Checks | What |" whose Checks cell names result ids separated by commas (v22_checks.py --list shows
them; a stand-alone script's id is in its own doc). A row passes when every one of its checks' newest results is PASS;
a check that "RAN" (nothing to compare against) leaves the row open until someone writes "ran is enough" in its What.

From v25 the bar may have a fourth column, Strength (Emren's decisions file for v25, section 11): mandatory,
calibration or diagnostic. A check's result is then PASS, FAIL (or MISS), INCONCLUSIVE, or RAN; a row's state is the
worst of its checks' (FAIL, INCONCLUSIVE, OPEN while a check has not run, PASS). A row whose What begins "NOT
APPLICABLE:" is a coherent cut and needs its row named in the "For v25.1" section, or it fails. "Ran is enough" does
not apply: RAN counts as INCONCLUSIVE on a mandatory row, and as run on the others. READY needs every mandatory row PASS
or NOT APPLICABLE and every other row run; calibration and diagnostic results are reported and do not block.
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "chroma-env")); sys.path.insert(0, HERE)
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(HERE))
from paths import path
import results

EMREN = 3 * 3600   # Emren's clock is UTC+3


def emren(t):
    """A UTC time from results.jsonl ("2026-10-08 13:19:35") in Emren's clock ("10-08 16:19")."""
    try:
        s = time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S")) + EMREN
        return time.strftime("%m-%d %H:%M", time.localtime(s))
    except ValueError:
        return t


def parse_scope(text):
    meta = {}
    for k in ("commit", "since"):
        m = re.search(r"^%s:\s*(\S.*?)\s*$" % k, text, re.M)
        if m and not m.group(1).startswith("<"):
            meta[k] = m.group(1)
    sections, cur = {}, None
    for ln in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", ln)
        if m:
            cur = m.group(1).strip().lower(); sections[cur] = []
        elif cur:
            sections[cur].append(ln)
    bar = []
    for ln in sections.get("bar", []):
        if not ln.lstrip().startswith("|"):   # only table lines are rows; prose with a "|" in it (a<b|c>) is not
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "row" or set(cells[0]) <= set("-: "):
            continue
        checks = [c.strip().strip("`") for c in cells[1].split(",") if c.strip()]
        strength = cells[3].lower() if len(cells) > 3 and cells[3] else None
        if strength not in (None, "mandatory", "calibration", "diagnostic"):
            sys.exit(f"bar row {cells[0]}: strength '{cells[3]}' is not mandatory, calibration or diagnostic")
        bar.append(dict(row=cells[0], checks=checks, what=cells[2], strength=strength))
    return meta, {k: "\n".join(v).strip() for k, v in sections.items()}, bar


def row_state(b, states, cut):
    """One row's state under a bar with strengths: the worst of its checks' results (FAIL, INCONCLUSIVE, OPEN, PASS)."""
    if b["what"].lower().startswith("not applicable"):
        return "NOT APPLICABLE" if re.search(r"(^|\W)%s(\W|$)" % re.escape(b["row"].split()[0]), cut) else "FAIL"
    worst = "PASS"
    for s in states:
        s = {"MISS": "FAIL", "NA": "INCONCLUSIVE", "N/A": "INCONCLUSIVE"}.get(s, s)  # N/A only by a written cut
        if s == "RAN":
            s = "INCONCLUSIVE" if b["strength"] == "mandatory" else "PASS"
        elif s == "WAITING":
            s = "OPEN"
        elif s not in ("PASS", "FAIL", "INCONCLUSIVE"):
            s = "INCONCLUSIVE"
        if ["PASS", "OPEN", "INCONCLUSIVE", "FAIL"].index(s) > ["PASS", "OPEN", "INCONCLUSIVE", "FAIL"].index(worst):
            worst = s
    return worst


def counts(r, meta):
    if meta.get("since") and r.get("time", "") < meta["since"]:
        return False
    if meta.get("commit"):
        c = (r.get("candidate") or {}).get("commit", "")
        return bool(c) and c.startswith(meta["commit"][:12]) and not (r.get("candidate") or {}).get("dirty")
    return True


def build(version):
    d = path("release", "records", version)
    scope_p = os.path.join(d, "scope.md")
    if not os.path.exists(scope_p):
        sys.exit(f"no {scope_p}: write it first (record.py {version} --new gives one to fill in)")
    meta, sec, bar = parse_scope(open(scope_p, encoding="utf-8").read())
    newest = {}
    for r in results.read():
        if counts(r, meta):
            newest[r["check"]] = r
    rows, open_rows, failed = [], [], []
    inconclusive, reported = [], []               # strength rows only: mandatory INCONCLUSIVE; calibration misses
    cut = sec.get("for v25.1", "") + "\n" + sec.get("for " + version + ".1", "")
    for b in bar:
        got = [newest.get(c) for c in b["checks"]]
        states = [g["result"] if g else "WAITING" for g in got]
        if b["strength"] is None:                 # a bar of three columns: as before v25
            ran_ok = "ran is enough" in b["what"].lower()
            if any(s in ("FAIL", "MISS") for s in states):
                state = "FAIL"; failed.append(b["row"])
            elif all(s == "PASS" or (s == "RAN" and ran_ok) for s in states):
                state = "PASS"
            else:
                state = "OPEN"; open_rows.append(b["row"])
        else:
            state = row_state(b, states, cut)
            name = f"{b['row']} ({b['strength']})"
            if b["strength"] == "mandatory":
                {"FAIL": failed, "INCONCLUSIVE": inconclusive, "OPEN": open_rows}.get(state, []).append(b["row"])
            elif state == "OPEN":
                open_rows.append(name)
            elif state in ("FAIL", "INCONCLUSIVE"):
                reported.append(f"{name} {state}")
        cells = []
        for c, g in zip(b["checks"], got):
            if not g:
                cells.append(f"{c}: not run")
                continue
            rep = os.path.relpath(g["report"], path("release")) if g.get("report", "").startswith(path("release")) else g.get("report", "")
            cells.append(f"{c}: {g['result']}{' (reused)' if g.get('reused_from') else ''}, {emren(g['time'])}"
                         + (f", `{rep}`" if rep else "") + (f"; {g['note'][:140]}" if g.get("note") and g["result"] != "PASS" else ""))
        st = ('**' + state + '**' if state != 'OPEN' else state) + (f" ({b['strength']})" if b["strength"] else "")
        rows.append(f"| {b['row']} | {b['what']} | {st} | {'<br>'.join(cells)} |")
    n_pass = sum(1 for r in rows if "**PASS**" in r or "**NOT APPLICABLE**" in r)
    ok = not open_rows and not failed and not inconclusive and bar
    strengths = any(b["strength"] for b in bar)
    verdict = (("READY: every mandatory row passes and every other row has run" if strengths
                else "READY: every row of the bar passes") if ok else
               "NOT READY: " + "; ".join(x for x in (f"failed {', '.join(failed)}" if failed else "",
                                                       f"inconclusive {', '.join(inconclusive)}" if inconclusive else "",
                                                       f"open {', '.join(open_rows)}" if open_rows else "",
                                                       "the bar is empty" if not bar else "") if x))
    if reported:
        verdict += ". Reported, not blocking: " + ", ".join(reported)
    now = time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time() + EMREN))
    out = [f"# Chroma release record: {version}", "",
           f"Built by `chroma-release/record.py {version}` at {now} Emren's time (UTC+3) from `out/results.jsonl` and "
           f"`records/{version}/scope.md`. Do not edit this file: change scope.md or run the checks, then run record.py again.", ""]
    if strengths:
        out += ["Each row has a strength (mandatory, calibration or diagnostic). Only mandatory rows decide READY; the "
                "others are reported with their results. A row reads PASS, FAIL, INCONCLUSIVE, OPEN (not run yet) or NOT "
                "APPLICABLE (a cut written under the next version).", ""]
    if meta.get("commit"):
        out += [f"Candidate: repository commit `{meta['commit']}` (only results of checks run on it count).", ""]
    if meta.get("since"):
        out += [f"Results from {meta['since']} UTC on.", ""]
    for name, body in sec.items():                 # every section in scope.md's order; the bar comes last, as a table
        if name != "bar" and body:
            out += [f"## {name[0].upper() + name[1:]}", "", body, ""]
    out += ["## The bar", "", f"**{verdict}.** {n_pass} of {len(bar)} rows pass.", "",
            "| Row | What | State | Checks (newest result, Emren's time, report) |", "|---|---|---|---|"] + rows + [""]
    open(os.path.join(d, "RECORD.md"), "w", encoding="utf-8").write("\n".join(out))
    print(f"{version}: {verdict}. {n_pass} of {len(bar)} rows pass. Written {os.path.join(d, 'RECORD.md')}")
    return 0 if verdict.startswith("READY") else 1


def new(version):
    d = path("release", "records", version)
    p = os.path.join(d, "scope.md")
    if os.path.exists(p):
        sys.exit(f"{p} exists; edit it")
    os.makedirs(d, exist_ok=True)
    lst = subprocess.run([sys.executable, "-B", os.path.join(HERE, "v22_checks.py"), "--list", "--json"], capture_output=True,
                         text=True, check=True).stdout
    rows = {}                                         # one bar row per record row (C-X1, C-L1, ...), its quick checks together
    for ln in lst.splitlines():
        c = json.loads(ln)
        if c["level"] in ("fast", "quick"):
            rows.setdefault(c["row"], []).append(c)
    bar = [f"| {r} | {', '.join(c['id'] for c in cs)} | {'; '.join(c['what'] for c in cs)} |" for r, cs in rows.items()]
    open(p, "w", encoding="utf-8").write(f"""# {version}: scope, rulings and bar

Written by people; record.py builds RECORD.md from it and the check results.

commit: <the repository commit of main this version is checked from; leave the angle brackets until it is chosen>
since: <YYYY-MM-DD HH:MM UTC, optional>

## Scope

<What this version changes, in Emren's words where there are any, with the date and time.>

## Rulings

<Emren's and the coordinator's rulings on the bar, one bullet each, with the date and time.>

## Bar

The publish bar Emren set on 10-07 (chroma-env/DECISIONS.md): every owner's checks on the final files. Same-lives
versions (no rate change) prove identical lives at 1,600 lives over four seeds instead of rerunning the statistics
(Emren 10-08 12:04 UTC). Add the version's own rows (speedpass, saves, the browser drivers) and remove what does not apply.

| Row | Checks | What |
|---|---|---|
""" + "\n".join(bar) + "\n")
    print(f"wrote {p}: fill in Scope, Rulings and the commit; {len(bar)} quick checks in the bar")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        print(__doc__); sys.exit(2)
    sys.exit(new(sys.argv[1]) if "--new" in sys.argv else build(sys.argv[1]))
