import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
ids = sys.argv[3:]
out = []
masks = {}
for m in re.finditer(r'<mask id="([^"]+)".*?</mask>', src, re.S): masks[m.group(1)] = m.group(0)
pats = {m.group(1): m.group(0) for m in re.finditer(r'<pattern id="([^"]+)".*?</pattern>', src, re.S)}
need = set()
for i in ids:
    m = re.search(r'<symbol id="%s".*?</symbol>' % re.escape(i), src, re.S)
    if not m: print("missing", i, file=sys.stderr); continue
    s = m.group(0); out.append(s)
    for r in re.findall(r'url\(#([^)]+)\)', s): need.add(r)
defs = []
for r in sorted(need):
    if r in masks:
        defs.append(masks[r])
        for p in re.findall(r'url\(#([^)]+)\)', masks[r]):
            if p in pats: defs.append(pats[p])
    elif r in pats: defs.append(pats[r])
open(sys.argv[2], "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(defs) + "".join(out) + "</defs></svg>")
print(len(out), "symbols", len(defs), "defs")
