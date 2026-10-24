# Values and motives as human action: a source file for Chroma

Research file, 2026-10-04. Built from Schwartz's theory of basic values (ten values and the refined nineteen), studies of
values and behaviour, studies of value change over the life course, and motive research (Reiss's 16 basic desires,
Self-Determination Theory, Kasser and Ryan's aspirations, Cowen and Keltner's emotion categories, Chulef, Read and
Walsh's goal taxonomy, Emmons's personal strivings). Every section cites its sources. Text is paraphrase; short quotes
are marked. Acts are plain second-person acts a real person could do.

(Complete, 2026-10-05: sections 1 to 6.)

## How to read this file

Action line format:
`act` | value (sub-value) | life domain | stages | colors | map note

- Stages: child, juv (juvenile), ya (young adult), adult, mature, elder; "all" = every stage.
- Domains: play, school, friends, love, family, work, money, body (body and health), home, community, faith, conflict,
  leisure, aging, loss.
- `[inner]` marks an inner act (deciding, resenting, forgiving, daydreaming, ruminating). `[wrong]` marks an act most
  people would call a wrong (cheating, theft, betrayal, cruelty). Labels never preach and never say how it ends.
- Colors: my reading of the act under Magic's color pie (W U B R G), most fitting first; "U/B" means either reads
  well, "U+B" means both at once.
- Map note: the engine's value loadings give each value a leading color (see table below). `=map` means my reading
  agrees with the map's leading color(s) for that value. `!map` flags a disagreement, with the reason in a few words.
  Flags are notes for the engine thread; they are readings, not findings.

### The engine's map, as leading colors (for checking the flags)

Computed from the loadings given in the brief (largest positive first):

| value | W | U | B | R | G | leading colors |
|---|---|---|---|---|---|---|
| self-direction | -3 | .5 | 3.5 | 1.5 | -2.5 | B, then R |
| stimulation | -2.5 | -2 | 1.5 | 2.5 | .5 | R, then B |
| hedonism | -2.5 | -1.5 | 1.5 | 2.5 | 0 | R, then B |
| achievement | -1 | 2 | 2.5 | -.5 | -3 | B, then U |
| power | -1.5 | .5 | 1.5 | 1 | -1.5 | B, then R |
| security | 1.5 | 1.5 | -1 | -1.5 | -.5 | W and U |
| conformity | 3 | 2 | -2 | -3 | 0 | W, then U |
| tradition | 2.5 | -1.5 | -3.5 | -.5 | 3 | G, then W |
| benevolence | 1 | 0 | -1 | -1 | 1 | W and G |
| universalism | .5 | -1 | -1 | 0 | 1.5 | G, then W |

Recurring flags, so each line can stay short:
- **F1 curiosity**: acts of learning, study, puzzling out and wanting to understand read Blue. Under the map they score
  as self-direction, whose loading is mostly Black (U only .5). Self-direction-thought in the refined theory is the
  natural home for a Blue value (see section 1.2).
- **F2 head vs heart**: acts that are about deliberating, planning or holding back an impulse (Blue) versus acting on
  feeling, passion or impulse (Red). No Schwartz value covers this axis; stimulation and hedonism partly cover the Red
  side. Schwartz's culture-level split of intellectual autonomy versus affective autonomy is the nearest match (section 1.3).
- **F3 justice**: universalism-concern acts (equality, fairness, protecting the weak, law for all) read White more than
  Green; the map's universalism leads with Green.
- **F4 nature**: universalism-nature acts read Green; agrees with the map.
- **F5 institutional power**: power held through office, rank, law or an army reads White (or W+B); the map gives power
  a negative White loading.
- **F6 control by mind**: power through information, secrets, persuasion or manipulation reads Blue; the map gives
  power only U .5.
- **F7 simple pleasures**: sensory, unhurried pleasures (sun, food, rest, a garden) read Green; the map gives hedonism
  G 0 and leads with Red.
- **F8 discipline and mastery**: achievement through patient practice and perfecting a craft reads Blue more than
  Black; achievement through beating rivals reads Black; achievement through physical strength or natural gift reads
  Green or Red, which the map scores against (G -3).
- **F9 duty and loyalty**: benevolence-dependability (being someone people can rely on) reads White; benevolence-caring
  for kin and pack reads Green or White. Both agree with the map.
- **F10 self-direction as freedom of action**: self-direction-action (do it my way, nobody tells me) reads Red or Black;
  agrees with the map. Only self-direction-thought is the problem (F1).

## 1. The theory: ten values, nineteen values, and what they leave out

Sources:
- Schwartz, S. H. (2012). An overview of the Schwartz theory of basic values. Online Readings in Psychology and
  Culture, 2(1). https://doi.org/10.9707/2307-0919.1116 (PDF: https://scholarworks.gvsu.edu/cgi/viewcontent.cgi?article=1116&context=orpc)
- Schwartz, S. H., Cieciuch, J., Vecchione, M., Davidov, E., Fischer, R., Beierlein, C., ... Konty, M. (2012).
  Refining the theory of basic individual values. Journal of Personality and Social Psychology, 103(4), 663-688.
  (Full text read via https://avesis.tedu.edu.tr/yayin/5030e84d-d374-42d4-a46c-b6f7b2d08457/refining-the-theory-of-basic-individual-values)
- PVQ-40 item list and scoring key (Schwartz Portrait Values Questionnaire), read via
  https://carepatron.com/files/portrait-values-questionnaire.pdf. PVQ-RR item content as quoted in the 2012 paper and
  in https://arxiv.org/pdf/2509.24906 (the PVQ-RR item list itself sits behind sites I could not reach; see report).
- Schwartz, S. H. (2006). A theory of cultural value orientations: explication and applications. Comparative
  Sociology, 5(2-3), 137-182. Orientation summaries read via https://rdrr.io/github/emlaet/wwmetrics/man/Schwartz.html

### 1.1 The ten values (Schwartz 2012), paraphrased

| value | motivational goal (paraphrase) | marker values from the survey | grounded in |
|---|---|---|---|
| self-direction | think and act on your own: choose, create, explore | creativity, freedom, own goals, curious, independent | need for control and mastery; social demand for autonomy |
| stimulation | excitement, novelty and challenge | varied life, exciting life, daring | need for variety and optimal arousal |
| hedonism | pleasure and sensuous gratification for yourself | pleasure, enjoying life, self-indulgent | organismic needs and the pleasure of meeting them |
| achievement | personal success by showing competence against social standards | ambitious, successful, capable, influential | groups need competent performance |
| power | status and prestige, control or dominance over people and resources | authority, wealth, social power (also face, image) | institutions need some status differences |
| security | safety, harmony and stability of society, relationships and self | social order, family security, national security, clean, favours returned | basic individual and group needs |
| conformity | restrain acts and impulses that would upset or harm others or break norms | obedient, self-discipline, polite, honouring parents and elders | groups need members to hold back disruptive urges |
| tradition | respect and commitment to the customs and ideas of your culture or religion | respect for tradition, humble, devout, accepting your portion in life | shared practice and symbols turned into custom |
| benevolence | keep and raise the welfare of the people you deal with closely | helpful, honest, forgiving, responsible, loyal, true friendship, mature love | smooth group life; need for affiliation |
| universalism | understanding, tolerance and protection for all people and for nature | broadminded, social justice, equality, world at peace, world of beauty, unity with nature, wisdom | meeting outsiders; seeing that resources and nature are finite |

The circle: neighbours share motives and are compatible; opposites conflict. Two axes:
- **Openness to change** (self-direction, stimulation, part of hedonism) versus **conservation** (security, conformity,
  tradition).
- **Self-enhancement** (power, achievement, part of hedonism) versus **self-transcendence** (benevolence, universalism).
- A second reading: the top half (power, achievement, hedonism, stimulation, self-direction) has a **personal focus**,
  the bottom half a **social focus**; the left half (power, security, conformity, tradition) serves **self-protection
  against anxiety**, the right half (hedonism, stimulation, self-direction, universalism, benevolence) expresses
  **anxiety-free growth**. Achievement does both.
- Typical clashes the paper names: achievement against benevolence, stimulation against tradition, power against
  universalism.

Average ranking across nations (pan-cultural hierarchy, Schwartz 2012): benevolence (1), universalism (2),
self-direction (3), security (4), conformity (5), hedonism (6), achievement (7), tradition (8), stimulation (9),
power (10). The paper explains it by what groups need: warm cooperative ties first, then motivated productive and
inventive members, then some licence for self-oriented pleasure, while open power-seeking is discouraged. Where
families are very large (seven or more children), self-direction ranks far lower and conformity far higher.

Two cautions from the paper that matter for a simulator:
- Values steer action mostly when they are both important to the person and **activated** by the situation. They
  usually work outside awareness and come into awareness when an act would serve one cherished value and hurt another.
  This is exactly where a dilemma moment belongs.
- A value is not a trait. People can prize creativity and not be creative, or act obediently without prizing
  obedience. The engine can keep "what you value" and "what you habitually do" as separate quantities.

### 1.2 The refined nineteen values (Schwartz et al. 2012)

| refined value | definition (paraphrase of the paper's table) | higher-order group | notes for Chroma |
|---|---|---|---|
| self-direction-thought | freedom to cultivate your own ideas and abilities | openness | the curiosity and learning value; correlates more with education (r about .22) than self-direction-action (.12). **Best candidate home for Blue's curiosity (F1).** |
| self-direction-action | freedom to decide your own actions | openness | "make my own decisions", "rely on myself": reads Black and Red |
| stimulation | excitement, novelty and change | openness | |
| hedonism | pleasure and sensuous gratification | openness / self-enhancement border | |
| achievement | success according to social standards | self-enhancement | |
| power-dominance | power by controlling people | self-enhancement | the "tell others what to do" side; carries more of men's higher power scores |
| power-resources | power by controlling material and social resources | self-enhancement | the "wealth and what money can do" side; strongest predictor of "you can't get ahead without money" |
| face | security and power through keeping your public image and avoiding humiliation | self-enhancement / conservation border | new value; between power and security. Reputation, honour, not being shamed |
| security-personal | safety in your immediate surroundings | conservation | health, home, money for self; weak age link (r about .09) |
| security-societal | safety and stability in the wider society | conservation | strong state, order, country safe; age link r about .25; predicts seeing immigration as a threat |
| tradition | keep cultural, family or religious traditions | conservation | age link r about .26 |
| conformity-rules | comply with rules, laws and formal obligations | conservation | age link r about .26 |
| conformity-interpersonal | avoid upsetting or harming other people | conservation | sits nearer universalism; the gentle, tactful side; age link only r about .12 |
| humility | recognise your smallness in the larger scheme of things | conservation / self-transcendence border | modesty, accepting your lot; almost no age link (r about .02) |
| benevolence-dependability | be a reliable and trustworthy member of your group | self-transcendence | "others can count on me"; self-assured; higher in early adulthood with dependent children, then declines |
| benevolence-caring | devotion to the welfare of your group | self-transcendence | "help near ones, forgive, no grudges"; no age link |
| universalism-concern | equality, justice and protection for all people | self-transcendence | rises with age (r about .17). Reads White (F3) |
| universalism-nature | preservation of the natural environment | self-transcendence | rises with age (r about .26). Reads Green (F4) |
| universalism-tolerance | accept and understand people who are different | self-transcendence | rises least with age (r about .13); older people value tolerance of different ideas less |

Circle order (the paper's figure, going round): self-direction-thought, self-direction-action, stimulation,
hedonism, achievement, power-dominance, power-resources, face, security-personal, security-societal, tradition,
conformity-rules, conformity-interpersonal, humility, benevolence-dependability, benevolence-caring,
universalism-concern, universalism-nature, universalism-tolerance, and back to self-direction-thought.

PVQ item content that shows how the values look in a person's own words (paraphrased from the PVQ-40 and the PVQ-RR
items quoted in the sources): think up new ideas and be creative; form your views independently; be curious and try
to understand all sorts of things (scored as self-direction, a Blue act scored under Black: F1); make your own
decisions; rely on yourself; try new and different things; take risks and seek adventure; have a good time; enjoy
life's pleasures; be ambitious and capable; show your abilities and be admired; get ahead of others; be rich and have
expensive things; be the one in charge who tells others what to do; protect your public image; never be humiliated;
live in safe surroundings; avoid illness; keep your country secure and its government stable; keep things clean and
in order; follow rules even when nobody watches; never annoy anyone; respect parents and elders; keep customs and
religious duties; be humble and modest; be content with what you have; be a loyal, dependable friend; care for and
forgive those close to you; respond to the needs of people you know; protect the weak; treat everyone equally; listen
to people who are different; live in harmony with nature; defend nature.

### 1.3 What the theory leaves out, and where research can fill the gaps

**Gap A: Blue's curiosity and learning (F1).** The ten-value model folds curiosity into self-direction, so a curious
act scores mostly Black under the map. The refined model already splits self-direction-thought (ideas, abilities,
curiosity) from self-direction-action (choosing your own acts). Suggested reading: self-direction-thought loads Blue
strongly; self-direction-action keeps the current Black/Red loading. Further support:
- Schwartz's culture-level orientations (2006) split **intellectual autonomy** (pursue your own ideas: curiosity,
  broadmindedness, creativity) from **affective autonomy** (pursue pleasant, exciting, varied feeling for yourself).
  At the level of whole societies these are separate dimensions, which is the strongest published support for treating
  "free mind" and "free feeling" as two things.
- Reiss's basic desires include **curiosity** as one of sixteen separate desires (section 6.1), and Self-Determination
  Theory treats curiosity-driven, intrinsically motivated activity as the model case of autonomy and competence
  (section 6.2).
- Skimina et al. (2019) found self-direction-thought shows one of the clearest behavioural signatures of all values:
  reading books, studying subjects, going to lectures, museums and exhibitions, learning new skills (section 2).

**Gap B: head versus heart (Blue against Red, F2).** No Schwartz value is about whether you reason or feel your way
to a choice; values are goals, while head-versus-heart is a style of choosing. Places that touch it:
- Intellectual versus affective autonomy (above): the same "freedom" split into mind and feeling.
- Conformity's original definition is "restraint of actions, inclinations and impulses": impulse control is filed as
  conformity, which pulls Blue's self-control toward White.
- Stimulation and hedonism capture the Red pole's goals (feeling, thrill, pleasure) but not Red's trust in feeling as
  a guide to truth.
- A style variable from outside values research would fit better (for example Epstein's rational versus experiential
  thinking, or need for cognition). That is a suggestion, not something read for this file.

**Gap C: values that the refined split makes visible but the map lumps together.**
- Security-personal (my health, my savings, my door locked) versus security-societal (law, police, a stable state):
  the first reads Blue/Green/White, the second White.
- Conformity-rules (obey laws and rules) reads White; conformity-interpersonal (do not upset people, be tactful) reads
  White or Green, and sits closer to benevolence.
- Benevolence-dependability (be someone people can rely on) reads White; benevolence-caring (look after your own)
  reads Green and White.
- Universalism-concern reads White (justice, equality: F3); universalism-nature reads Green (F4); universalism-tolerance
  reads White/Green/Blue (open-minded acceptance), and also Red when it is about letting people be themselves.
- Power-dominance reads Black and Red (and White when it is office or rank, F5); power-resources reads Black (and Blue
  when it is control through knowledge, F6).
- Face (reputation, honour, never being shamed) reads White when it is honour and standing, Black when it is image
  management for advantage. Under the map it has no entry; as a blend of power and security it would score
  W 0, U 2, B .5, R -.5, G -2 (power plus security), that is Blue-leading, which feels wrong for honour. Suggest W/B.
- Humility (accept your lot, you are small in a big world) reads Green and White.

## 2. Values and behaviour: what the studies say

Sources:
- Bardi, A., & Schwartz, S. H. (2003). Values and behavior: strength and structure of relations. Personality and
  Social Psychology Bulletin, 29(10), 1207-1220. https://doi.org/10.1177/0146167203254602 (abstract read via
  https://kar.kent.ac.uk/4133; full item list not reachable, see report)
- Skimina, E., Cieciuch, J., Schwartz, S. H., Davidov, E., & Algesheimer, R. (2019). Behavioral signatures of values
  in everyday behavior in retrospective and real-time self-reports. Frontiers in Psychology, 10, 281.
  https://www.frontiersin.org/articles/10.3389/fpsyg.2019.00281/full
- Schwartz, S. H., Cieciuch, J., Vecchione, M., Torres, C., Dirilen-Gumus, O., & Butenko, T. (2017). Value tradeoffs
  propel and inhibit behavior: validating the 19 refined values in four countries. European Journal of Social
  Psychology, 47(3), 241-258. https://cris.huji.ac.il/en/publications/value-tradeoffs-propel-and-inhibit-behavior-validating-the-19-ref/
- Pavlović, Z., & Stepanović Ilić, I. (2022). Basic values as predictors of leisure-time activities among
  adolescents. Primenjena psihologija, 15(1), 85-117. https://primenjena.psihologija.ff.uns.ac.rs/index.php/pp/article/download/2349/2221
- Coelho, G. L. de H., Hanel, P. H. P., Johansen, M. K., & Maio, G. R. (2022). Mental representations of values and
  behaviors. European Journal of Personality, 36(6), 926-941. https://orca.cardiff.ac.uk/id/eprint/142426/

Findings that matter for the engine:
- **Some values show in behaviour far more than others** (Bardi and Schwartz 2003). Stimulation and tradition link
  strongly to the acts that express them; hedonism, power, universalism and self-direction moderately; security,
  conformity, achievement and benevolence only weakly. Their reading: where a social norm pushes everyone toward an act
  (be kind, be polite, work hard, be careful), the act stops telling you much about the person's values. For Chroma:
  a thrill-seeking act or a religious rite is strong evidence of a person's values; a polite or helpful act is weak
  evidence, since nearly everyone does it.
- **Behaviour is a trade-off.** Values on one side of the circle push an act, the values opposite hold it back
  (Schwartz et al. 2017, in four countries; Skimina et al. 2019). Praying is pushed by tradition and held back by
  hedonism; drinking and partying are pushed by stimulation, hedonism and power-resources and held back by conformity
  and both benevolence values. The same act can therefore be framed in a dilemma by naming the value that pushes and the
  value that brakes.
- **Behavioural signatures** (Skimina et al. 2019, everyday activity lists, retrospective and real-time):
  self-direction-thought: reading books, studying a subject, going to lectures, museums and art shows, learning new
  skills (one of the clearest signatures; supports F1). Stimulation and hedonism: drinking to intoxication, partying,
  gambling, betting on sport. Tradition: praying, reading sacred texts, going to services, talking about religion.
  Universalism-nature: gardening, composting, changing habits for the environment, picking up litter.
  Universalism-concern: giving to charity, and (oddly) household chores like dishes and making beds.
  Power-resources: drinking, gambling, partying, and less religious and environmental activity. Power-dominance: less
  housework, a weak interest in the stock market. Conformity: less drinking and partying. Benevolence: less gambling.
  Single acts correlate weakly with values; bundles of acts correlate much better (about .25 to .45). For Chroma: a
  person's value profile should show in the pattern of many small acts, not in one act.
- **Adolescent leisure** (Pavlović and Stepanović Ilić 2022): hedonism and stimulation predict entertainment and going
  out; self-direction predicts music, culture and arts; conformity and tradition predict sport (organised, rule-bound
  activity). Effects are small one by one.
- **One act, many values** (Coelho et al. 2022): most behaviours sit near several values at once, and people disagree
  most about what self-enhancement acts mean (is working late ambition, security or duty?). This supports Chroma's
  idea that means and ends can differ in color.

Typical value-expressive acts in the style of Bardi and Schwartz's behaviour list (examples recalled from the published
item list, paraphrased; check against the paper before quoting): self-direction: examine the reasons behind a rule
before you obey it, invent your own way of arranging your room; stimulation: watch thrillers, go to places you have
never been, do unconventional things; hedonism: take it easy and relax, eat or drink when not hungry, buy things purely
for your pleasure; achievement: study late before exams even when well prepared, work longer than others to get
ahead; power: pick friends by their status, push others to go along with your opinions; security: avoid walking alone
at night in dangerous places, refuse to open the door to strangers, buy goods made in your own country; conformity:
obey your parents, avoid confronting people you dislike; tradition: keep the customs of the holidays, play down your
own talents; benevolence: lend things readily to neighbours, keep promises; universalism: use products that spare the
environment, make sure everyone you know gets equal treatment, read or watch programmes about other cultures.

## 3. Value-expressive acts, value by value

Sources: definitions and sub-values from Schwartz (2012) and Schwartz et al. (2012); behaviour patterns from Bardi and
Schwartz (2003), Skimina et al. (2019) and Schwartz et al. (2017), all cited in sections 1 and 2. The acts are my own
paraphrased examples built on those definitions, spread over domains and stages; they are not survey items.

Line format: `act` | value (sub-value) | domain | stages | colors | map note.

### 3.1 Self-direction (map: B, then R)

Definition: independent thought and action; choosing, creating, exploring. Motivational goal: be the author of your own
thoughts and acts. Refined split: **thought** (cultivate your own ideas and abilities) and **action** (decide your own
acts). Self-direction-thought is where Blue's curiosity lives (F1); self-direction-action reads Red and Black (F10).

Self-direction-thought
- take apart the old radio to see how it works | SD-thought | play | child | U | !map F1
- ask "why" until the grown-up runs out of answers | SD-thought | family | child | U | !map F1
- build the fort to your own design instead of the kit's | SD-thought | play | child | U/R | !map F1 (R part fits)
- invent a secret language with your best friend | SD-thought | friends | child, juv | U | !map F1
- read the encyclopedia under the covers with a torch | SD-thought | leisure | child, juv | U | !map F1
- pick the hard science elective nobody else takes | SD-thought | school | juv | U | !map F1
- challenge the teacher's answer in class, with evidence | SD-thought | school | juv, ya | U/R | !map F1
- [inner] decide privately that you no longer believe what your family believes | SD-thought | faith | juv, ya | U/B | B fits; U for the reasoning
- teach yourself to code from free videos at night | SD-thought | work | juv, ya, adult | U | !map F1
- keep a notebook of your own ideas and theories | SD-thought | leisure | all | U | !map F1
- write the novel nobody asked for | SD-thought | leisure | ya, adult, mature | U/R | !map F1 (R expression fits)
- switch your degree from law to philosophy | SD-thought | school | ya | U | !map F1
- take an evening course in astronomy at fifty | SD-thought | leisure | mature | U | !map F1
- learn a language at seventy to read a poet in the original | SD-thought | aging | elder | U | !map F1
- [inner] daydream a better way to run the workshop | SD-thought | work | adult | U | !map F1
- read the other side's best book before you argue | SD-thought | conflict | ya, adult | U/W | !map F1
- form your own view on the election from the source documents | SD-thought | community | adult | U | !map F1
- compose a song about the breakup | SD-thought | love | juv, ya | R/U | =map (R)
- paint in the style your art teacher dislikes | SD-thought | school | juv, ya | R/U | =map (R)
- [inner] doubt the doctor's diagnosis and research it yourself | SD-thought | body | adult, mature | U/B | partial: B fits, U leads
- study the scripture critically and reach your own reading | SD-thought | faith | adult | U | !map F1
- take up chess problems to keep your mind sharp | SD-thought | aging | elder | U | !map F1
- after a death, read philosophy to understand what dying is | SD-thought | loss | adult, mature, elder | U | !map F1
- invent a new dish instead of making grandmother's | SD-thought | home | adult | U/R | !map F1
- vote against your own party on your own reasoning | SD-thought | community | adult | U/B | partial F1
- homeschool the children by a method you designed | SD-thought | family | adult | U/B | partial F1

Self-direction-action
- insist on dressing yourself, mismatched socks and all | SD-action | family | child | R | =map
- walk to school by your own route | SD-action | school | child, juv | R | =map
- refuse to join the team your father picked for you | SD-action | family | juv | R/B | =map
- get a weekend job so you never have to ask for money | SD-action | money | juv | B/R | =map
- move out at eighteen into a tiny room of your own | SD-action | home | ya | R/B | =map
- choose a partner your family does not approve of | SD-action | love | ya, adult | R | =map
- turn down the match your family arranged | SD-action | love | ya | R/B | =map
- quit the steady job to freelance | SD-action | work | ya, adult | R/B | =map
- start your own small business | SD-action | work | adult | B/R | =map
- refuse to sign the loyalty pledge at work | SD-action | work | adult | R/B | =map
- keep your own surname after marriage | SD-action | love | ya, adult | B/R | =map
- decide to stay childfree despite the pressure | SD-action | family | ya, adult | B | =map
- leave the faith of your upbringing openly | SD-action | faith | ya, adult | B/R | =map
- travel alone across a continent | SD-action | leisure | ya | R | =map
- build your own house without a contractor | SD-action | home | adult | R/G | partial: G self-reliance scores against the map (G -2.5)
- live off-grid on a smallholding | SD-action | home | adult, mature | G/R | !map: self-sufficient Green autonomy, map G -2.5
- refuse to retire when the company expects you to | SD-action | work | mature, elder | R/B | =map
- refuse the care home and stay in your own flat | SD-action | aging | elder | R/B/G | =map (G home ties)
- manage your own medicines against your children's wishes | SD-action | body | elder | B | =map
- write your will and plan your funeral without asking anyone | SD-action | loss | elder | B/U | =map
- grieve your own way and skip the expected rites | SD-action | loss | adult | R/B | =map
- choose how you present yourself, whatever your family thinks | SD-action | body | juv, ya, adult | R/B | =map
- [inner] resent being told what to do, all day, at the new job | SD-action | work | ya, adult | R | =map
- [inner] decide you will never again let anyone run your life | SD-action | love | ya, adult | B/R | =map
- [wrong] forge your parent's signature on the permission slip | SD-action | school | juv | B/R | =map
- [wrong] lie about your age to get into the club | SD-action | leisure | juv | R/B | =map
- [wrong] climb out the window at night against the house rules | SD-action | family | juv | R | =map

### 3.2 Stimulation (map: R, then B)

Definition: excitement, novelty and challenge in life. Motivational goal: keep life varied and keep arousal up.
Grounded in the need for variety. Stimulation is one of the two values most visible in behaviour (Bardi and Schwartz
2003). Novelty sought for knowledge reads Blue (F1); novelty sought for feeling reads Red (agrees).

- climb the tallest tree in the park | stimulation | play | child | R | =map
- ride your bike down the steepest hill with no hands | stimulation | play | child, juv | R | =map
- dare a friend to ring the doorbell and run | stimulation | friends | child | R | =map
- beg to go on the biggest roller coaster | stimulation | play | child | R | =map
- explore the woods past where you are allowed to go | stimulation | play | child, juv | R/G | =map
- switch hobbies every few months | stimulation | leisure | juv, ya | R | =map
- try out for the school play on a whim | stimulation | school | juv | R | =map
- take the dare at the party | stimulation | friends | juv | R | =map
- explore the abandoned factory at night | stimulation | play | juv, ya | R/U | =map
- go to a concert in another city with no plan for the night | stimulation | friends | juv, ya | R | =map
- start a band | stimulation | leisure | juv, ya | R | =map
- hitchhike to the coast | stimulation | leisure | ya | R | =map
- take a gap year to backpack | stimulation | leisure | ya | R | =map
- learn fire-dancing at a festival | stimulation | leisure | ya | R | =map
- go to the reality-show audition | stimulation | leisure | ya | R/B | =map
- go on a blind date a stranger set up | stimulation | love | ya, adult | R | =map
- fall for someone because they are unpredictable | stimulation | love | juv, ya | R | =map
- move to a new city every two years | stimulation | home | ya, adult | R | =map
- take the job abroad in a country you know nothing about | stimulation | work | ya, adult | R/U | =map (U if curiosity, F1)
- learn to skydive | stimulation | body | ya, adult | R | =map
- take up night swimming in the lake | stimulation | body | ya, adult | R/G | =map
- ride a motorbike on mountain roads | stimulation | leisure | ya, adult, mature | R | =map
- go storm chasing | stimulation | leisure | ya, adult | R/G | =map
- explore caves with a club | stimulation | leisure | juv, ya, adult | R/G/U | =map
- eat the strangest dish on the menu | stimulation | leisure | all | R | =map
- volunteer for the risky field assignment | stimulation | work | adult | R | =map
- start a business in a trade you know nothing about | stimulation | work | adult | R | =map
- bet on the long shot | stimulation | money | ya, adult | R/B | =map
- rearrange the whole house on a Sunday | stimulation | home | adult | R | =map
- take a different route home every day | stimulation | home | adult | R | =map
- book a surprise trip for your partner | stimulation | love | adult | R | =map
- go to another faith's festival just to see it | stimulation | faith | adult | R/U | partial F1
- join the protest march because it makes you feel alive | stimulation | community | juv, ya | R | =map
- take up salsa dancing at sixty | stimulation | leisure | mature, elder | R | =map
- cross a desert by jeep after you retire | stimulation | aging | mature, elder | R | =map
- move abroad in retirement | stimulation | aging | mature, elder | R | =map
- book a solo cruise the year after your spouse dies | stimulation | loss | elder | R | =map
- [inner] daydream about dropping everything and sailing away | stimulation | home | adult, mature | R | =map
- [inner] feel the itch to quit after a year in any job | stimulation | work | ya, adult | R | =map
- [inner] crave a crisis because calm feels dead | stimulation | conflict | ya, adult | R | =map
- [wrong] shoplift for the thrill | stimulation | money | juv | R/B | =map
- [wrong] race cars on a public road at night | stimulation | leisure | juv, ya | R | =map
- [wrong] start a fight to break the boredom | stimulation | conflict | juv, ya | R | =map
- [wrong] have an affair for the excitement | stimulation | love | adult | R/B | =map

### 3.3 Hedonism (map: R, then B)

Definition: pleasure or sensuous gratification for yourself. Motivational goal: enjoy life and feel good now.
Grounded in organismic needs and the pleasure of meeting them. Sits between openness and self-enhancement. Loud,
impulsive pleasure reads Red; luxury and indulgence as reward reads Black; slow sensory pleasures read Green (F7).

- eat the icing off the cake first | hedonism | play | child | R | =map
- stay in the bath until your fingers wrinkle | hedonism | home | child | G/R | partial F7
- beg for one more cartoon before bed | hedonism | home | child | R | =map
- trade your packed lunch for a candy bar | hedonism | school | child | R/B | =map
- spend the whole allowance on sweets | hedonism | money | child, juv | R | =map
- lie in the grass watching clouds instead of doing homework | hedonism | leisure | child, juv | G | !map F7
- skip practice to go to the beach | hedonism | leisure | juv | R | =map
- throw a house party while your parents are away | hedonism | friends | juv | R | =map
- sleep until noon at the weekend | hedonism | home | juv, ya | R/G | =map
- spend your first paycheque on a designer jacket | hedonism | money | ya | B/R | =map
- eat street food on the walk home every night | hedonism | leisure | ya | R | =map
- date several people at once with no commitment | hedonism | love | ya | R/B | =map
- buy the games console with the rent money | hedonism | money | ya | R/B | =map
- choose the job with short hours over the job with high pay | hedonism | work | ya, adult | R/G | =map (G part)
- have a lazy Sunday in bed with your partner | hedonism | love | ya, adult | R/G | =map
- dance all night at the wedding | hedonism | community | juv, ya, adult | R | =map
- order the tasting menu on your birthday | hedonism | leisure | adult | R/B | =map
- book a spa weekend | hedonism | body | adult | G/R | partial F7
- buy the expensive wine for an ordinary Tuesday | hedonism | money | adult | B/R | =map
- take a long lunch in the sun | hedonism | work | adult | G/R | partial F7
- cook an elaborate meal just for yourself | hedonism | home | adult | R/G | =map
- choose the sweetest fruit at the market by its smell | hedonism | home | adult | G | !map F7
- lounge by the pool all holiday | hedonism | leisure | adult | R/G | =map
- buy a hot tub | hedonism | home | adult | R/B | =map
- treat yourself to a massage after the breakup | hedonism | love | ya, adult | R/G | =map
- stay up late reading for pleasure | hedonism | leisure | all | R/U | =map
- leave the service early for a long brunch | hedonism | faith | adult | R | =map
- leave the funeral meal early for a quiet drink alone | hedonism | loss | adult | R/B | =map
- spend the inheritance on a long trip | hedonism | loss | adult, mature | R/B | =map
- take up wine tasting | hedonism | leisure | adult, mature | R/B | =map
- buy the sports car in midlife | hedonism | money | mature | R/B | =map
- have a quiet beer on the porch watching the sunset | hedonism | home | adult, mature, elder | G/R | partial F7
- grow tomatoes for the joy of eating them warm from the vine | hedonism | home | adult, mature, elder | G | !map F7
- spend the savings on a cruise in retirement | hedonism | money | mature, elder | R/B | =map
- eat dessert first at seventy, because why not | hedonism | aging | elder | R | =map
- take a nap every afternoon | hedonism | body | elder | G | !map F7
- sneak sweets after the doctor says no | hedonism | body | elder | R | =map
- [inner] daydream about the holiday all through the meeting | hedonism | work | adult | R | =map
- [inner] decide life is too short for diets | hedonism | body | adult, mature | R | =map
- [inner] savour the memory of a perfect summer | hedonism | aging | elder | G/R | partial F7
- [wrong] call in sick to watch a whole series | hedonism | work | ya, adult | R/B | =map
- [wrong] drink until you black out | hedonism | body | ya | R/B | =map
- [wrong] take the pill a stranger offers at the festival | hedonism | body | ya | R/B | =map
- [wrong] steal a bottle from the shop | hedonism | money | juv | B/R | =map
- [wrong] put the private dinner on the company card | hedonism | work | adult | B | =map

### 3.4 Achievement (map: B, then U; G -3)

Definition: personal success through showing competence by social standards. Motivational goal: be capable and be
seen to be capable. Grounded in the group's need for competent performance. Weakly visible in behaviour because the
norm to work hard is so widespread (Bardi and Schwartz 2003). Achievement by beating rivals reads Black; by patient
mastery reads Blue; by strength, endurance or a craft rooted in land and community reads Green or Red (F8).

- race to finish the puzzle first | achievement | play | child | R/B | partial: competitive play reads R (map R -.5)
- collect every gold star on the chart | achievement | school | child | W/B | partial: approval by the rules reads W
- practise the piano every day for the recital | achievement | leisure | child, juv | U/W | =map (U); F8
- show your report card to every relative | achievement | family | child, juv | B/W | =map
- learn every name in the new class on the first day | achievement | school | juv | U/W | =map (U)
- run for class president | achievement | school | juv | B/W | =map
- train for the regional swimming final | achievement | body | juv, ya | G/R/B | !map F8 (physical prowess)
- study late before the exam even when you are ready | achievement | school | juv, ya | U/B | =map
- [inner] decide you will be the first in your family with a degree | achievement | school | juv, ya | B/W | =map (W family pride)
- take extra courses to graduate early | achievement | school | ya | U/B | =map
- pick the degree that pays best | achievement | school | ya | B | =map
- do the unpaid internship in the big city | achievement | work | ya | B | =map
- take the job you hate because it looks good on paper | achievement | work | ya | B | =map
- become the youngest manager in the company | achievement | work | ya | B | =map
- save hard to buy a flat before thirty | achievement | money | ya | B/U/W | =map
- set a personal record at the gym | achievement | body | ya, adult | R/G/B | !map F8 partly
- work every weekend to make partner | achievement | work | adult | B | =map
- master a craft over ten years | achievement | work | adult | U | =map (U); F8
- publish your research | achievement | work | adult | U/B | =map
- win the dinner argument by sheer preparation | achievement | conflict | adult | U/B | =map
- get the promotion before your rival does | achievement | work | adult | B | =map
- run a marathon under four hours | achievement | body | adult | R/G/B | !map F8
- coach your child's team to win the league | achievement | family | adult | B/R/W | partial
- push your child to top the class | achievement | family | adult | B/U | =map
- learn to cook as well as a professional | achievement | home | adult | U | =map (U)
- teach yourself to fix your own car | achievement | home | adult | U/R | =map (U)
- keep a perfect lawn to outshine the neighbours | achievement | home | adult, mature | B/G | partial
- enter your preserves at the county fair | achievement | community | adult, mature | G/W | !map F8 (craft in community)
- win the chili contest at the town fair | achievement | community | adult | R/G/B | partial
- top the fundraising leaderboard for the cause | achievement | community | adult | W/B | partial
- grow the biggest congregation in the district | achievement | faith | adult | B/W | partial (W church)
- outwork everyone on the farm at harvest | achievement | work | adult | G/W | !map F8 (G work ethic)
- learn a new skill every year to stay employable | achievement | work | adult, mature | U/B | =map
- be the best-dressed mourner at the funeral | achievement | loss | adult | B | =map (also face)
- finish the degree at sixty | achievement | school | mature | U/B | =map
- take up a competitive sport after you retire | achievement | aging | mature, elder | R/B | partial
- keep working past seventy to stay at the top | achievement | work | elder | B | =map
- write a bestselling memoir in retirement | achievement | aging | elder | B/U | =map
- hand-carve a perfect chair for your grandchild | achievement | family | elder | U/G | !map F8 (G craft for kin)
- [inner] compare your salary with your old classmates' | achievement | money | adult | B | =map
- [inner] replay every mistake in the presentation all night | achievement | work | adult | U/B | =map
- [inner] envy your sister's success | achievement | family | adult | B | =map
- [inner] promise yourself you will prove the doubters wrong | achievement | conflict | juv, ya | B/R | =map
- [wrong] cheat on the exam to keep top marks | achievement | school | juv, ya | B | =map
- [wrong] pay someone to write your essay | achievement | school | ya | B | =map
- [wrong] pad your CV with a degree you never finished | achievement | work | ya, adult | B | =map
- [wrong] take credit for a colleague's idea | achievement | work | adult | B | =map
- [wrong] take banned drugs to win the race | achievement | body | ya | B | =map
- [wrong] fake the sales figures to hit the target | achievement | work | adult | B | =map

### 3.5 Power (map: B, then R; W -1.5, G -1.5), with face

Definition: social status and prestige, control or dominance over people and resources. Motivational goal: be on top
and hold the levers. Refined split: **dominance** (make people do what you want), **resources** (control through
money and goods), and the new value **face** (keep your public image, avoid humiliation), which sits between power and
security. Power through office, rank or law reads White (F5); through secrets and persuasion reads Blue (F6).

Power-dominance
- boss the younger kids in the game | power-dominance | play | child | R/B | =map
- decide who may sit at your lunch table | power-dominance | school | child, juv | B | =map
- lead the gang that rules the playground | power-dominance | friends | child, juv | R/B | =map
- become team captain and pick the line-up | power-dominance | play | juv | W/R | partial F5
- spread a rumour to topple the most popular girl | power-dominance | friends | juv | B/U | =map (F6 part)
- win the argument by shouting the other person down | power-dominance | conflict | all | R | =map
- join the army officer track | power-dominance | work | ya | W/B | !map F5
- become the one who gives orders on the building site | power-dominance | work | adult | R/W | partial
- climb to head of department and set the rules | power-dominance | work | adult | W/B | !map F5
- fire the employee who challenged you in a meeting | power-dominance | work | adult | B | =map
- play your colleagues against each other | power-dominance | work | adult | B/U | =map (F6)
- organise the strike and lead it | power-dominance | work | adult | R/W | partial
- collect secrets to use against your rivals | power-dominance | conflict | adult | U/B | !map F6
- make every family decision without asking anyone | power-dominance | family | adult | B/W | partial
- take over the family business ahead of your siblings | power-dominance | family | adult | B | =map
- run for mayor | power-dominance | community | adult, mature | W/B | !map F5
- chair the church council | power-dominance | faith | adult, mature | W | !map F5
- pull rank to get a better hospital room | power-dominance | body | elder | B/W | partial
- threaten to cut a child out of the will | power-dominance | family | elder | B | =map
- become the elder whose word settles every quarrel | power-dominance | community | elder | W/G | !map F5
- [inner] fantasise about humiliating your boss | power-dominance | work | adult | B/R | =map
- [inner] decide you will never be at anyone's mercy again | power-dominance | conflict | ya, adult | B | =map
- [inner] feel quiet satisfaction when your rival fails | power-dominance | conflict | adult | B | =map
- [wrong] bully a smaller kid for their lunch money | power-dominance | school | child, juv | B/R | =map
- [wrong] control what your partner wears and who they see | power-dominance | love | ya, adult | B | =map
- [wrong] read your partner's messages in secret | power-dominance | love | ya, adult | B/U | =map
- [wrong] betray your business partner to take control | power-dominance | work | adult | B | =map

Power-resources
- hoard the best toys and trade them for favours | power-resources | play | child | B | =map
- run a sweet-selling racket at school | power-resources | money | juv | B | =map
- choose friends whose parents are rich | power-resources | friends | juv, ya | B | =map
- take the high-paying job over the meaningful one | power-resources | work | ya, adult | B | =map
- invest hard to be a millionaire by forty | power-resources | money | ya, adult | B/R | =map
- marry for money | power-resources | love | ya, adult | B | =map
- buy rental flats one by one | power-resources | money | adult | B | =map
- buy the biggest house on the street | power-resources | home | adult | B | =map
- corner the local market for your trade | power-resources | work | adult | B/U | =map
- hold the family purse strings tightly | power-resources | family | adult, mature | B/W | =map
- use your money to get your child into the elite school | power-resources | family | adult | B | =map
- buy a seat on the charity's board | power-resources | community | mature | B/W | partial
- [wrong] skim money from the club treasury | power-resources | money | adult | B | =map
- [wrong] hide income offshore to avoid tax | power-resources | money | adult, mature | B/U | =map
- [wrong] press an ageing parent to sign the house over to you | power-resources | family | adult | B | =map
- [wrong] keep the inheritance from your siblings | power-resources | loss | adult, mature | B | =map

Face (no map entry; as a power plus security blend it would lead Blue; I read it White for honour, Black for image)
- never admit you were wrong in front of others | face | conflict | all | B/W | no entry
- cry only where nobody can see | face | loss | child, juv | W/B | no entry
- post only the best photos of your life | face | leisure | juv, ya, adult | B | no entry
- hide the family's money troubles from the neighbours | face | money | adult | W/B | no entry
- say the divorce was your idea | face | love | adult | B | no entry
- go to the wedding despite the feud, to keep up appearances | face | family | adult | W | no entry
- demand an apology after a public insult | face | conflict | adult | W/R | no entry
- refuse the food bank out of pride | face | money | adult, elder | W/B | no entry
- keep the illness secret so nobody pities you | face | body | mature, elder | B/W | no entry
- give your name to a building with a large donation | face | community | mature, elder | B/W | no entry
- throw a lavish funeral to show the family's standing | face | loss | adult | W/B | no entry
- [inner] relive a public humiliation for years | face | conflict | all | B/W | no entry
- [wrong] lie to the neighbours to cover up your son's arrest | face | family | adult | B | no entry
- [wrong] strike back at the family that slighted your family's name | face | conflict | ya, adult | R/B | no entry

### 3.6 Security (map: W and U)

Definition: safety, harmony and stability of society, of relationships and of self. Motivational goal: keep harm
away and keep things predictable. Refined split: **personal** (safety in your own surroundings: health, home, money)
and **societal** (a safe, stable country and order). Weakly visible in behaviour (Bardi and Schwartz 2003), partly
because caution is the norm. Security by planning reads Blue, by rule and community reads White, by self-sufficiency
and home ground reads Green, by force reads Red or Black.

Security-personal
- keep the nightlight on | security-personal | home | child | W/U | =map
- stay close to your parent in crowds | security-personal | family | child | W/G | partial (G kin)
- refuse to go into the deep end | security-personal | body | child | W/U | =map
- eat only the foods you already know | security-personal | body | child, elder | W/G | partial
- save birthday money in a jar | security-personal | money | child | U/W | =map
- lock your diary and hide the key | security-personal | home | juv | U | =map
- pick the friend everyone trusts | security-personal | friends | juv | W | =map
- avoid the dark park on the walk home | security-personal | body | juv, ya, adult | U/W | =map
- choose the safe college close to home | security-personal | school | ya | W/G | partial (G home)
- learn self-defence | security-personal | body | ya, adult | R/W | partial: protection by force reads R (map R -1.5)
- take the safer job with the pension | security-personal | work | ya, adult | W/U | =map
- build an emergency fund of six months' pay | security-personal | money | adult | U | =map
- buy every kind of insurance on offer | security-personal | money | adult | U/W | =map
- put extra locks and an alarm on the house | security-personal | home | adult | U/W | =map
- buy a gun for the house | security-personal | home | adult | B/R/W | partial: force reads B/R
- move to a safer neighbourhood | security-personal | home | adult | W/U | =map
- stockpile food and water in the cellar | security-personal | home | adult | U/G | partial: G self-sufficiency
- keep the job you hate for the health insurance | security-personal | work | adult | W/U | =map
- stay in a stale marriage for the stability | security-personal | love | adult, mature | W | =map
- get every check-up on time | security-personal | body | adult, mature | U/W | =map
- quit smoking after the scare | security-personal | body | adult, mature | U/W/G | =map
- vaccinate the children on schedule | security-personal | family | adult | W/U | =map
- tell nobody where you keep your savings | security-personal | money | adult | U/B | partial
- pay off the mortgage early | security-personal | money | adult, mature | U/W | =map
- stick with the bank your parents used | security-personal | money | adult | W/G | partial
- keep the house clean and in order | security-personal | home | all | W | =map
- keep cash under the mattress | security-personal | money | elder | U/B | partial
- wear the medical alarm your daughter bought | security-personal | aging | elder | U/W | =map
- move in with your son after the fall | security-personal | aging | elder | W/G | partial
- [inner] worry every night about losing your job | security-personal | work | adult | U/W | =map
- [inner] check three times that the stove is off | security-personal | home | adult, elder | U | =map
- [inner] decide never to borrow money again | security-personal | money | adult | U/W | =map
- [wrong] hide money from your spouse just in case | security-personal | love | adult | B/U | partial

Security-societal
- vote for the law-and-order candidate | security-societal | community | adult | W | =map
- join the neighbourhood watch | security-societal | community | adult, mature | W | =map
- report the unattended bag to the guard | security-societal | community | adult | W | =map
- back tighter border controls | security-societal | community | adult, mature | W/B | partial
- enlist after the attack on your country | security-societal | community | ya | W/R | partial (R part)
- buy goods made in your own country | security-societal | money | adult | W/G | partial
- vote in every election | security-societal | community | adult | W | =map
- back the strong leader in the crisis | security-societal | community | adult | W/B | partial
- keep the children inside during the riots | security-societal | family | adult | W/U | =map
- pray for peace in the land | security-societal | faith | all | W | =map
- keep the curfew during the epidemic | security-societal | community | all | W | =map
- give to the volunteer fire brigade | security-societal | community | adult | W | =map
- train as a nurse for a secure career that the town needs | security-societal | work | ya | W/U | =map

### 3.7 Conformity (map: W, then U; R -3)

Definition: restraint of actions, inclinations and impulses likely to upset or harm others and break social
expectations. Motivational goal: fit, and do not disrupt. Refined split: **rules** (laws and formal duties) and
**interpersonal** (do not upset or hurt people). Rules reads White; interpersonal tact reads White or Green; holding
back an impulse reads Blue (F2). Weakly visible in behaviour because most people conform on most days. Note that
conformity to a peer group can produce rule-breaking.

Conformity-rules
- wait for the green light even when the road is empty | conformity-rules | community | child | W | =map
- put up your hand before speaking | conformity-rules | school | child | W | =map
- finish your homework before you play | conformity-rules | school | child | W/U | =map
- keep your parents' curfew to the minute | conformity-rules | family | juv | W | =map
- wear the uniform exactly by the rules | conformity-rules | school | juv | W | =map
- tell the teacher a classmate cheated | conformity-rules | school | juv | W | =map
- finish the degree you started because you said you would | conformity-rules | school | ya | W | =map
- keep to the speed limit | conformity-rules | community | ya, adult, mature, elder | W | =map
- pay every parking fine on time | conformity-rules | money | adult | W | =map
- declare every euro on your tax return | conformity-rules | money | adult | W | =map
- hand back the extra change the cashier gave you | conformity-rules | money | all | W | =map
- follow the safety rules on site even when they slow you down | conformity-rules | work | adult | W/U | =map
- report your own mistake to the supervisor | conformity-rules | work | adult | W | =map
- sign the marriage contract the lawyer drafted | conformity-rules | love | adult | W/U | =map
- keep the food rules of your faith at the work dinner | conformity-rules | faith | adult | W | =map
- follow the will exactly though you disagree with it | conformity-rules | loss | adult | W | =map
- follow the doctor's orders to the letter | conformity-rules | body | mature, elder | W/U | =map
- move into assisted living because the children insist | conformity-rules | aging | elder | W | =map

Conformity-interpersonal
- eat everything on your plate at a friend's house | conformity-interpersonal | friends | child | W | =map
- keep quiet in the restaurant | conformity-interpersonal | leisure | child | W | =map
- go along with the group's choice of film | conformity-interpersonal | friends | juv, ya | W | =map
- stay in the friend group you have outgrown | conformity-interpersonal | friends | ya | W | =map
- take the job your parents want for you | conformity-interpersonal | work | ya | W | =map
- marry within the circle your family expects | conformity-interpersonal | love | ya | W/G | =map
- hide your tattoo at the family gathering | conformity-interpersonal | family | ya, adult | W | =map
- call your mother every Sunday because she expects it | conformity-interpersonal | family | adult | W | =map
- laugh at your boss's joke | conformity-interpersonal | work | adult | W/B | partial
- keep your opinion to yourself in the meeting | conformity-interpersonal | work | adult | W/U | =map
- go to the office party though you would rather not | conformity-interpersonal | work | adult | W | =map
- bite your tongue when your in-laws criticise | conformity-interpersonal | family | adult | W/U | =map
- not mention your promotion to a friend who just lost a job | conformity-interpersonal | friends | adult | W/G | =map
- join the club all your colleagues belong to | conformity-interpersonal | community | adult | W | =map
- keep your garden looking like the neighbours' | conformity-interpersonal | home | adult | W | =map
- accept the seat they give you at the wedding | conformity-interpersonal | community | adult | W | =map
- turn the music down for the neighbours | conformity-interpersonal | home | all | W | =map
- say you love the gift | conformity-interpersonal | friends | all | W | =map
- keep the peace at dinner rather than start an argument | conformity-interpersonal | family | all | W/U | =map
- dress soberly for the funeral | conformity-interpersonal | loss | all | W | =map
- [inner] swallow your anger at the slight | conformity-interpersonal | conflict | all | W/U | =map (U restraint, F2)
- [inner] decide not to make a scene | conformity-interpersonal | conflict | all | W/U | =map
- [inner] hold back tears in public | conformity-interpersonal | loss | all | W/U | =map (F2)
- [inner] feel guilty for disappointing your father | conformity-interpersonal | family | juv, ya, adult | W | =map
- [wrong] join in teasing the new kid so you are not next | conformity-interpersonal | school | child, juv | B/W | partial: going along reads W, the act reads B
- [wrong] go along when the group shoplifts | conformity-interpersonal | friends | juv | B/R | !map: peer conformity against the rules
- [wrong] stay silent about a colleague's misconduct to avoid trouble | conformity-interpersonal | work | adult | W/B | partial

### 3.8 Tradition (map: G, then W; B -3.5, U -1.5), with humility

Definition: respect, commitment and acceptance of the customs and ideas your culture or religion provides.
Motivational goal: keep faith with those who came before. Tradition is one of the two values most visible in
behaviour (prayer, services, holy texts). The refined theory keeps **tradition** (keep cultural, family or religious
ways) and splits off **humility** (recognise your smallness, accept your lot). Religious rite and duty read White;
ancestry, land, the old ways and "how it has always been" read Green. Memorising the old texts reads partly Blue
(map U -1.5).

Tradition
- help set the table for the holiday feast | tradition | family | child | W/G | =map
- learn the old songs from your grandmother | tradition | family | child | G/W | =map
- memorise the sacred verses for your coming-of-age | tradition | faith | child, juv | W/U | partial: memory work reads U (map U -1.5)
- learn your grandparents' language | tradition | family | juv, ya | G/W | =map
- join the folk-dance group | tradition | leisure | juv, ya | G/W | =map
- follow your father into his trade | tradition | work | ya | G/W | =map
- accept the match your family arranges | tradition | love | ya | W/G | =map
- have a religious wedding to please the elders | tradition | love | ya | W | =map
- go home every year for the harvest festival | tradition | home | ya, adult | G | =map
- light the candles on the feast day | tradition | faith | all | W | =map
- go to services every week | tradition | faith | all | W | =map
- pray before every meal | tradition | faith | all | W | =map
- keep the weekly day of rest | tradition | faith | all | W | =map
- wear traditional dress at the festival | tradition | community | all | G/W | =map
- defer to the eldest at every family decision | tradition | family | all | W/G | =map
- fast through the holy month | tradition | faith | juv, ya, adult, mature, elder | W | =map
- keep the family recipe exactly as written | tradition | home | adult | G/W | =map
- keep the food rules of your faith at home | tradition | home | adult | W | =map
- name the baby after a grandparent | tradition | family | adult | G/W | =map
- bring the baby into the family faith by its rite | tradition | faith | adult | W | =map
- dress the children in the clothes of your faith | tradition | family | adult | W | =map
- turn down the job that needs you on the holy day | tradition | work | adult | W | =map
- use the remedies your grandmother taught you | tradition | body | adult, elder | G | =map
- refuse surgery and go to the traditional healer | tradition | body | adult | G | =map
- refuse to sell the heirloom however tight money gets | tradition | money | adult | G/W | =map
- join the lodge your father belonged to | tradition | community | adult | W | =map
- play the old instrument at weddings | tradition | community | juv, ya, adult, mature, elder | G/W | =map
- look after the ancestral shrine | tradition | faith | adult | G/W | =map
- go on pilgrimage | tradition | faith | adult, mature, elder | W | =map
- tend the family graves on the day of the dead | tradition | loss | all | G/W | =map
- mourn for the full traditional period | tradition | loss | adult | W/G | =map
- bury your father by the old rites | tradition | loss | adult | W/G | =map
- cook the dead person's favourite dish on the anniversary | tradition | loss | adult | G | =map
- keep your mother's house as it was after she dies | tradition | loss | adult | G | =map
- keep the farm in the family against every good offer | tradition | home | adult, mature | G | =map
- renew your vows in the church where you married | tradition | love | mature | W | =map
- keep the old village festival alive | tradition | community | mature, elder | G/W | =map
- vote for the party that defends the old ways | tradition | community | mature | W/G | =map
- teach the grandchildren the old stories | tradition | aging | elder | G/W | =map
- [inner] feel ashamed for breaking the fast | tradition | faith | ya, adult | W | =map
- [inner] decide to raise your children in the faith you left | tradition | faith | adult | W/G | =map
- [inner] long for the way the holidays used to be | tradition | aging | mature, elder | G | =map
- [wrong] cut off your daughter for marrying outside the faith | tradition | family | mature | W/B | partial: the rejection reads B (map B -3.5)
- [wrong] join the old feud against the neighbouring family | tradition | conflict | ya, adult | R/G | partial: blood feud reads R

Humility (refined value; no map entry of its own, scored under tradition)
- let your little cousin win and never tell | humility | play | child | W/G | =map (as tradition)
- play down your prize at the family dinner | humility | family | juv, adult | W | =map
- give the credit to the team at the award night | humility | work | adult | W | =map
- take the worst bed so your guests get the best | humility | home | adult | W | =map
- take the small job at church without complaint | humility | faith | adult | W | =map
- stand under the night sky and feel how small you are | humility | leisure | all | G | =map
- step down so a younger person can lead | humility | work | mature, elder | W/G | =map
- ask the young nurse for help without embarrassment | humility | aging | elder | W/G | =map
- [inner] accept that you will never be famous | humility | aging | mature | G/W | =map
- [inner] accept the illness as your lot | humility | body | mature, elder | G/W | =map

### 3.9 Benevolence (map: W and G; B -1, R -1)

Definition: preserving and enhancing the welfare of the people you are in frequent personal contact with. Motivational
goal: look after your own. Ranked first of all values on average across nations. Refined split: **caring** (devotion to
the welfare of your group: help, forgive, no grudges) and **dependability** (be a reliable, trustworthy member: others
can count on me). Weakly visible in behaviour, because kindness to your own is the norm. Caring reads Green and White;
dependability reads White (F9). Loyalty that breaks the law for kin reads Green, Red or Black, not White.

Benevolence-caring
- share your sweets with your little brother | benevolence-caring | family | child | W/G | =map
- comfort a crying classmate | benevolence-caring | school | child | W/G | =map
- make a birthday card for grandma | benevolence-caring | family | child | G/W | =map
- stand up for your friend when they are teased | benevolence-caring | friends | child, juv | W/R | partial: hot loyalty reads R
- take the blame to protect your sister | benevolence-caring | family | child, juv | W/R | partial
- stay up all night talking a friend through a breakup | benevolence-caring | friends | juv, ya | G/W/R | =map
- visit your grandmother every week in the home | benevolence-caring | aging | ya, adult | G/W | =map
- give your partner the last piece of cake | benevolence-caring | love | all | W/G | =map
- cook for the friend who just had a baby | benevolence-caring | friends | adult | G/W | =map
- move back home to nurse a dying parent | benevolence-caring | family | adult | G/W | =map
- take in your sister's children when she cannot cope | benevolence-caring | family | adult | G/W | =map
- give your partner a kidney | benevolence-caring | body | adult | W/G | =map
- cut your hours to be with the children | benevolence-caring | work | adult | G/W | =map
- lend money to a cousin knowing it will not come back | benevolence-caring | money | adult | W/G | =map
- forgive your father for the years he was gone | benevolence-caring | family | adult | W/G | =map
- make peace with your brother after the funeral | benevolence-caring | loss | adult | W/G | =map
- help your neighbour move house | benevolence-caring | community | adult | W | =map
- bring soup to the neighbour who is ill | benevolence-caring | community | all | W/G | =map
- look after a friend's dog while they are in hospital | benevolence-caring | friends | adult | G/W | =map
- pray for a friend in trouble | benevolence-caring | faith | all | W | =map
- sit with a dying friend in the hospice | benevolence-caring | loss | adult, mature | W/G | =map
- care for your spouse through dementia | benevolence-caring | aging | elder | G/W | =map
- write letters to the grandchildren | benevolence-caring | aging | elder | G/W | =map
- [inner] forgive the friend who forgot your birthday | benevolence-caring | friends | all | W/G | =map
- [inner] decide to let go of the grudge against your brother | benevolence-caring | family | adult | W/G | =map
- [wrong] lie to the police to cover for your son | benevolence-caring | family | adult | G/R/B | !map: loyalty over law is not White
- [wrong] steal the medicine your wife cannot afford | benevolence-caring | body | adult | R/G | !map: the means read R
- [wrong] pull strings to get your friend's child into the school | benevolence-caring | community | adult | G/B | partial

Benevolence-dependability
- keep your promise to walk the dog every day | benevolence-dependability | home | child | W | =map
- return the borrowed book on time | benevolence-dependability | school | juv | W | =map
- keep the secret you were trusted with | benevolence-dependability | friends | all | W/U | =map
- be the designated driver | benevolence-dependability | friends | ya | W | =map
- be the friend who answers at three in the morning | benevolence-dependability | friends | ya, adult | W | =map
- show up for every shift | benevolence-dependability | work | adult | W | =map
- cover the night shift for a colleague whose child is sick | benevolence-dependability | work | adult | W/G | =map
- pay back the loan to the day | benevolence-dependability | money | adult | W | =map
- stay faithful while your partner works abroad | benevolence-dependability | love | adult | W | =map
- be a godparent who actually shows up | benevolence-dependability | family | adult | W | =map
- tell your friend the truth about their drinking | benevolence-dependability | friends | adult | W/U/R | =map
- coach the youth team every season for years | benevolence-dependability | community | adult, mature | W | =map
- keep the family business going so the workers keep their jobs | benevolence-dependability | work | mature | W/G | =map
- carry out your parent's will faithfully | benevolence-dependability | loss | adult | W | =map
- [inner] feel the weight of everyone counting on you | benevolence-dependability | family | adult | W | =map
- [inner] vow never to let your children down as your father did | benevolence-dependability | family | ya, adult | W | =map

### 3.10 Universalism (map: G, then W; U -1, B -1)

Definition: understanding, appreciation, tolerance and protection for the welfare of all people and of nature.
Motivational goal: care about everyone, not only your own. Includes wisdom, a world at peace and a world of beauty.
Refined split: **concern** (equality, justice, protection for all), **nature** (preserve the environment) and
**tolerance** (accept and understand people who differ). Concern reads White (F3), nature reads Green (F4), tolerance
reads White, Green or Blue (open mind). Wrongs done for a universalist end usually have Red means.

Universalism-concern
- give your pocket money to the man begging outside the shop | universalism-concern | community | child | W/G | partial F3
- invite the lonely new kid to play | universalism-concern | school | child, juv | W | !map F3
- refuse to laugh at the racist joke | universalism-concern | friends | juv, ya | W | !map F3
- start a petition at school for fair grading | universalism-concern | school | juv | W | !map F3
- march for equal rights | universalism-concern | community | juv, ya, adult | W/R | !map F3
- volunteer at the food bank on Sundays | universalism-concern | community | adult | W | !map F3
- become a public defender | universalism-concern | work | ya, adult | W | !map F3
- pay your workers a fair wage when cheaper is possible | universalism-concern | work | adult | W | !map F3
- blow the whistle on fraud at work | universalism-concern | work | adult | W | !map F3
- boycott the brand that uses child labour | universalism-concern | money | adult | W | !map F3
- give a tenth of your income to charity | universalism-concern | money | adult | W | !map F3
- split the housework evenly with your partner | universalism-concern | love | ya, adult | W | !map F3
- vote for higher taxes to fund the schools | universalism-concern | community | adult | W | !map F3
- sponsor a refugee family | universalism-concern | community | adult, mature | W/G | partial
- join the peace vigil | universalism-concern | faith | all | W | !map F3
- leave your estate to a hunger charity | universalism-concern | loss | elder | W | !map F3
- [inner] feel your blood rise at an injustice on the news | universalism-concern | community | all | W/R | !map F3
- [inner] decide your life must serve something bigger than you | universalism-concern | faith | ya, adult | W | !map F3
- [wrong] break into the lab to free the animals | universalism-concern | conflict | ya | R/G | partial: Green end, Red means
- [wrong] smash the bank's windows in protest | universalism-concern | conflict | ya | R | !map: Red means for a White end

Universalism-nature
- rescue the beetle from the swimming pool | universalism-nature | play | child | G | =map F4
- plant a tree on your birthday | universalism-nature | home | child | G | =map
- give up meat for the animals' sake | universalism-nature | body | juv, ya | G/W | =map
- pick up litter on the beach | universalism-nature | community | all | G/W | =map
- take a job with the national park | universalism-nature | work | ya | G | =map
- chain yourself to a tree to stop the road | universalism-nature | conflict | ya | G/R | =map
- compost the kitchen scraps | universalism-nature | home | adult | G | =map
- cycle to work to cut your emissions | universalism-nature | work | adult | G/W | =map
- join the campaign to save the local wood | universalism-nature | community | adult | G | =map
- refuse to fly for a year | universalism-nature | leisure | adult | G/W | =map
- keep bees | universalism-nature | home | adult, mature, elder | G | =map
- teach the grandchildren the names of the birds | universalism-nature | aging | elder | G | =map
- leave your land to a nature trust | universalism-nature | loss | elder | G | =map
- [inner] grieve for the forest that was cut down | universalism-nature | loss | adult | G | =map

Universalism-tolerance (and wisdom)
- befriend the kid who does not speak your language | universalism-tolerance | school | child | W/G | partial
- learn about another faith's holy days | universalism-tolerance | faith | juv, adult | U/W | !map F1 partly
- read books from countries you have never visited | universalism-tolerance | leisure | all | U/W | !map F1
- date someone from a different faith | universalism-tolerance | love | ya | R/W/G | partial
- listen fully to a friend whose politics you hate | universalism-tolerance | friends | adult | W/U | partial
- hire the candidate with the unusual background | universalism-tolerance | work | adult | W | !map F3
- move into a mixed neighbourhood on purpose | universalism-tolerance | home | adult | W | partial
- take in an exchange student | universalism-tolerance | home | adult | W/G | partial
- welcome your child's same-sex partner at the table | universalism-tolerance | family | mature | W/G | partial
- make peace with the old enemy village | universalism-tolerance | conflict | elder | W | !map F3
- [inner] change your mind about a group you once despised | universalism-tolerance | conflict | adult, mature | W/U | partial
- [inner] accept that your grown child lives a life you do not understand | universalism-tolerance | family | mature, elder | G/W | =map
- [inner] look back over your whole life and make peace with it | universalism (wisdom) | aging | elder | G/W/U | =map

### 3.11 Count and pattern of flags in section 3

Acts per value: self-direction 53 (thought 26, action 27); stimulation 44; hedonism 45; achievement 49; power 57
(dominance 27, resources 16, face 14); security 46 (personal 33, societal 13); conformity 45 (rules 18,
interpersonal 27); tradition 54 (tradition 44, humility 10); benevolence 44 (caring 28, dependability 16);
universalism 47 (concern 20, nature 14, tolerance and wisdom 13). Total 484.

Where my readings disagree with the map most often:
1. Self-direction-thought (F1): nearly every curiosity and learning act reads Blue and scores Black. Largest and most
   systematic gap. Splitting self-direction into thought (Blue-leading) and action (Black/Red-leading) would fix most.
2. Universalism-concern (F3): fairness, equality and charity acts read White and score Green. A refined split with
   concern leading White and nature leading Green would fix this.
3. Institutional power (F5) and power by mind (F6): offices, ranks and elections read White; secrets and manipulation
   read Blue. The map gives power W -1.5 and U .5.
4. Hedonism's quiet pleasures (F7) and achievement by body or craft (F8): Green readings scored at G 0 and G -3.
5. Face and humility have no entries. Face reads W/B; humility reads W/G.
6. Value-driven wrongs often have means of a different color from the value's end (lying to the police out of
   loyalty, smashing windows for justice). The means/ends split in the library format already handles this.

## 4. Value dilemmas: real choices where two values clash

Sources:
- Schwartz, S. H. (2012), and Schwartz et al. (2012), cited in section 1: the circle, the idea that opposite values
  cannot be served by one act, and that values come into awareness when an act would serve one and hurt another.
- Schwartz, S. H., et al. (2017). Value tradeoffs propel and inhibit behavior. European Journal of Social Psychology,
  47(3), 241-258 (cited in section 2): the value on one side of the circle pushes an act, the opposite value brakes it.
- Bardi, A., & Schwartz, S. H. (2003), cited in section 2: values predict acts best where no strong norm already
  decides the act for everyone.
- Tetlock, P. E. (1986). A value pluralism model of ideological reasoning. Journal of Personality and Social
  Psychology, 50(4), 819-827. Summary read via https://psychology.iresearchnet.com/social-psychology/social-cognition/value-pluralism-model/
- Tetlock, P. E. (2003). Thinking the unthinkable: sacred values and taboo cognitions. Trends in Cognitive Sciences,
  7(7), 320-324. https://www.gwern.net/doc/philosophy/ethics/2003-tetlock.pdf (builds on Tetlock, Kristel, Elson,
  Green & Lerner 2000, The psychology of the unthinkable, JPSP 78(5), 853-870).
- Waytz, A., Dungan, J., & Young, L. (2013). The whistleblower's dilemma and the fairness-loyalty tradeoff. Journal of
  Experimental Social Psychology, 49, 1027-1033. https://moralitylab.bc.edu/wp-content/uploads/sites/192/2011/10/WaytzDunganYoungWB.pdf
- Burroughs, J. E., & Rindfleisch, A. (2002). Materialism and well-being: a conflicting values perspective. Journal of
  Consumer Research, 29(3), 348-370. https://ideas.repec.org/a/oup/jconrs/v29y2002i3p348-70.html
- Berg, J. M., Grant, A. M., & Johnson, V. (2010). When callings are calling: crafting work and leisure in pursuit of
  unanswered occupational callings. Organization Science, 21(5), 973-994. https://ideas.repec.org/a/inm/ororsc/v21y2010i5p973-994.html
- Knafo, A., & Schwartz, S. H. (2003). Parenting and adolescents' accuracy in perceiving parental values. Child
  Development, 74(2), 595-611. https://cris.huji.ac.il/en/publications/parenting-and-adolescents-accuracy-in-perceiving-parental-values/
- AARP and S&P Global (2024). Working caregivers survey (1,200 caregivers at large US firms, autumn 2023).
  https://www.aarp.org/caregiving/life-balance/info-2024/working-caregivers-report
- Berry, J. W. (1997). Immigration, acculturation, and adaptation. Applied Psychology, 46(1), 5-34 (the four
  acculturation strategies; overview read via https://www.simplypsychology.org/acculturation-definition.html).

### 4.1 What the research says about value conflict, as rules a simulator can use

- **Where the sharpest dilemmas sit.** Values opposite on the circle (openness against conservation, self-enhancement
  against self-transcendence) cannot be served by one act, so a choice between them is felt as a loss either way
  (Schwartz 2012). The value that pushes an act and the value that brakes it can both be named for any act (Schwartz
  et al. 2017). Neighbouring values can also clash: loyalty to a friend against fairness to everyone is a clash
  inside the social-focus half of the circle (Waytz et al. 2013).
- **When a dilemma is felt at all.** A value guides choice when it is important to the person and the situation
  activates it (Schwartz 2012). Engine check: raise a dilemma only when both values are in the person's top four or
  five and the event touches both.
- **Equal or unequal weights.** Tetlock's value pluralism model: when one value clearly outweighs the other, people
  decide fast and play the weaker value down (denying it, or bolstering the stronger one). When the two are about
  equally strong, the conflict is painful and people think harder: they weigh both sides and look for trade-off rules
  and compromises ("integrative complexity"). Engine check: small gap between the two values means more deliberation,
  more compromise responses and more lingering distress; a large gap means a quick choice and a story that excuses it.
- **Evasion is a real response.** Under accountability, people facing a hard trade-off often pass the buck,
  procrastinate or blur the choice (Tetlock, summarised in the value pluralism entry above). Each dilemma below
  therefore includes at least one delay, hand-off or narrowly-true answer.
- **Sacred against secular.** Tetlock (2003) splits trade-offs into routine (secular against secular: money against
  convenience), taboo (sacred against secular: a parent's care against a salary) and tragic (sacred against sacred:
  one child's need against another's). Onlookers punish taboo trade-offs with outrage, and even lingering over one
  draws blame, while hesitating over a tragic trade-off is seen as proper gravity. People who merely considered a taboo
  trade-off perform acts of moral cleansing afterwards. Engine hook: after a taboo choice, raise the chance of a
  cleansing act (a donation, a rite, a visit, a confession).
- **Fairness against loyalty.** In Waytz et al. (2013), people who rank fairness above loyalty were more willing to
  report wrongdoing (r about .28), willingness fell with closeness (strangers about 5.3 on a 7-point scale, family
  about 4.3), and writing an essay on fairness rather than loyalty raised reporting, most of all for friends and
  family. Engine: reporting likelihood falls with the closeness of the wrongdoer and rises with universalism-concern
  and conformity-rules over benevolence-caring.
- **Chronic conflict costs well-being.** Burroughs and Rindfleisch (2002, 373 adults and 120 students): materialism
  lowers well-being most when it clashes with strongly held family and religious values; the clash itself is a source
  of stress. Engine: a person who keeps choosing self-enhancement against their own strong self-transcendence or
  tradition values should accumulate stress, not only the effects of the choices.
- **The road not taken.** Berg, Grant and Johnson (2010, 31 interviews): people with an unanswered calling reshape
  their job (stress the tasks near the calling, add tasks, reframe the role) or pursue the calling in leisure
  (watching others do it, hobbies). This brings enjoyment and meaning but also regret and stress. The "safe job versus
  calling" dilemma thus has two compromise responses, job crafting and leisure crafting.
- **Care against career in numbers.** In the AARP and S&P Global survey (2024), 67% of working caregivers had some
  difficulty balancing work and care; 27% cut hours or went part-time, 16% turned down a promotion, 16% stopped work
  for a time. These give rough base rates for the response mix in the care dilemma.
- **Parents and children.** Adolescents perceive their parents' values more accurately when parents are warm and less
  controlling (Knafo and Schwartz 2003, 547 Israeli teenagers). For the faith-and-child dilemmas: a warm, less
  controlling parent is likelier to see the child's choice coming and less likely to be blindsided.
- **Migrants choosing between cultures.** Berry's four strategies (integration: keep the old and join the new;
  assimilation: join the new and drop the old; separation: keep the old and stay apart; marginalisation: lose both)
  give the response set for migrant family dilemmas.

### 4.2 The dilemmas

Format. Each dilemma names the clash, where the two values sit on the circle, the stages and domains, and a one-line
situation. Then five responses, each:
`response` | value(s) the response serves | colors (my reading) | map: the engine's leading colors for those
values (loadings summed when two or more; colors listed are those at 40% or more of the top loading) | map note.
`=map` means my first color is among the map's leading colors; `=map (X)` means it matches the map's second color;
`partial` means a later color of mine matches; `!map` means none does. Face is scored as the average of power and
security, humility as tradition, as in section 1.3. Responses are written without outcomes.

#### 4.2.1 Tell the teacher who broke the window, or keep your friend's secret
Clash: conformity-rules (honesty to authority) vs benevolence-caring (loyalty to a friend)  
Circle: conservation against self-transcendence, neighbours; a child's version of the fairness-loyalty trade-off  
Stages: child, juv  
Domains: school, friends  
Situation: The window is broken, the teacher asks the class who did it, and you saw your best friend throw the ball.

- tell the teacher the whole truth when asked | conformity-rules | W | map W, U | =map
- say nothing and take the class detention with everyone | benevolence-caring | G/W | map W, G | =map (G)
- urge your friend to own up before the teacher finds out | benevolence-dependability + conformity-rules | W | map W, U | =map
- [wrong] say you saw an older kid do it | benevolence-caring | B/R | map W, G | !map: the lie reads B and R; loyalty is only the motive
- slip an anonymous note to the teacher so nobody knows it was you | conformity-rules + security-personal | U/W | map W, U | =map (U)

#### 4.2.2 Share the new toy, or keep it for yourself
Clash: hedonism + power-resources (it is mine and I want it) vs benevolence-caring + conformity-interpersonal (be kind; the house rule to share)  
Circle: openness and self-enhancement against conservation and self-transcendence, opposite  
Stages: child  
Domains: play, family  
Situation: You got the remote-control car for your birthday and your little brother is crying for a turn.

- keep it and play with it alone in your room | hedonism + power-resources | B/R | map R, B | =map (B)
- hand it to your brother because he is crying | benevolence-caring | G/W | map W, G | =map (G)
- take turns by the kitchen timer | universalism-concern + conformity-rules | W/U | map W, G | =map
- lend it only in exchange for his best sticker | power-resources | B/U | map B, R | =map
- run to a parent and let them decide | conformity-rules | W | map W, U | =map

#### 4.2.3 Play with the popular group, or stay with the left-out kid
Clash: face + conformity-interpersonal (fit in, be seen with the right group) vs universalism-concern + benevolence-caring (include the outsider)  
Circle: self-enhancement and conservation against self-transcendence  
Stages: child, juv  
Domains: school, friends, play  
Situation: The popular kids finally invite you into their game, but the shy girl you usually play with will be left alone.

- join the popular game and ignore the left-out kid | face + conformity-interpersonal | B/W | map W, U | partial: climbing for status reads B
- stay with the left-out kid and lose your chance with the group | universalism-concern + benevolence-caring | W/G | map G, W | =map (W)
- bring the left-out kid along into the popular game | universalism-concern + conformity-interpersonal | W | map W, G | =map
- go off alone with a book that break time | self-direction-thought | U | map B, R | !map F1: withdrawal into thought reads U
- [inner] tell yourself the left-out kid does not really want friends | face | B | map U | !map: a self-serving story reads B; face alone scores Blue (section 1.3)

#### 4.2.4 Quit the music lessons, or keep going
Clash: hedonism + self-direction-action (do what I enjoy, my choice) vs conformity-interpersonal (do not let down the parents who pay) + achievement (finish what you start)  
Circle: openness against conservation; achievement, a neighbour of hedonism, sides here with conformity  
Stages: child, juv  
Domains: leisure, family  
Situation: Two years of piano lessons your parents work extra shifts to pay for, and you dread every one.

- quit and spend the afternoons playing outside | hedonism + self-direction-action | R/G | map B, R | =map (R)
- keep going so you do not disappoint them | conformity-interpersonal | W | map W, U | =map
- practise hard for the spring competition, then quit | achievement | B/U | map B, U | =map
- ask to switch to the drums instead | self-direction-action + stimulation | R | map B, R | =map (R)
- [wrong] skip the lessons in secret and spend the fee | hedonism + power-resources | B/R | map R, B | =map (B)

#### 4.2.5 Copy the leaked answers, or sit the exam honestly
Clash: achievement + face (the grade, your parents' pride) vs conformity-rules + universalism-concern (rules and fairness to the others)  
Circle: self-enhancement against conservation and self-transcendence  
Stages: juv, ya  
Domains: school  
Situation: The answers to the final exam are going round the group chat the night before.

- [wrong] copy the answers | achievement + face | B | map U, B | =map (B)
- refuse and study through the night instead | achievement + conformity-rules | U/W | map U, W | =map
- report the leak to the head teacher | universalism-concern + conformity-rules | W | map W, G | =map
- refuse to look, but say nothing about the others | conformity-rules + benevolence-caring | W/G | map W, U | =map
- [inner] tell yourself everyone does it, so it does not count | achievement | B | map B, U | =map

#### 4.2.6 Go to the party, or to the family festival
Clash: stimulation + hedonism vs tradition + benevolence-caring  
Circle: openness against conservation, opposite  
Stages: juv, ya  
Domains: family, faith, leisure  
Situation: The biggest party of the year falls on the night of the family's religious festival dinner.

- skip the festival and go to the party | stimulation + hedonism | R | map R, B | =map
- go to the festival and sulk all evening | tradition + conformity-interpersonal | W/G | map W, G | =map
- go to the festival, then slip off to the party at midnight | tradition + stimulation | R/G | map G, R | =map (R)
- bring your friends to the festival | tradition + benevolence-caring | G/W | map G, W | =map
- [wrong] tell your parents you are ill and go to the party | hedonism + self-direction-action | B/R | map B, R | =map

#### 4.2.7 Defend a bullied classmate, or keep your own standing
Clash: universalism-concern + benevolence-caring vs security-personal + face  
Circle: self-transcendence against conservation and self-enhancement  
Stages: juv  
Domains: school, conflict  
Situation: Three boys corner a smaller classmate at the lockers and everyone is watching to see what you do.

- step in and tell them to stop | universalism-concern | W/R | map G | !map F3: protecting the weak reads W; hot courage reads R
- stay out of it so you are not the next target | security-personal | B/U | map W, U | partial: self-protection at another's cost reads B
- tell a teacher quietly after school | universalism-concern + conformity-rules | W/U | map W, G | =map
- sit with the bullied kid at lunch the next day | benevolence-caring + universalism-concern | G/W | map G, W | =map
- [wrong] laugh along with the bullies | face + conformity-interpersonal | B | map W, U | !map: joining cruelty for standing reads B

#### 4.2.8 Art school, or the medicine degree your parents want
Clash: self-direction (thought and action) vs conformity-interpersonal (honour your parents) + security-personal  
Circle: openness against conservation, opposite  
Stages: juv, ya  
Domains: school, family, work  
Situation: You have a place at art school, and your parents, who gave up a great deal for you, have set their hearts on medicine.

- enrol in art school against their wishes | self-direction-action + self-direction-thought | R/U | map B, R | =map (R)
- enrol in medicine to honour them | conformity-interpersonal + security-personal | W/U | map W, U | =map
- study medicine and keep painting at night | conformity-interpersonal + self-direction-thought | U/W | map U, B | =map
- take a gap year to decide | self-direction-thought | U | map B, R | !map F1/F2: deliberating reads U
- propose architecture as a middle way both sides can accept | achievement + conformity-interpersonal | U/W | map U, W | =map

#### 4.2.9 Tell your devout family you have stopped believing
Clash: self-direction-thought + benevolence-dependability (honesty) vs tradition + conformity-interpersonal (family harmony)  
Circle: openness against conservation  
Stages: juv, ya, adult  
Domains: faith, family  
Situation: You no longer believe what your family believes, and the whole family still goes to services together every week.

- tell them plainly at dinner | self-direction-thought + benevolence-dependability | U/R | map B | !map F1: reasoned honesty reads U; saying it out loud reads R
- keep going to services and keep quiet | conformity-interpersonal + tradition | W/G | map W, G | =map
- keep the rites you love and quietly drop the beliefs | tradition + self-direction-thought | G/U | map R, G | =map (G)
- tell one sibling and let the news travel | conformity-interpersonal | U/B | map W, U | =map (U)
- [inner] decide to wait until you live on your own | security-personal | U/B | map W, U | =map (U)

#### 4.2.10 A safe job, or a calling
Clash: security-personal + power-resources (a salary, a pension) vs self-direction + universalism-concern (the work you feel called to)  
Circle: conservation and self-enhancement against openness and self-transcendence  
Stages: ya, adult  
Domains: work, money  
Situation: A permanent post in the tax office, or a low-paid job teaching in a remote village school that you have wanted since you were twelve.

- take the safe post and never look back | security-personal + power-resources | U/W | map U | =map
- answer the calling and live on little | self-direction-action + universalism-concern | W/G | map B, R | !map: a calling to serve reads W/G; the map scores it as self-direction's Black
- take the safe post and teach evening classes for free (leisure crafting) | security-personal + self-direction-thought | U/G | map B, U | =map (U)
- take the safe post and steer it toward training and outreach (job crafting) | achievement + self-direction-thought | U/B | map B, U | =map (U)
- [inner] keep postponing the choice, year after year | security-personal | U/G | map W, U | =map (U)

#### 4.2.11 Move abroad to study, or stay near your family
Clash: stimulation + self-direction-thought vs benevolence-caring + security-personal  
Circle: openness against conservation and self-transcendence  
Stages: ya  
Domains: home, family, school  
Situation: A scholarship abroad, the same month your mother's health begins to fail.

- go, and call home every Sunday | stimulation + self-direction-thought | R/U | map B, R | =map (R)
- stay and study at the local college | benevolence-caring + security-personal | G/W | map W, U | partial: staying with kin on home ground reads G
- go for one year, then decide | stimulation + security-personal | U/R | map R, B | partial: a hedged plan reads U
- go, and send part of the stipend home | stimulation + benevolence-dependability | R/W | map R, G | =map
- [inner] stay, and resent the ones who kept you | conformity-interpersonal | R | map W, U | !map: resentment reads R

#### 4.2.12 Marry the partner your family will not accept
Clash: self-direction-action + benevolence-caring (for the partner) vs tradition + conformity-interpersonal  
Circle: openness against conservation  
Stages: ya, adult  
Domains: love, faith, family  
Situation: You want to marry someone of another faith, and your parents say they will not come to the wedding.

- marry anyway and accept the break | self-direction-action + benevolence-caring | R/G | map B | !map: a love match against the family reads R and G; the map gives B
- end it to keep the family whole | tradition + conformity-interpersonal + benevolence-caring | W/G | map W, G | =map
- marry after a long effort to win the family round | benevolence-caring + conformity-interpersonal | W/U | map W, U | =map
- marry in both traditions, with two ceremonies | tradition + universalism-tolerance | G/W | map G, W | =map
- elope and tell them afterwards | self-direction-action + stimulation | R | map B, R | =map (R)

#### 4.2.13 Loyalty to a friend, or honesty to the boss
Clash: benevolence-caring (loyalty) vs conformity-rules + universalism-concern (fairness)  
Circle: neighbours in the social-focus half of the circle; the fairness-loyalty trade-off (Waytz et al. 2013)  
Stages: ya, adult  
Domains: work, friends  
Situation: Your friend and colleague has been padding his expense claims, and your manager asks you straight out whether you know anything.

- tell the manager the truth | conformity-rules + universalism-concern | W | map W, G | =map
- say you know nothing | benevolence-caring | G/B | map W, G | =map (G)
- warn your friend privately to stop and pay it back | benevolence-caring + benevolence-dependability | W/G | map W, G | =map
- answer only exactly what is asked, narrowly true | face + security-personal | U/B | map U, W | =map
- [inner] decide the company owes him that money anyway | benevolence-caring + power-resources | B/R | map U, B | =map (B)

#### 4.2.14 The well-paid job at the polluting firm
Clash: power-resources + achievement vs universalism-nature  
Circle: self-enhancement against self-transcendence, opposite  
Stages: ya, adult  
Domains: work, money  
Situation: The best offer you have ever had comes from a company whose plant fouls the river you swam in as a child.

- take it and enjoy the salary | power-resources + achievement | B | map B, U | =map
- turn it down for a lower-paid job in conservation | universalism-nature | G | map G | =map
- take it and push for cleaner methods from inside | achievement + universalism-nature | U/G | map B, U | =map (U)
- take it and give a share of every pay cheque to river groups | power-resources + universalism-nature | W/B | map R, B | partial: offsetting is a bargain with conscience (moral cleansing, Tetlock 2003)
- [inner] tell yourself someone else would take it anyway | power-resources | B | map B, R | =map

#### 4.2.15 Join the protest that may get you arrested
Clash: universalism-concern + stimulation vs security-personal + conformity-rules (career, a clean record)  
Circle: self-transcendence and openness against conservation  
Stages: juv, ya  
Domains: community, conflict  
Situation: The march is set to block the bridge, and a record could cost you the teaching post you start in September.

- go and link arms at the front | universalism-concern + stimulation | W/R | map R, G | partial F3: justice reads W
- stay home and give to the legal fund | universalism-concern + security-personal | W/U | map W, G | =map
- go as a legal observer in a bright vest | universalism-concern + conformity-rules | W/U | map W, G | =map
- stay away and say protests achieve nothing | security-societal + conformity-rules | U/W | map W, U | =map (U)
- post about it all night online instead | universalism-concern + stimulation | R/W | map R, G | =map

#### 4.2.16 A year of travel, or a deposit on a flat
Clash: stimulation + self-direction-thought vs security-personal + achievement  
Circle: openness against conservation  
Stages: ya  
Domains: money, leisure, home  
Situation: Six years of savings: enough for a year on the road, or for the deposit on a small flat before prices rise again.

- travel for the year | stimulation + self-direction-thought | R/U | map B, R | =map (R)
- buy the flat | security-personal + achievement | U/W | map U, B | =map
- travel for three months and keep the rest | stimulation + security-personal | R/U | map R, B | =map
- buy the flat and let a room to pay for short trips | security-personal + power-resources | U/B | map U | =map
- [inner] keep checking flights and flats and choose neither | security-personal | U/R | map W, U | =map (U)

#### 4.2.17 Care for an aging parent, or take the career move
Clash: benevolence-caring + tradition (filial duty) vs achievement + self-direction-action  
Circle: self-transcendence and conservation against self-enhancement and openness; a taboo trade-off when framed as money against a parent (Tetlock 2003)  
Stages: adult, mature  
Domains: family, work, aging  
Situation: The promotion you worked ten years for is in another city, the same month your widowed father can no longer live alone.

- turn down the promotion and stay near him | benevolence-caring + tradition | G/W | map G, W | =map
- take the promotion and visit every month | achievement | B | map B, U | =map
- take the promotion and move him into your new home | benevolence-caring + achievement | G/B | map U, B | partial: bringing kin along reads G; the map scores the blend Blue and Black
- take the job and pay for a good care home near you | achievement + security-personal | B/U | map U, B | =map (B)
- ask your sister to take on the care | achievement | B/W | map B, U | =map

#### 4.2.18 Have a child now, or keep the career on track
Clash: benevolence-caring + tradition (family) vs achievement + self-direction-action + hedonism  
Circle: self-transcendence and conservation against self-enhancement and openness  
Stages: ya, adult  
Domains: family, work, body  
Situation: You both want children someday, and the fellowship that would make your name lasts three more years.

- have the child now and slow the career | benevolence-caring + tradition | G/W | map G, W | =map
- wait until after the fellowship | achievement | B/U | map B, U | =map
- decide against having children | self-direction-action + hedonism | B | map B, R | =map
- have the child and split leave equally with your partner | benevolence-caring + universalism-concern | W/G | map G, W | =map (W)
- freeze eggs and decide later | achievement + security-personal | U/B | map U, B | =map

#### 4.2.19 Stay in a dull marriage for the children, or leave for a new love
Clash: benevolence-dependability + tradition (the vows) vs self-direction-action + hedonism  
Circle: conservation and self-transcendence against openness, opposite  
Stages: adult, mature  
Domains: love, family  
Situation: Twenty quiet years, two children still at school, and someone at work who makes you feel alive.

- stay and keep your vows | benevolence-dependability + tradition | W | map G, W | =map (W)
- leave and start again | self-direction-action + hedonism | R/B | map B, R | =map (R)
- stay until the youngest leaves school | benevolence-dependability + security-personal | W/U | map W, U | =map
- go to counselling to rebuild the marriage | benevolence-dependability + self-direction-thought | U/W | map B | !map: deliberate repair reads U and W; the blend scores Black under the map
- [wrong] stay and carry on an affair in secret | hedonism + face | B/R | map R, B | =map (B)

#### 4.2.20 Blow the whistle on the safety problem, or protect your job and your team
Clash: universalism-concern + conformity-rules vs security-personal + benevolence-dependability (loyalty to the team)  
Circle: self-transcendence against conservation, with loyalty on the other side; Waytz et al. (2013)  
Stages: adult  
Domains: work, community  
Situation: You find the test results the plant manager buried, and your whole team's jobs depend on the contract.

- report it to the regulator | universalism-concern + conformity-rules | W | map W, G | =map
- raise it inside the firm and give them a month | conformity-rules + benevolence-dependability | W/U | map W, U | =map
- keep quiet and keep your job | security-personal | B/U | map W, U | partial: silent self-protection at others' risk reads B
- leak the documents anonymously to a journalist | universalism-concern + security-personal | U/W | map W, G | partial F6: working through secrets reads U
- resign and warn your friends there privately | benevolence-caring + security-personal | G/W | map W, U | partial: warning your own pack first reads G

#### 4.2.21 Overtime for the promotion, or evenings with the children
Clash: achievement + power-resources vs benevolence-caring  
Circle: self-enhancement against self-transcendence, opposite  
Stages: adult  
Domains: work, family  
Situation: The partner track means staying late every night for a year, and the children are six and nine.

- take the overtime and the promotion | achievement + power-resources | B | map B, U | =map
- refuse the overtime and be home by six | benevolence-caring | G/W | map W, G | =map (G)
- stay late two nights, home the other three | achievement + benevolence-caring | W/B | map U, B | partial: a fair rota reads W
- bring the children to the office on Saturdays | benevolence-caring + achievement | G/R | map U, B | !map: an improvised mix of family and work reads G and R
- [inner] tell yourself the money is for the children anyway | achievement | B/W | map B, U | =map

#### 4.2.22 Faith, or your grown child's choice
Clash: tradition + conformity-rules vs benevolence-caring + universalism-tolerance  
Circle: conservation against self-transcendence; for the devout, a sacred value against a sacred value (tragic, Tetlock 2003)  
Stages: mature, elder  
Domains: faith, family  
Situation: Your daughter is marrying outside the faith and has asked you to walk her down the aisle at a civil ceremony.

- refuse to attend the wedding | tradition + conformity-rules | W/G | map W, G | =map
- attend and welcome the new partner warmly | benevolence-caring + universalism-tolerance | G/W | map G, W | =map
- attend, and ask your own clergy to bless the couple privately | tradition + benevolence-caring | W/G | map G, W | =map (W)
- [inner] attend, then stay cold and distant for years | tradition + face | B/W | map W, G | partial: a grudge kept to save face reads B
- pray for them and leave it in God's hands | tradition + humility | W/G | map G, W | =map (W)

#### 4.2.23 Lend the savings to your brother, or keep them for your children's schooling
Clash: benevolence-caring (for a sibling) vs benevolence-caring (for your children) + security-personal  
Circle: one value against itself: a tragic trade-off (Tetlock 2003)  
Stages: adult  
Domains: money, family  
Situation: Your brother will lose his house without a loan the size of your children's education fund.

- lend him all of it | benevolence-caring | G/W | map W, G | =map (G)
- refuse and keep it for the children | security-personal + benevolence-caring | U/G | map W, U | =map (U)
- lend half and write down the terms | benevolence-caring + conformity-rules | W/U | map W, U | =map
- help him find work and a cheaper place instead of giving cash | benevolence-caring + achievement | U/W | map U, B | =map
- ask your parents to share the burden with you | benevolence-caring + tradition | G/W | map G, W | =map

#### 4.2.24 Back the refugee housing in your village, or oppose it
Clash: universalism-concern + universalism-tolerance vs security-societal + tradition  
Circle: self-transcendence against conservation  
Stages: adult, mature, elder  
Domains: community  
Situation: The council proposes housing forty refugee families on the old school site, and the village hall meeting is tonight.

- speak for it at the meeting | universalism-concern + universalism-tolerance | W | map G | !map F3: hospitality and equal treatment read W
- sign the petition against it | security-societal + tradition | W/G | map W, G | =map
- support it and volunteer to welcome the families | universalism-concern + benevolence-caring | W/G | map G, W | =map (W)
- support it in private and stay quiet in public | universalism-concern + conformity-interpersonal | U/W | map W, G | partial: hidden support reads U
- ask for smaller numbers and a slower timetable | security-societal + universalism-concern | W/U | map W, G | =map

#### 4.2.25 Keep the old language at home, or let the children fit in
Clash: tradition + benevolence-caring vs achievement + conformity-rules (to the new country's ways)  
Circle: conservation against self-enhancement; Berry's acculturation strategies  
Stages: adult  
Domains: family, home, community  
Situation: Your family has migrated, the children answer you in the new language now, and their grandmother cannot follow.

- speak only the old language at home and send them to heritage school (separation) | tradition | G/W | map G, W | =map
- speak only the new language so they get ahead (assimilation) | achievement + conformity-rules | U/B | map U, W | =map
- keep both: the old at home, the new outside (integration) | tradition + achievement | G/U | map W | !map: a bicultural home reads G and U; the blend scores White
- let the children choose and follow their lead | universalism-tolerance + self-direction-action | G/R | map B, R | partial: letting the young grow their own way reads G
- [inner] grieve that your grandchildren will not know your songs | tradition | G | map G, W | =map

#### 4.2.26 Start your own business with the house as collateral
Clash: self-direction-action + achievement + stimulation vs security-personal (the family home)  
Circle: openness and self-enhancement against conservation  
Stages: adult, mature  
Domains: work, money, home  
Situation: The bank will lend you enough to open the workshop, if you put the house up as security.

- sign the loan and go for it | self-direction-action + stimulation + achievement | B/R | map B, R | =map
- keep the salary and drop the idea | security-personal | U/W | map W, U | =map (U)
- start small at nights while keeping the job | self-direction-action + security-personal | U/B | map B, U | =map (U)
- find a partner to carry half the risk | achievement + security-personal | U/B | map U, B | =map
- ask your spouse to make the call with you | benevolence-dependability + conformity-interpersonal | W | map W, U | =map

#### 4.2.27 Give up the drink or the cigarettes you love, on the doctor's order
Clash: hedonism vs security-personal (health) + benevolence-caring (the family wants you around)  
Circle: openness against conservation and self-transcendence  
Stages: adult, mature, elder  
Domains: body  
Situation: The scan is clear for now, and the doctor says the habit you have enjoyed for thirty years must stop.

- quit on the spot | security-personal | U/W | map W, U | =map (U)
- carry on and enjoy the time you have | hedonism | R/G | map R, B | =map
- cut down to weekends only | hedonism + security-personal | U/R | map R, B | partial: rationed pleasure reads U
- quit for your grandchildren's sake | benevolence-caring + security-personal | W/G | map W, U | =map
- [inner] promise to quit next month, every month | hedonism | R/B | map R, B | =map

#### 4.2.28 Your grown son admits he stole from his employer
Clash: benevolence-caring vs conformity-rules + universalism-concern  
Circle: neighbours in the social-focus half, as in 4.2.13, but now with your own child (closeness lowers reporting, Waytz et al. 2013)  
Stages: adult, mature  
Domains: family, conflict  
Situation: He tells you at the kitchen table, shaking, and the audit starts on Monday.

- urge him to confess and stand by him through it | benevolence-dependability + conformity-rules | W | map W, U | =map
- [wrong] help him hide the money | benevolence-caring | G/B | map W, G | partial: loyalty over law reads G and B, not the White half of benevolence
- pay it back yourself, quietly, before anyone notices | benevolence-caring + security-personal | B/G | map W, U | !map: buying the problem away reads B; kin-first reads G
- report him yourself | conformity-rules + universalism-concern | W | map W, G | =map
- [inner] stop speaking to him for a year | conformity-rules + face | W/B | map W, U | =map

#### 4.2.29 Retire early to chase the dream, or keep earning
Clash: stimulation + hedonism vs security-personal + benevolence-dependability (the family still counts on your income)  
Circle: openness against conservation  
Stages: mature  
Domains: work, money, aging  
Situation: At fifty-five you could take the reduced pension and sail, but the youngest is still at university.

- retire now and buy the boat | stimulation + hedonism | R | map R, B | =map
- keep working until the full pension | security-personal + benevolence-dependability | W/U | map W, U | =map
- go part-time and start the dream slowly | security-personal + stimulation | U/R | map R, B | partial: a phased plan reads U
- keep working and take one long voyage a year | security-personal + hedonism | U/R | map R, B | partial: a phased plan reads U
- [inner] decide the dream was only a daydream after all | humility | G/W | map G, W | =map

#### 4.2.30 Fund your grown child's house deposit from your retirement savings
Clash: benevolence-caring vs security-personal  
Circle: self-transcendence against conservation, neighbours  
Stages: mature  
Domains: money, family  
Situation: Your son and his wife cannot buy without help, and the sum is a third of what you have saved for old age.

- give them the money | benevolence-caring | G/W | map W, G | =map (G)
- refuse, gently, and explain why | security-personal | U/W | map W, U | =map (U)
- lend it with a written repayment plan | benevolence-caring + conformity-rules | W/U | map W, U | =map
- give it as an advance on the inheritance, the same for each child | benevolence-caring + universalism-concern | W | map G, W | =map (W)
- give it on condition they buy near you | benevolence-caring + security-personal | B/G | map W, U | !map: a gift with strings reads B

#### 4.2.31 Mind the grandchildren every day, or keep your new freedom
Clash: benevolence-caring + tradition vs self-direction-action + hedonism  
Circle: self-transcendence and conservation against openness  
Stages: mature, elder  
Domains: family, leisure, aging  
Situation: You retired in spring with plans to paint and travel, and your daughter asks you to take the baby every weekday.

- take the baby every weekday | benevolence-caring + tradition | G/W | map G, W | =map
- say no and keep your painting class and trips | self-direction-action + hedonism | R/B | map B, R | =map (R)
- take the baby two days a week and hold to it | benevolence-caring + self-direction-action | W/G | map B | !map: a firm, fair limit reads W
- pay for a childminder instead | benevolence-caring + power-resources | B/G | map U, B | =map (B)
- take the grandchild along on your trips | benevolence-caring + stimulation | G/R | map R, G | =map (G)

#### 4.2.32 An old friend on the board asks for your vote on a dubious deal
Clash: benevolence-dependability (loyalty) vs universalism-concern + conformity-rules  
Circle: neighbours in the social-focus half; fairness against loyalty again, at the top of an organisation  
Stages: mature  
Domains: work, community, friends  
Situation: The housing association board votes tomorrow on a land deal that would profit your oldest friend's brother.

- vote with your friend | benevolence-dependability | G/B | map W, G | partial: loyalty to a friend over the rules reads G and B
- vote against and tell him why to his face | universalism-concern + conformity-rules | W | map W, G | =map
- abstain | conformity-interpersonal | W/U | map W, U | =map
- ask for an independent valuation before any vote | conformity-rules + self-direction-thought | U/W | map U, B | =map
- [wrong] vote for it in exchange for his support on your own project | power-resources + power-dominance | B | map B, R | =map

#### 4.2.33 Take over the family farm, or sell it
Clash: tradition + benevolence-caring vs power-resources + achievement  
Circle: conservation and self-transcendence against self-enhancement  
Stages: adult, mature  
Domains: work, home, family  
Situation: Your father has died, the farm has been in the family for four generations, and a developer has made an offer.

- take it over and live on its thin margins | tradition + benevolence-caring | G | map G, W | =map
- sell to the developer and invest the money | power-resources + achievement | B | map B, U | =map
- keep the land and lease it to a young farmer | tradition + power-resources | G/U | map G, W | =map
- sell to the nature trust for less | universalism-nature + tradition | G/W | map G, W | =map
- turn it into a farm-stay business | tradition + achievement | G/B | map W | !map: heritage turned to profit reads G and B; the blend scores White

#### 4.2.34 Give up the car keys
Clash: self-direction-action vs security-personal + universalism-concern (other people's safety)  
Circle: openness against conservation  
Stages: elder  
Domains: aging, body  
Situation: You scraped two cars in the supermarket car park this month, and your son has asked you to stop driving.

- keep driving and wave the worry away | self-direction-action | R/B | map B, R | =map (R)
- hand over the keys the day the doctor advises it | security-personal + universalism-concern | W | map W, G | =map
- drive only by day and only near home | self-direction-action + security-personal | U/W | map B, U | =map (U)
- sell the car and learn the bus routes | self-direction-thought + security-personal | U/G | map B, U | =map (U)
- let your daughter hide the keys and pretend not to notice | face + conformity-interpersonal | G/W | map W, U | partial: graceful letting-go reads G

#### 4.2.35 Move into the care home, or stay in your own house
Clash: self-direction-action + tradition (your home, your place) vs security-personal + benevolence-caring (not being a burden)  
Circle: openness and conservation pull in different ways here: home is both freedom and tradition  
Stages: elder  
Domains: home, aging, family  
Situation: After the second fall, the family and the nurse agree you cannot keep managing the stairs alone.

- stay in your house with a call button and daily visits | self-direction-action + security-personal | G/B | map B, U | partial: your own ground reads G
- move into the care home before anyone has to insist | security-personal + benevolence-caring | U/W | map W, U | =map (U)
- move in with your daughter's family | benevolence-caring + tradition | G/W | map G, W | =map
- sell the house and move to a flat near the shops | security-personal + self-direction-action | U/B | map B, U | =map (U)
- refuse all help and dare them to move you | self-direction-action + face | R/B | map B, U | partial: defiance reads R

#### 4.2.36 Tell the family an old secret before you die, or keep the peace
Clash: benevolence-dependability (honesty) vs conformity-interpersonal + face (family harmony, your good name)  
Circle: self-transcendence against conservation and face  
Stages: elder  
Domains: family, loss  
Situation: Your eldest does not know that the man who raised him was not his father, and you are the last one who knows.

- tell him yourself, face to face | benevolence-dependability + self-direction-action | W/R | map B | !map: confession reads W; the blend scores Black
- tell only him and ask him to keep it | benevolence-dependability + conformity-interpersonal | W/U | map W, U | =map
- write it in a letter to be opened after the funeral | face + benevolence-dependability | U/W | map W, U | =map (U)
- take the secret with you | face + security-personal | B/U | map U, W | partial: secrecy to protect your own name reads B
- confess it to your priest instead | tradition + humility | W/G | map G, W | =map (W)

#### 4.2.37 Divide the inheritance equally, or reward the child who cared for you
Clash: universalism-concern (equal shares) vs benevolence-caring + security-personal (favours returned)  
Circle: within self-transcendence, plus reciprocity from security  
Stages: elder  
Domains: money, family, loss  
Situation: One daughter nursed you for six years; the other two visited at Christmas.

- split everything equally | universalism-concern + tradition | W | map G, W | =map (W)
- leave more to the daughter who cared for you | benevolence-caring + security-personal | W/G | map W, U | =map
- leave her the house and split the rest equally | universalism-concern + benevolence-caring | W | map G, W | =map (W)
- give gifts now while you can see the joy they bring | hedonism + benevolence-caring | G/R | map R, G | =map (G)
- leave it all to charity and let them sort out the rest | universalism-concern | W | map G | !map F3: impartial giving reads W

#### 4.2.38 Hard treatment for more time, or comfort for the time left
Clash: security-personal (staying alive) + benevolence-caring (the family wants more time) vs humility (accepting the end) + hedonism  
Circle: conservation against openness, with humility at the border of self-transcendence  
Stages: elder  
Domains: body, loss  
Situation: The specialist offers another round of treatment that may buy a year, with hard side effects.

- take every treatment on offer | security-personal + benevolence-caring | U/W | map W, U | =map (U)
- stop treatment and go home | humility + self-direction-action | G | map R, G | =map (G)
- try one round and decide after | security-personal + self-direction-thought | U | map B, U | =map (U)
- let your children decide | benevolence-caring + conformity-interpersonal | W | map W, U | =map
- spend the time and money on one last journey | hedonism + stimulation | R/G | map R, B | =map

#### 4.2.39 Remarry after the death of a spouse
Clash: hedonism + self-direction-action (a new love, your own life) vs tradition + conformity-interpersonal (the children's feelings, loyalty to the dead)  
Circle: openness against conservation  
Stages: elder  
Domains: love, family, loss  
Situation: Two years after your wife's death you want to marry a woman from the choir, and your children are upset.

- marry her and tell the children afterwards | self-direction-action + hedonism | R | map B, R | =map (R)
- stay companions but never marry | conformity-interpersonal + benevolence-caring | W/G | map W, U | =map
- wait until a full year of mourning has passed | tradition + conformity-interpersonal | W/G | map W, G | =map
- give her up to keep the peace with the children | conformity-interpersonal + tradition | W | map W, G | =map
- [inner] keep your late wife's photo up and carry both loves | benevolence-caring + tradition | G/W | map G, W | =map

#### 4.2.40 Keep the money you found, or hand it in
Clash: hedonism + power-resources vs conformity-rules + benevolence-caring (for the owner)  
Circle: openness and self-enhancement against conservation and self-transcendence  
Stages: child, juv  
Domains: money, community  
Situation: On the way home from school you find a purse with more money in it than you get in a year, and nobody saw.

- hand it in at the school office | conformity-rules | W | map W, U | =map
- keep it and buy the game you wanted | hedonism + power-resources | R/B | map R, B | =map
- take the money and post the empty purse back to the address inside | power-resources + benevolence-caring | B/W | map U, B | =map (B)
- give it to your mother and let her decide | conformity-rules | W | map W, U | =map
- keep a little as a finder's fee and hand in the rest | hedonism + conformity-rules | B/W | map W, U | partial: a self-awarded fee reads B

#### 4.2.41 Watch the film your parents forbade, at the sleepover
Clash: stimulation + conformity-interpersonal (go along with your friends) vs conformity-rules (your parents' rule) + benevolence-dependability (your word)  
Circle: openness against conservation, with conformity on both sides (peers against parents)  
Stages: child  
Domains: friends, family, leisure  
Situation: Everyone at the sleepover is about to watch the horror film your parents said you are too young for.

- watch it with everyone | stimulation + conformity-interpersonal | R | map W, G | !map: a thrill shared with the group reads R; the summed loadings nearly cancel
- go, and sit in the kitchen during the film | conformity-rules + benevolence-dependability | W | map W, U | =map
- call your parents and ask if you may, just this once | conformity-rules | W/U | map W, U | =map
- say you feel ill and go home | security-personal | U/B | map W, U | =map (U)
- watch it, then tell your parents yourself the next day | stimulation + benevolence-dependability | R/W | map R, G | =map


### 4.3 Count and pattern of flags in section 4

41 dilemmas, 205 responses (8 marked `[wrong]`, 15 `[inner]`). Stages (a dilemma can cover several): child 6,
juvenile 10, young adult 12, adult 17, mature 12, elder 10. Domains most used: family, work, money; every domain in
the file's list appears at least twice. Flags: `=map` 160 (78%), `partial` 24, `!map` 21. Agreement is higher than in section 3
because most responses serve benevolence, security, conformity or tradition, where the map and my readings agree.

Patterns in the disagreements:
1. **Compromises lose their color when loadings are summed.** A compromise serves two opposite values, and summing
   their loadings cancels most of both. Benevolence plus self-direction scores plain Black; tradition plus achievement
   scores White; benevolence plus achievement scores Blue and Black; stimulation plus conformity nearly cancels to
   nothing. My readings of the same compromises color them by their means: a firm, fair rota reads White; a phased or
   hedged plan reads Blue; an improvised mix reads Red or Green; a bicultural home reads Green and Blue. Suggestion: the
   engine colors a compromise response by the way it is carried out (rule, plan, improvisation, custom) rather than
   only by the sum of the two ends.
2. **Self-protection at someone else's cost.** Security-personal acts that keep you safe while another person pays
   (stay out of the fight, keep quiet about the safety problem) read Black, while the map gives security White and
   Blue. Suggestion: security bought at another's expense counts as Black.
3. **Loyalty over rules.** Benevolence acts that defy a rule to protect your own (hide the money, vote with the
   friend) read Green and Black, not White; the same pattern section 3 found for lying to the police (F9 caveat).
4. **Justice (F3) again.** Hospitality, equal shares and impartial giving read White; the map leads universalism
   with Green.
5. **Hedged and delayed choices read Blue (F2).** Gap years, phased retirements, trial rounds of treatment and
   "decide later" all read Blue whatever value they serve: deliberation is a style, not a value.
6. **Home ground and kin read Green.** Staying with family on home ground, refusing to leave your own house and
   warning your own people first read Green; the map gives security G -0.5.
7. **Face alone scores Blue.** As section 1.3 predicted, a face-saving story or a secret kept for your good name reads
   Black, while face (power plus security) scores Blue. Suggest W/B for face, as in section 1.3.

Engine notes drawn from 4.1:
- Raise a dilemma only when both values are high for the person and the event touches both (Schwartz 2012).
- Gap between the two value weights sets the style: a large gap gives a quick choice plus an excusing story (the
  `[inner]` "tell yourself" responses); a small gap gives deliberation, compromise or delay (Tetlock 1986).
- Each dilemma has a choose-A, choose-B, compromise, evade (delay, hand-off, narrow truth) and reframe or wrong
  option, so the response set itself spans the five colors more often than not.
- Taboo framings (money against a parent, a child or a faith) should add onlooker outrage and a later chance of a
  cleansing act; tragic framings (a child against a sibling) should add lasting distress but less blame (Tetlock 2003).
- Repeatedly choosing against a strong value adds stress over time (Burroughs and Rindfleisch 2002); an unanswered
  calling keeps generating crafting acts and regret (Berg et al. 2010).

## 5. Inner drivers: states that build up and push a person to act

Note on cross-references: section 1.3 points to "section 6.1" (Reiss's basic desires) and "section 6.2"
(Self-Determination Theory). That material is here, in section 5.1 and 5.2; section 6 covers value change.

Sources (read online for this file unless marked "not re-read"):
- Reiss, S. (2004). Multifaceted nature of intrinsic motivation: the theory of 16 basic desires. Review of General
  Psychology, 8(3), 179-193. Desire list and intrinsic feelings read via
  https://mindfulnessmuse.com/individual-differences/16-universal-desires-and-what-drives-your-behavior-part-one and
  https://mindfulnessmuse.com/individual-differences/16-universal-desires-what-drives-your-behavior-part-two
- Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social
  development, and well-being. American Psychologist, 55(1), 68-78 (not re-read); Vansteenkiste, M., & Ryan, R. M.
  (2013). On psychological growth and vulnerability: basic psychological need satisfaction and need frustration as a
  unifying principle. Journal of Psychotherapy Integration, 23(3), 263-280 (not re-read).
- Kasser, T., & Ryan, R. M. (1993, 1996), Aspiration Index: wealth, fame, image (extrinsic); relationships, personal
  growth, community contribution (intrinsic); health (neither). https://selfdeterminationtheory.org/aspirations-index
- Cowen, A. S., & Keltner, D. (2017). Self-report captures 27 distinct categories of emotion bridged by continuous
  gradients. PNAS, 114(38), E7900-E7909. https://pmc.ncbi.nlm.nih.gov/articles/PMC5617253/
- Fredrickson, B. L. (2001). The role of positive emotions in positive psychology: the broaden-and-build theory.
  American Psychologist, 56(3), 218-226 (not re-read).
- Loneliness: Luhmann, M., & Hawkley, L. C. (2016). Age differences in loneliness from late adolescence to oldest old
  age. Developmental Psychology, 52(6), 943-959. https://www.diw.de/de/diw_01.c.775340.de/s_9560.html ; Cacioppo's
  evolutionary theory of loneliness as summarised in https://knowledge.uchicago.edu/record/6403/files/journal.pone.0203491.pdf
- Boredom: Westgate, E. C., & Wilson, T. D. (2018). Boring thoughts and bored minds: the MAC model of boredom and
  cognitive engagement. Psychological Review, 125(5), 689-713; Westgate (2020) chapter read via
  https://eclass-b.uoa.gr/modules/document/file.php/PPP387/boredom.pdf ; Wilson, T. D., et al. (2014). Just think:
  the challenges of the disengaged mind. Science, 345, 75-77.
- Envy: van de Ven, N., Zeelenberg, M., & Pieters, R. (2009). Leveling up and down: the experiences of benign and
  malicious envy. Emotion, 9(3), 419-429. https://repository.tilburguniversity.edu/items/2a96534b-4cec-4018-811b-ef111b0444cd ;
  Henniger, N. E., & Harris, C. R. (2015). Envy across adulthood: the what and the who. Basic and Applied Social
  Psychology, 37(6), 303-318. https://www.sciencedaily.com/releases/2015/11/151104124648.htm
- Nostalgia: Zhou, X., Sedikides, C., Wildschut, T., & Gao, D.-G. (2008). Counteracting loneliness: on the restorative
  function of nostalgia. Psychological Science, 19(10), 1023-1029.
  https://www.psychologicalscience.org/news/releases/those-were-the-days-counteracting-loneliness-with-nostalgia.html ;
  Routledge, C., et al. (2011). The past makes the present meaningful. JPSP, 101(3), 638-652 (not re-read).
- Awe: Keltner, D., & Haidt, J. (2003). Approaching awe. Cognition and Emotion, 17(2), 297-314 (not re-read); Piff,
  P. K., Dietze, P., Feinberg, M., Stancato, D. M., & Keltner, D. (2015). Awe, the small self, and prosocial behavior.
  JPSP, 108(6), 883-899. https://news.uci.edu/faculty/awe-promotes-altruistic-behavior-uci-led-study-finds
- Midlife and round birthdays: Wethington, E. (2000). Expecting stress: Americans and the "midlife crisis".
  Motivation and Emotion, 24(2), 85-103. https://news.cornell.edu/node/279696 ; Alter, A. L., & Hershfield, H. E.
  (2014). People search for meaning when they approach a new decade in chronological age. PNAS, 111(48),
  17066-17070. https://bps.org.uk/research-digest/why-youre-particularly-likely-run-your-first-marathon-when-your-age-ends-9
- Fresh starts: Dai, H., Milkman, K. L., & Riis, J. (2014). The fresh start effect: temporal landmarks motivate
  aspirational behavior. Management Science, 60(10), 2563-2582.
  https://anderson-review.ucla.edu/wp-content/uploads/2021/03/Dai-Milkman-Riis_FreshStartEffect_2014_Mgmt_Sci.pdf
- Terror management: Burke, B. L., Martens, A., & Faucher, E. H. (2010). Two decades of terror management theory: a
  meta-analysis. PSPR, 14(2), 155-195 (not re-read); 2025 meta-analytic review of mortality salience studies, JPSP
  129(1), doi:10.1037/pspa0000438, summary read via https://ifp.nyu.edu/2025/meta-analyses-systematic-reviews/pspa0000438/
- Regret: Gilovich, T., & Medvec, V. H. (1995). The experience of regret. Psychological Review, 102(2), 379-395;
  Gilovich, Medvec & Kahneman (1998). Varieties of regret. Psychological Review, 105(3), 602-605.
  https://www.kellogg.northwestern.edu/academics-research/research/detail/1998/varieties-of-regret-a-debate-and-partial-resolution/
- Homesickness: Stroebe, M., Schut, H., & Nauta, M. H. (2015). Homesickness: a systematic review of the scientific
  literature. Review of General Psychology, 19(2), 157-171. https://mindwise-groningen.nl/working-on-the-homesick-blues/
- Burnout: Maslach, C., & Leiter, M. P. (2016). Understanding the burnout experience. World Psychiatry, 15(2), 103-111
  (full text not reachable; content from memory of the paper).
- Desire and self-control: Hofmann, W., Vohs, K. D., & Baumeister, R. F. (2012). What people desire, feel conflicted
  about, and try to resist in everyday life. Psychological Science, 23(6), 582-588.
  https://experts.umn.edu/en/publications/what-people-desire-feel-conflicted-about-and-try-to-resist-in-eve/
- Longing for a child: Brase, G. L., & Brase, S. L. (2012). Emotional regulation of fertility decision making: what is
  the nature and structure of "baby fever"? Emotion, 12(5), 1141-1154. https://www.goodtherapy.org/blog/baby-fever-causes-factors-1102123
- Life longings: Scheibe, S., Freund, A. M., & Baltes, P. B. (2007). Toward a developmental psychology of Sehnsucht
  (life longings). Developmental Psychology, 43(3), 778-795. https://refubium.fu-berlin.de/handle/fub188/12017
- Time horizons: Carstensen, L. L. (2006). The influence of a sense of time on human development. Science, 312,
  1913-1915 (not re-read); overview https://en.wikipedia.org/wiki/Socioemotional_selectivity_theory
- Meaning: Steger, M. F., Oishi, S., & Kashdan, T. B. (2009). Meaning in life across the life span. Journal of
  Positive Psychology, 4(1), 43-52. https://instituteofcoaching.org/resources/meaning-life-across-life-span-levels-and-correlates-meaning-life-emerging-adulthood-older
- Usefulness in old age: Gruenewald, T. L., Karlamangla, A. S., Greendale, G. A., Singer, B. H., & Seeman, T. E.
  (2007). Feelings of usefulness to others, disability, and mortality in older adults. Journals of Gerontology B,
  62(1), P28-P37. https://ccpr.ucla.edu/wp-content/uploads/2024/04/Feelings-of-Usefulness-to-Others_-Disability_-and-Mortality-in-Older-Adults_-The-MacArthur-Study-of-Successful-Aging.pdf
- Grief: Stroebe, M., & Schut, H. (1999). The dual process model of coping with bereavement. Death Studies, 23(3),
  197-224; Bonanno, G. A. (2004). Loss, trauma, and human resilience. American Psychologist, 59(1), 20-28; Lundorff,
  M., et al. (2017). Prevalence of prolonged grief disorder in adult bereavement. Journal of Affective Disorders, 212,
  138-149 (all not re-read; PubMed blocked).
- Other emotion and motive sources, not re-read for this file: Tangney, Stuewig & Mashek (2007), Moral emotions and
  moral behavior, Annual Review of Psychology 58, 345-372 (shame and guilt); Tracy & Robins (2007), JPSP 92(3),
  506-525 (authentic and hubristic pride); Williams & DeSteno (2008), JPSP 94(6), 1007-1017 (pride and perseverance);
  Carver & Harmon-Jones (2009), Psychological Bulletin 135(2), 183-204 (anger as approach); Brehm (1966), A theory of
  psychological reactance; Williams (2009), Ostracism: a temporal need-threat model, Advances in Experimental Social
  Psychology 41, 275-314; Algoe (2012), Find, remind, and bind: the functions of gratitude, Social and Personality
  Psychology Compass 6(6), 455-469; Algoe & Haidt (2009), Journal of Positive Psychology 4(2), 105-127 (elevation,
  gratitude, admiration); Thrash & Elliot (2003), JPSP 84(4), 871-889 (inspiration); Snyder (2002), Psychological
  Inquiry 13(4), 249-275 (hope); Loewenstein (1994), Psychological Bulletin 116(1), 75-98 (curiosity as an
  information gap); Anderson, Hildreth & Howland (2015), Psychological Bulletin 141(3), 574-601 (desire for status);
  Kilduff, Elfenbein & Staw (2010), Academy of Management Journal 53(5), 943-969 (rivalry); McAdams & de St. Aubin
  (1992), JPSP 62(6), 1003-1015 (generativity); Gilbert & Allan (1998), Psychological Medicine 28(3), 585-598
  (entrapment); Steinberg et al. (2008), Developmental Psychology 44(6), 1764-1778 (sensation seeking by age);
  Neugarten, Moore & Lowe (1965), American Journal of Sociology 70(6), 710-717 (the social clock); Gable et al.
  (2004), JPSP 87(2), 228-245 (sharing good news); Dunn, Aknin & Norton (2008), Science 319, 1687-1688 (spending on
  others); Goetz, Keltner & Simon-Thomas (2010), Psychological Bulletin 136(3), 351-374 (compassion); Nguyen, Ryan &
  Deci (2018), PSPB 44(1), 92-106 (solitude); Przybylski et al. (2013), Computers in Human Behavior 29(4), 1841-1848
  (fear of missing out); Feeney (2004), JPSP 87(5), 631-648 (a secure base and exploration); Csikszentmihalyi (1990),
  Flow; Festinger (1957), A theory of cognitive dissonance; Smith, Pettigrew, Pippin & Bialosiewicz (2012), PSPR 16(3),
  203-232 (relative deprivation).

### 5.1 Reiss's sixteen desires, with the nearest Schwartz values and a color reading

Reiss (2004) treats each desire as a separate end that people want for its own sake, each with its own intrinsic
feeling. People differ in how strongly they hold each desire, and a satisfied desire stops pushing for a while. For
Chroma, each desire is a candidate rate at which a matching inner driver builds up.

| desire | wants | intrinsic feeling | nearest Schwartz value(s) | my color reading |
|---|---|---|---|---|
| acceptance | approval, inclusion | self-confidence | face, conformity-interpersonal | W |
| curiosity | knowledge | wonder | self-direction-thought | U (F1) |
| eating | food | satiation | hedonism | G/R (F7) |
| family | to raise children | parental love | benevolence-caring | G/W |
| honor | to live by a moral code, loyalty to heritage | loyalty | tradition, conformity-rules | W |
| idealism | social justice, altruism | compassion | universalism-concern | W (F3) |
| independence | self-reliance | freedom | self-direction-action | R/B (F10) |
| order | organisation, routine, cleanliness | stability | security-personal, conformity-rules | W/U |
| physical activity | exercise, strength | vitality | stimulation, achievement (body) | R/G (F8) |
| power | influence, leadership | efficacy | power-dominance, achievement | B (W for office, F5) |
| romance | beauty, courtship, sex | desire | hedonism, stimulation | R |
| saving | to collect, to keep | ownership | security-personal, power-resources | U/B |
| social contact | companionship, play | fun | benevolence-caring, stimulation | R/G |
| status | standing, attention | self-importance | power, face | B/W |
| tranquility | freedom from fear and pain | safety, relaxation | security-personal | W/G |
| vengeance | to get even, to compete | vindication | power-dominance | R/B |

Four desires have no clear home in the ten values: curiosity (split off as self-direction-thought, F1), eating and
physical activity (bodily appetites the values model does not treat as values), and vengeance (closest to
power-dominance, but it is about answering a wrong, not about ruling).

### 5.2 How inner drivers work, as rules a simulator can use

- **A driver is a stock.** It fills while its triggers hold, drains with time, and drains fast when an act answers it
  (a lonely person who joins a choir). When it passes a threshold, the person acts; the person's value profile picks
  which of the typical responses they take. The same driver gives different acts in different people: that is where
  the colors come from.
- **Three basic needs (Self-Determination Theory).** Autonomy (acting from your own choice), competence (being
  effective) and relatedness (being close to others). When they are satisfied, people grow, explore and act from
  interest; when they are actively frustrated (controlled, belittled, rejected), people shift toward defensive and
  compensatory acts: rigid habits, chasing approval, money and image as stand-ins (Ryan and Deci 2000; Vansteenkiste
  and Ryan 2013). Engine: under need frustration, tilt the response choice toward extrinsic responses (wealth, fame,
  image: mostly Black); under need satisfaction, toward intrinsic ones (relationships, growth, community: Green,
  White, Blue).
- **Intrinsic and extrinsic goals.** Putting wealth, fame and image above relationships, growth and community goes with
  poorer well-being (Kasser and Ryan 1993, 1996). Engine: a person whose drivers are answered by extrinsic responses
  should drain the driver more slowly (the need under the driver is not really met).
- **Pleasant states open, painful states narrow.** Positive emotions widen the range of acts a person considers and
  build lasting resources (friends, skills, health); negative emotions narrow toward one action tendency (attack,
  flee, hide, repair) (Fredrickson 2001). Engine: pleasant drivers should offer exploratory and social responses with
  more variety; painful drivers have tighter response sets.
- **States blend.** Cowen and Keltner (2017) found 27 kinds of reported emotional experience (admiration, adoration,
  aesthetic appreciation, amusement, anger, anxiety, awe, awkwardness, boredom, calmness, confusion, craving, disgust,
  empathic pain, entrancement, excitement, fear, horror, interest, joy, nostalgia, relief, romance, sadness,
  satisfaction, sexual desire, surprise), joined by smooth gradients rather than sharp borders. Envy, guilt, pride,
  contempt, disappointment, sympathy and triumph were among the 34 tested but did not stand out as separate
  categories in their video ratings. Engine: allow two drivers at once (loneliness with nostalgia, grief with
  gratitude), and let neighbouring states pass into each other.
- **Landmarks lower the threshold for change.** Aspirational acts spike after temporal landmarks: in Dai, Milkman and
  Riis (2014), gym visits rose about 33% at the start of a week, 12% at the start of a year and 47% at the start of a
  semester; commitment contracts rose about 145% at the start of a year; Google searches for "diet" rose about 82% at
  the year's start. People whose age ends in 9 search more for meaning and make more big changes (Alter and Hershfield
  2014). Engine: on a new year, birthday, move, new job or a round-number age, drivers of change cross their threshold
  more easily, and responses tilt toward resolutions.
- **Age shifts the drivers.** As the future feels shorter, people favour emotionally meaningful goals over gathering
  knowledge and contacts, prune their networks to close ties, and attend more to the positive (socioemotional
  selectivity, Carstensen 2006). Loneliness is highest in young adults and the oldest old (Luhmann and Hawkley 2016).
  Envy falls with age (about 80% of under-30s versus 69% of over-50s report it in the past year; Henniger and Harris
  2015). Search for meaning is higher early in life, presence of meaning higher later (Steger et al. 2009). Sensation
  seeking peaks in the late teens (Steinberg et al. 2008).
- **Trigger vocabulary.** The triggers below use a small set of checkable conditions:
  - need levels the engine can track: belonging, autonomy, competence, security, stimulation, meaning, status, rest,
    intimacy (each low, middling or high, and for how long);
  - recent events with a window: a loss, move, birth, breakup, wedding, promotion, job loss, illness or diagnosis,
    retirement, a child leaving home, an insult, a rejection, praise, a win ("within the month", "within the year");
  - comparisons: a peer's success or milestone (same sex, within about five years of age, in a domain the person
    cares about);
  - the calendar: a round birthday, an age ending in 9, an anniversary of a loss, New Year, the start of a season;
  - surroundings: cues tied to a habit, confinement, crowding, nature, a place from childhood.

### 5.3 Painful and draining drivers

Format for every driver below: kind and links (Reiss desire, SDT need, Cowen and Keltner category where one fits),
triggers as conditions, what makes it likelier or rarer, the stages where it is common, a research note, then five
typical responses: `response` | value(s) | colors (my reading) | map note against the engine's map (same method as
section 4: loadings summed for two values; `!map` notes give the reason).

#### 5.3.1 Loneliness
Kind and links: painful, slow-building. Reiss: social contact. SDT: relatedness frustrated. Cowen and Keltner:
sadness.  
Triggers: belonging low for 3+ weeks; or a move to a new town within 6 months; or a partner died or left within the
year; or living alone and seeing a friend less than weekly; or the last close friend moved away.  
Likelier / rarer: likelier in young adults and the oldest old, with low income, poor health or limited mobility,
single, living alone; rarer with a confidant, daily contact with kin, a pet, a club or congregation, a happy
partnership.  
Stages: juv, ya (peak), elder (peak in the oldest old); any stage after a move or a loss.  
Research: Loneliness is high in young adulthood and among the oldest old, and at every age is predicted by few
friends, little contact and low social engagement (Luhmann and Hawkley 2016, n = 16,132). In Cacioppo's evolutionary
account it works like hunger, pushing toward reconnection, but it also raises vigilance for social threat, so a lonely
person can both seek others and pull away. Loneliness also triggers nostalgia, which raises felt social support (Zhou
et al. 2008).

- join the choir that meets in the church hall | tradition + benevolence-caring | G/W | =map
- call an old friend you have not spoken to in years | benevolence-caring | G/W | =map (G)
- get a dog | benevolence-caring + hedonism | G | =map (G)
- sign up for a dating app | stimulation + hedonism | R | =map
- [inner] decide people are not worth the trouble and stop trying | security-personal | B/U | partial: withdrawal for self-protection reads B

#### 5.3.2 Boredom
Kind and links: painful, fast or chronic. Reiss: curiosity and physical activity unmet. SDT: autonomy and competence
low. Cowen and Keltner: boredom.  
Triggers: the same routine for 1+ year with no new task; or stimulation low for 2+ weeks; or a task far below or far
above skill; or a task that serves no goal the person holds now; or confinement (illness, a long wait, house arrest of
any kind).  
Likelier / rarer: likelier in adolescents and young adults, high sensation seekers, people with little control over
their day, after retirement without plans; rarer with absorbing hobbies, autonomy at work, a goal the routine clearly
serves.  
Stages: juv, ya (peak), adult in routine jobs, elder in care settings.  
Research: In the MAC model (Westgate and Wilson 2018; Westgate 2020), boredom follows when attention fails (the task
is too easy or too hard) or when meaning fails (the task is not tied to an active goal); either is enough. People
respond by changing the task's difficulty, building resources (sleep, coffee, skill), re-finding the task's meaning,
or switching to something new or something pleasant. In Wilson et al. (2014), 12 of 18 men and 6 of 24 women gave
themselves an electric shock rather than sit 15 minutes alone with their thoughts.

- take up a risky new hobby such as climbing | stimulation | R | =map
- ask the boss for harder work or a new project | achievement + self-direction-thought | U/B | =map (U)
- start an evening class in something you know nothing about | self-direction-thought | U | !map F1
- remind yourself the dull job pays for the house you want | security-personal + achievement | U/W | =map
- [wrong] shoplift for the thrill of it | stimulation + hedonism | R/B | =map

#### 5.3.3 Envy
Kind and links: painful, fast. Reiss: status, acceptance. SDT: competence threatened by comparison. Cowen and Keltner:
tested, but merged with other categories.  
Triggers: a peer's success in a domain the person cares about (same sex, within about five years of age); or a
sibling's or friend's promotion, wedding, baby or new house; or weeks of social media full of peers' highlights; or
being passed over in favour of someone similar.  
Likelier / rarer: likelier when the domain is central to identity, the rival is similar, and the person's own standing
is low or falling; benign (move-up) envy when the gap feels deserved and closeable, malicious (pull-down) envy when it
feels undeserved; rarer with age and with gratitude.  
Stages: juv, ya (peak: romance, looks, school, social success), adult and mature (money, work).  
Research: Benign envy pushes people to improve their own position; malicious envy pushes them to damage the other's
(van de Ven et al. 2009, in three countries). About 80% of under-30s and 69% of over-50s reported envy in the past
year; young adults envied romance (about 40%), looks, school and social success, older adults money and work; people
envied others of their own sex and about their own age (Henniger and Harris 2015).

- train harder to catch up | achievement | B/U | =map
- ask the rival how they did it | self-direction-thought + achievement | U/W | =map (U)
- [wrong] spread a rumour about the rival | power-dominance + face | B | =map
- [inner] tell yourself their success is shallow | face | B | !map: a sour-grapes story reads B; face alone scores Blue
- count your own blessings and stop scrolling | humility | G/W | =map

#### 5.3.4 Guilt
Kind and links: painful. Reiss: honor, idealism. SDT: relatedness. Cowen and Keltner: tested, but merged with other
categories.  
Triggers: the person broke a promise or hurt someone close within the week; or acted against a value they rank high
(benevolence, conformity, tradition); or prospered where others suffered (a layoff survivor, a migrant whose family
stayed behind); or missed a parent's last days.  
Likelier / rarer: likelier with high benevolence, conformity or tradition, a conscientious temperament, a known
victim; rarer when the harm is diffuse, others share the blame, or empathy is low.  
Stages: all, from about age 3-4.  
Research: Guilt centres on a bad act ("I did a bad thing") and pushes toward repair: apology, confession, amends.
Shame centres on the self ("I am bad") and pushes toward hiding, denial or anger (Tangney, Stuewig and Mashek 2007).
Guilt is a pro-social driver; shame much less so.

- apologise and make it right | benevolence-dependability | W | =map
- confess to a priest or an elder | tradition | W/G | =map (W)
- give money to a cause to balance the books | universalism-concern | W | !map F3: moral cleansing (Tetlock 2003) reads W
- avoid the person you wronged | security-personal | B/U | partial: avoidance for your own comfort reads B
- [inner] deny yourself every pleasure for a month as a penance | conformity-rules | W/B | =map

#### 5.3.5 Shame
Kind and links: painful. Reiss: acceptance, honor, status. SDT: relatedness and competence. Cowen and Keltner: near
awkwardness.  
Triggers: a public failure or exposure within the month (an exam failed, a firing, a debt or secret revealed, a
relative arrested); or repeated criticism of who the person is rather than what they did; or a visible mark of low
standing (poverty, illness, a body others mock).  
Likelier / rarer: likelier with high face and conformity values, in honour cultures, with harsh or critical parents,
low self-esteem; rarer with unconditional support, a forgiving community, self-compassion.  
Stages: juv (peak sensitivity), then all.  
Research: Shame tends to drive hiding, escape, denial and sometimes anger turned outward (Tangney et al. 2007).

- move to a city where nobody knows you | self-direction-action + security-personal | B/R | =map
- stop going out and stop answering the phone | security-personal | U/B | =map (U)
- lash out at the one who exposed you | power-dominance | R/B | =map (R)
- work twice as hard to win back your good name | face + achievement | W/B | partial: restoring honour reads W
- own it in public and ask for forgiveness | benevolence-dependability + humility | W/G | =map (W)

#### 5.3.6 Restlessness and stagnation
Kind and links: painful, slow. Reiss: independence, curiosity. SDT: autonomy and competence. Erikson: stagnation.  
Triggers: the same job, town and routine for 5+ years with no new role; or stimulation low for months; or an age
ending in 9 or 0; or a child left home within the year; or a friend or sibling made a big change.  
Likelier / rarer: likelier with high stimulation and self-direction values, at ages ending in 9, after a fresh-start
landmark; rarer with growth inside the current life (a new role, a new child, a project), high security and tradition
values.  
Stages: ya, adult, mature (midlife).  
Research: At ages ending in 9, people search more for meaning, are 48% overrepresented among first-time marathon
runners, and are overrepresented among men using an affair website (about 18%) (Alter and Hershfield 2014). Most
adults never report a midlife crisis: about a quarter of US adults over 35 said they had one, and more than half of
those tied it to events such as illness or job loss rather than to ageing (Wethington 2000).

- train for your first marathon | achievement | R/G | !map F8: physical challenge reads R/G
- quit and travel for six months | stimulation + self-direction-action | R | =map (R)
- retrain for a different career | self-direction-thought + achievement | U/B | =map (U)
- take on a new role at church or in the union | tradition + benevolence-dependability | W/G | =map (W)
- [wrong] begin an affair | hedonism + stimulation | R/B | =map

#### 5.3.7 Burnout
Kind and links: painful, slow. Reiss: tranquility. SDT: autonomy and competence frustrated. Maslach: exhaustion,
cynicism, a sense of ineffectiveness.  
Triggers: work or care hours high for 3+ months, together with any of: control low, reward low, unfair treatment, a
team without support, a clash between the person's values and the job's demands; or no rest day for weeks.  
Likelier / rarer: likelier in caring jobs, with high benevolence-dependability (cannot say no), perfectionism, low
control, unfair treatment; rarer with autonomy, fair reward, a supportive team, firm limits on hours.  
Stages: ya, adult, mature.  
Research: Burnout has three parts (exhaustion, cynicism, a sense of ineffectiveness) and grows out of mismatch between
person and job in six areas: workload, control, reward, community, fairness and values (Maslach and Leiter 2016).

- take sick leave and sleep for a week | security-personal | G/U | partial F7: rest reads G
- quit with no plan | self-direction-action | R | =map (R)
- ask for fewer hours and hold the line | security-personal + conformity-rules | W/U | =map
- go cynical and do the bare minimum | hedonism | B/R | =map (B)
- move to work that fits your values | universalism-concern + self-direction-thought | W/U | !map: work that fits your conscience reads W/U

#### 5.3.8 Grief
Kind and links: painful. Reiss: family, social contact. SDT: relatedness lost. Cowen and Keltner: sadness, empathic
pain.  
Triggers: the death of a partner, child, parent, sibling or close friend within the year (strongest in the first 6
months); anniversaries, holidays and the dead person's things re-trigger it.  
Likelier / rarer: likelier to be long after a sudden or violent death, the death of a child or partner, heavy
dependence on the dead person, few other ties; rarer with a wide network, faith and ritual, a chance to say goodbye.
Roughly one bereaved adult in ten develops prolonged grief (Lundorff et al. 2017); most show resilience or steady
recovery (Bonanno 2004).  
Stages: all; partner loss commonest for elders.  
Research: In the dual process model (Stroebe and Schut 1999), healthy grieving swings between loss-oriented coping
(crying, remembering, visiting the grave) and restoration-oriented coping (new tasks, new roles, time off from grief).
Engine: alternate the two kinds of response rather than draining grief in one act.

- keep the rites and visit the grave every week | tradition | G/W | =map
- learn to do the tasks your partner always did | security-personal | U/G | =map (U)
- start a fund in their name | universalism-concern + benevolence-dependability | W | =map (W)
- drink to dull it | hedonism | B/R | =map (B)
- [inner] rage at God for taking them | self-direction-action | R | =map (R)

#### 5.3.9 Meaninglessness
Kind and links: painful. Reiss: idealism. SDT: all three needs low. Search for meaning.  
Triggers: meaning low for 2+ months; or a goal served for years is reached or lost (graduation, retirement, children
gone, a cause won or lost); or an age ending in 9 or 0; or a brush with death; or success that brought no joy.  
Likelier / rarer: likelier in young adults, after extrinsic goals are met, after losing a faith; rarer with close
ties, a faith, generative roles, work felt as a calling.  
Stages: ya, mature, elder.  
Research: Search for meaning is highest early in life and presence of meaning highest later; in later life, searching
goes with lower well-being more strongly than in youth (Steger, Oishi and Kashdan 2009, n = 8,756). Meaninglessness
and boredom both call up nostalgia, which restores a sense of meaning (Routledge et al. 2011).

- return to the faith of your childhood | tradition | W/G | =map (W)
- volunteer at the hospice | universalism-concern + benevolence-caring | W/G | =map (W)
- read philosophy and keep a journal | self-direction-thought | U | !map F1
- buy the sports car | hedonism + power-resources | B/R | =map (B)
- decide to have a child, or another one | benevolence-caring + tradition | G/W | =map

#### 5.3.10 Homesickness
Kind and links: painful. Reiss: family, tranquility. SDT: relatedness. A "mini-grief" for home (Stroebe et al. 2015).  
Triggers: moved away within 3 months (first year at university, a job abroad, military service, migration, boarding
school, a care home), and ties at home strong; worse at holidays and family events.  
Likelier / rarer: likelier with insecure attachment, strong family ties, a first separation, a new place very unlike
home, few new friends; rarer with physical activity and distraction, prior time away, quick new friendships (Stroebe,
Schut and Nauta 2015).  
Stages: child (camp, boarding school), juv, ya (first move), migrants at any age, elder entering care.  
Research: Homesickness goes with anxiety, low mood, poorer concentration and higher dropout among students; distance
from home does not predict it well (Stroebe et al. 2015).

- phone home every night | benevolence-caring | G/W | =map (G)
- cook your grandmother's recipes for new friends | tradition + benevolence-caring | G/W | =map
- drop out and go home | security-personal + tradition | G/W | =map (G)
- join the society of people from your home region | tradition + conformity-interpersonal | W/G | =map
- throw yourself into exploring the new city | stimulation | R | =map

#### 5.3.11 Fear of death
Kind and links: painful, often outside awareness. Reiss: tranquility. Terror management theory. Cowen and Keltner:
fear, anxiety.  
Triggers: the death of someone the person's age within the year; or a health scare or diagnosis; or a round birthday
from 40 on; or a funeral, a disaster or a war in the news; or the death of the last parent ("next in line").  
Likelier / rarer: likelier in young adults (death anxiety tends to fall with age, with a second rise for women around
their fifties: Russac et al. 2007, Death Studies 31(6), 549-561, not re-read), with weak faith and few ties; rarer
with strong faith, a sense of a life well lived, generative roles.  
Stages: ya, adult, mature.  
Research: Terror management theory holds that reminders of death push people to defend their worldview, strive for
self-esteem and seek symbolic immortality (children, works, a name). A 2010 meta-analysis found a moderate effect
(Burke et al. 2010); a 2025 meta-analytic review (JPSP 129(1)) finds the effects highly heterogeneous, many studies
underpowered, and advises assuming a small effect (about r = .18). Use this as a weak, noisy driver.

- write your will and put your papers in order | security-personal | U/W | =map (U)
- go back to church | tradition | W/G | =map (W)
- write your memoirs for the grandchildren | tradition + achievement | G/U | !map: a legacy for kin reads G
- book the trip you always postponed | stimulation + hedonism | R | =map
- [inner] defend your country's ways more fiercely against outsiders | security-societal + tradition | W/G | =map

#### 5.3.12 Anger
Kind and links: painful but energising, fast. Reiss: vengeance. SDT: autonomy blocked. Cowen and Keltner: anger.  
Triggers: an insult or slight within the day; or someone blocks a goal; or unfair treatment of the person or their
own; or property damaged; or a promise broken.  
Likelier / rarer: likelier with high power and face values, tiredness, hunger, pain, alcohol, a history with this
person; rarer with high conformity-interpersonal, empathy for the offender, time to cool off.  
Stages: all; tantrums in child; peaks in juv.  
Research: Anger is an approach emotion: it pushes toward the source of the problem rather than away from it (Carver
and Harmon-Jones 2009).

- confront them face to face | power-dominance | R | =map (R)
- write a formal complaint | conformity-rules | W/U | =map
- go for a hard run to burn it off | conformity-interpersonal | R/G | !map: venting through the body reads R/G
- forgive and let it go | benevolence-caring + humility | W/G | =map (W)
- [wrong] slash their tyres | power-dominance | R/B | =map (R)

#### 5.3.13 Craving
Kind and links: painful pull, fast. Reiss: eating, romance, tranquility. Cowen and Keltner: craving.  
Triggers: a cue tied to a habit (a smell, a place, a time of day, a friend who uses); or 1+ day without a habitual
pleasure; or stress, tiredness or sadness; or the evening after a day of hard self-control.  
Likelier / rarer: likelier with an established habit or addiction, high hedonism, earlier self-control the same day,
stress; rarer in cue-free surroundings, with absorbing goals, after sleep.  
Stages: juv, ya, adult (any stage).  
Research: In a week of experience sampling (205 adults, 7,827 desires), desires for sleep and sex were the most
intense, leisure and sleep clashed most with other goals, and media use and work were where self-control failed most;
more self-control earlier in the day predicted more failure later (Hofmann, Vohs and Baumeister 2012).

- give in and enjoy it | hedonism | R/B | =map
- go for a walk until it passes | security-personal | U/G | =map (U)
- pour every bottle in the house down the sink | security-personal + conformity-rules | U/W | =map (U)
- call your sponsor or a friend for help | benevolence-caring | W | =map
- [wrong] take money from your parents' purse to pay for it | hedonism + power-resources | B/R | =map (B)

#### 5.3.14 Feeling trapped
Kind and links: painful. Reiss: independence. SDT: autonomy frustrated. Entrapment, reactance.  
Triggers: autonomy low for months with no exit in sight (debt, a contract, a visa tied to a job, a marriage, a caring
role, a small town, a disability); or a plan to leave blocked again within the year.  
Likelier / rarer: likelier with high self-direction and stimulation values, low income, dependence on one person,
social pressure against leaving; rarer with savings, a network outside the trap, a sense of purpose in the role.  
Stages: juv (home), ya, adult (marriage, work, care), elder (care home).  
Research: Feeling defeated and trapped, with escape blocked, goes with low mood (Gilbert and Allan 1998). When a
freedom is threatened, people want it more and act to restore it (reactance, Brehm 1966).

- save in secret for the day you leave | self-direction-action + security-personal | U/B | =map (U)
- leave suddenly, with one bag | self-direction-action + stimulation | R | =map (R)
- accept it as your lot and find what peace you can | humility | G/W | =map
- fight for change from inside: a union, a family meeting | universalism-concern + conformity-rules | W | =map
- escape into daydreams and novels every night | hedonism + self-direction-thought | U/R | partial F1: escape into the mind reads U

#### 5.3.15 A sense of injustice
Kind and links: painful but energising. Reiss: idealism, vengeance. Cowen and Keltner: anger. Relative deprivation.  
Triggers: the person or their group treated worse than others for no fair reason within the month (passed over,
underpaid, singled out by police, an unfair verdict); or news of an injustice touching a value they hold high; or a
rule enforced on them and waived for the powerful.  
Likelier / rarer: likelier with high universalism-concern and conformity-rules (rules should bind everyone), when the
unfairness is felt on behalf of a group, when it comes with anger rather than resignation, and when change looks
possible; rarer when the system is seen as legitimate, when the person benefits from it, or with low sense of
efficacy.  
Stages: child (from about 3-4, unequal shares), juv (peak), ya, adult.  
Research: Relative deprivation (judging one's lot unfair compared with a reference group) predicts collective action
best when it is felt for a group and comes with anger (Smith, Pettigrew et al. 2012).

- join the union and organise | universalism-concern + benevolence-dependability | W | =map (W)
- take them to court | conformity-rules + universalism-concern | W/U | =map
- speak out publicly and name names | universalism-concern + stimulation | W/R | partial F3: justice reads W
- [wrong] take what you are owed from the till | power-resources | B/R | =map
- [inner] decide nothing ever changes and stop voting | humility | B/G | partial: cynical resignation reads B

#### 5.3.16 Jealousy
Kind and links: painful, fast. Reiss: romance, family. Guards a bond against a rival (envy wants what another has;
jealousy fears losing what one has).  
Triggers: a partner's attention to a rival within the week (messages, time, praise); or a new sibling (child); or a
best friend's new best friend; or a parent's new partner.  
Likelier / rarer: likelier with anxious attachment, low self-esteem, an earlier betrayal, heavy dependence on the
partner; rarer with secure attachment, years of trust, a full life outside the relationship.  
Stages: child (a new sibling), juv (friends), ya, adult (partners).  
Research: The envy-jealousy split follows standard usage (Buss 2000, The dangerous passion; not re-read).

- tell them how you feel and ask for reassurance | conformity-interpersonal + benevolence-caring | W/G | =map
- [wrong] read their messages in secret | security-personal | B/U | partial: snooping reads B
- make yourself more attentive and attractive to win them back | face | B/R | !map: winning back attention reads B
- flirt with someone else to even the score | hedonism + power-dominance | R/B | =map
- end it before you get hurt | security-personal + self-direction-action | B/R | =map

#### 5.3.17 Feeling old
Kind and links: painful, slow. Reiss: physical activity, status. Subjective age.  
Triggers: a round birthday from 40; or the body failing at something it used to do (stairs, a sport, reading small
print); or being offered a seat; or a younger boss; or a first grandchild; or a peer's death.  
Likelier / rarer: likelier with negative views of ageing, poor health, retirement, a youth-centred job or culture;
rarer with good health, mixed-age friendships, positive views of ageing.  
Stages: mature, elder; first felt around 40.  
Research: Most adults over 40 feel about 20% younger than their age (Rubin and Berntsen 2006, Psychonomic Bulletin and
Review 13(5), 776-780; not re-read). Positive views of one's own ageing are linked to longer life (Levy et al. 2002,
JPSP 83(2), 261-270; not re-read). Engine: "feeling old" fires when felt age catches up with real age, not at a fixed
age.

- take up a demanding new sport | achievement + stimulation | R/G | =map (R)
- dye your hair and buy younger clothes | face + hedonism | B/R | =map (B)
- start mentoring the young colleagues | benevolence-dependability | W/G | =map
- book every check-up and follow every medical rule | security-personal + conformity-rules | U/W | =map (U)
- [inner] accept the lines on your face as a record of your life | humility | G/W | =map

#### 5.3.18 Feeling invisible
Kind and links: painful. Reiss: acceptance, status. SDT: relatedness and competence. Ostracism.  
Triggers: no one asks the person's opinion for weeks; or passed over in talk, at work or in the family; or messages
and posts unanswered; or left out of an event peers attend; or retirement plus a shrinking network.  
Likelier / rarer: likelier in older people (older women especially in youth-centred settings), newcomers, quiet
people, low-status roles; rarer with a role others rely on, a close circle, public standing.  
Stages: juv (left out), adult (overlooked at work), mature, elder.  
Research: Ostracism threatens belonging, self-esteem, control and a sense of mattering. After the first sting, people
either try to win back belonging (pleasing, conforming, joining) or to regain control and be noticed (provocation,
sometimes aggression); long-lasting exclusion ends in resignation and withdrawal (Williams 2009).

- work hard to please and fit in | conformity-interpersonal | W | =map
- do something outrageous to be noticed | stimulation + face | R/B | =map
- write to the newspaper every week | face + self-direction-thought | U/R | =map (U)
- join a new group where people know your name | benevolence-caring | G/W | =map (G)
- [inner] withdraw and stop trying to be heard | humility | G | =map

#### 5.3.19 Regret for the road not taken
Kind and links: painful, slow. Cowen and Keltner: sadness, disappointment.  
Triggers: meeting someone who lives the life the person turned down; or a reunion; or an age ending in 9 or 0; or the
last chance for a path closing (an age limit, a fertility limit, a parent's death); or a child making the choice the
person did not.  
Likelier / rarer: likelier for things not done (in the long run), in education, career and romance, and where the
chance still seems open; rarer with acceptance and a sense that the other path was never really open.  
Stages: adult, mature, elder.  
Research: People regret actions more in the short run and inactions more in the long run; some inaction regrets turn
wistful, others stay painful (Gilovich and Medvec 1995; Gilovich, Medvec and Kahneman 1998).

- go back to school for the degree you never finished | self-direction-thought + achievement | U/B | =map (U)
- find your first love online and write to them | hedonism + stimulation | R | =map
- push your child toward the path you missed | power-dominance + achievement | B/W | =map
- open the café at sixty after all | self-direction-action + achievement + stimulation | R/B | =map (R)
- [inner] tell yourself it was never meant to be | humility | G/W | =map

#### 5.3.20 Humiliation and wounded honour
Kind and links: painful, energising. Reiss: vengeance, honor, status. Refined value: face.  
Triggers: mocked or insulted in front of others within the week; or the person's family, faith or group insulted; or
beaten publicly by a rival; or betrayed by someone trusted.  
Likelier / rarer: likelier with high face and power values, in honour cultures, among young men, when the audience
matters to the person; rarer with high humility, self-compassion, an apology received.  
Stages: juv, ya (peak), adult.  
Research: Reiss's vengeance (get even, confront offenders) and the refined value of face (avoid humiliation) meet in
this state.

- challenge them in front of the same audience | power-dominance + face | R/B | =map (R)
- demand a public apology | face + conformity-rules | W | =map
- beat them fairly next time | achievement | B/R | =map
- [wrong] spread their secrets in return | power-dominance | B | =map
- [inner] swallow it and keep your dignity | conformity-interpersonal + humility | W/G | =map

#### 5.3.21 Money worry
Kind and links: painful, chronic. Reiss: saving, tranquility. Scarcity.  
Triggers: bills above income for 2+ months; or a job lost or hours cut within the year; or debt rising for 3+ months;
or a large unexpected cost (a repair, a medical bill); or prices rising faster than pay.  
Likelier / rarer: likelier with low income, no savings, dependants, insecure work; rarer with savings, a second income
in the home, family who can help, modest wants.  
Stages: ya, adult (with children), elder (on a fixed income).  
Research: Scarcity narrows attention to the immediate shortfall; in one study, thinking about a hard financial problem
lowered poorer participants' scores on cognitive tests (Mani, Mullainathan, Shafir and Zhao 2013, Science 341,
976-980; not re-read).

- take a second job | security-personal + achievement | U/B | =map
- cut every expense and keep a budget to the penny | security-personal | U/W | =map (U)
- ask your family for help | tradition + benevolence-caring | G/W | =map
- buy lottery tickets every week | hedonism + stimulation | R/B | =map
- [wrong] fiddle the benefit forms | power-resources + security-personal | B | !map: cheating for money reads B

#### 5.3.22 Fear and feeling unsafe
Kind and links: painful, fast or chronic. Reiss: tranquility. Cowen and Keltner: fear, anxiety.  
Triggers: a crime, accident or threat within the month (to the person, a neighbour, or in local news); or war, unrest
or disaster nearby; or a threatening ex-partner; or a new route home after dark.  
Likelier / rarer: likelier with high security values, past victimisation, living alone, a high-crime area; rarer with
trusted neighbours and trusted police.  
Stages: all; child (fears of the dark), elder (falls, crime).  
Research: Security values rise after threat; see section 6.

- buy better locks and an alarm | security-personal | U/W | =map (U)
- move in with family | security-personal + tradition | G/W | =map (G)
- take a self-defence class | security-personal | R/W | partial: protection by force reads R (as in section 3.6)
- start a neighbourhood watch | security-societal + benevolence-dependability | W | =map
- get a big dog | security-personal + benevolence-caring | G/R | !map: a guard animal reads G

#### 5.3.23 Feeling controlled
Kind and links: painful, fast. Reiss: independence. SDT: autonomy frustrated. Reactance.  
Triggers: a new rule or restriction aimed at the person within the week (a curfew, a dress code, being watched, a
partner checking up, a doctor's ban); or someone making choices for them; or being told what to feel.  
Likelier / rarer: likelier with high self-direction and stimulation values, in adolescence, when the rule seems
illegitimate; rarer when the rule is explained, agreed together, or comes from a trusted authority.  
Stages: child (from about 2), juv (peak), ya, elder (when grown children take over).  
Research: A threatened freedom becomes more attractive, and people act to restore it, sometimes by doing exactly the
forbidden thing (Brehm 1966). Requests that give reasons and choice provoke less defiance than controlling ones (SDT).

- do exactly what you were forbidden | self-direction-action + stimulation | R | =map (R)
- argue the rule point by point, with reasons | self-direction-thought | U/R | partial F1
- obey to their face and break it behind their back | self-direction-action + face | B/U | =map
- negotiate a compromise you can live with | conformity-interpersonal + self-direction-action | W/U | partial: a negotiated rule reads W
- obey and swallow the resentment | conformity-rules | W | =map

#### 5.3.24 Falling behind the social clock
Kind and links: painful, slow. Reiss: status, family, acceptance. The social clock.  
Triggers: peers' weddings, babies, houses or promotions while the person has none; or an age past the local norm for a
milestone; or a parent asking "when?" at every visit.  
Likelier / rarer: likelier where age norms are tight, with high conformity and tradition values, in the late 20s and
the 30s; rarer where norms are loose, with a chosen alternative life, with peers on similar paths.  
Stages: ya, adult.  
Research: People share expectations about the right age for marriage, children, a home and a career step, and feel
early or late against them (Neugarten, Moore and Lowe 1965). Envy is aimed mostly at same-age peers (Henniger and
Harris 2015).

- say yes to the next suitable match | tradition + conformity-rules | W/G | =map
- work longer hours to reach the next rung | achievement | B | =map
- buy a small flat on your own | security-personal + achievement | U/B | =map
- throw yourself into a cause instead | universalism-concern | W | !map F3
- [inner] decide the timetable belongs to someone else, and drop it | self-direction-action | R/B | =map (R)

#### 5.3.25 Disappointment
Kind and links: painful, short. Cowen and Keltner: tested, merged with sadness.  
Triggers: an expected good thing did not come within the week (a rejection letter, a lost bid, a broken promise, a
cancelled holiday); stronger the bigger the hope.  
Likelier / rarer: likelier with high expectations and heavy investment; rarer with modest hopes and a fallback plan.  
Stages: all; sharp and short in child, frequent in ya (applications, rejections).  
Research: Disappointment sits on the gradient toward sadness in Cowen and Keltner's map.

- try again next year with a better plan | achievement + self-direction-thought | U/B | =map (U)
- ask the panel for feedback and listen | self-direction-thought | U | !map F1
- take the second choice and make the best of it | humility + security-personal | G/W | =map (G)
- comfort-eat a whole cake | hedonism | G/R | partial F7
- sulk for days and refuse to talk about it | face | R/B | !map: sulking reads R

#### 5.3.26 Resentment
Kind and links: painful, slow: anger stored over time. Reiss: vengeance, honor.  
Triggers: an unfair burden carried for months (all the housework, all the care, a sibling who never helps, a boss who
takes the credit); or an old wrong never acknowledged; or a parent's favouritism.  
Likelier / rarer: likelier with high universalism-concern (fairness) and face, when complaints go unheard, with little
power to change things; rarer with an apology, a fair split, a voice in decisions.  
Stages: juv (siblings), adult (marriage, work, care), mature, elder (inheritance).  
Research: Stored anger at unfairness; the fairness side of the loyalty-fairness trade-off (section 4.1) turned inward.

- finally tell them what you have been carrying | universalism-concern + self-direction-action | R/W | =map (R)
- insist on a written rota | conformity-rules + universalism-concern | W | =map
- keep a list of every wrong | face + power-dominance | B/U | =map
- forgive and draw a line under it | benevolence-caring + humility | W/G | =map (W)
- [wrong] quietly stop doing your share | hedonism | B/R | =map (B)

#### 5.3.27 Fear of missing out
Kind and links: painful, fast. Reiss: social contact, status. SDT: low need satisfaction.  
Triggers: watching peers' events online from home; or an invitation not received; or a trip the person cannot afford;
or a big event on the same night as a duty.  
Likelier / rarer: likelier in the young, in heavy social media users, and in people whose needs for autonomy,
competence and relatedness are poorly met (Przybylski et al. 2013); rarer with a full social life, low stimulation
values, older age.  
Stages: juv, ya (peak).  
Research: In Przybylski et al. (2013) fear of missing out was highest in young adults and young men, and linked to low
need satisfaction and low mood.

- drop everything and go | stimulation + hedonism | R | =map
- post your own highlights to compete | face + achievement | B | =map (B)
- plan your own party | benevolence-caring + stimulation | R/G | =map
- delete the apps for a month | security-personal | U/G | =map (U)
- [inner] tell yourself you would not have enjoyed it anyway | humility | B/G | partial: a sour-grapes story reads B

#### 5.3.28 Worry about looks
Kind and links: painful, chronic. Reiss: romance, acceptance, status. Kasser and Ryan: image (an extrinsic
aspiration).  
Triggers: a hurtful remark about the body within the month; or weeks of comparison with images; or weight, skin or
hair changes (puberty, pregnancy, illness, age); or a wedding, reunion or beach holiday ahead.  
Likelier / rarer: likelier in adolescents, with high face and image goals, in appearance-centred groups; rarer with a
body-neutral family, sport for fun, older age (appearance envy is mostly a young person's envy: Henniger and Harris
2015).  
Stages: juv (peak), ya, adult.  
Research: Image is one of the three extrinsic aspirations in the Aspiration Index; ranking it high goes with poorer
well-being (Kasser and Ryan 1996).

- diet hard before the wedding | achievement + face | U/B | =map
- train at the gym every morning | achievement | B/R | =map
- save up for cosmetic surgery | face | B | !map: buying a new face reads B; face scores Blue
- wear what you like and stop caring | self-direction-action | R | =map (R)
- stop going swimming with your friends | security-personal + conformity-interpersonal | U/W | =map (U)

#### 5.3.29 Caregiver strain
Kind and links: painful, slow. Reiss: family, tranquility. SDT: autonomy frustrated, relatedness strained.  
Triggers: caring for an ill, disabled or frail relative for 3+ months at 10+ hours a week with little respite; or care
on top of full-time work; or the person cared for no longer recognises the carer.  
Likelier / rarer: likelier for daughters and wives, with high benevolence-dependability and tradition (filial duty),
low income, dementia care, no sibling sharing the load; rarer with respite services, shared care, a flexible employer.  
Stages: adult, mature (caring for parents while raising children), elder (caring for a spouse).  
Research: 67% of working caregivers report some difficulty balancing work and care, 84% say caring raises their daily
stress, 27% have cut hours and 16% stopped work for a time (AARP and S&P Global 2024; see section 4.1).

- arrange a place in a care home | security-personal | U/W | =map (U)
- insist your brother takes every other weekend | universalism-concern + conformity-rules | W | =map
- cut your hours at work | benevolence-caring | G/W | =map (G)
- join the carers' group at the community centre | conformity-interpersonal + benevolence-caring | W/G | =map
- book a week of respite care and go to the sea | hedonism | G/R | partial F7

#### 5.3.30 Feeling useless
Kind and links: painful, slow. Reiss: power, family, status. SDT: competence and relatedness.  
Triggers: retirement within the year; or the youngest child left home within the year; or out of work for 3+ months;
or a disability that ends a role; or the family no longer asks for help or advice.  
Likelier / rarer: likelier when identity rested on one role (the provider, the mother, the boss), with low
generativity, in elders with few contacts; rarer with volunteer work, grandchildren, a craft, part-time "bridge" work.  
Stages: mature (empty nest, retirement), elder.  
Research: Older adults (70-79) who rarely or never felt useful to others had about three times the odds of new
disability and more than four times the odds of dying over seven years (Gruenewald et al. 2007, n = 1,030). Most
parents' marital satisfaction rises when the children leave (Gorchoff, John and Helson 2008, Psychological Science
19(11), 1194-1200; not re-read), so the empty nest is a risk, not a rule.

- volunteer at the food bank three days a week | universalism-concern + benevolence-caring | W/G | =map (W)
- offer to mind the grandchildren | benevolence-caring + tradition | G/W | =map
- go back to part-time work in your old trade | achievement + security-personal | U/B | =map
- start the business you always talked about | self-direction-action + achievement | B/R | =map
- [inner] decide you are a burden and keep out of everyone's way | humility + conformity-interpersonal | W/G | =map

#### 5.3.31 Disillusionment
Kind and links: painful. Reiss: idealism, honor.  
Triggers: a trusted institution, leader, faith or cause shown to be corrupt or false within the year (a scandal in the
church, the party or the firm, a hero exposed); or years of effort for a cause with nothing to show; or a mentor's
betrayal.  
Likelier / rarer: likelier with high tradition or universalism invested in that institution and strong earlier
commitment; rarer with several sources of meaning and looser loyalties.  
Stages: juv, ya (first ideals broken), adult, mature.  
Research: Disillusionment is the main route out of a commitment; see section 6 on conversion and leaving a faith.

- leave the church or the party | self-direction-action + self-direction-thought | B/R | =map
- stay and fight to clean it up | universalism-concern + conformity-rules | W | =map
- throw yourself into a new movement | stimulation + universalism-concern | R/W | =map
- keep the faith and drop the institution | tradition + self-direction-thought | G/U | =map (G)
- [inner] decide every cause is a con and look after yourself | power-resources | B | =map

#### 5.3.32 Inner conflict: having acted against your own values
Kind and links: painful. Cognitive dissonance.  
Triggers: within the month the person did something that contradicts a value in their top three (a vegetarian ate
meat, an honest person lied, prayers were skipped, a vote went against conscience); or a job that requires such acts
every week.  
Likelier / rarer: likelier with strongly held, openly stated values and public commitments; rarer with low
self-scrutiny and plenty of excuses at hand.  
Stages: juv, ya, adult (any stage).  
Research: A clash between an act and a belief is unpleasant, and people reduce it by changing the act, changing the
belief, or adding justifications (Festinger 1957). In Chroma terms this is the after-effect of a section 4 dilemma.

- change the behaviour and make a public vow | benevolence-dependability + conformity-rules | W | =map
- confess and do a penance | tradition | W/G | =map (W)
- quit the job that forces it on you | universalism-concern + self-direction-action | W/R | partial: leaving for conscience reads W
- find a good reason why this case was different | face | U/B | =map
- [inner] decide the rule was never that important | self-direction-action | B/R | =map

#### 5.3.33 Moral disgust
Kind and links: painful, fast. Cowen and Keltner: disgust.  
Triggers: witnessing or learning of a degrading, cruel or corrupt act within the week; or a betrayal of trust by
someone respected; or a violation of something sacred (a desecrated grave, a mocked rite).  
Likelier / rarer: likelier with high tradition and conformity values and strong purity norms; rarer with high
universalism-tolerance and openness.  
Stages: juv, ya, adult, mature, elder.  
Research: Disgust lies on the gradient from anxiety through fear and horror to disgust in Cowen and Keltner (2017).
Violations of sacred values provoke outrage and acts of cleansing (Tetlock 2003).

- cut the person off completely | tradition + conformity-rules | W | =map
- report it to the authorities | conformity-rules + universalism-concern | W | =map
- clean the whole house from top to bottom | security-personal + conformity-rules | W/U | =map
- denounce it loudly in public | universalism-concern + stimulation | R/W | =map
- [inner] lose all respect for them, in silence | face | B/W | !map: cold contempt reads B

#### 5.3.34 Heartbreak
Kind and links: painful. Reiss: romance. SDT: relatedness lost. Cowen and Keltner: sadness.  
Triggers: a breakup or rejection by a romantic partner within 3 months; or the former partner marries someone else; or
a confessed love refused.  
Likelier / rarer: likelier after a long or a first relationship, for the one who was left, with anxious attachment;
rarer with a wide network, a new interest, for the one who left.  
Stages: juv, ya (peak), adult, mature (divorce).  
Research: Heartbreak is grief-like and follows the same swing between dwelling on the loss and rebuilding (5.3.8).

- cut your hair short and change your look | self-direction-action + stimulation | R | =map (R)
- go out every night with your friends | stimulation + hedonism | R | =map
- throw yourself into study or work | achievement | B/U | =map
- pour it all into songs or poems | self-direction-thought | R/U | =map (R)
- [wrong] keep calling and turning up at their door | power-dominance | R/B | =map (R)

#### 5.3.35 Dread before a test
Kind and links: painful, anticipatory. Cowen and Keltner: anxiety.  
Triggers: an exam, interview, performance, operation or court date within 2 weeks, with high stakes; or an earlier
failure in the same kind of test.  
Likelier / rarer: likelier with high achievement and face values, perfectionism, parental pressure; rarer with
experience, low stakes, good preparation.  
Stages: child, juv, ya (exams), adult (interviews, operations, court).  
Research: Anticipatory anxiety pulls toward either over-preparation or avoidance; which one depends on the person's
sense of control.

- prepare obsessively | achievement | U/B | =map (U)
- rehearse it with a friend playing the examiner | achievement + benevolence-caring | U/W | =map
- pray for help | tradition | W/G | =map (W)
- drink to calm your nerves | hedonism | B/R | =map (B)
- phone in sick on the day | security-personal + face | U/B | =map

#### 5.3.36 Chronic pain or illness
Kind and links: painful, chronic. Reiss: tranquility, physical activity.  
Triggers: pain or a limiting illness for 3+ months; or a new diagnosis within the year; or a flare after a calm spell.  
Likelier / rarer: likelier in mature and elder stages, after physical work, with low income; rarer with good care,
flexible work, people to help.  
Stages: adult, mature, elder.  
Research: Illness is also one of the life events that predicts value change (section 6).

- research every treatment and push your doctors | self-direction-thought + security-personal | U/B | =map (U)
- try the healer your grandmother trusted | tradition | G/W | =map
- keep working through the pain to prove you still can | achievement + face | B/R | =map (B)
- join a patients' group and campaign for better care | universalism-concern + benevolence-caring | W/G | =map (W)
- [inner] accept it and rebuild your days around it | humility | G/W | =map

#### 5.3.37 Worry for a child
Kind and links: painful, chronic. Reiss: family. Cowen and Keltner: anxiety.  
Triggers: a child ill, failing at school, using drugs, in a risky job, abroad in danger, out late without word; or a
teenager who stops talking; or an adult child's failing marriage or debts.  
Likelier / rarer: likelier with high benevolence-caring and security values, a child with health or behaviour
problems, single parenthood; rarer with a steady co-parent and a child who confides.  
Stages: adult, mature, elder.  
Research: Parents' worry is the protective urge (5.4.10) under threat.

- sit down and talk to the child, calmly | benevolence-caring | W/G | =map
- tighten the rules and the curfew | conformity-rules + security-personal | W/U | =map
- move house to get them away from the wrong crowd | security-personal + benevolence-caring | G/W | partial: uprooting for your young reads G
- pay for the best help money can buy | benevolence-caring + power-resources | B/G | =map (B)
- [wrong] read their diary | security-personal | B/U | partial: snooping reads B

#### 5.3.38 Fear of being left
Kind and links: painful. Reiss: romance, acceptance. Attachment anxiety.  
Triggers: a partner growing distant for weeks (less talk, less touch, more time away); or an old abandonment
re-awakened (a parent who left, an earlier partner who left); or the partner's new job, new friends or a move.  
Likelier / rarer: likelier with anxious attachment, a history of abandonment, money or housing tied to the partner;
rarer with secure attachment, one's own friends and income.  
Stages: ya, adult, mature.  
Research: Anxious attachment heightens alarm at signs of distance (Hazan and Shaver 1987, JPSP 52(3), 511-524; not
re-read).

- call them several times a day | security-personal + benevolence-caring | R/G | !map: clinging reads R
- talk it through with them honestly | benevolence-dependability | W | =map
- plan a holiday to win back closeness | benevolence-caring + hedonism | R/G | =map
- suggest couples counselling | benevolence-dependability + self-direction-thought | U/W | !map: deliberate repair reads U and W; the blend scores Black
- pull away first so it hurts less | self-direction-action + security-personal | B | =map

#### 5.3.39 Defeat and a sense of failure
Kind and links: painful. Reiss: power, status. SDT: competence frustrated.  
Triggers: a loss in a contest that mattered (an election, a final, a failed business, a lost court case) within the
month; or the same goal failed 3+ times; or bankruptcy.  
Likelier / rarer: likelier with high achievement and power values and public stakes; rarer with other areas of
competence, a supportive coach or family, a long view.  
Stages: juv, ya, adult.  
Research: Whether defeat leads to renewed effort or to giving up depends on whether the person sees the cause as
fixable; pride after success increases perseverance (Williams and DeSteno 2008), and rivalry raises effort (Kilduff et
al. 2010).

- work out what went wrong and train again | achievement + self-direction-thought | U/B | =map (U)
- congratulate the winner and mean it | conformity-interpersonal + benevolence-caring | W | =map
- give it up for good and find something else | humility | G/B | =map
- blame the referee and the system | face | R/B | !map: blaming others reads R and B
- [wrong] cheat next time | achievement | B | =map

#### 5.3.40 Social anxiety
Kind and links: painful, anticipatory. Reiss: acceptance. Cowen and Keltner: anxiety, awkwardness.  
Triggers: a party, speech, date, new class or room of strangers within the week; or a recent embarrassment; or a move
to a new school or job.  
Likelier / rarer: likelier in adolescents, shy temperaments, after bullying, with high face and
conformity-interpersonal values; rarer with practice, a trusted companion, a set role at the event.  
Stages: juv (peak), ya.  
Research: Fear of being judged pulls toward avoidance or toward a safe role; practice and a defined role lower it.

- stay home with a made-up excuse | security-personal | U/B | =map (U)
- go, and stick close to the one person you know | benevolence-caring + security-personal | W/G | =map
- drink before you go | hedonism | B/R | =map (B)
- offer to help in the kitchen so you have a role | conformity-interpersonal + benevolence-dependability | W | =map
- push yourself to talk to three strangers | achievement + stimulation | R/B | =map (R)

### 5.4 Pleasant and energising drivers

Pleasant states push action as much as painful ones: approach states (curiosity, ambition, love, inspiration) start
new projects, and calm states (contentment, gratitude) push toward keeping, savouring and giving. Positive emotions
widen the range of acts a person considers (Fredrickson 2001), so the response sets below are deliberately more
varied. Same format as 5.3.

#### 5.4.1 Curiosity
Kind and links: pleasant, energising. Reiss: curiosity. SDT: intrinsic motivation (autonomy, competence). Cowen and
Keltner: interest.  
Triggers: a gap noticed between what the person knows and wants to know (a puzzle, a mystery, a half-told story, a
strange object); or a new place, person or field within reach; or security and competence at least middling (enough
safety to explore).  
Likelier / rarer: likelier with high self-direction-thought, free time, a secure base (feeling supported raises
exploration: Feeney 2004); rarer under threat, exhaustion, money worry or a fixed routine. General novelty seeking
falls after adolescence, but interest in chosen subjects can stay strong into old age.  
Stages: child (peak), juv, ya; elder (chosen subjects).  
Research: In Loewenstein's information-gap account (1994), curiosity is a felt lack caused by a gap in knowledge,
strongest when the gap looks small enough to close, and it pushes toward finding the missing piece. Curiosity is the
desire that the ten-value model files under self-direction (F1).

- take the clock apart to see how it works | self-direction-thought | U | !map F1
- travel to see the place for yourself | stimulation + self-direction-thought | R/U | =map (R)
- ask the stranger on the train about their life | universalism-tolerance + self-direction-thought | U/W | !map F1: interest in other lives reads U
- dig into the family history in the archives | tradition + self-direction-thought | U/G | partial F1: research reads U
- [wrong] open the letter addressed to someone else | self-direction-thought | U/B | partial F1

#### 5.4.2 Pride
Kind and links: pleasant, energising. Reiss: status, power. Cowen and Keltner: tested, merged (near triumph and
satisfaction). Authentic and hubristic pride.  
Triggers: a success the person worked for within the week (an exam passed, a job well done, a house built, a child
raised); or praise from someone they respect; or a skill mastered.  
Likelier / rarer: authentic pride likelier when success is credited to effort; hubristic pride (arrogance) likelier
with high power and face values and a sense of fixed superiority; rarer with high humility and where self-praise is
frowned on.  
Stages: all; strong in child ("watch me!") and juv.  
Research: Authentic pride (from effort) goes with achievement and prosocial acts; hubristic pride (from feeling
superior) goes with aggression and antisocial acts (Tracy and Robins 2007). Pride raises perseverance on the next hard
task (Williams and DeSteno 2008).

- take on a harder challenge | achievement | B/U | =map
- throw a party to celebrate | hedonism + benevolence-caring | R/G | =map
- frame the certificate and hang it on the wall | face + achievement | W/B | partial: displayed honours read W
- teach the skill to someone younger | benevolence-caring | W/G | =map
- [inner] start looking down on those who did not make it | power-dominance | B | =map

#### 5.4.3 Ambition
Kind and links: energising, slow-burning. Reiss: power, status. Kasser and Ryan: wealth and fame (extrinsic) or growth
(intrinsic).  
Triggers: a visible ladder with the next rung within reach; or a mentor's encouragement; or a rival's rise; or a first
taste of success; or growing up with little and wanting more than one's parents had.  
Likelier / rarer: likelier with high achievement and power values, in young adults, after a pride experience; rarer
with high humility and tradition, after burnout, and in old age as time horizons shrink (Carstensen 2006).  
Stages: juv, ya (peak), adult.  
Research: Ambition aimed at intrinsic goals (growth, contribution) goes with better well-being than ambition aimed at
wealth and fame (Kasser and Ryan 1996).

- apply for the top job | achievement + power-dominance | B | =map
- start your own company | self-direction-action + achievement | B/R | =map
- study at night for a second degree | achievement + self-direction-thought | U/B | =map (U)
- run for the town council | power-dominance + universalism-concern | W/B | partial F5: office reads W
- [wrong] take credit for a colleague's work | achievement | B | =map

#### 5.4.4 Hope
Kind and links: pleasant, energising. Snyder's hope: agency (the will) and pathways (the ways).  
Triggers: a path to a wanted goal appears within the month (a job to apply for, a treatment trial, a visa lottery, an
offer of reconciliation); or a crisis eases; or someone the person respects believes in them.  
Likelier / rarer: likelier with past successes, social support, faith; rarer after repeated failure, in depression,
under chronic scarcity.  
Stages: all.  
Research: Hopeful people make more plans, find more routes to a goal and keep going after setbacks (Snyder 2002).

- apply for everything going | achievement | B/U | =map
- make a step-by-step plan | security-personal + self-direction-thought | U | =map (U)
- pray and give thanks in advance | tradition | W/G | =map (W)
- tell all your friends before it is certain | stimulation | R | =map
- start saving for the new life | security-personal | U/W | =map (U)

#### 5.4.5 Inspiration
Kind and links: energising. Inspired by something, and inspired to do something.  
Triggers: seeing someone do something excellent within the day (a performance, a speech, a feat); or a new idea
arriving; or reading or hearing something that opens a possibility.  
Likelier / rarer: likelier with openness, mastery goals, absorption; rarer with fatigue, routine, cynicism.  
Stages: juv, ya, adult (any stage).  
Research: Inspiration has two parts, being moved by something and being moved to act on it, and it predicts creative
output (Thrash and Elliot 2003).

- start writing that same night | self-direction-thought | U/R | partial F1
- sign up for lessons with the master | achievement + self-direction-thought | U/B | =map (U)
- quit to follow the new idea | self-direction-action + stimulation | R | =map (R)
- share the speech with everyone you know | universalism-concern + benevolence-caring | W/R | =map (W)
- copy your hero's style down to the haircut | face + hedonism | R/B | =map

#### 5.4.6 Awe
Kind and links: pleasant, sometimes tinged with fear. Cowen and Keltner: awe. Vastness plus a need to make sense of
it.  
Triggers: something vast within the day: mountains, the ocean, a night sky, a storm, a cathedral, a birth, a great
work of art, a crowd moving as one; or a big new idea.  
Likelier / rarer: likelier with openness, time outdoors, travel, faith; rarer in cities without nature, in hurry, in
front of screens.  
Stages: all; frequent in child; often reported by elders.  
Research: Awe answers something vast that the mind must stretch to take in (Keltner and Haidt 2003). It shrinks the
sense of self and raises generosity: people who spent a minute looking up into tall eucalyptus trees helped a stranger
more than people who looked at a building (Piff et al. 2015).

- give more freely to strangers that week | universalism-concern | G/W | =map
- take up astronomy | self-direction-thought + universalism-nature | U/G | !map F1: wonder turned to study reads U
- go on a pilgrimage | tradition | W/G | =map (W)
- plan to climb the mountain next year | stimulation + achievement | R/G | =map (R)
- [inner] feel your worries shrink to their true size | humility | G | =map

#### 5.4.7 Gratitude
Kind and links: pleasant. Find, remind, bind.  
Triggers: help, a gift or a kindness that cost the giver something, within the week; or surviving a danger; or a
reminder of what one has (visiting the sick, coming home after hard travel).  
Likelier / rarer: likelier when the benefit was intended and costly, with high benevolence; rarer with entitlement,
high power values, suspicion of motives.  
Stages: all; tends to deepen with age.  
Research: Gratitude helps people find good partners, reminds them of the bonds they have and binds them closer (Algoe
2012); it pushes toward returning the favour and passing it on.

- return the favour twice over | benevolence-dependability + security-personal | W/G | =map
- write a thank-you letter to your old teacher | benevolence-caring | W/G | =map
- pay it forward to a stranger | universalism-concern | W/G | partial F3: passing kindness to anyone reads W
- say grace before every meal | tradition | W/G | =map (W)
- [inner] decide to spend less time chasing more | humility | G/W | =map

#### 5.4.8 Contentment
Kind and links: pleasant, calm. Cowen and Keltner: satisfaction, calmness. Reiss: tranquility.  
Triggers: needs met for months (belonging, security and competence middling to high) with no major threat; or a goal
reached and enjoyed; or a quiet evening after a full day.  
Likelier / rarer: likelier in later life (as time horizons shrink, people favour emotionally meaningful present goals:
Carstensen 2006), with secure income and close ties; rarer with high stimulation and achievement values, in
comparison-heavy surroundings.  
Stages: adult, mature, elder (common).  
Research: Calm positive states push toward savouring and keeping things as they are; contentment broadens by folding
recent experience into one's picture of self and world (Fredrickson 2001).

- stay where you are and turn down the move | security-personal + tradition | G/W | =map (G)
- tend the garden every evening | universalism-nature + hedonism | G | =map (G)
- invite the neighbours for a long lunch | benevolence-caring + hedonism | G/R | =map (G)
- say no to the promotion | humility | G/W | =map
- put money aside for the grandchildren | security-personal + benevolence-caring | U/G | =map (U)

#### 5.4.9 The urge to create
Kind and links: energising. Reiss: curiosity, independence. SDT: autonomy, competence.  
Triggers: free time and materials at hand; or a strong feeling to express (love, grief, anger); or inspiration within
the week; or a gap the person can see ("nobody has made this").  
Likelier / rarer: likelier with high self-direction, early encouragement, earlier flow experiences; rarer with harsh
criticism, no spare time, being watched or graded.  
Stages: child (play), juv, ya, mature and elder (time freed after work).  
Research: Everyday creative activity on one day predicts more energy and flourishing the next (Conner, DeYoung and
Silvia 2018, Journal of Positive Psychology 13(2), 181-189; not re-read).

- paint all weekend | self-direction-thought + hedonism | R/U | =map (R)
- build the furniture for your house | self-direction-thought + security-personal | U/G | =map (U)
- start a band with friends | stimulation + benevolence-caring | R | =map
- carve a toy for your grandchild | benevolence-caring + tradition | G | =map
- [wrong] paint a mural on the railway bridge at night | self-direction-action + stimulation | R | =map (R)

#### 5.4.10 The urge to protect
Kind and links: energising. Reiss: family, honor. Tend-and-befriend.  
Triggers: someone in the person's care threatened within the day (a child, a younger sibling, an old parent, a pet, a
friend); or a small, helpless being nearby; or news of harm to the person's group.  
Likelier / rarer: likelier in parents (most of all of infants) and with high benevolence-caring and security values;
rarer with low empathy or exhaustion.  
Stages: child (younger siblings), adult (parents), mature, elder (grandparents).  
Research: Under threat, caring for the young and drawing close to others is a common response alongside fight or
flight, especially among women (Taylor et al. 2000, Psychological Review 107(3), 411-429; not re-read).

- step between them and the danger | benevolence-caring | G/R | =map (G)
- move the family somewhere safer | security-personal + benevolence-caring | G/W | partial: uprooting for your young reads G
- teach the children to stand up for themselves | security-personal + achievement | R/U | partial: protection by force reads R
- lobby for a crossing outside the school | security-societal + universalism-concern | W | =map
- [wrong] threaten the bully's father | power-dominance + benevolence-caring | R/B | partial: protection by threat reads R

#### 5.4.11 Tenderness and adoration
Kind and links: pleasant. Cowen and Keltner: adoration. Reiss: family, romance.  
Triggers: time with a baby, small child, partner, grandchild or pet; or seeing them asleep, hurt or delighted; or a
reunion after time apart.  
Likelier / rarer: likelier in new parents and grandparents and with high benevolence-caring; rarer with exhaustion or
low mood.  
Stages: adult, mature, elder; also juv (pets, younger siblings).  
Research: Adoration is one of Cowen and Keltner's 27 categories, near romance and sympathy on their map.

- take the afternoon off to be with them | benevolence-caring + hedonism | G/R | =map (G)
- buy them the gift they have been wishing for | benevolence-caring + power-resources | G/B | partial: a loving gift reads G
- write them a letter to read when they are grown | benevolence-dependability + tradition | W/G | =map (W)
- put savings aside in their name | security-personal + benevolence-caring | U/G | =map (U)
- [inner] hold them close and say nothing | benevolence-caring | G | =map (G)

#### 5.4.12 Falling in love
Kind and links: pleasant, energising. Reiss: romance. Cowen and Keltner: romance (sexual desire is a neighbouring
category).  
Triggers: repeated contact over weeks with an attractive, kind, similar person; or a shared adventure or danger; or
learning that the other person likes you back.  
Likelier / rarer: likelier in young adults and once an old heartbreak has healed, with high stimulation and hedonism
values; rarer in a contented partnership, or where the culture forbids the match and conformity is high.  
Stages: juv, ya (peak), adult, elder (late love).  
Research: Romance sits close to adoration and sexual desire on Cowen and Keltner's map; here it is the urge to court
and be near.

- write them a love letter | hedonism + self-direction-thought | R | =map (R)
- rearrange your whole week to see them | hedonism + stimulation | R | =map
- bring them home to meet the family | tradition + benevolence-dependability | W/G | =map (W)
- plan a future together on paper | security-personal + benevolence-dependability | U/W | =map (U)
- [wrong] leave your partner for them within the week | hedonism + self-direction-action | R/B | =map (R)

#### 5.4.13 Excitement and anticipation
Kind and links: pleasant, energising. Cowen and Keltner: excitement.  
Triggers: a looked-forward-to event within 2 weeks (a trip, a wedding, a match, a first day, a birth due); or a new
opportunity opening.  
Likelier / rarer: likelier with high stimulation values; rarer with anxiety or exhaustion.  
Stages: child (birthdays, holidays), juv, ya.  
Research: Excitement is an approach state; it raises spending and planning before the event.

- count down the days and tell everyone | stimulation | R | =map
- prepare every detail in advance | security-personal + achievement | U/W | =map
- spend more than you planned before you even go | hedonism | R/B | =map
- share the plan with the whole family | benevolence-caring | G/W | =map (G)
- lie awake and go for a walk at midnight | stimulation + hedonism | R/G | =map

#### 5.4.14 Joy
Kind and links: pleasant. Cowen and Keltner: joy. Sharing good news.  
Triggers: good news within the day (a birth, a cure, a win, an acceptance, a homecoming); or a long-wanted goal
reached.  
Likelier / rarer: likelier to grow when shared and celebrated; rarer, or soured, among envious listeners.  
Stages: all.  
Research: Telling others about good news raises positive feeling beyond the event itself, most when the listener
responds with active enthusiasm (Gable et al. 2004).

- phone everyone you love | benevolence-caring | G/W | =map (G)
- throw a party | hedonism + stimulation | R | =map
- give thanks at the temple | tradition | W/G | =map (W)
- buy a round for the whole bar | hedonism + benevolence-caring | R/G | =map
- give a gift to someone who has less | universalism-concern | W/G | partial F3

#### 5.4.15 Amusement and playfulness
Kind and links: pleasant. Cowen and Keltner: amusement. Reiss: social contact.  
Triggers: a joke, a game, a silly situation or a funny friend within the day; or free time with peers; or a child at
play nearby.  
Likelier / rarer: likelier with high stimulation and hedonism, in groups, after relief; rarer in formal settings and
under stress.  
Stages: child (peak), juv, and all.  
Research: Amusement is one of the most social of the 27 categories; it spreads in groups.

- play a prank on your brother | stimulation | R | =map
- sign up for the amateur comedy night | stimulation + achievement | R | =map (R)
- play board games with the family every Sunday | benevolence-caring + tradition | G/W | =map
- make the widow laugh at the wake with a story about him | benevolence-caring + conformity-interpersonal | R/W | partial: humour as comfort reads R
- [wrong] mock the teacher behind her back | stimulation + power-dominance | R/B | =map

#### 5.4.16 Admiration
Kind and links: pleasant, energising. Cowen and Keltner: admiration. One of the "other-praising" emotions.  
Triggers: seeing someone show exceptional skill or talent within the week (a teacher, an athlete, a craftsman, a
parent); or meeting a hero.  
Likelier / rarer: likelier with high achievement and self-direction and a belief that skill can grow; rarer when the
admired one is a close rival (it turns to envy) or with cynicism.  
Stages: child (heroes), juv, ya.  
Research: Admiration for skill pushes people to improve and to seek out the admired person; elevation (moral beauty)
pushes toward kindness instead (Algoe and Haidt 2009).

- ask them to take you on as an apprentice | achievement + self-direction-thought | U/W | =map (U)
- practise their move until you have it | achievement | U/B | =map (U)
- collect everything they have made | hedonism | R/G | =map
- tell them how much they mean to you | benevolence-caring | W/G | =map
- join the club they founded | tradition + conformity-interpersonal | W/G | =map

#### 5.4.17 Elevation
Kind and links: pleasant, warm. Moral beauty.  
Triggers: witnessing or hearing of unusual goodness within the day (a stranger's sacrifice, forgiveness of an enemy, a
rescue); or a moving true story.  
Likelier / rarer: likelier with high benevolence and universalism, in religious people; rarer with cynicism.  
Stages: juv, ya, adult, elder.  
Research: Elevation brings warmth in the chest and a wish to be a better person and to help others (Algoe and Haidt
2009). Elevation is White by nature; its responses vary less than most.

- volunteer the next weekend | universalism-concern + benevolence-caring | W/G | =map (W)
- forgive someone you had a grudge against | benevolence-caring + humility | W/G | =map (W)
- give blood | universalism-concern | W | !map F3
- tell the story to your children at dinner | tradition + benevolence-dependability | W/G | =map (W)
- [inner] resolve to live up to that example | benevolence-dependability | W | =map

#### 5.4.18 Compassion
Kind and links: warm, energising. Cowen and Keltner: empathic pain (sympathy tested, merged). Reiss: idealism.  
Triggers: seeing someone suffer within the day (a person sleeping rough, a crying child, a sick neighbour, refugees on
the news), when the suffering seems undeserved and the person can help.  
Likelier / rarer: likelier with high benevolence and universalism, past experience of the same suffering, feeling
secure oneself; rarer when the sufferer is blamed, when victims are many and faceless, under one's own stress.  
Stages: all.  
Research: Compassion is the feeling that arises on seeing another suffer and that moves people to help (Goetz, Keltner
and Simon-Thomas 2010). Spending money on others raised happiness more than spending it on oneself (Dunn, Aknin and
Norton 2008).

- give money on the spot | universalism-concern | G/W | =map
- sit with them and listen | benevolence-caring | G/W | =map (G)
- take the stray dog home | benevolence-caring + universalism-nature | G | =map
- organise a collection at work | universalism-concern + conformity-rules | W | =map
- look away and walk on faster | security-personal | B/U | partial: self-protective avoidance reads B

#### 5.4.19 Aesthetic delight
Kind and links: pleasant. Cowen and Keltner: aesthetic appreciation, entrancement.  
Triggers: beautiful music, art, landscape, craft or a well-made thing within the day; or a museum, concert or garden
visit.  
Likelier / rarer: likelier with openness and training in an art; rarer with hurry and noise.  
Stages: all.  
Research: Aesthetic appreciation lies on Cowen and Keltner's gradient between calmness and awe.

- buy the painting you cannot really afford | hedonism + power-resources | R/B | =map
- plant a garden for its beauty | universalism-nature + hedonism | G | =map (G)
- learn to play the piece yourself | self-direction-thought + achievement | U/R | =map (U)
- campaign to save the old theatre | tradition + universalism-concern | W/G | =map (W)
- take the children to the concert | benevolence-caring + tradition | G/W | =map

#### 5.4.20 Calm and peace
Kind and links: pleasant, low arousal. Cowen and Keltner: calmness. Reiss: tranquility.  
Triggers: time in nature, after prayer or meditation, in a quiet house, after a hard task is finished; or a threat
gone for weeks.  
Likelier / rarer: likelier in safe surroundings and in older age; rarer with high stimulation values, noise, crowding.  
Stages: adult, mature, elder.  
Research: Calm is a state people protect once they have it; its responses keep and repeat rather than change.

- meditate every morning | humility | G/U | =map
- move to the countryside | universalism-nature + security-personal | G | =map (G)
- go on a silent retreat at the monastery | tradition | W/G | =map (W)
- keep the routine exactly as it is | conformity-rules + security-personal | W/U | =map
- [inner] turn down the invitation to protect your quiet evening | security-personal | G/U | partial F7: guarding quiet reads G

#### 5.4.21 Relief
Kind and links: pleasant. Cowen and Keltner: relief.  
Triggers: a feared outcome did not happen, within the day (a clear scan, an acquittal, a child home safe, an exam
passed, a storm that missed).  
Likelier / rarer: stronger after long dread and high stakes.  
Stages: all.  
Research: Relief often brings vows ("never again") and gratitude; the vows fade fast, so the engine can let the old
habit return.

- make a vow to change your life | benevolence-dependability + tradition | W | =map (W)
- celebrate with a big night out | hedonism + stimulation | R | =map
- give thanks at church | tradition | W/G | =map (W)
- call everyone who worried with you | benevolence-caring | G/W | =map (G)
- go straight back to the old ways as if nothing happened | hedonism | R/G | =map

#### 5.4.22 Triumph
Kind and links: pleasant, energising. Cowen and Keltner: tested, merged (near excitement and pride).  
Triggers: beating a rival or overcoming a hard obstacle within the day (a final won, a case won, an election won, a
summit reached).  
Likelier / rarer: likelier with high power, achievement and stimulation; rarer with humility.  
Stages: juv, ya, adult.  
Research: Rivalry raises motivation and effort (Kilduff et al. 2010); a win over a rival invites raising the stakes.

- raise the stakes and aim for the national title | achievement | B/R | =map
- gloat in front of the loser | power-dominance + face | B/R | =map
- shake hands and thank the other side | conformity-interpersonal + benevolence-caring | W | =map
- spend the prize money on a celebration | hedonism | R | =map
- share the credit with the whole team | benevolence-caring + universalism-concern | W/G | =map (W)

#### 5.4.23 Confidence: being on a roll
Kind and links: energising. SDT: competence satisfied. Self-efficacy.  
Triggers: competence high for weeks; or several successes in a row; or praise from a demanding judge.  
Likelier / rarer: likelier after authentic pride, in supportive surroundings; rarer with impostor feelings or a harsh
critic close by.  
Stages: juv, ya, adult.  
Research: The positive counterpart of defeat (5.3.39): success breeds bigger attempts.

- ask for the raise | achievement + power-resources | B | =map
- speak up at the meeting | self-direction-action + achievement | R/B | partial: speaking out reads R
- take a risky bet | stimulation + power-resources | R/B | =map
- help a struggling colleague | benevolence-caring | W/G | =map
- start a new project on the side | self-direction-action + self-direction-thought | R/U | =map (R)

#### 5.4.24 Flow
Kind and links: pleasant, absorbing. Cowen and Keltner: entrancement.  
Triggers: a task with clear goals, quick feedback and challenge matched to skill, lasting an hour or more; repeated
over weeks.  
Likelier / rarer: likelier with a craft, sport, game or instrument already partly mastered; rarer with interruptions
and with tasks far too easy or too hard.  
Stages: juv, ya, adult, mature.  
Research: In flow, attention is fully absorbed, self-consciousness drops and time seems to change speed; people return
to flow activities for their own sake (Csikszentmihalyi 1990). Flow is the opposite of boredom in the MAC model:
attention and meaning both engaged.

- practise every day for hours | achievement + self-direction-thought | U | =map (U)
- turn the hobby into your job | self-direction-action + achievement | U/B | =map (U)
- lose track of time and miss dinner again | hedonism + self-direction-thought | U/R | partial F1
- teach a class in it | benevolence-dependability + achievement | U/W | =map
- build a workshop in the garage | self-direction-thought + security-personal | U/G | =map (U)

#### 5.4.25 Belonging
Kind and links: pleasant. Reiss: social contact, acceptance. SDT: relatedness satisfied.  
Triggers: belonging high for weeks; or a ritual, festival, match or march with a crowd within the week; or being
welcomed into a group (a team, a congregation, a partner's family).  
Likelier / rarer: likelier with high tradition and conformity, team sports, religion; rarer for outsiders and with
high self-direction-action.  
Stages: all; strongest in juv peer groups.  
Research: Belonging answers the need behind loneliness (5.3.1) and feeling invisible (5.3.18).

- wear the colours to every match | tradition + conformity-interpersonal | W/R | =map
- volunteer for the committee | benevolence-dependability + conformity-rules | W | =map
- march with your people at the festival | tradition | G/W | =map
- introduce a newcomer to the group | benevolence-caring + universalism-tolerance | W/G | =map (W)
- [wrong] join in when the group taunts the other side's fans | conformity-interpersonal + power-dominance | R/B | !map: crowd taunting reads R and B

#### 5.4.26 Feeling loved and secure
Kind and links: pleasant, steadying. Attachment: a secure base.  
Triggers: intimacy and belonging high for months; or a partner or parent clearly backing a risky plan; or a
reconciliation.  
Likelier / rarer: likelier with secure attachment and a stable partner; rarer after betrayal and with anxious
attachment.  
Stages: child (with parents), ya, adult, elder.  
Research: A partner who supports one's goals without taking them over makes people explore more and pursue goals more
boldly (Feeney 2004).

- apply for the job abroad you were afraid of | stimulation + achievement | R/B | =map (R)
- start the degree you put off | self-direction-thought | U/R | partial F1
- propose marriage | tradition + benevolence-dependability | W/G | =map (W)
- open up about an old wound | benevolence-dependability | W/G | =map
- give more time to friends and neighbours | benevolence-caring + universalism-concern | G/W | =map

#### 5.4.27 Generativity
Kind and links: energising, slow. Erikson: generativity against stagnation. Reiss: family, idealism.  
Triggers: age about 40-65 with a role toward the young (parent, teacher, boss, aunt or uncle); or someone asks for
advice; or a sense of time running out; or a first grandchild.  
Likelier / rarer: likelier with high benevolence and universalism and with parenthood; rarer with stagnation and
self-absorption.  
Stages: adult, mature (peak), elder.  
Research: Concern for the next generation, measured by the Loyola Generativity Scale, rises into midlife (McAdams and
de St. Aubin 1992).

- mentor a young colleague | benevolence-dependability | W/G | =map
- start an apprenticeship scheme at your firm | achievement + benevolence-dependability | U/W | =map
- write down the family recipes and stories | tradition | G/W | =map
- endow a prize at your old school | universalism-concern + tradition | W/G | =map (W)
- plant an orchard you will not live to harvest | universalism-nature + tradition | G | =map

#### 5.4.28 Purpose and a calling
Kind and links: energising. Reiss: idealism, honor. Work as a calling.  
Triggers: meaning high and tied to one cause for months; or a "call" moment within the year (a sermon, a mentor, a
crisis witnessed); or a skill meeting a need the person cares about.  
Likelier / rarer: likelier with high universalism, benevolence or tradition; rarer when extrinsic goals dominate.  
Stages: juv, ya (when callings form), adult.  
Research: Callings bring meaning and costs: zookeepers who saw their work as a calling accepted lower pay and harder
conditions (Bunderson and Thompson 2009, Administrative Science Quarterly 54(1), 32-57; not re-read). Unanswered
callings stay with people (Berg et al. 2010; section 4).

- take the low-paid job that serves the cause | universalism-concern | W | !map F3
- train as a nurse at forty | benevolence-caring + achievement | W/U | partial: training to serve reads W
- give up your weekends for the work | benevolence-dependability | W | =map
- take holy orders | tradition | W/G | =map (W)
- recruit your friends to the cause | universalism-concern + conformity-interpersonal | W/R | =map

#### 5.4.29 Vitality
Kind and links: energising. Reiss: physical activity. SDT: vitality as a sign of met needs.  
Triggers: health good and rest high for weeks; or recovery from an illness; or a month of regular exercise; or the
first warm days of spring.  
Likelier / rarer: likelier with exercise, sleep and time outdoors; rarer with illness and overwork.  
Stages: child, juv, ya, adult; elder after recovery.  
Research: Vitality is the bodily face of need satisfaction in SDT; it raises the take-up of physical and social
challenges.

- enter a race | achievement + stimulation | R/G | =map (R)
- dig over the whole garden in a day | universalism-nature + hedonism | G/R | =map (G)
- take on extra shifts | achievement + power-resources | B | =map
- dance until dawn | hedonism + stimulation | R | =map
- [inner] decide this is the year you will do everything | self-direction-action + stimulation | R | =map (R)

#### 5.4.30 Attraction and desire
Kind and links: pleasant, energising. Reiss: romance. Cowen and Keltner: sexual desire (category name only; nothing
explicit here).  
Triggers: an attractive person nearby who returns attention; or a long time without intimacy; or a party, a dance,
travel.  
Likelier / rarer: likelier in young adults and with high hedonism and stimulation; rarer with low mood, tiredness, or
where the match is forbidden and conformity is high.  
Stages: juv, ya (peak), adult.  
Research: Sexual desire was among the most intense everyday desires in Hofmann et al. (2012).

- ask them to dance | hedonism + stimulation | R | =map
- dress up and go where they will be | hedonism + face | R/B | =map
- write a poem you never send | self-direction-thought | R/U | =map (R)
- [wrong] cheat on your partner | hedonism | R/B | =map
- [inner] decide to wait and get to know them first | conformity-rules + benevolence-dependability | W/U | =map

#### 5.4.31 Freedom and release
Kind and links: pleasant, energising. Reiss: independence. SDT: autonomy restored.  
Triggers: a long constraint ended within 3 months: graduation, leaving home, a divorce the person wanted, the end of a
caring role, retirement, discharge from the army, the last child leaving, the mortgage paid off.  
Likelier / rarer: likelier with high self-direction and stimulation and after a long constraint; rarer when the ending
was unwanted (then grief or uselessness: 5.3.8, 5.3.30).  
Stages: ya, adult, mature, elder (early retirement).  
Research: Retirement brings little lasting change in well-being for most people; a minority dip and then recover, and
declining health matters more than money (Wang 2007, Journal of Applied Psychology 92(2), 455-474; group sizes not
re-read).

- travel somewhere you have never been | stimulation | R | =map
- take up all the hobbies you postponed | hedonism + self-direction-thought | R/U | =map (R)
- redecorate the house exactly to your own taste | self-direction-action + hedonism | R/G | =map (R)
- throw a farewell party for the old life | hedonism + benevolence-caring | R/G | =map
- sign up to volunteer full time | universalism-concern + benevolence-dependability | W/G | =map (W)

#### 5.4.32 The fresh-start feeling
Kind and links: energising. Temporal landmarks.  
Triggers: New Year, a birthday, a Monday, the first day of a month, season or term; a move, a new job, a recovery; an
age ending in 9 or 0.  
Likelier / rarer: likelier for people with goals they have failed at before; rarer with contentment.  
Stages: all; strongest from juv to adult.  
Research: Aspirational acts (gym visits, diet searches, commitment contracts) rise after temporal landmarks (Dai,
Milkman and Riis 2014; numbers in 5.2).

- join the gym | achievement + security-personal | U/R | =map
- start a strict diet | security-personal | U/W | =map (U)
- write a list of resolutions | achievement + self-direction-thought | U | =map (U)
- clear out the house and give half of it away | humility | G/W | =map
- [inner] forgive yourself for last year | humility + benevolence-caring | W/G | =map (W)

#### 5.4.33 A sense of the sacred
Kind and links: pleasant, deep. Reiss: honor, idealism. Close to awe.  
Triggers: a rite (a wedding, a funeral, a festival), a holy place, prayer, a birth or a deathbed within the week; or
sacred music.  
Likelier / rarer: likelier with high tradition and benevolence; secular people report it too, in nature and art.  
Stages: all; often stronger in elders.  
Research: The sacred is where Tetlock's sacred values (section 4.1) come from: what feels sacred is what people refuse
to trade.

- go to services more often | tradition | W/G | =map (W)
- make a pilgrimage | tradition + stimulation | G/R | =map
- give a tenth of your income | universalism-concern + tradition | W | =map (W)
- study the scriptures every evening | self-direction-thought + tradition | U/W | !map F1: study reads U
- [inner] feel your dead close by and talk to them | tradition + benevolence-caring | G/W | =map

#### 5.4.34 Competitive fire
Kind and links: energising. Reiss: vengeance (in its competing sense), power. Rivalry.  
Triggers: a known rival in the same arena (a classmate, a sibling, a rival firm, the next town's team) after repeated
close contests; or the rival ahead this season.  
Likelier / rarer: likelier with similar rivals, repeated close contests, high achievement and power; rarer where
cooperation is the norm.  
Stages: child (siblings), juv, ya, adult.  
Research: Rivalry is a relationship built from repeated, close contests between similar competitors, and it raises
effort and performance (Kilduff, Elfenbein and Staw 2010).

- train twice as hard this season | achievement | B/U | =map
- study the rival's every move | achievement + self-direction-thought | U/B | =map (U)
- team up with the rival against a bigger threat | power-dominance + security-personal | U/W | =map
- shake hands and buy them a drink afterwards | conformity-interpersonal + benevolence-caring | W/R | =map
- [wrong] tamper with the rival's equipment | power-dominance + achievement | B | =map

#### 5.4.35 Hunger for mastery
Kind and links: energising. SDT: competence. The wish to get good at something.  
Triggers: a skill partly learned, with visible progress for weeks; or a teacher who sets the bar high; or someone
better close by.  
Likelier / rarer: likelier with high achievement and self-direction-thought; rarer with harsh feedback on failure.  
Stages: child (learning to ride or read), juv, ya, adult; elder (new skills).  
Research: Competence is one of the three basic needs; mastery is its active, growing form (Ryan and Deci 2000).

- practise scales every morning | achievement | U | =map (U)
- enter the competition | achievement + stimulation | R/B | =map (R)
- travel to study under a master | self-direction-thought + stimulation | U/R | partial F1
- write the manual so others can learn | benevolence-dependability + achievement | U/W | =map
- make your own tools | self-direction-thought + security-personal | U/G | =map (U)

#### 5.4.36 A friendship spark
Kind and links: pleasant. Reiss: social contact.  
Triggers: repeated meetings with someone of similar interests and humour (a new classmate, a colleague, a neighbour, a
parent at the school gate); or a shared adventure; or a confidence exchanged.  
Likelier / rarer: likelier in child, juv and ya, and in new settings; rarer later in life, when networks narrow to
close ties (Carstensen 2006), and in busy family years.  
Stages: child, juv, ya (peak); elder after a move.  
Research: The answer to loneliness that comes from outside rather than from effort.

- invite them over for dinner | benevolence-caring + hedonism | G/R | =map (G)
- start a project together | stimulation + self-direction-thought | R/U | =map (R)
- introduce them to your other friends | benevolence-caring + universalism-tolerance | W/G | =map (W)
- tell them a secret | benevolence-dependability | W/U | =map
- drop your old friend for the new one | hedonism + stimulation | R/B | =map

#### 5.4.37 A windfall
Kind and links: pleasant, energising. Reiss: saving, power.  
Triggers: an unexpected gain within the month (an inheritance, a bonus, a lottery win, a sale above the asking price);
or income rising well above needs.  
Likelier / rarer: likelier to be spent on oneself with high hedonism and power, given away with high benevolence and
universalism, saved with high security.  
Stages: adult, mature, elder.  
Research: Spending on others raised happiness more than spending on oneself (Dunn, Aknin and Norton 2008).

- pay off the mortgage | security-personal | U/W | =map (U)
- buy the car you always wanted | hedonism + power-resources | B/R | =map (B)
- give a share to your brothers and sisters | benevolence-caring | W/G | =map
- give to a charity | universalism-concern | W | !map F3
- invest it in a new venture | achievement + power-resources | B/U | =map

#### 5.4.38 Thirst for thrill
Kind and links: energising. Reiss: physical activity. Sensation seeking.  
Triggers: stimulation low for weeks; or friends daring the person; or a new risky chance (a motorbike, a cliff, a
casino, a night out); or adolescence itself.  
Likelier / rarer: likelier in late adolescence (sensation seeking peaks in the late teens: Steinberg et al. 2008), in
young men, with peers watching; rarer with age, parenthood, high security values.  
Stages: juv (peak), ya.  
Research: The energising counterpart of boredom (5.3.2).

- jump off the high rocks into the sea | stimulation | R | =map
- take up skydiving with a proper club | stimulation + security-personal | R/U | =map
- bet a month's wages on a horse | stimulation + power-resources | R/B | =map
- join the army for the adventure | stimulation + conformity-rules | R/W | partial: adventure reads R
- [wrong] race cars on the ring road at night | stimulation + power-dominance | R | =map

#### 5.4.39 Pride in another
Kind and links: pleasant. Reiss: family. (Yiddish "naches": pride in one's children.)  
Triggers: a child, grandchild, student or protégé succeeds within the week (graduates, marries, wins, finds work); or
a friend's success the person helped bring about.  
Likelier / rarer: likelier with high benevolence and when the person contributed; rarer when the success leaves the
person behind (then envy: 5.3.3).  
Stages: adult, mature, elder.  
Research: Pride in others is the generative side of pride (5.4.2, 5.4.27).

- tell everyone at the club | face + benevolence-caring | W/B | =map
- throw them a party | hedonism + benevolence-caring | G/R | =map (G)
- give them money for the next step | benevolence-caring + power-resources | G/B | partial: a gift to your own reads G
- push them toward the next, bigger goal | achievement + power-dominance | B | =map
- [inner] feel that your own life was worth it | humility | G/W | =map

#### 5.4.40 Feeling young again
Kind and links: pleasant, energising. Subjective age.  
Triggers: within the month: a new love, a new baby or grandchild, a new skill, a move, recovery from illness, time
spent with young people.  
Likelier / rarer: likelier in good health and with positive views of ageing; rarer with chronic pain.  
Stages: mature, elder.  
Research: The counterpart of feeling old (5.3.17): felt age drops below real age.

- book the adventure holiday | stimulation | R | =map
- take up dancing | hedonism + stimulation | R | =map
- go back to university | self-direction-thought | U | !map F1
- start a new business | self-direction-action + achievement | B/R | =map
- [wrong] spend the savings on a sports car without telling your spouse | hedonism + power-resources | R/B | =map

#### 5.4.41 Acceptance and integrity
Kind and links: pleasant, calm. Erikson: integrity against despair. Life review.  
Triggers: elder stage with a long marriage or a working life completed; or a life review after a diagnosis; or a
reconciliation with an old enemy; or grandchildren thriving.  
Likelier / rarer: likelier when generativity was met, with few unresolved regrets, with faith; rarer with unresolved
grudges and regrets.  
Stages: elder.  
Research: Erikson's last stage: looking back and accepting one's one and only life, against despair. The positivity of
later life (Carstensen 2006) helps.

- make peace with your brother | benevolence-caring + humility | W/G | =map (W)
- give your things away while you are alive | humility + benevolence-caring | G/W | =map
- write your life story for the family | tradition | G/W | =map
- plan your own funeral, calmly | security-personal + humility | U/G | partial: calm planning reads U
- [inner] forgive yourself for what you could not do | humility | G/W | =map

#### 5.4.42 The urge to be alone
Kind and links: pleasant or restorative. Chosen solitude.  
Triggers: rest low and social contact high for days (a family holiday, a busy job, a full house); or after a conflict;
or a creative project waiting.  
Likelier / rarer: likelier with introversion and high self-direction; rarer when lonely. Chosen solitude feels better
than imposed solitude.  
Stages: juv (privacy), adult (parents of small children), elder.  
Research: Time alone lowers high-arousal feelings, good and bad, and raises calm; solitude freely chosen feels better
than solitude imposed (Nguyen, Ryan and Deci 2018).

- go walking alone in the hills | universalism-nature + hedonism | G | =map (G)
- lock the door and read all evening | self-direction-thought + hedonism | U/G | !map F1: solitude with a book reads U
- rent a cabin alone for a week | self-direction-action | B/G | =map
- tell the family plainly you need an evening to yourself | self-direction-action + conformity-interpersonal | W/B | partial: a stated, fair claim reads W
- [inner] stop answering the phone after eight | security-personal | U/B | =map (U)

#### 5.4.43 Wanderlust
Kind and links: energising. Reiss: curiosity, independence.  
Triggers: stimulation low for months; or a travel story or film; or a friend back from abroad; or a fresh-start
landmark; or savings reaching a goal.  
Likelier / rarer: likelier in ya and with high stimulation and self-direction; rarer with small children, a caring
role, high security values.  
Stages: juv, ya (peak), mature (after children leave), elder (early retirement).  
Research: Wanderlust is the pleasant pull toward elsewhere; restlessness (5.3.6) is the painful push away from here.

- buy a one-way ticket | stimulation + self-direction-action | R | =map (R)
- plan a trip a year in advance | stimulation + security-personal | U/R | partial: a planned journey reads U
- take a job abroad | achievement + stimulation | B/R | =map
- learn the language before you go | self-direction-thought | U | !map F1
- walk the old pilgrim route | tradition + stimulation | G/R | =map

#### 5.4.44 Love of place
Kind and links: pleasant, steadying. Reiss: family, tranquility. Attachment to place.  
Triggers: years in one place; family graves nearby; a landscape tied to childhood; coming back after time away; a
threat to the place (a road, a mine, a sale).  
Likelier / rarer: likelier in rural and long-settled families and with high tradition; rarer for people who have moved
often.  
Stages: adult, mature, elder.  
Research: The Green counterpart of wanderlust: the pull to stay, tend and defend.

- turn down the job that means moving | tradition + security-personal | G/W | =map (G)
- join the campaign against the motorway | universalism-nature + tradition | G | =map
- restore the old family house | tradition + achievement | G/U | !map: heritage restored reads G and U; the blend scores White
- write the history of the village | tradition + self-direction-thought | U/G | partial F1: local history reads U
- bring your children back to grow up there | tradition + benevolence-caring | G/W | =map


### 5.5 Bittersweet longings

These mix pleasure and pain; they pull toward something absent. Same format.

#### 5.5.1 Nostalgia
Kind and links: bittersweet, mostly pleasant. Cowen and Keltner: nostalgia.  
Triggers: loneliness, meaninglessness or boredom within the week; or old music, smells, photos, places; or a reunion,
an anniversary, the turn of a year.  
Likelier / rarer: likelier when lonely, at transitions, and in resilient people, who use it to repair; common at all
ages.  
Stages: all; frequent in ya (transitions) and elder.  
Research: Loneliness triggers nostalgia, and nostalgia raises felt social support, most in resilient people (Zhou et
al. 2008); nostalgia also restores a sense of meaning (Routledge et al. 2011).

- call your childhood friend | benevolence-caring | G/W | =map (G)
- organise the class reunion | benevolence-caring + tradition | G/W | =map
- cook the dishes of your childhood | tradition + hedonism | G | =map
- buy back the car you drove at twenty | hedonism + stimulation | R | =map
- [inner] dwell on how much better things used to be | tradition + security-societal | W/G | =map

#### 5.5.2 Longing for a child
Kind and links: bittersweet, energising. Reiss: family. "Baby fever".  
Triggers: age about 25-40; or friends' or siblings' new babies; or holding a baby; or a wedding; or a fertility
deadline coming close; or a partner's wish.  
Likelier / rarer: likelier after positive experiences with children, in women more than men, and with willingness to
give up time, money and freedom for a baby; rarer after negative experiences with children (Brase and Brase 2012).  
Stages: ya, adult.  
Research: The longing for a baby is distinct from sexual desire in both sexes (Brase and Brase 2012; 853 non-student
adults and 337 students). Reminders of death may raise the wish for children (Wisman and Goldenberg 2005, JPSP 89(1),
46-61; not re-read).

- try for a baby | benevolence-caring + tradition | G/W | =map
- start fertility treatment | security-personal + benevolence-caring | U/G | =map (U)
- adopt or foster a child | universalism-concern + benevolence-caring | W/G | =map (W)
- become the favourite aunt or uncle | benevolence-caring | G | =map (G)
- [inner] decide your work will be your legacy instead | achievement | B/U | =map

#### 5.5.3 Longing for love
Kind and links: bittersweet. Reiss: romance.  
Triggers: single for 1+ year with intimacy low; or a friend's wedding; or holidays alone; or couples everywhere.  
Likelier / rarer: likelier in ya and after divorce or widowhood, with high benevolence and hedonism; rarer with a full
social life and contentment with being single.  
Stages: ya, adult, mature, elder.  
Research: Romantic loneliness is a distinct strand of loneliness (5.3.1); it answers to a partner, not to friends.

- ask friends to set you up | benevolence-caring + conformity-interpersonal | W/G | =map
- join a dating site | hedonism + stimulation | R | =map
- go to the dances at the community hall | hedonism + tradition | R/G | =map (R)
- accept the match your family suggests | tradition + conformity-rules | W/G | =map
- [inner] pour the longing into romance novels | hedonism | R/G | =map

#### 5.5.4 Life longing
Kind and links: bittersweet. Sehnsucht: longing for an ideal, unlived life.  
Triggers: reminders of unlived paths (5.3.19); an age ending in 9 or 0; a place or song tied to a dream.  
Likelier / rarer: common across adulthood with small age effects; longings felt as uncontrollable go with lower
well-being, but they also give direction (Scheibe, Freund and Baltes 2007, n = 299, ages 19-81).  
Stages: ya, adult, mature, elder.  
Research: Life longings are recurring thoughts of an ideal life, felt as incomplete, mixing sweet and bitter feeling;
they give direction for development and help people manage goals they cannot reach (Scheibe et al. 2007).

- take one real step toward the dream this year | self-direction-action + achievement | B/R | =map
- live the dream in small doses: sailing at weekends | hedonism + stimulation | R | =map
- write the dream into a novel | self-direction-thought | U/R | partial F1
- help your child live the dream you missed | benevolence-caring | G/W | =map (G)
- [inner] let it stay a dream, and love it as one | humility | G | =map

#### 5.5.5 Need for recognition
Kind and links: mixed, energising. Reiss: status, acceptance. The desire for status.  
Triggers: competence high but status low for months (good work unnoticed); or a colleague credited for the person's
work; or a milestone that passed without praise; or a parent who never praised.  
Likelier / rarer: likelier with high power, achievement and face values; rarer with high humility and intrinsic goals.  
Stages: juv, ya, adult, mature.  
Research: The desire for status (respect, admiration and voluntary deference from others) is a fundamental human
motive, found across cultures and ages (Anderson, Hildreth and Howland 2015).

- ask your boss directly for the credit | achievement + face | B/W | =map (B)
- enter your work for a prize | achievement | B/U | =map
- post your achievements online | face + hedonism | B/R | =map (B)
- take on a leadership role in the community | power-dominance + benevolence-dependability | W/B | partial F5: an office reads W
- [inner] tell yourself the work matters, not the credit | humility | G/W | =map

### 5.6 Count, balance and pattern of flags in section 5

89 drivers: 40 painful or draining (5.3), 44 pleasant or energising (5.4), 5 bittersweet longings (5.5). 445
responses (24 marked `[wrong]`, 35 `[inner]`). Stage mentions (a driver can list several): child 21, juvenile 49,
young adult 53, adult 54, mature 33, elder 41, "all" 19. Flags: `=map` 370 (83%), `partial` 44, `!map` 31.

Every driver named in the brief has an entry: loneliness 5.3.1, boredom 5.3.2, envy 5.3.3, guilt 5.3.4, shame 5.3.5,
restlessness 5.3.6, burnout 5.3.7, grief 5.3.8, meaninglessness 5.3.9, homesickness 5.3.10, fear of death 5.3.11,
anger 5.3.12, craving 5.3.13, feeling trapped 5.3.14, a sense of injustice 5.3.15, jealousy 5.3.16, feeling old
5.3.17, feeling invisible 5.3.18; curiosity 5.4.1, pride 5.4.2, ambition 5.4.3, hope 5.4.4, inspiration 5.4.5, awe
5.4.6, gratitude 5.4.7, contentment 5.4.8, the urge to create 5.4.9, to protect 5.4.10, to be alone 5.4.42; nostalgia
5.5.1, longing for a child 5.5.2, longing for love 5.5.3, need for recognition 5.5.5.

First colors of the responses (my readings), as a rough color profile of each kind of driver:
- painful drivers: W 53, R 41, B 41, U 36, G 29. Painful states spread over all five colors: guilt, shame and
  injustice pull White; anger, heartbreak and feeling controlled pull Red; envy, money worry and self-protection pull
  Black.
- pleasant drivers: R 56, W 56, G 46, U 43, B 19. Pleasant states are rarely answered in Black: only ambition, triumph,
  windfalls and recognition lean that way. Excitement, love, thrill and vitality lead Red; gratitude, elevation and
  compassion lead White; contentment, calm, love of place and generativity lead Green; curiosity, mastery and flow lead
  Blue.
- bittersweet longings lean Green (home, kin, the past).

Where my readings disagree with the map (the same causes as sections 3 and 4):
1. F1 again: curiosity, mastery, inspiration and study responses read Blue and score Black.
2. F3 again: giving, charity, gratitude passed on and elevation read White; universalism scores Green first.
3. Self-protective avoidance (looking away, avoiding the person you wronged, snooping) reads Black while security
   scores White and Blue (section 4.3, point 2).
4. Rest and quiet (sick leave, guarding a calm evening, comfort food) read Green (F7).
5. Blended responses lose their color when loadings are summed (section 4.3, point 1): deliberate repair
   (counselling), restoring a family house, bicultural or heritage acts.

Engine notes:
- Painful drivers mostly fire on deficits that last (weeks or months of low belonging, autonomy, competence, meaning)
  or on a recent loss or threat; pleasant drivers mostly fire on recent events (a win, good news, a beautiful place)
  or on needs met for a long time (contentment, feeling loved, calm). A simulator that only tracks deficits will
  produce only half of these.
- Pleasant drivers should not always be "spent" by an act: gratitude, awe and elevation raise later prosocial acts
  for days, and feeling loved raises exploration for months (Fredrickson 2001; Feeney 2004).
- Several drivers come in pairs that share triggers and differ in valence: restlessness and wanderlust, feeling old
  and feeling young again, defeat and confidence, loneliness and belonging, feeling trapped and freedom, boredom and
  thirst for thrill. The engine can pick between them from the person's resources (money, health, ties): the same
  trigger reads as an opening when resources are high and as a trap when they are low.

## 6. Value change over a life

Sources (read online for this file unless marked "not re-read"):
- Bardi, A., Lee, J. A., Hofmann-Towfigh, N., & Soutar, G. (2009). The structure of intraindividual value change.
  JPSP, 97(5), 913-929. https://pure.royalholloway.ac.uk/files/4416729/VChStructure_LastWordVersion.pdf
- Bardi, A., Buchanan, K. E., Goodwin, R., Slabu, L., & Robinson, M. (2014). Value stability and change during
  self-chosen life transitions: self-selection versus socialization effects. JPSP, 106(1), 131-147.
  https://bura.brunel.ac.uk/bitstream/2438/8395/5/Fulltext.pdf
- Bardi, A. (talk summary). Change in personal values: how, when, what, and effects on well-being.
  https://talks.cam.ac.uk/talk/index/7680/
- Bardi, A., & Goodwin, R. (2011). The dual route to value change: individual processes and cultural moderators.
  Journal of Cross-Cultural Psychology, 42(2), 271-287.
  https://repository.royalholloway.ac.uk/items/476c3e7d-625e-432b-cf15-83f65f388c39/9/Bardi_Goodwin_Value_Change_final.pdf
- Milfont, T. L., Milojev, P., & Sibley, C. G. (2016). Values stability and change in adulthood: a 3-year
  longitudinal study of rank-order stability and mean-level differences. PSPB, 42(5), 572-588.
  https://researchspace.auckland.ac.nz/handle/2292/31537 . (The brief names "Milfont et al. 2010"; the Milfont paper
  on value stability and age I could find is this 2016 one. Milfont's 2010 papers are on environmental values.)
- Vecchione, M., Schwartz, S. H., Alessandri, G., Döring, A. K., Castellani, V., & Caprara, M. G. (2016). Stability
  and change of basic personal values in early adulthood: an 8-year longitudinal study. Journal of Research in
  Personality, 63, 111-122. https://cris.huji.ac.il/en/publications/stability-and-change-of-basic-personal-values-in-early-adulthood-/
- Jin, J. (2010). Stability and change in values: a meta-analysis of longitudinal studies (dissertation, University
  of Illinois). https://www.ideals.illinois.edu/items/16255
- Gouveia, V. V., Vione, K. C., Milfont, T. L., & Fischer, R. (2015). Patterns of value change during the life span:
  some evidence from a functional approach to values. PSPB, 41(9), 1276-1290. Summary read via
  https://www.psychologytoday.com/us/blog/ulterior-motives/201509/how-do-people-s-values-change-they-get-older
- Robinson, O. C. (2013). Values and adult age: findings from two cohorts of the European Social Survey. European
  Journal of Ageing, 10(1), 11-23. https://gala.gre.ac.uk/id/eprint/8968/
- Borg, I., Hertel, G., & Hermann, D. (2017). Age and personal values: similar value circles with shifting
  priorities. Psychology and Aging, 32(7), 636-641 (ESS data). Read via
  https://community.jmp.com/kvoqx44227/attachments/kvoqx44227/jmp-wish-list/5409/1/CORE%20VALUES%20STABILITY%20AGE.pdf
- Schwartz, S. H. (2005). Robustness and fruitfulness of a theory of universals in individual values. In A. Tamayo &
  J. Porto (Eds.), Valores e comportamento nas organizações (pp. 56-95) (not re-read; the age correlations of the
  refined values from Schwartz et al. 2012 are in section 1.2).
- Kandler, C., Gottschling, J., & Spinath, F. M. (2016). Genetic and environmental parent-child transmission of value
  orientations: an extended twin family study. Child Development, 87(1), 270-284.
  https://gwern.net/doc/genetics/heritable/2016-kandler.pdf
- Uzefovsky, F., Döring, A. K., & Knafo-Noam, A. (2016). Values in middle childhood: social and genetic contributions.
  Social Development, 25(3), 482-502. https://cris.huji.ac.il/en/publications/values-in-middle-childhood-social-and-genetic-contributions/
- Daniel, E., Fortuna, K., Thrun, S. K., Cioban, S., & Knafo, A. (2013). Brief report: early adolescents' value
  development at war time. Journal of Adolescence, 36(4), 651-655.
  https://cris.iucc.ac.il/en/publications/brief-report-early-adolescents-value-development-at-war-time/
- Verkasalo, M., Goodwin, R., & Bezmenova, I. (2006). Values following a major terrorist incident: Finnish adolescent
  and student values before and after September 11, 2001. Journal of Applied Social Psychology, 36, 144-160.
  https://bura.brunel.ac.uk/handle/2438/1838
- Sortheix, F. M., Parker, P. D., Lechner, C. M., & Schwartz, S. H. (2019). Changes in young Europeans' values during
  the global financial crisis. Social Psychological and Personality Science, 10(1), 15-25.
  https://jyx.jyu.fi/handle/123456789/56115
- Lönnqvist, J.-E., Jasinskaja-Lahti, I., & Verkasalo, M. (2013). Rebound effect in personal values: Ingrian Finnish
  migrants' values two years after migration. Journal of Cross-Cultural Psychology, 44(7), 1122-1126.
  https://metatoc.com/papers/2571-rebound-effect-in-personal-values-ingrian-finnish-migrants-values-two-years-after-migration
- Parenthood: Lönnqvist, J.-E., Leikas, S., & Verkasalo, M. (2018). Value change in men and women entering
  parenthood: new mothers' value priorities shift towards conservation values. Personality and Individual
  Differences, 120, 47-51 (not re-read; the finding is also summarised, citing a review, in
  https://en.wikipedia.org/wiki/Theory_of_basic_human_values). Asselmann, E., & Specht, J. (2021). Testing the social
  investment principle around childbirth. European Journal of Personality, 35(1), 85-102 (traits, not values).
  https://www.diw.de/de/diw_01.c.796793.de/s_12008.html
- Paloutzian, R. F., Richardson, J. T., & Rambo, L. R. (1999). Religious conversion and personality change. Journal
  of Personality, 67(6), 1047-1079, as summarised in https://pure.uva.nl/ws/files/3671301/27094_UBA002001256_06.pdf
- Arieli, S., Grant, A. M., & Sagiv, L. (2014). Convincing yourself to care about others: an intervention for
  enhancing benevolence values. Journal of Personality, 82(1), 15-24.
  https://cris.huji.ac.il/en/publications/convincing-yourself-to-care-about-others-an-intervention-for-enha/
- Not re-read for this file: Rokeach, M. (1973), The nature of human values (value self-confrontation); Maio, G. R., &
  Olson, J. M. (1998), Values as truisms, JPSP 74(2), 294-311; Hitlin, S. (2003), Values as the core of personal
  identity, Social Psychology Quarterly 66(2), 118-137; Wood, W., & Neal, D. T. (2007), A new look at habits and the
  habit-goal interface, Psychological Review 114(4), 843-863; Tedeschi, R. G., & Calhoun, L. G. (2004),
  Posttraumatic growth, Psychological Inquiry 15(1), 1-18; Inglehart, R. (1997), Modernization and postmodernization
  (scarcity and socialisation hypotheses); Gaunt, R. (2006), Couple similarity and marital satisfaction, Journal of
  Personality 74(5), 1401-1420.

### 6.1 How much values change

- **Values are stable, but not fixed.** Over 3 months to 1 year, test-retest correlations of the ten values ran from
  about .48 to .76 in German adolescents and UK students; over 2 years in Australian adults (mean age 39) they ran
  from .26 to .58 (Bardi et al. 2009). In young Italian adults (aged 20-28 at the start), rank-order stability over
  4-year gaps averaged .69 and then .77, and three quarters of people kept a value hierarchy correlating above .45
  and then .61 with their earlier one (Vecchione et al. 2016). In a New Zealand national sample (n = 3,962, ages
  25-75), value priorities were highly stable over 3 years (Milfont et al. 2016).
- **Stability rises into adulthood.** A meta-analysis of longitudinal studies found rank-order stability rising with
  age and peaking in the later part of emerging adulthood, with emerging adulthood the period of the largest
  normative change (Jin 2010). Milfont et al. (2016) found one exception later in life: among women, the stability of
  conservation values peaked around 50 and fell afterwards.
- **Change follows the circle.** When one value rises, its neighbours rise a little and the values opposite fall
  (Bardi et al. 2009, all four samples). Engine: never change one value alone; spread every change around the circle
  (neighbours move the same way at a fraction of the size, opposites move the other way).
- **Events matter more than birthdays.** In the Australian adult sample, the number of major life events predicted
  overall value change more strongly than age did (Bardi et al. 2009). Values that become useful in a new situation
  gain importance, and well-being follows the new fit only in the long run (Bardi, talk summary).
- **Part of a value profile is inherited.** In a twin-family study, genes accounted for roughly a quarter to two
  fifths of the variation in children's and parents' values (about 26% on average, about 37% after correcting for
  measurement error; achievement and self-transcendence near 47%, hedonism about 12%, security about 0), while
  direct environmental transmission from parent to child was close to zero (Kandler et al. 2016). In 7-year-old
  Israeli twins, three of the four higher-order values were moderately heritable (about 29-47%), while openness to
  change showed no genetic effect and some family-environment effect (about 19%) (Uzefovsky et al. 2016). Engine: a
  newborn's starting values can be drawn partly from the parents' values (genes), with the rest from unique
  experience; "copying" the parents through upbringing alone is weaker than folk belief suggests.

### 6.2 Age patterns

- **The adult pattern.** In European Social Survey data, age correlates positively with tradition (r about .33),
  conformity (.28) and security (.21), and negatively with stimulation (-.33), hedonism (-.26), achievement (-.26)
  and power (-.12); self-transcendence values rise weakly; the circle itself keeps the same shape at every age (Borg,
  Hertel and Hermann 2017). Robinson (2013) found the same: tradition rises most and stimulation falls most with age;
  conservation rises and openness falls; self-enhancement falls; self-transcendence is higher in midlife and old age
  than in young adulthood. These patterns replicated in two ESS rounds (2002 and 2008), in both sexes and in 12
  countries (self-enhancement in Spain the one exception). The refined values (section 1.2, Schwartz et al. 2012)
  add detail: security-societal, conformity-rules, tradition and universalism-nature rise with age (r about .25),
  universalism-concern somewhat (.17); humility, benevolence-caring and security-personal barely move.
- **Rough size, for an engine.** Converting these correlations into a yearly drift (my calculation, assuming age
  spread of about 17 years in the samples and a straight line): the strongest values (tradition, stimulation) move
  by about a fifth of a standard deviation per decade, conformity, hedonism and achievement by about a sixth,
  security by about an eighth, power by about a fourteenth. Over a whole adult life (18 to 80), tradition and
  stimulation shift by somewhat over one standard deviation. Cross-sectional age differences mix ageing with
  generation (older cohorts grew up in poorer, more traditional times), so treat about half of this as ageing and the
  rest as cohort, unless the engine also models history.
- **Childhood and adolescence.** By middle childhood the circle's structure is already present (Uzefovsky et al.
  2016 used a picture-based survey at age 7). Children rank hedonism and stimulation higher than their parents do;
  parents rank self-direction, power and security higher (Kandler et al. 2016). Over 9 months, German 15-year-olds
  rose in power and achievement and fell in benevolence and universalism (Bardi et al. 2009). In the Brazilian life
  span data (ages 12-65), "excitement" values (emotion, pleasure, sexuality) peak in adolescence and then fall, and
  "interaction" values (affection, belonging) are highest in adolescence and early adulthood (Gouveia et al. 2015).
- **Early adulthood.** From the early 20s to the early 30s, conservation, self-transcendence and power rose while
  achievement fell; openness stayed about level (Vecchione et al. 2016). This is the settling-down years: work,
  partners, children.
- **Midlife.** Gouveia et al. (2015) found "promotion" values (power, success) higher in early and late adulthood and
  lower in the middle years, when family duties dominate; "existence" values (health, stability) high early, lower in
  midlife, and a little higher again later. Normative values (tradition, religiosity) kept rising, most for women.
- **Later life.** Milfont et al. (2016): older adults and women give more weight to others' welfare and to
  tradition; younger adults and men to status and power. The later-life shift toward emotionally meaningful goals and
  close ties (section 5.2, Carstensen 2006) fits the rise of benevolence and tradition and the fall of stimulation and
  achievement.
- **Under the engine's map.** Applying the ESS age correlations above to the engine's loadings (my calculation; the
  three values Borg et al. give only as "weak" set to small values), ageing pushes the color profile toward White
  (+4.1) and Green (+2.0), slightly toward Blue (+0.7), and away from Black (-4.0) and Red (-2.9) (units are
  correlation times loading, useful only for direction). So if the engine ages people's values as the surveys show,
  people grow whiter and greener and less black and red with age. The adolescent pattern runs the other way (toward
  Black, Blue and Red; away from White and Green).

### 6.3 What changes values: life events, direction and rough size

Directions are as reported; sizes are rough and in the studies' own terms. "Confidence" is my judgement of how far an
engine can lean on the finding (sample size, design, replication).

| event | direction of change | rough size and time course | evidence | confidence |
|---|---|---|---|---|
| migration | toward the host country's values: in Polish migrants to Britain, self-direction rose and power moved toward British levels; in Ingrian Finnish migrants, universalism and security rose and achievement fell in the first year | multivariate change over 18 months d about .56; the gap to British values shrank from d .31 to .16; in the Finnish sample, changes partly reversed in year two (a rebound) | Bardi et al. 2014 (n = 151); Lönnqvist et al. 2013 (n = 136) | moderate |
| becoming a parent | mothers shift toward conservation (security, conformity, tradition), fathers barely change; trait openness falls after a first birth in both sexes | small; within the first years | Lönnqvist et al. 2018 (not re-read); Asselmann and Specht 2021 (n = 19,875, traits) | moderate for mothers |
| settling into adult life (work, partner, home in the 20s) | conservation, self-transcendence and power rise; achievement falls; openness level | moderate over 8 years | Vecchione et al. 2016 (n = 270) | good |
| marriage | spouses are similar in values mostly from the start (choice of partner); evidence for convergence over the years is weak | little or none | Gaunt 2006 (not re-read) | low |
| university study | strong self-selection (psychology students already higher in benevolence and universalism than business students); scattered, small changes over 3 years; education correlates with self-direction-thought (r about .22) | small causal effect | Bardi et al. 2014 (Study 2); Schwartz et al. 2012 (section 1.2) | moderate |
| entering an occupation (police training) | recruits already higher in conformity and power and lower in self-direction than the population; no measurable change over 9 months | none detected | Bardi et al. 2014 (Study 1, n = 39) | moderate |
| war at home (adolescents under bombing) | tradition, power and security rose; benevolence, universalism, self-direction, stimulation, hedonism and conformity fell; achievement fell, then rose | fast, within weeks | Daniel et al. 2013 (n = 39) | low (small sample) |
| a distant terror attack | security rose the day after, stimulation fell; back near baseline within weeks | small, short | Verkasalo et al. 2006 | moderate |
| economic crisis | among Europeans aged 16-35, security, tradition, benevolence (and a little conformity) rose; hedonism, self-direction and stimulation fell; power and achievement rose where welfare spending is low and fell where it is high | small; over the crisis years (ESS 2002-2014, 16 countries) | Sortheix et al. 2019 | good |
| growing up in affluence or scarcity | growing up secure favours openness and self-expression values over security values (Inglehart's scarcity and socialisation hypotheses) | slow; shows as cohort differences | Inglehart 1997 (not re-read) | low to moderate |
| many life events at once (illness, job loss, bereavement, moves) | more total value change; direction toward whatever the new situation makes useful | life events predicted change more than age did | Bardi et al. 2009 (Study 4); Bardi talk summary | moderate |
| serious illness or trauma (personal) | people often report greater appreciation of life, closer relationships and spiritual change (benevolence, tradition, savouring); acute threat raises security (see war and terror rows) | varies; self-reported growth may overstate change | Tedeschi and Calhoun 2004 (not re-read) | low |
| religious conversion | identity, goals, life story and the way traits are expressed change; basic traits and temperament do not; tradition (and benevolence for most faiths) rises sharply | large for tradition; can be quick | Paloutzian, Richardson and Rambo 1999 | moderate |
| retirement | no direct longitudinal study of values found; women's conservation values become less stable after about 50; the later-life turn to close ties and emotional goals predicts benevolence up, achievement and power down | unknown | Milfont et al. 2016; Carstensen 2006 (section 5) | low |
| widowhood, divorce | no direct study of values found; treat as a major life event (row above), with the direction set by what the new life demands (for example self-direction and security for someone now living alone) | unknown | my suggestion | low |
| deliberate effort | a 30-minute self-persuasion exercise raised benevolence for at least 4 weeks and raised willingness to volunteer; showing people the gap between their values and their ideals (Rokeach's self-confrontation) produced lasting change | small but lasting weeks or more | Arieli, Grant and Sagiv 2014 (n = 142); Rokeach 1973 (not re-read) | moderate |

Under the engine's map, these directions give color shifts (my calculation, equal unit changes for each value
named): war pushes toward White and Blue and away from Black and Red; an economic crisis toward White, Green and
Blue and away from Black and Red; a first year after migration (Ingrian Finnish pattern) toward Green and White and
away from Black; settling into adult life toward White and Green and away from Black and Red; mid-adolescence toward
Black, Blue and Red and away from Green and White.

### 6.4 What resists change: habit, identity and commitment

- **Values as truisms.** Many values are held as obvious truths that people have never had to defend. They are
  rarely challenged, so they rarely move; when people are made to think up reasons for them, they become easier to
  move (Maio and Olson 1998, as discussed by Bardi and Goodwin 2011).
- **Values as identity.** Values sit near the core of the self, and people protect them by reinterpreting or
  forgetting inconsistent information (Bardi and Goodwin 2011; Hitlin 2003). Engine: the higher a value ranks for a
  person, the smaller the effect of a single event on it.
- **People choose settings that fit.** Police recruits, psychology and business students and Polish migrants had all
  self-selected: their values already fitted the new setting before they entered it (Bardi et al. 2014). Chosen
  settings then confirm the values that led there, and the amount of socialisation tracked how many parts of life
  the transition changed: little for a new job, some for university, most for migration. Engine: the biggest value
  change should come from events that change many parts of life at once, or that the person did not choose (war,
  crisis, illness, a forced move); chosen transitions mostly reinforce.
- **Rebound.** Shocks fade. Security rose after a terror attack and returned toward baseline within weeks (Verkasalo
  et al. 2006); migrants' first-year changes partly reversed in the second year (Lönnqvist et al. 2013). Engine: give
  event effects a half-life (weeks for news, a year or two for a move), with a lasting remainder only for events
  that keep the new circumstances in place.
- **Habit.** Habits are triggered by familiar contexts and keep running even when goals change (Wood and Neal 2007).
  So behaviour lags behind value change, and a person can keep acting on a value they no longer hold, until the
  context changes. The reverse is one of the automatic routes to value change: repeated new behaviour in a new
  setting slowly reshapes the value hierarchy (adaptation, in Bardi and Goodwin 2011).
- **Commitment.** Public vows, sunk investments (a degree, a congregation, a marriage, a business) and people who
  depend on the person raise the cost of acting on a changed value. This is my reading of how the research above
  fits together rather than a finding read for this file; it is the reason section 4 dilemmas often end in
  compromise or delay rather than a clean switch.
- **Two routes and culture.** Values change by an automatic route (priming, repeated exposure, adapting to a new
  situation, identifying with a new group) and by an effortful route (reflection, persuasion, noticing a gap between
  acts and values). Persuasion can backfire when people argue back. People in collectivist and hierarchical cultures
  respond more to group identification and authority; people in individualist cultures resist direct persuasion but
  change when they decide to for themselves (Bardi and Goodwin 2011).
- **Age.** Rank-order stability rises from adolescence to a peak in the late twenties and thirties (Jin 2010; Bardi
  et al. 2009; Vecchione et al. 2016), and younger adults change somewhat more than older ones (Bardi, talk summary),
  though Milfont et al. (2016) found women's conservation values becoming less stable after about 50.

### 6.5 Rules an engine could use for value change

These turn the findings above into rules. The numbers are rough suggestions drawn from the studies, not findings.
1. **Yearly drift by stage.** Child and juvenile: hedonism and stimulation high; through the juvenile years power and
   achievement rise and benevolence and universalism fall a little. Young adult into adult: conservation and
   self-transcendence rise, achievement eases. Adult to elder: tradition, conformity and security rise and
   stimulation, hedonism, achievement and power fall, at most about 0.02 standard deviations a year for the
   fastest-moving values (6.2).
2. **Event shocks.** Each event in the table in 6.3 moves the values it names in the given direction: moderate
   shocks (around 0.2 to 0.5 SD) for migration, war at home, religious conversion and, for mothers, a first child;
   small shocks (0.2 SD or less) for the others. Each shock decays with a half-life (weeks for news events, a year or
   two for migration and crisis), leaving a lasting part only while the new circumstances last; conversion and
   parenthood mostly last.
3. **Spread around the circle.** Any change to one value moves its neighbours the same way at about half the size
   and moves the opposite values the other way at about half the size (structure from Bardi et al. 2009; the half is
   my suggestion).
4. **Resistance.** Scale every change by how stable the person's values are: lower in adolescence (test-retest
   about .5 over months), higher by the late twenties (about .7 to .8 over four years). Scale it down further for a
   person's top-ranked values and for values tied to public commitments.
5. **Self-selection.** Let the person's values choose their settings (jobs, partners, places) and let chosen settings
   reinforce those values only slightly; reserve large change for unchosen events and for transitions that change
   many parts of life at once.
6. **Dissonance.** When a person keeps acting against a value (section 5.3.32, inner conflict), either the act stops
   or the value slowly falls; the second is the automatic route of value change.
7. **Inheritance.** Draw a newborn's starting values partly (around a quarter to two fifths) from the parents'
   values, the rest from unique experience; direct "teaching" by upbringing adds little beyond that (Kandler et al.
   2016).
8. **Colors follow values.** Recompute the color profile from the values each year. Under the engine's map, the age
   trends make people whiter and greener and less red and black over a life (6.2); crisis and war push the same
   way faster; adolescence pushes toward Black, Blue and Red.

Gaps found in the research: no direct longitudinal studies of Schwartz values across retirement, widowhood, divorce
or a large windfall in adulthood turned up; those rows in 6.3 are suggestions. Most studies run for months to a few
years; lifelong change is pieced together from cross-sectional age differences, which mix ageing with generation.
