/* ---------------- the Book of Moments (points 11 and 15; Emren chose "Book and peace", 21:44): what every life met, kept in
   this browser across lives. It records; it does not rank. Rarity: the share of simulated modern Earth lives that meet a
   moment (rarity.py), until the engine and the Library tag real-life frequencies. ---------------- */
// item 3: the sides of the five questions (engine AXES, + side then - side), as the Book's Your Voice page says them
const VOICE_SIDE = [["others", "themselves"], ["safety", "freedom"], ["the head", "the heart"], ["what was meant to be", "their own will"], ["who they already were", "what they could make of themselves"]];
const BOOK_KEY = "chroma.book", CAT_KEY = "chroma.bookcat", BOOK_LIVES = 80;
const emptyBook = () => ({ v: 1, lives: {}, order: [], seen: {} });
let book = (() => { try { const b = JSON.parse(localStorage.getItem(BOOK_KEY) || "null"); if (b && b.v === 1 && b.seen && b.lives) return b; } catch (_) {} return emptyBook(); })();
let bookCat = (() => { try { return JSON.parse(localStorage.getItem(CAT_KEY) || "{}") || {}; } catch (_) { return {}; } })();
const catMaps = {};
function storeBook() { try { localStorage.setItem(BOOK_KEY, JSON.stringify(book)); } catch (_) {} }
function takeCat(c) { bookCat[c.world] = c; delete catMaps[c.world]; try { localStorage.setItem(CAT_KEY, JSON.stringify(bookCat)); } catch (_) {} }
const worldOf = (setting) => setting === "earth" ? "earth" : "base";
function catMap(world) {
  if (catMaps[world]) return catMaps[world];
  const c = bookCat[world]; if (!c) return null;
  const m = {};
  for (const [k, dom, tier, sh] of c.moments) m[k] = { name: k.slice(2), dom, tier, sh };
  for (const [n, sh] of c.deeds) m["d|" + n] = { name: n, sh };
  for (const [n, say, kind, sh] of c.titles) m["t|" + n] = { name: say, kind, sh };
  return (catMaps[world] = m);
}
function bookInfo(k) { for (const w of ["earth", "base"]) { const m = catMap(w); if (m && m[k]) return m[k]; } return null; }
// one life's record from the game: merged by its id, so a replayed or reloaded life never counts twice
function bookMerge(r) {
  if (!r || !r.id) return;
  const keys = [...(r.moments || []), ...(r.deeds || []).map((x) => "d|" + x), ...(r.titles || []).map((x) => "t|" + x),
    ...(r.idents || []).map((x) => "i|" + x), ...(r.long || []).map((x) => "l|" + x), "w|" + r.setting];
  let L = book.lives[r.id];
  if (!L) { L = book.lives[r.id] = { k: [], when: Date.now() }; book.order.push(r.id); }
  const had = new Set(L.k || []);
  for (const k of keys) if (!had.has(k)) { had.add(k); const s = book.seen[k] || (book.seen[k] = { n: 0, first: r.id }); s.n++; }
  Object.assign(L, { name: r.name, setting: r.setting, start: r.start, age: r.age, over: !!r.over, k: [...had] });
  if (r.final !== undefined) L.final = r.final;
  if (r.reading) L.reading = r.reading.words;
  if (r.voice) L.voice = r.voice;
  if (r.returns) L.returns = r.returns;   // Picks come back: a pick and the moment it came back as
  for (const id of book.order.slice(0, Math.max(0, book.order.length - BOOK_LIVES))) if (book.lives[id]) delete book.lives[id].k;   // counts stay
  storeBook();
}
const firstHere = (id) => Object.entries(book.seen).filter(([, s]) => s.first === id).map(([k]) => k);
function rareWord(sh) {
  if (sh == null) return "";
  if (sh === 0) return `not met in ${((bookCat.earth || {}).lives || 0).toLocaleString()} simulated lives`;
  return sh >= 0.5 ? "most lives meet it" : sh >= 0.2 ? "many lives meet it" : `about 1 life in ${Math.round(1 / sh)}`;
}
const isRare = (sh) => sh != null && sh < 0.1;
const STAR_DEEDS = new Set(["came out", "named their gender"]);   // N1d §5: rare moments of a life, starred like the others
const isStar = (k, i) => (k.startsWith("d|") ? STAR_DEEDS.has(k.slice(2)) : false) || !!(i && isRare(i.sh));
const momentName = (k) => cap(k.slice(2));
const bookDef = { moments: "A moment counts once a life meets it: a situation the story tells, or a life event.",
  rare: "Moments that fewer than 1 in 10 simulated modern Earth lives meet, from birth to 80, across the four Earth starts.",
  deeds: "Things a life did at least once, as the engine marks them: kept a word, made an enemy, came home.",
  titles: "Every title or status a life has held, even for a week.",
  long: "A title reached for when it works for fewer than 1 in 10 people. Made or missed, each is kept: the trying is part of the life.", idents: "The 31 combinations of colors a life can be, under Chroma's own names. A life is one while its colors stay above 22%." };
const bookEl = document.createElement("div"); bookEl.className = "help sheetwrap"; bookEl.hidden = true; document.body.appendChild(bookEl);
bookEl.addEventListener("click", (e) => { if (e.target === bookEl) closeBook(); });
function closeBook() { bookEl.hidden = true; bookEl.innerHTML = ""; hideTip(); }
function openBook() {
  hideTip(); closeHud(); closeSheet();
  const S = book.seen, has = (k) => !!(S[k] && S[k].n);
  const lives = book.order.map((id) => [id, book.lives[id]]).filter(([, L]) => L);
  const E_ = catMap("earth"), B_ = catMap("base");
  const count = (m, pre) => m ? Object.keys(m).filter((k) => pre.includes(k[0] + "|")) : [];
  const eMom = count(E_, ["s|", "e|"]), bMom = count(B_, ["s|", "e|"]).filter((k) => !E_ || !E_[k]);
  const deeds = [...new Set([...count(E_, ["d|"]), ...count(B_, ["d|"])])], titles = count(E_, ["t|"]);
  const ID_ = ((bookCat.earth || bookCat.base || {}).idents) || {}, idents = Object.entries(ID_).map(([l, v]) => [l, v[0]]);
  const met = (ks) => ks.filter(has).length;
  // G3 (B package): one count of moments. The Book's count is the situations the story tells plus the life events, and
  // says so, so it agrees with the situation count elsewhere (822 situations and 59 life events: 881 moments)
  const momDef = (ks) => { const s_ = ks.filter((k) => k.startsWith("s|")).length; return `${bookDef.moments} Here: ${s_} situations and ${ks.length - s_} life events.`; };
  const stat = (n, of, label, def) => `<div class="bst" data-def="${esc(def || "")}"><b>${n}</b>${of != null ? `<span class="of">of ${of}</span>` : ""}<span class="bl">${label}</span></div>`;
  // rare moments met, rarest first
  const rare = Object.keys(S).filter((k) => /^[sed]\|/.test(k) && S[k].n).map((k) => [k, bookInfo(k)]).filter(([k, i]) => i && (k.startsWith("d|") ? STAR_DEEDS.has(k.slice(2)) : isRare(i.sh))).sort((a, b) => (a[1].sh ?? 1) - (b[1].sh ?? 1));
  const rareRows = rare.slice(0, 40).map(([k, i]) => { const f = book.lives[S[k].first]; return `<div class="brow"><span class="bn">${ic("star")} ${esc(momentName(k))}</span><span class="muted">${esc(rareWord(i.sh))}${f ? ` · first: ${esc(f.name)}` : ""}</span></div>`; }).join("")
    + (rare.length > 40 ? `<div class="muted">and ${rare.length - 40} more</div>` : "");
  const unmetRare = eMom.filter((k) => !has(k) && isRare(E_[k].sh)).length;
  const longK = Object.keys(S).filter((k) => k.startsWith("l|") && S[k].n).sort((a, b) => S[b].n - S[a].n);
  const longRows = longK.slice(0, 20).map((k) => { const [, how, nm] = k.split("|"), i = bookInfo("t|" + nm), f = book.lives[S[k].first];
    return `<div class="brow"><span class="bn">${ic("star")} ${how === "made" ? "Made it" : "Missed"}: ${esc(shortSay((i && i.name) || nm))}</span><span class="muted">${S[k].n === 1 ? "once" : S[k].n + " lives"}${f ? ` · first: ${esc(f.name)}` : ""}</span></div>`; }).join("");
  // moments by part of life (modern Earth)
  const doms = {};
  for (const k of eMom) { const d = E_[k].dom || "life"; (doms[d] = doms[d] || [0, 0])[1]++; if (has(k)) doms[d][0]++; }
  const big = Object.entries(doms).filter(([, v]) => v[1] >= 6).sort((a, b) => b[1][1] - a[1][1]), small = Object.entries(doms).filter(([, v]) => v[1] < 6);
  if (small.length) big.push(["other", small.reduce((t, [, v]) => [t[0] + v[0], t[1] + v[1]], [0, 0]), small.map(([d]) => d)]);
  const domRows = big.map(([d, [a, n], parts]) => meterRow(esc(cap(d)), a / n, `${a} of ${n}`, "var(--gold)", parts ? "Smaller parts of life together: " + parts.join(", ") + "." : "")).join("");
  const identGrid = idents.map(([l, nm]) => `<span class="bid${has("i|" + l) ? " on" : ""}" data-l="${l}">${pips(lettersOf(l))}<span>${esc(nm)}</span>${has("i|" + l) ? `<span class="bn2">${S["i|" + l].n}</span>` : ""}</span>`).join("");
  const deedChips = deeds.map((k) => `<span class="chip bdeed${has(k) ? " on" : ""}">${STAR_DEEDS.has(k.slice(2)) ? ic("star") : ""}${esc(cap(k.slice(2)))}${has(k) ? ` <b>${S[k].n}</b>` : ""}</span>`).join("");
  const heldT = titles.filter(has).map((k) => E_[k]).sort((a, b) => (a.sh ?? 1) - (b.sh ?? 1));
  const titleChips = heldT.map((i) => `<span class="chip${isRare(i.sh) ? " rare" : ""}" data-tip="${esc(cap(i.kind || "") + (i.sh != null ? " · " + rareWord(i.sh) : ""))}">${isRare(i.sh) ? ic("star") : ""}${esc(cap(shortSay(i.name)))}</span>`).join("") || `<span class="empty">None yet</span>`;
  const lifeRows = lives.slice().reverse().slice(0, 30).map(([id, L]) => { const nw = firstHere(id).filter((k) => /^[se]\|/.test(k)).length;
    const fin = L.final != null ? (((bookCat[worldOf(L.setting)] || {}).idents || {})[L.final] || ["Still forming"])[0] : "";
    return `<div class="brow blife"><span class="bn"><b>${esc(L.name || "")}</b><span class="muted">${esc(SETTING_NAME[L.setting] || "")} · ${Math.floor(L.start || 0)} to ${Math.floor(L.age || 0)}${L.over ? "" : ", living"}${fin ? " · " + esc(fin) : ""}</span></span>${L.reading ? `<span class="rd">${esc(L.reading)}</span>` : ""}${nw ? `<span class="muted">${nw} moment${nw === 1 ? "" : "s"} first met in this life</span>` : ""}</div>`; }).join("");
  // item 3: Your Voice, the player's pushes across lives (the ten sides of the five questions), and one line per life
  const vl = lives.filter(([, L]) => L.voice && L.voice.n), vs = vl.reduce((t, [, L]) => { t.n += L.voice.n; t.steer += L.voice.steer; L.voice.ax.forEach((x, i) => { t.ax[i] += x; }); return t; }, { n: 0, steer: 0, ax: [0, 0, 0, 0, 0] });
  const vi = vs.ax.reduce((b, x, i) => Math.abs(x) > Math.abs(vs.ax[b]) ? i : b, 0), vside = VOICE_SIDE[vi][vs.ax[vi] > 0 ? 0 : 1];
  const voiceSum = !vl.length ? "" : !vs.steer ? `In ${vl.length === 1 ? "one life" : vl.length + " lives"} you have let them choose every time.` :
    `Across ${vl.length === 1 ? "one life" : vl.length + " lives"} you pushed in ${vs.steer} of ${vs.n} moments, most often for ${vside}.`;
  const voiceRows = vl.slice().reverse().filter(([, L]) => L.voice.line).slice(0, 12).map(([, L]) => `<div class="brow"><span class="bn">${esc(L.voice.line)}</span></div>`).join("");
  const backRows = lives.slice().reverse().flatMap(([, L]) => (L.returns || []).map((x) => [L.name, x])).slice(0, 12).map(([nm, x]) =>
    `<div class="brow"><span class="bn">${ic("link")} At ${Math.floor(x.a)}, “${esc(x.m)}”; at ${Math.floor(x.b)}, “${esc(x.n)}”</span><span class="muted">${esc(nm || "")}</span></div>`).join("");
  const worlds = ["earth", "tribal", "magic"].map((w) => `<span class="chip${has("w|" + w) ? " on" : " off"}">${ic(SETTING_ICON[w] || "globe")}${esc(SETTING_NAME[w] || w)}${has("w|" + w) ? ` <b>${S["w|" + w].n}</b>` : ""}</span>`).join("");
  bookEl.hidden = false;
  bookEl.innerHTML = `<div class="box paper sheet bookp" role="dialog" aria-label="The Book of Moments">
    <div class="shh"><div class="bhd">${ic("ci-bookshelf")}<div><div class="shn">The Book of Moments</div><div class="muted">${lives.length ? `What ${lives.length === 1 ? "one life has" : lives.length + " lives have"} met, kept in this browser.` : "What your lives meet is kept here, in this browser."} It records; it does not rank.</div></div></div>
      <button class="ghost" id="bkClose" aria-label="Close">${ic("x")}</button></div>
    ${lives.length ? `<div class="bstats">${stat(lives.length, null, lives.length === 1 ? "life" : "lives")}${stat(met(eMom), eMom.length, "moments, modern Earth", momDef(eMom))}${bMom.length ? stat(met(bMom), bMom.length, "moments, tribal and magic", momDef(bMom)) : ""}${stat(rare.length, rare.length + unmetRare, "rare moments", bookDef.rare)}${longK.length ? stat(longK.length, null, "long shots", bookDef.long) : ""}${stat(met(deeds), deeds.length, "deeds", bookDef.deeds)}${titles.length ? stat(met(titles), titles.length, "titles", bookDef.titles) : ""}${stat(met(idents.map(([l]) => "i|" + l)), idents.length, "identities", bookDef.idents)}</div>
    <div class="shg">
      <section><h4>Rare moments met</h4>${rareRows || `<span class="empty">None yet. ${unmetRare} wait somewhere in a life.</span>`}<h4>Long shots</h4>${longRows || `<span class="empty">None yet. Any title can be reached for against long odds; a miss is kept here too.</span>`}<h4>Lives</h4>${lifeRows}<h4>Worlds</h4><div class="perks">${worlds}</div></section>
      <section>${voiceSum ? `<h4>Your Voice</h4><p class="muted bvoice">${esc(voiceSum)}</p>${voiceRows}` : ""}${backRows ? `<h4>Picks that came back</h4>${backRows}` : ""}<h4>Identities lived</h4><div class="bids">${identGrid}</div><h4>Deeds</h4><div class="perks">${deedChips}</div></section>
      <section><h4>Moments by part of life</h4><div class="mts">${domRows}</div><h4>Titles held</h4><div class="perks">${titleChips}</div></section>
    </div>` : `<p class="bempty">Nothing yet. Every life you play writes into this book: the moments it meets, the people it becomes, the titles it holds. Rare moments are marked with a star.</p>`}</div>`;
  bookEl.querySelectorAll("[data-def]").forEach((el) => { if (el.dataset.def) setTip(el, () => tipBox(esc(el.querySelector(".bl").textContent), "", [], esc(el.dataset.def))); });
  bookEl.querySelectorAll("[data-tip]").forEach((el) => setTip(el, () => tipBox(esc(el.textContent), "", [], esc(el.dataset.tip))));
  bookEl.querySelectorAll(".bid").forEach((el) => setTip(el, () => { const l = el.dataset.l, s = S["i|" + l]; return tipBox(`${pips(lettersOf(l))} ${esc(el.textContent.replace(/\d+$/, ""))}`, esc((ID_[l] || [])[1] || ""), s ? [["Lives", String(s.n)], ["First", esc((book.lives[s.first] || {}).name || "")]] : [], s ? "" : "No life has been this yet."); }));
  $("bkClose").addEventListener("click", closeBook);
}

