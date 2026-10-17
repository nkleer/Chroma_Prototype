/* ---------------- worker link ---------------- */
let worker = null, ready = false, busy = false, hud = null, selected = null, digitBuf = "", digitTimer = null;
const stick = { bottom: true };
chronEl.addEventListener("scroll", () => { stick.bottom = chronEl.scrollHeight - chronEl.scrollTop - chronEl.clientHeight < 90; });
function send(text) {
  lastSent = text;
  if (!ready || busy) return;
  // Emren 10-07 01:57 (N3): a choice shows at once that it is being lived, and its outcome comes in the same window;
  // "Go on" closes the window before the weeks pass. sentFrom keeps the interlude out of the choice itself.
  const inPlay = hud && hud.mode === "play" && !hud.plan;
  sentFrom = inPlay && hud.cp && (text === "" || /^\d+$/.test(text)) ? "cp" : inPlay && hud.res && (text === "" || ["w", "m", "y", "d"].includes(text)) ? "res" : "";
  hideTip(); busy = true;
  if (sentFrom === "cp") markChoosing(text); else if (sentFrom === "res") closeEv();
  renderTransport(); lockInputs(true);
  worker.postMessage({ cmd: "line", text });
}
let sentFrom = "", choosing = null;
function markChoosing(text) {
  if (evWrap.hidden || !hud.cp) return;
  const o = text === "" ? hud.cp.options.find((x) => x.own) : hud.cp.options.find((x) => String(x.n) === text);
  choosing = { t: performance.now() };
  tableEl.classList.add("choosing");
  tableEl.querySelectorAll(".optdetail").forEach((x) => x.remove());
  tableEl.querySelectorAll(".opt").forEach((b) => b.classList.toggle("chosen", !!o && hud.cp.options[+b.dataset.i] === o));
  const ch = tableEl.querySelector(".opt.chosen"); if (ch) ch.scrollIntoView({ block: "nearest" });
  const f = tableEl.querySelector(".evf"), nm = (hud.life && hud.life.name) || "They";
  if (f) f.innerHTML = `<div class="trying" role="status"><span class="spin"></span><span><b>${esc(nm)}</b> ${text === "" ? "chooses for themselves" : "tries it"}<span class="dots"><i>.</i><i>.</i><i>.</i></span></span><span class="tbar"><i></i></span></div>`;
  const st = $("evStrip"); if (st && o) { st.classList.remove("idle"); st.innerHTML = `<div class="dt">${esc(nm)} ${text === "" ? "chooses for themselves" : "tries it"}: ${esc(cap(o.label))}</div>`; }
  if (ch && !narrow()) flyUp(ch);
}
// v22 next look, the one signature motion: the chosen card rises to the middle of the window with a gold ring, and when
// the outcome comes it turns over to its verdict, then gives way to the outcome window. Honours reduced motion.
const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let flyer = null;
function flyUp(card) {
  dropFlyer();
  if (reducedMotion()) return;
  const r = card.getBoundingClientRect(), box = tableEl.getBoundingClientRect();
  const w = Math.min(380, Math.max(300, r.width)), h = Math.max(r.height, 96);
  const el = document.createElement("div"); el.className = "flyer"; el.setAttribute("aria-hidden", "true");
  el.style.cssText = `left:${r.left}px;top:${r.top}px;width:${r.width}px;height:${r.height}px`;
  el.innerHTML = `<div class="fin"><div class="face front paper"><div class="optlook">${card.innerHTML}</div></div><div class="face back paper"></div></div><span class="fring"></span>`;
  document.body.appendChild(el); flyer = el; card.classList.add("lifted");
  const tx = box.left + box.width / 2 - w / 2, ty = box.top + box.height * 0.42 - h / 2;
  el.animate([{ left: r.left + "px", top: r.top + "px", width: r.width + "px", height: r.height + "px" },
    { left: tx + "px", top: ty + "px", width: w + "px", height: h + "px" }], { duration: 440, easing: "cubic-bezier(.2,.7,.2,1)", fill: "forwards" });
  el.classList.add("up");
}
function flipFlyer(worked, words) {
  const el = flyer; if (!el) return;
  const back = el.querySelector(".back");
  back.innerHTML = `<span class="fseal ${worked ? "ok" : "bad"}">${ic(worked ? "check" : "cross")}</span><b>${esc(words)}</b>`;
  el.classList.add("flip");
  setTimeout(() => { el.classList.add("gone"); setTimeout(() => { if (el.parentNode) el.remove(); if (flyer === el) flyer = null; }, 360); }, 900);
}
function dropFlyer() { if (flyer && flyer.parentNode) flyer.remove(); flyer = null; }
function closeEv() {
  if (evWrap.hidden) return;
  evWrap.classList.add("leaving"); tableEl.classList.remove("choosing");
  setTimeout(() => { evWrap.classList.remove("leaving"); if (busy || !(hud && (hud.cp || hud.res))) { showEv(false); tableEl.innerHTML = ""; lastCpKey = ""; } }, 180);
}
function pause() { if (worker && busy) worker.postMessage({ cmd: "stop" }); if (IL.on) ilFinish(); }
function toast(msg) {
  if (!msg) return;
  toastEl.textContent = msg; toastEl.classList.add("on");
  clearTimeout(toast.t); toast.t = setTimeout(() => toastEl.classList.remove("on"), 2200);
}
function lockInputs(on) { document.querySelectorAll(".tarot, .opt, #pushIt, #evLet, #goOn, .steps4 button, .ch, .tools [data-key]").forEach((b) => { b.disabled = on || b.hasAttribute("data-held") || (b.closest(".steps4") && !!(hud && (hud.cp || hud.mode !== "play"))); }); }

/* ---------------- the chronicle (the story, the main text) ---------------- */
let curYear = null, prologue = null, lastGuild = null, lastBecoming = "";
let ITEMS = [], MARKS = [];
const yearEls = new Map(), WORLD_SEEN = new Map();
const TAG_ICON = { birth: "sprout", start: "voice", choice: "sign", moment: "dot", ordinary: "dot", loss: "candle", death: "candle", crisis: "storm",
  outside: "globe", move: "route", era: "hourglass", read: "scroll", clash: "bolt", rite: "gate", turn: "compass", breakthrough: "burst",
  healed: "sprout", hardened: "shield", trouble: "rain", fortune: "sun", temper: "mask", ledger: "book", note: "dot", goal: "moon", memory: "ci-diary", kin: "ci-birth", hint: "compass",
  lever: "push", far: "ci-letter", body: "pulse", decline: "hourglass", ...GI.tag };   // spheres phase 4: an act on the town; far
                                                  // ties: news through a tie; v22.5: the body's and the mind's turns, a last decline
const KIND_ICON = { career: "case", partner: "heart", children: "child", community: "people", faith: "shrine", ...GI.kind };
const TAG_WORD = { choice: "Your moment", loss: "Loss", death: "Death", crisis: "Crisis", move: "A move", era: "The times", read: "Public life",
  clash: "Clash", rite: "A new stage", turn: "Turning point", breakthrough: "Breakthrough", healed: "Carried through", hardened: "Hardened",
  trouble: "Hard streak", fortune: "Lucky streak", temper: "Temperament", outside: "The world", commitment: "A title", moment: "A moment",
  ordinary: "Everyday", birth: "Birth", kin: "Family", start: "Your voice", note: "Note", hint: "How needs work", goal: "Dreams and plans", role: "Titles and perks",
  lever: "In town", far: "News through a tie", body: "Body and mind", decline: "The last season" };
const MINOR = new Set(["ordinary", "note", "outside", "read", "era", "temper"]);
const isMinor = (it) => MINOR.has(it.tag) || (it.tag === "role" && !it.title);      // a perk's line is a small one; a title's is not
const MARK_PRI = { death: 9, loss: 9, decline: 8, commitment: 8, clash: 7, turn: 7, breakthrough: 7, choice: 6, crisis: 6, move: 5, rite: 5, healed: 4, hardened: 4, goal: 3, trouble: 3, fortune: 3, role: 3, era: 2 };
// titles and perks (Emren 12:05): icons by perk kind and by status; a title of a life domain takes the domain's icon
const PERK_ICON = { skill: "ci-anvil", credential: "ci-diploma", standing: "ci-medal", bond: "ci-handshake", asset: "ci-open-chest" };
const PERK_KIND_WORD = { skill: "A skill", credential: "A credential", standing: "Standing", bond: "A bond", asset: "Something of their own" };
const STATUS_ICON = { graduate: "ci-mortarboard", veteran: "ci-swords", "has killed in war": "ci-swords", widowed: "ci-candle", retiree: "ci-bench",
  homeowner: "ci-key", newcomer: "ci-suitcase", immigrant: "ci-globe", "someone with a record": "ci-gavel", "ex-prisoner": "ci-broken-chain", "in recovery": "ci-sapling",
  divorced: "ci-heartbreak", "eldest child": "ci-domain-family", "carer for a parent": "ci-hand-on-heart", homeless: "ci-box", "out of work": "ci-door-shut",
  "cancer survivor": "ci-domain-health", "left the faith": "ci-door-open", "doctoral graduate": "ci-diploma",
  "first-generation university student": "ci-domain-study", "former foster child": "ci-teddy-bear", "adopted person": "ci-holding-hands", refugee: "ci-tent",
  "asylum applicant": "ci-letter", "naturalised citizen": "ci-flag", "bankruptcy or insolvency in their history": "ci-wallet",
  "on probation or community supervision": "ci-chain", "living in residential care": "ci-elder", "returned migrant": "ci-u-turn", "displaced by a disaster": "ci-storm" };
const roleIconOf = (d) => d.title ? (d.kind === "status" ? STATUS_ICON[d.name] || "ci-shield" : KIND_ICON[d.kind] || "anchor") : PERK_ICON[d.kind] || "star";
const iconFor = (it) => it.tag === "commitment" ? (KIND_ICON[it.kind] || "anchor") : it.tag === "goal" ? (GOAL_ICON[it.kind] || "moon") : it.tag === "role" ? roleIconOf(it) : (TAG_ICON[it.tag] || "dot");
function resetChron() {
  feedEl.innerHTML = ""; curYear = null; prologue = null; lastGuild = null; lastBecoming = ""; ITEMS = []; MARKS = []; yearEls.clear(); WORLD_SEEN.clear(); stick.bottom = true;
}
function foldOld() {
  const yrs = feedEl.querySelectorAll(".yr:not(.prologue)");
  for (let i = 0; i < yrs.length - 4; i++) if (!yrs[i].dataset.user) yrs[i].classList.add("closed");
}
function newYear(it) {
  const sec = document.createElement("section"); sec.className = "yr"; sec.dataset.age = it.age;
  // the year's name (5.5): the guild when it is new; who they are becoming when that is new (else the guild's epithet)
  const cs = labelColors(it.label), fresh = it.guild !== lastGuild, bnew = !!it.becoming && it.becoming !== lastBecoming;
  lastGuild = it.guild; lastBecoming = it.becoming || "";
  const ep = bnew ? it.becoming : fresh ? it.epithet : "";
  // item 6 (the game's lines_tied): the voice did most of the new name, said beside it
  const vh = it.voice_head ? `<span class="ep vh">${ic("voice")}${esc(it.voice_head)}</span>` : "";
  sec.innerHTML = `<div class="yh"><span class="ag"><small>AGE</small>${it.age}</span>${cs.length ? `<span class="gd">${pips(cs)}${fresh || bnew || vh ? `<span>${esc(it.guild)}</span>${ep ? `<span class="ep">${esc(ep)}</span>` : ""}${vh}` : ""}</span>` : ""}<span class="rule"></span><span class="icons"></span><span class="mood"><b style="height:${(3 + 11 * clamp(it.content)).toFixed(1)}px;background:var(--sat)"></b><b style="height:${(3 + 11 * clamp(it.peace)).toFixed(1)}px;background:var(--peace)"></b></span></div><p class="lead" hidden></p><div class="ents"></div>`;
  const head = sec.firstChild;
  setTip(head, () => tipBox(`Age ${it.age} · ${esc(cap(it.stage))}`, it.guild ? `${pips(cs)} ${esc(it.guild)}${it.becoming || it.epithet ? ", " + esc(it.becoming || it.epithet) : ""}` : "Colors still forming", [],
    bars([["Satisfaction", it.content, "var(--sat)", pct(it.content)], ["Peace", it.peace, "var(--peace)", pct(it.peace)]].concat(
      COLORS.map((c, i) => [CNAME[c], it.w[i] / 0.6, `var(--c${c})`, pct(it.w[i])]))) + (it.voice_head ? `<p>${ic("voice")} The voice's pushes did most of this change: ${esc(it.voice_head)}.</p>` : "") +
      `<p>${sec.classList.contains("closed") ? "Click to open the year." : "Click to fold the year."}</p>`));
  head.addEventListener("click", () => { sec.classList.toggle("closed"); sec.dataset.user = "1"; hideTip(); });
  sec._ents = sec.querySelector(".ents"); sec._icons = sec.querySelector(".icons"); sec._lead = sec.querySelector(".lead"); sec._seen = new Set();
  feedEl.appendChild(sec); yearEls.set(it.age, sec);
  foldOld();
  return sec;
}
function addEntry(it) {
  if (it.tag === "year") { if (curYear) { curYear._lead.hidden = false; curYear._lead.innerHTML = rich(it.text); curYear._lead.dataset.i = it._i; } return; }
  if (!curYear && !prologue) {
    prologue = document.createElement("section"); prologue.className = "yr prologue";
    const e = document.createElement("div"); e.className = "ents"; prologue.append(e); prologue._ents = e; feedEl.appendChild(prologue);
  }
  const host = curYear ? curYear._ents : prologue._ents;
  const el = document.createElement("div");
  const name = iconFor(it);
  // v22 next look: the world's news folds into one "In the world" line per year (each piece keeps its own item, for the
  // marks and the life line), and a line already told in the last three years is not told again
  if (it.tag === "world" && /^⟦O:[^⟧|]*\|[^⟧|]*\|1⟧/.test(it.text || "")) {
    const key = String(it.text || "").replace(/⟦[^⟧]*⟧/g, "").replace(/\s+/g, " ").trim().toLowerCase();
    const seen = WORLD_SEEN.get(key);
    if (seen != null && (it.age ?? 0) - seen < 3) return;
    WORLD_SEEN.set(key, it.age ?? 0);
    const sec = curYear || prologue, piece = `<span class="wp" id="it${it._i}" data-i="${it._i}">${rich(it.text)}</span>`;
    if (sec._world) { sec._world.insertAdjacentHTML("beforeend", piece); return; }
    el.className = "en world minor wline"; el.dataset.i = it._i;
    el.innerHTML = `<span class="gut">${ic("ci-newspaper")}</span><span class="wk">In the world</span>${piece}`;
    setTip(el.querySelector(".gut"), () => tipBox(`${ic("ci-newspaper")} In the world`, "The public news of this year: everyone lives through it. What reaches their own life is told on its own line.", [], ""));
    sec._world = el; host.appendChild(el); return;
  }
  el.className = "en " + it.tag + (isMinor(it) ? " minor" : ""); el.dataset.i = it._i; el.id = "it" + it._i;
  if (it.tag === "ledger") { el.textContent = it.text.trim(); host.appendChild(el); return; }
  if (it.tag === "start") { el.textContent = it.text.replace(/=+/g, "").trim(); host.appendChild(el); return; }
  let res = "";
  if (it.tag === "choice") {
    const { means, ends } = splitColors(it.colors);
    const cs = [...new Set(means.concat(ends))];
    el.style.setProperty("--edge", cs.length === 1 ? `var(--c${cs[0]})` : cs.length ? `linear-gradient(180deg, ${cs.map((c) => `var(--c${c})`).join(", ")})` : "var(--gold)");
    res = `<span class="res">${it.pushed ? `${ic("push")} pushed ` : ""}${it.ok ? `<span class="ok">${ic("check")}</span>` : `<span class="bad">${ic("cross")}</span>`}</span>`;
  }
  let chips = "";
  if (it.tag === "choice" && it.res) {
    const r = it.res;
    chips = (r.heart || r.head ? `<span class="tag ${r.heart && r.head ? "head" : r.heart ? "heart" : "head"}">${ic(r.heart && !r.head ? "heart" : "head")}${r.heart && r.head ? "heart and head" : r.heart ? "heart" : "head"}</span>` : "") +
      (r.regret ? `<span class="tag regret">${ic("rain")}regret</span>` : "") + (r.became || []).map((c) => chgChip(c)).join("") +
      (r.closer && r.closer.distance < 0.05 ? `<span class="tag" data-y="1">${pips(lettersOf(r.closer.identity))}closer to ${esc(r.closer.guild)}</span>` : "") +
      (r.lesson ? `<span class="tag" data-n="1">${ic("rune")}</span>` : "");
    chips = chips ? `<div class="rchips">${chips}</div>` : "";
  }
  el.innerHTML = `<span class="gut${name === "dot" ? " nod" : ""}">${ic(name)}</span>${res}${rich(it.text)}${chips}`;
  if (it.tag === "choice" && it.res) el.classList.add("fresh");
  if (chips) {
    el.querySelectorAll("[data-z]").forEach((x) => { const z = x.dataset.z.split("|"); setTip(x, () => changeTip(z[0], +z[1], +z[2])); });
    const ly = el.querySelector("[data-n]"); if (ly) setTip(ly, () => tipBox(`${ic("rune")} How the world works`, rich(it.res.lesson.line), [], LESSON_WHY[it.res.lesson.key] || ""));
    const cy = el.querySelector("[data-y]"); if (cy) setTip(cy, () => tipBox(`${pips(lettersOf(it.res.closer.identity))} Closer to ${esc(it.res.closer.guild)}`, "", [["Still to go", `${(it.res.closer.distance * 100).toFixed(1)} pts`]], ""));
    el.querySelectorAll(".tag.heart, .tag.head").forEach((x) => setTip(x, () => tipBox(`${ic("voice")} Heart and head`, "", [], it.res.heart && it.res.head ? "Heart and head wanted the same thing, and they did it." : it.res.heart ? "They followed the heart over the head." : "They followed the head over the heart.")));
  }
  setTip(el.querySelector(".gut"), () => tipBox(`${ic(name)} ${esc(TAG_WORD[it.tag] || cap(it.tag))}`, it.sit ? esc(cap(it.sit)) : it.tag === "role" ? esc(cap(it.name) + ": " + it.what) : it.kind ? esc(cap(it.kind) + (it.what ? ": " + it.what : "")) : "", [["Age", (it.age ?? 0).toFixed(1)]]));
  host.appendChild(el);
  if (curYear && !isMinor(it) && !curYear._seen.has(name) && curYear._seen.size < 6) {
    curYear._seen.add(name); curYear._icons.insertAdjacentHTML("beforeend", ic(name));
  }
}
function addFeed(items) {
  for (const it of items || []) {
    if (it.tag === "birth") resetChron();
    it._i = ITEMS.length; ITEMS.push(it);
    if (it.tag === "chapter") curYear = newYear(it); else addEntry(it);
    if (MARK_PRI[it.tag] && !(it.tag === "commitment" && it.what === "inherited") && !(it.tag === "role" && !it.title)) MARKS.push(it);
  }
  if (items && items.length && stick.bottom) chronEl.scrollTop = chronEl.scrollHeight;
}
function openYear(age, itemIndex) {
  let sec = yearEls.get(age);
  if (!sec) { const ages = [...yearEls.keys()].filter((a) => a <= age); if (ages.length) sec = yearEls.get(Math.max(...ages)); }
  if (!sec) return;
  sec.classList.remove("closed"); sec.dataset.user = "1";
  const target = itemIndex != null ? document.getElementById("it" + itemIndex) : null;
  (target || sec).scrollIntoView({ block: target ? "center" : "start", behavior: "smooth" });
  sec.classList.remove("flash"); void sec.offsetWidth; sec.classList.add("flash");
  stick.bottom = false;
}

