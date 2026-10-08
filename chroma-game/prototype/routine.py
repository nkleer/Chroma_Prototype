"""Everyday routine lines for the interlude between moments (game-side built-in lines)."""

import re
import string
from collections import Counter

ROUTINE = [
    # (text, when)

    # ------------------------------------------------------------------
    # Modern Earth (E): any age
    # ------------------------------------------------------------------
    ("Rain ticks against the kitchen window most mornings, and the radiator clanks awake a few minutes after {N} does.", dict(age=(0, 110), world="E")),
    ("The streetlight outside {N}'s window flickers on at dusk and hums faintly until the first bus goes by.", dict(age=(0, 110), world="E")),
    ("Every Monday night {N} hears the whole street dragging its bins to the kerb in the dark.", dict(age=(0, 110), world="E")),
    ("The neighbour's cat sits on {N}'s windowsill every afternoon as though it pays rent there.", dict(age=(0, 110), world="E")),
    ("Sunday mornings in {N}'s home smell of toast, and the radio talks quietly to whoever is listening.", dict(age=(0, 110), world="E")),
    ("Saturdays begin with the washing machine thumping through its spin cycle, and {N}'s whole home shakes along with it.", dict(age=(0, 110), world="E")),
    ("Somewhere in the building a pipe knocks every night, and {N} has long since stopped hearing it.", dict(age=(0, 110), world="E")),
    ("Dinner at {N}'s table is at six, give or take the length of the news.", dict(age=(0, 110), world="E")),
    ("The {place} sounds different on Sunday mornings, and {N} can tell the day without looking at a calendar.", dict(age=(4, 110), world="E")),

    # ------------------------------------------------------------------
    # Modern Earth: toddlers
    # ------------------------------------------------------------------
    ("Naps come after lunch with one sock always missing, while the afternoon light moves slowly across {N}'s cot.", dict(age=(0, 3), world="E")),
    ("The whole household tiptoes around {N}'s nap schedule, and the doorbell has a handwritten note taped over it.", dict(age=(0, 2), world="E")),
    ("Breakfast is porridge in the high chair, and roughly a third of it ends up on {N}'s bib or the floor.", dict(age=(0, 3), world="E")),
    ("Each morning {N} rides to the shops in a pushchair, pointing at every dog, pigeon, and bus along the way.", dict(age=(0, 4), world="E")),
    ("Bath time comes after dinner, with a plastic duck, far too many bubbles, and {N} refusing to get out.", dict(age=(1, 6), world="E")),
    ("When the bin lorry comes on Tuesdays, {N} waves from the front window at the crew in orange vests.", dict(age=(1, 6), world="E")),
    ("Most afternoons {N} builds block towers on the living room rug and knocks them down with great satisfaction.", dict(age=(1, 6), world="E")),
    ("The same picture book gets read every night, and {N} corrects anyone who tries to skip a page.", dict(age=(2, 6), world="E")),
    ("Nursery drop-off is at eight, and {N} always needs one more hug at the gate before going in.", dict(age=(2, 5), world="E")),
    ("{parent} sings the same off-key song at bedtime, and {N} is usually asleep before the second verse.", dict(age=(0, 6), world="E", need=("parent_alive",))),
    ("Any jingle on the television sets {N} dancing, bouncing at the knees with both arms in the air.", dict(age=(1, 6), world="E", color="R")),
    ("In the garden {N} digs for worms with a plastic spade and gives each one a name.", dict(age=(2, 6), world="E", color="G")),
    ("Every morning the kitchen cupboards get emptied, and {N} lines up the tins by size on the lino.", dict(age=(1, 5), world="E", color="U")),
    ("At nursery {N} is the one who tidies the toy cars into neat rows before anyone asks.", dict(age=(3, 6), world="E", color="W")),
    ("Puddle walks happen whenever it rains, in yellow wellies that are slowly getting too small for {N}.", dict(age=(2, 6), world="E", season="autumn")),
    ("On hot days {N} splashes in a paddling pool on the lawn, squealing whenever the hose comes out.", dict(age=(1, 6), world="E", season="summer")),

    # ------------------------------------------------------------------
    # Modern Earth: children
    # ------------------------------------------------------------------
    ("The walk to school takes twelve minutes, or twenty if {N} stops to inspect every interesting stick.", dict(age=(5, 11), world="E")),
    ("Homework happens at the kitchen table while dinner cooks, and {N} sighs heavily over long division.", dict(age=(8, 13), world="E")),
    ("Football stickers get traded at break time, and {N} keeps the shiny ones in a biscuit tin under the bed.", dict(age=(7, 12), world="E")),
    ("Saturday mornings mean cartoons in pyjamas until someone calls breakfast for the third time and {N} wanders in.", dict(age=(6, 13), world="E")),
    ("Spelling tests are on Fridays, so on Thursday nights {N} practises the list out loud in the bath.", dict(age=(6, 11), world="E")),
    ("Most afternoons {N} rides a bike in slow circles around the close until the streetlights come on.", dict(age=(7, 13), world="E")),
    ("Mondays are hamster days, and {N} feeds the class pet with enormous seriousness and a tiny scoop.", dict(age=(6, 11), world="E", color="W")),
    ("A broken alarm clock lives on {N}'s desk, and most evenings another piece of it comes off.", dict(age=(8, 13), world="E", color="U")),
    ("At break time {N} sells old comics to classmates, always at a small and carefully calculated profit.", dict(age=(8, 13), world="E", color="B")),
    ("Every walk home becomes an expedition, with {N} climbing low walls and taking the long way through the woods.", dict(age=(7, 13), world="E", color="R")),
    ("{N} and {friend} walk home together every day, arguing about which superhero would win.", dict(age=(7, 13), world="E", need=("friend",))),
    ("{N} has the same argument about screen time with {parent} every evening, and it always ends the same way.", dict(age=(8, 13), world="E", need=("parent_alive",))),
    ("In spring {N} hunts for frogspawn in the park pond with a jam jar and wet sleeves.", dict(age=(5, 12), world="E", color="G", season="spring")),
    ("Summer holidays mean long days at the park, ice lollies, and {N} coming home with grass on everything.", dict(age=(6, 13), world="E", season="summer")),
    ("Autumn means a new pencil case, new shoes that pinch, and {N} learning a new teacher's habits all over again.", dict(age=(5, 13), world="E", season="autumn")),
    ("On winter mornings {N} draws faces in the frost on the bus window all the way to school.", dict(age=(6, 13), world="E", season="winter")),
    ("Hand-me-down school jumpers still have someone else's name inside the collar, and {N} has stopped minding.", dict(age=(5, 16), world="E", need=("poor",))),
    ("Tuesdays after school mean {circle}, and {N} comes home starving and full of news.", dict(age=(7, 16), world="E", need=("community",))),
    ("An inhaler lives in the front pocket of {N}'s school bag, and {N} always knows exactly where it is.", dict(age=(6, 18), world="E", need=("in_poor_health",))),

    # ------------------------------------------------------------------
    # Modern Earth: teenagers
    # ------------------------------------------------------------------
    ("Most school mornings {N} sleeps through two alarms and eats toast on the way to the bus stop.", dict(age=(13, 18), world="E")),
    ("In the evenings {N} does homework with headphones in, one playlist on repeat, and the phone face down, mostly.", dict(age=(13, 18), world="E")),
    ("Saturday afternoons go to the shopping centre with friends, where {N} buys almost nothing and stays for hours.", dict(age=(13, 18), world="E")),
    ("Group chats buzz until midnight, and {N} reads every message even when there is nothing to say.", dict(age=(13, 20), world="E")),
    ("After dinner {N} sulks upstairs most nights, then comes down at ten looking for cereal.", dict(age=(13, 17), world="E")),
    ("Twenty minutes go into {N}'s hair every morning, and the wind undoes it in two.", dict(age=(13, 18), world="E")),
    ("{N} does the washing up every night as part of a deal with {parent} that nobody remembers making.", dict(age=(12, 18), world="E", need=("parent_alive",))),
    ("On Sundays {N} volunteers at the food bank with {parent}, sorting tins into neat rows by date.", dict(age=(13, 18), world="E", need=("parent_alive",), color="W")),
    ("Revision timetables cover {N}'s bedroom wall in colour codes, and about half of them get followed.", dict(age=(14, 19), world="E", need=("student",), color="U")),
    ("Friday nights mean horror films at someone's house with {friend}, both of them pretending not to be scared.", dict(age=(13, 19), world="E", need=("friend",), color="R")),
    ("Guitar practice happens every evening behind a firmly shut door, and {N} has mastered the same four chords.", dict(age=(12, 18), world="E", color="R")),
    ("Between lessons {N} checks resale prices for trainers online with the steady focus of a stockbroker.", dict(age=(13, 18), world="E", color="B")),
    ("Walking the dog round the block after school is the one time each day {N}'s phone stays in a pocket.", dict(age=(11, 18), world="E", color="G")),
    ("{N} keeps a close eye on the class rankings each term and studies hardest just before they are posted.", dict(age=(12, 18), world="E", need=("student",), color="B")),
    ("Exam season means late nights at the desk, flashcards on every surface, and {N} eating dinner one-handed.", dict(age=(15, 25), world="E", need=("student",), season="spring")),
    ("During homework {N} chews the end of every pen and has a drawer full of ruined biros.", dict(age=(11, 18), world="E", need=("stressed",))),

    # ------------------------------------------------------------------
    # Modern Earth: young adults and general adult life
    # ------------------------------------------------------------------
    ("Most weeks {N} lives on pasta and toast, and the fridge holds condiments and good intentions.", dict(age=(18, 26), world="E")),
    ("The flat's cleaning rota is still on the fridge, and {N} is still the only one who reads it.", dict(age=(18, 28), world="E")),
    ("Rent day comes on the first, and {N} checks the bank balance twice before and once after.", dict(age=(18, 35), world="E")),
    ("Sunday evenings mean {N} cooks five identical lunches that are already boring by Wednesday.", dict(age=(20, 40), world="E")),
    ("Three mornings a week {N} runs along the canal, timing every lap on a cheap watch.", dict(age=(18, 55), world="E")),
    ("Laundry happens at the launderette on Sundays, where {N} reads old magazines while the dryers turn.", dict(age=(18, 30), world="E")),
    ("On Friday nights {N} has a cheap pint with friends at the same pub, the same table, the same arguments.", dict(age=(18, 35), world="E", color="R")),
    ("Saturday nights {N} goes dancing until the last bus, then eats chips from the paper on the walk home.", dict(age=(18, 40), world="E", color="R")),
    ("The weekly shop happens on Thursday evenings, and {N} always forgets the one thing that started the list.", dict(age=(20, 90), world="E")),
    ("Most Fridays {N} falls asleep on the sofa before the film reaches its second act.", dict(age=(30, 90), world="E")),
    ("Hoovering the stairs happens on Saturday mornings, and {N} leaves the top step for later every single time.", dict(age=(25, 110), world="E")),
    ("Breakfast is eaten standing at the counter most days, with {N} reading the cereal box like a newspaper.", dict(age=(10, 110), world="E")),
    ("Twice a week {N} loses the keys and finds them in the first place already checked.", dict(age=(14, 110), world="E")),
    ("{N} reads the news on the phone each morning and then, against all advice, reads the comments.", dict(age=(16, 90), world="E")),
    ("Before buying anything, even a kettle, {N} reads every single review and then buys the first one anyway.", dict(age=(35, 110), world="E")),

    # ------------------------------------------------------------------
    # Modern Earth: older adults and elders
    # ------------------------------------------------------------------
    ("Getting up from the sofa now comes with a small groan, and {N} has started doing it for effect.", dict(age=(50, 110), world="E")),
    ("Reading glasses live in every room, and {N} still cannot find a pair when the post arrives.", dict(age=(48, 110), world="E")),
    ("Morning stretches by the bed are mostly a conversation between {N} and two opinionated knees.", dict(age=(50, 110), world="E")),
    ("After lunch {N} naps in the armchair with the radio on and insists afterwards on having heard every word.", dict(age=(65, 110), world="E")),
    ("The stairs take a little longer every year, so {N} keeps a book on the landing for the rest stop.", dict(age=(70, 110), world="E")),
    ("The local paper gets read front to back every morning, notices first and weather last, while {N}'s tea goes cold.", dict(age=(65, 110), world="E")),
    ("At nine each morning {N} walks to the bakery, and the usual loaf is wrapped before the door has closed.", dict(age=(65, 110), world="E")),
    ("Every afternoon {N} takes a slow loop of the park and nods to the same dog walkers by the pond.", dict(age=(65, 110), world="E")),
    ("Phone calls at {N}'s house are taken in the hallway, standing up, and conducted at considerable volume.", dict(age=(70, 110), world="E")),
    ("The six o'clock quiz is a nightly fixture, with {N} answering out loud and arguing with the host.", dict(age=(55, 110), world="E")),

    # ------------------------------------------------------------------
    # Modern Earth: work, study, retirement
    # ------------------------------------------------------------------
    ("Mornings start with the 7:40 bus; {N} reads the same paperback for a month.", dict(age=(18, 64), world="E", need=("career",))),
    ("Every payday {N} buys a proper coffee instead of the office one and makes it last all morning.", dict(age=(18, 66), world="E", need=("career",))),
    ("Over dinner {N} talks about life as {job} until someone gently changes the subject.", dict(age=(20, 70), world="E", need=("career",))),
    ("Commuting means the same platform, the same faces, and {N} nodding to people whose names remain a mystery.", dict(age=(20, 66), world="E", need=("career",))),
    ("After a long day working as {job}, {N} puts both feet up on the coffee table and refuses to move.", dict(age=(20, 70), world="E", need=("career",))),
    ("The office kettle is always empty when {N} gets to it, and refilling it has become a quiet duty.", dict(age=(18, 66), world="E", need=("career",), color="W")),
    ("{N} arrives at work ten minutes before the boss every day, and makes sure the boss notices.", dict(age=(20, 66), world="E", need=("career",), color="B")),
    ("On the morning train {N} reads industry news, quietly working out who is getting promoted next.", dict(age=(22, 66), world="E", need=("career",), color="B")),
    ("Friday drinks with colleagues are where {N} does business, remembering every child's name and the boss's golf handicap.", dict(age=(22, 66), world="E", need=("career",), color="B")),
    ("{N} keeps a notebook of small ideas for working better as {job}, and tries one of them each week.", dict(age=(20, 66), world="E", need=("career",), color="U")),
    ("Loud music fills the drive to work, and {N} arrives already halfway into a good mood.", dict(age=(18, 66), world="E", need=("career",), color="R")),
    ("The same blue lunchbox comes to work every day, and {N} eats from it on the same bench outside.", dict(age=(20, 66), world="E", need=("career",), color="G")),
    ("Every winter {N} catches the same cold in the same week and blames the same colleague.", dict(age=(20, 66), world="E", need=("career",), season="winter")),
    ("Lectures start at nine, and {N} usually arrives at quarter past with a coffee and no pen.", dict(age=(18, 25), world="E", need=("student",))),
    ("The library's third floor has a desk by the radiator, and {N} claims it most afternoons.", dict(age=(18, 30), world="E", need=("student",), color="U")),
    ("{N} studies at the kitchen table after the others go to bed, highlighters lined up by colour.", dict(age=(16, 60), world="E", need=("student",))),
    ("Retirement means the morning paper read all the way through, including the parts {N} used to skip.", dict(age=(55, 110), world="E", need=("retired",))),
    ("Still waking at six from decades of work, {N} now has nowhere in particular to be.", dict(age=(55, 110), world="E", need=("retired",))),
    ("Weekday mornings the supermarket is quiet, and {N} pushes the trolley slowly down every single aisle.", dict(age=(58, 110), world="E", need=("retired",))),
    ("Two mornings a week {N} volunteers at the charity shop, pricing jumpers and discussing the weather at length.", dict(age=(58, 110), world="E", need=("retired",), color="W")),
    ("{N} minds the grandchildren on Wednesdays, and the afternoon always ends with biscuits and a muddy park.", dict(age=(55, 110), world="E", need=("retired", "children"), color="G")),

    # ------------------------------------------------------------------
    # Modern Earth: home life and people
    # ------------------------------------------------------------------
    ("{N} and {partner} split the cooking: one chops, one stirs, and both of them taste too often.", dict(age=(20, 110), world="E", need=("partner",), color="G")),
    ("{partner} always takes the left side of the bed, and {N} stopped arguing about it years ago.", dict(age=(25, 110), world="E", need=("partner",))),
    ("On Sundays {N} and {partner} do the crossword together, arguing over clues neither of them knows.", dict(age=(25, 110), world="E", need=("partner",), color="U")),
    ("A cup of tea goes from {N} to {partner} every morning, a habit older than either of them can remember.", dict(age=(40, 110), world="E", need=("partner",))),
    ("While the pasta water boils on Saturdays, {N} and {partner} dance badly around the kitchen.", dict(age=(18, 80), world="E", need=("partner",), color="R")),
    ("On the last Sunday of each month {N} and {partner} sit down with the bills and a pot of tea.", dict(age=(25, 90), world="E", need=("partner",), color="W")),
    ("The school run starts at eight, with {child} hunting for one shoe and {N} hunting for the car keys.", dict(age=(25, 50), world="E", need=("children",))),
    ("Bedtime takes {N} an hour most nights, with {child} asking for water, then a story, then more water.", dict(age=(22, 45), world="E", need=("children",))),
    ("Every Sunday {N} stands on the touchline at {child}'s football with a thermos and frozen fingers.", dict(age=(28, 55), world="E", need=("children",))),
    ("{child} calls every Sunday evening, and {N} has the kettle on and a chair pulled up beside the phone.", dict(age=(55, 110), world="E", need=("children",), color="G")),
    ("Old drawings by {child} still curl on the fridge door, long after the fridge has run out of room.", dict(age=(35, 110), world="E", need=("children",))),
    ("At the kitchen table {N} helps {child} with maths homework, after quietly checking the answers online first.", dict(age=(30, 55), world="E", need=("children",), color="U")),
    ("Cooking for one most nights, {N} has become quite good at halving recipes without a calculator.", dict(age=(22, 110), world="E", need=("no_partner",))),
    ("The whole bed, the whole duvet, and the whole remote belong to {N}, and all three get used generously.", dict(age=(18, 110), world="E", need=("no_partner",))),
    ("On Friday nights {N} orders a takeaway for one and watches whatever nobody else would have agreed to.", dict(age=(20, 90), world="E", need=("no_partner",))),
    ("Weekends belong to {N} alone, and most of them start with a long, unhurried bath and the radio.", dict(age=(20, 110), world="E", need=("no_partner",))),
    ("Friends keep offering to set {N} up with someone, and {N} keeps politely changing the subject.", dict(age=(22, 60), world="E", need=("no_partner",))),
    ("{N} and {friend} have a standing call on Sunday afternoons that always runs an hour too long.", dict(age=(16, 110), world="E", need=("friend",))),
    ("{friend} comes round on Thursday nights with crisps, and {N} supplies the complaints about the week.", dict(age=(20, 110), world="E", need=("friend",))),
    ("Once a month {N} and {friend} meet at the same café and order the same lemon cake.", dict(age=(35, 110), world="E", need=("friend",))),
    ("Every dog {N} passes on the walk to the shops gets photographed for {friend}, who replies with scores.", dict(age=(18, 66), world="E", need=("friend",), color="R")),
    ("Every Sunday evening {N} rings {parent} and hears the week's news about neighbours {N} has never met.", dict(age=(20, 80), world="E", need=("parent_alive",))),
    ("On Saturdays {N} drives {parent} to the supermarket and carries the bags up without being asked.", dict(age=(35, 80), world="E", need=("parent_alive",), color="W")),
    ("{parent} still posts {N} newspaper clippings, folded small, about things {N} once mentioned liking.", dict(age=(25, 75), world="E", need=("parent_alive",))),

    # ------------------------------------------------------------------
    # Modern Earth: faith and belonging
    # ------------------------------------------------------------------
    ("Before every meal {N} says a short prayer under their breath, even when eating alone.", dict(age=(6, 110), world="E", need=("faith",))),
    ("Each morning before breakfast {N} prays in the same quiet corner of the bedroom.", dict(age=(10, 110), world="E", need=("faith",))),
    ("On holy days {N} cooks the old dishes, and the kitchen smells exactly as it did in childhood.", dict(age=(25, 110), world="E", need=("faith",), color="G")),
    ("Every week {N} helps set out chairs at the place of worship, and stacks them again afterwards.", dict(age=(12, 110), world="E", need=("faith",), color="W")),
    ("A few verses get read each night before sleep, and {N} marks the page with an old bus ticket.", dict(age=(12, 110), world="E", need=("faith",))),
    ("Thursdays belong to {circle}, and {N} would cancel almost anything else before missing a week.", dict(age=(13, 110), world="E", need=("community",))),
    ("{N} makes the tea at {circle} every week, because somebody has to and {N} knows where the cups go.", dict(age=(18, 110), world="E", need=("community",), color="W")),
    ("After {circle} on Wednesdays {N} has one drink with the regulars and is home by ten.", dict(age=(18, 110), world="E", need=("community",))),
    ("A lucky jumper goes to {circle} every week, and {N} washes it only with great reluctance.", dict(age=(10, 110), world="E", need=("community",), color="R")),

    # ------------------------------------------------------------------
    # Modern Earth: circumstances and moods
    # ------------------------------------------------------------------
    ("Dinner plans follow the yellow stickers, with {N} shopping late in the day for whatever has been reduced.", dict(age=(18, 110), world="E", need=("poor",))),
    ("Near the end of each month {N} counts coins on the kitchen table to see how far the week can stretch.", dict(age=(18, 110), world="E", need=("poor",))),
    ("All winter {N} wears two jumpers indoors so the heating can stay off a little longer.", dict(age=(16, 110), world="E", need=("poor",), season="winter")),
    ("Walking instead of taking the bus saves {N} a little money most days and fills an hour.", dict(age=(14, 110), world="E", need=("poor",))),
    ("Groceries arrive by delivery on Thursdays, and {N} still somehow nips out for one forgotten thing.", dict(age=(25, 110), world="E", need=("wealthy",))),
    ("Most Saturdays {N} plays a round of golf, mainly for the lunch at the clubhouse afterwards.", dict(age=(35, 90), world="E", need=("wealthy",))),
    ("A cleaner comes on Wednesdays, and {N} tidies up beforehand so as not to be quietly judged.", dict(age=(25, 110), world="E", need=("wealthy",))),
    ("First class on the Monday train suits {N}, with the financial pages folded neatly into quarters.", dict(age=(30, 70), world="E", need=("wealthy",), color="B")),
    ("{N} checks work email in bed at night, again at six, and again in the queue for coffee.", dict(age=(20, 66), world="E", need=("career", "stressed"))),
    ("Lists of lists cover the hall table, and {N}'s to-do pile somehow never shrinks.", dict(age=(18, 90), world="E", need=("stressed",))),
    ("Around three most nights {N} lies awake running through tomorrow, then sleeps straight through the alarm.", dict(age=(16, 90), world="E", need=("stressed",))),
    ("Lunch most days is a cereal bar eaten at a red light, with {N} already ten minutes late.", dict(age=(22, 66), world="E", need=("stressed",))),
    ("{N} hums while washing up, usually something from the radio and usually with the wrong words.", dict(age=(6, 110), world="E", need=("happy",))),
    ("Most mornings {N} says good morning to the bus driver and actually means it.", dict(age=(10, 110), world="E", need=("happy",))),
    ("Roughly once a week {N} buys flowers from the corner shop on the way home, for no reason at all.", dict(age=(18, 110), world="E", need=("happy",))),
    ("On the morning walk {N} waves at neighbours and stops to chat longer than strictly necessary.", dict(age=(30, 110), world="E", need=("happy",))),
    ("{N} sits in the parked car outside the house a little longer each evening before going in.", dict(age=(25, 90), world="E", need=("unhappy",))),
    ("Most evenings {N} scrolls the phone in bed until the screen dims, without really reading any of it.", dict(age=(13, 90), world="E", need=("unhappy",))),
    ("Breakfast gets skipped most mornings, and {N}'s days start grey whatever the weather is doing.", dict(age=(13, 110), world="E", need=("unhappy",))),
    ("Weekends drift by in pyjamas, with {N} meaning to go out and somehow never quite managing it.", dict(age=(16, 90), world="E", need=("unhappy",))),
    ("{N} talks to the cat over breakfast, and the cat, to be fair, is a decent listener.", dict(age=(18, 110), world="E", need=("lonely",))),
    ("The television stays on for company, and {N} knows the evening presenters' voices better than anyone's.", dict(age=(20, 110), world="E", need=("lonely",))),
    ("At the checkout {N} lingers, because the cashier's small talk is often the longest chat of the day.", dict(age=(30, 110), world="E", need=("lonely",))),
    ("At lunchtime {N} eats alone at the end of the long canteen table, reading the same book slowly.", dict(age=(11, 30), world="E", need=("lonely",))),
    ("Sunday afternoons stretch long, and {N} sets the table for one with a proper cloth anyway.", dict(age=(60, 110), world="E", need=("lonely",), color="G")),
    ("The first tea of the day gets drunk at the back door, with {N} watching the sky decide what to do.", dict(age=(16, 110), world="E", need=("calm",))),
    ("Evenings end with {N} folding laundry in front of the news, one warm towel at a time.", dict(age=(20, 110), world="E", need=("calm",))),
    ("A jigsaw takes over the dining table for weeks at a time, and {N} will not be rushed with it.", dict(age=(8, 110), world="E", need=("calm",))),
    ("{N} takes the slow road through the {place}, the one lined with trees, and never minds the extra minutes.", dict(age=(18, 90), world="E", need=("calm",))),
    ("Every few months {N} rearranges the living room furniture, then quietly puts most of it back.", dict(age=(18, 110), world="E", need=("restless",))),
    ("During phone calls {N} paces the hallway and has worn a faint track into the carpet.", dict(age=(14, 110), world="E", need=("restless",))),
    ("Every few weekends {N} gets a train somewhere new, walks around for an afternoon, and comes back.", dict(age=(18, 80), world="E", need=("restless",), color="R")),
    ("{N} browses job adverts on the bus most mornings, not really looking, just looking.", dict(age=(20, 60), world="E", need=("career", "restless"))),
    ("Every Sunday night {N} sorts pills into a plastic week-box, morning and evening, Monday to Sunday.", dict(age=(40, 110), world="E", need=("in_poor_health",))),
    ("The doctor's waiting room has the same magazines every month, and {N} has read all of them twice.", dict(age=(30, 110), world="E", need=("in_poor_health",))),
    ("{N} takes the stairs one at a time now, resting halfway at the window over the car park.", dict(age=(55, 110), world="E", need=("in_poor_health",))),
    ("The queue at the pharmacy is long every Thursday, and {N} knows most of the people in it by now.", dict(age=(40, 110), world="E", need=("in_poor_health",))),

    # ------------------------------------------------------------------
    # Modern Earth: leading colour in free time
    # ------------------------------------------------------------------
    ("Every evening {N} sorts the recycling into four boxes and gently corrects anyone who gets it wrong.", dict(age=(10, 110), world="E", color="W")),
    ("Each morning {N} knocks on the old neighbour's door, just to check the milk has been taken in.", dict(age=(20, 110), world="E", color="W")),
    ("{N} writes birthday cards weeks ahead and lines them up on the mantelpiece, stamped and ready.", dict(age=(55, 110), world="E", color="W")),
    ("Podcasts about history play while {N} cooks, and the best facts get repeated at dinner.", dict(age=(16, 110), world="E", color="U")),
    ("On Sundays {N} fixes small appliances at the kitchen table, screws laid out in order on a tea towel.", dict(age=(20, 110), world="E", color="U")),
    ("Every weekend gets planned on a spreadsheet, and {N} includes a column for rainy-day alternatives.", dict(age=(20, 80), world="E", color="U")),
    ("Every morning {N} does the cryptic crossword in pen, purely as a matter of principle.", dict(age=(45, 110), world="E", color="U")),
    ("Six library books come home every fortnight, and {N} finishes, on average, about four of them.", dict(age=(8, 110), world="E", color="U")),
    ("Weekends are for selling old furniture online, which {N} cleans up and prices just above what it is worth.", dict(age=(20, 80), world="E", color="B")),
    ("Once a month {N} checks what the house is worth online, just to see.", dict(age=(30, 110), world="E", color="B")),
    ("{N} reads business books in bed and underlines the parts about negotiation twice.", dict(age=(18, 70), world="E", color="B")),
    ("Every Saturday {N} buys a lottery ticket and has already spent the jackpot several times over.", dict(age=(18, 110), world="E", color="B")),
    ("Even for errands {N} wears a pressed shirt, because one never knows who might be in the bank queue.", dict(age=(25, 110), world="E", color="B")),
    ("Over toast each morning {N} checks the pension investments and phones the bank whenever anything dips.", dict(age=(60, 110), world="E", color="B")),
    ("{N} sings in the shower every morning, loudly, and the neighbours have learned the whole setlist.", dict(age=(8, 110), world="E", color="R")),
    ("On Sunday afternoons {N} still plays old records and sings along to the parts that matter.", dict(age=(55, 110), world="E", color="R")),
    ("The same television advert makes {N} cry every time it comes on, and the channel stays put.", dict(age=(12, 110), world="E", color="R")),
    ("Saturday mornings belong to the allotment, where {N} weeds the same patch and chats over the fence.", dict(age=(30, 110), world="E", color="G")),
    ("Sunday lunch is always at two and always a roast, and {N} has stopped pretending it could be otherwise.", dict(age=(10, 110), world="E", color="G")),

    # ------------------------------------------------------------------
    # Modern Earth: seasons
    # ------------------------------------------------------------------
    ("In spring {N} keeps the kitchen window open while washing up, listening to blackbirds argue in the hedge.", dict(age=(12, 110), world="E", season="spring")),
    ("Every spring the hay fever arrives on schedule, and {N} keeps tissues in every coat pocket.", dict(age=(6, 110), world="E", season="spring")),
    ("On the first sunny Saturday of spring {N} cleans every window, and the house smells of vinegar all day.", dict(age=(25, 110), world="E", color="W", season="spring")),
    ("Each spring {N} sows tomato seeds in yoghurt pots on the windowsill and talks to them a little.", dict(age=(25, 110), world="E", color="G", season="spring")),
    ("On summer evenings {N} eats dinner with the back door open, and moths come in to visit the lamp.", dict(age=(4, 110), world="E", season="summer")),
    ("All summer {N} carries a bottle of water everywhere and complains about the heat with real dedication.", dict(age=(13, 110), world="E", season="summer")),
    ("The bedroom window stays wide open all summer, and {N} falls asleep to scooters and distant laughter.", dict(age=(13, 110), world="E", season="summer")),
    ("On summer Sundays {N} stands over a barbecue that takes an hour to light and five minutes to char everything.", dict(age=(20, 110), world="E", season="summer")),
    ("Autumn evenings draw in early, and {N} walks home under orange streetlights with a collar turned up.", dict(age=(10, 110), world="E", season="autumn")),
    ("When the heating comes back on each autumn, {N} goes round bleeding the radiators with a little brass key.", dict(age=(25, 110), world="E", color="U", season="autumn")),
    ("Autumn Saturdays mean raking leaves, though {N} knows full well the tree has plenty more to drop.", dict(age=(14, 110), world="E", color="G", season="autumn")),
    ("Every autumn Sunday {N} makes the same soup and freezes portions labelled in shaky marker pen.", dict(age=(25, 110), world="E", color="G", season="autumn")),
    ("On winter mornings {N} scrapes ice off the windscreen with a supermarket loyalty card.", dict(age=(18, 90), world="E", season="winter")),
    ("In winter the radiator by the sofa becomes {N}'s spot, and everyone else has learned to sit elsewhere.", dict(age=(3, 110), world="E", season="winter")),
    ("In the weeks before the winter holidays {N} wraps presents badly at the kitchen table, using far too much tape.", dict(age=(12, 110), world="E", season="winter")),

    # ------------------------------------------------------------------
    # Tribal (T): any age
    # ------------------------------------------------------------------
    ("Most evenings the whole {place} eats around the long fire, and the dogs wait patiently for whatever {N} drops.", dict(age=(0, 110), world="T")),
    ("Rain drums on the longhouse roof through the wet nights, and {N} falls asleep to its steady beat.", dict(age=(0, 110), world="T")),
    ("Smoke from the fish racks drifts through the {place} each morning and clings to {N}'s hair all day.", dict(age=(0, 110), world="T")),
    ("Most mornings {N} wakes to the sound of the river while cold mist lifts slowly off the water.", dict(age=(0, 110), world="T")),
    ("Someone in the longhouse always snores, someone always shushes them, and {N} sleeps through both.", dict(age=(0, 110), world="T")),
    ("When the light goes, the {place} goes quiet early, and {N} lies listening to owls and the settling fire.", dict(age=(0, 110), world="T")),
    ("Each morning the camp dogs follow {N} down to the river and back, hoping for scraps.", dict(age=(2, 110), world="T")),
    ("At dusk the elders tell the old stories by the fire, and {N} has heard most of them a hundred times.", dict(age=(4, 110), world="T")),

    # ------------------------------------------------------------------
    # Tribal: toddlers and children
    # ------------------------------------------------------------------
    ("{N} rides in a carrying sling while the root diggers work, watching birds move through the high branches.", dict(age=(0, 3), world="T")),
    ("{N} sleeps in a cradleboard propped against the longhouse post while the grown-ups work close by.", dict(age=(0, 2), world="T")),
    ("Older cousins take turns carrying {N} around the camp, and {N} is rarely set down before noon.", dict(age=(0, 3), world="T")),
    ("Through the hottest part of the day {N} naps on a pile of soft hides, wrapped in someone's cloak.", dict(age=(0, 5), world="T")),
    ("Pebbles from the river get stacked beside the drying racks every morning, and {N} gleefully knocks them over.", dict(age=(1, 6), world="T")),
    ("Every day {N} toddles after the older children to the shallows and gets carried back soaking wet.", dict(age=(2, 6), world="T")),
    ("{N} sits with the grandmothers while they weave baskets and is given a handful of reeds to tangle.", dict(age=(2, 6), world="T", color="G")),
    ("Winter days mean {N} wrapped in furs by the longhouse fire, watching sparks rise toward the smoke hole.", dict(age=(0, 6), world="T", season="winter")),
    ("Most days {N} gathers firewood with the other children, racing to see whose bundle is biggest.", dict(age=(6, 13), world="T")),
    ("In the shallows {N} spends long afternoons catching minnows by hand and letting most of them go.", dict(age=(5, 13), world="T")),
    ("Every evening {N} and the other children play a hiding game among the drying racks until called in.", dict(age=(5, 12), world="T")),
    ("Armed with a stick and a loud voice, {N} scares birds away from the drying berries every afternoon.", dict(age=(5, 12), world="T", color="W")),
    ("Each evening an elder teaches {N} a new knot, and {N} ties and unties the cord until it frays.", dict(age=(6, 13), world="T", color="U")),

    # ------------------------------------------------------------------
    # Tribal: young people
    # ------------------------------------------------------------------
    ("At dawn {N} goes out with the young hunters, mostly carrying the nets and keeping very quiet.", dict(age=(13, 18), world="T")),
    ("Evenings by the fire mean scraping hides for {N}, while the older ones talk over the last hunt.", dict(age=(12, 18), world="T")),
    ("Every evening {N} and the other young ones swim across the river and back, just to prove they can.", dict(age=(12, 20), world="T", color="R")),
    ("Whenever the river camps meet, {N} trades carved bone beads with the other young people, always angling for the better string.", dict(age=(12, 25), world="T", color="B")),

    # ------------------------------------------------------------------
    # Tribal: adults and elders
    # ------------------------------------------------------------------
    ("Every evening {N} mends fishing nets, the bone needle moving in and out in the firelight.", dict(age=(10, 110), world="T")),
    ("Long afternoons go into twisting bark fibre into cord, which {N} measures by arm lengths along the wall.", dict(age=(8, 110), world="T")),
    ("Each morning {N} checks the fish traps in the shallows and carries the catch back in a reed basket.", dict(age=(14, 70), world="T")),
    ("Most evenings {N} knaps a fresh flint edge, since the old one always dulls just before a hunt.", dict(age=(16, 80), world="T", color="U")),
    ("Every day {N} marks the river's height with a notch on the old post and compares it with last year's.", dict(age=(14, 110), world="T", color="U")),
    ("When the clan council meets at new moon, {N} sits near the back and speaks only when it matters.", dict(age=(25, 110), world="T", color="W")),
    ("Whenever the baskets are shared out, {N} quietly slips a little more of the catch to the old ones.", dict(age=(18, 110), world="T", color="W")),
    ("{N} saves the best furs and trades them only for the finest flint whenever the river people visit.", dict(age=(18, 90), world="T", color="B")),
    ("Whenever the clan gathers, {N} sits where the elders can see and nods at the right moments.", dict(age=(16, 60), world="T", color="B")),
    ("Most nights {N} drums by the fire after the meal, and the children dance until they are sent to bed.", dict(age=(14, 110), world="T", color="R")),
    ("Each morning {N} grinds acorn flour on the flat stone, its hollow worn smooth by many hands before.", dict(age=(8, 110), world="T", color="G")),
    ("Through the long afternoons {N} sits at the longhouse door sorting seeds and correcting the young ones' baskets.", dict(age=(60, 110), world="T")),
    ("The children bring {N} the first berries of every picking, and {N} pretends to judge them very carefully.", dict(age=(60, 110), world="T")),
    ("On the path to the river {N} leans on a walking stick now and rests at the same flat rock.", dict(age=(65, 110), world="T")),
    ("{N} sleeps closest to the fire now, in a spot the young ones keep warm until {N} lies down.", dict(age=(65, 110), world="T")),

    # ------------------------------------------------------------------
    # Tribal: people, faith, circumstances
    # ------------------------------------------------------------------
    ("Each morning {partner} braids {N}'s hair down by the river, slowly, the same way every day.", dict(age=(18, 110), world="T", need=("partner",), color="G")),
    ("{N} carries {child} on one hip while checking the fish traps, and {child} names every fish.", dict(age=(18, 45), world="T", need=("children",))),
    ("{child} brings {N} the softest meat at every meal now, without needing to be asked.", dict(age=(55, 110), world="T", need=("children",))),
    ("Each moon {N} restitches {parent}'s hide shoes, and {parent} says the stitches were finer in the old days.", dict(age=(16, 70), world="T", need=("parent_alive",))),
    ("On full-moon nights {N} drums with {circle}, and the beat carries far across the river.", dict(age=(14, 110), world="T", need=("community",), color="R")),
    ("{N} leaves a small share of each meal at the spirit stone, as the old ones always have.", dict(age=(6, 110), world="T", need=("faith",), color="G")),
    ("Every morning {N} drinks bitter willow-bark tea with a grimace, and the aching eases a little.", dict(age=(30, 110), world="T", need=("in_poor_health",))),
    ("{N}'s share of the catch is always the small fish, and {N} knows twelve ways to cook them.", dict(age=(8, 110), world="T", need=("poor",))),
    ("Most evenings {N} sits at the edge of the fire, close enough to hear the stories but not to be in them.", dict(age=(10, 110), world="T", need=("lonely",))),

    # ------------------------------------------------------------------
    # Tribal: seasons
    # ------------------------------------------------------------------
    ("In spring {N} gathers fiddleheads and fresh shoots along the river banks, filling a bark basket each morning.", dict(age=(6, 110), world="T", season="spring")),
    ("When the ice breaks each spring, {N} helps drag the canoes down to the water and scrub the winter off them.", dict(age=(12, 80), world="T", season="spring")),
    ("Summer days mean berry picking on the hillside, and {N} eats about one berry for every two in the basket.", dict(age=(4, 110), world="T", season="summer")),
    ("On summer nights {N} sleeps outside the longhouse under the stars with the other young ones.", dict(age=(8, 25), world="T", season="summer")),
    ("In autumn {N} spends whole days gathering acorns and hazelnuts, and the stained fingers last for weeks.", dict(age=(4, 110), world="T", season="autumn")),
    ("Each autumn {N} packs smoked salmon into bark boxes for the winter, layer upon careful layer.", dict(age=(10, 110), world="T", color="G", season="autumn")),
    ("Through the winter {N} sits close to the fire stitching furs, and the days are short and the stories long.", dict(age=(10, 110), world="T", season="winter")),

    # ------------------------------------------------------------------
    # Magic (M): any age
    # ------------------------------------------------------------------
    ("The tower bells ring the hours across the {place}, and {N} has long since stopped counting them.", dict(age=(0, 110), world="M")),
    ("Each evening the lamplighters wake the glowstones with a word, and {N}'s window turns gold.", dict(age=(0, 110), world="M")),
    ("At dawn the kitchen kettle in {N}'s home whistles itself warm, a small charm nobody remembers setting.", dict(age=(0, 110), world="M")),
    ("On market days the square below fills with spice smoke and cheap firework charms, and {N} wakes early to the noise.", dict(age=(0, 110), world="M")),
    ("The house cat sleeps on the warm wardstone by {N}'s door, and nobody has the heart to move it.", dict(age=(0, 110), world="M")),
    ("Most nights rain slides off the weather ward above the {place}, and {N} falls asleep to its soft hiss.", dict(age=(0, 110), world="M")),
    ("Messenger crows bring the post at noon, and one of them always stops on {N}'s sill to complain.", dict(age=(0, 110), world="M")),
    ("Supper at {N}'s table is lit by a single glowstone that flickers whenever someone laughs too hard.", dict(age=(0, 110), world="M")),

    # ------------------------------------------------------------------
    # Magic: toddlers and children
    # ------------------------------------------------------------------
    ("{N} naps in a cradle that rocks itself, humming a lullaby charm that has worn a little thin.", dict(age=(0, 2), world="M")),
    ("Paper stars charmed to drift turn slowly above {N}'s cot, and {N} watches them for ages.", dict(age=(0, 2), world="M")),
    ("Wrapped in a blanket stitched with warming runes, {N} sleeps through the clatter of the market below.", dict(age=(0, 3), world="M")),
    ("On washing days {N} chases the soap bubbles drifting off the laundry charms and never quite catches one.", dict(age=(1, 6), world="M")),
    ("Each morning {N} watches the levitation lift haul crates up the tower and points at every single one.", dict(age=(1, 6), world="M")),
    ("Breakfast is honey bread, and {N} feeds the crusts to the messenger crow, which is strictly not allowed.", dict(age=(2, 6), world="M")),
    ("Chalk circles cover the kitchen floor every morning, drawn by {N}, and so far they do nothing at all.", dict(age=(2, 6), world="M", color="U")),
    ("{parent} hums the old counting spell at bedtime, and the ceiling stars glow once for every number.", dict(age=(0, 6), world="M", need=("parent_alive",))),
    ("Every morning {N} walks to the academy's little school, practising spell letters on a slate along the way.", dict(age=(5, 12), world="M")),
    ("Chalk dust from the morning lessons covers {N}'s sleeves by noon, however carefully {N} sits.", dict(age=(6, 13), world="M")),
    ("Under the blankets {N} practises the light charm every night, and the glow gets a little steadier each week.", dict(age=(7, 14), world="M")),
    ("After school {N} plays tag in the guild square, where the fountain charm splashes anyone who stands still.", dict(age=(6, 13), world="M")),
    ("Each evening {N} sweeps the tower stairs, a chore that somehow has more steps every time.", dict(age=(6, 13), world="M", color="W")),
    ("On market days {N} runs errands to the herb stalls for coppers and spends them on sugared roots.", dict(age=(7, 13), world="M", color="B")),
    ("{N} and {friend} spend afternoons on the archive steps, trading spell cards and arguing about the rare ones.", dict(age=(7, 14), world="M", need=("friend",))),

    # ------------------------------------------------------------------
    # Magic: young people
    # ------------------------------------------------------------------
    ("Most days {N} sleeps through the dawn bell and runs up the academy stairs with toast in hand.", dict(age=(13, 20), world="M")),
    ("Every evening {N} copies rune tables by lamplight at the kitchen table, sighing at the long ones.", dict(age=(12, 18), world="M")),
    ("Lecture notes get copied by enchanted quill, and {N} still somehow loses the important page every week.", dict(age=(13, 22), world="M", need=("student",))),
    ("Evenings on the tower roof mean {N} and the other apprentices setting off small sparks over the {place}.", dict(age=(13, 20), world="M", color="R")),
    ("{N} trades homework spells to younger students for sweets and favours, keeping a careful ledger of debts.", dict(age=(12, 18), world="M", color="B")),

    # ------------------------------------------------------------------
    # Magic: adults and elders
    # ------------------------------------------------------------------
    ("On the way home {N} buys bread from the same baker, who keeps it warm with a small charm.", dict(age=(8, 110), world="M")),
    ("Every few evenings {N} recharges the house glowstones, muttering the words while doing something else entirely.", dict(age=(12, 110), world="M")),
    ("After a day's work as {job}, {N} scrubs the ink and spell-chalk from both hands at the yard pump.", dict(age=(18, 70), world="M", need=("career",))),
    ("{N} logs every spell sold in the guild's ledger at day's end, in ink that dries itself.", dict(age=(18, 70), world="M", need=("career",), color="W")),
    ("On rest-day mornings {N} re-chalks the wards on the doorstep, which the rain always washes away by midweek.", dict(age=(20, 110), world="M", color="W")),
    ("Most evenings {N} reads in the archive's quiet room, borrowing three scrolls and returning two.", dict(age=(14, 110), world="M", color="U")),
    ("{N} tinkers with a broken scrying mirror on the kitchen table, sure it only needs the right word.", dict(age=(16, 110), world="M", color="U")),
    ("{N} haggles at the rune market every week and, on principle, never pays the first price asked.", dict(age=(18, 110), world="M", color="B")),
    ("On festival nights {N} sings with the street musicians, and the lanterns overhead pulse to the beat.", dict(age=(14, 90), world="M", color="R")),
    ("Rest days are for flying a kite charmed to stay aloft long after the wind has dropped, and {N} rarely misses one.", dict(age=(6, 110), world="M", color="R")),
    ("Each evening {N} tends the herb boxes on the tower balcony, pinching back whatever the pigeons missed.", dict(age=(18, 110), world="M", color="G")),
    ("{N} reads by a glowstone that needs recharging more often than it used to, much like {N}.", dict(age=(60, 110), world="M")),
    ("Every morning {N} rubs warming salve into stiff knees, bought from the same healer for twenty years.", dict(age=(55, 110), world="M")),
    ("A blanket of warming runes across both knees, {N} naps through the noon bell most days.", dict(age=(65, 110), world="M")),

    # ------------------------------------------------------------------
    # Magic: people, faith, circumstances
    # ------------------------------------------------------------------
    ("{N} and {partner} take turns setting the morning fire charm and argue cheerfully about whose turn it is.", dict(age=(18, 110), world="M", need=("partner",))),
    ("{N} walks {child} to the academy gate each morning, checking the slate for forgotten homework.", dict(age=(25, 50), world="M", need=("children",))),
    ("Every rest day {N} visits {parent} in the lower town and fixes whichever charm has stopped working.", dict(age=(20, 80), world="M", need=("parent_alive",), color="W")),
    ("Each week {N} attends {circle}, and the meeting always overruns because someone reads the minutes aloud.", dict(age=(16, 110), world="M", need=("community",), color="W")),
    ("{N} lights a candle at the star shrine each evening, a small habit older than the tower itself.", dict(age=(6, 110), world="M", need=("faith",), color="G")),
    ("The academy's long library keeps {N} until the lamps dim themselves at midnight, most nights of term.", dict(age=(16, 30), world="M", need=("student",), color="U")),
    ("Each evening {N} counts copper coins on the table and decides which charm can wait another week.", dict(age=(16, 110), world="M", need=("poor",))),
    ("Every fortnight {N} visits the healer's hall for a fresh tonic and waits on the same hard bench.", dict(age=(30, 110), world="M", need=("in_poor_health",))),
    ("Most nights {N} rereads the guild contracts by candlelight, certain some clause has been missed.", dict(age=(20, 70), world="M", need=("career", "stressed"))),

    # ------------------------------------------------------------------
    # Magic: seasons
    # ------------------------------------------------------------------
    ("In spring the tower gardens wake, and {N} takes the long way through them to see the new shoots.", dict(age=(6, 110), world="M", color="G", season="spring")),
    ("Each spring {N} helps scrub the winter soot from the tower's warding runes, bucket by bucket.", dict(age=(12, 90), world="M", color="W", season="spring")),
    ("On summer evenings {N} sits on the tower steps eating cold plums while the cooling charms hum.", dict(age=(6, 110), world="M", season="summer")),
    ("Summer means no academy, and {N} spends long days at the river with a fishing charm that never works.", dict(age=(8, 18), world="M", season="summer")),
    ("Every autumn {N} brews the family tonic from a recipe in an old book with a cracked spine.", dict(age=(18, 110), world="M", color="G", season="autumn")),
    ("In autumn {N} sweeps leaves from the steps every morning, and the wind charm always brings more back.", dict(age=(16, 110), world="M", season="autumn")),
    ("Every winter {N} renews the frost wards on the windows and still wakes to ice on the inside.", dict(age=(16, 110), world="M", season="winter")),
    ("On winter nights {N} toasts bread over the hearth charm, and the whole room smells of it.", dict(age=(3, 110), world="M", season="winter")),
]

# Every slot name the lines may use.
SLOTS = {"N", "place", "partner", "child", "friend", "parent", "job", "circle"}

# Slots that may only appear when the matching need is part of the line's conditions.
SLOT_NEEDS = {
    "partner": "partner",
    "child": "children",
    "friend": "friend",
    "parent": "parent_alive",
    "job": "career",
    "circle": "community",
}

NEEDS = (
    "career", "student", "retired", "partner", "children", "no_partner", "faith",
    "community", "friend", "parent_alive", "poor", "wealthy", "stressed", "happy",
    "unhappy", "lonely", "calm", "restless", "in_poor_health",
)
# Needs that can never hold together.
CONFLICTS = (("partner", "no_partner"), ("poor", "wealthy"), ("happy", "unhappy"))

WORLDS = "ETM"
COLORS = "WUBRG"
SEASONS = ("spring", "summer", "autumn", "winter")
WHEN_KEYS = {"age", "world", "need", "color", "season"}
AGE_BANDS = (
    ("toddler", 0, 6), ("child", 6, 13), ("teen", 13, 18), ("young adult", 18, 30),
    ("adult", 30, 50), ("older adult", 50, 65), ("elder", 65, 110),
)

# Style guards.
MIN_WORDS, MAX_WORDS = 8, 22
CHARACTER_PRONOUNS = re.compile(r"\b(he|she|him|her|his|hers|himself|herself)\b", re.IGNORECASE)

# Coverage targets.
MIN_POOL = 10  # need-free lines for every world and age, worst case over leading color and season
MIN_EARTH_PER_NEED = 4
MIN_PER_COLOR = {"E": 12, "T": 3, "M": 3}
MIN_PER_SEASON = {"E": 6, "T": 2, "M": 2}


def slots_in(text):
    """Return the slot names used in text."""
    return {field for _, field, _, _ in string.Formatter().parse(text) if field is not None}


def worlds_of(when):
    return when.get("world", WORLDS)


def pool_size(entries, age, color, season):
    """Need-free lines open to a character of this age, leading color and current season."""
    return sum(
        1 for when in entries
        if when["age"][0] <= age < when["age"][1]
        and when.get("color") in (None, color)
        and when.get("season") in (None, season)
    )


def check():
    seen = set()
    for i, entry in enumerate(ROUTINE):
        assert isinstance(entry, tuple) and len(entry) == 2, f"entry {i} is not a (text, when) pair"
        text, when = entry
        where = f"line {i}: {text!r}"
        assert isinstance(text, str) and text and text == text.strip(), f"{where}: bad text"
        assert isinstance(when, dict), f"{where}: when must be a dict"
        assert set(when) <= WHEN_KEYS, f"{where}: unknown keys {sorted(set(when) - WHEN_KEYS)}"

        # Slots.
        for _, field, spec, conv in string.Formatter().parse(text):
            if field is None:
                continue
            assert field in SLOTS, f"{where}: unknown slot {{{field}}}"
            assert not spec and conv is None, f"{where}: slot {{{field}}} has a format spec"
        needs = when.get("need", ())
        assert isinstance(needs, tuple), f"{where}: need must be a tuple"
        for slot in slots_in(text):
            if slot in SLOT_NEEDS:
                assert SLOT_NEEDS[slot] in needs, f"{where}: {{{slot}}} needs need={SLOT_NEEDS[slot]!r}"

        # Age.
        assert "age" in when, f"{where}: missing age"
        age = when["age"]
        assert isinstance(age, tuple) and len(age) == 2 and all(type(a) is int for a in age), f"{where}: bad age {age!r}"
        assert 0 <= age[0] < age[1] <= 110, f"{where}: bad age range {age!r}"

        # World.
        world = worlds_of(when)
        assert isinstance(world, str) and world, f"{where}: bad world {world!r}"
        assert set(world) <= set(WORLDS) and len(set(world)) == len(world), f"{where}: bad world {world!r}"

        # Needs.
        for need in needs:
            assert need in NEEDS, f"{where}: unknown need {need!r}"
        assert len(set(needs)) == len(needs), f"{where}: repeated need"
        for a, b in CONFLICTS:
            assert not (a in needs and b in needs), f"{where}: {a} conflicts with {b}"

        # Color and season.
        if "color" in when:
            assert when["color"] in tuple(COLORS), f"{where}: bad color {when['color']!r}"
        if "season" in when:
            assert when["season"] in SEASONS, f"{where}: bad season {when['season']!r}"

        # Punctuation and style.
        assert "—" not in text, f"{where}: em dash"
        assert "!" not in text, f"{where}: exclamation mark"
        assert not CHARACTER_PRONOUNS.search(text), f"{where}: gendered pronoun"
        assert text.endswith(".") and ". " not in text and "?" not in text, f"{where}: not one sentence"
        words = len(text.split())
        assert MIN_WORDS <= words <= MAX_WORDS, f"{where}: {words} words"

        # Repeats.
        key = " ".join(text.lower().split())
        assert key not in seen, f"{where}: repeated line"
        seen.add(key)

    # ---- counts and coverage ----
    by_world = {w: [when for _, when in ROUTINE if w in worlds_of(when)] for w in WORLDS}
    total = len(ROUTINE)
    print(f"Routine lines: {total}")
    print("  " + "   ".join(f"{w}: {len(by_world[w])}" for w in WORLDS))
    young = sum(1 for when in by_world["E"] if when["age"][0] < 18 and when["age"][1] <= 20)
    print(f"  E lines written for ages 0-18: {young}")

    def table(title, keys, count):
        print(f"\n{title}")
        print(f"  {'':16}" + "".join(f"{w:>6}" for w in WORLDS))
        for key in keys:
            label = key if isinstance(key, str) else key[0]
            print(f"  {label:16}" + "".join(f"{count(w, key):>6}" for w in WORLDS))

    def band_count(w, band):
        _, lo, hi = band
        return sum(1 for when in by_world[w] if when["age"][0] < hi and when["age"][1] > lo)

    def min_pool(w, band):
        _, lo, hi = band
        free = [when for when in by_world[w] if not when.get("need")]
        return min(pool_size(free, a, c, s) for a in range(lo, hi) for c in COLORS for s in SEASONS)

    table("Per age band (lines whose range overlaps the band)", AGE_BANDS, band_count)
    table("Smallest need-free pool in band (worst age, color, season)", AGE_BANDS, min_pool)
    table("Per need", NEEDS, lambda w, n: sum(1 for when in by_world[w] if n in when.get("need", ())))
    table("Per color", tuple(COLORS), lambda w, c: sum(1 for when in by_world[w] if when.get("color") == c))
    table("Per season", SEASONS, lambda w, s: sum(1 for when in by_world[w] if when.get("season") == s))
    table("No need, no color, no season", ("unconditional",),
          lambda w, _: sum(1 for when in by_world[w] if not set(when) & {"need", "color", "season"}))

    openers = Counter(text.split()[0].strip(",") for text, _ in ROUTINE)
    print("\nMost common opening words: " + ", ".join(
        f"{word} {n} ({n * 100 // total}%)" for word, n in openers.most_common(6)))

    # Coverage targets.
    for w in WORLDS:
        for band in AGE_BANDS:
            assert band_count(w, band) > 0, f"no {w} lines for {band[0]}"
            assert min_pool(w, band) >= MIN_POOL, f"{w} {band[0]}: need-free pool below {MIN_POOL}"
        for c in COLORS:
            n = sum(1 for when in by_world[w] if when.get("color") == c)
            assert n >= MIN_PER_COLOR[w], f"{w} color {c}: only {n} lines"
        for s in SEASONS:
            n = sum(1 for when in by_world[w] if when.get("season") == s)
            assert n >= MIN_PER_SEASON[w], f"{w} season {s}: only {n} lines"
    for need in NEEDS:
        n = sum(1 for when in by_world["E"] if need in when.get("need", ()))
        assert n >= MIN_EARTH_PER_NEED, f"E need {need}: only {n} lines"
    print("\nAll checks passed.")


if __name__ == "__main__":
    check()
