# Cause audit: the 330 title and perk rules (L1, "Every change has a cause")

Library thread, 2026-10-18. This audit compares each rule in `earth_rules.ROLES` (main 39123cf) with the Library's own `gained=` words in `earth_perks_titles.py`, for two uses.

- **E1 and the game's cause lines (now):** the line names the clause that held. A rule marked **loose** can name a true clause that reads wrong: "since 'a pet of your own'" for a dog that was a kitten. Until `cause_fit` lands, the game should use the Library's words for what was met, as the design says.
- **E2 `cause_fit` (next joint refit):** each loose or missing rule gets the condition it implies, in the engine's vocabulary. A reading the engine doesn't have yet is written `NEW:<name>`.

The work was done by four helpers, one per quarter of the rules, against a shared rubric, then vetted by the Library. Vetting set five verdicts by hand: the school-leaving certificate and swimming keep their age reading, and soldier, apprentice and seeker come through job and commitment events. Every moment and mark named below exists in earth.py or the engine.

Counts: fine 190, loose 105, missing 29, fine-age 5, none-ok 1.

- **fine:** the clause that held explains the gain truly. This includes job and commitment titles given through their event, and titles that grow from a held title.
- **loose:** the condition fires in cases the words exclude.
- **missing:** the words name a real cause the condition doesn't read.
- **fine-age:** the age or stage is the honest cause.
- **none-ok:** there is no condition and the words name no cause either.

Tier A (33 rules) are the ones whose cause line would read false. Tier B are vaguer readings, mostly a generic mark such as 'learned a skill' standing for a specific skill.

## Two bugs (sent to the Engine, 10-18)

An AST scan of every condition in earth_rules finds two operator-precedence bugs. `&` and `|` bind tighter than `>=` in Python.

- **boxing or martial arts:** `mkn('learned a skill') >= 2 & (age <= 40)` is read as `mkn(...) >= (2 & (age <= 40))`, which is `>= 0` and always true. So the perk comes at any age with no skill. Fix: `(mkn('learned a skill') >= 2) & (age <= 40)`.
- **home nursing:** `mkn('helped someone in need') >= 2 | has('carer for a parent')` is read as `mkn(...) >= (2 | has(...))`. For a carer that is `>= 3`, so being a carer alone never gives it. Fix: `(mkn('helped someone in need') >= 2) | has('carer for a parent')`.

Both fixes change lives. The Engine confirmed both (10-18) and takes them into `cause_fit` (E2) as its first two misfits, refitted and proved at the joint refit.

## Tier A: causes that would read false

| Rule | Verdict | Today's condition | What is wrong | Condition it implies |
|---|---|---|---|---|
| parent of three or more | loose | `has('mother or father') & (yrs_children >= 3) & (yrs_children <= 15) & held_partner` | Reads only years as a parent with a partner, so a parent of one qualifies; the Library needs a third child. | `has('mother or father') & (alive_child >= 3) & had(['a child is born'], 1)` |
| stepparent | loose | `held_partner & (yrs_partner < 3) & ~held_children & (age >= 22)` | Fires for anyone with a new partner and no children; the engine never checks that the partner has children. | `held_partner & (yrs_partner < 3) & ~held_children & NEW:partner_has_kids (the partner brought children from before)` |
| foster parent | loose | `(age >= 25) & (money > .4) & mk('helped someone in need')` | Any 'helped someone in need' (carrying shopping) plus money starts fostering; the Library names taking in a child. | `(age >= 25) & (money > .4) & (mk('took them in', 2) \| had(['you take in a child who needs a home'], 1))` |
| adoptive parent | missing | `(age >= 25) & held_partner & ~held_children & (yrs_partner >= 3)` | Only age and a childless partnership, so the cause line would say 'with a partner'; the Library names 'you take in a child who needs a home'. | `(age >= 25) & ~held_children & (mk('took them in', 2) \| had(['you take in a child who needs a home'], 1))` |
| grandparent | loose | `has('mother or father') & (yrs_children >= 22)` | Guessed from 22 years as a parent, so it fires when no child has a child; 'your first grandchild' is a real moment. | `has('mother or father') & had(['your first grandchild'], 1)` |
| convert | loose | `~was('regular worshipper') \| was('left the faith')` | The clause is a negation (never a [regular worshipper]), true for anyone never raised in a faith; it names no search or welcome. | `held_faith & (was('seeker') \| had(['welcomed into a community', 'a friend takes another faith', 'a new faith comes to town'], 2)) & NEW:raised_other (not raised in this faith)` |
| graduate | loose | `has('school-leaving certificate') & (age >= 20) & (age <= 30)` | Any [school-leaving certificate] holder graduates by chance at 20 to 30; the Library needs 'you win a scholarship or a place'. | `has('school-leaving certificate') & (age >= 20) & (had(['you win a scholarship or a place'], 12) \| was('first-generation university student'))` |
| has killed in war | loose | `has('soldier') & (yrs_career >= 1)` | Any [soldier] after a year qualifies in peacetime; the Library needs 'war comes'. | `has('soldier') & had(['war comes'], 3)` |
| immigrant | loose | `ago_move < 1` | Any move within the year counts, so moving to the next town makes an immigrant; the Library means another country. | `had(['the first months in a new country', 'work and a room abroad, if you go this month'], 1) \| NEW:moved_abroad (a move that crosses a border, also as a child with the family)` |
| someone with a record | loose | `mk('defied an authority', 1) \| mk('hid a wrong', 1) \| mk('took a wild risk', 1)` | Fires on 'took a wild risk', 'defied an authority' or 'hid a wrong' with no law broken. | `mk('broke the law', 2)` |
| ex-prisoner | loose | `has('someone with a record') & mk('defied an authority', 2)` | 'defied an authority' plus a record is not a sentence served; the Library needs time in prison. | `has('someone with a record') & (yrs_out < 1)` |
| cancer survivor | loose | `had(['a frightening diagnosis'], 1) & (health > .4)` | Any 'a frightening diagnosis' counts, not only cancer, and the all-clear comes within a year. | `had(['a frightening diagnosis'], 3) & (health > .4) & NEW:cancer_diagnosis (the diagnosis was cancer)` |
| boxing or martial arts | loose | `mkn('learned a skill') >= 2 & (age <= 40)` | Precedence bug: `mkn(..) >= 2 & (age <= 40)` parses as `mkn(..) >= (2 & ..)` = `>= 0`, always true, so anyone gets it; the Library names 'a fight after school'. | `(mkn('learned a skill') >= 2) & (age <= 40) & had(['a fight after school', 'someone starts mocking you online'], 3)` |
| home nursing | loose | `mkn('helped someone in need') >= 2 \| has('carer for a parent')` | Two of any 'helped someone in need' give nursing, and a precedence bug makes the carer path need three marks instead of none. | `has('carer for a parent') \| ((mkn('helped someone in need') >= 2) & had(['flu, alone in a rented room', 'your child falls seriously ill', 'your partner falls seriously ill'], 3))` |
| citizenship | loose | `has('immigrant')` | Fires in the first year as an [immigrant], and immigrant itself comes from any move; the Library asks for years of residence and an oath, and 'the oath of citizenship' exists. | `(has('immigrant') & (yrs_has('immigrant') >= 5)) \| had(['the oath of citizenship'], 1)` |
| drinks licence | loose | `~has('someone with a record') & held_career` | Any career with no record fires it, so a nurse or clerk gets a licence to sell drink; the Library ties it to taking on a pub or shop. | `~has('someone with a record') & (age >= 18) & (has('shop owner') \| has('waiter or bartender') \| NEW:pub keeper (a title for running a pub))` |
| local hero | loose | `mk('helped someone in need', 1) & mk('took a wild risk', 1)` | Any help plus any wild risk in the same year fires it, though unrelated; the Library names 'a stranger saves you, or you save one'. | `had(['a stranger saves you, or you save one'], 1) & mk('helped someone in need', 1)` |
| friend for life | loose | `mk('made a friend')` | Any 'made a friend' fires it, while the Library names the moment 'a friend for life' itself. | `had(['a friend for life', 'a best friend of your own'], 2)` |
| dog of one's own | loose | `had(['a pet of your own', 'a stray dog follows you home'], 1)` | 'a pet of your own' can be any pet, so a kitten or a fish reads as the cause of a dog. | `had(['a stray dog follows you home'], 1) \| (had(['a pet of your own'], 1) & NEW:pet kind (which animal the pet is))` |
| inheritance | loose | `ago_death < 1` | ago_death counts any death, a friend's or a neighbour's, while the Library names 'a parent dies' and 'an unexpected legacy'. | `had(['a parent dies', 'a grandparent dies', 'losing a grandparent', 'an unexpected legacy'], 1)` |
| scholarship | loose | `(age >= 11) & (age <= 20) & (mkn('learned a skill') >= 3)` | Three skills in a school-age window fire it without ever winning; the Library names 'you win a scholarship or a place' itself. | `had(['you win a scholarship or a place'], 1)` |
| spouse in a family-arranged marriage | missing | `has('wife or husband') & (yrs_has('wife or husband') < 1)` | Any new marriage can become 'family-arranged' at 3% a year; the family introduction the words require is never read. | `has('wife or husband') & (yrs_has('wife or husband') < 1) & NEW:family_introduction the marriage began with a family introduction chosen in 'getting married'` |
| parent of an only child | loose | `has('mother or father') & (yrs_children >= 4) & ~was('parent of an only child') & ~had(['a child is born', 'a baby on the way, planned or not'], 4)` | Once the youngest of several children is four, ~had('a child is born', 4) holds, so a parent of three can be named parent of an only child. | `has('mother or father') & (yrs_children >= 4) & (kid_young >= yrs_children) & ~was('parent of an only child')` |
| guardian of an unrelated child | loose | `(age >= 21) & mk('helped someone in need')` | Any 'helped someone in need' mark, such as carrying a neighbour's shopping, can make a child's guardian; the words need a will or a court and taking a child in. | `(age >= 21) & had(['you take in a child who needs a home'], 1) & mk('took them in')` |
| first-generation university student | missing | `has('school-leaving certificate') & (age >= 17) & (age <= 25) & ~has('graduate') & ~was('first-generation university student')` | The engine never reads the parents, so a child of two graduates can be first-generation; enrolment ('you win a scholarship or a place') is not read either. | `has('school-leaving certificate') & (age >= 17) & (age <= 25) & ~has('graduate') & NEW:parents_no_degree no parent holds [graduate]` |
| former foster child | missing | `False` | req is False, so it is never gained, yet the words name 'going into foster care', a real moment. | `had(['going into foster care'], 110)` |
| asylum applicant | loose | `(ago_move < 1) & (had(['war comes'], 3) \| mk('moved away', 1)) & ~was('asylum applicant')` | mk('moved away') from any move, even to the next town, can make an asylum applicant; the words need flight from war or persecution. | `(ago_move < 1) & (had(['war comes'], 3) \| NEW:persecuted a recorded threat or persecution at home) & ~was('asylum applicant')` |
| living in residential care | loose | `(had(['moving to a smaller home or into care'], 1) & (age >= 60)) \| ((age >= 80) & (health < .5))` | 'moving to a smaller home or into care' also covers a smaller home, and age 80 with poor health alone puts someone in a care home. | `had(['moving to a smaller home or into care'], 1) & NEW:into_care the pick in that moment chose care, not a smaller home` |
| displaced by a disaster | loose | `had(['losing the home', 'war comes'], 1)` | 'losing the home' can be a repossession, and 'war comes' alone gives it with no displacement, which the words exclude. | `had(['losing the home'], 1) & (had(['war comes', 'the flood wall gives way'], 1) \| NEW:home_destroyed the home was lost to flood, fire or storm)` |
| award for bravery | loose | `(has('firefighter') \| has('lifeboat volunteer') \| has('search-and-rescue volunteer') \| has('paramedic') \| has('police officer') \| has('soldier') \| has('local hero')) & mk('took a wild risk', 2) & mk('helped someone in need', 2)` | A rescuer's 'took a wild risk' and 'helped someone in need' can come from two unrelated picks; the words say both at once, in 'a stranger saves you, or you save one'. | `(has('firefighter') \| has('lifeboat volunteer') \| has('search-and-rescue volunteer') \| has('paramedic') \| has('police officer') \| has('soldier') \| has('local hero')) & had(['a stranger saves you, or you save one'], 1)` |
| business partner | loose | `(age >= 18) & (has('founder of a firm') \| has('shop owner') \| has('plumber') \| has('carpenter') \| has('tattoo artist') \| has('architect') \| has('accountant') \| has('psychotherapist') \| has('estate agent') \| has('farmer'))` | Any [plumber], [farmer] or [psychotherapist] gains a business partner with no partner moment; the words name 'a friend wants to start a project with you' or 'a chance to start a business of your own'. | `(age >= 18) & (has('founder of a firm') \| has('shop owner') \| had(['a friend wants to start a project with you', 'a chance to start a business of your own'], 2)) & mk('made a friend', 5)` |
| godchild | loose | `(age >= 16) & (mkn('made a friend') >= 2) & (has('friend for life') \| has('regular worshipper') \| has('believer on the big days'))` | A [regular worshipper] with two friends becomes a godparent with no one asking; the real moment 'asked to stand for a child at the naming' exists and is not read. | `had(['asked to stand for a child at the naming'], 1) \| ((age >= 16) & (has('friend for life') \| (alive_sibling > 0)) & (mkn('made a friend') >= 2) & chance(.1))` |
| cat of one's own | loose | `had(['a pet of your own'], 1) \| (age >= 18)` | 'a pet of your own' also gives [dog of one's own], so the pet can be a dog, and the (age >= 18) branch gives a cat to any adult for no reason. | `(had(['a pet of your own'], 1) & NEW:pet_is_cat (the pet pick names a cat)) \| ((age >= 18) & NEW:cat_taken_in (a kitten from a neighbour or a shelter cat))` |

## Proposal: a perk "pet of one's own"

Today 'a pet of your own' gives [dog of one's own] at rate .5 a year, and [cat of one's own] too. So a kitten can become a dog (preset 1, seed 7). The moment doesn't say which animal it is.

The proposal is a new bond perk, "pet of one's own" (a small animal: a kitten, a rabbit, a bird), gained from 'a pet of your own' and lost with 'your pet dies'. [dog of one's own] would come only from 'a stray dog follows you home', or from a pick that names a dog, which needs `NEW:pet kind`. [cat of one's own] would come from a kitten pick, or by itself at 18 and over with a cause: phrase ("a kitten from a neighbour").

Adding a perk changes the role table, and with it lives. So it rides `cause_fit`, with the Engine's say on the shares, and is not in this PR. The `gained=` words of both perks already read this way in this PR.

## Readings the engine doesn't have (NEW:)

`cause_fit` needs these to tighten the rules above. Each is named in the implied condition of at least one rule: `adoption_record`, `bee_hobby`, `cancer_diagnosis`, `car_work`, `card nights`, `cat_taken_in`, `child_abroad`, `child_assessed`, `engineering_apprentice`, `family business`, `family_garden`, `family_introduction`, `farm_family`, `first-aid course`, `friend in office`, `heating_trade`, `heritage_event`, `home_destroyed`, `into_care`, `moved_abroad`, `offshore_work`, `old family`, `parent_tongue`, `parents_no_degree`, `partner from an old family`, `partner_has_kids`, `persecuted`, `pet kind`, `pet_is_cat`, `pub keeper`, `raised_other`, `riding_lessons`, `school_choir`, `science_degree`, `yrs_was`.

The most used are a parent's degree (first-generation students), which animal a pet is, a move that crosses a border (immigrant, asylum, family abroad), and the years a past title was held.

## Rules that keep an age, stage, money or no condition (cause: phrases in L2)

These are gained in time, and the clause the engine can name is an age, a stage, a money level or nothing. L2 writes a `cause:` phrase for each, in words true for today's rule. Where `cause_fit` later gives the rule a real condition, its phrase is retired at that refit:

adopted person, boxing or martial arts, carer for a parent, choir member, dancing, driving licence, eldest child, family abroad, family business, family who will always take you in, first-aid certificate, godparent who looks out, good credit, growing food, historical reenactment member, homeless, homeowner, housing-cooperative member, hunting and fishing, immigrant, in a street gang, instrument of one's own, motorbike licence, old family name, on the team, party member, passport, savings, school-leaving certificate, scout or guide, second language, secure tenancy, swimming, teachers' favourite.

## Word fixes in this PR (lives unchanged)

The engine and the game never read `gained=` or `lost=`, so these 33 fixes change no life. They make the Library's words name the moments and marks a rule should read (in 'quotes', as real moment and mark names). They also drop names of real faiths (Sunday school, madrasa, Hebrew school, christening):

apprentice, baker, beekeeping, boat of one's own, car mechanics, cat of one's own, celebrant authorisation, chainsaw ticket, citizenship, convert, digital-rights advocate, disability-rights organiser, dog of one's own, editing, fishing licence, fixing things, godchild, godparent who looks out, good name in town (lost), hives of one's own, hunting and fishing, immigrant, inheritance, instrument of one's own, partner in a multigenerational household, psychotherapist, public speaking, restorative-justice advocate, scripture, someone with a record, striking a deal, used to night shifts (lost), working with data.

## Notes for cause_fit

- **Shares:** several implied conditions narrow a rule to moments that are rarer than the rule's share needs. Examples are the graduate (the scholarship moment), the grandparent ('your first grandchild') and the godchild. The refit should keep each title inside its realism target, widening a moment list or raising a rate where needed, not dropping the cause.
- **had() windows:** read events such as 'a bitter election', 'a wave of layoffs at work' and 'break-ins on the street' have no age range. Check that `had()` sees them before using them.
- **Vocabulary check:** `older_siblings` and `younger_siblings` (eldest child) are real engine readings (engine.py, N4), though vocab.txt doesn't list them.

## Every rule

Tier A first, then by verdict. "Cause today" is the kind of clause E1 will name: moment, mark, title/perk, money, age/stage, job-event or none.

| Rule | Verdict | Tier | Cause today | Why | Condition it implies |
|---|---|---|---|---|---|
| parent of three or more | loose | A | title/perk | Reads only years as a parent with a partner, so a parent of one qualifies; the Library needs a third child. | `has('mother or father') & (alive_child >= 3) & had(['a child is born'], 1)` |
| stepparent | loose | A | title/perk | Fires for anyone with a new partner and no children; the engine never checks that the partner has children. | `held_partner & (yrs_partner < 3) & ~held_children & NEW:partner_has_kids (the partner brought children from before)` |
| foster parent | loose | A | mark | Any 'helped someone in need' (carrying shopping) plus money starts fostering; the Library names taking in a child. | `(age >= 25) & (money > .4) & (mk('took them in', 2) \| had(['you take in a child who needs a home'], 1))` |
| grandparent | loose | A | title/perk | Guessed from 22 years as a parent, so it fires when no child has a child; 'your first grandchild' is a real moment. | `has('mother or father') & had(['your first grandchild'], 1)` |
| convert | loose | A | title/perk | The clause is a negation (never a [regular worshipper]), true for anyone never raised in a faith; it names no search or welcome. | `held_faith & (was('seeker') \| had(['welcomed into a community', 'a friend takes another faith', 'a new faith comes to town'], 2)) & NEW:raised_other (not raised in this faith)` |
| graduate | loose | A | title/perk | Any [school-leaving certificate] holder graduates by chance at 20 to 30; the Library needs 'you win a scholarship or a place'. | `has('school-leaving certificate') & (age >= 20) & (had(['you win a scholarship or a place'], 12) \| was('first-generation university student'))` |
| has killed in war | loose | A | title/perk | Any [soldier] after a year qualifies in peacetime; the Library needs 'war comes'. | `has('soldier') & had(['war comes'], 3)` |
| immigrant | loose | A | age/stage | Any move within the year counts, so moving to the next town makes an immigrant; the Library means another country. | `had(['the first months in a new country', 'work and a room abroad, if you go this month'], 1) \| NEW:moved_abroad (a move that crosses a border, also as a child with the family)` |
| someone with a record | loose | A | mark | Fires on 'took a wild risk', 'defied an authority' or 'hid a wrong' with no law broken. | `mk('broke the law', 2)` |
| ex-prisoner | loose | A | mark | 'defied an authority' plus a record is not a sentence served; the Library needs time in prison. | `has('someone with a record') & (yrs_out < 1)` |
| cancer survivor | loose | A | moment | Any 'a frightening diagnosis' counts, not only cancer, and the all-clear comes within a year. | `had(['a frightening diagnosis'], 3) & (health > .4) & NEW:cancer_diagnosis (the diagnosis was cancer)` |
| boxing or martial arts | loose | A | none | Precedence bug: `mkn(..) >= 2 & (age <= 40)` parses as `mkn(..) >= (2 & ..)` = `>= 0`, always true, so anyone gets it; the Library names 'a fight after school'. | `(mkn('learned a skill') >= 2) & (age <= 40) & had(['a fight after school', 'someone starts mocking you online'], 3)` |
| home nursing | loose | A | mark | Two of any 'helped someone in need' give nursing, and a precedence bug makes the carer path need three marks instead of none. | `has('carer for a parent') \| ((mkn('helped someone in need') >= 2) & had(['flu, alone in a rented room', 'your child falls seriously ill', 'your partner falls seriously ill'], 3))` |
| citizenship | loose | A | title/perk | Fires in the first year as an [immigrant], and immigrant itself comes from any move; the Library asks for years of residence and an oath, and 'the oath of citizenship' exists. | `(has('immigrant') & (yrs_has('immigrant') >= 5)) \| had(['the oath of citizenship'], 1)` |
| drinks licence | loose | A | title/perk | Any career with no record fires it, so a nurse or clerk gets a licence to sell drink; the Library ties it to taking on a pub or shop. | `~has('someone with a record') & (age >= 18) & (has('shop owner') \| has('waiter or bartender') \| NEW:pub keeper (a title for running a pub))` |
| local hero | loose | A | mark | Any help plus any wild risk in the same year fires it, though unrelated; the Library names 'a stranger saves you, or you save one'. | `had(['a stranger saves you, or you save one'], 1) & mk('helped someone in need', 1)` |
| friend for life | loose | A | mark | Any 'made a friend' fires it, while the Library names the moment 'a friend for life' itself. | `had(['a friend for life', 'a best friend of your own'], 2)` |
| dog of one's own | loose | A | moment | 'a pet of your own' can be any pet, so a kitten or a fish reads as the cause of a dog. | `had(['a stray dog follows you home'], 1) \| (had(['a pet of your own'], 1) & NEW:pet kind (which animal the pet is))` |
| inheritance | loose | A | moment | ago_death counts any death, a friend's or a neighbour's, while the Library names 'a parent dies' and 'an unexpected legacy'. | `had(['a parent dies', 'a grandparent dies', 'losing a grandparent', 'an unexpected legacy'], 1)` |
| scholarship | loose | A | mark | Three skills in a school-age window fire it without ever winning; the Library names 'you win a scholarship or a place' itself. | `had(['you win a scholarship or a place'], 1)` |
| parent of an only child | loose | A | title/perk | Once the youngest of several children is four, ~had('a child is born', 4) holds, so a parent of three can be named parent of an only child. | `has('mother or father') & (yrs_children >= 4) & (kid_young >= yrs_children) & ~was('parent of an only child')` |
| guardian of an unrelated child | loose | A | mark | Any 'helped someone in need' mark, such as carrying a neighbour's shopping, can make a child's guardian; the words need a will or a court and taking a child in. | `(age >= 21) & had(['you take in a child who needs a home'], 1) & mk('took them in')` |
| asylum applicant | loose | A | moment | mk('moved away') from any move, even to the next town, can make an asylum applicant; the words need flight from war or persecution. | `(ago_move < 1) & (had(['war comes'], 3) \| NEW:persecuted a recorded threat or persecution at home) & ~was('asylum applicant')` |
| living in residential care | loose | A | moment | 'moving to a smaller home or into care' also covers a smaller home, and age 80 with poor health alone puts someone in a care home. | `had(['moving to a smaller home or into care'], 1) & NEW:into_care the pick in that moment chose care, not a smaller home` |
| displaced by a disaster | loose | A | moment | 'losing the home' can be a repossession, and 'war comes' alone gives it with no displacement, which the words exclude. | `had(['losing the home'], 1) & (had(['war comes', 'the flood wall gives way'], 1) \| NEW:home_destroyed the home was lost to flood, fire or storm)` |
| award for bravery | loose | A | mark | A rescuer's 'took a wild risk' and 'helped someone in need' can come from two unrelated picks; the words say both at once, in 'a stranger saves you, or you save one'. | `(has('firefighter') \| has('lifeboat volunteer') \| has('search-and-rescue volunteer') \| has('paramedic') \| has('police officer') \| has('soldier') \| has('local hero')) & had(['a stranger saves you, or you save one'], 1)` |
| business partner | loose | A | title/perk | Any [plumber], [farmer] or [psychotherapist] gains a business partner with no partner moment; the words name 'a friend wants to start a project with you' or 'a chance to start a business of your own'. | `(age >= 18) & (has('founder of a firm') \| has('shop owner') \| had(['a friend wants to start a project with you', 'a chance to start a business of your own'], 2)) & mk('made a friend', 5)` |
| godchild | loose | A | title/perk | A [regular worshipper] with two friends becomes a godparent with no one asking; the real moment 'asked to stand for a child at the naming' exists and is not read. | `had(['asked to stand for a child at the naming'], 1) \| ((age >= 16) & (has('friend for life') \| (alive_sibling > 0)) & (mkn('made a friend') >= 2) & chance(.1))` |
| cat of one's own | loose | A | moment | 'a pet of your own' also gives [dog of one's own], so the pet can be a dog, and the (age >= 18) branch gives a cat to any adult for no reason. | `(had(['a pet of your own'], 1) & NEW:pet_is_cat (the pet pick names a cat)) \| ((age >= 18) & NEW:cat_taken_in (a kitten from a neighbour or a shelter cat))` |
| adoptive parent | missing | A | title/perk | Only age and a childless partnership, so the cause line would say 'with a partner'; the Library names 'you take in a child who needs a home'. | `(age >= 25) & ~held_children & (mk('took them in', 2) \| had(['you take in a child who needs a home'], 1))` |
| spouse in a family-arranged marriage | missing | A | title/perk | Any new marriage can become 'family-arranged' at 3% a year; the family introduction the words require is never read. | `has('wife or husband') & (yrs_has('wife or husband') < 1) & NEW:family_introduction the marriage began with a family introduction chosen in 'getting married'` |
| first-generation university student | missing | A | title/perk | The engine never reads the parents, so a child of two graduates can be first-generation; enrolment ('you win a scholarship or a place') is not read either. | `has('school-leaving certificate') & (age >= 17) & (age <= 25) & ~has('graduate') & NEW:parents_no_degree no parent holds [graduate]` |
| former foster child | missing | A | none | req is False, so it is never gained, yet the words name 'going into foster care', a real moment. | `had(['going into foster care'], 110)` |
| farmer | loose | B | title/perk | [family business] is any family firm (a relative's shop counts), so a shop child becomes a farmer; the Library means a family farm. | `has('plot of land') \| (has('family business') & NEW:farm_family (the family business is a farm))` |
| founder of a firm | loose | B | mark | Any 'took a wild risk' (a dare, a cliff jump) plus money makes a founder; the Library names a business chance. | `(has('savings') \| (money > .6)) & mk('took a wild risk', 2) & had(['a chance to start a business of your own', 'a friend wants to start a project with you', 'an idea for a side business', 'an old friend asks to go into business'], 2)` |
| in a street gang | loose | B | money | Low money alone starts gang life with no fight or friends, and there is no lower age; the Library names 'a fight after school' or 'money runs out at home'. | `(age >= 12) & (age <= 25) & (had(['a fight after school', 'money runs out at home'], 2) \| mk('made an enemy', 1)) & ((money < .3) \| mk('made an enemy', 1))` |
| homeowner | loose | B | money | Money over .5 alone buys a home without [savings] or [good credit]; the Library names 'buying a home' with both. | `(age >= 22) & ((has('savings') & has('good credit')) \| has('inheritance') \| had(['buying a home', 'an unexpected legacy'], 1))` |
| musical instrument | loose | B | title/perk | Owning an [instrument of one's own] alone gives the skill with no lessons or 'learned a skill'. | `has('instrument of one\'s own') & (mkn('learned a skill') >= 2) & had(['you take up an instrument or a language', 'a band or a sport that takes over your life', 'a free music school with instruments to borrow', 'a band that needs a drummer'], 5)` |
| fixing things | loose | B | mark | Any 'learned a skill' (a piano lesson) gives it; the Library names 'the house needs repairs'. | `mk('learned a skill', 3) & had(['the house needs repairs', 'a broken lamp at the repair cafe', 'up the ladder to clear the gutters'], 3)` |
| car mechanics | loose | B | mark | Any two 'learned a skill' marks give engines; the Library names an old car and a garage job. | `(mkn('learned a skill') >= 2) & (had(['the car no one makes parts for'], 3) \| NEW:car_work (a garage job or an old car of one's own that keeps failing))` |
| growing food | loose | B | age/stage | The age clause gives every child under 15 the skill with no garden; the Library names a grandmother's garden. | `had(['tending an allotment', 'an afternoon in the garden', 'a front garden left to grow'], 3) \| ((age <= 14) & (alive_grandparent > 0) & NEW:family_garden (a parent or grandparent who grows food))` |
| sewing and mending | loose | B | mark | Any 'learned a skill' gives it; the Library names 'a box of craft things and a free hour' and being taught. | `mk('learned a skill', 3) & had(['a box of craft things and a free hour'], 3)` |
| public speaking | loose | B | mark | Any skill plus any wild risk (a cliff jump and a piano lesson) gives it; the Library names a debate, a play or a speech. | `(mk('learned a skill', 2) \| mk('took a wild risk', 2)) & had(['a debate or contest at school', 'the school play', 'the toast at the wedding', 'the club or congregation asks you to lead', 'the first time you speak at the meeting'], 2)` |
| bookkeeping | loose | B | mark | Any 'learned a skill' after 16 gives it; the Library names 'a budget that will not balance' and 'your first tax form and a stack of bills'. | `mk('learned a skill', 2) & (age >= 16) & had(['a budget that will not balance', 'your first tax form and a stack of bills', 'two evening classes and time for one'], 2)` |
| writing code | loose | B | mark | Any two 'learned a skill' marks give code; the Library names 'a new hobby you cannot put down' or 'new technology changes your job'. | `(mkn('learned a skill') >= 2) & had(['a new hobby you cannot put down', 'new technology changes your job'], 3)` |
| drawing and painting | loose | B | mark | Any 'learned a skill' gives it; the Library names 'a box of craft things and a free hour' and 'the urge to make something'. | `mk('learned a skill', 3) & had(['a box of craft things and a free hour', 'the urge to make something', 'a teacher who sees something in you'], 3)` |
| selling | loose | B | mark | Any 'made a friend' makes someone able to sell anything; the Library names a shop job, a side business or a year in sales. | `had(['a Saturday job at the corner shop', 'an idea for a side business'], 3) \| (yrs_has('salesperson') >= 1)` |
| finding things out | loose | B | mark | Any 'learned a skill' gives it, so a piano or cooking lesson reads as the cause of a curiosity the Library ties to 'a curiosity that will not let go' or a degree. | `had(['a curiosity that will not let go'], 3) \| has('graduate')` |
| minding small children | loose | B | mark | Any 'helped someone in need' fires it, such as helping a stranger, while the Library names a little cousin, babysitting or being a parent. | `had(['your little cousin comes to stay'], 5) \| held_children \| has('mother or father')` |
| calming people down | loose | B | mark | Two 'helped someone in need' of any kind fire it (lending money, giving a lift), while the Library names nursing shifts and tense moments handled well. | `(mkn('helped someone in need') >= 2) & (has('nurse') \| had(['a teenager in your care breaks the rules', 'you see a stranger being harassed', 'a friend is being picked on'], 5))` |
| striking a deal | loose | B | mark | Any 'took a wild risk' (a dare, a jump) gives a bargaining skill; the Library names a raise won, a market stall or a home bought well. | `(age >= 16) & had(['a bonus or a raise', 'haggling at the Sunday market', 'buying a home'], 3)` |
| cards for money | loose | B | mark | Any 'took a wild risk' gives a card skill with no card game at all; the Library names poker nights and 'a game of cards with old rivals'. | `had(['a game of cards with old rivals'], 3) \| (mk('took a wild risk') & NEW:card nights (a moment of regular card games for money, ages 14 and up))` |
| teaching | loose | B | mark | Any skill plus any help in the same span fires it, while the Library names mentoring a colleague, being a [teacher] or [youth coach], or practice noticed. | `has('teacher') \| has('youth coach') \| had(['a younger colleague needs a mentor', 'a young learner at the kitchen table', 'years of practice are noticed'], 3)` |
| regular at the local | loose | B | mark | Any 'made a friend' after 18 fires it, a school or work friend included, while the Library says years at the same table. | `(age >= 18) & (ago_move > 2) & had(['a seat at the regulars\' table', 'the Tuesday pub quiz', 'a new friend at the community centre'], 3)` |
| inner circle at work | loose | B | title/perk | Five years in any job fires it, while the Library names 'your team lands a big contract', 'you are offered the top job' or a [friend in power]. | `held_career & (yrs_career >= 3) & (had(['your team lands a big contract', 'you are offered the top job'], 3) \| has('friend in power'))` |
| mentor | loose | B | mark | Any skill or any help fires it, while the Library names 'a teacher or coach who believes in you' or an older hand at work. | `had(['a teacher or coach who believes in you', 'a teacher who sees something in you', 'learned from the best'], 2)` |
| friend in power | loose | B | mark | Any three friends fire it, though none need hold power; the Library names a friend who rose high or the boss's boss. | `(mkn('made a friend') >= 3) & NEW:friend in office (a friend tie whose holder has a senior or leading title)` |
| patron | loose | B | mark | Any wild risk plus several skills fire it, while the Library names 'an unexpected chance: a grant, a role, a stage' with money behind it. | `(mkn('learned a skill') >= 4) & had(['an unexpected chance: a grant, a role, a stage', 'a backer for the workshop'], 2)` |
| neighbour who has your back | loose | B | mark | Any friend or help after 18 fires it, none with a neighbour; the Library names new people next door and break-ins on the street. | `(age >= 18) & (ago_move > 1) & had(['new people move in next door', 'break-ins on the street', 'break-ins on your side of town', 'a young neighbour needs help'], 2)` |
| old comrades | loose | B | title/perk | was('soldier') with yrs_career >= 3 counts years in any later job, so a short stint as a soldier then a desk job fires it; the needs name [veteran], which is not a title. | `(was('soldier') & NEW:yrs_was (years a title was held, past or present) >= 3) \| (yrs_has('on the team') >= 5)` |
| machinist | loose | B | mark | Two 'learned a skill' marks of any kind, such as piano lessons, make a machinist, while the words need an apprenticeship or years on a factory floor. | `was('apprentice') \| (has('factory worker') & (yrs_has('factory worker') >= 3))` |
| welder | loose | B | mark | Two 'learned a skill' marks of any kind give welding work, but the words name an apprenticeship or a welding course and tests. | `was('apprentice') \| has('building trade') \| was('factory worker')` |
| commercial pilot | loose | B | title/perk | Any [graduate] or any former [soldier] can become a pilot in time, but the words name flight training paid from savings or loans, or a military flying career. | `(age >= 19) & (age <= 40) & ~has('someone with a record') & (health > .6) & (has('savings') \| (was('soldier') & has('navigation')))` |
| funeral director | loose | B | job-event | Two 'helped someone in need' marks open the funeral trade, which the words never mention; they name a trainee post, often a [family business], and a [strong stomach]. | `(age >= 20) & (has('family business') \| has('strong stomach'))` |
| sound engineer | loose | B | mark | Any two 'learned a skill' marks, such as cooking and bookkeeping, open studio work; the words point to a [musical instrument] and sound mixing. | `has('musical instrument') \| was('stage technician')` |
| stage technician | loose | B | mark | Any two 'learned a skill' marks open stage work, but the words name helping with school or amateur shows and practical skill. | `(age >= 17) & (has('fixing things') \| had(['the school play'], 10))` |
| novelist | loose | B | mark | Any three 'learned a skill' marks make a novelist in time, but the words need a long writing practice and a first book. | `(age >= 20) & (has('writing stories') \| had(['the notebooks come together'], 3))` |
| court interpreter | loose | B | title/perk | [second language] alone gives court work in time, but the words need an interpreting qualification, often after years as a [translator]. | `(age >= 23) & ~has('someone with a record') & has('second language') & (was('translator') \| had(['earning a qualification'], 3))` |
| parent of independent adult children | loose | B | title/perk | ~kids_home also holds when young children live elsewhere, but the words say the youngest has grown up and left home. | `has('mother or father') & held_children & ~kids_home & (kid_young >= 18)` |
| amateur astronomer in a club | loose | B | moment | 'awe' at anything and the general [finding things out] skill also lead to an astronomy club; the words name the night sky, an eclipse or a telescope. | `(age >= 10) & (had(['more stars than anyone could count', 'the sun goes dark at noon'], 10) \| has('good telescope'))` |
| community-radio presenter | loose | B | mark | Any 'learned a skill' mark, such as knitting, opens a radio slot; the words point to [public speaking]. | `(age >= 16) & has('public speaking')` |
| lifeboat volunteer | loose | B | title/perk | Any good swimmer, even far inland, can join lifeboat crew; the words say a coastal station recruits them and they live near it. | `(age >= 17) & (age <= 55) & has('swimming') & (health > .6) & had(['the lifeboat station calls for crew'], 1)` |
| festival organiser | loose | B | mark | Two 'made a friend' marks make a festival organiser; the words name the planning group behind 'a festival comes to town'. | `(age >= 16) & (mkn('made a friend') >= 2) & had(['a festival comes to town', 'the folk festival in the field', 'a festival weekend'], 2)` |
| book-club organiser | loose | B | mark | Any 'made a friend' mark starts a book club; nothing reads a love of books. | `(age >= 16) & mk('made a friend') & has("reader's ticket")` |
| board-game club organiser | loose | B | mark | Any 'made a friend' mark starts a game club; nothing reads a love of games or a game night. | `(age >= 14) & mk('made a friend') & had(['a board game night with the family', 'a chess tournament in the school hall', 'a game of cards with old rivals'], 10)` |
| member of a monastic community | loose | B | title/perk | req reads only no partner and no children, so if `after` does not gate it a single adult with no faith can join; the cause line would name an absence. | `(age >= 18) & ~held_partner & ~kids_home & held_faith & (yrs_faith >= 2)` |
| congregation musician | loose | B | title/perk | req reads only a [musical instrument], so without the `after` gate any player becomes a congregation's musician with no faith at all. | `(age >= 12) & held_faith & (has('musical instrument') \| has('singing'))` |
| interfaith-dialogue participant | loose | B | mark | Any 'made a friend' mark is named as the cause; the words name a shared meal or vigil between congregations. | `(age >= 16) & (yrs_faith >= 2) & had(['the leaders of every faith share a meal', 'an invitation to a dialogue circle', 'a friend takes another faith'], 2)` |
| disability-rights organiser | loose | B | moment | 'a sense of injustice' over anything leads to disability organising; the words name a local barrier met in life. | `(age >= 16) & (had(['living with a chronic illness', 'a serious accident or illness'], 3) \| has('parent coordinating complex support needs') \| has('carer for a parent'))` |
| restorative-justice advocate | loose | B | moment | 'a sense of injustice' over anything is named as the cause; the words name a court case close to home or being 'robbed or attacked in the street'. | `(age >= 18) & (had(['robbed or attacked in the street'], 3) \| was('someone with a record'))` |
| digital-rights advocate | loose | B | title/perk | Being mocked online as a teen or general [finding things out] leads to digital-rights work; the words name surveillance or a data leak. | `(age >= 16) & (has('writing code') \| had(['your name in the leaked files', 'the private files get out'], 3))` |
| doctoral graduate | loose | B | title/perk | Any three 'learned a skill' marks after a degree give a doctorate; the words need research and 'earning a qualification'. | `has('graduate') & (age >= 25) & (age <= 45) & had(['earning a qualification'], 1)` |
| returned migrant | loose | B | mark | 'moved away' and 'came home' marks come from moves and returns within the country too, but the words need years abroad. | `(age >= 20) & mk('came home', 1) & (was('immigrant') \| had(['the first months in a new country'], 40))` |
| seafarer's papers | loose | B | title/perk | 'a trip far from home', such as a school trip, plus [swimming] gives seafarer's papers; the words name a cadetship or 'the itch to be somewhere else'. | `(has('merchant seafarer') \| ((age >= 18) & (age <= 35) & has('swimming') & had(['the itch to be somewhere else'], 2))) & (health >= .45)` |
| sea survival certificate | loose | B | title/perk | Any [trade ticket] or [welder] under 56 can gain it with no offshore work, so 'with [trade ticket]' reads false for a plumber or carpenter. | `has('commercial fisher') \| has('lifeboat volunteer') \| has('merchant seafarer') \| ((has('welder') \| has('rigging ticket')) & NEW:offshore_work (a post on a rig or a wind farm at sea))` |
| fishing licence | loose | B | moment | 'a weekend hike' gives a fishing licence with no fishing, and 'a day at the beach' (ages 3 to 12) only fires at exactly 12; real fishing moments exist but are not read. | `has('hunting and fishing') \| has('commercial fisher') \| ((age >= 12) & had(['fishing the canal with friends', 'a first fish on a grandparent\'s line', 'teaching a grandchild to fish'], 3))` |
| gas safety registration | loose | B | title/perk | The [trade ticket] branch lets a carpenter or welder register to work on gas; the words mean a plumbing or heating trade. | `(has('plumber') & (yrs_career >= 2)) \| (has('trade ticket') & NEW:heating_trade (the ticket earned in plumbing or heating) & (age >= 21))` |
| welding certificate | loose | B | title/perk | An [apprentice] in any trade (a baker's apprentice) with two 'learned a skill' marks, piano lessons included, gains a welding certificate. | `has('welder') \| (has('welding') & (has('apprentice') \| has('machinist') \| has('builder')))` |
| chainsaw ticket | loose | B | title/perk | [fixing things] comes from any 'learned a skill' mark, so a piano lesson can lead to a chainsaw ticket; the words name only [forester], [farmer] and tree work. | `(age >= 16) & (has('forester') \| has('farmer') \| ((has('plot of land') \| has('knowing the woods')) & chance(.1)))` |
| cleared to work with children | loose | B | title/perk | Any community commitment (a chess club, a choir) can bring a children's check through held_community; the words name roles with children or a parent helper. | `(age >= 16) & ~has('someone with a record') & (has('teacher') \| has('youth coach') \| has('foster parent') \| has('adoptive parent') \| has('school-governance board member') \| has('lay religious teacher') \| has('parent-association organiser') \| has('guardian of an unrelated child') \| has('nurse') \| has('paramedic') \| has('physician') \| has('midwife') \| (kids_home & chance(.1)))` |
| celebrant authorisation | loose | B | moment | 'dancing at a wedding' (ages 40 to 65) is being a guest, not being asked to lead one, so 'since dancing at a wedding' reads odd for a licence to marry people. | `(has('civil celebrant') \| has('ordained religious minister') \| (has('public speaking') & had(['a friend\'s wedding', 'the toast at the wedding'], 1) & chance(.2))) & ~has('someone with a record')` |
| diving certificate | loose | B | moment | 'a day at the beach' (ages 3 to 12) is a child's day out, not a week's dive course, so 'since a day at the beach at 10' reads odd. | `has('swimming') & (age >= 10) & (health > .5) & had(['a long-planned trip', 'a trip far from home', 'the fortnight away'], 1)` |
| hives of one's own | loose | B | moment | [growing food] is held by most children (age 14 or under), and 'a new hobby you cannot put down' can be any hobby, so hives come with no sign of bees. | `(age >= 14) & (has('plot of land') \| has('farmer') \| had(['tending an allotment'], 2)) & NEW:bee_hobby (a hobby moment or pick that names bees)` |
| boat of one's own | loose | B | title/perk | Childhood [swimming] plus money buys a boat; the words name [savings] and summers by the water, and swimming only helps. | `(age >= 16) & has('savings') & (has('boat handling') \| has('hunting and fishing'))` |
| horse of one's own | loose | B | moment | 'a pet of your own' can be a hamster, and [handling animals] comes from a dog or cat, so 'since a pet of your own' reads odd for a horse. | `(age >= 6) & (money > .3) & (has('plot of land') \| has('farmer') \| NEW:riding_lessons (years of lessons at a riding school))` |
| good telescope | loose | B | moment | 'awe' is any awe and [finding things out] comes from any 'learned a skill' mark, so a telescope can come with no night sky in it. | `(age >= 10) & (has('amateur astronomer in a club') \| (had(['more stars than anyone could count', 'the sun goes dark at noon'], 3) & chance(.1)))` |
| research grant | loose | B | title/perk | Any [graduate] with five 'learned a skill' marks, music or cooking included, can win a grant; the words name a funded proposal, 'an unexpected chance: a grant, a role, a stage'. | `(age >= 23) & (has('doctoral graduate') \| has('archaeologist') \| has('museum curator') \| has('professional conservator') \| has('archivist') \| (has('graduate') & had(['an unexpected chance: a grant, a role, a stage'], 1)))` |
| machining | loose | B | title/perk | Having been an [apprentice] in any trade (a baker, a hairdresser) with two 'learned a skill' marks gives machining; the words say an engineering apprentice place. | `has('machinist') \| (was('apprentice') & NEW:engineering_apprentice (the apprentice place was in engineering)) \| (has('factory worker') & has('fixing things'))` |
| boat handling | loose | B | moment | 'a day at the beach' with [swimming] gives boat handling with no boat; the words name a sailing club at 'summer camp' or a berth. | `has('merchant seafarer') \| has('commercial fisher') \| has('lifeboat volunteer') \| has('hunting and fishing') \| (has('swimming') & had(['summer camp', 'the river rising on canoe day'], 2))` |
| beekeeping | loose | B | moment | 'a new hobby you cannot put down' can be any hobby, and every [farmer] gains it, so beekeeping comes with no hive. | `has('professional beekeeper') \| has('hives of one\'s own') \| (has('farmer') & chance(.1))` |
| editing | loose | B | title/perk | Any [graduate] with three 'learned a skill' marks gains editing; the words name a student paper, journalism and editorial work. | `has('book editor') \| has('journalist') \| has('doctoral graduate') \| (has('graduate') & (has('writing stories') \| has('reporting')))` |
| writing stories | loose | B | moment | 'the urge to make something' is any making (pottery, a shed), so it gives a writing skill the words tie to notebooks and 'inspiration strikes'. | `has('novelist') \| (had(['inspiration strikes', 'the notebooks come together'], 3) & (mkn('learned a skill') >= 2))` |
| archive research | loose | B | title/perk | Any 40-year-old with [finding things out] gains it; the age stands in for the family tree after 'a grandparent dies' that the words name. | `has('archivist') \| has('museum curator') \| has('archaeologist') \| has('doctoral graduate') \| (has('finding things out') & had(['a grandparent dies', 'a parent dies', 'losing a grandparent'], 3))` |
| lab work | loose | B | title/perk | Any [graduate] under 31 with three 'learned a skill' marks gains lab work; the words say a science degree and a bench. | `has('laboratory technician') \| has('pharmacist') \| has('physician') \| has('veterinarian') \| has('doctoral graduate') \| (has('graduate') & NEW:science_degree (the degree was in a science))` |
| working with data | loose | B | title/perk | Any [graduate] with three 'learned a skill' marks gains it; the words name a statistics course, a growing spreadsheet or 'new technology changes your job'. | `has('data analyst') \| has('accountant') \| has('software developer') \| has('cybersecurity analyst') \| has('doctoral graduate') \| (has('office clerk') & has('bookkeeping')) \| ((has('bookkeeping') \| has('writing code')) & had(['the spreadsheet the last clerk left behind', 'new technology changes your job'], 3))` |
| singing | loose | B | title/perk | The (age <= 14) branch gives singing to any child with no choir, so the cause would be age alone; 'an open rehearsal at the community choir' is named but not read. | `has('choir member') \| has('congregation musician') \| has('amateur band member') \| has('regular worshipper') \| had(['an open rehearsal at the community choir'], 2) \| ((age <= 14) & NEW:school_choir (a child joins the school choir))` |
| organising people | loose | B | title/perk | Two years in any community commitment counts as organising; the words name an organiser's role or being asked to lead. | `has('parent-association organiser') \| has('festival organiser') \| has('shift manager') \| has('founder of a firm') \| (held_community & had(['the club or congregation asks you to lead', 'the parents ask you to run the year\'s events', 'they ask you to lead because you stood up once'], 3))` |
| emergency care | loose | B | title/perk | [first-aid certificate] plus any 'helped someone in need' mark (carrying shopping) gives emergency care; the words name a rescue, 'a stranger saves you, or you save one'. | `has('paramedic') \| has('firefighter') \| has('search-and-rescue volunteer') \| has('lifeboat volunteer') \| has('nurse') \| has('physician') \| has('midwife') \| has('police officer') \| has('soldier') \| (has('first-aid certificate') & had(['a stranger saves you, or you save one'], 2))` |
| source who trusts you | loose | B | title/perk | Any [journalist] or campaigner gains a trusted source with no 'kept your word'; the words need years of it. | `(has('journalist') \| has('digital-rights advocate') \| has('civil-liberties campaigner')) & (mkn('kept your word') >= 2)` |
| on the team | missing | B | age/stage | The engine reads a colour share, not a cause; the Library names 'tryouts for the team', 'sports day' and 'a band or a sport that takes over your life'. | `(age <= 40) & had(['tryouts for the team', 'sports day', 'a band or a sport that takes over your life'], 2)` |
| scout or guide | missing | B | age/stage | Only an age cap, while the Library names a friend bringing them and 'summer camp'. | `(age <= 14) & (mk('made a friend') \| had(['summer camp'], 1))` |
| party member | missing | B | age/stage | Entry is fine, but the in-time path is age only while the Library names 'a bitter election' and a friend's invitation. | `(age >= 18) & (had(['a bitter election', 'election day'], 1) \| mk('made a friend'))` |
| carer for a parent | missing | B | age/stage | Only a living parent and age, so the line would say 'aged 30'; the Library names 'a parent comes to stay for a week' and 'a heart attack or stroke'. | `(alive_parent > 0) & had(['a parent comes to stay for a week', 'a heart attack or stroke', 'a parent unwell and far from a doctor', 'a parent whose care has been cut back'], 2)` |
| second language | missing | B | none | Rate only, while the Library names a parent's tongue, school, 'a trip far from home' and 'you take up an instrument or a language'. | `had(['a trip far from home', 'you take up an instrument or a language', 'learning the local language', 'a weekend school for the old language'], 3) \| NEW:parent_tongue (a parent speaks another mother tongue)` |
| dancing | missing | B | none | Rate only, while the Library names 'dancing at a wedding', classes and 'a festival weekend'. | `had(['dancing at a wedding', 'a festival weekend', 'a beginners\' salsa class'], 2)` |
| hunting and fishing | missing | B | none | Rate only, while the moments 'a first fish on a grandparent's line' and 'fishing the canal with friends' fit the Library's words. | `had(['a first fish on a grandparent\'s line', 'fishing the canal with friends'], 3)` |
| first-aid certificate | missing | B | none | Rate only, but the Library names a day's course at work or with a youth group; 'the firm will pay for one course' exists for the work route. | `had(['the firm will pay for one course'], 1) \| NEW:first-aid course (a day's course at school, work or a youth group)` |
| passport | missing | B | none | Rate only from birth, but the Library names 'a trip far from home' and 'a long-planned trip', which are real moments. | `had(['a trip far from home', 'a long-planned trip', 'the first months in a new country'], 1)` |
| motorbike licence | missing | B | none | Rate only, but the Library names a test at sixteen or seventeen or 'the itch to be somewhere else', a real moment. | `(age >= 16) & ((age <= 18) \| had(['the itch to be somewhere else'], 2))` |
| old family name | missing | B | age/stage | Early-age luck only, but the Library names a family rooted in the town for generations, or marrying into one. | `NEW:old family (a birth flag that the family has lived in the town for generations) \| (has('wife or husband') & NEW:partner from an old family)` |
| teachers' favourite | missing | B | age/stage | Age only, but the Library names 'a test at school tomorrow' passed, and teacher moments exist. | `(age <= 16) & had(['a test at school tomorrow', 'a teacher who sees something in you', 'a teacher or coach who believes in you'], 2)` |
| family who will always take you in | missing | B | age/stage | Birth luck only; the Library also names 'making peace with family you had cut off', a real moment the engine ignores. | `(age <= 4) \| had(['making peace with family you had cut off'], 1)` |
| family business | missing | B | age/stage | Fires only at 14 by age luck, but the Library names a relative's shop or a hand-down, and 'a parent asks you to take over the family shop' exists. | `had(['a parent asks you to take over the family shop'], 1) \| NEW:family business (a birth flag that the family owns a business)` |
| instrument of one's own | missing | B | age/stage | Age only, but real music moments exist: 'a band or a sport that takes over your life', 'you take up an instrument or a language'. | `had(['a band or a sport that takes over your life', 'you take up an instrument or a language', 'a free music school with instruments to borrow'], 2)` |
| baker | missing | B | age/stage | Gained in time at age 16 alone, while the words name early bakery shifts; the engine's [cook] and [shop assistant] routes are not read in req. | `(age >= 16) & (was('cook') \| was('shop assistant'))` |
| partner in a multigenerational household | missing | B | title/perk | It reads only a living parent and no recent move, so couples whose parents live far away get it; a parent moving in is never read. | `has('wife or husband') & (alive_parent > 0) & had(['a parent comes to stay for a week', 'a parent who can no longer live alone', 'a parent asks you to move back home'], 2)` |
| parent with a child living abroad | missing | B | title/perk | Any parent of an 18-year-old can get it; the engine never reads that a child moved to another country. | `has('mother or father') & (yrs_children >= 18) & NEW:child_abroad a grown child has moved to another country` |
| home-educating parent | missing | B | title/perk | Any parent of a school-age child can take it up; the unhappy spell at school or the move the words name is not read. | `has('mother or father') & kids_home & (yrs_children >= 4) & (yrs_children <= 16) & (had(['the school\'s report on the child'], 2) \| (ago_move < 1))` |
| grandparent raising a grandchild | missing | B | title/perk | Any grandparent under 75 can get it in time; the grandchild coming to live with them, which the words name, is never read. | `has('grandparent') & (age <= 75) & had(['you take in a child who needs a home'], 1) & mk('took them in')` |
| parent coordinating complex support needs | missing | B | title/perk | Any parent with a child at home can get it; the assessment or diagnosis that the words start from is never read. | `has('mother or father') & kids_home & NEW:child_assessed a child in the household has an assessment or diagnosis of support needs` |
| choir member | missing | B | age/stage | Gained in time from age 8 alone; the audition or open rehearsal and the [singing] the words name are not read. | `(age >= 8) & (has('singing') \| had(['an open rehearsal at the community choir'], 1))` |
| historical reenactment member | missing | B | age/stage | Gained in time from age 14 alone; the public event at a castle or battlefield is not read, and [period kit] only follows membership. | `(age >= 14) & NEW:heritage_event a public event at a castle or an old battlefield` |
| housing-cooperative member | missing | B | age/stage | It reads only age and no move in a year, while the words say they buy a share or come up the list and move in. | `(age >= 18) & had(['an empty flat in the cooperative'], 1)` |
| adopted person | missing | B | age/stage | Gained at random before age 3 by luck alone; the words name a recorded adoption, which the engine does not record. | `(age < 3.05) & NEW:adoption_record an adoption placing the child with new parents` |
| swimming | fine-age |  | age/stage | Children mostly learn to swim in lessons the life does not show; it keeps its age reading and gets a cause: phrase. | |
| driving licence | fine-age |  | age/stage | The Library's cause is lessons and a test at 17 or so, which is a stage; the engine reads age only and needs a cause phrase. | |
| school-leaving certificate | fine-age |  | age/stage | Most people leave school with one; the end of school is the true cause, so it keeps its age reading and gets a cause: phrase. Requiring an exam moment would make it rare. | |
| family abroad | fine-age |  | age/stage | The [immigrant] path is truthful; the birth path reads only an early age and needs a cause phrase for a family spread over two countries. | |
| godparent who looks out | fine-age |  | age/stage | Chosen at a naming in infancy is a birth stage; the engine reads early age and needs a phrase. The gained text names a faith rite. | |
| a long shot that missed | none-ok |  | none | No Library entry and rate 0: it never comes in time and arrives only through whatever pick or event sets it, which names its own cause. | |
| shop assistant | fine |  | job-event | Career with an empty dict, given through the job event ('a Saturday job at the corner shop', 'your first real job'), which names itself. | |
| waiter or bartender | fine |  | job-event | Career with an empty dict, given through the job event, which names itself. | |
| care worker | fine |  | job-event | Career with an empty dict, given through the job event ('a new job at last'), which names itself. | |
| factory worker | fine |  | job-event | Career with an empty dict, given through the job event, which names itself. | |
| office clerk | fine |  | title/perk | Job-event career gated by [school-leaving certificate], exactly the Library's need. | |
| nurse | fine |  | title/perk | Job-event career gated by [professional registration], which the Library names; the generic registration rule is a separate issue. | |
| teacher | fine |  | title/perk | Gated by [graduate] and [professional registration], as the Library's needs say. | |
| electrician | fine |  | title/perk | Grows from [apprentice] with [trade ticket], matching the Library's path. | |
| builder | fine |  | title/perk | An after title from [apprentice] plus entry through the job event; both match the Library. | |
| shop owner | fine |  | title/perk | Job-event career gated by [savings] or [family business], as the Library's needs say. | |
| soldier | fine |  | job-event | A career title given through the job event; the age and record clauses are gates. | |
| software developer | fine |  | title/perk | Gated by [writing code], the Library's own need; the looseness sits in [writing code]. | |
| shift manager | fine |  | title/perk | Grows from an entry job after a year with [reliable record], matching the Library. | |
| police officer | fine |  | job-event | Job-event career; age and no record are gates that match the Library's needs. | |
| cook | fine |  | job-event | Career with no req, given through the job event; grants only add a certificate. | |
| salesperson | fine |  | job-event | Career with an empty dict, given through the job event ('a job interview'). | |
| delivery driver | fine |  | title/perk | Gated by [driving licence], the Library's need. | |
| accountant | fine |  | title/perk | Gated by [bookkeeping], the Library's need. | |
| estate agent | fine |  | title/perk | Gated by [driving licence], the Library's need. | |
| head chef | fine |  | title/perk | Grows from [cook] after years in the job, as the Library says. | |
| apprentice | fine |  | job-event | A career title given through the job event; the age clause is a gate. | |
| girlfriend or boyfriend | fine |  | job-event | Partner commitment with an empty dict, given through the commitment event ('falling in love'). | |
| living together | fine |  | title/perk | Grows from [girlfriend or boyfriend] after a year, matching 'moving in with a partner'. | |
| engaged | fine |  | title/perk | Grows from a partner title after time together; the lose clause fits 'calling it off'. | |
| married again | fine |  | title/perk | Married with [divorced] or [widowed] before, as the Library says; note those two are not roles in rules.json, so check the engine has them or this never fires. | |
| wife or husband | fine |  | title/perk | Grows from a partner title on marriage with no earlier divorce or loss, as the Library says. | |
| partner of many years | fine |  | title/perk | Grows from a married or living-together title after twenty years, as the Library's needs say. | |
| mother or father | fine |  | job-event | Entry commitment given through the child event ('a child is born'). | |
| single parent | fine |  | title/perk | A parent with kids at home and no partner for a year, matching a breakup, a death or raising alone. | |
| prefect | fine |  | title/perk | Gated by [teachers' favourite], the Library's need. | |
| team captain | fine |  | title/perk | Grows from [on the team] after two seasons, as the Library says. | |
| neighbourhood volunteer | fine |  | mark | 'helped someone in need' leading to volunteering is in line with the Library's words. | |
| union rep | fine |  | mark | Years in a job plus 'defied an authority', the mark the Library names. | |
| local councillor | fine |  | title/perk | Gated by [good name in town], the Library's need. | |
| youth coach | fine |  | title/perk | Once [on the team], with children and age, matching the Library's parent on the touchline. | |
| residents' committee member | fine |  | title/perk | Gated by [homeowner], the Library's need; 'a seat on the residents' committee' could sharpen it later. | |
| club treasurer | fine |  | title/perk | Gated by [bookkeeping] and [reliable record], the Library's needs. | |
| regular worshipper | fine |  | job-event | Faith commitment with an empty dict, given through the faith event. | |
| deacon or elder | fine |  | title/perk | Grows from [regular worshipper] with [known face at worship], as the Library says. | |
| activist in a cause | fine |  | moment | Reads 'a sense of injustice' and 'a protest in your city', both named by the Library. | |
| seeker | fine |  | job-event | A faith commitment started through the commitment event, which names its own moment. | |
| in recovery | fine |  | moment | Follows 'an addiction takes hold', exactly as the Library says. | |
| eldest child | fine |  | age/stage | No older and some younger siblings, the Library's own cause (older_siblings and younger_siblings are not in vocab.txt; check they exist). | |
| homeless | fine |  | money | Almost no money and no ties is the Library's 'nowhere to go'; the cause line reads true. | |
| cooking for a crowd | fine |  | moment | Reads 'learning to cook for yourself' and 'a holiday meal with the whole family', both named by the Library. | |
| building trade | fine |  | title/perk | From [apprentice] or [builder]; the say is a trade in their hands, which an apprenticeship gives. | |
| scripture | fine |  | title/perk | Grows from having been a [regular worshipper], as the Library says; the gained text names real faith schools, so a neutral wording is offered. | |
| professional registration | fine |  | title/perk | Comes with a [graduate] degree under 40, matching the Library's degree, exam and fee. | |
| lorry or bus licence | fine |  | title/perk | Needs a [driving licence] and a job, in line with a course paid by an employer. | |
| trade ticket | fine |  | title/perk | Comes at the end of an [apprentice] stretch or from the [building trade], as the Library says. | |
| hunting licence | fine |  | title/perk | Grows from [hunting and fishing] with no record, matching the Library. | |
| coaching badge | fine |  | title/perk | Grows from having been [on the team], as the Library needs. | |
| referee's badge | fine |  | title/perk | Grows from having been [on the team], as the Library needs. | |
| good name in town | fine |  | mark | Reads several 'kept your word' and 'helped someone in need' while settled, as the Library says; but the loss reads 'hid a wrong', a secret, while the Library says a public scandal. | |
| rank | fine |  | title/perk | Years in a career plus a [reliable record], in line with years of service. | |
| known face at worship | fine |  | title/perk | Years as a [regular worshipper] in one faith, as the Library says. | |
| reliable record | fine |  | mark | Several 'kept your word', exactly as the Library says. | |
| good credit | fine |  | money | Adult with money to spare reads as bills paid on time, in line with the Library. | |
| the one everyone asks | fine |  | mark | Many 'learned a skill' after 25 matches the Library's needs and 'years of practice are noticed'. | |
| following online | fine |  | moment | Reads 'wanting to be noticed', the moment the Library names. | |
| name in the field | fine |  | mark | Ten career years and many skills match the Library's needs for a name in a field. | |
| not to be crossed | fine |  | mark | Several 'made an enemy', as the Library needs. | |
| old school network | fine |  | title/perk | Grows from [graduate], as the Library needs. | |
| sponsor in recovery | fine |  | title/perk | Comes soon after [in recovery], as the Library says. | |
| contact in the trade | fine |  | title/perk | Years in a career, matching years of work done well for the same people. | |
| in-laws who took you in | fine |  | title/perk | Needs a partner title, as the Library says. | |
| savings | fine |  | money | Money left over reads as savings, in line with the Library. | |
| paid-off home | fine |  | title/perk | Twenty years as a [homeowner] reads as the last mortgage payment. | |
| car | fine |  | title/perk | A [driving licence] and some money, as the Library needs. | |
| workplace pension | fine |  | title/perk | Two years in a job after 22, as the Library needs. | |
| plot of land | fine |  | moment | Reads 'tending an allotment' or [farmer], as the Library says. | |
| shares | fine |  | title/perk | [savings] or a pension plus money, in line with the Library. | |
| van and tools | fine |  | title/perk | Trade plus [driving licence], as the Library needs. | |
| flat to rent out | fine |  | title/perk | [savings] or [inheritance] plus [good credit] and money, as the Library needs. | |
| place by the sea | fine |  | title/perk | [savings] or [inheritance] plus money, as the Library needs. | |
| workshop | fine |  | title/perk | Grows from [fixing things], as the Library needs. | |
| laboratory technician | fine |  | job-event | A job title given through a job event, gated on [school-leaving certificate] as the Library needs. | |
| paramedic | fine |  | job-event | A job title given through a job event, gated on registration and a licence as the Library needs. | |
| physician | fine |  | job-event | A job title given through a job event, gated on [graduate] and registration. | |
| psychotherapist | fine |  | title/perk | Grows from [nurse] or [teacher] or comes through a job event, gated on [graduate]; the gained text does not mention the nurse or teacher route. | |
| pharmacist | fine |  | job-event | A job title given through a job event, gated on [graduate] and registration. | |
| veterinarian | fine |  | job-event | A job title given through a job event, gated on [graduate] and registration. | |
| midwife | fine |  | title/perk | Grows from [nurse] or comes through a job event, as the Library says. | |
| firefighter | fine |  | job-event | A job title given through a job event, gated on age, health and no record. | |
| emergency dispatcher | fine |  | title/perk | Grows from the emergency services or comes through a job event, as the Library says. | |
| translator | fine |  | job-event | A job title given through a job event, gated on [second language]. | |
| journalist | fine |  | job-event | A job title given through a job event, gated on [graduate] or [finding things out]. | |
| book editor | fine |  | title/perk | Grows from [journalist] or comes through a job event, gated on [graduate]. | |
| archivist | fine |  | job-event | A job title given through a job event, gated on [graduate]. | |
| museum curator | fine |  | title/perk | Grows from [archivist] or [archaeologist] or comes through a job event. | |
| archaeologist | fine |  | job-event | A job title given through a job event, gated on [graduate]. | |
| land surveyor | fine |  | job-event | A job title given through a job event, gated on [graduate] or the [apprentice] route. | |
| urban planner | fine |  | job-event | A job title given through a job event, gated on [graduate]. | |
| architect | fine |  | job-event | A job title given through a job event, gated on [graduate] and registration. | |
| civil engineer | fine |  | job-event | A job title given through a job event, gated on [graduate]. | |
| data analyst | fine |  | title/perk | Grows from [office clerk] or [accountant] or comes through a job event, in line with the Library. | |
| cybersecurity analyst | fine |  | title/perk | Grows from [software developer] or [data analyst] or comes through a job event, gated on [writing code]. | |
| plumber | fine |  | title/perk | Naming [trade ticket] or [building trade] matches the words' needs exactly. | |
| carpenter | fine |  | title/perk | Naming [building trade] or [trade ticket] matches the words' needs exactly. | |
| cleaner | fine |  | job-event | Empty career rule given only through a job event, which the words also name ('a job interview', an agency placement). | |
| sanitation worker | fine |  | job-event | Career with an age gate only and no rate, so it comes through a job event; the age 18 gate matches the words. | |
| postal worker | fine |  | job-event | Career with an age gate only and no rate, so it comes through a job event; the words name a delivery round, which is that job. | |
| train driver | fine |  | job-event | No rate, so it comes through a job event; the age, health and no-record gate matches the words' needs. | |
| merchant seafarer | fine |  | job-event | No rate, so it comes through a job event; the age and health gate fits a cadetship or first voyage. | |
| commercial fisher | fine |  | job-event | No rate, so it comes through a job event; [family business] or youth plus health is a fair gate for a berth on a boat. | |
| forester | fine |  | job-event | No rate, so it comes through a job event; [graduate] or [apprentice] is what the words themselves ask. | |
| professional beekeeper | fine |  | title/perk | Needs [hives of one's own] together with years of skill, which is the words' own path from a few hives to a business. | |
| civil celebrant | fine |  | job-event | No rate, so it comes through a job event; [public speaking] and no record match the words' needs. | |
| tattoo artist | fine |  | job-event | No rate, so it comes through a job event; [drawing and painting] and age 18 match the words' needs. | |
| video-game developer | fine |  | title/perk | Naming [writing code] or [drawing and painting] matches the words' needs. | |
| professional athlete | fine |  | job-event | No rate, so it comes through a job event; years [on the team], age and health match the words. | |
| professional conservator | fine |  | job-event | No rate, so it comes through a job event; [graduate] is what the words ask. | |
| newlywed | fine |  | title/perk | Naming [wife or husband] or [married again] in its first year is exactly the words' cause. | |
| caregiving partner | fine |  | job-event | No rate, so it comes only from the act in a moment about a partner falling ill, as the words say; held_partner is just the gate. | |
| nonromantic life partner | fine |  | mark | Two 'made a friend' marks with no partner fits two close friends choosing a shared life. | |
| parent raising a child across languages | fine |  | title/perk | Naming [second language], [immigrant] or [family abroad] with a child at home matches the words. | |
| community-garden coordinator | fine |  | moment | Naming 'tending an allotment' or [growing food] matches the words. | |
| repair-cafe volunteer | fine |  | title/perk | Naming [fixing things], [sewing and mending] or [car mechanics] matches the repair skills the words need. | |
| community-mediation volunteer | fine |  | title/perk | Naming [calming people down] fits the words' needs. | |
| search-and-rescue volunteer | fine |  | title/perk | Naming [first-aid certificate] with age and good health matches the words' needs. | |
| school-governance board member | fine |  | title/perk | A child at home or [good name in town] is the words' own 'often' route to a board seat. | |
| parent-association organiser | fine |  | title/perk | A child of school age at home is what the words need. | |
| sports referee | fine |  | title/perk | Naming [referee's badge] matches the words. | |
| amateur band member | fine |  | title/perk | Naming [musical instrument] matches the words. | |
| community-kitchen volunteer | fine |  | mark | 'helped someone in need' is a fair cause for joining a meal service rota. | |
| neighbourhood-watch coordinator | fine |  | moment | Naming 'break-ins on the street' or 'robbed or attacked in the street' matches the words. | |
| prison visitor | fine |  | mark | Repeated 'helped someone in need' is a fair cause for volunteering with a visiting scheme; the words name no other life cause. | |
| ordained religious minister | fine |  | title/perk | Years of faith and [scripture], growing from [regular worshipper], match the words. | |
| lay religious teacher | fine |  | title/perk | Years of faith with [scripture] or [teaching] match the words. | |
| animal-shelter campaigner | fine |  | moment | Naming 'a pet of your own', 'a stray dog follows you home' or [dog of one's own] matches the words. | |
| civil-liberties campaigner | fine |  | moment | Naming 'a sense of injustice', 'a protest in your city' or 'a bitter election' matches the words. | |
| refugee | fine |  | title/perk | Grows from a held [asylum applicant] after half a year, as the words say. | |
| naturalised citizen | fine |  | title/perk | Naming [citizenship] with [immigrant] matches the words. | |
| bankruptcy or insolvency in their history | fine |  | moment | Naming 'financial ruin' matches the words. | |
| on probation or community supervision | fine |  | title/perk | A new [someone with a record] or [ex-prisoner] matches the words. | |
| airline pilot licence | fine |  | title/perk | It comes with [commercial pilot], as the words say. | |
| train driving licence | fine |  | title/perk | It comes with [train driver], as the words say. | |
| site safety card | fine |  | title/perk | Building-site titles and an apprentice in the building trade match the words. | |
| rigging ticket | fine |  | title/perk | A [stage technician] after a year, or [builder] and [welder] crews, as the words say. | |
| chartered status | fine |  | title/perk | Four years in one of the four named professions, as the words say. | |
| food hygiene certificate | fine |  | title/perk | Kitchen, bakery, care and shop titles match the first shift in food work the words describe. | |
| lifeguard qualification | fine |  | title/perk | [swimming], age 16 or more and good health are the words' own needs for the pool course. | |
| tattoo licence | fine |  | title/perk | It comes with [tattoo artist], as the words say. | |
| court interpreter accreditation | fine |  | title/perk | [court interpreter] or years as a [translator], no record, age 23 or more, as the words say. | |
| press card | fine |  | title/perk | A first year as a [journalist], as the words say. | |
| therapy accreditation | fine |  | title/perk | It comes with [psychotherapist]; the rare nurse or teacher route with [calming people down] matches the words. | |
| mediation accreditation | fine |  | title/perk | It comes with the two named mediation roles, and the career route needs [calming people down] as the words do. | |
| reader's ticket | fine |  | title/perk | [finding things out], [graduate] or a death in the family match the family history, thesis and book the words name. | |
| permanent residence | fine |  | title/perk | Years as an [immigrant] or a [refugee] without [citizenship], as the words say. | |
| share in a fishing boat | fine |  | title/perk | Years as a [commercial fisher] with [savings], an [inheritance] or a [family business], as the words say. | |
| studio of one's own | fine |  | title/perk | [tattoo artist], [sound engineer], or an art or instrument with rent money, as the words say. | |
| premises of one's own | fine |  | title/perk | [shop owner] or a practice title with money matches a lease for a practice of their own; 'a chance to start a business of your own' could be added later. | |
| period kit | fine |  | title/perk | It comes with [historical reenactment member], as the words say. | |
| stake in the firm | fine |  | title/perk | Years in a practice title, [inner circle at work] or a [family business], as the words say. | |
| collection of one's own | fine |  | moment | 'a curiosity that will not let go', a new hobby and 'an unexpected legacy' match the words. | |
| tools of one's own | fine |  | title/perk | Trade titles buy their own tools, as the words say. | |
| camper van | fine |  | moment | [driving licence], money and the named moments or an empty nest match the words ('retiree' is not in rules.json, so check that title exists). | |
| secure tenancy | fine |  | money | Low money and years in place, [homeless] or 'losing the home' match the waiting list and housing need in the words. | |
| welding | fine |  | title/perk | [welder], a farm or a garage trade matches the words. | |
| baking | fine |  | title/perk | [baker], [cook], [cooking for a crowd] or 'learning to cook for yourself' match the kitchen the words describe. | |
| restoring old things | fine |  | title/perk | [fixing things] or [sewing and mending] is the words' own need; 'a chair rescued from a skip' and 'a broken lamp at the repair cafe' could be read too. | |
| navigation | fine |  | title/perk | The named titles and 'a weekend hike' match the words. | |
| sea legs | fine |  | title/perk | A berth at sea or [boat handling], as the words say. | |
| knowing the woods | fine |  | title/perk | [forester], [hunting and fishing], a [scout or guide] troop or 'a long walk alone' match the words. | |
| handling animals | fine |  | title/perk | A farm, a pet, the shelter or a vet's training, as the words say. | |
| interpreting | fine |  | title/perk | [second language] with an [immigrant] or [refugee] life, or the interpreting titles, match the words. | |
| reporting | fine |  | title/perk | [journalist], a radio show, or [finding things out] with [writing stories] match the words. | |
| keeping systems secure | fine |  | title/perk | [writing code] is the words' own need, plus the security titles. | |
| sound mixing | fine |  | title/perk | Band, church, radio and stage titles running the desk match the words. | |
| stagecraft | fine |  | title/perk | Stage titles or 'the school play' with [fixing things] match the words. | |
| counselling | fine |  | title/perk | [calming people down] after many 'helped someone in need' marks, or the pastoral titles, as the words say. | |
| leading a ceremony | fine |  | title/perk | The ceremony titles, or [public speaking] after 'a memorial service for a friend', as the words say. | |
| settling disputes | fine |  | title/perk | The mediation, union and manager titles, or [calming people down], match the words. | |
| campaigning | fine |  | title/perk | Campaign titles and the named protests match the words. | |
| handling red tape | fine |  | title/perk | Caring, migrant and business titles, or the named paperwork moments, match the words. | |
| strong stomach | fine |  | title/perk | The ambulance, ward, funeral and farm titles match the words. | |
| used to night shifts | fine |  | title/perk | Night-work titles match the words; the loss reads any end of career, not a move to a day job. | |
| head for heights | fine |  | title/perk | Height titles, or [keeping fit] with 'took a wild risk', which is the words' own need. | |
| keeping fit | fine |  | title/perk | Sport and fitness titles and the named moments match the words. | |
| book in print | fine |  | title/perk | Writing titles and [writing stories] match the words. | |
| published research | fine |  | title/perk | Research and clinical titles match the words. | |
| loyal clientele | fine |  | title/perk | Three years in a client-facing trade, as the words say. | |
| voice at the town hall | fine |  | title/perk | Civic titles, or [good name in town] with years in the community, match the words. | |
| name on the local scene | fine |  | title/perk | Scene titles match the gigs, shows and festivals in the words. | |
| trusted with the keys | fine |  | title/perk | [reliable record] or a key-holding role matches the words. | |
| trophies won | fine |  | title/perk | Seasons [on the team] or a sport title match the words. | |
| crew that has your back | fine |  | title/perk | Crew titles that work in danger or under pressure match the words. | |
| apprentice of one's own | fine |  | title/perk | Five years in a named trade, as the words say. | |
| carers' group | fine |  | title/perk | A caring role, as the words say. | |
| people from home | fine |  | title/perk | A migrant title, or a recent 'moved away', matches the words. | |
