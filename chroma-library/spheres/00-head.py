# Chroma Library: the spheres of society, the words the game reads (item 15, phase 1). Library thread, 2026-10-09.
# Plain data, modern days. Keys are sphere and colour ("gather.R") or the subsector ("gather.house"), never a name,
# so a rename never breaks a key (chroma-ideas/spheres-implementation.md section 4). Drawn from
# chroma-ideas/spheres-data/<sphere>.json and checked by chroma-library/tests/check_spheres.py.
#
# SPHERE        each sphere's name and the question it answers in a life
# FACE          the 45 faces: name (a motive, never a place), the line, and the hover line for each driver that moves it
# PLACE         the 60 kinds of place: the modern name and five readings, one per face (role and reading)
# RUNG          the five rungs of standing per sphere, in LADDER order (newcomer, regular, known, pillar, leader)
# PLACE_SHORT   the seven epoch place names over five words, shortened (the epoch words wait for item 17)
# PAIR          the 90 pair faces: name, idea, line, shadow, modern place and role
# EVENT         the 175 modern sphere events: name, tone, the town's line and the character's
# CAST          each face's default modern person: role, place, line, age, sex, setting
# CASCADE       the 13 modern cascades: each step's event, the world's line and the character's
# HAUNT         the 31 haunt kinds: names, keeper, regular and patron words, go-between, newcomer and known lines
# SHADOW, GREY, DEEP  phase 5: each face's shadow, each sphere's grey side, the deep state's panel words
# No line names a color.

SPHERE = {
    'rule': dict(name='Rule and law', question='Whose say counts, mine included, and will I get a fair hearing when I am wronged?'),
    'gather': dict(name='Gathering', question='When the work is done, where do I go, who knows my name there, and what do we become together?'),
    'arts': dict(name='Arts and lore', question='Whose songs and stories made me, which are mine, and what will I add that others will sing or tell after me?'),
    'faith': dict(name='Faith and rites', question='What is my life for, who stands with me at its turning points, and what do I owe to what is beyond me?'),
    'care': dict(name='Care and healing', question='When a body fails, mine or someone I love, who carries whom, at what cost, and what do we owe each other?'),
    'learn': dict(name='Learning', question='What will I come to know and be able to do, who will teach me, and which doors will my learning open or close?'),
    'prod': dict(name='Production', question='What will my hands and days make, with whom and on whose terms, and will it feed us and mean something?'),
    'comm': dict(name='Commerce', question='What is a fair exchange, whom can I trust with what I have, and will my trade and debts free my life or bind it?'),
    'prot': dict(name='Protection', question='Who keeps me and mine safe, at what price, and will I ever be asked to stand guard, or to fight?'),
}

