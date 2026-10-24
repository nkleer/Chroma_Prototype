# Sourced by Release's v25 helper scripts (la_ship.sh, rarity_part.sh). Cloud helpers count only when their lives equal
# Release's container's byte for byte (evaluation.md section 5: lives differ by CPU SIMD level), so before any work a
# helper plays four small probes (seeds 41-44, 20 lives x 40 years, the shipped set) and compares them with Release's.
F=/mnt/project-files; H=$F/chroma-release/out/v24/heights; V=$F/chroma-release/out/v25
E25=225679d46e1c1bd254453760c00f40940857a06c   # the Engine's freeze (E): the probes' commit, whatever a job checks
SHA=${SHA:-$E25}; S7=${SHA:0:7}
unset CHROMA_ROOT CHROMA_ENGINE CHROMA_GAME CHROMA_ENGINE_DIR CHROMA_LIBRARY_DIR CHROMA_PACKS_DIR READ_GOALS LIB PACKS PACK_DIR PACK_MOMENTS OUT_DIR
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
CORES=$(env -u OMP_NUM_THREADS nproc)
ME=$(python3 -c "import numpy as np, sys, platform; from numpy._core._multiarray_umath import __cpu_features__ as f; print(sys.version.split()[0], np.__version__, platform.libc_ver()[1], ' '.join(sorted(k for k,v in f.items() if v)))")
setup_tree() {   # $1 = scratch folder: the commit's tree at $1/wt; $2 = the commit (default $SHA)
  local X=$1 R SHA=${2:-$SHA}
  [ "$(git -C $X/wt rev-parse HEAD 2>/dev/null)" = "$SHA" ] && return 0
  R=${REPO:-/home/claude/chroma_prototype}; [ -e $R/.git ] || { R=$X/repo; [ -e $R/.git ] || git clone -q https://github.com/nkleer/Chroma_Prototype.git $R || return 2; }
  git -C $R cat-file -e "$SHA^{commit}" 2>/dev/null || git -C $R fetch -q origin '+refs/heads/feature/v25:refs/remotes/origin/feature/v25' || return 2
  git -C $R worktree remove --force $X/wt 2>/dev/null; rm -rf $X/wt; git -C $R worktree prune
  git -C $R worktree add -q --detach $X/wt "$SHA" || return 2
  [ "$(git -C $X/wt rev-parse HEAD)" = "$SHA" ]
}
ship_px() { (cd $1/chroma-engine/v22-speedpass && python3 -B -c "import json, engine as E; print(json.dumps({**E.SHIP_V25_BATCH, **E.SHIP_V25}, sort_keys=True))"); }
same_machine() {   # $1 = scratch folder with wt/ set up at E; prints one line; 0 when all four probes equal Release's
  local X=$1 s px got want bad=0
  [ "$(git -C $X/wt rev-parse HEAD 2>/dev/null)" = "$E25" ] || { echo "STOP: the probes need E's tree in $X/wt"; return 2; }
  [ "$(md5sum < $H/heights_engine24.py | cut -c1-32)" = c196bfdf055089bfcd453129403da649 ] || { echo "STOP: heights_engine24.py changed"; return 2; }
  cp $H/heights_engine24.py $X/; px=$(ship_px $X/wt) || return 2
  for s in 41 42 43 44; do python3 -B $X/heights_engine24.py $X/wt $s 20 40 $X/probe$s.json "$px" > $X/probe$s.log 2>&1 & done; wait
  for s in 41 42 43 44; do
    got=$(python3 -c "import json, hashlib; d = json.load(open('$X/probe$s.json')); d.pop('secs', None); d.pop('tree', None); print(hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest())" 2>/dev/null)
    want=$(awk -v s=$s '$1 == s {print $2}' $V/probe_ref_${E25:0:7}.txt)
    [ -n "$got" ] && [ "$got" = "$want" ] || bad=$((bad + 1))
  done
  [ $bad = 0 ] && { echo "same machine: 4 of 4 probes equal Release's ($ME)"; return 0; }
  echo "STOP: $bad of 4 probes differ from Release's lives on this machine ($ME)"; return 3
}
probe_here() {   # any job: E's tree in ${TMPDIR:-/tmp}/v25_probe, then the four probes
  local X=${TMPDIR:-/tmp}/v25_probe; mkdir -p $X
  setup_tree $X $E25 || { echo "STOP: no tree for E $E25"; return 2; }
  same_machine $X
}
