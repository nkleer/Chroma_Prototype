# Chroma content pack: Stage and Screen. The pack in the other worlds.
# Pathways and packs thread, 2026-10-06, after Emren (21:37): modern world conditions and terms first, "but dont forget
# that applications must be feasible for other wordly setting, even including supernatural sometimes." The catalogue
# stays in modern Earth terms (the base catalogue has no worlds field); this file gives each title and perk its form in
# the game's tribal and magic worlds (chroma-game/prototype/story.py, SETTINGS and WORLD: "clans, hunts, elders and the
# turning seasons, before cities"; "towers, guilds and old powers; a gift may awaken"), so the pathway keeps the same
# shape everywhere: the same rungs, doors, crossings and falls, and a lead on every road. Plain data for the Library and
# the game; nothing runs.
#
# The shape of the stage in each world:
#   earth   youth theatres, school plays, amateur societies, drama schools, the fringe, theatres, film and television
#           sets, voice booths; agents, casting directors, producers, critics and the actors' union.
#   tribal  the band tells its stories at the fire in the long nights: tellers speak them, players act them in masks
#           and skins, the hidden voices speak for the spirits and the animals from behind a hide screen, and the
#           shadow-players throw the hunt onto the cave wall by firelight (the nearest thing to a screen). At the
#           turning seasons the band plays its great tellings, and at the summer gathering of the clans one player
#           wears the great mask of the first ancestor (the lead). An old teller keeps the stories and teaches the
#           children. Gifts of meat, hides and shells stand where fees stand; there are no contracts, and a teller-player
#           is kept by the band through the winter.
#   magic   walled cities with playhouses under a licence from the Crown or an Order; travelling companies with wagons;
#           the guild of players, its school and its ranks; illusionist players whose glamours make a scene appear in
#           the air (the nearest thing to a screen), and mirror-plays shown in scrying glasses in the great houses;
#           voices for the speaking-stones and the puppet theatres. Patrons, play-merchants and players' brokers stand
#           where producers and agents stand; heralds and broadsheets carry the notices.
#
# Supernatural ways onto the stage and off it are possible sometimes and never forced: they come as world-only doors,
# crossings and falls (WORLD_ONLY_STAGE below, planned in MOMENTS-BRIEF.md, part 5), each one optional, each one with a
# price. Modern Earth has no magic and no supernatural moments.
#
# Fields: tribal and magic, the form in that world (a plain phrase the story can use); note, how it maps: "same rung"
# when the role exists as it is, "nearest" when the role cannot exist there and a stand-in keeps the pathway's shape.

WORLDS_STAGE = {
    # ------------------------------------------------ pack titles: the actor's road
    "professional actor": dict(
        tribal="a teller-player, kept by the band through the winter to play the old stories at the fire",
        magic="a player in a licensed company of a city playhouse, or of a travelling company with wagons",
        note="tribal: nearest (no wages: kept in meat and gifts); magic: same rung"),
    "voice actor": dict(
        tribal="a hidden voice, who speaks for the spirits and the animals from behind the hide screen",
        magic="a voice for the speaking-stones and the puppet theatres of the city",
        note="same rung"),
    "lead actor or actress": dict(
        tribal="the one who wears the great mask: the first ancestor in the summer telling, or the hero of the "
               "winter tellings",
        magic="the leading player of a company, whose name the herald cries before the play",
        note="same rung, a facet on the player's title (or on the hidden voice)"),
    "director": dict(
        tribal="the shaper of a telling, who says who plays which spirit and where the fire throws the shadows",
        magic="master of the play in a playhouse or a travelling company",
        note="same rung"),
    "artistic director": dict(
        tribal="keeper of the tellings of the summer gathering, who decides which stories the clans will see",
        magic="master of a royal, guild or Order playhouse",
        note="same rung, a facet on the shaper's title"),
    "playwright or screenwriter": dict(
        tribal="a maker of new tellings, who sets new words and new deeds to the old stories",
        magic="a play-maker, who writes for the playhouses, the illusionists and the mirror-plays",
        note="tribal: nearest (no writing: the telling is made and kept by voice); magic: same rung"),
    "producer": dict(
        tribal="the one who gathers the hides, the masks, the fires and the feast for a great telling, and is owed "
               "for it",
        magic="a play-merchant, who puts up the coin for a company and takes a share of the takings",
        note="tribal: nearest (gifts and debts stand for money); magic: same rung"),
    "stage manager": dict(
        tribal="keeper of the fire and the masks, who gives each player the sign to come into the light",
        magic="the book-keeper of a playhouse, who prompts, calls the changes and runs the play from the wings",
        note="same rung"),
    "casting director": dict(
        tribal="the elder who chooses which young one will play which spirit",
        magic="the company's chooser of players",
        note="same rung"),
    "talent agent": dict(
        tribal="a go-between who speaks for a teller to the other bands, and takes a share of the gifts",
        magic="a players' broker, who places players with companies and patrons for a cut",
        note="tribal: nearest; magic: same rung"),
    "drama teacher": dict(
        tribal="an old teller who teaches the children the tellings, the voices and the masks",
        magic="a master at the players' guild school",
        note="same rung"),
    # ------------------------------------------------ community and statuses
    "background artist": dict(
        tribal="one of the many in a great telling: the herd, the war band, the dead",
        magic="a walk-on, hired by the night for the crowd scenes and the illusionists' processions",
        note="same rung"),
    "amateur actor": dict(
        tribal="a player in the band's own tellings at the turning seasons",
        magic="one of the guild's mystery players, who play the old pageants on feast days",
        note="same rung"),
    "youth theatre member": dict(
        tribal="one of the children who play the small spirits and the animals in the tellings",
        magic="a child in the players' guild's children's company",
        note="same rung"),
    "community theatre director": dict(
        tribal="the one who shapes the band's own telling at midwinter",
        magic="the guild's master of pageants",
        note="same rung"),
    "drama school student": dict(
        tribal="an apprentice to an old teller for three winters",
        magic="a scholar of the players' guild school",
        note="same rung"),
    "understudy": dict(
        tribal="the one who learns the great mask's telling in case its wearer falls sick",
        magic="a second to the leading player, word-perfect and waiting",
        note="same rung"),
    # ------------------------------------------------ pack perks: skills
    "acting": dict(tribal="playing a part at the fire", magic="playing a part", note="same"),
    "screen acting": dict(tribal="playing for the shadow wall, where every small move is thrown huge",
                          magic="playing for the illusionist's glamour and the scrying glass",
                          note="nearest in both: no cameras; the same craft of the small, true gesture"),
    "improvisation": dict(tribal="making a telling up as the fire burns", magic="playing without a book",
                          note="same"),
    "stage combat": dict(tribal="fighting in the telling with spears that never touch",
                         magic="stage swordplay with blunted blades", note="same"),
    "accents and voices": dict(tribal="the voices of every clan and every beast",
                               magic="the speech of every city and every race of the realm", note="same"),
    "learning lines": dict(tribal="keeping a telling word for word", magic="learning a part by the book",
                           note="same"),
    "auditioning": dict(tribal="showing the elders what you can play", magic="trying out before a company",
                        note="same"),
    "telling a story aloud": dict(tribal="telling the old stories at the fire", magic="telling tales in the "
                                  "tavern and the great hall", note="same"),
    "directing actors": dict(tribal="shaping the players of a telling", magic="directing a company", note="same"),
    "a casting eye": dict(tribal="seeing which young one is the bear and which the crow",
                          magic="an eye for the right player", note="same"),
    "writing scripts": dict(tribal="making new tellings", magic="writing plays", note="tribal: nearest (by voice)"),
    "calling the show": dict(tribal="giving the signs at the fire", magic="calling the changes from the wings",
                             note="same"),
    # ------------------------------------------------ pack perks: access
    "union card": dict(tribal="a place among the band's tellers, given by the old ones",
                       magic="the players' guild token", note="tribal: nearest; magic: same"),
    "drama school diploma": dict(tribal="three winters at an old teller's side, and the mark that shows it",
                                 magic="the guild school's seal", note="same"),
    "child performance licence": dict(tribal="the mother's and the elders' leave for a child to play at the "
                                      "gathering, with a kinswoman always beside it",
                                      magic="the guild's licence for a child player, signed by a parent, with a "
                                            "chaperone and lessons kept",
                                      note="same: a child plays only with a guardian beside it"),
    "casting directory listing": dict(tribal="a name the other bands ask for", magic="a name on the brokers' roll",
                                      note="tribal: nearest; magic: same"),
    "a fringe slot": dict(tribal="a place by the outer fires at the gathering, where anyone may play",
                          magic="a pitch at the fair's booths, under the fair's licence", note="same"),
    # ------------------------------------------------ pack perks: standing, bonds, assets
    "a lead role to remember": dict(tribal="once wore the great mask, and the band still talks of it",
                                    magic="once played the lead, and the town still talks of it", note="same"),
    "good notices": dict(tribal="praise from the elders after the telling", magic="good notices in the broadsheets",
                         note="same"),
    "a known face": dict(tribal="a face every band knows from the gatherings",
                         magic="a face the whole city knows from the glamours and the glasses", note="same"),
    "an award for acting": dict(tribal="the gift of the best hide at the gathering, given to the finest player",
                                magic="the guild's laurel for the season's best player", note="same"),
    "a cult following": dict(tribal="a few who follow you from fire to fire", magic="a small, devoted following in "
                             "the city", note="same"),
    "an agent who believes in you": dict(tribal="a go-between who speaks for you at every fire",
                                         magic="a broker who fights for you", note="same"),
    "a director who keeps casting you": dict(tribal="a shaper who always wants you in the telling",
                                             magic="a master of the play who keeps casting you", note="same"),
    "a company that feels like family": dict(tribal="the tellers of your band", magic="a company like family",
                                             note="same"),
    "a year group from drama school": dict(tribal="the others who learned at the old teller's side with you",
                                           magic="your year at the guild school", note="same"),
    "a producer who backs you": dict(tribal="a family that gives the feast for your telling",
                                     magic="a patron or play-merchant who backs you", note="same"),
    "a showreel": dict(tribal="a telling the bands ask you to play again and again",
                       magic="a glamour-reel: a crystal holding your best scenes", note="tribal: nearest; magic: same"),
    "repeat fees": dict(tribal="gifts that keep coming each time your telling is told",
                        magic="a share each time your mirror-play is shown", note="same"),
    "a company of your own": dict(tribal="your own band of players, who walk with you to the gatherings",
                                  magic="a company of your own, with a wagon and a licence", note="same"),
    # ------------------------------------------------ base titles the pathway uses
    "stage technician": dict(tribal="the one who builds the screens and keeps the fires", magic="a stage-wright of "
                             "the playhouse, who keeps its traps and its flying ropes", note="same side door"),
    "teacher": dict(tribal="an elder who teaches the children", magic="a schoolmaster", note="same side door"),
    "novelist": dict(tribal="a maker of long tellings", magic="a writer of romances", note="tribal: nearest"),
    "festival organiser": dict(tribal="the one who prepares the summer gathering", magic="a master of the fair",
                               note="same side door"),
    "community-radio presenter": dict(tribal="the camp's crier", magic="a herald of the ward", note="nearest"),
    "grandparent": dict(tribal="an old one who tells the children the stories", magic="a grandparent",
                        note="same"),
    # ------------------------------------------------ base perks the pathway uses
    "stagecraft": dict(tribal="masks, fires and screens", magic="traps, ropes and lamps", note="same"),
    "singing": dict(tribal="singing the old songs", magic="singing", note="same"),
    "dancing": dict(tribal="the dances of the seasons", magic="dancing", note="same"),
    "writing stories": dict(tribal="making stories", magic="writing tales", note="same"),
    "public speaking": dict(tribal="speaking at the fire", magic="speaking in hall", note="same"),
    "following online": dict(tribal="a name the young ones repeat", magic="a name in the broadsheets' gossip",
                             note="nearest in both"),
    "name on the local scene": dict(tribal="a name at every fire of the band", magic="a name in the taverns of the "
                                    "ward", note="same"),
    "good name in town": dict(tribal="a good name in the band", magic="a good name in the city", note="same"),
    "mentor": dict(tribal="an old teller who takes you on", magic="an old player who takes you on", note="same"),
    "patron": dict(tribal="a great family who feeds your telling", magic="a noble patron", note="same"),
    "contact in the trade": dict(tribal="a friend among the tellers of another band", magic="a friend in the guild",
                                 note="same"),
    "cleared to work with children": dict(tribal="trusted by the mothers with the children",
                                          magic="the guild's leave to teach children", note="same"),
    "teaching": dict(tribal="teaching the young", magic="teaching", note="same"),
    "graduate": dict(tribal="years at the elders' teaching", magic="a scholar of the academy",
                     note="tribal: nearest (no degrees); magic: same"),
    "scholarship": dict(tribal="a family that feeds you while you learn", magic="a bursary of the guild school",
                        note="same"),
    "savings": dict(tribal="stores laid by", magic="coin put by", note="same"),
    "striking a deal": dict(tribal="trading gift for gift", magic="striking a bargain", note="same"),
    "organising people": dict(tribal="getting the band to move together", magic="getting a company to move "
                              "together", note="same"),
    "selling": dict(tribal="talking a family into a gift", magic="selling", note="same"),
    "second language": dict(tribal="the tongue of another clan", magic="another tongue of the realm", note="same"),
    "boxing or martial arts": dict(tribal="wrestling and the spear dance", magic="swordplay", note="same"),
    "reliable record": dict(tribal="a name for being there", magic="a reliable name", note="same"),
    "studio of one's own": dict(tribal="a hide-walled place of your own for the voices",
                                magic="a quiet room with a speaking-stone of your own", note="nearest"),
    # ------------------------------------------------ the shared reach ladder (chroma-packs/core/reach.py)
    "known across the country": dict(tribal="known among all the clans of the valley", magic="known across the realm",
                                     note="same rung"),
    "a household name": dict(tribal="a name told at every fire, for generations",
                             magic="a name in every tavern song of the realm", note="same rung"),
}

# World-only doors, crossings and falls (planned in MOMENTS-BRIEF.md, part 5, "World-only moments"). Each is optional,
# comes sometimes, and has a price; none is forced. Earth has none: modern Earth has no magic. Each of the four
# crossings offers the lead in that world, so the lead is reachable on the tribal and magic roads too.
WORLD_ONLY_STAGE = {
    "the old teller dies at midwinter": dict(only="tribal", kind="door",
                                             what="the band's old teller dies in the long nights, and the tellings "
                                                  "need a new voice: a young player, the one who learned at the old "
                                                  "one's side, or nobody"),
    "chosen to wear the great mask": dict(only="tribal", kind="crossing",
                                          what="the elders choose who will wear the great mask of the first ancestor "
                                               "at the summer gathering (the lead), and the mask is said to take "
                                               "something from whoever wears it"),
    "the mimic who mocks the chief": dict(only="tribal", kind="fall",
                                          what="a player who mocks the chief in a telling: the band laughs, the "
                                               "chief does not"),
    "the spirits ride the dancer": dict(only="tribal", kind="fall",
                                        what="in the deepest telling a player goes into a trance the shaman cannot "
                                             "read, and the band fears what rides them"),
    "the illusionist players come to town": dict(only="magic", kind="door",
                                                 what="a company whose glamours make every scene appear in the air "
                                                      "comes to town, and needs players, hands and a child for the "
                                                      "fairy"),
    "a glamour that makes the play real": dict(only="magic", kind="crossing",
                                               what="an illusionist offers a glamour that makes the audience see and "
                                                    "feel the play as real, for the lead's night; the glamour asks "
                                                    "for something of the player"),
    "the mask that changes its wearer": dict(only="magic", kind="door",
                                             what="an old mask in a costume trunk lets its wearer become anyone on "
                                                  "stage, and a little more of them each time"),
    "the theatre where the dead come to watch": dict(only="magic", kind="crossing",
                                                     what="an old playhouse where the dead fill the gallery on one "
                                                          "night a year; whoever leads that night is remembered by "
                                                          "both worlds"),
}
