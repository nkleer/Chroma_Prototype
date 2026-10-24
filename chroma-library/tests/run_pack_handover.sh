#!/bin/bash
# Pack hand-over (v22 Politics, 2026-10-07; re-pointed 2026-10-08 for the v23 round after the cleanup removed the
# old staging copy): rebuild the staged earth_<pack>.py from chroma-packs/<pack>, check it, stage it if the build
# checks pass, then C-L4 titles and C-L6 reach on the engine copy.
# Usage: [PK=politics] [ST=staging dir] [CAT=catalogue] run_pack_handover.sh <out dir> <engine copy>
set -u
PATHS=${CHROMA_ROOT:-/mnt/project-files}/chroma-env   # folder names: chroma-env/paths.py
pth() { python3 -B -c "import sys; sys.path.insert(0, '$PATHS'); from paths import P; print(P['$1'])"; }
L=$(pth library_live); P=$(pth packs_live); O=${1:?out dir}; ENG=${2:?engine copy}
PK=${PK:-politics}; ST=${ST:-$(pth library_v23)}; CAT=${CAT:-$L/drafts/next4/earth_perks_titles.py}
OTHERS=$(for x in science politics stage; do [ $x != $PK ] && echo -n "$x "; done)
export PYTHONDONTWRITEBYTECODE=1 PACK_DIR=$P
rm -rf "$O"; mkdir -p "$O/build" "$O/lib"
cp $P/$PK/$PK-*.lib "$O/build/"; cp $L/build.py $L/earth_voice.py "$O/build/"
(cd "$O/build" && python3 build.py $PK > "$O/build.out" 2>&1); echo "build exit $?" >> "$O/build.out"
(cd "$O/build" && python3 $L/check.py "$O/build/$PK.py" > "$O/check_politics.out" 2>&1); echo "check exit $?" >> "$O/check_politics.out"
(cd $L/drafts && python3 check_setting.py "$P/$PK" > "$O/setting.out" 2>&1); echo "setting exit $?" >> "$O/setting.out"
cp $ST/earth.py "$CAT" "$O/lib/"; for x in $OTHERS; do cp $ST/earth_$x.py "$O/lib/"; done
cp "$O/build/$PK.py" "$O/lib/earth_$PK.py"
python3 - "$O/lib" > "$O/names.out" 2>&1 <<'PY'
import sys, importlib.util, collections
d = sys.argv[1]; c = collections.Counter()
for f in ("earth", "earth_science", "earth_politics", "earth_stage"):
    s = importlib.util.spec_from_file_location(f, f"{d}/{f}.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    for x in m.SITUATIONS + list(getattr(m, "ECHOES", [])) + list(getattr(m, "EVENTS_READ", [])): c[x["name"]] += 1
dup = [k for k, v in c.items() if v > 1]; print("names", len(c), "duplicates", dup)
PY
(cd "$ENG" && python3 -c "
import sys; sys.dont_write_bytecode=True
import engine as E, batch as B
B.LIB_DIR='$O/lib'
L=B.load_batch('earth', roles='$O/lib/earth_perks_titles.py', packs=['science','politics','stage'])
o=E.run(N=10, years=20, seed=3, lib=L); print('engine load ok', L['S'])" > "$O/load.out" 2>&1); echo "load exit $?" >> "$O/load.out"
md5sum "$O/lib/earth_$PK.py" > "$O/md5.out"
# gate: stage the new build the moment the build checks pass, so its md5 can go out before the title shares run
ok=1
grep -q "^build exit 0" "$O/build.out" && grep -q "no layout problems" "$O/build.out" || ok=0
grep -q "^check exit 0" "$O/check_politics.out" || ok=0
grep -q "^setting exit 0" "$O/setting.out" && grep -q "^setting: no year" "$O/setting.out" || ok=0
grep -q "duplicates \[\]" "$O/names.out" || ok=0
grep -q "^load exit 0" "$O/load.out" && grep -q "engine load ok" "$O/load.out" || ok=0
if [ $ok = 1 ]; then
  cp $ST/earth_$PK.py "$O/staged-before.py"
  cp "$O/lib/earth_$PK.py" $ST/earth_$PK.py
  cmp "$O/lib/earth_$PK.py" $ST/earth_$PK.py && md5sum $ST/earth_$PK.py > "$O/STAGED"
else
  echo "build checks failed" > "$O/CHECKS_FAILED"; exit 1
fi
[ "${STOP_AFTER_STAGE:-0}" = 1 ] && exit 0
cd "$O"
( python3 $L/tests/titles_by_source.py "$O/lib" "$O/titles.json" "$ENG" science,politics,stage > "$O/titles.out" 2>&1; echo "titles exit $?" >> "$O/titles.out" ) &
( python3 $L/tests/reach.py "$O/lib" "$O/reach.json" "$ENG" science,politics,stage > "$O/reach.out" 2>&1; echo "reach exit $?" >> "$O/reach.out" ) &
wait
python3 $L/tests/split_titles.py "$O/titles.json" "$O/lib/earth_perks_titles.py" > "$O/split.out" 2>&1
echo done > "$O/DONE"
