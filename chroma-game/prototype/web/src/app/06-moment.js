/* ---------------- part 2: the moment and its cards ---------------- */
const STRAIN = { no: 0, low: 1, medium: 2, high: 3 };
const ARROW = { "much worse": ["down", "▼▼"], worse: ["down", "▼"], "about right": ["eq", "●"], better: ["up", "▲"], "much better": ["up", "▲▲"] };
const MISREAD = { hopeful: ["down", "▼"], doubtful: ["up", "▲"], fair: ["eq", "●"] };
const MISREAD_WORD = { hopeful: "they think it likelier than it is", doubtful: "they think it less likely than it is", fair: "they read it about right" };
function shortName(label) {
  let s = cap(String(label).trim());
  const m = s.match(/^(.{10,}?)(,|;| — | - |:| and | until | so that | to see | while )/);
  if (m) s = m[1];
  if (s.length > 30) s = s.slice(0, 29).replace(/\s+\S*$/, "") + "…";
  return s;
}
function frameBG(cs) {
  if (!cs.length) return "linear-gradient(160deg,#5b566a,#2f2c3a)";
  if (cs.length === 1) return `linear-gradient(160deg, ${FRAME[cs[0]][0]}, ${FRAME[cs[0]][1]})`;
  if (cs.length === 2) return `linear-gradient(100deg, ${FRAME[cs[0]][0]}, ${FRAME[cs[0]][1]} 48%, ${FRAME[cs[1]][1]} 52%, ${FRAME[cs[1]][0]})`;
  return "linear-gradient(160deg, #ecd087, #a07a2c 55%, #e0bd6a)";
}
function artBG(cs) {
  if (!cs.length) return "radial-gradient(circle at 50% 60%, #6d6880, #1b1924)";
  if (cs.length === 1) return `radial-gradient(circle at 50% 62%, ${ART[cs[0]][0]} 0%, ${ART[cs[0]][1]} 72%)`;
  return `radial-gradient(circle at 30% 60%, ${ART[cs[0]][0]}cc 0%, transparent 55%), radial-gradient(circle at 72% 45%, ${ART[cs[1]][0]}cc 0%, transparent 55%), linear-gradient(110deg, ${ART[cs[0]][1]}, ${ART[cs[1]][1]})`;
}
function fxHTML(f) {
  const one = (x, cls) => { const k = x.slice(1); return `<span class="${cls}">${x[0] === "+" ? "+" : "−"}${ic(RES_ICON[k] || "dot")}</span>`; };
  const parts = (f.cost || []).map((x) => one(x, "c")).concat((f.win || []).map((x) => one(x, "w")), (f.lose || []).map((x) => one(x, "l")));
  return parts.length ? `<span class="fx">${parts.slice(0, 7).join("")}</span>` : "";
}
function firstThought(s) { const m = String(s || "").match(/⟦t:[^⟧]*⟧\*[^*]*\*⟦\/⟧/); return m ? m[0] : ""; }
const narrow = () => window.matchMedia("(max-width: 640px)").matches;

/* ---------------- the event window (Emren 09:25: a Paradox-style pop-up over the life, options as readable rows) ---------------- */
const evWrap = $("evwrap"), evBack = $("evback");
evBack.className = "evback"; evBack.innerHTML = `${ic("flag")} Back to the moment`;
evBack.addEventListener("click", () => setPeek(false));
function setPeek(on) { evWrap.classList.toggle("peek", on); evBack.hidden = !on || evWrap.hidden; if (on) { hideTip(); waitingCard(); } }
function showEv(on) { if (!on) { evWrap.hidden = true; evBack.hidden = true; evWrap.classList.remove("peek"); placeEv(false); } else evWrap.hidden = false; }
// v22 next look: the outcome window lies over the story column only, so the crest stays in view and its wheel and meters
// move while the result is read (desktop, where the crest is beside the story); the moment window covers the table
function placeEv(atRes) {
  const over = !!atRes && !evWrap.hidden && window.innerWidth > 1040 && !narrow();
  evWrap.classList.toggle("overstage", over);
  if (!over) { evWrap.style.left = evWrap.style.top = evWrap.style.width = evWrap.style.height = ""; return; }
  const r = stageEl.getBoundingClientRect();
  Object.assign(evWrap.style, { left: r.left + "px", top: r.top + "px", width: r.width + "px", height: r.height + "px" });
}
addEventListener("resize", () => { if (!evWrap.hidden && evWrap.classList.contains("overstage")) placeEv(true); });
// while a moment is set aside to look at the life, it waits as a card at the foot of the story (the Back button)
function waitingCard() {
  const cp = hud && hud.cp; if (!cp) { evBack.innerHTML = `${ic("flag")} Back to the moment`; return; }
  const pic = picImg(cp.art);
  evBack.innerHTML = `${pic || `<span class="wg">${ic("flag")}</span>`}<span class="wt"><small>A moment is waiting</small><b>${esc(cap(cp.title))}</b></span><span class="wgo">${ic("flag")} Open the moment</span>`;
}
const ACC_CLS = { "would go with it": "a0", "okay with it": "a1", reluctant: "a2", "against it": "a3", "their own pick": "own" };
const ACC_WORD = { "would go with it": "Would go with it", "okay with it": "Okay with it", reluctant: "Reluctant", "against it": "Against it", "their own pick": "Their own pick" };
const ACC_HELP = { "would go with it": "What they lean to, or close to it: pushed here, it costs them nothing.", "okay with it": "Not their first wish, but they are not against it: pushed here, it costs them nothing.",
  reluctant: "They would rather not: its colors lean against theirs, or they would rather do nothing. Weaker effort, some strain, and a wanting they swallow.", "against it": "It goes against who they are and who they want to be: half-hearted effort, strain, and pent-up wanting that can break through later.",
  "their own pick": "What they lean toward right now. Letting them choose costs nothing." };
const PLATE = { W: "#a88d3c", U: "#2c69b0", B: "#4a3a5e", R: "#b44627", G: "#2d7a46" };
const LIFE_ICON = [[/loss|grief|death/, "candle"], [/love|partner/, "heart"], [/child/, "child"], [/family|home/, "home"], [/work|money|career/, "case"],
  [/school|study|learning|mentor|mind/, "book"], [/friend|community|neighbour|team|choir/, "people"], [/faith|meaning|calling|tradition/, "shrine"],
  [/body|health|aging|sport/, "pulse"], [/nature/, "leaf"], [/conflict|risk|fear/, "bolt"], [/public|era|media/, "globe"], [/inner|identity|memory|passion/, "voice"],
  [/leisure|play|music|making|performing|food|travel/, "star"]];
function artIcon(a) {               // the moment's first life domain the icon set knows, then its tier, then a rough match
  const ds = String((a && a.life) || "").split(",").map((x) => x.trim()).filter(Boolean);
  for (const d of ds) if (GI.domain[d]) return GI.domain[d];
  if (a && GI.tier[a.tier]) return GI.tier[a.tier];
  const s = ds.join(" "); for (const [re, x] of LIFE_ICON) if (re.test(s)) return x; return a && a.recon ? "route" : "sign";
}
// an option's icon: drawn for this very option, else what the act is (a title it starts, money, a mark it leaves), else its color's mana symbol
function optIcon(o, sit) {
  const own = (GI.option[sit] || [])[o.k];
  if (own) return own;
  const t = String(o.tag || "").replace(/[-+][\d.]+$/, "");
  return GI.act[t] || (o.mark && GI.act[o.mark]) || null;
}
// the picture area: the moment's colors and a glyph for its part of life, until the visuals thread's pictures land (chroma-art/)
// the moment's picture (the visuals thread's engravings, chroma-art/game/pictures.json): by situation, then the original of a
// child version, then the first life domain, then the tier; the colors and a glyph show until it loads, or if it is missing
const PICS = __PICS__;
{ const f = $("fab"), u = PICS.texture && PICS.texture.unwritten_future; if (f && u) f.style.backgroundImage = `url("${u}")`; }
// a tribal or magic life shows its own world's tarot card (V The River, VI The Spires) wherever an Earth picture would show:
// the engravings are of the modern Earth (v22 patch, Emren 10-07 21:44 UTC); Earth lives read the pictures as before
const WORLD_CARD = { tribal: "5", magic: "6" };
const worldCard = (L) => { const k = WORLD_CARD[L && L.setting]; return k ? (PICS.tarot && PICS.tarot[k]) || "" : null; };
function picBase(a) {
  const d = String(a.life || "").split(",").map((x) => x.trim()).find((x) => PICS.domain[x]);
  return (d && PICS.domain[d]) || PICS.tier[a.tier] || "";
}
function picFor(a) {
  if (!a) return "";
  const w = worldCard(hud && hud.life); if (w != null) return w;
  return PICS.situation[a.sit] || PICS.situation[a.variant_of] || picBase(a);
}
// PIC_PACKS: picture -> pack. The rarer moments' pictures travel together in pics/pack-<n>.json (picture -> base64; made by
// web/src/build.py and tools/webdir.py) so one published version stays under the artifact's 511 files. A packed picture
// shows its part-of-life picture until its pack has loaded, then swaps in (data-pic keeps its name for the lights).
const PIC_PACKS = __PIC_PACKS__;
const PACKED = new Map(), PACKING = new Map();
function unpack(n) {
  if (PACKING.has(n)) return;
  PACKING.set(n, fetch(`pics/pack-${n}.json`).then((r) => (r.ok ? r.json() : null)).then((pk) => {
    if (!pk) return;
    for (const u in pk) PACKED.set(u, "data:image/webp;base64," + pk[u]);
    document.querySelectorAll("img[data-want]").forEach((img) => {
      const b = PACKED.get(img.dataset.want); if (!b) return;
      const im = img.cloneNode(); im.src = b; im.dataset.pic = img.dataset.want; im.removeAttribute("data-want"); img.replaceWith(im);
    });
  }).catch(() => {}));
}
function picImg(a) {
  const u = picFor(a); if (!u) return "";
  const k = PIC_PACKS[u], img = (src, at) => `<img src="${esc(src)}"${at} alt="" decoding="async" onerror="this.remove()">`;
  if (!k) return img(u, "");
  if (PACKED.has(u)) return img(PACKED.get(u), ` data-pic="${esc(u)}"`);
  unpack(k);
  return img(picBase(a) || PICS.tier.everyday || "", ` data-want="${esc(u)}"`);
}
function evArt(cs, icon, extra = "", a = null) {
  return `<div class="evart" style="--art:${artBG(cs)}"><span class="stars"></span><span class="glyph">${ic(icon)}</span>${picImg(a)}${extra}</div>`;
}
function plate(ends) {
  if (!ends.length) return "#8a8174";
  return ends.length > 1 ? `linear-gradient(135deg, ${PLATE[ends[0]]} 0 50%, ${PLATE[ends[1]]} 50%)` : PLATE[ends[0]];
}
// v22 next look: an option is a compact card in a two-column grid. The icon tile carries the option's colors and its
// number (renumbered on the page in the order shown; the key still sends the engine's own number), the cost in colors sits
// at the top right, felt odds as a small ring gem with ▲/▼ only where reality differs. Badges only for what changes a
// decision: their own pick, the heart's and the head's pick, would rather not, against it, closed by the law or means.
// The rest (needs met, what may follow, perks that help) reads in the strip under the cards; .os keeps it for the phone.
const tileBG = (cs) => { const v = cs.map((c) => `var(--p${c})`); return !v.length ? "#d9cfbd" : v.length === 1 ? v[0] : `linear-gradient(135deg, ${v.map((x, k) => `${x} ${Math.round(k * 100 / (v.length - 1))}%`).join(", ")})`; };
function feltGem(f, cls, arrow) {
  const C = 2 * Math.PI * 6.5, v = clamp(f, 0.01, 0.99);
  return `<span class="gem"><svg viewBox="0 0 16 16" aria-hidden="true"><circle class="g0" cx="8" cy="8" r="6.5"/><circle class="g1" cx="8" cy="8" r="6.5" stroke-dasharray="${(v * C).toFixed(1)} ${C.toFixed(1)}"/></svg><b>${fpct(f)}</b>${arrow && cls !== "eq" ? `<i class="${cls}">${arrow}</i>` : ""}</span>`;
}
// Stakes on the card (the game's stakes switch): what a way changes for good, from the Library's own fields. The person
// its mark touches is a chip ahead of the titles and perks; a closed way's backfire and the risk to life are its "if it fails"
const STAKE_DOWN = new Set(["made an enemy", "refused someone in need", "broke your word"]);
const stakeChips = (sk) => sk.people ? [`<span class="mk2 rb stake ${STAKE_DOWN.has(sk.mark) ? "down" : "up"}">${ic("people")}${esc(sk.people)}</span>`] : [];
const stakeFails = (sk) => [sk.cost, sk.fails, sk.risk].filter(Boolean).join(", and ");
// Bold ways (the game's bold switch): a bold way's chip, and "likelier" or "harder for them" when their own odds sit ten
// points or more from the written chance it feels; what it wins for good is a chip ahead of the rest
const boldChips = (o) => !o.bold ? [] : [`<span class="mk2 bold">${ic("bolt")}bold</span>`].concat(o.bold.fit_say ? [`<span class="mk2 boldfit ${o.bold.fit === "likelier" ? "up" : "down"}">${esc(o.bold.fit_say)}</span>`] : []);
function optRow(o, i, num) {
  const pass = !o.means.length, st = o.status, ends = [...new Set(o.ends)], f = o.follows || {};
  const acc = o.own ? "their own pick" : o.accept || "okay with it";
  const oicon = pass ? null : optIcon(o, (hud && hud.cp && hud.cp.art && hud.cp.art.sit) || "");
  const [cls, arrow] = o.reality ? MISREAD[o.reality.misread] || ["eq", "●"] : ARROW[o.hint] || ["eq", ""];
  const n = num || o.n, cs = actColors(o.means, o.ends);
  const marks = [];
  if (o.own) marks.push(`<span class="mk2 own">${ic("crown")}their own pick</span>`);
  marks.push(...boldChips(o));
  if (o.heart_pick) marks.push(`<span class="mk2 heart">${ic("heart")}heart</span>`);
  if (o.head_pick) marks.push(`<span class="mk2 head">${ic("head")}head</span>`);
  if (o.shadow) marks.push(`<span class="mk2 shd" data-shd="${esc(o.shadow.state)}" data-shi="${esc(o.shadow.icon)}">${ic(o.shadow.icon)}their shadow pulls here</span>`);   // item 2, once seen
  if (!o.own && (acc === "reluctant" || acc === "against it")) marks.push(`<span class="mk2 rel">${acc === "against it" ? "against it" : "would rather not"}</span>`);
  if (st === "out of reach") marks.push(`<span class="mk2 law why">${ic("lock")}${esc(o.why || "out of reach")}</span>`);
  else if (o.needs && o.closed) marks.push(`<span class="mk2 law why">${ic("lock")}${esc(CLOSED_WORD[o.closed] || "closed")}</span>`);
  if (o.lever) marks.push(`<span class="mk2 lever">${ic(o.lever.icon)}${esc(o.lever.name)}</span>`);
  if (o.wcause) marks.push(`<span class="mk2 wcause ${o.wcause.how}" data-wc="${esc(o.wcause.hover)}">${ic(o.wcause.how === "closed" ? "lock" : "globe")}${esc(o.wcause.note)}</span>`);   // WL3
  if (o.seen && o.seen.kind !== "none") marks.push(`<span class="mk2 seen" data-sn="${esc(o.seen.text)}" style="cursor:help;color:var(${o.seen.kind === "wrong" ? "--stress" : o.seen.kind === "seen" ? "--peace" : "--ink2"})">${ic("eye")}${esc(o.seen.word)}</span>`);   // S6
  if (!o.own && Math.abs(o.era || 0) >= 0.3) marks.push(`<span class="mk2 era ${o.era > 0 ? "with" : "against"}">${ic("globe")}${o.era > 0 ? "with the times" : "against the times"}</span>`);   // P3
  const hp = (o.helped || []).find((h) => h.name === o.helped_row);     // a perk that sets this option apart; the strip lists all
  if (hp) marks.push(`<span class="mk2 rb up">${ic(roleIconOf(hp))}${esc(hp.pred)}</span>`);
  const sk = o.at_stake || {}, lasting = stakeChips(sk);   // Stakes on the card: what it changes for good comes first
  if (sk.win) lasting.unshift(`<span class="mk2 rb up stake">${ic("star")}${esc(sk.win)}</span>`);
  for (const x of (o.roles_fx || [])) lasting.push(`<span class="mk2 rb ${x.gain ? "up" : "down"}${x.when === "fail" ? " iffail" : ""}">${ic(roleIconOf(x))}${x.gain ? "+" : "−"} ${esc(x.title ? shortSay(x.say) : x.name)}</span>`);
  marks.push(...lasting.slice(0, hud && hud.cp && hud.cp.stake_card ? 2 : 1));
  if (sk.risk || sk.fails || sk.cost) marks.push(`<span class="mk2 rb down iffail stake">${ic(sk.risk ? "pulse" : "burst")}if it fails: ${esc(sk.risk || sk.cost || sk.fails)}</span>`);
  const bits = [];                                      // the small print, shown on the phone and in the strip
  if (f.needs && f.needs.length) bits.push(`<span>meets ${esc(f.needs.join(" and "))}</span>`);
  for (const x of (f.lift || [])) bits.push(`<span class="up">${ic(NEED_ICON[x.need] || "dot")} ${esc(NEED_LONG[x.need] || x.need)} is ${esc(x.word)}: ${esc(x.lift)}</span>`);
  if (o.commit) bits.push(`<span>${ic(KIND_ICON[o.commit] || "anchor")} could start ${o.commit_say ? esc(o.commit_say) : "a " + esc(o.commit)}</span>`);
  if (o.needs) bits.push(`<span class="why">${ic("lock")} ${esc(o.needs.line)}</span>`);
  if (sk.win) bits.push(`<span class="up">${ic("star")} for good: ${esc(sk.win)}</span>`);
  if (sk.people) bits.push(`<span class="${STAKE_DOWN.has(o.mark) ? "down" : "up"}">${ic("people")} ${esc(sk.people)}</span>`);
  if (sk.risk || sk.fails || sk.cost) bits.push(`<span class="down">if it fails: ${esc(stakeFails(sk))}</span>`);
  if (!pass) bits.push(fxHTML(f));
  if (pass) return `<button class="opt pass onone" data-i="${i}" data-num="${n}" style="--n:${i}" aria-label="${esc(n + ": " + cap(o.label) + ". " + ACC_WORD[acc])}">
    ${ic("hourglass")}<span class="obody"><span class="ot">${esc(cap(o.label))}</span><span class="os"><span>Nothing changes now; wanting and pressure keep building.</span></span></span>
    <span class="acc ${ACC_CLS[acc]}">${o.own ? ic("crown") : ""}${ACC_WORD[acc]}</span><span class="keyn">key ${n}</span></button>`;
  return `<button class="opt${o.own ? " own" : ""}${st === "out of reach" ? " far" : ""}${st === "didn't think of it" ? " ghost" : ""}" data-i="${i}" data-num="${n}" style="--n:${i};--tile:${tileBG(cs)}" aria-label="${esc(n + ": " + cap(o.label) + ". " + ACC_WORD[acc] + ". Feels " + fpct(o.felt))}">
    <span class="oi">${oicon ? ic(oicon) : `<svg class="mana" aria-hidden="true"><use href="#${MANA(ends[0] || cs[0])}"/></svg>`}<span class="no">${n}</span></span>
    <span class="ocost">${pips(cs)}</span>
    <span class="obody"><span class="ot">${esc(cap(o.label))}</span><span class="os">${bits.filter(Boolean).join("")}</span></span>
    <span class="ometa">${marks.join("")}<span class="acc ${ACC_CLS[acc]}">${o.own ? ic("crown") : ""}${ACC_WORD[acc]}</span><span class="odds"><small>feels</small>${feltGem(o.felt, cls, arrow)}</span></span>
  </button>`;
}
// the reading strip: what one option means, filled on hover or focus (it replaces the floating tooltip at a moment)
function stripHTML(o, num) {
  const f = o.follows || {}, acc = o.own ? "their own pick" : o.accept || "okay with it", facts = [];
  const pass = !o.means.length;
  if (!pass) {
    if (o.bold) facts.push(`<span><b>Bold</b> lower odds, and it changes something for good either way${o.bold.fit_say ? `; <span class="${o.bold.fit === "likelier" ? "up" : "down"}">${esc(o.bold.fit_say)}</span>` : ""}</span>`);
    facts.push(`<span><b>Feels</b> ${fpct(o.felt)}${o.reality ? (o.reality.misread !== "fair" ? `, <span class="${o.reality.misread === "hopeful" ? "down" : "up"}">${o.reality.misread === "hopeful" ? "reality is harsher" : "reality is kinder"}</span>` : ", about right") : o.hint ? `, looks ${esc(o.hint)}` : ""}</span>`);
    if (o.base != null) facts.push(`<span><b>Most people</b> ${baseWord(o.base).replace(/^it /, "")}</span>`);
  }
  facts.push(`<span><b>${esc(ACC_WORD[acc])}</b>${o.status === "didn't think of it" ? " · hadn't thought of it" : ""}${acc === "against it" && o.clash && o.clash.length ? ` · ${o.clash.map((c) => CNAME[c]).join(" and ")} against who they are` : ""}</span>`);
  if (o.status === "considered" && !o.own && o.lean != null) facts.push(`<span><b>Their lean</b> ${pct(o.lean)}</span>`);
  if (f.needs && f.needs.length) facts.push(`<span><b>Meets</b> ${esc(f.needs.join(", "))}</span>`);
  if ((f.lift || []).length) facts.push(`<span class="up"><b>Lacking</b> ${f.lift.map((x) => `${esc(NEED_LONG[x.need] || x.need)} at ${pct(x.level)}: ${esc(x.lift)} to satisfaction if it works`).join("; ")}</span>`);
  if (!o.own && !pass && o.rel >= 0.02) facts.push(`<span${o.resent > o.rel + 0.005 ? ' class="down"' : ""}><b>If you push</b> ${o.resent < 0.05 ? "little resentment" : o.resent < 0.3 ? "some resentment" : o.resent < 0.6 ? "resentment: strain and pent-up wanting" : "strong resentment"}${Math.abs(o.trust || 0) >= 0.05 ? ` (${o.trust > 0 ? "they trust you" : "they distrust you"} in these colors)` : ""}; it counts against their own life unless it gives them something they lack</span>`);
  if (f.cost && f.cost.length) facts.push(`<span><b>Costs</b> ${f.cost.map((x) => `${ic(RES_ICON[x.slice(1)] || "dot")}${esc(x.slice(1))}`).join(" ")}</span>`);
  if (!pass) facts.push(`<span><b>If it works</b> ${f.win && f.win.length ? `<span class="up">${f.win.map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`).join(" ")}</span>, ` : ""}toward ${pips(o.ends)}</span>`);
  const sk = o.at_stake || {};                          // Stakes on the card
  if (sk.win) facts.push(`<span><b>For good</b> <span class="up">${esc(sk.win)}</span></span>`);
  if (sk.people) facts.push(`<span><b>For good</b> <span class="${STAKE_DOWN.has(o.mark) ? "down" : "up"}">${esc(sk.people)}</span></span>`);
  if (!pass) facts.push(`<span><b>If it fails</b> <span class="down">${(sk.risk || sk.fails || sk.cost ? [esc(stakeFails(sk))] : []).concat((f.lose || []).map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`), ["strain", "doubt"]).join(", ")}</span></span>`);
  if (o.commit) facts.push(`<span><b>Could start</b> ${ic(KIND_ICON[o.commit] || "anchor")} a ${esc(o.commit)}${f.commit_p ? ` (about ${pct(f.commit_p)})` : ""}</span>`);
  if (o.seen) facts.push(`<span><b>Seen it done</b> ${esc(o.seen.text)}</span>`);   // S6
  if (o.lever) facts.push(`<span class="lever"><b>A push on the world</b> ${ic(o.lever.icon)}${esc(o.lever.what || o.lever.name)}${o.lever.target ? ` (${esc(o.lever.target)})` : ""}</span>`);
  if (o.status === "out of reach") facts.push(`<span class="down"><b>Out of reach</b> ${esc(o.why)}; can be forced, at higher risk</span>`);
  if (o.needs) facts.push(`<span><b>Needs</b> ${esc(o.needs.line)}${o.closed ? `; without it ${CLOSED_WORD[o.closed] || "the world"} stands in the way` : ""}</span>`);
  if ((o.helped || []).length) facts.push(`<span><b>Helped by</b> ${o.helped.map((h) => `${esc(h.pred)}${h.plus ? ` <span class="up">+${h.plus}%</span>` : ""}`).join(", ")}</span>`);
  if ((o.roles_fx || []).length) facts.push(`<span><b>Titles and perks</b> ${o.roles_fx.map((x) => `<span class="${x.gain ? "up" : "down"}">${esc(x.line)}</span>`).join("; ")}</span>`);
  return `<div class="dt"><span class="num">${num}</span> ${esc(cap(o.label))}</div><div class="facts">${facts.join("")}</div><div class="dhelp">${esc(ACC_HELP[acc])}</div>`;
}
function hhBars(o) {
  const why = (side) => ((o.drivers || {})[side] || []).map(([n, v]) => `<span class="${v > 0 ? "up" : "down"}">${v > 0 ? "+" : "−"}</span>${esc(n)}`).join(", ");
  const row = (icon, v, col, w) => `<div class="tipbar"><span style="color:${col}">${ic(icon)}</span><i><b style="width:${(clamp(v / 0.6) * 100).toFixed(0)}%;background:${col}"></b></i><span>${pct(v)}</span></div>${w ? `<div class="muted" style="font-size:var(--fs-1);margin:-1px 0 3px 20px">${w}</div>` : ""}`;
  return row("heart", o.heart, "var(--heart)", why("heart")) + row("head", o.head, "var(--head)", why("head"));
}
function tipOption(o, name, num) {
  const f = o.follows || {}, rows = [], acc = o.own ? "their own pick" : o.accept || "okay with it";
  // no colour or pair is called an enemy (implementation list item 5, chroma-philosophy/enemy-pairs.md): the option goes against who they are
  const against = acc === "against it" && o.clash && o.clash.length ? `<br><span class="down">${o.clash.map((c) => pip(c)).join("")} This goes against who they are</span>` : "";
  rows.push(["How they feel", `<b>${ACC_WORD[acc]}</b>` + (o.status === "didn't think of it" ? " (they hadn't thought of it)" : "") + against]);
  if (o.lever) rows.push(["A push on the world", `${ic(o.lever.icon)} ${esc(o.lever.name)}: ${esc(o.lever.what)}${o.lever.target ? ` (${esc(o.lever.target)})` : ""}`]);
  if (o.means.length) {
    if (o.bold) rows.push(["Bold", `lower odds, and it changes something for good either way${o.bold.fit_say ? `<br><span class="${o.bold.fit === "likelier" ? "up" : "down"}">${esc(o.bold.fit_say)}</span>` : ""}`]);
    rows.push(["Feels", `${fpct(o.felt)} likely to work`]);
    if (o.base != null) rows.push(["For most people", baseWord(o.base)]);
    if (o.reality) rows.push(["Reality, roughly", `works ${esc(o.reality.band)}` + (o.reality.misread !== "fair" ? `<br><span class="${o.reality.misread === "hopeful" ? "down" : "up"}">${MISREAD_WORD[o.reality.misread]}</span>${o.reality.why ? ` (${esc(o.reality.why)})` : ""}` : "")]);
    else rows.push(["Reality", o.hint ? `looks ${o.hint}` : "–"]);
    if (o.heart != null) rows.push(["Heart and head", hhBars(o)]);
    rows.push(["Colors", colorsHTML(o.means, o.ends) + " " + actColors(o.means, o.ends).map((c) => CNAME[c]).join(" and ")]);
  }
  if (o.status === "considered" && !o.own) rows.push(["Their lean", `${pct(o.lean)} likely to pick it themselves`]);
  if (o.seen) rows.push(["Seen it done", esc(o.seen.text)]);   // S6
  if (o.status === "out of reach") rows.push(["Out of reach", `${esc(o.why)}; can be forced, at higher risk`]);
  if (f.needs && f.needs.length) rows.push(["Meets", esc(f.needs.join(", "))]);
  if (f.cost && f.cost.length) rows.push(["Costs", f.cost.map((x) => `${ic(RES_ICON[x.slice(1)] || "dot")} ${esc(x.slice(1))}`).join(" ")]);
  if (f.win && f.win.length) rows.push(["If it works", `<span class="up">${f.win.map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`).join(" ")}</span>, draws them toward ${colorsHTML(o.ends, o.ends)}`]);
  else if (o.means.length) rows.push(["If it works", `draws them toward ${colorsHTML(o.ends, o.ends)}`]);
  const sk = o.at_stake || {};                          // Stakes on the card
  if (sk.win) rows.push(["For good", `<span class="up">${ic("star")} ${esc(sk.win)}</span>`]);
  if (sk.people) rows.push(["For good", `<span class="${STAKE_DOWN.has(o.mark) ? "down" : "up"}">${ic("people")} ${esc(sk.people)}</span>`]);
  if (o.means.length) rows.push(["If it fails", `<span class="down">${(sk.risk || sk.fails || sk.cost ? [esc(stakeFails(sk))] : []).concat((f.lose || []).map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`), ["strain", "doubt in these ways"]).join(", ")}</span>`]);
  if (o.commit) rows.push(["Could start", `${ic(KIND_ICON[o.commit] || "anchor")} a ${esc(o.commit)}` + (f.commit_p ? ` (about ${pct(f.commit_p)})` : "")]);
  if (o.needs) rows.push(["Needs", `${esc(cap(o.needs.line))}` + (o.closed ? `. Without it, ${CLOSED_WORD[o.closed] || "the world"} stands in the way: it can still be tried, at higher risk.` : ".")]);
  if ((o.helped || []).length) rows.push(["Helped by", o.helped.map((h) => `${ic(roleIconOf(h))} ${esc(cap(h.pred))}${h.plus ? ` <span class="up">+${h.plus}%</span>` : ""}`).join("<br>")]);
  if ((o.roles_fx || []).length) rows.push(["Titles and perks", o.roles_fx.map((x) => `<span class="${x.gain ? "up" : "down"}">${ic(roleIconOf(x))}</span> ${esc(x.line)}`).join("<br>")]);
  if (o.heart_pick || o.head_pick) rows.unshift(["Inner voice", (o.heart_pick ? `<span style="color:var(--heart)">${ic("heart")} the heart's pick</span> ` : "") + (o.head_pick ? `<span style="color:var(--head)">${ic("head")} the head's pick</span>` : "")]);
  return tipBox(`<span class="num">${num || o.n}</span> ${esc(cap(o.label))}`, "", rows, esc(ACC_HELP[acc]));
}
let lastArt = null, lastCpKey = "", CPNUM = new Map();
// G1 (B package): "Out of reach, but you could force it" folds into one row until opened; the choice is kept in this
// browser. Folded cards are not drawn at all, so nothing hidden can be hovered, clicked or measured. openOOR(num) opens
// the fold and focuses that card: a number key on a folded card shows it first, and the same key again pushes.
let oorOpen = false; try { oorOpen = localStorage.getItem("chroma.oorOpen") === "1"; } catch (_) {}
let openOOR = null;
function evHead(kick, title, right) { return `<div class="evh"><span class="kick">${kick}</span><h2 id="evTitle">${title}</h2>${right || ""}</div>`; }
function renderTable(h) {
  const cp = h && h.cp, L = h && h.life;
  const atres = !cp && !!(h && h.res) && !busy;
  stageEl.classList.toggle("atcp", (!!cp || atres) && !busy);
  stageEl.classList.toggle("atres", atres);
  if (!atres) feedEl.querySelectorAll(".en.fresh").forEach((x) => x.classList.remove("fresh"));
  if (choosing && busy) return;                       // the choice is being lived: the window keeps it, with its spinner
  if (choosing && atres) {                            // a beat of "trying" before the outcome, so the change reads as one
    const wait = (flyer ? 600 : 520) - (performance.now() - choosing.t);
    if (wait > 0) { clearTimeout(renderTable.t); renderTable.t = setTimeout(() => renderTable(hud), wait); return; }
  }
  const reveal = !!choosing && atres;
  choosing = null; tableEl.classList.remove("choosing");
  if (!reveal) dropFlyer();
  if (atres) return renderResolution(h, reveal);
  if (!cp || busy) { showEv(false); tableEl.innerHTML = ""; selected = null; lastCpKey = ""; return; }
  const key = cp.age + "|" + cp.title;
  if (key === lastCpKey && !evWrap.hidden) return;
  placeEv(false); dropFlyer();
  lastCpKey = key; selected = null; lastArt = cp.art || null;
  const n = cp.stake_word === "very high" ? 3 : cp.stake_word === "high" ? 2 : 1;
  const idx = cp.options.map((o, i) => [o, i]);
  // numbers in the order shown (Do nothing last), so a set-aside option leaves no gap; CPNUM maps them back
  const groups = [["considered", ""], ["didn't think of it", "Ways they haven't thought of"], ["out of reach", "Out of reach, but you could force it"]];
  const order = [];
  const parts = groups.map(([st, title]) => {
    const xs = idx.filter(([o]) => o.status === st && o.means.length).sort((a, b) => a[0].n - b[0].n);
    xs.forEach(([o]) => order.push(o));
    return [title, xs, st];
  });
  const passes = idx.filter(([o]) => !o.means.length);
  passes.forEach(([o]) => order.push(o));
  CPNUM = new Map(order.map((o, k) => [k + 1, o]));
  const numOf = (o) => order.indexOf(o) + 1;
  const cards = (xs) => xs.map(([o, i]) => optRow(o, i, numOf(o))).join("");
  const oorXs = (parts.find((p) => p[2] === "out of reach") || [0, []])[1];
  const nums = (xs) => { const a = numOf(xs[0][0]), b = numOf(xs[xs.length - 1][0]); return a === b ? `key ${a}` : `keys ${a}–${b}`; };
  const rows = parts.map(([title, xs, st]) => !xs.length ? "" : st === "out of reach"
      ? `<button type="button" class="ask sub oorfold" id="evOOR" aria-expanded="${oorOpen}" aria-controls="evOORg">${ic("lock")} ${title} <small>${xs.length} ${xs.length > 1 ? "options" : "option"} · ${nums(xs)}</small><span class="chev" aria-hidden="true">▸</span></button>`
        + `<div class="ogrid oorg" id="evOORg">${oorOpen ? cards(xs) : ""}</div>`
      : (title ? `<div class="ask sub">${title}</div>` : "") + `<div class="ogrid">${cards(xs)}</div>`).join("")
    + passes.map(([o, i]) => optRow(o, i, numOf(o))).join("");
  const pick = cp.options.filter((o) => o.heart_pick || o.head_pick || o.own);
  const cs = [...new Set([].concat(...pick.map((o) => o.ends)))].slice(0, 2);
  const a = cp.art || {}, kick = [`Age ${Math.floor(cp.age)}`, a.tier, String(a.life || "").split(",")[0].trim()].filter(Boolean).map(esc).join(" · ");
  // the inner voice in three short lines: what the heart says, what the head says, what they would do left alone
  const hp = cp.options.find((o) => o.heart_pick), dp = cp.options.find((o) => o.head_pick), op = cp.options.find((o) => o.own);
  const vline = (k, icon, who, o) => o ? `<div class="vline ${k}"><span class="vi">${ic(icon)}</span><span><small>${who}</small><em>${esc(cap(o.label))}</em></span></div>` : "";
  const vlines = cp.voice ? (hp && hp === dp ? vline("hd", "heart", "Heart and head agree", hp) : vline("h", "heart", "The heart says", hp) + vline("d", "head", "The head says", dp)) + vline("o", "crown", `Left alone, ${esc(L.name)} would`, op) : "";
  const asides = cp.voice ? cp.voice.asides.filter((x) => !/⟦j:lean_other⟧/.test(x)) : [];
  tableEl.innerHTML = evHead(`${ic("flag")} ${kick}`, esc(cap(cp.title)),
      `${cp.voice ? tugBar(cp.voice.self_control, "tug") : ""}<span class="stakes">${[1, 2, 3].map((k) => `<span class="${k <= n ? "" : "off"}">${ic("flame")}</span>`).join("")}</span>`) + `
    <div class="evl">${evArt(cs, artIcon(cp.art), "", cp.art)}
      <div class="evtext">
        ${cp.season && cp.season.this_week ? `<p class="seasonnote" id="cpSeason">${ic("gate")} ${cp.season.transform ? "A turning point of this season: this choice can change who they become." : esc(seasonWords(cp.season)) + "."}</p>` : ""}
        ${cp.scene ? `<p class="scene" data-i="cp">${rich(cp.scene)}</p>` : ""}
        ${cp.thread ? `<p class="note thread" id="cpThread" tabindex="0">${ic("link")} ${rich(cp.thread.line)}</p>` : ""}
        ${cp.extra ? `<p class="note">${rich(cp.extra)}</p>` : ""}
        ${cp.thought ? `<p class="note">${rich(cp.thought)}</p>` : ""}
        ${cp.voice ? `<div class="voicebox"><p class="insight">${rich(cp.voice.line)}</p><div class="vlines">${vlines}</div>${asides.map((x) => `<p class="aside">${rich(x)}</p>`).join("")}</div>` : ""}
      </div></div>
    <div class="evr" id="evOpts"><div class="ask">What will ${esc(L.name)} do? <small>${touchUI ? "tap to read · tap again to push" : "hover to read · click or press its number to push"}</small></div>${rows}
      ${touchUI ? "" : `<div class="dstrip idle" id="evStrip" aria-live="polite"><div class="dt">Hover a card to read it here: how sure ${esc(L.name)} feels, what it would meet, what may follow.</div></div>`}</div>
    <div class="evf"><button class="primary" id="evLet">${ic("crown")} Let ${esc(narrow() ? "them" : L.name)} choose</button>
      <span class="lean" id="evLean" role="group" aria-label="Lean toward a color"><small>Lean</small>${COLORS.map((c) => `<button class="ghost lc" data-lc="${c}" aria-label="Lean toward ${CNAME[c]}">${pip(c)}</button>`).join("")}</span>
      <span class="legend"><span><b>Feels</b> how sure ${esc(L.name)} is it will work · ▲ reality kinder · ▼ harsher</span></span>
      <button class="ghost" id="evPeek">${ic("eye")} Look at the life</button></div>`;
  showEv(true); setPeek(false);
  $("evOpts").scrollTop = 0;
  if (cp.voice) setTip($("tug"), () => voiceTip([cp.voice.key, cp.voice.heart_driver, cp.voice.head_driver, cp.voice.self_control]));
  // F5 (item 4): a moment that follows from an earlier pick says so; the hover gives the cause plainly
  if (cp.thread) setTip($("cpThread"), () => tipBox(`${ic("link")} ${cp.thread.key === "seed" ? "A pick comes back" : "A thread of this life"}`, esc(cp.thread.cause), [], "Only this life's own picks are used."));
  setTip(tableEl.querySelector(".stakes"), () => tipBox(`${ic("flame")} Stakes: ${cp.stake_word}`, "How much this moment can change them.", [], ""));
  $("evLet").addEventListener("click", () => send(""));
  tableEl.querySelectorAll("[data-shd]").forEach((el) => setTip(el, () => tipBox(`${ic(el.dataset.shi)} Their shadow pulls here`, "",
    [], `The heart picks this partly from the pull of the ${esc(el.dataset.shd)} side in ${esc(L.name)}: without that pull, the heart would pick another. ${esc(L.name)} has seen this in themselves before.`)));   // item 2
  tableEl.querySelectorAll("[data-wc]").forEach((el) => setTip(el, () => tipBox(`${ic("globe")} ${esc(el.textContent)}`, esc(el.dataset.wc), [], "The world around them, not their own colors.")));   // WL3
  tableEl.querySelectorAll("[data-sn]").forEach((el) => setTip(el, () => tipBox(`${ic("eye")} ${esc(cap(el.textContent))}`, esc(el.dataset.sn), [], "What they have watched the people they know try makes a path feel open, or closed.")));   // S6
  // P3: a light steer tilts their own pick toward a color; it costs only what it changed, less with the times
  tableEl.querySelectorAll("[data-lc]").forEach((b) => {
    const c = b.dataset.lc, e = cp.era, fit = e && e.i >= 0.2 ? lettersOf(e.letters).includes(c) : false;
    b.addEventListener("click", () => send("~" + c));
    setTip(b, () => tipBox(`${pip(c)} Lean toward ${CNAME[c]}`, `They still choose for themselves, but lean toward ${CNAME[c]} ways.`,
      e && e.i >= 0.2 ? [["The times", `${pips(lettersOf(e.letters))} pull ${fit ? "this way: it costs less" : "elsewhere"}`]] : [],
      "If they would have done it anyway, it costs nothing. If it tips them off their own pick, it costs as much of a push as it changed."));
  });
  const own = cp.options.find((o) => o.own); setTip($("evLet"), () => tipBox(`${ic("crown")} Their own choice`, own ? esc(cap(own.label)) : "", [], "They act as they lean, with no cost. Key Enter."));
  $("evPeek").addEventListener("click", () => setPeek(true));
  const strip = $("evStrip"), idleStrip = strip ? strip.innerHTML : "";
  const fill = (o, num) => { if (!strip) return; strip.classList.remove("idle"); strip.innerHTML = stripHTML(o, num); };
  // v22.1: when the mouse leaves a card, the reading goes back to the card that has keyboard focus, or to a card still
  // under the mouse, before it goes idle (v22 closed it even while another card had focus)
  let hov = null;
  const unfill = () => {
    if (!strip || tableEl.classList.contains("choosing")) return;
    const f = document.activeElement;
    if (f && f.classList && f.classList.contains("opt") && tableEl.contains(f)) return fill(cp.options[+f.dataset.i], +f.dataset.num);
    if (hov && hov[2].isConnected) return fill(hov[0], hov[1]);
    strip.classList.add("idle"); strip.innerHTML = idleStrip;
  };
  const bindOpt = (b) => {
    const o = cp.options[+b.dataset.i], num = +b.dataset.num;
    const hl = (on) => hudEl.querySelectorAll(".orb").forEach((x) => x.classList.toggle("hl", on && o.ends.includes(x.dataset.c)));
    b.addEventListener("pointerenter", (e) => { if (e.pointerType !== "touch") { hov = [o, num, b]; hl(true); fill(o, num); } });
    b.addEventListener("pointerleave", () => { if (hov && hov[2] === b) hov = null; hl(false); unfill(); });
    b.addEventListener("focus", () => fill(o, num)); b.addEventListener("blur", () => setTimeout(unfill, 0));   // after focus has landed
    b.addEventListener("click", () => {
      const go = () => send(o.own ? "" : String(o.n));
      if (!touchUI || selected === o.n) return go();
      selected = o.n;
      tableEl.querySelectorAll(".opt").forEach((x) => x.classList.toggle("sel", x === b));
      tableEl.querySelectorAll(".optdetail").forEach((x) => x.remove());
      const d = document.createElement("div"); d.className = "optdetail";
      d.innerHTML = tipOption(o, L.name, num) + `<div class="center" style="margin-top:8px"><button class="primary" id="pushIt">${ic(o.own ? "crown" : "push")} ${o.own ? "Let them choose this" : "Push them to this"}</button></div>`;
      b.after(d); $("pushIt").addEventListener("click", go);
      d.scrollIntoView({ block: "nearest" });
    });
  };
  tableEl.querySelectorAll(".opt").forEach(bindOpt);
  const fold = $("evOOR");
  const setOOR = (on) => {
    const g = $("evOORg"); if (!fold || !g) return;
    const had = g.contains(document.activeElement);
    oorOpen = on; try { localStorage.setItem("chroma.oorOpen", on ? "1" : ""); } catch (_) {}
    fold.setAttribute("aria-expanded", String(on));
    if (hov && g.contains(hov[2])) hov = null;
    g.innerHTML = on ? cards(oorXs) : "";
    g.querySelectorAll(".opt").forEach(bindOpt);
    if (had) fold.focus();
    unfill();
  };
  openOOR = fold ? (num) => { if (!oorOpen) setOOR(true); const b = $("evOORg").querySelector(`.opt[data-num="${num}"]`); if (b) { b.focus({ preventScroll: true }); b.scrollIntoView({ block: "nearest" }); } } : null;
  if (fold) fold.addEventListener("click", () => { setOOR(!oorOpen); if (oorOpen) { const g = $("evOORg"); if (g.lastElementChild) g.lastElementChild.scrollIntoView({ block: "nearest" }); } });
}

const SURPRISE = { better: "better than they expected", "as expected": "as they expected", worse: "worse than they feared" };
function renderResolution(h, reveal) {
  const r = h.res, L = h.life;
  const key = "res|" + r.age + "|" + r.title;
  if (key === lastCpKey && !evWrap.hidden) return;
  tableEl.classList.toggle("reveal", !!reveal); if (reveal) setTimeout(() => tableEl.classList.remove("reveal"), 900);
  lastCpKey = key; selected = null;
  const { means, ends } = splitColors(r.colors);
  const hhs = (r.pushed ? `<span class="tag push">${ic("push")}pushed by you${r.rel >= 0.02 ? ` · they were ${r.rel < 0.3 ? "okay with it" : r.rel < 0.6 ? "reluctant" : "against it"}` : ""}</span>` : "") +
    (r.with_heart ? `<span class="tag heart">${ic("heart")}the heart's choice</span>` : "") + (r.with_head ? `<span class="tag head">${ic("head")}the head's choice</span>` : "") +
    (!r.with_heart && !r.with_head && !r.pushed ? `<span class="tag">${ic("route")}a third way</span>` : "") + (r.regret ? `<span class="tag regret">${ic("rain")}will be regretted</span>` : "");
  const people = (r.people || []).map(castById).filter(Boolean).slice(0, 5).map((p) => `<span class="av${p.alive ? "" : " gone"}" data-pid="${p.id}" style="--ac:${GROUP_COL[ROLE_GROUP[baseRole(p.role)] || "other"]}">${esc(p.name[0])}</span>`).join("");
  const top = (r.became || []).map((c) => c.what);
  const chips = (r.became || []).map((c) => chgChip(c, true)).concat((r.changes || []).filter((c) => !top.includes(c.what) && !c.what.startsWith("color:")).slice(0, 5).map((c) => chgChip(c))).join("");
  const dw = r.dw || [0, 0, 0, 0, 0], mx = Math.max(0.4, ...dw.map(Math.abs));
  const cmove = `<div class="cmove" id="cmove">${COLORS.map((c, i) => { const v = dw[i], hgt = Math.abs(v) / mx * 19; return `<div class="cb"><div class="col"><b style="background:var(--c${c});${v >= 0 ? `bottom:50%;height:${hgt.toFixed(1)}px` : `top:50%;height:${hgt.toFixed(1)}px`}"></b></div>${pip(c)}</div>`; }).join("")}</div>`;
  const cl = r.closer, nowC = lettersOf(r.identity && r.identity.now);
  const toward = cl ? `<div class="toward" id="toward">${pips(nowC.length ? nowC : ["W"])}<span>${ic("push")}</span>${pips(lettersOf(cl.identity))}<div><div class="tw">${esc(cl.guild)}</div><small>${cl.distance < 0.05 ? "a step away" : "on the way"}</small></div><div class="dist"><b style="width:${(clamp(1 - cl.distance / 0.15) * 100).toFixed(0)}%"></b></div></div>` :
    nowC.length ? `<div class="toward" id="toward">${pips(nowC)}<div><div class="tw">${esc(r.identity.guild)}</div><small>their colors now</small></div></div>` : "";
  const les = r.lessons || [];
  const vword = `${r.worked ? "It worked" : "It went badly"}${SURPRISE[r.surprise] ? ", " + SURPRISE[r.surprise] : ""}`;
  tableEl.innerHTML = evHead(`${ic("rune")} What came of it · Age ${Math.floor(r.age)}`, esc(cap(r.act)), colorsHTML(means, ends)) + `
    <div class="evl">${evArt(ends.length ? ends : means, artIcon(lastArt), `<span class="seal2 ${r.worked ? "ok" : "bad"}">${ic(r.worked ? "check" : "cross")}</span>`, lastArt)}
      <div class="evtext">
        <div class="verdict vbig ${r.worked ? "ok" : "bad"}"><span class="sur">${esc(vword)}</span></div>
        ${r.world_push ? `<div class="verdict"><span class="tag${r.world_push.backfire ? " down" : ""}">${ic("ci-crowd")}${esc(r.world_push.target ? cap(r.world_push.target) + ": " : "")}${esc(r.world_push.backfire ? "it backfired" : r.world_push.word)}</span></div>` : ""}
        ${r.long_shot ? `<div class="verdict"><span class="tag lshot">${ic("star")}a long shot${(r.long_shot.tries || 1) > 1 ? `, try ${r.long_shot.tries}` : ""}, ${r.long_shot.made ? "made" : "missed"}: ${esc(odds100(r.long_shot.odds))}</span>${r.long_shot.rung ? ` <span class="tag">${ic("route")}after ${r.long_shot.rung.years <= 1 ? "a year" : r.long_shot.rung.years + " years"} ${/^(a|an|the|one) /.test(r.long_shot.rung.say) ? "as " : ""}${esc(r.long_shot.rung.say)}</span>` : ""}</div>` : ""}
        <div class="verdict">${hhs}</div>
        ${people ? `<div class="verdict"><span class="muted">With</span><span class="with">${people}</span></div>` : ""}
      </div></div>
    <div class="evr"><div class="reso-r">
      <p class="scene" data-i="res">${rich(r.text)}</p>
      ${r.pressure ? `<p class="note pressure">${esc(r.pressure)}</p>` : ""}
      ${r.back ? `<p class="note thread" id="rBack" tabindex="0">${ic("link")} ${rich(r.back.line)}</p>` : ""}
      ${r.rename ? `<div class="rename" id="rename"><span class="k">${ic("quill")} A new name?</span><span>${esc(L.name)} names who they are. They may take a new name, or keep their own.</span>
        <div class="inrow"><input class="field" id="rnTxt" type="text" maxlength="24" autocomplete="off" spellcheck="false" value="${esc(r.rename.suggest)}" aria-label="New name"><button class="primary" id="rnTake">${ic("quill")} Take it</button><button class="ghost" id="rnKeep">Keep ${esc(r.rename.old)}</button></div></div>` : ""}
      ${chips ? `<div class="became">${chips}</div>` : ""}
      ${(r.needs || []).length ? `<div class="ndmove" id="ndmove">${r.needs.slice(0, 4).map((x) => `<div class="r">${ic(NEED_ICON[x.need] || "dot")}<span>${esc(cap(NEED_LONG[x.need] || x.need))}</span><span class="${x.delta > 0 ? "up" : "down"}">${pct(x.before)} → ${pct(x.after)}</span>${x.lacking && x.delta > 0 ? `<small class="muted">was lacking</small>` : ""}</div>`).join("")}</div>` : ""}
      ${r.hindsight && r.hindsight.line ? `<p class="hind ${r.hindsight.kind === "accepted" ? "up" : "down"}" id="hind">${rich(r.hindsight.line)}</p>` : ""}
      <div class="row2 shiftbox">${cmove}${toward}</div>
      ${(r.states || []).length ? `<div class="states">${r.states.map((x) => `<span class="st g${x.what === "gained" ? x.good : 0}${x.what === "gained" ? "" : " gone"}">${ic(x.icon)}${x.what === "gained" ? "Now " : "No longer "}${esc(x.word)}</span>`).join("")}</div>` : ""}
      ${(r.roles || []).length ? `<div class="states">${r.roles.map((x, i) => `<span class="st rl g${x.up ? 1 : 0}${x.up ? "" : " gone"}" data-rr="${i}">${ic(roleIconOf(x))}${esc(x.up && x.title ? "Now " + x.word : cap(x.word))}</span>`).join("")}</div>` : ""}
      ${les.length ? `<div class="lesson">${ic("rune")}<div><span class="k">How the world works</span>${rich(les[0].line)}${les.slice(1, 2).map((x) => `<span class="more">${rich(x.line)}</span>`).join("")}</div></div>` : ""}
    </div></div>
    <div class="evf"><button class="primary" id="goOn">${ic("play")} Go on</button><span class="legend"><span>Hover the changes and colors for the numbers behind them</span></span>
      <button class="ghost" id="evPeek">${ic("eye")} Look at the life</button></div>`;
  showEv(true); setPeek(false); placeEv(true);
  if (reveal && flyer) flipFlyer(r.worked, vword); else dropFlyer();
  $("goOn").addEventListener("click", () => send(""));
  $("evPeek").addEventListener("click", () => setPeek(true));
  if (r.rename) {
    const rn = (v) => { const box = $("rename"); if (box) box.remove(); lastSent = "="; if (!ready || busy) return; worker.postMessage({ cmd: "line", text: "=" + v }); };
    $("rnTake").addEventListener("click", () => rn(($("rnTxt").value || "").trim() || r.rename.suggest));
    $("rnKeep").addEventListener("click", () => rn(r.rename.old));
    $("rnTxt").addEventListener("keydown", (e) => { e.stopPropagation(); if (e.key === "Enter") { e.preventDefault(); $("rnTake").click(); } });
  }
  tableEl.querySelectorAll("[data-z]").forEach((x) => { const z = x.dataset.z.split("|"); setTip(x, () => changeTip(z[0], +z[1], +z[2])); });
  if ($("ndmove")) setTip($("ndmove"), () => tipBox(`${ic("compass")} Needs this week`, "", (r.needs || []).map((x) => [esc(cap(NEED_LONG[x.need] || x.need)), `${pct(x.before)} → ${pct(x.after)} (${sgn(x.delta * 100)} pts)`]), "An act that works feeds the needs its ends serve, and a lacking need lifts satisfaction most. Needs also fade a little every week."));
  if ($("hind")) setTip($("hind"), () => tipBox(`${ic("voice")} Looking back on your push`, "", [["Trust in you, these colors", `${sgn((r.hindsight.trust_before || 0) * 100)} → ${sgn((r.hindsight.trust_after || 0) * 100)}`]],
    r.hindsight.kind === "accepted" ? "It worked and gave them something they lacked, so part of the push's cost is undone: less strain and pent-up wanting, and it counts less against their own life." : "It failed, or gave them nothing they lacked. They hold it against you, and later pushes in these colors cost more."));
  if ($("rBack")) setTip($("rBack"), () => tipBox(`${ic("link")} A pick came back`, esc(r.back.cause), [], "Only this life's own picks are used."));   // Picks come back
  tableEl.querySelectorAll("[data-pid]").forEach((x) => setTip(x, () => personTip(+x.dataset.pid)));
  tableEl.querySelectorAll("[data-rr]").forEach((x) => { const d = r.roles[+x.dataset.rr]; setTip(x, () => roleTip(d, findRole(d.name))); });
  setTip($("cmove"), () => tipBox(`${ic("wheel")} The colors this week`, "", [["Moved", colorMoves(r.dw)]], (r.push || []).map((p) => `${esc(cap(p.why))}: ${p.dir} ${pip(p.color)}`).join("<br>") || "Points are shares of 100."));
  if ($("toward")) setTip($("toward"), () => cl ? tipBox(`${pips(lettersOf(cl.identity))} Moving toward ${esc(cl.guild)}`, "", [["Still to go", `${(cl.distance * 100).toFixed(1)} pts`]], "A color joins above 22% and leaves below 18%; the name follows the colors of the last four years.") : tipBox(`${pips(nowC)} ${esc(r.identity.guild)}`, "", [], "No identity is close to changing this week."));
  tableEl.querySelectorAll(".verdict .tag").forEach((x) => setTip(x, () => tipBox(`${ic("voice")} Heart and head`, "", [], x.classList.contains("push") ? "You chose for them. If they were okay with it, it cost little; the less they wanted it, the more it cost: effort, strain and pent-up wanting." : x.classList.contains("regret") ? "The heart won against the head, and it failed. Regret lingers, and it can bring back what was let go." : "Before the choice, the heart (impulse) and the head (reflection) each had a favourite. This is which one they followed.")));
}

