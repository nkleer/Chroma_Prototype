# S7 "Ways to lead" (chroma-ideas/social-mechanics.md S7; switch lead_ways, off until v22.4). The game's words for a post.
# LEAD_WAY    world_keys.LEAD_WAYS, the five ways a post is held (rules W, knowing U, favours B, inspiring R, custom G; the
#             game keeps the colour), as a phrase after "leading": "leading by fair rules".
# LEAD_LEGIT  legitimacy in words, (legit_min, word) best first; the game takes the first pair the post's legitimacy (0 to 1)
#             reaches. Under .2 a post falls.
# LEAD_PLACE  the plain name of what a leading title leads (world_people.LEAD_TITLES), the lead moments' {place}; then
#             SETTING_PLACE for a setting they lead (world_keys.GROUP_KINDS), then SPHERE_PLACE by sphere, the last resort.
LEAD_WAY = dict(rules='by fair rules', knowing='by knowing best', favours='by favours owed', inspiring='by inspiring people',
                custom='as one of them, by the old ways')
LEAD_LEGIT = [(.7, 'firmly accepted'), (.45, 'accepted'), (.2, 'doubted'), (0, 'losing their hold')]
LEAD_PLACE = {
    'head of government': 'the government', 'minister': 'the ministry', 'party leader': 'the party',
    'member of parliament': 'the constituency', 'mayor': 'the town hall', 'local councillor': 'the ward on the council',
    'lay judge': 'the bench', 'research group leader': 'the research group',
    'community centre manager': 'the community centre', 'artistic director': 'the company', 'shift manager': 'the shift',
    'head chef': 'the kitchen', 'founder of a firm': 'the firm', 'union rep': 'the union branch', 'shop owner': 'the shop',
    'café or bar owner': 'the café', 'community theatre director': 'the community theatre',
    'deacon or elder': 'the congregation', 'team captain': 'the team', 'community-garden coordinator': 'the community garden',
    'parent-association organiser': "the parents' association", 'book-club organiser': 'the book club',
    'board-game club organiser': 'the games club', 'neighbourhood-watch coordinator': 'the neighbourhood watch',
    'festival organiser': 'the festival', 'volunteer research organiser': 'the volunteer research group',
    'disability-rights organiser': 'the rights group', 'campaign organiser': 'the campaign',
    'founder of a movement': 'the movement',
}
SETTING_PLACE = {
    'household': 'the household', 'class': 'the class', 'work': 'the workplace', 'congregation': 'the congregation',
    'club': 'the club', 'scene': 'the scene', 'online': 'the online group', 'neighbours': 'the street', 'gang': 'the crew',
    'unit': 'the unit', 'ward': 'the ward', 'movement': 'the movement',
}
SPHERE_PLACE = dict(rule='the council', gather='the hall', arts='the company', faith='the congregation', care='the clinic',
                    learn='the school', prod='the works', comm='the business', prot='the station')

