"""The outer world's key words (chroma-engine/world-fields.md, settled 2026-10-07): one list each, shared by world.py,
world_people.py, batch.py (it checks the Library's new fields against them) and the game (it writes the words).
Changing a list changes the Library format: say so in world-fields.md first."""

# moments
TIME_OF_YEAR = ["winter", "spring", "summer", "autumn"]
HOLY_KEYS = ["feast", "fast", "pilgrimage", "mourning"]
WHO_SLOTS = ["parent", "grandparent", "elder", "sibling", "friend", "rival", "mentor", "boss", "colleague", "partner", "ex",
             "prospect", "child", "dead", "teacher", "neighbour"]
WHO_SLOTS += ["keeper", "regular", "patron", "go-between"]   # spheres (item 15): a haunt's people (phase 2 fills them)
CAST_WANTS = ["money", "care", "successor", "grandchild", "love", "rival", "forgiveness", "home", "stop", "secret"]
CAST_WANTS += ["far_hard", "far_good", "far_mixed"]   # far_ties (item 18): a tie in another town touched by an event there
CAST_WANTS += ["caught", "odd"]   # S3, S4 (chroma-ideas/social-mechanics.md): caught between two of their places; the odd one
                                  # out at a place. Fired by the place reading (sph_eyes, sph_odd), never a cast member's wish
CAUGHT_TAGS = ["side_a", "side_b", "bridge", "apart", "back"]   # S3: an option's caught: (side with place_a or place_b, bridge
                                                                # them, keep them apart, step back)
ODD_TAGS = ["blend", "hold", "leave"]                           # S4: an option's odd: (blend in, hold on, leave)
CAST_WANTS += ["lead_take", "lead_crisis", "lead_fall", "lead_routine", "lead_hand"]   # lead_ways (S7): a post's moments,
#   fired with no holder (cid -1): taking the post, a crisis of its way, its fall, the turn to routine, handing it on
# sacred lines (S5, chroma-ideas/social-mechanics.md): moments the life's own state brings, with no cast member holding
# the want (cid -1): an offer on a held line, a tragic trade-off between two held lines, amends after crossing one. They
# go last: the cast's wants are the ones before them (world_people.NW)
CAST_WANTS += ["sacred", "tragic", "amends"]
OWN_WANTS = ["sacred", "tragic", "amends"]
# the spheres finishing pack, part 2 (place_turnover, finish-pack-draft.md): "the place closed" and "the new place",
# fired with no holder (cid -1) when a haunt of the life's closes, and when a new place opens in its slot. After the own
# wants, so every index before them stays (none is a cast member's wish)
CAST_WANTS += ["place_closed", "place_opened"]
PLACE_WANTS = ["place_closed", "place_opened"]
# spheres finishing pack, part 4 (former inmates as ties, prison_ties): a moment with a fellow inmate, open only while the
# life holds an active former-inmate tie, the closest of whom takes its first who: slot (never a cast member's wish)
CAST_WANTS += ["fellow_inmate"]
SACRED_KINDS = ["promise", "truth", "own_say", "loved", "home"]   # a line's kind (sacred:), W U B R G in the Canon's order
OFFER_KINDS = ["money", "post", "favour"]                          # what an offer gives (offer:; dynamics.json offers kind)
OFFER_ROUNDS = ["first", "raised"]                                 # the first offer, or the raised one after a refusal (round:)
LINE_TAGS = ["hold", "cross"]          # an offer moment's option (line:): holds the line or crosses it
TRAGIC_TAGS = ["a", "b", "torn"]       # a tragic moment's option (tragic:): holds the first line and crosses the second (a),
                                       # the reverse (b), or gives a little of both (torn)
HEAL_TAGS = ["amends", "reflect", "not_yet"]   # an amends moment's option (heal:): amends and reflect heal the wound
TOUCHES = ["work", "money", "home", "health", "safety", "standing"]   # far_ties: what a far event touched (touch:)
LEAD_WAYS = ["rules", "knowing", "favours", "inspiring", "custom"]   # lead_ways (S7): the five ways, W U B R G (lead_way:, lead:)
FALL_KEYS = ["go", "fight", "again"]     # lead_ways: a fall moment's options (fall:): the post ends, kept at a cost, stand again later
HAND_KEYS = ["chosen", "open", "stay"]   # lead_ways: a hand-over moment's options (hand:): a chosen successor, an open contest, stay on
GROUP_KINDS = ["household", "class", "work", "congregation", "club", "scene", "online", "neighbours", "gang", "unit", "ward",
               "movement"]
FEATURES = ["city", "town", "village", "remote", "capital", "suburb", "university", "port", "coast", "industry", "mining",
            "farming", "fishing", "mountain", "resort", "boom"]
INST_KINDS = ["school", "university", "employer", "bank", "hospital", "police", "court", "prison", "army", "faith body",
              "media", "party", "union", "charity", "council", "ministry"]
# options
from realm_earth import LAW_KEYS, NORM_KEYS, LAW_V23, LAW_KEYS_ALL, NORM_KEYS_ALL   # Earth's (realm_earth.py)
LAW_STATES = ["legal", "restricted", "banned"]
from realm_earth import TECH_KEYS   # Earth's (realm_earth.py)
LEVERS = ["exit", "voice", "loyalty", "neglect", "subvert"]
LEVERS += ["found", "fund", "lead", "office"]                # spheres (item 15): levers by standing (phase 4 gives them effects)
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
