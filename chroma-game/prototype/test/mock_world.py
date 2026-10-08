"""A stand-in for the engine's outer world, for testing the game's world panel, circle, reach and levers before the
engine's world lands. Shapes follow chroma-game/world-hooks-for-engine.md. Test only: never pinned or published.
   source = MockWorld(seed); game.Game.world_source = source  (or call source(t) directly)"""
import random

COLORS = "WUBRG"
LAWS = ["same_sex_marriage", "cannabis", "assisted_dying", "strike_action", "home_schooling", "conscription"]
NORMS = ["living together unmarried", "a mother working full time", "same-sex couples", "tattoos at work", "eating no meat"]
RIGHTS = ["speech", "faith", "movement", "sexuality", "women"]


def mix(rnd, lead):
    v = [rnd.random() * 0.15 + 0.05 for _ in COLORS]
    for c in lead:
        v[COLORS.index(c)] += 0.35
    s = sum(v)
    return [round(x / s, 2) for x in v]


class MockWorld:
    def __init__(self, seed=1, born_t=0, years=90):
        rnd = random.Random(seed)
        self.born_t = born_t
        self.record = []
        t = born_t - 30 * 52                                   # history starts before birth
        end = born_t + years * 52
        eras = ["WU", "BG", "UR", "WG", "BR", "W", "URG"]
        era_i, next_era = 0, t
        next_el, next_rec, unemp = t + 52, t + rnd.randint(150, 400), 5.0
        gov = "WU"; self.figures = [dict(id=i, role=r, colors=mix(rnd, rnd.choice(["W", "U", "B", "R", "G", "WU", "BR"])), standing=3 if i < 2 else 2,
                                         alive=True) for i, r in enumerate(["head", "opposition", "star", "athlete", "preacher", "scientist", "magnate", "activist"])]
        for f in self.figures:
            f["read"] = f.pop("colors")
        while t < end:
            if t >= next_era:
                ls = eras[era_i % len(eras)]; era_i += 1
                self.record.append(dict(t=t, kind="era", domain="era", big=True, colors=mix(rnd, ls), kind_of=rnd.choice(["policy", "institutions", "cosmology"])))
                next_era = t + rnd.randint(12, 26) * 52
            if t >= next_el:
                gov = rnd.choice(["WU", "BG", "WG", "UR", "B", "RG"])
                self.record.append(dict(t=t, kind="election", domain="state", big=True, colors=mix(rnd, gov), leader=0, support=0.4 + rnd.random() * 0.15, turnout=0.66))
                next_el = t + rnd.randint(4, 5) * 52
            if t >= next_rec:
                sev = rnd.choices(["mild", "severe", "crisis"], [70, 25, 5])[0]
                self.record.append(dict(t=t + 13, kind="recession", domain="econ", big=sev != "mild", severity=sev))
                self.record.append(dict(t=t + 52, kind="recession_over", domain="econ", big=False))
                unemp += {"mild": 1.5, "severe": 3, "crisis": 5}[sev]
                next_rec = t + rnd.randint(200, 420)
            if rnd.random() < 0.02:
                k = rnd.choice(LAWS)
                self.record.append(dict(t=t, kind="law", domain="state", big=False, law=k, state=rnd.choice(["legal", "restricted", "banned"])))
            if rnd.random() < 0.012:
                self.record.append(dict(t=t, kind="disaster", domain="nature", big=True, disaster=rnd.choice(["a flood", "a storm", "a wildfire"]), locality=rnd.randint(0, 14)))
            if rnd.random() < 0.004:
                self.record.append(dict(t=t, kind="pandemic", domain="nature", big=True, phase="rising"))
            if rnd.random() < 0.002:
                self.record.append(dict(t=t, kind="war", domain="state", big=True, war="abroad"))
            if rnd.random() < 0.03:
                self.record.append(dict(t=t, kind="poll", domain="cult", big=False, norm=rnd.choice(NORMS), share=rnd.random()))
            if rnd.random() < 0.008:
                self.record.append(dict(t=t, kind=rnd.choice(["scandal", "figure_rise", "figure_fall"]), domain="figure", big=False, figure=rnd.randint(0, 7)))
            if rnd.random() < 0.01:
                self.record.append(dict(t=t, kind=rnd.choice(["layoffs", "closure", "crime_wave", "local_election"]), domain=rnd.choice(["inst", "place"]),
                                        big=False, inst_kind=rnd.choice(["factory", "hospital", "school"]), locality=3, colors=mix(rnd, "WG")))
            unemp = 5 + (unemp - 5) * 0.97
            self.record.append(dict(t=t, kind="figures", domain="econ", big=False, unemp=round(unemp + rnd.random() * 0.3, 1)))
            t += 13
        self.gov, self.rnd = gov, rnd
        self.cast = []
        roles = [("mother", 1), ("father", 1), ("best friend", 1), ("partner", 1), ("sister", 2), ("grandmother", 2), ("cousin", 3),
                 ("friend", 2), ("friend", 3), ("mentor", 3), ("colleague", 4), ("neighbour", 4), ("rival", 4), ("ex", 4), ("classmate", 4)]
        for i, (r, layer) in enumerate(roles * 2):
            self.cast.append(dict(id=100 + i, sex=rnd.choice(["female", "male"]), born_t=born_t + rnd.randint(-60, 10) * 52, roles=[r],
                                  layer=min(4, layer + (i >= len(roles))), closeness=rnd.random(), trust=rnd.random(),
                                  read=mix(rnd, rnd.choice(COLORS)), alive=rnd.random() > 0.08, want=rnd.choice([None, None, "a loan", "help moving"])))

    def __call__(self, t):
        """Everything the game reads at hidden week t: (snapshot, record so far, cast, standing)."""
        rec = [r for r in self.record if r["t"] <= t]
        era = next((r for r in reversed(rec) if r["kind"] == "era"), None)
        el = next((r for r in reversed(rec) if r["kind"] == "election"), None)
        fig = next((r for r in reversed(rec) if r["kind"] == "figures"), dict(unemp=5))
        snap = dict(era=dict(colors=era["colors"], kind=era["kind_of"], since_t=era["t"]) if era else None,
                    econ=dict(phase_published="recession" if any(r["kind"] == "recession" and t - r["t"] < 52 for r in rec) else "expansion",
                              unemp=fig["unemp"], infl=2.1, housing=0.3),
                    gov=dict(colors=el["colors"], leader=0, support=el["support"], next_election_t=el["t"] + 4 * 52) if el else None,
                    laws={k: "legal" for k in LAWS[:3]}, rights={k: 0.9 for k in RIGHTS}, war="peace", pandemic="none",
                    figures=self.figures, season=("winter", "spring", "summer", "autumn")[(t // 13) % 4],
                    place=dict(locality=3, kind="industrial town", society=0))
        standing = dict(close=dict(standing=3, felt=0.8, hint="about right"), place=dict(standing=1, felt=0.45, hint="less than they think"),
                        inst=dict(standing=0, felt=0.1, hint="about right"), society=dict(standing=0, felt=0.05, hint="about right"))
        return snap, rec, self.cast, standing
