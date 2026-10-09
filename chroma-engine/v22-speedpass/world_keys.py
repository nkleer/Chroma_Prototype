"""The outer world's key words (chroma-engine/world-fields.md, settled 2026-10-07): one list each, shared by world.py,
world_people.py, batch.py (it checks the Library's new fields against them) and the game (it writes the words).
Changing a list changes the Library format: say so in world-fields.md first."""

# moments
TIME_OF_YEAR = ["winter", "spring", "summer", "autumn"]
HOLY_KEYS = ["feast", "fast", "pilgrimage", "mourning"]
WHO_SLOTS = ["parent", "grandparent", "elder", "sibling", "friend", "rival", "mentor", "boss", "colleague", "partner", "ex",
             "prospect", "child", "dead", "teacher", "neighbour"]
CAST_WANTS = ["money", "care", "successor", "grandchild", "love", "rival", "forgiveness", "home", "stop", "secret"]
GROUP_KINDS = ["household", "class", "work", "congregation", "club", "scene", "online", "neighbours", "gang", "unit", "ward",
               "movement"]
FEATURES = ["city", "town", "village", "remote", "capital", "suburb", "university", "port", "coast", "industry", "mining",
            "farming", "fishing", "mountain", "resort", "boom"]
INST_KINDS = ["school", "university", "employer", "bank", "hospital", "police", "court", "prison", "army", "faith body",
              "media", "party", "union", "charity", "council", "ministry"]
# options
LAW_KEYS = ["drugs", "divorce", "abortion", "same-sex marriage", "conscription", "guns", "gambling", "alcohol", "sex work",
            "euthanasia", "home schooling", "death penalty", "adoption",
            "tobacco", "knives", "drink-driving", "prescription medicines", "childminding", "gender on papers"]   # v23: W38 held-back
# v23: a key written with a leading minus closes the option the other way round (law: -conscription, evading a call-up
# where conscription is in force; norm: -same-sex marriage, snubbing a same-sex partner where it is accepted)
NORM_KEYS = LAW_KEYS + ["cohabiting", "tattoos", "single parenthood", "faith in public", "leaving a faith", "coming out",
                        "role crossing", "transition", "mixed marriage"]
# "role crossing": acceptance of living across the expected role for one's sex (was "women at work"); options use role:
# "transition": acceptance of living as one's own gender (chroma-identity/for-the-engine.md)
LAW_STATES = ["legal", "restricted", "banned"]
TECH_KEYS = ["phone", "computer", "internet", "video calls", "online dating", "remote work", "ai helper", "modern medicine",
             "car", "plane"]
LEVERS = ["exit", "voice", "loyalty", "neglect", "subvert"]
DOMAINS = ["close", "group", "place", "institution", "state", "economy", "culture", "tech", "nature", "belief", "abroad"]
RECORD_DOMAINS = DOMAINS + ["figure", "era"]          # the public record and history log also name these
# titles (catalogue keywords)
SECTORS = ["farm", "industry", "services", "knowledge", "public"]
RINGS = ["close", "settings and place", "institutions", "state, economy and culture"]   # standing and felt reach
