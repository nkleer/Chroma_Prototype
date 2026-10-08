# Chroma content pack: Science, Research and Discovery (modern Earth). Catalogue: titles and perks.
# Pathways and packs thread, 2026-10-05. Draft for Emren's review. Source: Emren's "Science, Research & Discovery:
# expanded design v2" (roles in section 4, perks in section 7, color expressions in section 8); the document is
# inspiration, not a spec. Plain data in the fields of chroma-library/earth_perks_titles.py (its header defines every
# field); nothing is imported and nothing runs. The pack only adds: it reuses the base catalogue's [laboratory
# technician], [doctoral graduate], [graduate], [lab work], [working with data], [writing code], [finding things out],
# [archive research], [published research], [name in the field], [research grant], [mentor] and [public speaking]
# instead of repeating them. The reach ladder ([known across the country], [a household name]) is shared by every
# pathway pack and lives in chroma-packs/core/reach.py.
#
# Departures from Emren's document, on purpose:
#   - Perks carry ways. In Chroma a skill, standing or bond perk gives better odds to acts done in certain ways, so it
#     needs colors; they are balanced over the five colors. Emren's document keeps perks colorless.
#   - Method facets (bench, field, computational, archival, theoretical) are story notes on the title, not extra titles.
#   - A research project is an asset perk, [a research project under way], that the project's moments need (holds:)
#     and that ends when the project closes. The player's plan to finish it can sit on top (engine v7 plans).
#   - Appointments (postdoctoral researcher, professor) are colorless facets on the career title (engine refines),
#     as the document asks ("colorless appointment metadata"). The engine is asked to accept ways="" on a facet.
#
# Shares: share of people in a modern rich country who ever hold it. OECD Main Science and Technology Indicators: about
# 10 researchers per 1,000 people in work (full-time equivalents, about two in three of them in business R&D); OECD
# Education at a Glance: about 1.1 to 1.3 adults in 100 aged 25 to 64 hold a doctorate; Pew Research Center (2020): about
# 1 US adult in 10 took part in a citizen science activity in the past year. Everything else is an estimate.

# Round 5, 2026-10-07: the outer world's keywords (chroma-engine/world-fields.md, W38 and W40): sector= on every career,
# institution= (an at: value) and standing= (0 an ordinary person, 1 local, 2 inside power, 3 national; chroma-world
# spec-7 section 2) on every career and summit.
TITLES = []
PERKS = []

# ---------------------------------------------------------------- careers: the research pathway
TITLES += [
  dict(name="research assistant", kind="career", sector="knowledge", institution="university", standing=0, ways="W U",
       profiles=[("W U", "Delivers each assigned task to the standard the project needs, and learns why it matters."),
                 ("B", "Treats the post as a stepping stone and collects the skills and names that lead somewhere."),
                 ("R", "Throws themself into whatever the lab is chasing, hoping one question will catch fire.")],
       meets="need:competence+.06 need:meaning+.04 res:money+.03 res:time-.08 need:autonomy-.03",
       ages=(20, 67), share=.02,   # estimate: many science graduates hold a supervised research post for a year or
                                   # two; OECD counts about 10 researchers per 1,000 in work, plus their support staff
       say="a research assistant",
       gained="'a lab needs hands for the summer' or 'a research post you are half qualified for', usually after "
              "[graduate]; a supervisor who says yes",
       lost="the contract ending ('the contract runs out'); a step up to [research scientist]; a move into another "
            "field",
       needs="[graduate] in most settings, or years of [lab work] or [working with data]; a supervised appointment"),
  dict(name="research scientist", kind="career", sector="knowledge", institution="university", standing=0, ways="U",
       profiles=[("U", "Wants to understand, and refines the explanation until it survives every comparison."),
                 ("W U", "Builds evidence that other people can rely on when they have to decide."),
                 ("R G", "Investigates a place, a living thing or a tradition through years of close involvement.")],
       meets="need:competence+.1 need:meaning+.1 need:autonomy+.04 res:money+.06 res:time-.12",
       ages=(24, 80), share=.012,   # estimate: OECD about 10 researchers per 1,000 in work; about a third hold
                                    # research-scientist posts rather than R&D engineering; turnover over a career
       say="a research scientist",
       gained="a [doctoral graduate] taken on after 'the contract runs out'; years as a [research assistant] or a "
              "[laboratory technician] with 'learned a skill' many times and [published research]",
       lost="'leaving research for another life'; a step up; a contract that is not renewed and no other post",
       needs="usually [doctoral graduate]; sustained responsibility for questions and evidence, not a degree alone",
       turning="A careful result says the opposite of what the scientist hoped, and the grant report is due."),
  dict(name="research project lead", kind="career", sector="knowledge", institution="university", standing=1, ways="W B",
       profiles=[("W B", "Negotiates people, money and time for work that is valuable but easy to neglect."),
                 ("U R", "Tries unconventional designs and tests them carefully before anyone else dares."),
                 ("G", "Keeps the work, the people and the records whole through the project's seasons.")],
       meets="need:competence+.08 need:autonomy+.06 need:meaning+.06 res:money+.06 res:time-.14",
       ages=(27, 75), share=.005,   # estimate: about one research scientist in two leads a defined project at some time
       say="leading a research project",
       gained="a funded proposal ([research grant]) and an institution that puts them in charge of it; years as a "
              "[research scientist], [research software engineer] or [research data steward]",
       lost="the end of the project with no next one; a step up to [research group leader]; 'the work you would rather be "
            "doing' chosen over managing",
       needs="[research grant] or an assigned project; [a research project under way]"),
  dict(name="research group leader", kind="career", sector="knowledge", institution="university", standing=1, ways="W U B",
       profiles=[("W U B", "Builds a capable research group through standards, expertise and negotiation."),
                 ("W R G", "Shapes questions together with the people and places the research serves."),
                 ("B R", "Runs an independent agenda and strikes unconventional partnerships to keep it going.")],
       meets="need:autonomy+.08 need:competence+.06 need:meaning+.06 res:money+.08 res:time-.15 res:health-.02",
       ages=(30, 80), share=.002,   # estimate: about one research scientist in six leads a group of their own
       say="leading a research group",
       gained="'they want you to lead a group', after years of [published research] and a [research grant]; an "
              "institutional appointment or an equivalent responsibility",
       lost="the money running out with no new grant; stepping back to specialist work; retirement",
       needs="[research grant]; [published research] or [name in the field]; an institution that appoints them"),
  dict(name="research facility lead", kind="career", sector="knowledge", institution="university", standing=2, ways="W G",
       profiles=[("W G", "Keeps long-lived instruments and records running as a service to everyone who relies on them."),
                 ("B G", "Protects irreplaceable equipment and know-how, and keeps a specialist practice independent."),
                 ("U", "Keeps the machines at the edge of what they can measure, and teaches others how.")],
       meets="need:competence+.1 need:belonging+.04 need:meaning+.04 res:money+.06 res:time-.1",
       ages=(28, 70), share=.0005,   # estimate: shared facilities (microscopy, sequencing, telescopes, archives) are
                                     # few, each with one head
       say="running a research facility",
       gained="'the facility needs a head', after years as a [laboratory technician] or a [research scientist] with "
              "[instrument troubleshooting]",
       lost="the facility closing or merged; a move to a larger one; retirement",
       needs="[instrument troubleshooting] and years on the machines; the institution's appointment"),
  dict(name="independent investigator", kind="career", sector="knowledge", institution="charity", standing=1, ways="U B",
       profiles=[("U B", "Builds a scarce speciality and uses it to win the freedom to choose their own questions."),
                 ("R", "Follows a question they care about wherever it goes, on their own terms."),
                 ("B R G", "Sustains years of independent inquiry around a place or a system that matters to them.")],
       meets="need:autonomy+.12 need:meaning+.08 res:money-.04 res:time-.08 need:belonging-.04",
       ages=(25, 95), share=.0005,   # estimate: self-directed researchers with their own agenda, inside or outside an
                                     # institution
       say="an independent investigator",
       gained="'a fellowship of your own'; or savings, a grant or a patron and the nerve to go alone after 'nobody "
              "pays for this question'",
       lost="the money running out; an affiliation that brings back a boss; giving the question up",
       needs="the resources and permissions the work needs; [published research] or [a finding that held up] helps "
             "a great deal"),
]

# ---------------------------------------------------------------- careers: side roads of the research pathway
TITLES += [
  dict(name="research software engineer", kind="career", sector="knowledge", institution="university", standing=0, ways="U",
       profiles=[("U", "Builds reliable tools, because good questions die on bad software."),
                 ("U R", "Loves making things that work, and invents the tool nobody asked for yet."),
                 ("B", "Makes sure the tool everyone depends on is theirs, and keeps it the best there is.")],
       meets="need:competence+.1 need:autonomy+.04 res:money+.08 res:time-.1",
       ages=(20, 70), share=.002,   # estimate: a recent profession; national societies count a few thousand each
       say="a research software engineer",
       gained="'a research post you are half qualified for' with [writing code]; years as a [software developer] or "
              "a [data analyst] near a lab",
       lost="the project's money ending; a move back to industry",
       needs="[writing code]; a sustained appointment or an equivalent commitment"),
  dict(name="research data steward", kind="career", sector="knowledge", institution="university", standing=0, ways="W G",
       profiles=[("W G", "Keeps evidence documented and usable for people who are not born yet."),
                 ("G", "Knows the history of every column, the way a farmer knows each field."),
                 ("B", "Knows that whoever keeps good data shapes the conversation, and guards access well.")],
       meets="need:competence+.08 need:meaning+.05 res:money+.06 res:time-.08",
       ages=(22, 70), share=.001,   # estimate
       say="a research data steward",
       gained="'a research post you are half qualified for' with [working with data] or [archive research]; years "
              "as an [archivist] or a [data analyst]",
       lost="the post cut; a step up; a move into another field",
       needs="[working with data] or [archive research]"),
  dict(name="evidence synthesis specialist", kind="career", sector="knowledge", institution="university", standing=0, ways="W U",
       profiles=[("W U", "Compares the evidence in the open, so that shared decisions can rest on it."),
                 ("W R", "Feels bound to settle questions that matter, and works through the evidence with urgency."),
                 ("U B G", "Builds patient, durable methods and a long expertise few others have.")],
       meets="need:competence+.08 need:meaning+.06 res:money+.06 res:time-.08",
       ages=(24, 75), share=.0005,   # estimate
       say="an evidence synthesis specialist",
       gained="years as a [research scientist] or [research assistant] with [evidence synthesis]",
       lost="the post ending; a move into policy or teaching",
       needs="[evidence synthesis]; [graduate]"),
  dict(name="science communication specialist", kind="career", sector="knowledge", institution="media", standing=0, ways="R",
       profiles=[("R", "Shares the thrill of finding things out with anyone who will listen."),
                 ("W", "Gives the public accurate evidence and honest doubt, because people have a right to both."),
                 ("B", "Builds an audience and uses it to get science heard where decisions are made.")],
       meets="need:meaning+.08 need:belonging+.04 res:money+.04 res:time-.08 res:ties+.03",
       ages=(22, 75), share=.001,   # estimate: museums, press offices, science journalism and broadcasting
       say="a science communicator",
       gained="'leaving research for another life' with [explaining science]; a [journalist] who turns to science",
       lost="the post or the programme ending; a return to research",
       needs="[explaining science] or [public speaking]; sustained responsibility for accurate communication"),
  dict(name="participatory research coordinator", kind="career", sector="knowledge", institution="charity", standing=0, ways="G W",
       profiles=[("G W", "Grows questions together with a community over many years."),
                 ("R G", "Works alongside people out of love for the place and its life."),
                 ("U W", "Designs the work so that every volunteer's contribution counts as evidence.")],
       meets="need:belonging+.06 need:meaning+.08 res:money+.03 res:time-.1 res:ties+.04",
       ages=(22, 75), share=.0005,   # estimate
       say="coordinating a community research project",
       gained="a [volunteer research organiser] or a [research scientist] whose project becomes the job; 'a community "
              "proposes a better question'",
       lost="the money or the partnership ending",
       needs="[community listening]; a partnership the community agrees to"),
]

# ---------------------------------------------------------------- community: research as a pastime
# If the same work becomes the person's job, the career title takes over (Emren's document: never count it twice).
TITLES += [
  dict(name="citizen scientist", kind="community", ways="U R",
       profiles=[("U R", "Counts, measures and uploads, because finding things out is a thrill."),
                 ("G", "Watches one patch of the world closely through the seasons."),
                 ("W", "Adds to a shared record, because many careful hands make it reliable.")],
       meets="need:meaning+.04 need:competence+.03 res:time-.04",
       ages=(12, 100), share=.06,   # Pew Research Center 2020: about 1 US adult in 10 took part in a citizen science
                                   # activity in the past year; fewer keep at it for a season or more
       say="a citizen scientist",
       gained="'volunteers wanted to count what lives here' or 'a project online asks for a thousand pairs of eyes'",
       lost="the season ending and not coming back; no time any more",
       needs="nothing but time and attention; some projects ask for training"),
  dict(name="community observer", kind="community", ways="G W",
       profiles=[("G W", "Keeps the long record of one place, the way someone always has."),
                 ("B", "Gathers local evidence to give the neighbourhood a say against those who decide."),
                 ("R", "Is out at dawn every week because they love the river.")],
       meets="need:belonging+.04 need:meaning+.05 res:time-.05",
       ages=(12, 100), share=.02,   # estimate: long-term monitoring volunteers (weather stations, bird and butterfly
                                    # counts, river sampling)
       say="keeping a long record of one place",
       gained="'volunteers wanted to count what lives here', kept up for years; 'the same stretch of river, every "
              "Sunday'",
       lost="moving away; the body no longer up to the walk",
       needs="a place visited again and again"),
  dict(name="volunteer research organiser", kind="community", ways="W B",
       profiles=[("W B", "Organises volunteers and money so that the project outlasts its founders."),
                 ("U R", "Gets people excited about a question and designs a way they can help answer it."),
                 ("G", "Holds a circle of volunteers together the way a family holds together.")],
       meets="need:belonging+.05 need:meaning+.06 need:autonomy+.03 res:time-.08 res:ties+.03",
       ages=(18, 90), share=.003,   # estimate
       say="organising volunteer research",
       gained="years as a [citizen scientist] or [community observer]; 'a community proposes a better question'",
       lost="burning out; handing it on; the project folding",
       needs="[organising people] helps; volunteers willing to follow"),
]

# ---------------------------------------------------------------- facets: appointments, colorless (engine refines)
TITLES += [
  dict(name="postdoctoral researcher", kind="career", sector="knowledge", institution="university", standing=0, ways="", refines="research scientist",
       meets="need:autonomy-.03 res:money-.02 need:safety-.04", lasts=5,
       ages=(25, 45), share=.006,   # estimate: about half of science doctorates hold at least one fixed-term
                                    # postdoctoral post
       say="a postdoc",
       gained="the first years as a [research scientist] after [doctoral graduate], on fixed-term contracts",
       lost="a permanent post, a fellowship, or 'leaving research for another life'; it fades after five years",
       needs="[doctoral graduate]; a facet held on top of [research scientist], never in its place"),
  dict(name="professor", kind="career", sector="knowledge", institution="university", standing=2, ways="", refines="research scientist; research group leader",
       meets="need:safety+.04 need:competence+.03 res:time-.04",
       ages=(32, 80), share=.002,   # estimate: the UK has about 25,000 professors and the US about 180,000 full
                                    # professors at a time
       say="a professor",
       gained="an institution's appointment after years of [published research], teaching and [name in the field]",
       lost="retirement (an emeritus keeps the name in the story); leaving the institution",
       needs="[research scientist] or [research group leader]; a facet held on top, never in its place"),
]

# ---------------------------------------------------------------- perks: skills
PERKS += [
  dict(name="experimental design", kind="skill", ways="U R", odds=.05, skill_half=12, retires=None,
       ages=(18, 95), share=.01,   # estimate
       say="can design a sound experiment",
       gained="years as a [research assistant] or [research scientist]; 'a careful result that says no' taken "
              "seriously",
       lost="years away from research", needs="[lab work], [working with data] or [finding things out]"),
  dict(name="statistical judgment", kind="skill", ways="U B", odds=.05, skill_half=10, retires=None,
       ages=(18, 95), share=.02,   # estimate: researchers, analysts and some clinicians
       say="has a sound judgment for statistics",
       gained="[working with data] for years with [research scientist] or [data analyst]; a hard lesson from 'an "
              "error in your published work'",
       lost="years away from data", needs="[working with data]"),
  dict(name="instrument troubleshooting", kind="skill", ways="R U", odds=.04, skill_half=8, retires=None,
       ages=(18, 85), share=.01,   # estimate
       say="can bring a failing instrument back",
       gained="years at the bench as a [laboratory technician] or [research scientist]; 'the old instrument fails "
              "before the big run'",
       lost="years away from the machines", needs="[lab work]"),
  dict(name="fieldwork", kind="skill", ways="G R", odds=.05, skill_half=12, retires=None,
       ages=(16, 90), share=.01,   # estimate: field scientists, surveyors, long-term volunteers
       say="knows how to work in the field",
       gained="seasons outdoors as a [research scientist], [community observer] or [archaeologist]; 'the field "
              "season is lost' and saved",
       lost="years indoors; a body no longer up to it", needs="[knowing the woods] or [navigation] helps"),
  dict(name="qualitative interpretation", kind="skill", ways="G U", odds=.04, skill_half=12, retires=None,
       ages=(18, 100), share=.008,   # estimate: social and health researchers who interview and observe
       say="can read what people's accounts really say",
       gained="years of interviews and observation as a [research scientist] or [participatory research coordinator]",
       lost="years away from the work", needs="[community listening] or [counselling] helps"),
  dict(name="reproducible workflow", kind="skill", ways="W G", odds=.04, skill_half=8, retires=None,
       ages=(18, 90), share=.008,   # estimate
       say="keeps work that someone else can pick up and repeat",
       gained="a handover that worked; years as a [research software engineer] or [research data steward]",
       lost="years of careless habits", needs="[writing code] or [working with data]"),
  dict(name="evidence synthesis", kind="skill", ways="W U", odds=.04, skill_half=10, retires=None,
       ages=(20, 100), share=.004,   # estimate
       say="can weigh a whole field's evidence fairly",
       gained="years as an [evidence synthesis specialist], or as a [research scientist] writing reviews",
       lost="years away from the literature", needs="[finding things out]; [reader's ticket] helps"),
  dict(name="supervising researchers", kind="skill", ways="W G", odds=.05, skill_half=15, retires=None,
       ages=(25, 100), share=.006,   # estimate
       say="knows how to bring a young researcher on",
       gained="a junior who becomes independent ('a team member knows more than you now'); years as a [research "
              "group leader] or [professor]",
       lost="years without students", needs="[research scientist] or [research facility lead] for years"),
  dict(name="credit negotiation", kind="skill", ways="B W", odds=.04, skill_half=10, retires=None,
       ages=(20, 100), share=.006,   # estimate
       say="knows how to settle who gets the credit",
       gained="'whose name goes first' settled well; 'your name is not on the paper' fought out",
       lost="years out of shared work", needs="[research assistant] or a later research title"),
  dict(name="community listening", kind="skill", ways="G R", odds=.05, skill_half=12, retires=None,
       ages=(16, 100), share=.01,   # estimate: researchers, organisers and volunteers who work with communities
       say="listens to a community until it changes the question",
       gained="'a community proposes a better question' taken up; years as a [community observer] or "
              "[participatory research coordinator]",
       lost="years away from the people", needs="nothing but patience"),
  dict(name="grant writing", kind="skill", ways="B U", odds=.05, skill_half=6, retires=None,
       ages=(22, 90), share=.008,   # estimate
       say="can write a proposal that gets funded",
       gained="'the funding call closes on Friday' met, win or lose; [research grant] won",
       lost="years without writing one", needs="[graduate]; an institution, a charity or a patron to apply to"),
  dict(name="project triage", kind="skill", ways="B G", odds=.04, skill_half=10, retires=None,
       ages=(22, 100), share=.006,   # estimate
       say="knows when to stop a project and save what is good in it",
       gained="a project closed well ('the field season is lost', 'a careful result that says no'); years as a "
              "[research project lead]",
       lost="years without projects", needs="[a research project under way] at least once"),
  dict(name="explaining science", kind="skill", ways="R W", odds=.05, skill_half=8, retires=None,
       ages=(16, 100), share=.008,   # estimate
       say="can make a finding make sense to anyone",
       gained="public talks, school visits, a radio slot; years as a [science communication specialist]",
       lost="years without an audience", needs="[public speaking] helps"),
  dict(name="research integrity", kind="skill", ways="W", odds=.04, skill_half=15, retires=None,
       ages=(18, 100), share=.01,   # estimate
       say="handles data, claims and credit with care",
       gained="'pressure to say more than the data show' resisted; 'an error in your published work' corrected; "
              "'owned up' in research",
       lost="'hid a wrong' in research work", needs="a research title or [citizen scientist]"),
  dict(name="automating analysis", kind="skill", ways="B U", odds=.04, skill_half=4, retires=None,
       ages=(16, 90), share=.006,   # estimate
       say="can automate an analysis and check where it fails",
       gained="years as a [research software engineer]; [writing code] used on research data",
       lost="the tools moving on", needs="[writing code]"),
  dict(name="a nose for the odd result", kind="skill", ways="R G", odds=.04, skill_half=10, retires=None,
       ages=(12, 100), share=.01,   # estimate
       say="notices the result that does not fit",
       gained="'a careful result that says no' followed up; years of [fieldwork] or [lab work]; 'a curiosity that "
              "will not let go'",
       lost="years of routine", needs="nothing but attention"),
]

# ---------------------------------------------------------------- perks: access (odds 0; they work through requires:)
PERKS += [
  dict(name="institutional affiliation", kind="credential", ways="W B", odds=0, skill_half=None, retires=None,
       ages=(18, 90), share=.03,   # estimate: anyone with a post, a visiting status or a library card at a research
                                   # institution
       say="has an institution behind them",
       gained="a research title at a university, institute, museum or company; a visiting post",
       lost="the post ending; 'leaving research for another life'",
       needs="a research title, or an institution's agreement"),
  dict(name="ethics approval", kind="credential", ways="W U", odds=0, skill_half=None, retires=None,
       ages=(20, 90), share=.006,   # estimate
       say="has the approvals the study needs",
       gained="a study with people, animals or protected places approved by the committee",
       lost="the study ending; a breach",
       needs="[institutional affiliation] in most countries"),
  dict(name="field permit", kind="credential", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(18, 90), share=.005,   # estimate
       say="has permission to work on the site",
       gained="permission for the season from a landowner, a park or a government",
       lost="the season over; a broken condition",
       needs="a project and someone who grants it"),
  dict(name="instrument time", kind="asset", ways="U B", odds=0, skill_half=None, retires=None,
       ages=(20, 90), share=.006,   # estimate
       say="has time booked on the big machine",
       gained="a booking won at a shared facility; a [research grant] that pays for it",
       lost="'the instrument time you were promised' going to someone else; the booking over",
       needs="[institutional affiliation] and a project"),
  dict(name="a research project under way", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(16, 95), share=.03,   # estimate: researchers, plus volunteers and organisers who run a project of their own
       say="has a research project under way",
       gained="a funded proposal, an assigned project, or a question chased on one's own time",
       lost="the project closed: shared, abandoned, or 'the field season is lost' for good",
       needs="a question and some way to answer it"),
]

# ---------------------------------------------------------------- perks: standing and bonds
PERKS += [
  dict(name="a dataset others use", kind="standing", ways="G B", odds=.04, skill_half=20, retires=None,
       ages=(20, 110), share=.004,   # estimate
       say="has made a dataset others use",
       gained="careful records kept for years; 'an old dataset suddenly matters'",
       lost="the data lost or withdrawn", needs="[reproducible workflow] or years of [fieldwork]"),
  dict(name="a finding that held up", kind="standing", ways="W U", odds=.05, skill_half=20, retires=None,
       ages=(22, 110), share=.004,   # estimate
       say="made a finding that held up",
       gained="a result others repeated; 'a careful result that says no' that turned out right",
       lost="the finding overturned later", needs="[published research]"),
  dict(name="a method others use", kind="standing", ways="B R", odds=.05, skill_half=15, retires=None,
       ages=(22, 110), share=.002,   # estimate
       say="made a method others use",
       gained="a tool, a procedure or a piece of software adopted beyond their own group",
       lost="a better method replaces it", needs="[experimental design], [automating analysis] or "
                                                  "[instrument troubleshooting]"),
  dict(name="research collaborators", kind="bond", ways="U B", odds=.04, skill_half=6, retires=None,
       ages=(20, 100), share=.01,   # estimate
       say="has collaborators who share the work",
       gained="a project done together that worked; 'a collaboration that goes unusually well'",
       lost="a falling-out over credit; years apart", needs="a research title"),
  dict(name="former students", kind="bond", ways="U W", odds=.03, skill_half=10, retires=None,
       ages=(30, 110), share=.004,   # estimate
       say="has former students who still call",
       gained="[supervising researchers] for years; a junior who became independent",
       lost="years of silence", needs="[supervising researchers]"),
  dict(name="community partners", kind="bond", ways="G R", odds=.04, skill_half=6, retires=None,
       ages=(18, 100), share=.005,   # estimate
       say="has a community that works with them",
       gained="'a community proposes a better question' taken up; years as a [participatory research coordinator]",
       lost="a promise to the community broken", needs="[community listening]"),
  dict(name="a loyal research team", kind="bond", ways="B R", odds=.05, skill_half=4, retires=None,
       ages=(28, 95), share=.002,   # estimate
       say="has a team that would follow them anywhere",
       gained="years as a [research group leader] or [research project lead] with people who stay",
       lost="the team scattered; a broken promise to them", needs="[research group leader] or [research project lead]"),
]
