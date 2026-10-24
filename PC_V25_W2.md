# Release's v25 kit, part 3: wave 2 on G' (not for merging)

Copy it over the PC's copy of the part 1 kit (`cp -r <clone>/chroma-release /mnt/project-files/`). Changed: short-v25/run.sh (jobs `pb` and
`nbase`), out/heights/heights_play.py (also records the role events, start_age and yrs_w, for PB; md5 cab6bb27c29c),
out/v24/heights/run.sh (job `steerU`), and main's or Release's newer copies of cloud_lib.sh, la_ship.sh, check_pin.py and
the two fit probes.

    G=96568b08c40728a863ece7ec2ccc398a88be9797   # G': the frozen candidate (65ecdf9 + rarity + golden)
    E=65ecdf9193b9ef9d0045426cb8a78e66f90a09aa   # the Engine's freeze
    NOPROBE=1 SHA=$G REFIT=$E REPO=<checkout> bash /mnt/project-files/chroma-release/short-v25/run.sh <job>

In this order, after wave 1 and LB:
1. hp_aims, hp_aims2 (A1, SK: 48 lives).
2. rollA rollB rollC (rollA reads wave 1's out/roll8_65ecdf9_* folders), needs, st1, hover, foot.
3. f15a f15b f15c f15d, pr30a pr30b pr30c, gameA gameB gameC, fitk, fit12, fp.
4. hp_none, hp_let, hp_reader on G', and the same three on the base e69b3bf (`SHA=e69b3bfefb0934b1b034cd93e384211837f22825`,
   no REFIT); then copy the base's lives into out/heights/play_e69b3bf/, where fp4.py and the A3 judge read them.
5. pb on G', and pb on the played base 7a8cac6 (`SHA=7a8cac6`, no REFIT).
6. nbase on 34721bb (`SHA=34721bb`, no REFIT): needs with no ship hook.
7. hp_oracle, gv24.
8. Once their parts are in: f15m, pr30m, ndm (G' against the PC's 34721bb), fp4.

## Returns (a pc/ branch, as before)

The played lives (out/v24/heights/play_96568b0/, wide_96568b0/, play_7a8cac6/ steerU_*, play_e69b3bf/, with their
ledger/ folders), every report the jobs write (out/roll_96568b0/, out/v24/needs/needs_96568b0_*.txt, st1, hover, fp,
foot, fp4, gv24, out/f15_96568b0/ judge text, push_rare's merge, out/v22checks_*/), the new lines of out/results.jsonl,
each job's console output, and the md5s of the lives.
