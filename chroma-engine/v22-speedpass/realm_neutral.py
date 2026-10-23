"""The neutral world (v25, chroma-engine/notes/v25/other-shapes.md section 1): a test world for Release's core-even rows,
never offered to a player. Chosen by P["realm"] = "neutral" (world_fit.realm); everything not named here is Earth's.

Every sphere's starting mix is .2 a colour (SPH_M0_EVEN), the places' faces are their town's (PLACE_FACES_EVEN, no lasting
lean of their own), the bodies drift colour-even (inst_even on), there is no formal layer, and every profile dimension
sits at its middle with no spread, so what a world rewards is r = mix / .2 = 1 everywhere at the start. Nothing here may
import the engine.
"""
from realm_earth import *  # noqa: F401,F403   (Earth's words and the core's facts)
from realm_earth import PROFILES as _EARTH_PROFILES

SPH_M0_EVEN = True        # every sphere's starting mix .2 a colour, in every epoch
PLACE_FACES_EVEN = True   # a place's face follows its town's sphere mix, without a lasting lean of its own
INST_EVEN = True          # the bodies drift toward their own past and their leaders' colours (world param inst_even)
TILT_LAYER = (0.0, 0.0, 0.0, 0.0, 0.0)
PROFILES = {kind: {nm: dict(e, **{lay: {d: (0.5, 0.0) for d in e[lay]} for lay in ("values", "practices", "incentives")},
                            source="the neutral world: every dimension at its middle", note="")
                   for nm, e in ents.items()}
            for kind, ents in _EARTH_PROFILES.items()}
