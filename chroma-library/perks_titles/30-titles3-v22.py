# =============================== TITLES, volume 3: the "v22" update, A16 (Library, 2026-10-09) ===============================
# The titles held back in the release batch for want of a decided mechanic (change-later.md, "From the release batch"),
# taken in on Emren's "Implement A16" (10-08 23:44 UTC), and three more first jobs so the first career spreads over
# more entry titles (change-later.md; care worker is there already). Shares are estimates for the titles check (C-L4).
TITLES += [
  dict(name="warehouse worker", kind="career", sector="services", sphere="prod", face="prod.R", ways="B R",
       profiles=[("B R", "Works fast for the bonus and the overtime, and takes the shifts others turn down."),
                 ("W U", "Keeps the line moving: learns the scanner, the system and the safety rules, every shift.")],
       meets="res:money+.03 res:health-.03 res:time-.08 need:autonomy-.03",
       ages=(16, 70), share=.06,   # estimate: warehouse and storage workers are about 1 US worker in 80 (BLS), with
                                   # high turnover, so many more hold the job for a while, often as a first job
       say="a warehouse worker",
       gained="'your first real job' through an agency, 'a new job at last' on the night shift at a distribution centre",
       lost="the contract ending, an injury, a better job",
       needs="a safety induction; a forklift ticket helps"),
  dict(name="receptionist", kind="career", sector="services", ways="W U",
       profiles=[("W U", "Keeps the front desk in order and knows where everything and everyone is."),
                 ("G", "The warm first face people see, who remembers their names.")],
       meets="res:money+.02 need:belonging+.02 res:time-.08",
       ages=(16, 75), share=.05,   # estimate: receptionists are about 1 US worker in 150 (BLS), with high turnover
       say="a receptionist",
       gained="'a job interview' for the front desk of a clinic, an office or a hotel, often as 'your first full-time job'",
       lost="another job, the desk replaced by a screen, retirement",
       needs="a tidy manner and a little computer skill"),
  dict(name="security guard", kind="career", sector="services", sphere="prot", face="prot.W", ways="W",
       profiles=[("W", "Keeps order at the door and by the book."),
                 ("U", "Watches the screens through the night and notices what others miss.")],
       meets="res:money+.02 need:safety-.02 res:time-.1 res:health-.02",
       ages=(18, 75), share=.05,   # estimate: security guards are about 1 US worker in 150 (BLS), many of them for a
                                   # few years, often as a first or a second job
       say="a security guard",
       gained="'a new job at last' with a security firm, after a short licence course",
       lost="the contract moving to another firm, nights wearing them down, another job",
       needs="a clean record in most places, and the guard's licence"),
  dict(name="union member", kind="community", sphere="prod", face="prod.W", ways="W R",
       profiles=[("W R", "Keeps faith with the people they work beside, and stands with them when it counts."),
                 ("U B", "Knows the agreement line by line, and makes it pay for the members.")],
       meets="need:belonging+.03 need:safety+.02 res:money-.01",
       ages=(16, 90), share=.25,   # about 1 worker in 6 across the OECD belongs to a union (OECD 2019), more in the
                                   # public sector and in the past; estimate for ever holding a card
       say="a union member",
       gained="joining at work, or holding the line in 'a strike vote at work'",
       lost="leaving the job or the union, letting the card lapse",
       needs="a job with a union"),
  dict(name="street preacher", kind="faith", sphere="faith", face="faith.R", ways="W R",
       meets="need:meaning+.08 need:belonging-.02 res:time-.05",
       ages=(14, 100), share=.005,   # estimate: a few in a thousand ever preach in the open street
       say="a street preacher",
       gained="taking a box to the corner of the square in 'a revival fills the square'",
       lost="the fire going out, a congregation of their own, the police moving them on for good",
       needs="a faith held hard enough to say it out loud to strangers"),
  dict(name="conscientious objector", kind="status", ways="",
       meets="need:meaning+.03 need:belonging-.03", lasts="life",
       ages=(18, 110), share=.003,   # estimate: only where service is compulsory, and few of those called object
       say="a conscientious objector",
       gained="objecting on conscience before the board in 'the call to serve', and serving in a care home instead",
       lost="never; it stays on the record",
       needs="a call-up, and a board that accepts the objection"),
  dict(name="national service done", kind="status", ways="",
       meets="need:competence+.02 res:ties+.02", lasts="life",
       ages=(19, 110), share=.02,   # estimate: about 3 in 1,000 young adults a year are called in this setting, most
                                    # serve a term
       say="someone who did their national service",
       gained="the end of the term served after 'the call to serve'",
       lost="never",
       needs="[soldier] held through a term that began with 'the call to serve'"),
  dict(name="permanent resident", kind="status", ways="",
       meets="need:safety+.03", lasts="life",
       ages=(5, 110), share=.08,   # as [permanent residence], the perk that carries the access: the two come together
       say="a permanent resident",
       gained="'residence papers at the government office'",
       lost="[naturalised citizen] takes its place in how people name them; the perk stays",
       needs="[immigrant] or [refugee], years of legal residence"),
  dict(name="without papers", kind="status", ways="",
       meets="need:safety-.08 res:freedom-.08 res:money-.03", lasts=5,   # until papers come or they leave; 5 caps it
       ages=(5, 110), share=.01,   # estimate: undocumented people are a few residents in 100 in the US and fewer in
                                   # most of Europe
       say="living without papers",
       gained="a refused residence application in 'residence papers at the government office', and staying anyway",
       lost="papers granted at last, leaving the country, being sent back",
       needs="[immigrant] or [refugee]"),
  dict(name="served the old regime", kind="status", ways="",
       meets="need:safety-.03 need:belonging-.03", lasts="life",
       ages=(16, 110), share=.002,   # estimate: 'the old order falls' reaches about 2 lives in 100
       say="someone who served the old regime",
       gained="standing with the last of the old guard in 'the old order falls'",
       lost="never; the new order remembers",
       needs="the old order falling in their lifetime"),
  dict(name="veteran of a revolution", kind="status", ways="",
       meets="need:meaning+.03 need:belonging+.02", lasts="life",
       ages=(16, 110), share=.003,   # estimate: 'the old order falls' reaches about 2 lives in 100
       say="a veteran of the revolution",
       gained="pushing at the palace gates in 'the old order falls'",
       lost="never",
       needs="the old order falling in their lifetime"),
  dict(name="founder of a movement", kind="status", ways="",   # stage 3, C5 (stage3-rules.md section 5)
       meets="need:meaning+.05 need:autonomy+.03", lasts="life",
       ages=(25, 110), share=.001,   # estimate: 'a following of your own' reaches at most about 1 life in 1,000
       say="the founder of a movement",
       gained="founding a movement of their own and keeping a following around it",   # not quoted: the moment is post-cut, the check reads the live earth.md
       lost="never",
       needs="a new movement founded in their lifetime, by them"),
  dict(name="known as a strike-breaker", kind="status", ways="",
       meets="need:belonging-.05 res:ties-.03", lasts=15,   # memories at work fade; 15 caps it
       ages=(18, 90), share=.02,   # estimate: about 3 lives in 10 meet a strike ballot, few keep working through it
       say="known as a strike-breaker",
       gained="voting no and working through the strike in 'a strike vote at work'",
       lost="a new workplace, the years",
       needs="a job with a union and a strike"),
]

