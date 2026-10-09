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
            "euthanasia", "home schooling", "death penalty", "adoption"]
# v23: a key written with a leading minus closes the option the other way round (law: -conscription, evading a call-up
# where conscription is in force; norm: -same-sex marriage, snubbing a same-sex partner where it is accepted)
NORM_KEYS = LAW_KEYS + ["cohabiting", "tattoos", "single parenthood", "faith in public", "leaving a faith", "coming out",
                        "role crossing", "transition", "mixed marriage"]
# W38b (the Library's held-back law keys): options may name them in law: and norm:. The world does not model them yet:
# they read at their modern state (world.py LAW_MOD, NORM_MOD) until the world's switch for them is built (v22.3 refit).
LAW_V23 = ["tobacco", "knives", "drink-driving", "prescription medicines", "childminding", "gender on papers"]
LAW_KEYS_ALL = LAW_KEYS + LAW_V23           # what an option's law: may name
NORM_KEYS_ALL = NORM_KEYS + LAW_V23         # what an option's norm: may name
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
# the spheres of society (item 15; world-fields.md, "The spheres of society", 10-09). Read by the sphere layer and checked
# against chroma-ideas/spheres-data by tools/sphere_tables.py (sphere_data.py holds the tables)
EPOCHS = ["bands", "villages", "cities", "realms", "sail", "machine", "modern", "magic"]
SPHERES = ["rule", "gather", "arts", "faith", "care", "learn", "prod", "comm", "prot"]
FACES = ["W", "U", "B", "R", "G"]        # a face is a sphere and a colour: "gather.R"; its name is a Library word
PAIRS = ["WU", "UB", "BR", "RG", "GW", "WB", "UR", "BG", "RW", "GU"]   # a pair face: "prot.RW" (other letter orders read alike)
SPHERE_FACES = [f"{s}.{c}" for s in SPHERES for c in FACES]           # 45
SPHERE_PAIRS = [f"{s}.{p}" for s in SPHERES for p in PAIRS]           # 90
SUBSECTORS = {"rule": ["counsel", "office", "judgment", "law", "sanction", "voice"],
              "gather": ["house", "hall", "great", "games", "circle", "night", "talk"],
              "arts": ["song", "stage", "screen", "tale", "page", "craft", "rite"],
              "faith": ["congregation", "rites", "calendar", "orders", "works", "seeking", "shrines"],
              "care": ["hearth", "birth", "healers", "physic", "houses", "rescue", "public"],
              "learn": ["rearing", "schooling", "apprentice", "higher", "keeping", "finding"],
              "prod": ["wild", "land", "ground", "craft", "works", "founding"],
              "comm": ["gift", "market", "shop", "far", "credit", "office", "hire"],
              "prot": ["watch", "host", "hire", "watchers", "walls", "rescue", "holding"]}   # 60
HAUNT_KINDS = ["gather.house", "gather.hall", "gather.games", "gather.circle", "gather.night",
               "arts.song", "arts.stage", "arts.tale", "arts.page", "arts.craft",
               "faith.congregation", "faith.orders", "faith.seeking", "learn.keeping", "learn.higher",
               "care.houses", "comm.market", "comm.shop", "comm.credit", "prod.wild", "prod.land", "prod.craft",
               "prot.watch", "prot.host", "rule.voice", "rule.counsel",
               "gather.great", "gather.talk", "arts.screen", "faith.shrines", "prot.rescue"]   # 31
DRIVERS = ["insecurity", "plenty", "war", "crowding", "inequality", "schooling", "exposure", "change"]
HAZARD_VARS = ["war_drop", "outbreak_drop", "disaster_now", "meaning_gap", "welfare", "old_share"]
FACE_NEEDS = ["safety", "belonging", "meaning"]    # autonomy and competence come from acting as oneself, in any face
TIME_ROWS = ["work", "learn", "haunts", "faith", "care_given", "service", "civic", "market"]
JOIN = {"joined": 1.0, "tied": 0.5, "apart": 0.0}
LADDER = ["newcomer", "regular", "known", "pillar", "leader"]
SEPARATION = ["close-knit", "own", "apart"]
CELL_AGE = ["young", "mid", "old"]
CELL_SEX = ["f", "m", "mixed"]
CELL_SETTING = ["camp", "rural", "town", "city", "sea"]
EVENT_FAMILIES = ["plenty_and_want", "boom_and_bust", "the_land", "a_house_opens", "a_house_closes", "a_keeper_passes",
                  "something_new", "strangers_come", "the_rule_opens", "the_rule_closes", "power_breaks", "war_and_peace",
                  "sickness_and_disaster", "trust_broken", "help_ourselves", "rites_of_life", "names_rise_and_fall", "quarrels"]
# Replace (spheres-implementation.md section 5): each group kind, institution kind and part of the state has a home sphere
# (employer and work go by sector; the second sphere of scene, media, neighbours and household is a share, not a home)
GROUP_SPHERE = {"household": "care", "class": "learn", "work": None, "congregation": "faith", "club": "gather",
                "scene": "gather", "online": "gather", "neighbours": "gather", "gang": "prot", "unit": "prot",
                "ward": "care", "movement": "rule"}
INST_SPHERE = {"school": "learn", "university": "learn", "employer": None, "bank": "comm", "hospital": "care",
               "police": "prot", "court": "rule", "prison": "prot", "army": "prot", "faith body": "faith", "media": "gather",
               "party": "rule", "union": "prod", "charity": "care", "council": "rule", "ministry": "rule"}
SECTOR_SPHERE = {"farm": "prod", "industry": "prod", "services": "comm", "knowledge": "learn", "public": "rule"}
STATE_SPHERE = {"say": "rule", "law_book": "rule", "rights": "rule", "purse": "rule", "war": "prot", "force": "prot"}
