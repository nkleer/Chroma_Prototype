# ---------- volume 2, partner, children, community, faith and status (T2-046 to T2-100); facets (refines=) sit on
# the title they refine and take no slot
TITLES += [
  # ---------- partner: facets on [wife or husband], and one partnership of its own kind
  # T2-046
  dict(name="newlywed", kind="partner", ways="R", refines="wife or husband; married again",
       profiles=[("R", "Lives the first stretch of marriage as a joyful, expressive beginning."),
                 ("U", "Learns deliberately how the new shared arrangement actually works."),
                 ("G", "Grows into the wider family that the marriage joins to their own.")],   # third: Library
       meets="need:belonging+.03 need:meaning+.03 res:money-.03 res:time-.02", lasts=2,
       ages=(16, 110), share=.65,   # as [wife or husband] (first marriages): nearly every one begins with this stretch
       say="newly married",
       gained="'getting married', in a registry office or a hall full of cousins; the first year or two after the wedding",
       lost="settling into the ordinary [wife or husband] after a year or two; a separation; 'your partner dies'",
       needs="[wife or husband]; a facet held on top of it, never in its place"),
  # T2-047
  dict(name="caregiving partner", kind="partner", ways="W G", refines="wife or husband; living together; married again; partner of many years; nonromantic life partner",
       profiles=[("W G", "Makes continuing care part of an existing bond and shared life."),
                 ("B", "Protects the partner's agency while maintaining boundaries around their own capacity."),
                 ("R", "Keeps warmth and spontaneity alive in a shared life reshaped by care.")],   # third: Library
       meets="need:meaning+.05 need:belonging+.03 need:autonomy-.03 res:time-.12 res:money-.03 res:health-.03",
       lasts=10,
       ages=(18, 110), share=.15,   # estimate: 3 in 5 people become carers at some point (Carers UK), about 1 family
                                    # carer in 8 cares for a spouse or partner (AARP and NAC 2020), and most couples who
                                    # grow old together see one fall seriously ill; raised from .08 (2026-10-05 17:45)
       say="caring for their partner",
       gained="a partner needs sustained practical support after a stroke, an accident or a long illness, and help "
              "becomes daily care; taken by an act in a moment about a partner falling ill",
       lost="care needs changing, paid care or another arrangement taking over, a separation, 'your partner dies'",
       needs="[wife or husband], a willing partnership on both sides and a real ongoing care responsibility",
       turning="The help that was welcomed last month now feels intrusive. Love has to include another conversation."),
  # T2-048
  dict(name="nonromantic life partner", kind="partner", ways="W U",
       profiles=[("W U", "Builds a deliberate shared life through clear, mutually chosen responsibilities."),
                 ("G", "Experiences a lasting bond as the form of belonging that fits their lives."),
                 ("B", "Chooses a shared life on their own terms rather than the form others expect.")],   # third: Library
       meets="need:belonging+.08 need:safety+.05 need:autonomy-.05 res:money+.03",
       ages=(20, 110), share=.01,   # estimate
       say="in a nonromantic life partnership",
       gained="two close friends, often after years of sharing a flat or seeing each other through 'a long dark "
              "season', agree to build their lives together without romance",
       lost="ending or reshaping the partnership, 'falling in love' with someone else, a death",
       needs="two adults who both agree; age 20 or more; not a marriage, a tenancy or legal next of kin unless they "
             "arrange one",
       turning="A form offers only spouse, relative or friend. None quite describes the responsibilities they have "
               "chosen."),
  # T2-049
  dict(name="spouse in a family-arranged marriage", kind="partner", ways="G W", refines="wife or husband; married again",
       profiles=[("G W", "Finds a chosen partnership within an existing web of family relationships."),
                 ("B", "Negotiates the introduction and marriage as a deliberate personal decision.")],
       meets="need:belonging+.03 need:autonomy-.02 res:ties+.03",
       ages=(18, 110), share=.02,   # estimate: common in some communities, rare in most of the population
       say="married through a family introduction",
       gained="a family introduction, meetings with both families and then alone, and a marriage both adults freely "
              "choose: 'getting married'",
       lost="the marriage settling into another description such as [partner of many years], a separation, "
            "'your partner dies'",
       needs="[wife or husband]; a consensual adult marriage: an arranged introduction is not a forced marriage"),
  # T2-050
  dict(name="partner in a multigenerational household", kind="partner", ways="G B", refines="wife or husband; living together; married again; partner of many years",
       profiles=[("G B", "Combines household continuity with negotiated space for the couple's own life."),
                 ("U R", "Learns and experiments with ways of sharing a home across generations.")],
       meets="need:autonomy-.05 res:ties+.05 res:money+.03 res:time-.03",
       ages=(18, 110), share=.06,   # about 18% of Americans lived in a multigenerational home in 2021 (Pew), fewer in
                                    # most of Europe; estimate for a couple sharing a home with a parent
       say="in a multigenerational household",
       gained="'a parent comes to stay for a week' and stays, 'a parent who can no longer live alone' moves in, or "
              "the couple moves in with parents",
       lost="moving to a home of their own, a separation, the household changing when the older generation dies or "
            "moves into care",
       needs="[wife or husband] and a living parent under the same roof; who owns or rents the home is recorded "
             "separately"),

  # ---------- children: facets on [mother or father] and [grandparent], and one guardianship of its own kind
  # T2-051
  dict(name="parent of an only child", kind="children", ways="G U", refines="mother or father",
       profiles=[("G U", "Learns the particular child's needs without assuming one family pattern suits everyone."),
                 ("R", "Makes room for a close, expressive relationship and the child's growing individuality.")],
       meets="",   # Emren: it inherits the parenthood effects of [mother or father]
       ages=(16, 110), share=.15,   # about 1 US mother in 5 at the end of her childbearing years has one child (Pew
                                    # 2015); estimate
       say="the parent of an only child",
       gained="a few years after 'a child is born' with no brother or sister following, the one-child family becomes "
              "the way the household is described",
       lost="another child joining the family; parenthood itself remains",
       needs="[mother or father] with one child; no prediction about children to come"),
  # T2-052
  dict(name="parent of independent adult children", kind="children", ways="G", refines="mother or father",
       profiles=[("G", "Accepts that care continues while daily control and responsibility recede."),
                 ("U", "Learns a new relationship based on adult-to-adult communication."),
                 ("B R", "Reclaims the freedom and ambitions that years of daily parenting set aside.")],   # third: Library
       meets="need:autonomy+.05 res:time+.08",   # gives back part of the time [mother or father] still charges
       ages=(36, 110), share=.55,   # estimate: most parents see the youngest settled on their own
       say="the parent of grown-up children",
       gained="'the children leave home': the youngest settles on their own, and parenting becomes adult to adult",
       lost="a return to intensive care, another phase of parenting such as [grandparent]; the family history remains",
       needs="[mother or father] with no child at home who needs daily care",
       turning="The old advice is ready on the tongue. This time, the parent asks whether advice is wanted."),
  # T2-053
  dict(name="parent with a child living abroad", kind="children", ways="R G", refines="mother or father",
       profiles=[("R G", "Keeps affection and family roots alive across distance."),
                 ("W U", "Builds dependable arrangements for contact and practical responsibilities.")],
       meets="res:ties-.03 res:money-.03",
       ages=(36, 110), share=.08,   # estimate: emigrants are a few in 100 of the native-born in most rich countries
                                    # (OECD), and a parent of two or three has two or three chances
       say="a parent with a child abroad",
       gained="a grown child takes a job, a degree or a partner in another country; 'a long-planned trip' becomes a "
              "visit",
       lost="the child coming back, the parent moving to join them, a different care arrangement",
       needs="[mother or father] and a grown child living in another country"),
  # T2-054
  dict(name="home-educating parent", kind="children", ways="U R", refines="mother or father",
       profiles=[("U R", "Adapts learning through curiosity, experimentation and the child's interests."),
                 ("W", "Accepts a sustained educational responsibility and works to provide a dependable structure."),
                 ("B", "Takes charge of the child's education to pursue the opportunities the family judges best.")],
                 # third: Library
       meets="need:meaning+.05 need:belonging+.03 res:time-.12 res:money-.05", lasts=12,
       ages=(20, 70), share=.03,   # US: about 3 school-age children in 100 were home-schooled in 2019 (NCES), more
                                   # since 2020; about 1 in 100 in England; estimate
       say="a home-educating parent",
       gained="the household registers a home-education arrangement where the law allows it, after an unhappy spell "
              "at school, a move or a long-held wish, and the child has a say",
       lost="a return to school or college, the end of compulsory schooling, the responsibility passing to someone else",
       needs="[mother or father] with a child of school age at home; local eligibility and a real educational "
             "responsibility"),
  # T2-055
  dict(name="guardian of an unrelated child", kind="children", ways="W B",
       profiles=[("W B", "Accepts explicit responsibility while protecting the child's practical interests and "
                         "agency."),
                 ("G", "Builds continuity and belonging in a relationship not based on shared ancestry.")],
       meets="need:meaning+.1 need:autonomy-.03 res:time-.12 res:money-.05",
       ages=(21, 85), share=.003,   # estimate: far rarer than fostering or adoption
       say="a child's guardian",
       gained="named guardian in the will of a close friend, or appointed by a court under the rules of the setting; "
              "'you take in a child who needs a home'",
       lost="the guardianship ending, an adoption, another arrangement, the child growing up and setting out alone",
       needs="a recognised guardianship of a child who is not a relative; age 21 or more; distinct from [foster "
             "parent], [adoptive parent] and babysitting"),
  # T2-056
  dict(name="grandparent raising a grandchild", kind="children", ways="G W", refines="grandparent",
       profiles=[("G W", "Carries family continuity into a new period of daily care."),
                 ("B", "Uses experience and resources to protect the grandchild's future options.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.12 res:money-.05 res:health-.03", lasts=18,
       ages=(38, 90), share=.02,   # US: over 2 million grandparents are responsible for grandchildren living with
                                   # them (Census ACS); estimate
       say="raising a grandchild",
       gained="a grandchild comes to live with them for the long term, by a family arrangement or a kinship order; "
              "'you take in a child who needs a home'",
       lost="care passing back to a parent or to someone else, the grandchild growing up and leaving, another family "
            "arrangement",
       needs="[grandparent] and the daily care of the grandchild; legal authority is recorded separately",
       turning="The school gate is familiar, but the other parents belong to their children's generation."),
  # T2-057
  dict(name="parent coordinating complex support needs", kind="children", ways="W U", refines="mother or father",
       profiles=[("W U", "Coordinates services and routines so a child's actual needs are met."),
                 ("B R", "Advocates firmly and creatively when standard arrangements fail the child.")],
       meets="need:meaning+.05 need:autonomy-.03 res:time-.1 res:money-.05",
       ages=(16, 100), share=.05,   # England: about 5 pupils in 100 have an education, health and care plan (DfE
                                    # 2024); estimate
       say="coordinating a child's support",
       gained=("an assessment or a diagnosis is followed by years of plans, appointments and meetings with the school "
               "and other services, where [handling red tape] is learned the hard way"),
       lost="the needs changing, the coordination passing to someone else, an adult child taking charge with the "
            "right support",
       needs="[mother or father] and substantial real coordination work; the condition of the child carries no color"),
  # T2-058
  dict(name="parent raising a child across languages", kind="children", ways="G R", refines="mother or father",
       profiles=[("G R", "Makes multiple languages part of family belonging and everyday expression."),
                 ("U", "Learns how to support the child's changing use and understanding of languages."),
                 ("B", "Treats each language as an advantage the child will carry into later life.")],   # third: Library
       meets="need:meaning+.03 res:ties+.03 res:time-.03",
       ages=(16, 80), share=.1,   # US: about 1 child in 5 speaks a language other than English at home (Census
                                  # ACS); estimate for an active practice
       say="raising a child in more than one language",
       gained="a household keeps two or more languages alive in bedtime stories, calls with the grandparents and "
              "weekend classes; [second language] or [family abroad] helps",
       lost="the practice fading, the child growing up and leaving home, another description of the parenting "
            "coming to matter more",
       needs="[mother or father] with a child at home and an active practice, not only parents of different "
             "nationalities"),

  # ---------- community: up to three at once ([club member] stays the generic adult club)
  # T2-059
  dict(name="choir member", kind="community", sphere="arts", face="arts.W", ways="W G",
       profiles=[("W G", "Sustains a shared musical practice through belonging and preparation."),
                 ("B", "Develops a chosen public voice and a place beyond their usual social role.")],
       meets="need:belonging+.08 need:meaning+.03 res:time-.05",
       ages=(8, 100), share=.12,   # UK: about 2.1 million people sing in some 40,000 choirs (Voices Now 2017);
                                   # estimate for ever, school choirs included
       say="in a choir",
       gained="an audition or an open rehearsal on a weeknight leads to regular membership: a school, church or "
              "community choir",
       lost="leaving, a move ('moved away'), the choir closing",
       needs="a willing ensemble and whatever audition in [singing] it asks",
       turning="The newest member has a beautiful voice but keeps rushing the shared phrase. The choir has to make "
               "room without losing each other."),
  # T2-060
  dict(name="community-garden coordinator", kind="community", ways="G U",
       profiles=[("G U", "Learns what the place and its growers need over time."),
                 ("W B", "Negotiates plots and responsibilities so a shared resource remains workable.")],
       meets="need:meaning+.05 need:belonging+.05 res:time-.08",
       ages=(18, 90), share=.01,   # estimate
       say="the community garden's coordinator",
       gained="the garden members ask them to coordinate the next season, often after years of 'tending an allotment'",
       lost="handing over at the yearly meeting, a move, the landowner withdrawing permission for the site",
       needs="a mandate from the members and access to the garden; [growing food] helps"),
  # T2-061
  dict(name="repair-cafe volunteer", kind="community", sphere="learn", face="learn.R", ways="U W",
       profiles=[("U W", "Makes practical knowledge useful to others through reliable help."),
                 ("R G", "Enjoys the encounter with a stubborn object and the person who brought it.")],
       meets="need:meaning+.05 res:ties+.05 res:time-.05",
       ages=(16, 90), share=.005,   # estimate: some thousands of repair cafes worldwide, most in the Netherlands,
                                    # Germany, Belgium and Britain
       say="a repair-cafe volunteer",
       gained="a monthly repair event in the library or a church hall becomes a regular commitment",
       lost="stepping back, the venue closing, a move",
       needs="[fixing things], [sewing and mending] or another repair skill, and the agreed limits of the group"),
  # T2-062
  dict(name="amateur astronomer in a club", kind="community", sphere="learn", face="learn.U", ways="U",
       profiles=[("U", "Shares careful observation and persistent questions."),
                 ("R G", "Joins because looking at the night sky feels astonishing and grounding.")],
       meets="need:meaning+.05 need:belonging+.03 need:competence+.03 res:time-.05 res:money-.02",
       ages=(10, 100), share=.005,   # estimate
       say="an amateur astronomer",
       gained="a public observing evening, 'more stars than anyone could count' or 'the sun goes dark at noon' leads "
              "to joining a club",
       lost="leaving, a move, the club winding down",
       needs="membership and access to observing sessions; a [good telescope] helps but is not required"),
  # T2-063
  dict(name="historical reenactment member", kind="community", sphere="arts", face="arts.G", ways="G W",
       profiles=[("G W", "Keeps a shared practice alive through craft and group responsibilities."),
                 ("B R", "Uses performance to try an expressive identity far from everyday work.")],
       meets="need:belonging+.08 need:autonomy+.03 res:money-.03 res:time-.05",
       ages=(14, 85), share=.004,   # estimate
       say="a historical reenactor",
       gained="a public event at a castle or an old battlefield leads to joining a group, its drill and its sewing "
              "evenings",
       lost="leaving, interests changing, the group closing",
       needs="a place in the group, [period kit] and the safety arrangements its events require",
       turning="Someone asks whether the costume is accurate. Someone else asks whose history never gets "
               "represented."),
  # T2-064
  dict(name="community-radio presenter", kind="community", ways="R U",
       profiles=[("R U", "Explores ideas and voices through an expressive format."),
                 ("W", "Provides dependable local information that larger broadcasters overlook."),
                 ("B", "Builds a voice and a following of their own outside the larger stations.")],   # third: Library
       meets="need:meaning+.05 need:competence+.03 res:ties+.03 res:time-.05",
       ages=(16, 90), share=.004,   # estimate; a paid presenter holds a career instead
       say="a community-radio presenter",
       gained="a trial programme on the local station becomes a regular weekly slot",
       lost="the slot ending, the station closing, stepping back",
       needs="the approval of the station and its production training; [public speaking] helps",
       turning="A neighbour with no broadcasting experience tells a story nobody else in town has covered."),
  # T2-065
  dict(name="community-mediation volunteer", kind="community", sphere="rule", face="rule.G", ways="W U",
       profiles=[("W U", "Helps people understand a dispute and find an accountable process."),
                 ("G", "Protects the possibility of living alongside each other after the dispute.")],
       meets="need:meaning+.05 need:competence+.03 res:time-.05 res:health-.02",
       ages=(21, 85), share=.004,   # estimate
       say="a volunteer mediator",
       gained="a training course in [settling disputes] leads to supervised mediation of disputes between neighbours",
       lost="leaving the service, no longer meeting its suitability rules, the service closing",
       needs=("mediation training ([mediation accreditation]), impartiality and a recognised service; [calming people "
              "down]")),
  # T2-066
  dict(name="search-and-rescue volunteer", kind="community", sphere="care", face="care.R", ways="W R",
       profiles=[("W R", "Accepts preparation and teamwork for moments requiring decisive help."),
                 ("U", "Finds commitment in mastering a demanding coordinated practice."),
                 ("B G", "Tests their own endurance against terrain and weather they know closely.")],   # third: Library
       meets="need:meaning+.08 need:belonging+.05 res:time-.08 res:health-.02",
       ages=(18, 70), share=.003,   # estimate
       say="a search-and-rescue volunteer",
       gained="selection, a probationary year and training lead to a place in a recognised mountain, cave or lowland "
              "rescue team",
       lost="stepping back, a move, no longer meeting the fitness and readiness rules",
       needs=("team-specific skills ([navigation], [emergency care]) and authorisation; [first-aid certificate]; good "
              "health")),
  # T2-067
  dict(name="lifeboat volunteer", kind="community", sphere="care", face="care.R", ways="W G",
       profiles=[("W G", "Protects a coastal community through dependable service."),
                 ("B R", "Chooses a demanding practical commitment that gives life personal direction.")],
       meets="need:meaning+.08 need:belonging+.05 need:safety-.02 res:time-.08",
       ages=(17, 65), share=.002,   # estimate: the British and Irish lifeboat service has about 5,000 volunteer crew
                                    # (RNLI); a lifeboat station is needed
       say="lifeboat crew",
       gained="a coastal rescue station recruits and trains them; the pager goes on the first night",
       lost="leaving, moving inland, losing operational eligibility through age or health",
       needs=("selection, sea training ([boat handling], [sea survival certificate]) and operational authorisation; "
              "[swimming]; living near the station")),
  # T2-068
  dict(name="school-governance board member", kind="community", sphere="learn", face="learn.W", ways="W U",
       profiles=[("W U", "Reviews decisions and responsibilities affecting a school community."),
                 ("B G", "Protects a school's local continuity while negotiating resources.")],
       meets="need:meaning+.05 res:ties+.03 res:time-.05",
       ages=(18, 85), share=.02,   # England has about 250,000 school governors and trustees (National Governance
                                   # Association); estimate for ever
       say="a school governor",
       gained="a parent election or a community appointment brings a seat on the board of a school",
       lost="the term ending, resigning, removal",
       needs=("eligibility, with [cleared to work with children], and formal appointment; often a child at the school "
              "or [good name in town]")),
  # T2-069
  dict(name="parent-association organiser", kind="community", ways="R W",
       profiles=[("R W", "Turns concern for children into shared practical action."),
                 ("U B", "Makes the association effective by understanding constraints and building leverage.")],
       meets="need:belonging+.05 need:meaning+.05 res:time-.05",
       ages=(18, 70), share=.04,   # estimate
       say="running the parents' association",
       gained="other parents at the school gate ask them to organise the year: the summer fair, the quiz night, the "
              "coat drive",
       lost="handing over, the children changing schools or growing up, the group ending",
       needs="a child at the school and a recognised role in the group; not a governance mandate"),
  # T2-070
  dict(name="housing-cooperative member", kind="community", sphere="comm", face="comm.G", ways="G W",
       profiles=[("G W", "Shares responsibility for a place to live over the long term."),
                 ("U B", "Uses collective ownership or governance to gain practical control through informed "
                         "decisions.")],
       meets="need:belonging+.05 need:autonomy+.03 res:money-.03 res:time-.03",
       ages=(18, 110), share=.04,   # estimate: cooperative housing is common in Scandinavia and parts of Germany and
                                    # Switzerland, rare in Britain and the US
       say="a member of a housing cooperative",
       gained="they buy a share or come up the waiting list, move in, and take on the duties of membership: meetings, "
              "a rota, a vote on the budget",
       lost="selling or giving up the membership, a move, the cooperative dissolving",
       needs="actual membership and whatever housing and financial conditions the cooperative sets",
       turning="The roof needs money now; three households cannot afford the proposed contribution."),
  # T2-071
  dict(name="sports referee", kind="community", sphere="gather", face="gather.W", ways="W",
       profiles=[("W", "Keeps a contest workable through consistent judgment."),
                 ("R", "Loves the live pace and the challenge of responding clearly in the moment.")],
       meets="need:competence+.05 need:belonging-.02 res:ties+.03 res:time-.05",
       ages=(14, 75), share=.02,   # estimate: most who earn the referee's badge officiate for a while; a paid
                                   # referee holds a career instead
       say="a referee",
       gained="the course for [referee's badge], then regular appointments to youth and amateur fixtures",
       lost="stopping appointments, the badge lapsing, interests changing; the knees go",
       needs="[referee's badge] and the approval of the competition"),
  # T2-072
  dict(name="festival organiser", kind="community", sphere="gather", face="gather.G", ways="R U",
       profiles=[("R U", "Invents an occasion that brings different experiences together."),
                 ("W B", "Makes a public celebration feasible through agreements, budgets and clear "
                         "responsibilities.")],
       meets="need:meaning+.05 need:belonging+.05 res:time-.08",
       ages=(16, 85), share=.01,   # estimate
       say="a festival organiser",
       gained="the planning group behind 'a festival comes to town' or the yearly street party gives them an ongoing "
              "organising role",
       lost="handing over, cancellation, 'burnout'",
       needs="an actual mandate and the event permissions the council requires"),
  # T2-073
  dict(name="amateur band member", kind="community", sphere="arts", face="arts.R", ways="R",
       profiles=[("R", "Shares direct expression and the pleasure of making music together."),
                 ("U", "Builds music through arrangements, constraints and systematic rehearsal.")],
       meets="need:belonging+.05 need:autonomy+.05 res:time-.05 res:money-.02",
       ages=(12, 90), share=.08,   # estimate
       say="in a band",
       gained="'a band or a sport that takes over your life': a rehearsal in a garage becomes a continuing place in "
              "the band",
       lost="leaving, the band splitting, a move",
       needs="[musical instrument] or [singing], and a willing group"),
  # T2-074
  dict(name="book-club organiser", kind="community", sphere="gather", face="gather.U", ways="U G",
       profiles=[("U G", "Helps people understand books in the context of their lives."),
                 ("B", "Creates a space for independent judgment beyond established cultural gatekeepers."),
                 ("R", "Picks books that spark strong feelings and lively argument.")],   # third: Library
       meets="need:meaning+.05 res:ties+.05 res:time-.03",
       ages=(16, 95), share=.02,   # estimate
       say="the book club's organiser",
       gained="they start arranging the monthly meetings and choosing the books, in a front room, a library or a cafe",
       lost="handing over, the group ending, a move",
       needs="willing readers and a recurring organising role"),
  # T2-075
  dict(name="community-kitchen volunteer", kind="community", sphere="gather", face="gather.W", ways="W G",
       profiles=[("W G", "Makes nourishment a reliable shared practice."),
                 ("B R", "Builds a practical space where people can contribute and eat on their own terms.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.05 res:health-.02",
       ages=(16, 90), share=.03,   # estimate
       say="a community-kitchen volunteer",
       gained="a meal service or a food bank takes them onto its weekly rota, often after 'a volunteer drive in your "
              "neighbourhood'",
       lost="stepping back, the service closing, another commitment taking priority",
       needs="an induction, food-safety training ([food hygiene certificate]) and agreed duties"),
  # T2-076
  dict(name="neighbourhood-watch coordinator", kind="community", sphere="prot", face="prot.G", ways="W U",
       profiles=[("W U", "Organises clear, proportionate information-sharing and reporting."),
                 ("G", "Cares about familiar neighbours and everyday continuity.")],
       meets="need:safety+.03 res:ties+.03 res:time-.03",
       ages=(21, 90), share=.015,   # estimate
       say="the neighbourhood-watch coordinator",
       gained="after 'break-ins on the street', residents ask them to coordinate an agreed local scheme",
       lost="handing over, a move, the scheme ending",
       needs="a recognised community role with clear limits; no police authority"),
  # T2-077
  dict(name="prison visitor", kind="community", ways="G W",
       profiles=[("G W", "Maintains human connection across a setting that separates people from ordinary life."),
                 ("B", "Supports a person's continuing agency and identity beyond their conviction.")],
       meets="need:meaning+.08 res:ties+.02 res:time-.03",
       ages=(21, 85), share=.002,   # estimate
       say="a prison visitor",
       gained="a recognised visiting scheme accepts them after checks and training",
       lost="the arrangement ending, withdrawing, a move",
       needs="the approval of the prison, training and the agreement of the person visited",
       turning="A conversation about an ordinary television programme matters because almost every other "
               "conversation has been about the person's case."),
  # T2-078
  dict(name="board-game club organiser", kind="community", sphere="gather", face="gather.U", ways="U R",
       profiles=[("U R", "Designs a varied shared experience through rules, discovery and play."),
                 ("W", "Makes the club dependable and welcoming through fair practical arrangements.")],
       meets="need:belonging+.05 need:meaning+.03 res:time-.05 res:money-.02",
       ages=(14, 90), share=.01,   # estimate
       say="running a board-game club",
       gained="a recurring game night in a cafe or the back room of a pub grows into an organised club",
       lost="handing over, the venue closing, the club dispersing",
       needs="willing players, a venue or an online space, and a continuing role",
       turning="An experienced player wants a demanding game; the newcomer has never touched a rulebook. The evening "
               "needs a place for both."),

  # ---------- faith and causes: one at a time; paid ministry stays here
  # T2-079
  dict(name="ordained religious minister", kind="faith", sphere="faith", face="faith.W", ways="W G",
       profiles=[("W G", "Sustains shared ritual and care within a continuing tradition."),
                 ("U", "Treats interpretation and difficult questions as a lifelong responsibility."),
                 ("R", "Leads worship and pastoral care through felt conviction and personal presence.")],
                 # third: Library
       meets="need:meaning+.12 need:belonging+.05 need:autonomy-.05 res:ties+.05 res:time-.1 res:money+.08",
       ages=(23, 85), share=.004,   # estimate: clergy are a few workers in 1,000
       say="a minister of religion",
       gained=("years of training ([leading a ceremony]) and the community's own process of discernment lead to "
               "ordination and a recognised ministry"),
       lost="retirement, leaving ministry, the tradition withdrawing its recognition",
       needs="[regular worshipper] or [convert] for years; [scripture]; the recognition and requirements of the "
             "tradition, often with [graduate]"),
  # T2-080
  dict(name="member of a monastic community", kind="faith", sphere="faith", face="faith.U", ways="W G",
       profiles=[("W G", "Orders daily life around shared spiritual practice and continuity."),
                 ("B", "Freely chooses a demanding life that rejects a socially expected route to status or "
                       "consumption.")],
       meets="need:meaning+.12 need:belonging+.1 need:autonomy-.1 res:time-.1 res:freedom-.05",
       ages=(18, 110), share=.001,   # estimate
       say="a member of a monastic community",
       gained="a period of discernment, stays as a guest, then years as a novice before accepted membership",
       lost="leaving, moving to another community, death",
       needs="voluntary adult participation and the admission process of the community; usually no partner and no "
             "children at home",
       turning="The quiet life still contains washing up, disagreement and a person whose habits are difficult to "
               "bear."),
  # T2-081
  dict(name="lay religious teacher", kind="faith", sphere="faith", face="faith.U", ways="W U",
       profiles=[("W U", "Helps others understand a tradition with care and consistency."),
                 ("R", "Teaches through stories, feeling and vivid connection to ordinary life."),
                 ("G", "Passes the tradition on as it was handed down, within the shared life of the community.")],
                 # third: Library
       meets="need:meaning+.08 need:competence+.05 res:ties+.03 res:time-.05",
       ages=(16, 90), share=.03,   # estimate
       say="a lay teacher of the faith",
       gained="the congregation asks them to lead a recurring class: Sunday school, a study group, weekend lessons "
              "for the children",
       lost="stepping down, a change in faith, the class ending",
       needs="[regular worshipper] for some years; [scripture] or [teaching]; recognition by the community; distinct "
             "from [teacher]"),
  # T2-082
  dict(name="congregation musician", kind="faith", sphere="faith", face="faith.R", ways="R W",
       profiles=[("R W", "Gives shared belief an expressive public form."),
                 ("U", "Develops the musical structure and technique that let others participate.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.05",
       ages=(12, 90), share=.02,   # estimate
       say="the congregation's musician",
       gained="a regular place at the organ, in the band or leading the singing replaces occasional help",
       lost="stepping back, a move to another congregation, leaving the role",
       needs="[musical instrument] or a trained voice ([singing]), and the agreement of the congregation",
       turning="A familiar song no longer fits the occasion. Changing it may feel like care to some and loss to "
               "others."),
  # T2-083
  dict(name="interfaith-dialogue participant", kind="faith", sphere="faith", face="faith.U", ways="W U",
       profiles=[("W U", "Builds careful understanding across differences without demanding agreement."),
                 ("R G", "Values the lived encounter, hospitality and unfamiliar practices of other communities.")],
       meets="need:meaning+.05 need:safety-.02 res:ties+.05 res:time-.03",
       ages=(16, 95), share=.01,   # estimate
       say="in an interfaith dialogue circle",
       gained="a dialogue circle between local congregations, begun with a shared meal or a vigil, becomes a "
              "continuing commitment",
       lost="leaving, the circle ending, another commitment",
       needs="a faith held for some years, voluntary participation and a recurring group"),
  # T2-084
  dict(name="animal-shelter campaigner", kind="faith", ways="G W",
       profiles=[("G W", "Works for durable responsibility toward animals in human care."),
                 ("B R", "Turns fierce personal concern into independent organising and fundraising.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.05 res:money-.02",
       ages=(14, 95), share=.02,   # estimate
       say="an animal-shelter campaigner",
       gained="repeated help at the shelter after 'a stray dog follows you home' or 'a pet of your own' grows into "
              "fundraising and campaigning",
       lost="the campaign ending, stepping back, a change of cause",
       needs="a real campaign role; handling the animals needs its own training ([handling animals])"),
  # T2-085
  dict(name="disability-rights organiser", kind="faith", ways="W B",
       profiles=[("W B", "Combines collective rights with individual control over one's life."),
                 ("U R", "Develops new forms of access and challenges assumptions through creative campaigning.")],
       meets="need:meaning+.08 need:autonomy+.03 res:time-.05 res:health-.02",
       ages=(16, 95), share=.01,   # estimate
       say="a disability-rights organiser",
       gained=("a barrier met after 'a serious accident or illness', 'living with a chronic illness' or in caring "
               "for someone leads to organising and [campaigning]"),
       lost="handing over, leaving the group, other commitments",
       needs="a recognised role in the cause and accountable participation; no disability status is required"),
  # T2-086
  dict(name="civil-liberties campaigner", kind="faith", ways="W B",
       profiles=[("W B", "Defends rights that protect people from arbitrary interference."),
                 ("R", "Acts because suppressed expression or constrained freedom feels intolerable.")],
       meets="need:meaning+.08 need:safety-.03 res:ties+.03 res:time-.05",
       ages=(16, 95), share=.01,   # estimate
       say="a civil-liberties campaigner",
       gained="'a sense of injustice' over one case, a protest or 'a bitter election' becomes a sustained campaign",
       lost="a campaign ending, 'burnout', a change of cause",
       needs="an actual group or an ongoing independent campaign",
       turning="The person whose right they are defending holds views they strongly dislike."),
  # T2-087
  dict(name="restorative-justice advocate", kind="faith", ways="G U",
       profiles=[("G U", "Seeks ways for repair to fit the actual people and context."),
                 ("R W", "Combines emotional recognition with obligations that make repair credible.")],
       meets="need:meaning+.08 need:belonging+.03 res:ties-.02 res:time-.05",
       ages=(18, 95), share=.005,   # estimate
       say="a restorative-justice advocate",
       gained="study, a court case close to home, a past as [someone with a record] or being 'robbed or attacked "
              "in the street' leads to a sustained advocacy role",
       lost="leaving the cause, handing over, a change of approach",
       needs=("a cause commitment; facilitating a formal meeting needs separate training in [settling disputes] "
              "([mediation accreditation]) and the consent of everyone involved")),
  # T2-088
  dict(name="digital-rights advocate", kind="faith", ways="U B",
       profiles=[("U B", "Understands systems to protect practical agency and control over personal information."),
                 ("W G", "Defends the continuity of shared digital resources people depend on.")],
       meets="need:meaning+.05 need:competence+.05 res:time-.05",
       ages=(16, 95), share=.005,   # estimate
       say="a digital-rights advocate",
       gained="'your name in the leaked files', a new surveillance scheme or a technology decision leads to "
              "sustained public-interest work",
       lost="stepping back, a change of cause, the group closing",
       needs="an ongoing cause role; [writing code] helps, but technical authority is not automatic",
       turning="The convenient new platform would make a volunteer group's work easier, but nobody knows who can keep "
               "its records."),

  # ---------- status: no colors, no destiny; any number at once
  # T2-089
  dict(name="doctoral graduate", kind="status", ways="",
       meets="need:competence+.03", lasts="life",   # only what it adds: [graduate] stays beside it with its own bonus
       ages=(24, 110), share=.01,   # about 1 adult in 100 aged 25 to 64 holds a doctorate across the OECD (OECD,
                                    # Education at a Glance)
       say="a doctoral graduate",
       gained="three to six years of research after a first degree, an examined thesis, then 'earning a qualification'",
       lost="never; a legal invalidation would be its own event",
       needs="[graduate]; the actual award of the doctorate, not only the study"),
  # T2-090
  dict(name="first-generation university student", kind="status", ways="",
       meets="need:meaning+.03 need:competence-.02", lasts=6,   # only while studying; 6 caps it
       ages=(17, 30), share=.15,   # US: 56% of undergraduates in 2015-16 had no parent with a bachelor's degree (RTI
                                   # for NASPA); estimate for ever
       say="the first in the family at university",
       gained="enrolment at a university when neither parent holds a degree; 'you win a scholarship or a place'",
       lost="graduating ([graduate]) or leaving the course; the history remains",
       needs="actual enrolment and a [school-leaving certificate]; first generation here means no parent with a "
             "university degree"),
  # T2-091
  dict(name="former foster child", kind="status", ways="",
       meets="", lasts="life",
       ages=(1, 110), share=.03,   # US: about 6 children in 100 are placed in foster care before 18 (Wildeman and
                                   # Emanuel 2014); fewer in most of Europe; estimate
       say="a former foster child",
       gained="'going into foster care' in childhood, which ends with a return home, an adoption, a guardianship or "
              "leaving care as a young adult",
       lost="never; it is a fact of their history",
       needs="a recorded foster placement in childhood"),
  # T2-092
  dict(name="adopted person", kind="status", ways="",
       meets="", lasts="life",
       ages=(0, 110), share=.02,   # about 2 children in 100 in the US are adopted (US Census 2010)
       say="adopted",
       gained="an adoption in childhood, by new parents, a stepparent or relatives, as the law of the setting defines it",
       lost="never; it is a fact of their history",
       needs="a recorded adoption; distinct from being an [adoptive parent]"),
  # T2-093
  dict(name="refugee", kind="status", ways="",
       meets="", lasts="life",
       ages=(0, 110), share=.01,   # estimate: refugees are a few residents in 100 in Germany and Sweden, far fewer in
                                   # most rich countries (UNHCR)
       say="a refugee",
       gained="protection granted on a claim for asylum ([asylum applicant]), or resettlement through a refugee "
              "programme",
       lost="the legal status changing, usually with [citizenship]; the history of displacement remains",
       needs="an actual status decision; [immigrant] comes with it"),
  # T2-094
  dict(name="asylum applicant", kind="status", ways="",
       meets="need:safety-.05 res:freedom-.03", lasts=5,   # only while the claim is pending; 5 caps it
       ages=(0, 110), share=.015,   # estimate
       say="seeking asylum",
       gained="arrival after 'war comes' or persecution at home ('moved away'), and a claim for protection lodged with "
              "the authorities",
       lost="a decision ([refugee] or a refusal), a withdrawal, another procedural outcome",
       needs="a lodged application still under consideration"),
  # T2-095
  dict(name="naturalised citizen", kind="status", ways="",
       meets="", lasts="life",   # legal access is applied once, by [citizenship]
       ages=(5, 110), share=.08,   # as [citizenship]: the two come together (next version: .06 to .08, change-later.md)
       say="a naturalised citizen",
       gained="years of residence, a test on the history and laws, and an oath at a ceremony; [citizenship] comes with "
              "it",
       lost="almost never; current citizenship is tracked by [citizenship]",
       needs="[immigrant] and a completed grant of [citizenship]"),
  # T2-096
  dict(name="bankruptcy or insolvency in their history", kind="status", ways="",
       meets="", lasts="life",
       ages=(18, 110), share=.06,   # England and Wales: about 1 adult in 400 becomes insolvent each year (Insolvency
                                    # Service, 2023); estimate for ever
       say="someone who has been through bankruptcy",
       gained="'financial ruin': a bankruptcy, a debt relief order or an insolvency arrangement completed through the "
              "courts or an official process",
       lost="never as history; the active restrictions end when the process discharges",
       needs="a recorded formal process; ordinary debt is not enough"),
  # T2-097
  dict(name="on probation or community supervision", kind="status", ways="",
       meets="res:freedom-.05 res:time-.03", lasts=3,   # only while the order runs; 3 caps it
       ages=(10, 110), share=.04,   # US: about 1 adult in 70 was on probation at the end of 2021 (BJS); fewer in
                                    # Europe; estimate for ever
       say="on probation",
       gained="a court order after a conviction ([someone with a record]) or release from prison on licence "
              "([ex-prisoner]): appointments, conditions, unpaid work",
       lost="completing the order, an amendment, revocation or another legal outcome",
       needs="an actual order with stated conditions"),
  # T2-098
  dict(name="living in residential care", kind="status", ways="",
       meets="need:safety+.05 res:money-.05", lasts="life",
       ages=(18, 110), share=.15,   # estimate: about 1 death in 5 in England and Wales takes place in a care home (ONS)
       say="living in a care home",
       gained="'moving to a smaller home or into care': a residential home, a nursing home or supported housing with "
              "care on site",
       lost="moving elsewhere, another support arrangement, death",
       needs="actual residence and a defined arrangement for support"),
  # T2-099
  dict(name="returned migrant", kind="status", ways="",
       meets="res:ties+.03 res:money-.02", lasts=3,   # the return phase; the migration history remains
       ages=(18, 110), share=.05,   # estimate
       say="back home after years abroad",
       gained="after years abroad ('moved away'), a move back ('came home') to a country once regarded as home; "
              "'roots call the one who moved away'",
       lost="the return settling into ordinary life; the migration history remains",
       needs="a real return after a substantial spell abroad"),
  # T2-100
  dict(name="displaced by a disaster", kind="status", ways="",
       meets="need:safety-.08 res:money-.05 res:ties-.03", lasts=5,   # until a stable arrangement; 5 caps it
       ages=(0, 110), share=.04,   # estimate: the US Census Household Pulse Survey counts a few million adults
                                   # displaced by disasters each year, most of them for under a month
       say="displaced by a disaster",
       gained="a flood, a fire, a storm or 'war comes' leaves the home unsafe or unusable: 'losing the home'",
       lost="a safe return, a settled new home, another stable arrangement; the event stays in their history",
       needs="a real displacement, not only living near 'a disaster in the next town'"),
]


