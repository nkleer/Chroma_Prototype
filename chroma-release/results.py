"""Check results in one file, so the release record can be built from them (backend plan item 4, chroma-env/backend-plan.md).

Every release check appends one line to chroma-release/out/results.jsonl when it ends: which check, PASS or FAIL (or RAN,
MISS), when, where its report is, and a short note. v22_checks.py writes one line per check it runs or reuses; the
stand-alone scripts (check_speedpass, check_saves, check_legacy, check_pin, ...) write their own with done() as their last
line, unless v22_checks.py ran them. record.py reads them.

Each line also goes to the machine's own file, out/results.d/<machine>.jsonl (<machine> is a random id kept in the
machine's temp folder): when several machines append to results.jsonl at the same moment over the shared folder, one
write can replace the other (10-09: eleven lines lost), and a file only one machine writes keeps every line. read()
takes both, drops lines that are the same, and orders them by time.

    from results import add
    add("saves", "PASS", report_path, note="6 presets", candidate={"game": "/tmp/build/prototype"})
    done("saves", rc, REPORT)          # a check script's last line before sys.exit(rc)

    python3 -B chroma-release/results.py add <check id> <PASS|FAIL|RAN|MISS> <report path> [note]   # from a shell script
        (CHROMA_COMMIT, when set, names the repository commit the files came from, as for done())
    python3 -B chroma-release/results.py latest [id prefix]                                        # the newest per check
"""
import json, os, sys, time, tempfile, secrets, glob

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import path

FILE = path("release_out", "results.jsonl")
MINE_DIR = path("release_out", "results.d")


def machine():
    """This machine's id for its own results file: made once and kept in the temp folder, which each machine has alone
    (every container's host name is "vm")."""
    p = os.path.join(tempfile.gettempdir(), "chroma_results_machine")
    try:
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        os.write(fd, secrets.token_hex(6).encode()); os.close(fd)
    except FileExistsError:
        pass
    for _ in range(50):
        m = open(p).read().strip()
        if m:
            return m
        time.sleep(0.01)
    return "unknown"


def add(check, result, report="", note="", candidate=None, run=None, secs=None, reused_from=None):
    """Append one result. result: PASS, FAIL, RAN (ran, nothing to compare) or MISS (differs from the reference)."""
    row = dict(check=check, result=result, time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), report=report, note=note)
    for k, v in (("candidate", candidate), ("run", run), ("secs", secs), ("reused_from", reused_from)):
        if v is not None:
            row[k] = v
    line = json.dumps(row, sort_keys=True) + "\n"
    os.makedirs(MINE_DIR, exist_ok=True)
    for fp in (FILE, os.path.join(MINE_DIR, machine() + ".jsonl")):
        with open(fp, "a") as f:
            f.write(line)
    return row


def done(check, rc, report="", note=""):
    """A stand-alone check script's last line: its result, unless v22_checks.py ran it (that records the result itself).
    rc is the exit code the script ends with. CHROMA_COMMIT, when set, names the repository commit the files came from."""
    if os.environ.get("CHROMA_REC_OUT"):
        return None
    cand = {"commit": os.environ["CHROMA_COMMIT"]} if os.environ.get("CHROMA_COMMIT") else None
    return add(check, "PASS" if rc == 0 else "FAIL", report, note, candidate=cand, run=" ".join(sys.argv))


def read():
    """Every result line, from results.jsonl and each machine's own file, once each, oldest first."""
    seen, out = set(), []
    for fp in [FILE] + sorted(glob.glob(os.path.join(MINE_DIR, "*.jsonl"))):
        if not os.path.exists(fp):
            continue
        for ln in open(fp):
            ln = ln.strip()
            if not ln or ln in seen:
                continue
            try:
                out.append(json.loads(ln)); seen.add(ln)
            except ValueError:
                pass
    out.sort(key=lambda r: r.get("time", ""))   # stable: lines of the same second keep their file order
    return out


def latest(prefix=""):
    """The newest result of each check whose id starts with prefix."""
    out = {}
    for r in read():
        if r["check"].startswith(prefix):
            out[r["check"]] = r
    return out


if __name__ == "__main__":
    if len(sys.argv) >= 5 and sys.argv[1] == "add":
        add(sys.argv[2], sys.argv[3], sys.argv[4], " ".join(sys.argv[5:]),
            candidate={"commit": os.environ["CHROMA_COMMIT"]} if os.environ.get("CHROMA_COMMIT") else None)
    elif len(sys.argv) >= 2 and sys.argv[1] == "latest":
        for k, r in sorted(latest(sys.argv[2] if len(sys.argv) > 2 else "").items()):
            print(f"{r['result']:5s} {k:22s} {r['time']} UTC  {r.get('note', '')[:80]}  {r.get('report', '')}")
    else:
        print(__doc__)
        sys.exit(2)
