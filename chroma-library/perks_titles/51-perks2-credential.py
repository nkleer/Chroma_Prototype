# ---------- volume 2, credential: a licence, a certificate or a paper; it can be suspended or taken, and the skill under it stays
PERKS += [
  dict(name="airline pilot licence", kind="credential", ways="U W", odds=0, skill_half=10, retires=65,
       ages=(19, 65), share=.0015,   # the US counts about a quarter of a million holders of commercial and airline
                                     # transport pilot certificates (FAA airmen statistics); estimate for ever
       say="holds an airline pilot licence",
       gained="years of flight school paid with loans or [savings], or flying in the forces, then the airline exams, a "
              "type rating and 'a job interview' in a simulator; it comes with [commercial pilot]",
       lost="a failed medical after 'a heart attack or stroke' or 'a warning from the doctor', a conviction, or letting "
            "it lapse after 'a wave of layoffs at work'; airline flying ends at 65, and the hands still know how to fly",
       needs="a first-class medical; not [someone with a record]; age 19 or more"),
  dict(name="train driving licence", kind="credential", ways="W", odds=0, skill_half=8, retires=None,
       ages=(20, 70), share=.001,   # Britain has about 20,000 train drivers (ASLEF), about 1 adult in 2,500 at a time;
                                    # estimate for ever
       say="is licensed to drive trains",
       gained="a selection day, a year of training on the rules and the routes, then a licence in their own name; it "
              "comes with [train driver]",
       lost="a failed medical, a conviction, or leaving the cab; route knowledge fades fast",
       needs="age 20 or more; regular medicals; not [someone with a record] for most operators"),
  dict(name="seafarer's papers", kind="credential", ways="R G", odds=0, skill_half=15, retires=None,
       ages=(16, 70), share=.003,   # estimate: officers and crew of rich countries' fleets, and the cruise-ship and
                                    # yacht crews who need the same basic safety training
       say="has seafarer's papers",
       gained="basic safety training at a maritime college (fire, first aid, survival, the lifeboat drill), a seafarer "
              "medical and a discharge book; a cadetship as a [merchant seafarer], or a season on a cruise ship after "
              "'the itch to be somewhere else'",
       lost="a failed seafarer medical; they lapse after years ashore, often after 'an offer of work ashore'",
       needs="age 16 or more; good health; [swimming] helps"),
  dict(name="sea survival certificate", kind="credential", ways="W R", odds=0, skill_half=5, retires=None,
       ages=(16, 75), share=.006,   # estimate: Britain asks it of every new commercial fisher (Seafish), and offshore
                                    # oil and wind workers renew theirs every four years
       say="is trained in sea survival",
       gained="a day in a training pool in a survival suit, righting a life raft and climbing in from the water; it "
              "comes with [commercial fisher], [lifeboat volunteer] and [merchant seafarer], and offshore work asks "
              "for it too",
       lost="it lapses four or five years after the course unless refreshed; leaving the sea lets it go",
       needs="a course paid by the boat, the station or an employer; [swimming] helps"),
  dict(name="fishing licence", kind="credential", ways="G R", odds=0, skill_half=15, retires=None,
       ages=(12, 100), share=.15,   # the US sells fishing licences to about 30 million people a year (US Fish and
                                    # Wildlife Service); England about a million rod licences (Environment Agency);
                                    # estimate for ever
       say="holds a fishing licence",
       gained="a rod licence after 'a first fish on a grandparent's line', 'fishing the canal with friends' or "
              "[hunting and fishing]; a permit for a [commercial fisher]",
       lost="not renewed one spring; a ban after an offence",
       needs="age 12 or 13 or more for a rod licence; a permit and a quota for commercial fishing"),
  dict(name="gas safety registration", kind="credential", ways="U B", odds=0, skill_half=10, retires=None,
       ages=(18, 75), share=.004,   # UK: about 130,000 engineers on the Gas Safe Register; US states license gas
                                    # fitters; estimate
       say="is registered to work on gas",
       gained="assessed on boilers and pipework after years as a [plumber] or a heating engineer, then a photo card "
              "and a number on the register",
       lost="a dangerous job found on inspection; the yearly registration let go after leaving the trade",
       needs="[trade ticket] or years as a [plumber]; an assessment every five years"),
  dict(name="welding certificate", kind="credential", ways="R W B", odds=0, skill_half=10, retires=None,
       ages=(16, 75), share=.008,   # the US counts over 400,000 welders, cutters, solderers and brazers (BLS), and
                                    # pipefitters and fabricators hold them too; estimate
       say="holds a welding certificate",
       gained="a test plate cut, bent and X-rayed after a course or an [apprentice] place; each certificate names a "
              "process and a position, and it comes with [welder]",
       lost="it lapses after six months without welding to that code; the hands keep the skill",
       needs="a welding course or an apprenticeship; 'learned a skill' several times"),
  dict(name="food hygiene certificate", kind="credential", ways="W G", odds=0, skill_half=5, retires=None,
       ages=(14, 90), share=.25,   # estimate: food work is one of the commonest first jobs; EU law requires food
                                   # handlers to be trained (Regulation 852/2004), and many US states ask for a food
                                   # handler card
       say="has a food hygiene certificate",
       gained="an afternoon's course and a short test before the first shift in a kitchen, a bakery or a care home; "
              "it comes with [cook], [baker] and [community-kitchen volunteer]",
       lost="it goes out of date after about three years away from food work; the habit of washing hands stays",
       needs="'your first real job' or 'a Saturday job at the corner shop' with food on the counter, or a place on a "
             "volunteer rota"),
  dict(name="tattoo licence", kind="credential", ways="R B", odds=0, skill_half=10, retires=None,
       ages=(18, 80), share=.0015,   # estimate: tattooists and cosmetic tattooists registered with a council or a
                                     # state health department
       say="is licensed to tattoo",
       gained="a hygiene course, an inspection of the studio and a registration in the artist's own name; it comes "
              "with [tattoo artist]",
       lost="a failed hygiene inspection, or letting it lapse after leaving the trade",
       needs="age 18 or more; [drawing and painting]; a studio that passes inspection"),
  dict(name="celebrant authorisation", kind="credential", ways="R W", odds=0, skill_half=10, retires=None,
       ages=(18, 95), share=.015,   # estimate: Australia has several thousand authorised marriage celebrants
                                    # (Attorney-General's Department); in the US many couples are married by a friend
                                    # ordained online; in most of Europe only registrars and clergy marry people
       say="is authorised to conduct weddings",
       gained="a place on the register with [civil celebrant]; ordination for an [ordained religious minister]; a "
              "one-day designation to lead 'a friend's wedding'",
       lost="struck from the register after a conviction, or the yearly training let go",
       needs="age 18 or more; legal recognition where the country gives it; [public speaking] helps"),
  dict(name="court interpreter accreditation", kind="credential", ways="W U", odds=0, skill_half=10, retires=None,
       ages=(23, 80), share=.0005,   # estimate: Britain's register of public service interpreters lists a few
                                     # thousand (NRPSI)
       say="is accredited to interpret in court",
       gained="an interpreting exam, a background check and an oath before the court; in many places the same oath "
              "lets a [translator] certify official papers; it comes with [court interpreter]",
       lost="a conviction, a complaint upheld, or letting it lapse after leaving the work",
       needs="[second language] at a professional level; not [someone with a record]; age 23 or more"),
  dict(name="chartered status", kind="credential", ways="U B", odds=0, skill_half=10, retires=None,
       ages=(25, 85), share=.006,   # the UK Engineering Council registers well over 100,000 Chartered Engineers; the
                                    # US licenses nearly half a million professional engineers (NSPE); estimate with
                                    # chartered surveyors and planners
       say="holds chartered status",
       gained="years of supervised work as a [civil engineer], a [land surveyor], an [architect] or an [urban "
              "planner], a written case and a professional review; letters after the name",
       lost="struck off after a complaint upheld, or resigned at retirement; the knowledge stays",
       needs="[graduate] or the [apprentice] route; four years or more in the work"),
  dict(name="rigging ticket", kind="credential", ways="R U", odds=0, skill_half=8, retires=None,
       ages=(18, 70), share=.006,   # estimate: stage and arena riggers are few; crane slingers and signallers on
                                    # building sites far more
       say="holds a rigging ticket",
       gained="a course in harnesses, hoists and load charts after a first year as a [stage technician], or on a "
              "building site as a slinger for [builder] and [welder] crews",
       lost="it lapses unless renewed every few years; a fall or a fault found ends the work at height",
       needs="a head for heights; a [site safety card] for building sites"),
  dict(name="press card", kind="credential", ways="U R", odds=0, skill_half=5, retires=None,
       ages=(18, 85), share=.004,   # estimate: about as many as work as journalists for a while
       say="carries a press card",
       gained="a first year of paid work as a [journalist], vouched for by an editor or a union",
       lost="handed back after leaving journalism; it must be renewed every few years",
       needs="[journalist]; work published or broadcast"),
  dict(name="therapy accreditation", kind="credential", ways="U G", odds=0, skill_half=15, retires=None,
       ages=(25, 85), share=.005,   # estimate: the US counts several hundred thousand licensed counsellors and family
                                    # therapists (BLS); Britain's counselling bodies have tens of thousands of members
       say="is accredited to practise therapy",
       gained="years of supervised clinical hours, therapy of their own and a panel's review; it comes with "
              "[psychotherapist], and some [nurse] and [teacher] careers turn to counselling this way",
       lost="struck off after a complaint upheld, or let go at retirement; what it taught stays",
       needs="[graduate]; a recognised training and supervision; not [someone with a record]"),
  dict(name="mediation accreditation", kind="credential", ways="W G", odds=0, skill_half=10, retires=None,
       ages=(21, 90), share=.005,   # estimate: community, family, workplace and court mediators
       say="is an accredited mediator",
       gained="a forty-hour course, role plays and supervised cases; it comes with [community-mediation volunteer], "
              "and a [restorative-justice advocate] trains this way to run a meeting",
       lost="it lapses without supervised cases and refresher hours",
       needs="[calming people down]; impartiality; age 21 or more"),
  dict(name="cleared to work with children", kind="credential", ways="W", odds=0, skill_half=None, retires=None,
       ages=(16, 95), share=.25,   # estimate: England's Disclosure and Barring Service issues several million
                                   # certificates a year; in Australia's states a working-with-children check is held
                                   # by a large minority of adults
       say="is cleared to work with children",
       gained="a background check for a first job or a volunteer role with children: as a [teacher], a [youth coach], "
              "a [school-governance board member], a [lay religious teacher] or a parent helper on the school trip",
       lost="a new conviction that shows on the check; otherwise it goes with the role and is renewed with the next",
       needs="age 16 or more; a role that asks for it; not [someone with a record] for most roles"),
  dict(name="site safety card", kind="credential", ways="W B", odds=0, skill_half=5, retires=None,
       ages=(16, 75), share=.1,   # UK: about 2 million CSCS cards in circulation (CSCS); US: OSHA's outreach courses
                                  # train about a million workers a year; estimate for ever
       say="has a site safety card",
       gained="a health and safety test before the first day on a building site, often as an [apprentice] or a "
              "[builder]; a [carpenter], a [welder] and a [civil engineer] carry one too",
       lost="it runs out after five years off the sites",
       needs="age 16 or more; a short course and a test"),
  dict(name="lifeguard qualification", kind="credential", ways="W R", odds=0, skill_half=5, retires=None,
       ages=(16, 70), share=.03,   # estimate: a common summer job for teenagers; pool lifeguard awards are renewed
                                   # every two years
       say="is a qualified lifeguard",
       gained="a pool course at sixteen or seventeen (towing a dummy, spinal holds, resuscitation), then 'your first "
              "real job' on the poolside or the beach; some go on to be a [lifeboat volunteer]",
       lost="it lapses after two years without requalifying, and the rescue drills fade",
       needs="[swimming], and strong; age 16 or more; a [first-aid certificate] comes with it"),
  dict(name="diving certificate", kind="credential", ways="R U", odds=0, skill_half=10, retires=None,
       ages=(10, 85), share=.04,   # PADI alone has issued close to 30 million certifications since 1967 (PADI), many to
                                   # holidaymakers from rich countries; estimate
       say="is a certified diver",
       gained="a week's course on 'a long-planned trip' or in a cold quarry at home: the classroom, the pool, then four "
              "open-water dives; some [archaeologist] and [search-and-rescue volunteer] teams dive",
       lost="it never lapses, though years out of the water mean a refresher first",
       needs="[swimming]; age 10 or more; a medical form"),
  dict(name="reader's ticket", kind="credential", ways="U G", odds=0, skill_half=15, retires=None,
       ages=(16, 110), share=.03,   # estimate: national libraries and record offices register many thousands of new
                                    # readers a year, family historians most of them
       say="holds a reader's ticket to the archives",
       gained="proof of address and a reason to look, at a national library or a county record office: family history "
              "after 'a parent dies', a thesis, a book; an [archivist] often starts in the reading room",
       lost="it expires and is renewed at the next visit",
       needs="age 16 or 18 or more; [finding things out] helps"),
  dict(name="permanent residence", kind="credential", ways="G B", odds=0, skill_half=None, retires=None,
       ages=(0, 110), share=.08,   # estimate: foreign-born people are about 14% of the population across rich OECD
                                   # countries (OECD), and most who stay are settled; the US counts about 13 million
                                   # green-card holders (DHS)
       say="has permanent residence",
       gained="years of legal residence as an [immigrant], or protection given to a [refugee] and later made "
              "permanent: a card that says the person may stay",
       lost="replaced by [citizenship], or given up on going home as a [returned migrant]; long years abroad can end "
            "it",
       needs="[immigrant]; years of legal residence, a clean record and the fee"),
  dict(name="chainsaw ticket", kind="credential", ways="G U", odds=0, skill_half=10, retires=None,
       ages=(16, 85), share=.015,   # estimate: forestry, tree and farm work ask for one in Britain; in Germany people
                                    # who cut their own firewood in a state forest take the course
       say="holds a chainsaw ticket",
       gained="a week's course on upkeep and felling, then an assessment in the woods; it comes with [forester], "
              "and a [farmer] or a [plot of land] with trees needs one too",
       lost="it does not lapse, but insurers want a refresher after years away",
       needs="age 16 or more; protective kit"),
]

