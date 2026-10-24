"""v24 FP3 fp_marks (records/v24/scope.md): none of the marks no title or perk rule reads is left unread; each is wired
(chroma-library/footprint_names.py MARKS_WIRED: read by the engine's people and world code) or retired (MARKS_RETIRED:
never a footprint in the marks stack).

    python3 -B fp_marks.py <tree>          exit 0 when FP3 holds

Release's reading: the marks are the Library's list (earth.MARKS, else the shared folder's build.MARKS, as
tests/check_footprint.py reads them); a mark is read by a rule when it appears quoted in the engine's rules_titles.py or
rules_perks.py (the check's own test). Every unread mark must be in MARKS_WIRED or MARKS_RETIRED, never both; each wired
mark must appear quoted in the engine code outside those two files (so the claim "the engine reads it" holds), and
no name in either list may be missing from the marks list. Plan §3 counts 14 unread marks; another count is printed."""
import glob, os, sys

tree = os.path.abspath(sys.argv[1])
LIB = os.path.join(tree, "chroma-library"); ENG = os.path.join(tree, "chroma-engine", "v22-speedpass")
sys.path.insert(0, LIB); sys.path.append("/mnt/project-files/chroma-library")   # build.py lives only in the shared folder
sys.dont_write_bytecode = True
import earth                                          # noqa: E402
from footprint_names import MARKS_WIRED, MARKS_RETIRED   # noqa: E402
marks = list(earth.MARKS) if isinstance(earth.MARKS, (list, tuple, set)) and earth.MARKS else None
src = "earth.MARKS"
if not marks:
    import build                                      # noqa: E402
    marks = list(build.MARKS); src = f"build.MARKS ({build.__file__})"
rules = "".join(open(os.path.join(ENG, f), encoding="utf-8").read() for f in ("rules_titles.py", "rules_perks.py"))
other = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(ENG, "*.py")))
                if os.path.basename(f) not in ("rules_titles.py", "rules_perks.py"))
read = [m for m in marks if f"'{m}'" in rules or f'"{m}"' in rules]
unread = [m for m in marks if m not in read]
W, Rt = set(MARKS_WIRED), set(MARKS_RETIRED)
left = [m for m in unread if m not in W and m not in Rt]
both = sorted(W & Rt)
unknown = sorted((W | Rt) - set(marks))
not_in_code = [m for m in sorted(W) if f"'{m}'" not in other and f'"{m}"' not in other]
print(f"FP3 on {tree}: {len(marks)} marks ({src}); {len(read)} read by a title or perk rule; {len(unread)} unread "
      f"(plan §3: 14): {len([m for m in unread if m in W])} wired, {len([m for m in unread if m in Rt])} retired")
for lab, xs in (("unread, neither wired nor retired", left), ("in both lists", both), ("named but not a mark", unknown),
                ("wired but not quoted in the engine code", not_in_code)):
    print(f"  {lab}: {', '.join(xs) if xs else 'none'}")
ok = not left and not both and not unknown and not not_in_code
print(f"FP3: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
