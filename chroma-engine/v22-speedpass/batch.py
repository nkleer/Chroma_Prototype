"""Load a Library batch (chroma-library/<world>.py, read only) into the engine's library format.

    from batch import load_batch
    L = load_batch("earth")             # situations + echoes + the engine's "reconsidering a commitment"
    L = load_batch("earth", roles="../../chroma-library/drafts/earth_perks_titles.py")   # with a draft catalogue
    o = engine.run(N, years, seed, lib=L)

The engine owns the reading: engine-side fixes to fields (earth_rules.FIXES) and the conditions for inner moments,
echoes, outside events read through the colors and life-event gates (earth_rules.INNER / ECHO / READ / LIFE).
"""
import copy
import importlib
import importlib.util
import json
import os
import re
import sys
sys.dont_write_bytecode = True     # loading the Library's and the packs' files leaves no __pycache__ in their folders

import numpy as np

import engine as E

LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "chroma-library")
PACK_DIR = os.environ.get("PACK_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "chroma-packs")
# PACK_DIR=<folder>: a frozen copy of chroma-packs for a long fit (calib_v8/pack_fit_all.sh), so edits mid-run cannot mix in
# an act field naming {title}: the title held that brings the person to the moment (engine and explain.title_held resolve it)
TITLE_HELD = -2
MISSED_TITLE = -3   # {missed}: the title of the person's last failed long shot (a second try, packs 08:02)
# drops: kind:<kind> (also takes:, suspends:): every title of that kind held (KIND_ACT - the kind's index in TITLE_KINDS)
KIND_ACT = -10
# content packs (Emren's point 8; card 21:03: approved packs are always on, with no switch at setup). A pack joins this list
# once the Library has built it and Emren has said go; its moments are then the Library's chroma-library/<world>_<pack>.py
PACKS = ["science", "politics", "stage"]   # the ONE GO-LIVE (Emren 10-06 01:32), engine three-pack fit

# the names a condition may use (one value per person, or a world scalar); see run() "batch conditions"
COND_VOCAB = """age age_mod decade_edge round_birthday stage child juvenile young_adult adult mature elder
safety belonging autonomy competence meaning  money time health ties freedom
stress mood satisfaction peace react steady base_mood outlook support wound trouble fortune cload
W U B R G  hW hU hB hR hG (acted ways, ten-year share)  eW eU eB eR eG (ends served, ten-year share)
held_X yrs_X ago_end_X for X in career partner children community faith; yrs_any kids_home retired widowed betrayed
alive_parent alive_sibling alive_friend alive_grandparent alive_child
ago_le ago_commit ago_move ago_death ago_loss ago_win ago_hard_win ago_fail_big ago_breakup ago_retire ago_child ago_job
ago_goal_end ago_hard (years since; 99 = never)
quiet lo_meaning vlo_meaning lo_belong lo_peace hi_stress lo_time lo_auto ok_needs ok_body easing flat_comp (weeks in a row)
fails13 hedon_n bodyhab_n n_moves heavy_risk bind_m n_dream n_passion n_plan regret horizon discipline self_control
harsh unrest prosper era founding (C5: a movement founded in the person's town within the year; true only with c5_faith on)
haunts (the spheres' haunts, phase 2: never true until they are built)
female male attr unease (point 11); trans nonbinary ace intersex partner_same named_gender cross_title role_fit
role_strict accept_trans (N1b)
mk(mark, years=None) mk_ok(mark, years=None) mkn(mark) mk_span(mark) had(situations, years) chance(p)  sa (echo: years since anchor)"""


def _fx(s, keys=("need", "res")):
    """'need:belonging+.15 res:money-.05' or 'belonging+.03' -> (need vector, resource vector)."""
    nv = np.zeros(E.NJ); rv = np.zeros(E.NR)
    for tok in (s or "").split():
        kind, _, body = tok.rpartition(":")
        k = 0
        while k < len(body) and (body[k].isalpha() or body[k] == "_"):
            k += 1
        key, num = body[:k], float(body[k:])
        if (kind == "need" or not kind) and key in E.NIDX:
            nv[E.NIDX[key]] += num
        elif key in E.RIDX:
            rv[E.RIDX[key]] += num
    return nv, rv


def _window(win, mn):
    """Adult readings start at mn; a child version (its window ends by mn) keeps its own window."""
    return tuple(win) if win[1] <= mn else (max(win[0], mn), win[1])


def _code(expr):
    return compile(expr or "True", "<cond>", "eval")


PERK_KINDS = ["skill", "credential", "standing", "bond", "asset"]
TITLE_KINDS = list(E.KNAMES) + ["status"]
WITHOUT = ["law", "approval", "means", "impossible"]
# what a missing requirement makes an option when the act says nothing: a title you do not hold cannot be acted as;
# a missing licence is against the law; a missing asset or skill is a lack of means; missing standing or a bond, of approval
WITHOUT_DEFAULT = dict(title=3, skill=2, credential=0, standing=1, bond=1, asset=2)
ACT_OPS = ("title", "drops", "grants", "takes", "suspends")


def _ways(s):
    v = np.zeros(E.C)
    toks = [c for c in (s or "").split() if c in E.IDX]
    for c in toks:
        v[E.IDX[c]] += 1.0 / len(toks)
    return v


def _names(s):
    return [x.strip() for x in str(s or "").split(";") if x.strip()]


def _lose(r):
    """A rule's ways of losing an item: lose is a condition (its words in lwhy, default "lost it") or a list of
    (condition, words), each loss told in its own words."""
    lz = r.get("lose")
    if not lz:
        return None
    pairs = [(lz, r.get("lwhy", "lost it"))] if isinstance(lz, str) else [(c_, w_) for c_, w_ in lz]
    return [(_code(c_), str(w_)) for c_, w_ in pairs]


def _rule1(nm, r, ID, norm, acc_mv, acc_fs, opt, extend):
    """One title's or perk's rule, compiled (_roles)."""
    bad = [x for x in r.get("after", []) if x not in ID]
    if bad:
        raise ValueError(f"{nm}: 'after' names unknown titles {bad}")
    bad = [x for x in r.get("rungs", []) if x not in ID]
    if bad:
        raise ValueError(f"{nm}: 'rungs' names unknown titles or perks {bad}")
    # a pack's EXTEND: a condition or-ed into the rule (at the rule's own rate), or dict(req, rate): a way in of its own
    more_ = []
    for x_ in (extend or {}).get(nm, []):
        if isinstance(x_, dict):
            more_.append((_code(x_["req"]), float(x_["rate"])))
        else:
            r["req"] = f"({r['req']}) | ({x_})" if r.get("req") else None   # a rule with no condition already lets anyone in
    return dict(req=_code(r.get("req")), rate=r.get("rate"), more=more_, after=[ID[x] for x in r.get("after", [])],
                lose=_lose(r), lrate=r.get("lrate", 0.0), lend=r.get("lend", "left"),
                starts=bool(r.get("starts")), entry=r.get("entry", not r.get("after")), weight=r.get("weight"),
                has_req=bool(r.get("req")),
                rungs=[ID[x] for x in r.get("rungs", [])],   # lower rungs kept on the step (a degree; packs
                # 11:29): counted as steps by the fit report, never dropped or gated like after=
                norm=float(norm.get(nm, 1.0)), acc_move=float(acc_mv.get(nm, 1.0)), acc_first=float(acc_fs.get(nm, 1.0)), grants=[ID[x] for x in r.get("grants", []) if x in ID or x not in opt])


def _roles(cat, R, L, extra=None, extend=None):
    """Titles and perks (chroma-engine/perks-titles-format.md): the world's catalogue, the engine's reading of how each is
    gained and lost (<world>_rules.ROLES), and the act fields on options (title, drops, grants, takes, suspends, requires,
    without; a field ending in _if_fails acts when the act fails)."""
    TT, PP = list(cat.TITLES), list(cat.PERKS)
    items = TT + PP; NT, NP = len(TT), len(PP); NI = NT + NP
    names = [x["name"] for x in items]; ID = {nm: i for i, nm in enumerate(names)}
    rules = {**getattr(R, "ROLES", {}), **(extra or {})}; norm = getattr(R, "ROLE_NORM", {})
    # a route that overfills a title (Library next3 §3: job moves bunched on office clerk, first jobs fell back on cleaner and
    # factory worker): the share of picks by that route that give the title (fitted below 1 by calib_v7/roles_check.py)
    acc_mv = getattr(R, "ROLE_ACC_MOVE", {}); acc_fs = getattr(R, "ROLE_ACC_FIRST", {})
    opt = getattr(R, "ROLES_OPTIONAL", set())            # rules for titles an older catalogue does not have yet
    unknown = [nm for nm in list(rules) + list(extend or {}) if nm not in ID and nm not in opt]
    if unknown:
        raise ValueError(f"rules for titles or perks not in the catalogue: {unknown}")
    G = dict(names=names, ID=ID, NT=NT, NP=NP, NI=NI, say=[x.get("say", x["name"]) for x in items],
             tkind=np.array([TITLE_KINDS.index(x["kind"]) for x in TT]), pkind=np.array([PERK_KINDS.index(x["kind"]) for x in PP]),
             ways=np.array([_ways(x.get("ways")) for x in items]).reshape(NI, E.C),
             ages=np.array([x.get("ages", (0, 110)) for x in items], float).reshape(NI, 2),
             share=np.array([float(x.get("share", 0.1)) for x in items]),
             lasts=np.array([np.inf if x.get("lasts", "life") in ("life", None) else float(x["lasts"]) for x in TT]),
             odds=np.array([float(x.get("odds") or 0.0) for x in PP]),
             half=np.array([0.0 if x.get("skill_half") is None else float(x["skill_half"]) for x in PP]),
             retires=np.array([np.inf if x.get("retires") is None else float(x["retires"]) for x in PP]))
    G["ind"] = (G["ways"] > 0).astype(float)
    # outer world keywords on titles (world-fields.md): sector= on careers; institution= and standing= (W40)
    import world_keys as WK_
    for kw_, voc_ in (("sector", WK_.SECTORS), ("institution", WK_.INST_KINDS)):
        bad_ = [(x["name"], x[kw_]) for x in TT if x.get(kw_) and x[kw_] not in voc_]
        if bad_:
            raise ValueError(f"titles with an unknown {kw_}=: {bad_} (known: {', '.join(voc_)})")
        G[kw_] = np.array([voc_.index(x[kw_]) if x.get(kw_) else -1 for x in TT], int)
    bad_ = [(x["name"], x["standing"]) for x in TT if x.get("standing") is not None and x["standing"] not in (0, 1, 2, 3)]
    if bad_:
        raise ValueError(f"titles with standing= outside 0 to 3: {bad_}")
    G["standing"] = np.array([int(x["standing"]) if x.get("standing") is not None else -1 for x in TT], int)
    # N1b (chroma-identity/for-the-engine.md §3): role=women or role=men on titles the world reserves for one sex
    bad_ = [(x["name"], x["role"]) for x in TT if x.get("role") and x["role"] not in ROLE_TITLE]
    if bad_:
        raise ValueError(f"titles with an unknown role=: {bad_} (known: {', '.join(ROLE_TITLE)})")
    G["role"] = np.array([ROLE_TITLE.index(x["role"]) if x.get("role") else -1 for x in TT], int)
    # profiles: two or three equally valid ways to hold a title, (colors, words); a person holds the one that fits them and
    # may move to another as their colors drift, without it counting as a new title. ways stays the first profile
    prs = [[(_ways(c), str(wd)) for c, wd in (x.get("profiles") or [])] or [(G["ways"][i], "")] for i, x in enumerate(items)]
    MP = max(len(p_) for p_ in prs)
    G["PW"] = np.zeros((NI, MP, E.C)); G["PN"] = np.array([len(p_) for p_ in prs])
    for i, p_ in enumerate(prs):
        for j, (v_, _) in enumerate(p_):
            G["PW"][i, j] = v_
    G["pwords"] = [[wd for _, wd in p_] for p_ in prs]
    # facets: a title that refines another for a while (newlywed of wife or husband); held on top of it, never in its place
    # (the catalogue's field, or the rules' when the nesting is the engine's reading: single parent on mother or father).
    # It can name several titles, as a list or with ";" (a caregiving partner, married or living together): the facet sits
    # on any of them. refines = the first, REFM = all
    def _reflist(v):
        return [] if not v else [str(z).strip() for z in v] if isinstance(v, (list, tuple)) else _names(v)
    G["refines"] = np.full(NI, -1); G["REFM"] = np.zeros((NI, NT), bool)
    for i, x in enumerate(items):
        rf_, rr_ = _reflist(x.get("refines")), _reflist((rules.get(x["name"]) or {}).get("refines"))
        if rf_ and rr_ and set(rf_) != set(rr_):
            raise ValueError(f"{x['name']}: the catalogue refines {rf_!r} but the rules {rr_!r}")
        for r_ in (rf_ or rr_):
            if r_ not in ID or ID[r_] >= NT or i >= NT or ID[r_] == i:
                raise ValueError(f"{x['name']}: refines must name a title, and only a title can refine one ({r_!r})")
            G["REFM"][i, ID[r_]] = True
            if G["refines"][i] < 0:
                G["refines"][i] = ID[r_]
    mn, mr = zip(*[_fx(x.get("meets")) for x in TT]) if NT else ((), ())
    G["meets_need"] = np.array(mn).reshape(NT, E.NJ); G["meets_res"] = np.array(mr).reshape(NT, E.NR)
    G["kindname"] = [x["kind"] for x in items]
    G["without_default"] = np.array([WITHOUT_DEFAULT["title"]] * NT + [WITHOUT_DEFAULT[x["kind"]] for x in PP])
    G["rule"] = []
    for i, nm in enumerate(names):
        G["rule"].append(_rule1(nm, dict(rules.get(nm, {})), ID, norm, acc_mv, acc_fs, opt, extend))
    # item 15, the sphere titles (earth_rules.SPH_TITLE_ROLES): compiled beside the rules, read only with sph_titles on
    G["rule_sph"] = {ID[nm]: _rule1(nm, dict(r_), ID, norm, acc_mv, acc_fs, opt, None)
                     for nm, r_ in getattr(R, "SPH_TITLE_ROLES", {}).items() if nm in ID}
    # act fields
    S, K = L["S"], L["K"]
    G["A_REQ"] = np.full((S, K), -1); G["A_WITHOUT"] = np.full((S, K), -1); G["S_REQ"] = np.full(S, -1)
    G["A_FX"] = {}; G["A_HASFX"] = np.zeros((S, K), bool)
    G["A_AIM"] = np.full((S, K), -1)                      # aims: <title>: choosing it sets a plan on that title (pathways)
    G["S_FX"] = {}; G["S_HASFX"] = np.zeros(S, bool)      # the moment itself gives it, whatever is chosen (title: at its top)
    # Emren's point 6 (2026-10-05): holds: names any of several titles or perks ("a | b", or "a; b"), or every title of a kind
    # ("kind:career"); tenure: lo-hi limits the moment to a holder of such a title for lo to hi years (new, settled, senior)
    G["S_HOLDM"] = np.zeros((S, NI), bool); G["S_HASHOLD"] = np.zeros(S, bool); G["S_TEN"] = np.full((S, 2), np.nan)
    missing = set()

    def look(nm):
        if nm == "{title}":            # the title held that brings the person to this moment (holds: a kind, or any of several)
            return TITLE_HELD
        if nm == "{missed}":           # the title the person's last failed long shot was for
            return MISSED_TITLE
        if nm.startswith("kind:"):     # every title of a kind held (drops: kind:partner)
            if nm[5:].strip() not in TITLE_KINDS:
                raise ValueError(f"{nm}: not a kind of title {TITLE_KINDS}")
            return KIND_ACT - TITLE_KINDS.index(nm[5:].strip())
        if nm not in ID:
            missing.add(nm); return -1
        return ID[nm]

    def first(s_):   # the first title or perk a requires: names (adjectives there are read by _adjectives)
        nm_ = [x for x in _names(str(s_ or "").replace("|", ";")) if x not in E.ADJ_ID and not x.startswith("kind:")]
        return look(nm_[0]) if nm_ else -1
    for si in range(S):
        src = L["src"][si] if si < len(L["src"]) else {}
        hs_ = src.get("holds") or src.get("requires")      # build.py compiles a moment's holds: into requires
        if hs_:
            G["S_REQ"][si] = first(hs_)
        if hs_ and ("|" in str(hs_) or ";" in str(hs_) or "kind:" in str(hs_) or src.get("holds")):
            for x_ in [y.strip() for y in str(hs_).replace("|", ";").split(";") if y.strip()]:
                if x_.startswith("kind:"):
                    kn_ = x_[5:].strip()
                    if kn_ not in TITLE_KINDS:
                        raise ValueError(f"{L['names'][si]}: holds: kind:{kn_} is not a kind of title {TITLE_KINDS}")
                    # a facet (senior, newlywed) is not a new title of the kind: it neither opens nor resets the moment
                    G["S_HOLDM"][si, [i for i in range(NT) if G["kindname"][i] == kn_ and G["refines"][i] < 0]] = True
                elif x_ not in E.ADJ_ID:
                    j_ = look(x_)
                    if j_ >= 0:
                        G["S_HOLDM"][si, j_] = True
            G["S_HASHOLD"][si] = G["S_HOLDM"][si].any()
        elif G["S_REQ"][si] >= 0:
            G["S_HOLDM"][si, G["S_REQ"][si]] = True; G["S_HASHOLD"][si] = True
        if src.get("tenure") is not None:
            tv_ = src["tenure"]
            tv_ = [float(x) for x in str(tv_).replace(" ", "").split("-") if x] if isinstance(tv_, str) else \
                [float(tv_)] * 2 if isinstance(tv_, (int, float)) else [float(x) for x in tv_]
            if not G["S_HASHOLD"][si]:
                raise ValueError(f"{L['names'][si]}: tenure: needs holds: (the title whose years it counts)")
            G["S_TEN"][si] = (tv_[0], tv_[-1] if len(tv_) > 1 else np.inf)
        sfx = [(op, look(nm), float(src.get("for_years", 1.0))) for op in ACT_OPS for nm in _names(src.get(op))]
        if any(j <= KIND_ACT and op in ("title", "grants") for op, j, _ in sfx):
            raise ValueError(f"{L['names'][si]}: a kind can be dropped, not given")
        if sfx and all(j >= 0 or j in (TITLE_HELD, MISSED_TITLE) or j <= KIND_ACT for _, j, _ in sfx):
            G["S_FX"][si] = sfx; G["S_HASFX"][si] = True
        for ki, nt in enumerate(L["notes"][si]):
            if not nt:
                continue
            if nt.get("requires") and first(nt["requires"]) >= 0:
                G["A_REQ"][si, ki] = first(nt["requires"])
                if nt.get("without"):
                    G["A_WITHOUT"][si, ki] = WITHOUT.index(str(nt["without"]).split(":")[0].strip())
            if nt.get("aims"):
                j_ = look(str(nt["aims"]).strip())
                if j_ >= NT:
                    raise ValueError(f"{L['names'][si]}: aims: must name a title ({nt['aims']!r} is a perk)")
                G["A_AIM"][si, ki] = j_
            fx = dict(ok=[], fail=[])
            for op in ACT_OPS:
                for key, when in ((op, "ok"), (op + "_if_fails", "fail")):
                    for nm in _names(nt.get(key)):
                        j = look(nm)
                        if j == TITLE_HELD and not G["S_HASHOLD"][si]:
                            raise ValueError(f"{L['names'][si]}: {key}: {{title}} needs holds: on the moment")
                        if j <= KIND_ACT and op in ("title", "grants"):
                            raise ValueError(f"{L['names'][si]}: {key}: {nm} - a kind can be dropped, not given")
                        if j >= 0 or j in (TITLE_HELD, MISSED_TITLE) or j <= KIND_ACT:
                            fx[when].append((op, j, float(nt.get("for_years", 1.0))))
            if fx["ok"] or fx["fail"]:
                G["A_FX"][(si, ki)] = fx; G["A_HASFX"][si, ki] = True
    if missing:
        raise ValueError(f"act fields name titles or perks not in the catalogue: {sorted(missing)}")
    # doors: the moments with a way into each title (an option that gives it, or the moment itself), for plans aimed at it
    G["DOORS"] = np.zeros((NI, S), bool)
    for (si, ki), fx in G["A_FX"].items():
        for op, j, _ in fx["ok"]:
            if op in ("title", "grants") and j >= 0:
                G["DOORS"][j, si] = True
    for si, sfx in G["S_FX"].items():
        for op, j, _ in sfx:
            if op in ("title", "grants") and j >= 0:
                G["DOORS"][j, si] = True
    return G


def _adjectives(L):
    """v7 adjectives (engine.ADJECTIVES) named in an option's or a situation's requires: (with or without titles and
    perks, and with or without a catalogue): the first adjective named there, and the option's without: if given."""
    S, K = L["S"], L["K"]
    L["ADJ_REQ"] = np.full((S, K), -1); L["ADJ_WOUT"] = np.full((S, K), -1); L["ADJ_SREQ"] = np.full(S, -1)
    for si in range(S):
        src = L["src"][si] if si < len(L["src"]) else {}
        aj = [x for x in _names(str(src.get("requires") or src.get("holds") or "").replace("|", ";")) if x in E.ADJ_ID]
        if aj:
            L["ADJ_SREQ"][si] = E.ADJ_ID[aj[0]]
        for ki, nt in enumerate(L["notes"][si]):
            aj = [x for x in _names((nt or {}).get("requires")) if x in E.ADJ_ID]
            if aj:
                L["ADJ_REQ"][si, ki] = E.ADJ_ID[aj[0]]
                if nt.get("without"):
                    L["ADJ_WOUT"][si, ki] = WITHOUT.index(str(nt["without"]).split(":")[0].strip())
    L["ADJ_ANY"] = bool((L["ADJ_REQ"] >= 0).any() or (L["ADJ_SREQ"] >= 0).any())


def _module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _packs(world, packs, pack_moments, R):
    """Content packs (chroma-packs/<pack>/, the pathways and packs thread's format, for-the-engine.md): the pack's catalogue
    (catalogue.py TITLES and PERKS), the shared core (core/reach.py, then every other core/*.py: TITLES and PERKS), the rules (roles.py ROLES_<PACK>, ROLES_REACH),
    the earned-odds lists (helps.py HELPS_<PACK>, HELPS_PERK_<PACK>, WINDOWS_<PACK>, LIFT_<PACK>), its moments (the Library's compiled <world>_<pack>.py, or
    a path in pack_moments for a test) and the engine's own conditions for its echoes, inner and read moments
    (<world>_rules.PACK_RULES[<pack>])."""
    out = dict(sits=[], reads=[], titles=[], perks=[], rules={}, helps={}, windows={}, lift={}, extend={}, target={},
               cond=dict(INNER={}, ECHO={}, LIFE={}, READ={}), names=list(packs))
    if not packs:
        return out
    core_ = os.path.join(PACK_DIR, "core")   # shared by every pack: reach.py first, then any other core/*.py (longshot.py)
    for f_ in sorted(os.listdir(core_), key=lambda x: (x != "reach.py", x)) if os.path.isdir(core_) else []:
        if f_.endswith(".py") and not f_.startswith("_"):
            cm_ = _module(os.path.join(core_, f_), "chroma_pack_reach" if f_ == "reach.py" else f"chroma_pack_core_{f_[:-3]}")
            out["titles"] += list(getattr(cm_, "TITLES", [])); out["perks"] += list(getattr(cm_, "PERKS", []))
            out["rules"].update(getattr(cm_, "ROLES", {}))   # e.g. dict(rate=0): only ever through an act, never "in time"
    for pk in packs:
        d_ = os.path.join(PACK_DIR, pk); up_ = pk.upper()
        if not os.path.isdir(d_):
            raise ValueError(f"no content pack {pk!r} in {os.path.abspath(PACK_DIR)}")
        cat = _module(os.path.join(d_, "catalogue.py"), f"chroma_pack_{pk}_catalogue")
        out["titles"] += list(cat.TITLES); out["perks"] += list(getattr(cat, "PERKS", []))
        rl = _module(os.path.join(d_, "roles.py"), f"chroma_pack_{pk}_roles")
        out["rules"].update(getattr(rl, f"ROLES_{up_}", {})); out["rules"].update(getattr(rl, "ROLES_REACH", {}))
        out["target"].update(getattr(rl, f"TARGET_{up_}", {}))     # fit targets: multiples of the catalogue share
        if FLOORS:   # titles a pack fits only with the floors on (item 16; Packs PR #33)
            out["target"].update(getattr(rl, f"TARGET_{up_}_FLOORS", {}))
        for nm_, x_ in getattr(rl, f"EXTEND_{up_}", {}).items():   # more ways into a rule the pack does not own
            out["extend"].setdefault(nm_, []).append(x_)
        if os.path.exists(os.path.join(d_, "helps.py")):
            hp = _module(os.path.join(d_, "helps.py"), f"chroma_pack_{pk}_helps")
            out["helps"].update(getattr(hp, f"HELPS_{up_}", {})); out["windows"].update(getattr(hp, f"WINDOWS_{up_}", {}))
            out["helps"].update(getattr(hp, f"HELPS_PERK_{up_}", {}))   # a standing perk an act grants (packs 03:04: the lead)
            out["lift"].update(getattr(hp, f"LIFT_{up_}", {}))
        mp_ = (pack_moments or {}).get(pk) or os.path.join(LIB_DIR, f"{world}_{pk}.py")
        if os.path.exists(mp_):
            M_ = _module(mp_, f"chroma_pack_{pk}_moments")
            out["sits"] += [copy.deepcopy(x) for x in list(M_.SITUATIONS) + list(getattr(M_, "ECHOES", []))]
            out["reads"] += list(getattr(M_, "EVENTS_READ", []))
        for k_, v_ in (getattr(R, "PACK_RULES", {}).get(pk) or {}).items():
            if k_ == "ROLES":   # the engine's own reading of a pack rule, over the pack's proposal
                for nm_, r_ in v_.items():
                    out["rules"][nm_] = {**out["rules"].get(nm_, {}), **r_}
            else:
                out["cond"][k_].update(v_)
    if os.environ.get("PACK_TARGET"):   # a test: {title or perk: multiplier or tier word}, over the packs' TARGET_<PACK>
        out["target"].update(json.loads(os.environ["PACK_TARGET"]))
    return out


def load_batch(world="earth", symmetric=False, roles=None, packs=None, pack_moments=None, setting="earth"):
    """packs: the content packs on top of the base (default PACKS, the approved ones); pack_moments: {pack: path of a
    compiled moments file} for a pack the Library has not built into chroma-library/ yet (tests). setting: the world the
    life is played in (earth, tribal, magic: the game's presets); a moment with only: <another world> is left out."""
    sys.path.insert(0, os.path.abspath(LIB_DIR))
    sys.modules.pop(world, None)                          # always read the batch from LIB_DIR as it is now
    try:
        B = importlib.import_module(world)
    finally:
        sys.path.pop(0)
    R = importlib.import_module(f"{world}_rules")
    PK = _packs(world, list(PACKS if packs is None else packs), pack_moments, R)
    INNER_ = {**R.INNER, **PK["cond"]["INNER"]}; ECHO_ = {**R.ECHO, **PK["cond"]["ECHO"]}
    LIFE_ = {**R.LIFE, **PK["cond"]["LIFE"]}; READ_ = {**R.READ, **PK["cond"]["READ"]}
    sits = [copy.deepcopy(s) for s in list(B.SITUATIONS) + list(getattr(B, "ECHOES", []))]
    base_names = {s["name"] for s in sits}
    clash = [s["name"] for s in PK["sits"] if s["name"] in base_names]
    if clash:
        raise ValueError(f"pack moments with the name of a base moment: {clash}")
    sits += PK["sits"]
    sits = [x for x in sits if not x.get("only") or setting in [w_.strip() for w_ in str(x["only"]).replace(",", " ").split()]]
    if not SPH_MOMENTS:   # the spheres' moments among a haunt's regulars (haunt:) or a rung's holders (ladder:) wait for
        sits = [x for x in sits if not x.get("haunt") and not x.get("ladder")]   # phases 2 and 4 (item 15)
    if not FAR_MOMENTS:   # far_ties' moments (cast_want: far_hard, far_good, far_mixed) wait for v22.3's refit (item 18)
        sits = [x for x in sits if not str(x.get("cast_want") or "").strip().startswith("far_")]
    if not LEAD_MOMENTS:   # lead_ways' moments (cast_want: lead_take, lead_crisis, lead_fall, lead_routine, lead_hand)
        sits = [x for x in sits if not str(x.get("cast_want") or "").strip().startswith("lead_")]   # wait for v22.3's refit (S7)
    key = lambda s: s.get("variant_of") or s["name"]      # a child version is its original for every rule keyed by name
    for s in sits:
        s.update(R.FIXES.get(key(s), {}))
        if s.get("tier") == "echo":                       # echoes come only through their anchor (no everyday draw)
            s.setdefault("rate", 0.3)
    for s in sits:   # adult inner moments are written in adult words ("patent it", "your income"), so they start at 12;
        mn_ = getattr(R, "INNER_MIN_AGE", 0)   # the Library's child versions (window ending by then) keep their own
        if s.get("tier") == "inner" and s["age"][1] > mn_:
            s["age"] = (max(s["age"][0], mn_), s["age"][1])
    for s in sits:   # drivers decide who, not how many (earth_rules.DRV_NORM; a child version's own, else its original's)
        dn_ = getattr(R, "DRV_NORM", {}); dk_ = s["name"] if dn_.get(s["name"], 0) > 0 else key(s)
        if s.get("per_year") and dn_.get(dk_, 0) > 0:
            s["per_year"] = tuple(x / dn_[dk_] for x in s["per_year"])
    recon = [s for s in E.SITUATIONS if s["name"] == "reconsidering a commitment"]
    L = E.compile_library(symmetric, sits + recon)
    names = L["names"]
    # conditions per situation: kind 1 inner, 2 echo, 3 life-event gate
    cond = []
    # variant_of: a child version of an event is the same event for once, kills, gates and names (only its window and
    # options differ; the windows must not overlap)
    L["ROOT"] = np.arange(L["S"]); L["FAMILY"] = {}
    for si, nm in enumerate(names):
        vo = L["src"][si].get("variant_of")
        if vo:
            if vo not in names:
                raise ValueError(f"{nm}: variant_of names an unknown situation {vo!r}")
            L["ROOT"][si] = names.index(vo)
            L["FAMILY"].setdefault(vo, [names.index(vo)]).append(si)
    for si, nm0 in enumerate(names):
        src = L["src"][si]
        tier = src.get("tier"); nm = src.get("variant_of") or nm0
        if tier == "inner" and nm in INNER_:
            c = INNER_[nm]; kind = 1
        elif tier == "echo" and nm in ECHO_:
            c = ECHO_[nm]; kind = 2
        elif nm in LIFE_:
            c = LIFE_[nm]; kind = 3
        else:
            continue
        dl = tuple(src.get("delay_years", (0, 0)))
        cond.append(dict(s=si, kind=kind, name=nm0, req=_code(c.get("req")), more=[_code(x) for x in c.get("more", [])],
                         less=[_code(x) for x in c.get("less", [])], anchor=_code(c["anchor"]) if "anchor" in c else None,
                         delay=dl, rtxt=str(c.get("req") or "")))
    missing = [s["name"] for s in sits if s.get("tier") in ("inner", "echo") and key(s) not in INNER_ and key(s) not in ECHO_
               and not s.get("threshold")]          # a season's moments come through their season, not a condition
    if missing:
        raise ValueError(f"no engine conditions for: {missing}")
    L["COND"] = cond
    L["ID_GATE"] = np.zeros((L["S"], len(ID_GATE_RE)), bool)
    for c_ in cond:
        L["ID_GATE"][c_["s"]] = [bool(r_.search(c_["rtxt"])) for r_ in ID_GATE_RE]
    # N1b: the adult intimacy moments (chroma-library/<world>-intimacy.lib), which come less often to an asexual person
    ip_ = os.path.join(LIB_DIR, f"{world}-intimacy.lib")
    inm_ = set(re.findall(r"^== (.+?)\s*$", open(ip_).read(), re.M)) if os.path.exists(ip_) else set()
    L["INTIM"] = np.array([si for si, nm_ in enumerate(names) if nm_ in inm_ or L["src"][si].get("variant_of") in inm_], int)
    L["ECHO"] = np.array([s.get("tier") == "echo" for s in L["src"]])
    L["INNER"] = np.array([s.get("tier") == "inner" for s in L["src"]])
    # outside events read through the person's colors
    evr = []
    for ev in list(getattr(B, "EVENTS_READ", [])) + PK["reads"]:
        if ev.get("only") and setting not in str(ev["only"]).replace(",", " ").split():
            continue
        c = READ_.get(ev["name"], {})
        bn, br = _fx(ev.get("base"))
        rd = ev["readings"]
        tm = ev.get("timing", {})
        evr.append(dict(name=ev["name"], source=ev.get("source"), tone=ev.get("tone"), base_need=bn, base_res=br,
                        lens=np.array([E.parse(r[1]) / max(E.parse(r[1]).sum(), 1e-9) for r in rd]),
                        impact=np.array([float(r[2]) for r in rd]),
                        also=[_fx(r[3]) for r in rd], want=np.array([E.IDX[r[4]] for r in rd]),
                        labels=[r[0] for r in rd], say=[r[5] if len(r) > 5 else "" for r in rd],
                        window=_window(tm.get("window", (0, 200)), getattr(R, "READ_MIN_AGE", 0)),
                        gap=tuple(tm.get("gap_years", (1.0, 5.0))),
                        req=_code(c.get("req")), more=[_code(x) for x in c.get("more", [])],
                        less=[_code(x) for x in c.get("less", [])]))
    L["EVR"] = evr
    L["REJOB"] = names.index(R.REJOB) if getattr(R, "REJOB", None) in names else -1
    L["PREMISE_TECH"] = dict(getattr(R, "PREMISE_TECH", {})); L["CAST_WANT"] = dict(getattr(R, "CAST_WANT", {}))
    L["world"] = world
    # v10: the Library's dreams (chroma-library/dreams.py, final 10-06 22:19 UTC): the sparks of this setting (earth, tribal,
    # magic) in place of library.py's seed DREAM_TRIGGERS, and the concrete dreams of this setting a new dream is named by
    dp_ = os.path.join(LIB_DIR, "dreams.py")
    if os.path.exists(dp_):
        D_ = _module(dp_, "dreams")
        if setting in D_.DREAM_TRIGGERS:
            L["DREAM_TRIGGERS"] = list(D_.DREAM_TRIGGERS[setting])
        L["DREAMS"] = [d_ for d_ in D_.DREAMS if setting in d_["worlds"].split()]
    L["SETTING"] = setting
    L["VOICE"] = getattr(B, "VOICE", {})      # v7: the character's inner voice and the world's lessons (explain.py keys)
    L["LESSONS"] = getattr(B, "LESSONS", {})
    L["HEART_WHY"] = getattr(B, "HEART_WHY", {})   # the Library's own why-phrases (first person), over explain.py's
    L["HEAD_WHY"] = getattr(B, "HEAD_WHY", {})
    # titles and perks: chroma-library/<world>_perks_titles.py, or a catalogue file given as roles= (a draft, for tests)
    path = roles or os.path.join(LIB_DIR, f"{world}_perks_titles.py")
    if roles is not False and os.path.exists(path):
        spec = importlib.util.spec_from_file_location(f"{world}_perks_titles", path)
        cat = importlib.util.module_from_spec(spec); spec.loader.exec_module(cat)
        if PK["names"]:   # a pack's titles and perks join the base catalogue, its rules the engine's
            have = {x["name"] for x in list(cat.TITLES) + list(cat.PERKS)}
            dup = [x["name"] for x in PK["titles"] + PK["perks"] if x["name"] in have]
            if dup:
                raise ValueError(f"pack titles or perks with the name of a base one: {dup}")
            cat = type("Catalogue", (), dict(TITLES=list(cat.TITLES) + PK["titles"], PERKS=list(cat.PERKS) + PK["perks"]))
        L["ROLES"] = _roles(cat, R, L, extra=PK["rules"], extend=PK["extend"])
        _earned(L, PK)
        _targets(L, PK, R)
    L["PACKS"] = PK["names"]
    _adjectives(L)
    _chance(L, R)
    _world_fields(L)
    return L


SLOT_RE = re.compile(r"\{([a-z]+)\}")
ROLE_VALS = ["women", "men", "keep", "cross"]   # N1b option field role:
ROLE_TITLE = ["women", "men"]                   # N1b title keyword role=
# N1b: which identity trait a moment's engine condition reads (gender, attraction, asexual, intersex): the week a moment
# gated on a trait first comes is the week the game may show that trait (found_*), and a came out mark in a moment
# gated on one trait only tells that trait
ID_GATE_RE = [re.compile(r"\b(unease|trans|nonbinary)\b"), re.compile(r"\battr\b"), re.compile(r"\bace\b"),
              re.compile(r"\bintersex\b")]
TOY_INFER = {"health": "winter", "loss": "winter", "love": "summer", "travel": "summer"}   # world-fields.md: mild tilts


def _world_fields(L):
    """The outer world's Library fields (chroma-engine/world-fields.md): moment fields time_of_year, holy, who,
    cast_want, group, where, at; option fields law, norm, tech, lever, pushes. Parsed into arrays the engine reads when
    the world is on; with none of them written, every array is empty and nothing changes. A value outside its list
    stops the load, naming the moment, the option and the value (these fields are new, so the check is strict)."""
    import world_keys as WK
    S, K = L["S"], L["K"]

    def vals(v):
        return [x.strip() for x in str(v).replace(";", ",").split(",") if x.strip()]

    def one(v, vocab, where_):
        out = []
        for x in vals(v):
            if x not in vocab:
                raise ValueError(f"{where_}: unknown value {x!r} (known: {', '.join(vocab)})")
            out.append(vocab.index(x))
        return out
    toy = np.zeros((S, 4)); toy_set = np.zeros(S, bool); holy = np.full(S, -1); want = np.full(S, -1); grp = np.full(S, -1)
    at = np.full(S, -1); where = np.zeros((S, len(WK.FEATURES)), bool); who = [[] for _ in range(S)]
    touch = np.full(S, -1)   # far_ties (item 18): what the far event touched (work, money, home, health, safety, standing)
    lway = np.full(S, -1)    # lead_ways (S7, chroma-ideas/social-mechanics.md): a crisis or fall moment's way (lead_way:)
    for si, src in enumerate(L["src"][:S]):
        nm = f"moment {src.get('name', si)!r}"
        if src.get("time_of_year"):
            toy[si, one(src["time_of_year"], WK.TIME_OF_YEAR, nm)] = 1.0; toy_set[si] = True
        else:   # inferred, gently: winter for illness and loss, summer for love and travel (spec-1 §1)
            for w_ in vals(src.get("life", "")):
                if w_ in TOY_INFER:
                    toy[si, WK.TIME_OF_YEAR.index(TOY_INFER[w_])] = 0.25
        if src.get("holy"):
            holy[si] = one(src["holy"], WK.HOLY_KEYS, nm)[0]
        if src.get("cast_want"):
            want[si] = one(src["cast_want"], WK.CAST_WANTS, nm)[0]
        elif (L.get("CAST_WANT") or {}).get(src.get("variant_of") or src.get("name")):   # earth_rules.CAST_WANT, by name
            want[si] = one(L["CAST_WANT"][src.get("variant_of") or src.get("name")], WK.CAST_WANTS, nm)[0]
        if src.get("touch"):
            touch[si] = one(src["touch"], WK.TOUCHES, nm)[0]
        if src.get("lead_way"):   # lead_ways (S7): the way a crisis or fall moment belongs to (rules .. custom)
            lway[si] = one(src["lead_way"], WK.LEAD_WAYS, nm)[0]
        if src.get("group"):
            grp[si] = one(src["group"], WK.GROUP_KINDS, nm)[0]
        if src.get("at"):
            at[si] = one(src["at"], WK.INST_KINDS, nm)[0]
        if src.get("where"):
            where[si, one(src["where"], WK.FEATURES, nm)] = True
        if src.get("who"):
            who[si] = [WK.WHO_SLOTS[i_] for i_ in one(src["who"], WK.WHO_SLOTS, nm)]
        else:   # inferred: the slots the text already names ({friend}, {parent}...), then slot words in roles:
            txt = " ".join(str(v) for k_, v in src.items() if k_ in ("worlds", "scenes", "outcomes"))
            seen = [x for x in SLOT_RE.findall(txt) if x in WK.WHO_SLOTS]
            seen += [x for x in vals(src.get("roles", "")) if x in WK.WHO_SLOTS]
            who[si] = list(dict.fromkeys(seen))
    law = np.full((S, K), -1); norm = np.full((S, K), -1); tech = np.full((S, K), -1); lever = np.full((S, K), -1)
    law_neg = np.zeros((S, K), bool); norm_neg = np.zeros((S, K), bool)   # a leading minus: the other way round
    push = np.full((S, K), -1); push_sub = {}; role = np.full((S, K), -1)
    olead = np.full((S, K), -1); ofall = np.full((S, K), -1); ohand = np.full((S, K), -1)   # lead_ways (S7): lead:, fall:, hand:
    for si in range(S):
        for ki, nt in enumerate(L["notes"][si]):
            if not nt:
                continue
            nm = f"moment {L['src'][si].get('name', si)!r}, option {ki + 1}"
            if nt.get("law"):   # a leading minus closes the option the other way round (v23 W38: -conscription)
                lv_ = str(nt["law"]).strip(); law_neg[si, ki] = lv_.startswith("-")
                law[si, ki] = one(lv_.lstrip("- "), WK.LAW_KEYS_ALL, nm)[0]
            if nt.get("norm"):
                nv_ = str(nt["norm"]).strip(); norm_neg[si, ki] = nv_.startswith("-")
                norm[si, ki] = one(nv_.lstrip("- "), WK.NORM_KEYS_ALL, nm)[0]
            if nt.get("tech"):
                tech[si, ki] = one(nt["tech"], WK.TECH_KEYS, nm)[0]
            if nt.get("role"):   # N1b: women, men (an act the world reserves for that sex), keep or cross (the scene's role)
                role[si, ki] = one(nt["role"], ROLE_VALS, nm)[0]
                if norm[si, ki] == WK.NORM_KEYS.index("role crossing"):
                    raise ValueError(f"{nm}: role: and norm: role crossing together (approval would close it twice; keep role:)")
            if nt.get("lever"):
                lever[si, ki] = one(nt["lever"], WK.LEVERS, nm)[0]
            if nt.get("lead"):   # lead_ways (S7): the way an option leads by (the post takes it, or keeps it)
                olead[si, ki] = one(nt["lead"], WK.LEAD_WAYS, nm)[0]
            if nt.get("fall"):   # lead_ways: a fall moment's answer (go, fight, again)
                ofall[si, ki] = one(nt["fall"], WK.FALL_KEYS, nm)[0]
            if nt.get("hand"):   # lead_ways: a hand-over moment's answer (chosen, open, stay)
                ohand[si, ki] = one(nt["hand"], WK.HAND_KEYS, nm)[0]
            if nt.get("pushes"):
                d_, *sub = str(nt["pushes"]).split(None, 1)
                push[si, ki] = one(d_, WK.DOMAINS, nm)[0]
                if sub:   # a group kind, an institution kind or a who slot, by the domain
                    voc_ = {"group": WK.GROUP_KINDS, "institution": WK.INST_KINDS, "close": WK.WHO_SLOTS}.get(d_.strip())
                    if voc_ is None or sub[0].strip() not in voc_:
                        raise ValueError(f"{nm}: pushes {nt['pushes']!r}: a sub-kind only follows group, institution or close, "
                                         f"from its own list")
                    push_sub[(si, ki)] = sub[0].strip()
    # the spheres (item 15; world-fields.md "New Library fields"): a moment's sphere, haunt kind and rung; an option's
    # face (sphere and colour; a pair face keeps its sphere and both colours). Strict: an unknown value fails loudly
    def sph_val(v, where_):
        x = str(v).strip()
        sp_, _, f_ = x.partition(".")
        if sp_ not in WK.SPHERES or (f_ and not (len(f_) in (1, 2) and all(c_ in "WUBRG" for c_ in f_) and len(set(f_)) == len(f_))):
            raise ValueError(f"{where_}: unknown sphere or face {x!r} (a sphere of {', '.join(WK.SPHERES)}, then .W .. .G or a pair)")
        return WK.SPHERES.index(sp_), ("WUBRG".index(f_) if len(f_) == 1 else -1), f_
    msph = np.full(S, -1); haunt = np.full(S, -1); ladder = np.full(S, -1)
    osph = np.full((S, K), -1); ocol = np.full((S, K), -1); hpick = np.zeros(S, bool)
    sphev = np.full(S, -1)      # a moment a sphere event brings (phase 3): the event's index in sphere_data.EV
    import sphere_data as SD_
    ev_key = {e_["key"]: i_ for i_, e_ in enumerate(SD_.EV)}
    for si, src in enumerate(L["src"][:S]):
        nm = f"moment {src.get('name', si)!r}"
        if src.get("sphere"):
            msph[si] = sph_val(src["sphere"], nm)[0]
        if src.get("haunt"):
            haunt[si] = one(src["haunt"], WK.HAUNT_KINDS, nm)[0]
        if src.get("ladder"):
            ladder[si] = one(src["ladder"], WK.LADDER, nm)[0]
        if src.get("sphere_event"):
            k_ = str(src["sphere_event"]).strip()
            if k_ not in ev_key:
                raise ValueError(f"{nm}: unknown sphere_event {k_!r} (an event key of the nine sphere files)")
            sphev[si] = ev_key[k_]
        for ki, nt in enumerate(L["notes"][si] if si < len(L["notes"]) else []):
            if nt and nt.get("sphere") and ki < K:
                osph[si, ki], ocol[si, ki], _ = sph_val(nt["sphere"], f"{nm}, option {ki + 1}")
    for c_ in L.get("COND", []):   # the haunt choices: inner moments gated on the word haunts (the engine applies the pick)
        if re.search(r"\bhaunts\b", c_.get("rtxt", "")):
            hpick[c_["s"]] = True
    prem = np.full(S, -1)   # W38: a moment that needs a technology to make sense (earth_rules.PREMISE_TECH, by name)
    for nm_, k_ in L.get("PREMISE_TECH", {}).items():
        if k_ not in WK.TECH_KEYS:
            raise ValueError(f"PREMISE_TECH {nm_!r}: unknown technology {k_!r}")
        for si in range(S):
            if L["names"][si] == nm_ or L["src"][si].get("variant_of") == nm_:
                prem[si] = WK.TECH_KEYS.index(k_)
    L.update(W_SPHERE=msph, W_HAUNT=haunt, W_LADDER=ladder, W_OSPH=osph, W_OCOL=ocol, W_HPICK=hpick, W_SPHEV=sphev)
    L.update(W_PREMISE=prem, W_TOY=toy, W_TOY_SET=toy_set, W_HOLY=holy, W_WANT=want, W_TOUCH=touch, W_GROUP=grp, W_AT=at, W_WHERE=where, W_WHO=who,
             W_LAW=law, W_NORM=norm, W_LAW_NEG=law_neg, W_NORM_NEG=norm_neg, W_TECH=tech, W_LEVER=lever, W_PUSH=push, W_PUSH_SUB=push_sub, ROLE_OPT=role)
    L.update(W_LEAD_WAY=lway, W_LEAD=olead, W_FALL=ofall, W_HAND=ohand)   # lead_ways (S7)


FAR_MOMENTS = False   # item 18: moments with cast_want: far_hard, far_good or far_mixed join the batch at v22.3's refit
LEAD_MOMENTS = False  # S7: moments with cast_want: lead_* (lead_ways) join the batch at v22.3's refit
SPH_MOMENTS = False   # item 15: moments with haunt: or ladder: join the batch once the spheres' haunts and rungs are built
FLOORS = False      # item 16: the floors for rare titles and perks (earth_rules.BUDGET_FLOORS); off until the v22.3 refit
TARGET_CAP = 0.25   # a multiplied target never asks for more than about 1 life in 4 (common community and entry titles)


TIERS = ("career", "summit", "community")   # TARGET_<PACK> may name a title's tier in place of a multiplier (engine 08:25)


def tier_lift(R, packs):
    """The fitted lift on the odds of acts that take a pack title of each tier (calib_v8/tier_fit.py), for this set of
    packs: earth_rules.TIER_LIFT[",".join(sorted(packs))], or the env TIER_LIFT (JSON, for the fit itself).
    {"career": logit lift, "summit": logit lift, "split": {summit title: extra logit lift}}."""
    if os.environ.get("TIER_LIFT"):
        return json.loads(os.environ["TIER_LIFT"])
    return dict(getattr(R, "TIER_LIFT", {}).get(",".join(sorted(packs)), {}))


def _targets(L, PK, R=None):
    """Big lives come more often than real shares (Emren 05:18, her "About 10x" card, packs thread 05:21), within one
    budget for all packs together (Emren, pack ideas thread, 08:14 relay): about 1 life in 3 holds a big career and about
    1 in 20 reaches a summit. TARGET_<PACK> in a pack's roles.py gives {title or perk: multiplier, or a tier word}:
    - a number: the fit aims at min(multiplier x share, TARGET_CAP), never below the share itself;
    - "career": one multiplier for all the loaded packs' career titles, the budget over their real share of lives
      (1 - the product of 1 - share), never below 1;
    - "summit": the summit budget split by the square root of each summit's real share (the rarest are seen, the order
      holds; engine 08:25), at least BUDGET["summit_floor"] each, never below the share;
    - "community": BUDGET["community"] times the share, capped at TARGET_CAP.
    The catalogue keeps real shares. Careers and summits reach the budget through one lift per tier (tier_lift, fitted by
    calib_v8/tier_fit.py). A tier under budget at the written rates is raised through who enters it (entry and move
    weights, exp(lift)) and, at most by exp(BUDGET["rung_cap"]), through yearly rates (Emren 09:18: steps keep their
    pace); ROLE_NORM does not touch them. The odds of an act that gives one rise with the lift by at most
    BUDGET["act_cap"] in logit (Emren 14:41: "Keep odds higher than real, but not super unrealistically"; .7 about
    doubles the odds: a written 50% wins about 2 in 3, 12% about 1 in 5), folded into the shown chance (_chance); the
    chance written on the roads is the real one (Emren 07:14: about 10% bare, 30-40% with stats and context). A tier
    over budget is lowered on both: background
    rates and the odds of every act that gives one, folded into the shown chance (_chance). Numbered and community items
    keep ROLE_NORM (calib_v7/roles_check.py).
    L["ROLES"]: TARGET (the fit target per item, the share where nothing is given), TIER (0 none, 1 career, 2 summit,
    3 community), BUDGET, TIER_LIFT, A_TIER (S x K: the career or summit an option's act gives, -1 for none)."""
    G = L["ROLES"]; G["TARGET"] = np.array(G["share"], float); G["TIER"] = np.zeros(G["NI"], np.int8)
    bud = dict(career=1 / 3, summit=1 / 20, community=10.0); bud.update(getattr(R, "BUDGET", {}) if R is not None else {})
    if FLOORS and R is not None:   # item 16's floors, off until the v22.3 refit
        bud.update(getattr(R, "BUDGET_FLOORS", {}))
    G["BUDGET"] = bud
    bad = [nm for nm in PK.get("target", {}) if nm not in G["ID"]]
    if bad:
        raise ValueError(f"TARGET names titles or perks the catalogue does not have: {sorted(bad)}")
    words = [m for m in PK.get("target", {}).values() if isinstance(m, str) and m not in TIERS]
    if words:
        raise ValueError(f"TARGET tier words must be one of {TIERS}: {sorted(set(words))}")
    for nm, m in PK.get("target", {}).items():
        i_ = G["ID"][nm]; sh_ = float(G["share"][i_])
        if isinstance(m, str):
            G["TIER"][i_] = TIERS.index(m) + 1
        else:
            G["TARGET"][i_] = max(sh_, min(float(m) * sh_, TARGET_CAP))
    sh = np.asarray(G["share"], float)
    car = np.nonzero(G["TIER"] == 1)[0]
    if len(car):
        mc = max(1.0, bud["career"] / max(1 - np.prod(1 - sh[car]), 1e-12))
        G["TARGET"][car] = np.maximum(sh[car], np.minimum(mc * sh[car], TARGET_CAP))
    sm = np.nonzero(G["TIER"] == 2)[0]
    if len(sm):
        tot = max(bud["summit"], 1 - np.prod(1 - sh[sm]))
        ts_ = tot * np.sqrt(sh[sm]) / np.sqrt(sh[sm]).sum()
        fl_ = min(float(bud.get("summit_floor", 0.0)), tot / len(sm))   # every summit seen at least this often
        for _ in range(len(sm)):
            lo_ = ts_ < fl_ - 1e-12
            if not lo_.any():
                break
            ts_[lo_] = fl_; ts_[~lo_] *= (tot - lo_.sum() * fl_) / ts_[~lo_].sum()
        G["TARGET"][sm] = np.maximum(sh[sm], np.minimum(ts_, TARGET_CAP))
    cm = np.nonzero(G["TIER"] == 3)[0]
    G["TARGET"][cm] = np.maximum(sh[cm], np.minimum(bud["community"] * sh[cm], TARGET_CAP))
    floor_kinds = ("career", "community", "faith")    # titles of one's own doing; statuses keep their real shares
    for i_ in range(G["NI"]):                          # the floors (Emren 10-09: rare titles must be more reachable)
        if i_ >= G["NT"]:
            fl_ = float(bud.get("perk_floor", 0.0))
        elif G["kindname"][i_] == "career" and G["TIER"][i_] != 2:
            fl_ = float(bud.get("career_floor", 0.0))
        elif G["kindname"][i_] in floor_kinds and G["TIER"][i_] != 2:
            fl_ = float(bud.get("title_floor", 0.0))
        else:
            continue
        G["TARGET"][i_] = max(G["TARGET"][i_], fl_)
    tl_ = tier_lift(R, PK.get("names", [])) if (len(car) or len(sm)) and R is not None else {}
    G["TIER_LIFT"] = tl_
    for i_ in np.concatenate([car, sm]).astype(int):   # who enters or moves into it (entry weights) by the whole lift; a
        z_ = tier_z(G, i_)                               # rung's yearly rate by at most rung_cap, so steps keep their pace
        G["rule"][i_]["norm"] = float(np.exp(z_)); G["rule"][i_]["hz"] = float(np.exp(min(z_, bud.get("rung_cap", 1.0))))
    G["TIER_Z"] = np.array([tier_z(G, i_) for i_ in range(G["NI"])])   # per item, for {missed} in the engine
    G["A_TIER"] = np.full((L["S"], L["K"]), -1)
    for (si, ki), fx in G["A_FX"].items():
        tg_ = [j for op, j, _ in fx["ok"] if op in ("title", "grants") and j >= 0 and G["TIER"][j] in (1, 2)]
        if tg_:
            G["A_TIER"][si, ki] = tg_[0]


def tier_z(G, i):
    """The budget's logit lift on a pack career or summit (0 for anything else)."""
    if G.get("TIER") is None or G["TIER"][i] not in (1, 2):
        return 0.0
    tl_ = G.get("TIER_LIFT") or {}
    return float(tl_.get(TIERS[G["TIER"][i] - 1], 0.0)) + float(tl_.get("split", {}).get(G["names"][i], 0.0))


def _earned(L, PK):
    """Earned odds (Emren 21:03: "give more chance than real odds, but keep it consistent and achievable, if player and
    character create a good strategy, and they are at right place at right time"). The same rule for every life: an act
    that takes a title gets a lift for preparation (the share of that title's HELPS the person holds: titles, perks, marks)
    and a lift for timing (the outside context in WINDOWS[moment], in driver words). Sizes: engine help_lift, window_lift.
    An act with no title: that grants a perk with its own HELPS (HELPS_PERK_<PACK>: the amateur lead, packs 03:04) earns
    the same way for that perk.
    L["ROLES"]["HELP"]: NI x NI (items that prepare for each title or perk), HELP_MK: NI x marks, HELP_N: list lengths;
    L["WINDOW"]: S x CTX (the context that opens each moment's window), WINDOW_REF: its most favourable value;
    A_EARN: S x K, the title (else the perk) each option's act earns for, -1 for none."""
    G = L["ROLES"]; NT, NI = G["NT"], G["NI"]; MK = list(L.get("MARKS", []))
    G["HELP"] = np.zeros((NI, NI), np.float32); G["HELP_MK"] = np.zeros((NI, max(len(MK), 1)), np.float32)
    G["HELP_N"] = np.zeros(NI); G["LIFT"] = np.ones(NI)   # LIFT_<PACK>: a share of both lifts (the summit stays a long shot)
    bad = []
    for t_, f_ in PK.get("lift", {}).items():
        if t_ not in G["ID"]:
            bad.append(t_)
        else:
            G["LIFT"][G["ID"][t_]] = float(f_)
    for t_, lst in PK["helps"].items():
        if t_ not in G["ID"]:
            bad.append(t_); continue
        i_ = G["ID"][t_]
        for x_ in lst:
            if x_.startswith("mark:"):
                if x_[5:] in MK:
                    G["HELP_MK"][i_, MK.index(x_[5:])] = 1
                else:
                    bad.append(x_)
            elif x_ in G["ID"]:
                G["HELP"][i_, G["ID"][x_]] = 1
            else:
                bad.append(x_)
        G["HELP_N"][i_] = len(lst)
    if bad:
        raise ValueError(f"helps.py names titles, perks or marks the catalogue does not have: {sorted(set(bad))}")
    L["WINDOW"] = np.zeros((L["S"], len(E.CTX))); L["WINDOW_REF"] = np.zeros(L["S"])
    L["WINDOW_MISSING"] = [nm for nm in PK["windows"] if nm not in L["names"]]   # not written yet, or not in this world
    for nm, words in PK["windows"].items():
        if nm not in L["names"]:
            continue
        si = L["names"].index(nm)
        L["WINDOW"][si] = E.parse(words, E.CIDX, len(E.CTX))
        L["WINDOW_REF"][si] = np.abs(L["WINDOW"][si]).sum()
    # the acts each lift applies to: an option whose act gives a title (title:, the first one written), else one that
    # grants a perk with its own helps (grants:)
    G["A_TITLE"] = np.full((L["S"], L["K"]), -1); G["A_EARN"] = np.full((L["S"], L["K"]), -1)
    G["A_MISSED"] = np.zeros((L["S"], L["K"]), bool)   # title: {missed}: the engine reads the title per person (packs 09:39)
    for (si, ki), fx in G["A_FX"].items():
        G["A_MISSED"][si, ki] = any(op == "title" and j == MISSED_TITLE for op, j, _ in fx["ok"])
        tt_ = [j for op, j, _ in fx["ok"] if op == "title" and 0 <= j < NT]
        gp_ = [j for op, j, _ in fx["ok"] if op == "grants" and j >= NT and G["HELP_N"][j] > 0]
        if tt_:
            G["A_TITLE"][si, ki] = tt_[0]
        if tt_ or gp_:
            G["A_EARN"][si, ki] = (tt_ or gp_)[0]


def _chance(L, R):
    """The Library's chance on an option (point 8, agreed 11:06): how often the act works for an ordinary person of the
    moment's ages. The engine sets the option's difficulty so that, for the people who meet this moment (their skill, the
    world's push and their perks, measured: <world>_rules.CHANCE_REF, calib_v7/chance_check.py), its true odds come to
    the chance; their own skill, perks, the moment's call and the world then move each person's odds from there.
    L["CHANCE"]: the chance (nan where an option has none: doing nothing, and batches without it)."""
    S, K = L["S"], L["K"]; D = E.DEFAULT
    L["CHANCE"] = np.full((S, K), np.nan)
    ref_ = getattr(R, "CHANCE_REF", {})
    dflt = np.mean([np.asarray(v, float)[:5] for v in ref_.values()], 0) if ref_ else np.full(E.C, 0.3)
    alpha = L["ALPHA"] - L["ALPHA"].mean(1, keepdims=True)
    ac_ = float(L["ROLES"].get("BUDGET", {}).get("act_cap", 0.0)) if "ROLES" in L else 0.0
    for si in range(S):
        rf = np.asarray(ref_.get(L["names"][si], dflt), float)
        er = float(rf[5]) if len(rf) > 5 else 0.0   # the mean earned lift of those who meet it, on title-giving options
        rf = rf[:5]
        at_ = L["ROLES"]["A_EARN"][si] if "ROLES" in L and "A_EARN" in L["ROLES"] else None
        tt_ = L["ROLES"]["A_TIER"][si] if "ROLES" in L and "A_TIER" in L["ROLES"] else None
        for ki, nt in enumerate(L["notes"][si]):
            c = (nt or {}).get("chance")
            if c is None or not L["MASK"][si, ki] or L["M"][si, ki].std() < 1e-9:
                continue
            c = float(c); c = c / 100.0 if c > 1.0 else c
            if tt_ is not None and tt_[ki] >= 0 and 0 < c < 1:   # the budget moves the odds of pack careers and summits:
                c = 1 / (1 + (1 - c) / c * np.exp(-min(ac_, tier_z(L["ROLES"], tt_[ki]))))   # down when over, up by at
                # most act_cap when under (Emren 14:41: "higher than real, but not super unrealistically"; _targets)
            c = min(max(c, 0.01), 0.99); L["CHANCE"][si, ki] = c
            m = L["M"][si, ki]
            L["DIFF"][si, ki] = (m @ rf + D["fit"] * (m @ alpha[si]) - np.log(c / (1 - c)) / D["gain"]
                                 - (D["closed_diff"] if L["CLOSED"][si, ki] >= 0 else 0.0)    # closed acts: rated if tried
                                 + (er / D["gain"] if at_ is not None and at_[ki] >= 0 else 0.0))   # the written chance is
            # the odds of those who meet it, their preparation for the title included (the packs, 01:40: election night)


if __name__ == "__main__":
    L = load_batch(sys.argv[1] if len(sys.argv) > 1 else "earth")
    print(L["S"], "situations,", len(L["COND"]), "conditions,", len(L["EVR"]), "read events,", len(L["MARKS"]), "marks")
    print("kills:", [(L["names"][i], E.ROLES[k]) for i, k in enumerate(L["KILLS"]) if k >= 0])
    print("ends:", [(L["names"][i], E.KNAMES[k]) for i, k in enumerate(L["ENDS"]) if k >= 0])
    print("once:", [(L["names"][i], E.KNAMES[k] if k >= 0 else "life") for i, k in enumerate(L["ONCE_K"]) if L["ONCE"][i]])
    print("moves:", [L["names"][i] for i in np.nonzero(L["MOVES"])[0]])
    print("marks:", L["MARKS"])
