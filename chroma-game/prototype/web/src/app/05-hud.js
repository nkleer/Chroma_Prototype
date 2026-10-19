/* ---------------- part 3: the character HUD ---------------- */
/* ---------------- point 7 (Emren 20:39): the spider graph. Where they are, where they want to be, what holds them, how fast
   they could move, and the edge of who they are (a color joins above 22%, leaves below 18%) ---------------- */
const SPA = [-90, -18, 54, 126, 198].map((a) => a * Math.PI / 180);
const SPR = 64, SPX = 100, SPY = 100;
const spRad = (v) => SPR * Math.sqrt(clamp(v, 0, 0.8) / 0.8);
const spAt = (i, r) => [SPX + r * Math.cos(SPA[i]), SPY + r * Math.sin(SPA[i])];
const spPts = (vs) => vs.map((v, i) => spAt(i, spRad(v)).map((x) => x.toFixed(1)).join(",")).join(" ");
const f1 = (p) => p.map((x) => x.toFixed(1)).join(",");
const circ = (r) => `M${(SPX - r).toFixed(1)} ${SPY}a${r.toFixed(1)} ${r.toFixed(1)} 0 1 0 ${(2 * r).toFixed(1)} 0a${r.toFixed(1)} ${r.toFixed(1)} 0 1 0 ${(-2 * r).toFixed(1)} 0`;
// o: {w, want, hold, acc, rule, id, hits, labels}; every array is the five colors W U B R G
function spiderSVG(o) {
  const id = o.id || "sp", w = o.w, P = w.map((v, i) => spAt(i, spRad(v)));
  let s = `<defs>${COLORS.map((c, i) => { const a = P[i], b = P[(i + 1) % 5]; return `<linearGradient id="${id}g${i}" gradientUnits="userSpaceOnUse" x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}"><stop offset="0" stop-color="var(--c${c})"/><stop offset="1" stop-color="var(--c${COLORS[(i + 1) % 5]})"/></linearGradient>`; }).join("")}</defs>`;
  for (const v of [0.4, 0.8]) s += `<polygon class="ring" points="${spPts([v, v, v, v, v])}"/>`;
  COLORS.forEach((_, i) => { const e = spAt(i, SPR); s += `<line class="ax" x1="${SPX}" y1="${SPY}" x2="${e[0].toFixed(1)}" y2="${e[1].toFixed(1)}"/>`; });
  const [enter, leave] = o.rule || [0.22, 0.18];
  s += `<path class="band" fill-rule="evenodd" d="${circ(spRad(enter))}${circ(spRad(leave))}"/>`;
  let fan = "";
  COLORS.forEach((_, i) => { const a = P[i], b = P[(i + 1) % 5]; fan += `<path d="M${SPX} ${SPY}L${a[0].toFixed(1)} ${a[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}Z" fill="url(#${id}g${i})"/>`; });
  s += `<g class="fan">${fan}</g>`;
  if (o.shadow) {   // item 2, light and shadow: the end of a colour's point, as far in as its shadow part, cut off and inked
    let sh = "";    // with the visuals thread's hatch mask (ci-hatch; crosshatch while the state shows). The cap is the
    o.shadow.forEach((x, i) => {   // polygon's tip cut square to the axis at (1 - s) of the point's length: a quarter in
      if (!x || x[0] < 0.05) return;   // shadow inks the outer quarter of the point (by length, so a small one still reads)
      const r1 = spRad(w[i]), r0 = r1 * (1 - x[0]);
      if (r1 - r0 < 0.6) return;
      const ux = Math.cos(SPA[i]), uy = Math.sin(SPA[i]), cut = (j) => {   // where the edge toward neighbour j crosses r0
        const b = P[j], pb = (b[0] - SPX) * ux + (b[1] - SPY) * uy, f = clamp((r1 - r0) / Math.max(r1 - pb, 1e-6));
        return [P[i][0] + (b[0] - P[i][0]) * f, P[i][1] + (b[1] - P[i][1]) * f];
      };
      const pts = `${f1(cut((i + 4) % 5))} ${f1(P[i])} ${f1(cut((i + 1) % 5))}`;
      sh += `<polygon class="shcap" points="${pts}"/><polygon class="shink" points="${pts}" mask="url(#${x[1] ? "ci-crosshatch" : "ci-hatch"})"/>`;
    });
    if (sh) s += `<g class="shd">${sh}</g>`;
  }
  if (o.window) s += `<circle class="win" cx="${SPX}" cy="${SPY}" r="${(SPR + 2).toFixed(1)}"/>`;
  if (o.hold) s += `<polygon class="hold" points="${spPts(o.hold)}"/>`;
  if (o.want) s += `<polygon class="want" points="${spPts(o.want)}"/>`;
  s += `<polygon class="pos" points="${spPts(w)}"/>`;
  if (o.want) COLORS.forEach((c, i) => {            // the pull: from where they are to where they want to be, thicker the faster they could move
    const a = spRad(w[i]), b = spRad(o.want[i]), d = b - a;
    if (Math.abs(d) < 2.2) return;
    const sw = 1.2 + 3 * clamp((o.acc ? o.acc[i] : 0.15) / 0.4), dir = Math.sign(d), head = Math.min(Math.abs(d) * 0.6, 3.5 + sw);
    const ux = Math.cos(SPA[i]), uy = Math.sin(SPA[i]), hw = sw / 2 + 2.6;
    const p0 = spAt(i, a), p1 = spAt(i, b - dir * head), tip = spAt(i, b);
    s += `<g class="pull" style="color:var(--c${c})"><line x1="${p0[0].toFixed(1)}" y1="${p0[1].toFixed(1)}" x2="${p1[0].toFixed(1)}" y2="${p1[1].toFixed(1)}" stroke-width="${sw.toFixed(1)}"/>` +
      `<polygon points="${f1(tip)} ${f1([p1[0] - uy * hw, p1[1] + ux * hw])} ${f1([p1[0] + uy * hw, p1[1] - ux * hw])}"/></g>`;
  });
  if (o.voice) COLORS.forEach((c, i) => {          // item 3: while the voice row is hovered, thin arrows toward where the voice pushes
    const a = spRad(w[i]), b = spRad(clamp(w[i] + o.voice[i], 0.01, 0.95)), d = b - a;
    if (Math.abs(d) < 1.5) return;
    const p0 = spAt(i, a), tip = spAt(i, b), ux = Math.cos(SPA[i]), uy = Math.sin(SPA[i]), dir = Math.sign(d), p1 = spAt(i, b - dir * 3.5);
    s += `<g class="vpull" style="color:var(--c${c})"><line x1="${p0[0].toFixed(1)}" y1="${p0[1].toFixed(1)}" x2="${p1[0].toFixed(1)}" y2="${p1[1].toFixed(1)}"/>` +
      `<polygon points="${f1(tip)} ${f1([p1[0] - uy * 3, p1[1] + ux * 3])} ${f1([p1[0] + uy * 3, p1[1] - ux * 3])}"/></g>`;
  });
  if (o.labels !== false) COLORS.forEach((c, i) => {
    const e = spAt(i, SPR + 15), on = o.label ? lettersOf(o.label).includes(c) : w[i] > enter;
    const bd = o.bands ? o.bands[i] : "";
    if (bd === "fading" || bd === "rising") s += `<circle class="bd ${bd}" cx="${e[0].toFixed(1)}" cy="${e[1].toFixed(1)}" r="14.5"/>`;
    s += `<g class="orb" data-c="${c}"><circle cx="${e[0].toFixed(1)}" cy="${e[1].toFixed(1)}" r="11.5" fill="var(--p${c})" stroke="rgb(0 0 0 / .5)" opacity="${on ? 1 : 0.5}"/><use class="gx" href="#${MANA(c)}" x="${(e[0] - 8).toFixed(1)}" y="${(e[1] - 8).toFixed(1)}" width="16" height="16" style="color:var(--pInk)" opacity="${on ? 1 : 0.55}"/></g>`;
    const ly = i === 0 ? e[1] + 4 : e[1] + 25, lx = i === 0 ? e[0] + 16 : e[0];
    s += `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="${i === 0 ? "start" : "middle"}" class="${on ? "on" : ""}">${pct(w[i])}</text>`;
    if (o.hits) { const hx = SPX + SPR * 0.62 * Math.cos(SPA[i]), hy = SPY + SPR * 0.62 * Math.sin(SPA[i]); s += `<circle class="hit" data-c="${i}" cx="${((hx + e[0]) / 2).toFixed(1)}" cy="${((hy + e[1]) / 2).toFixed(1)}" r="27"/>`; }
  });
  return s;
}
const spOf = (L, extra) => ({ w: L.w, want: L.w.map((v, i) => Math.max(0.01, v + L.demand[i])), hold: L.inertia.map((v) => v + 0.2), acc: L.acc,
  rule: (hud && hud.life && hud.life.ident_rule) || [0.22, 0.18], label: L.label, bands: L.dyn ? L.dyn.bands : null, window: !!(L.dyn && L.dyn.window),
  shadow: L.shadow ? L.shadow.cols.map((x) => x.show ? [x.part, x.on] : null) : null, ...(extra || {}) });
// the key under the graph; each word's hover is its exact definition
const SP_KEY = [["pos", "Now", "Their five colors now, as shares of 100."],
  ["want", "Wants", "Where their wanting points: the colors they would move to if nothing held them back."],
  ["hold", "Holds", "What holds them where they are: 40% what they notice first, 30% their habits, 30% the titles they have put themselves into."],
  ["pull", "Pull", "The arrow runs from where they are to where they want to be. It is thicker the faster they could change now: how open their age is, times self-control, times their belief they can act that way, times the doors open to them."],
  ["band", "Edge", "The band from 18% to 22%: a color joins who they are above 22% and leaves below 18%. A dashed ring on a color: it is fading, held only by that edge. A bright ring: it is rising toward it."]];
function spKeyHTML() { return `<div class="spkey">${SP_KEY.map(([k, w]) => `<span data-spk="${k}"><i class="k-${k}"></i>${w}</span>`).join("")}</div>`; }
function bindSpKey(root) { root.querySelectorAll("[data-spk]").forEach((el) => { const k = SP_KEY.find((x) => x[0] === el.dataset.spk); setTip(el, () => tipBox(`<i class="spk k-${k[0]}"></i> ${k[1]}`, "", [], k[2])); }); }
// a slow week-by-week animation of the graph (point 2): frames [{w, want}], played over ms; the last frame is drawn with base's hits
const anims = new WeakMap();
// E9: a weekly trace row is [t, five colors, five wants, bands as letters (i, f, r, o), the identity label]
const BAND_CODE = { i: "in", f: "fading", r: "rising", o: "out" };
const frameOf = (f) => ({ t: f[0], w: f.slice(1, 6), want: f.slice(6, 11), ...(typeof f[11] === "string" && f[11].length === 5 ? { bands: [...f[11]].map((c) => BAND_CODE[c] || ""), label: f[12] || "" } : {}) });
const bandsOf = (A) => (A && A.bands ? { bands: A.bands, label: A.label } : {});
function animSpider(svg, frames, ms, base, done) {
  const prev = anims.get(svg); if (prev) cancelAnimationFrame(prev.raf);
  if (!frames.length) { if (done) done(); return; }
  const t0 = performance.now(), n = frames.length, st = { raf: 0 };
  anims.set(svg, st);
  const lerp = (a, b, f) => a.map((v, i) => v + (b[i] - v) * f);
  const draw = (now) => {
    const x = n === 1 ? 1 : clamp((now - t0) / Math.max(1, ms)) * (n - 1), k = Math.min(n - 2, Math.floor(x)), f = n === 1 ? 0 : x - k;
    const A = frames[Math.max(0, k)], B = frames[Math.min(n - 1, k + 1)];
    const end = now - t0 >= ms;
    svg.innerHTML = spiderSVG({ ...base, ...(end ? {} : bandsOf(f < 0.5 ? A : B)), w: end ? frames[n - 1].w : lerp(A.w, B.w, f), want: end ? frames[n - 1].want : lerp(A.want, B.want, f), hits: end && base.hits });
    if (end) { anims.delete(svg); if (done) done(); } else st.raf = requestAnimationFrame(draw);
  };
  st.raf = requestAnimationFrame(draw);
}

/* ---------------- point 4: exact definitions ---------------- */
// each "around them" driver, exactly as the engine reads it to time life events (engine.py, the event context X)
const AROUND_DEF = {
  "own household": "A partner counts 1, children 1, a community ½; the sum, minus 1.",
  ties: "People they can lean on, 0 to 100, minus 50.",
  money: "Their money, 0 to 100, minus 50.",
  health: "Their health, 0 to 100, minus 50.",
  era: "How hard the era of these years is pushing; 0 in quiet times.",
  "harsh world": "How hard life is in this world; set by the world.",
  unrest: "How unsettled this society is; set by the world.",
  prosperity: "How well off this society is; set by the world.",
  community: "A community they belong to, times what they have put into it.",
  stress: "Strain minus 50, kept between −50% and +100%.",
  "recent trouble": "Blows of recent years, fading with time; up to 200%.",
  "recent fortune": "Lucky turns of recent years, fading with time; up to 200%." };
const aroundPct = (v) => `${v > 0 ? "+" : v < 0 ? "−" : ""}${Math.round(Math.abs(v) * 100)}%`;
function aroundBands(k) {
  const B = (hud && hud.around_bands) || {}, bs = B[k] || B["*"] || [], fl = ((hud && hud.around_floor) || {})[k] || ((hud && hud.around_floor) || {})["*"];
  return bs.map(([t, w]) => `${esc(w)} from ${aroundPct(t)}`).concat(fl ? [`${esc(fl)} below`] : []).join(", ");
}
function aroundTip(k, v) {
  const L = hud && hud.life, g = good(k, v), w = (L && L.around_words || {})[k] || "";
  return tipBox(`${ic("compass")} ${esc(cap(k))}: ${esc(w)} (${aroundPct(v)})`, esc(AROUND_DEF[k] || ""), [["Words", aroundBands(k)]],
    g > 0 ? "Now it makes good events likelier and hard ones rarer." : g < 0 ? "Now it makes hard events likelier." : "");
}
// a state's exact definition (engine.ADJECTIVES): the variable it reads over the last three months, where it begins and ends
function stateScale(var_, scale, v) {
  if (var_ === "stress") return `${Math.round(v / 1.5 * 100)}% of the most they can bear`;
  return scale === "of100" ? `${Math.round(v * 100)} of 100` : `${v < 0 ? "−" : ""}${Math.abs(Math.round(v * 100))} points`;
}
const oneIn = (s) => s >= 0.45 ? "about half" : `about 1 in ${Math.max(2, Math.round(1 / Math.max(s, 0.01)))}`;
function stateDef(x) {
  const D = (hud && hud.adj_defs && hud.adj_defs[x.name]) || x;
  const sc = (v) => stateScale(D.var, D.scale, v);
  return `${cap(D.reads)} ${D.side > 0 ? "above" : "below"} ${sc(D.on)} over the last three months; it ends ${D.side > 0 ? "below" : "above"} ${sc(D.off)}.`;
}
function stateTip(x) {
  const D = (hud && hud.adj_defs && hud.adj_defs[x.name]) || x;
  const rows = [];
  if (x.value != null) rows.push(["Now", stateScale(D.var, D.scale, x.value)]);
  if (x.years != null) rows.push(["For", yrsWord(x.years)]);
  if (D.share) rows.push(["Adults like this", oneIn(D.share)]);
  if (D.from_age) rows.push(["From age", String(Math.round(D.from_age))]);
  return tipBox(`${ic(x.icon)} ${esc(cap(x.word || D.say))}`, esc(stateDef(x)), rows, "");
}
// item 2, light and shadow (only with the engine's shadows switch on, hud.life.shadow): a colour's line ("Red 40%, a
// quarter of it in shadow: reckless at times"), where the shadow comes from, and whether they have seen it in themselves
function shadowRows(L, i) {
  const x = L.shadow && L.shadow.cols[i];
  if (!x || !x.show) return [];
  return [[`${ic(GI.shadow && GI.shadow[SH_GI[x.state]] || "dot")} Shadow`, `<b>${esc(x.line)}</b>`]].concat(x.src.length ? [["From", esc(x.src.join("; "))]] : [],
    x.seen ? [["Seen", "they have seen it in themselves"]] : []);
}
const SH_GI = { rigid: "rigid", indecisive: "indecisive", ruthless: "ruthless", reckless: "reckless", "stuck in their ways": "stuck" };   // ink-icons.json "shadow"
function shadowTip(x) {      // a shadow state's hover: its colour's line, its sources, and when it shows and goes
  const S = x.shadow || {}, on = (hud && hud.life && hud.life.shadow) || { on: 0.5, off: 0.35 };
  const rows = [];
  if (x.value != null) rows.push(["Pull now", `${Math.round(x.value * 100)} of 100`]);
  if (S.src && S.src.length) rows.push(["From", esc(S.src.join("; "))]);
  if (x.years != null) rows.push(["For", yrsWord(x.years)]);
  rows.push(["Seen", S.seen ? "they have seen it in themselves" : "not yet: they do not see it in themselves"]);
  return tipBox(`${ic(x.icon)} ${esc(cap(x.word))}`, S.line ? esc(S.line) : "", rows,
    `A color that rules a life casts a shadow. This shows when the shadow's pull passes ${Math.round(on.on * 100)} of 100 over the last three months, and goes below ${Math.round(on.off * 100)}.`);
}
const stTip = (x) => x.shadow !== undefined ? shadowTip(x) : stateTip(x);
const BAND_WORD = { in: "part of who they are", fading: "fading: at or under 22%, held by the edge", rising: "rising: above 18%, not yet part of them", out: "not part of who they are" };
function tipColor(L, i) {
  const c = COLORS[i], w = L.w[i], inId = lettersOf(L.label).includes(c), [enter, leave] = L.ident_rule || [0.22, 0.18];
  return tipBox(`${pip(c)} ${CNAME[c]}`, CIDEA[c], [
    ["Now", `<b>${pct(w)}</b>`],
    ["Wants", `${pct(Math.max(0, w + L.demand[i]))} (${updown(L.demand[i], 0, 100)} pts)`],
    ["Holds", pct(L.inertia[i] + 0.2)],
    ["Speed of change", pct(L.acc[i])],
    ["Skill in its ways", pct(L.skill[i])],
    ["Belief they can act so", pct(L.belief[i])],
    ["Notices first", pct(L.lens[i])],
    ["The story's voice", pct(L.voice[i])]].concat(L.dyn ? [["Place", BAND_WORD[L.dyn.bands[i]] || ""]] : [], shadowRows(L, i)),
    L.label ? (inId ? `${CNAME[c]} is part of who they are; it leaves below ${Math.round(leave * 100)}%.` : `${CNAME[c]} is not part of who they are; it joins above ${Math.round(enter * 100)}%.`) : "");
}
const RINGS = [
  ["content", "Content", GI.meter.content || "mood", "var(--sat)", "Satisfaction: how content they are with life right now. Happy is not the same as peaceful."],
  ["peace", "Peace", GI.meter.peace || "leaf", "var(--peace)", "How settled they are with who they are and how they live."],
  ["stress", "Strain", GI.meter.strain || "bolt", "var(--stress)", "The strain of the year. Pushing them against their will adds to it."],
  ["want", "Wanting", GI.meter.wanting || "flame", "var(--want)", "Pent-up wanting: what they were denied builds up. At the mark it breaks through and moves them on its own."]];
// every 0..1 quantity reaches the player as a percent (Emren 09:25: "0.58 is for me and you, 58% is for the player")
function ringPct(k, L) { return k === "want" ? pct(Math.min(1, L.want / Math.max(L.want_thr, 1e-9))) : k === "stress" ? pct(L.stress / 1.5) : pct(L[k]); }
// v22 next look: the four meters as slim bars, each with a tick at its usual level (satisfaction and peace: their average
// over the last ten years of the river; wanting: the mark where it breaks through)
function usualOf(k, L) {
  const R = (L.river || []).filter((r) => r[0] >= L.age - 10), col = k === "content" ? 6 : k === "peace" ? 7 : -1;
  if (col > 0 && R.length >= 2) return R.reduce((t, r) => t + r[col], 0) / R.length;
  return null;
}
function meterHTML(r, L) {
  const [k, label, icon, color] = r;
  let frac = clamp(L[k]), tick = usualOf(k, L);
  if (k === "stress") frac = clamp(L.stress / 1.5);
  if (k === "want") { const topv = Math.max(L.want_thr * 1.25, 1e-9); frac = clamp(L.want / topv); tick = L.want_thr / topv; }
  return `<div class="mtr" data-ring="${k}" style="--mc:${color}">${useIc(icon, "").replace("<use", '<svg class="i' + (isGi(icon) ? " gx" : "") + '" aria-hidden="true"><use') + "</svg>"}<span class="ml">${label}</span><span class="mbar"><i style="width:${(frac * 100).toFixed(1)}%"></i>${tick != null ? `<b style="left:${(clamp(tick) * 100).toFixed(1)}%"></b>` : ""}</span><span class="pv">${ringPct(k, L)}</span></div>`;
}
function ringHTML(r, L) {
  const [k, label, icon, color] = r, R0 = 22, C = 2 * Math.PI * R0;
  let v = L[k], frac = clamp(v), mark = "";
  if (k === "stress") frac = clamp(v / 1.5);
  if (k === "want") {
    const topv = Math.max(L.want_thr * 1.25, 1); frac = clamp(v / topv);
    const a = (L.want_thr / topv) * 2 * Math.PI - Math.PI / 2;
    mark = `<line class="mark" x1="${(28 + 18 * Math.cos(a)).toFixed(1)}" y1="${(28 + 18 * Math.sin(a)).toFixed(1)}" x2="${(28 + 26 * Math.cos(a)).toFixed(1)}" y2="${(28 + 26 * Math.sin(a)).toFixed(1)}"/>`;
  }
  return `<div class="rg" data-ring="${k}" style="color:${color}"><svg viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="${R0}"/><circle class="fg" cx="28" cy="28" r="${R0}" stroke="${color}" stroke-dasharray="${(frac * C).toFixed(1)} ${C.toFixed(1)}"/>${mark}${useIc(icon, 'x="19" y="19" width="18" height="18"')}</svg><b class="pv">${ringPct(k, L)}</b><span>${label}</span></div>`;
}
const MEANS = [["money", GI.res.money || "coin", "Savings and income.", "var(--sat)"], ["time", GI.res.time || "clock", "Hours left over after duties.", "var(--cU)"], ["health", GI.res.health || "pulse", "Body and energy.", "var(--cG)"],
  ["ties", GI.res.ties || "link", "People they can lean on.", "var(--cR)"], ["freedom", GI.res.freedom || "feather", "Room to choose for themselves.", "var(--arcane)"]];
const KINDS = [["career", "Work"], ["partner", "Love"], ["children", "Family"], ["community", "Circle"], ["faith", "Faith"]];
const ROLE_GROUP = { mother: "kin", father: "kin", sibling: "kin", grandparent: "kin", cousin: "kin", aunt: "kin", "late relative": "kin", child: "kin",
  partner: "love", companion: "love", prospect: "love", ex: "love", friend: "friend", neighbour: "friend",
  teacher: "work", mentor: "work", boss: "work", colleague: "work", "former boss": "work", rival: "rival" };
const GROUP_COL = { kin: "#d8b469", love: "#f08aa4", friend: "#5fcac3", work: "#8fa6d8", rival: "#f2856d", other: "#9a90b8" };
const ROLE_ICON = { kin: "home", love: "heart", friend: "people", work: "case", rival: "bolt", other: "dot", ...GI.role };
const baseRole = (r) => String(r || "").replace(/^old /, "");
const roleIcon = (r) => baseRole(r) === "child" ? (GI.role.child || "child") : ROLE_ICON[ROLE_GROUP[baseRole(r)] || "other"];
const BAD_UP = new Set(["harsh world", "unrest", "stress", "recent trouble"]), NEUTRAL = new Set(["own household", "era"]);
const good = (k, v) => NEUTRAL.has(k) ? 0 : (BAD_UP.has(k) ? -1 : 1) * Math.sign(v);
// v22.5 F1: one health bar with both halves, the body on the left and the mind on the right (only with the engine's body or
// mind switch on); its hover names what weighs on each now
const healthCol = (h) => `<span class="col two"><i style="height:${(clamp(h.body) * 100).toFixed(0)}%"></i><i class="mind" style="height:${(clamp(h.mind) * 100).toFixed(0)}%"></i></span>`;
function healthTip(L, r) {
  const h = L.health, rows = [["Now", pct(L.res.health)], ["Body", pct(h.body)], ["Mind", pct(h.mind)]];
  if (h.conditions.length) rows.push(["Living with", esc(h.conditions.join(", "))]);
  if (h.serious) rows.push(["Ill with", esc(h.serious)]);
  if (h.threats.length) rows.push(["Going through", esc(h.threats.join(", "))]);
  if (h.decline) rows.push(["Their last season", "the body is failing"]);
  return tipBox(`${ic(r[1])} Health`, "", rows, "Body and mind, half each. The body: constitution, age, habits, illness and injury. The mind: built over months from strain, losses, loneliness, meaning and rest. Each wears the other.");
}
function stateValue(x) { return x.var === "want" ? pct(x.value) + " of the way to breaking through" : x.var === "stress" ? pct(x.value / 1.5) + " of the most they can bear" : x.var === "mood" ? (x.value > 0 ? "lifted" : "lowered") + ` by recent weeks (${x.value > 0 ? "+" : "−"}${Math.round(Math.abs(x.value) * 100)}%)` : ["fortune", "trouble"].includes(x.var) ? (x.value >= 1.8 ? "one thing after another" : "some") : pct(x.value); }
function investWord(v) { return v >= 2 ? "a great deal" : v >= 1 ? "a lot" : v >= 0.35 ? "some" : "a little"; }
function temperWord(k, v) {
  const r = k === "react" ? v / 2 : v;
  return k === "react" ? (r >= 0.65 ? "hit hard by events" : r >= 0.4 ? "about average" : "hard to shake") :
    k === "steady" ? (v >= 0.6 ? "very sure of themselves" : v >= 0.3 ? "fairly sure" : "still searching") :
    k === "base_mood" ? (v >= 0.62 ? "sunny" : v >= 0.48 ? "even" : "low") : (v >= 0.55 ? "hopeful" : v >= 0.38 ? "middling" : "doubtful");
}
const TEMPER = [["react", "Reactive", "bolt", 2, "How hard events hit them."], ["steady", "Steady", "anchor", 1, "How sure they are of who they are."],
  ["base_mood", "Mood", "mood", 1, "Where their mood settles between events."], ["outlook", "Outlook", "sun", 1, "How sure they are that effort pays off."]];
// a title or perk's tooltip: its kind, the ways it asks for or helps, what it brings, and how it stands now
const shortSay = (x) => String(x || "").replace(/^(a|an|the) /, "");
// a title's name under its socket: the catalogue's say without its article, or a shorter word where the say runs long
const SOCK_WORD = { "girlfriend or boyfriend": "Sweetheart", "living together": "Living together", "partner of many years": "Years together",
  "regular worshipper": "Regular worshipper", "believer on the big days": "Big-days believer", "deacon or elder": "Elder",
  "residents' committee member": "Residents' committee", "neighbourhood volunteer": "Volunteer", "parent of three or more": "Parent of three+",
  psychotherapist: "Therapist", "cybersecurity analyst": "Security analyst", "neighbourhood-watch coordinator": "Street watch",
  "congregation musician": "Worship musician", "board-game club organiser": "Board-game club", "nonromantic life partner": "Life partner",
  "community-garden coordinator": "Garden coordinator", "search-and-rescue volunteer": "Rescue team", "parent-association organiser": "Parents' association",
  "housing-cooperative member": "Housing co-op", "community-kitchen volunteer": "Soup kitchen", "member of a monastic community": "Monastic life",
  "interfaith-dialogue participant": "Interfaith circle", "disability-rights organiser": "Disability rights", "restorative-justice advocate": "Restorative justice",
  "civil-liberties campaigner": "Civil liberties", "animal-shelter campaigner": "Animal shelter", "digital-rights advocate": "Digital rights",
  engaged: "Engaged", "community-radio presenter": "Radio presenter", "book-club organiser": "Book club", "lay religious teacher": "Lay teacher" };
const sockWord = (d) => SOCK_WORD[d.name] || cap(shortSay(d.say));
// a facet (a title held on top of another: newlywed on wife or husband), in a word or two under the socket
const FACET_WORD = { newlywed: "newlywed", "parent of three or more": "three or more", "parent of an only child": "an only child",
  "parent of independent adult children": "grown-up children", "parent with a child living abroad": "a child abroad", "home-educating parent": "home-educating",
  "parent coordinating complex support needs": "support needs", "parent raising a child across languages": "two languages", "caregiving partner": "caring for them",
  "spouse in a family-arranged marriage": "arranged", "partner in a multigenerational household": "with family", "grandparent raising a grandchild": "raising a grandchild" };
const facetWord = (f) => FACET_WORD[f.name] || shortSay(f.say);
// the Library's chance for an act: how often it works for an ordinary person of these ages
const baseWord = (b) => b >= 0.95 ? "it almost always works" : b < 0.05 ? "it almost never works" : `it works about ${Math.max(1, Math.min(9, Math.floor(b * 10 + 0.5)))} times in 10`;
const yrsWord = (y) => y < 1 ? "a few months" : y < 2 ? "about a year" : `${Math.round(y)} years`;
const waysHTML = (w) => { const cs = lettersOf(w || ""); return cs.length ? pips(cs) + " " + cs.map((c) => CNAME[c]).join(" and ") : "any"; };
const CLOSED_WORD = { law: "the law", approval: "the approval of others", means: "lack of means" };
function findRole(name) {
  const L = hud && hud.life; if (!L) return null;
  return (L.perks || []).find((x) => x.name === name) || (L.statuses || []).find((x) => x.name === name) ||
    [].concat(...(L.titles || []).map((t) => t.named || [])).find((x) => x.name === name) || null;
}
function roleTip(d, now) {
  const rows = [];
  if (d.title) {
    if (d.on) rows.push(["Held on", esc(cap(String(d.on)))]);
    if (d.profile) rows.push(["Their way", esc(d.profile)]);
    if (d.ways) rows.push(["Its ways", waysHTML(d.ways)]);
    if (d.meets && d.meets.length) rows.push(["Brings", d.meets.map(([w, g]) => `<span class="${g > 0 ? "up" : "down"}">${g > 0 ? "+" : "−"}${esc(w)}</span>`).join(", ")]);
  } else {
    rows.push(["Helps", d.plus > 0 ? `+${d.plus}% on acts in ${waysHTML(d.ways)} ways` : "opens doors that some acts need"]);
    if (d.half && d.kind === "skill") rows.push(["Unused", `half of it is gone in about ${d.half} years`]);
  }
  const st = now === undefined ? d : now;
  if (!st) rows.push(["Now", "not held"]);
  else if (st.state === "suspended") rows.push(["Now", `on hold${st.back_in > 0 ? ", back in " + yrsWord(st.back_in) : ""}`]);
  else if (st.state === "rusty") rows.push(["Now", "no longer held; it still helps a little while it fades"]);
  else if (st.years != null) rows.push(["Held", yrsWord(st.years)]);
  const head = d.title ? cap(shortSay(d.say || d.name)) : cap(d.name);
  const sub = d.title ? (d.kind === "status" ? "A status" : `A title in ${esc((KINDS.find((k) => k[0] === d.kind) || [0, cap(d.kind)])[1])}`) : PERK_KIND_WORD[d.kind] || "A perk";
  return tipBox(`${ic(roleIconOf(d))} ${esc(head)}`, sub, rows, "");
}
// a life holds about 25 perks: the HUD shows the first dozen (credentials, skills, assets, standing, bonds, then those on hold
// or fading) and a chip for the rest; the choice is remembered in this browser
const PERK_SHOW = 12;
let perksOpen = false; try { perksOpen = localStorage.getItem("chroma.perksOpen") === "1"; } catch (_) {}
let hudFrames = [], hudLast = null;
// Emren's point 6: a season of change between two stages of life, or into a new title (engine explain.season)
const seasonWords = (x) => `${x.kind === "stage" ? "Crossing into " + x.into : "Becoming " + x.into} · ${x.step_word}`;
const SEASON_DEF = "A season of change: the crossing, the in-between, then settling in. One moment in it can transform who they become.";
function seasonTip(x) { return tipBox(`${ic("gate")} ${esc(seasonWords(x))}`, SEASON_DEF, [["Step", `${x.step} of 3`], ["Weeks in", String(x.weeks_in)], ["Weeks left", String(x.weeks_left)]], ""); }
// item 15 "your places": the haunts they go to, their standing in each sphere, and their town's spheres (game.places_view)
const SPH_ICON = { rule: "sign", gather: "people", arts: "feather", faith: "candle", care: "heart", learn: "book", prod: "case", comm: "coin", prot: "shield" };
const FACE_ORDER = ["W", "U", "B", "R", "G"];
// v22.4: S4's mark on a place where their ways are rare (held on there for years, the odd one out now, or blended in)
const oddMark = (h) => h.held ? ` ${ic("anchor")}` : h.odd ? ` ${ic("star")}` : h.blended ? ` ${ic("mask")}` : "";
// v24 footprints (the game's foot switch): the life so far as six stacks, each a count and one plain line; a stack's
// items wait behind its hover, newest first. Six icons in all, never one per footprint (Emren 10-19)
function footHTML(F) {
  return `<div class="fstacks">${F.map((x) => `<div class="fst${x.n ? "" : " none"}" data-fk="${x.kind}">${ic(x.icon)}<span class="k">${esc(x.name)}</span><b>${x.n}</b><span class="l">${esc(x.line || (x.n ? "" : "none yet"))}</span></div>`).join("")}</div>`;
}
function footTips(root, F) {
  root.querySelectorAll("[data-fk]").forEach((el) => {
    const x = (F || []).find((y) => y.kind === el.dataset.fk);
    if (x && (x.items || []).length) setTip(el, () => tipBox(`${ic(x.icon)} ${esc(x.name)}: ${x.n}`, x.line ? esc(x.line) : "", x.items.map((i) => [`at ${Math.floor(i.age)}`, `${esc(i.word)} <span class="muted">${esc(i.sit)}</span>`]), ""));
  });
}
function placesHTML(L) {
  const P = L.places; if (!P) return "";
  const hs = (P.haunts || []).map((h, i) => `<span class="perk" data-pl="${i}" style="--pc:var(--c${h.lead})">${ic(SPH_ICON[h.sphere] || "home")}${esc(cap(h.name))}${h.setting ? ` ${ic("people")}` : ""}${oddMark(h)}</span>`).join("")
    + (P.settings || []).map((x, i) => `<span class="perk" data-pls="${i}" style="--pc:var(--c${x.lead || "W"})">${ic(SPH_ICON[x.sphere] || "people")}${esc(cap(x.name))} ${ic("people")}${oddMark(x)}</span>`).join("");   // S3: where their settings meet
  const ps = (P.posts || []).map((x, i) => `<span class="chip" data-plp="${i}">${ic("crown")}${esc(cap(x.title || x.name))} ${pip(x.colour)}</span>`).join("");   // S7: what they lead
  const up = (P.rungs || []).filter((r) => r.rung > 0);
  const rs = up.map((r) => `<span class="chip" data-plr="${r.sphere}">${ic(SPH_ICON[r.sphere] || "home")}${esc(cap(r.word))} <span class="pc">(${esc(r.sphere_name.toLowerCase())})</span></span>`).join("");
  const tw = (P.town || []).slice(0, 3).map((t) => `<span class="chip" data-plt="${t.sphere}">${ic(SPH_ICON[t.sphere] || "home")}${esc(t.sphere_name)} ${pip(t.lead)}</span>`).join("");
  if (!hs && !rs && !tw) return "";
  return `<div class="hsec"><h4>Their places</h4>${hs ? `<div class="perks">${hs}</div>` : `<span class="empty">No haunt of their own yet</span>`}
    <div class="chips">${rs || `<span class="muted">A newcomer in every sphere</span>`}</div>${ps ? `<div class="chips"><span class="muted">They lead</span> ${ps}</div>` : ""}${tw ? `<div class="chips"><span class="muted">Their town lives by</span> ${tw}</div>` : ""}</div>`;
}
// v22.4 on a place's hover: S1 how the sphere's decisions feel to them, S3 their name there and its last word on them, S4 the odd one out
const fairRows = (P, sp) => { const f = (P.fair || {})[sp]; return f ? [["Fairness", `<span class="${f.side === "fair" ? "up" : "down"}">${esc(f.line)}</span>`]] : []; };
const ODD_ROW = { held: ["Held on", "their ways are rare here, and years of holding to them have started to move the place"],
  odd: ["The odd one out", "their ways are rare here: they are noticed more, and pressed to blend in"], blended: ["Blended in", "they took on this place's ways"] };
function eyesRows(h) {
  if (h.name_word == null) return [];
  const rows = [["Their name here", esc(cap(h.name_word))]];
  if (h.read) rows.push(["Last word on them", `“Thinks you ${esc(h.read)}”`]);
  if (h.go) rows.push(["A go-between", "someone here carries word to their other places"]);
  const o = h.held ? ODD_ROW.held : h.odd ? ODD_ROW.odd : h.blended ? ODD_ROW.blended : null;
  if (o) rows.push([o[0], esc(o[1])]);
  return rows;
}
function bindPlaces(L) {
  const P = L.places; if (!P) return;
  const faces = (fs) => FACE_ORDER.map((c, i) => [c, fs[i]]).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([c, v]) => `${pip(c)} ${pct(v)}`).join(" ");
  hudEl.querySelectorAll("[data-pl]").forEach((el) => { const h = P.haunts[+el.dataset.pl]; setTip(el, () => tipBox(`${ic(SPH_ICON[h.sphere] || "home")} ${esc(cap(h.name))}`, esc(h.lead_line),
    [["A place of", esc(cap(h.kind))], ["Sphere", esc(h.sphere_name)], ["Its way", `${pip(h.lead)} ${esc(h.lead_name)}`], ["Who sets the tone", faces(h.faces)]].concat(h.keeper ? [["Kept by", esc(h.keeper)]] : [], eyesRows(h), fairRows(P, h.sphere)),
    h.setting ? "One of their own circles meets here." : "A place they go to; the regulars there know their face.")); });
  hudEl.querySelectorAll("[data-pls]").forEach((el) => { const x = P.settings[+el.dataset.pls]; setTip(el, () => tipBox(`${ic(SPH_ICON[x.sphere] || "people")} ${esc(cap(x.name))}`, x.setting ? `Where their ${esc(x.setting)} meets` : "",
    [["Sphere", esc(x.sphere_name)]].concat(x.lead_name ? [["Its way", `${pip(x.lead)} ${esc(x.lead_name)}`]] : [], eyesRows(x), fairRows(P, x.sphere)), "One of their own circles meets here.")); });
  hudEl.querySelectorAll("[data-plp]").forEach((el) => { const x = P.posts[+el.dataset.plp]; setTip(el, () => tipBox(`${ic("crown")} Leads ${esc(x.name)}`, x.title ? esc(cap(x.title)) : esc(x.sphere_name || ""),
    [["Their way", `${pip(x.colour)} ${esc(x.way)}`], ["Held", esc(cap(x.legit_word))], ["For", yrsWord(Math.max(0, L.age - x.since))]].concat(x.terms ? [["Terms served", String(x.terms)]] : [], x.falls ? [["Shaken", `${x.falls} time${x.falls > 1 ? "s" : ""}`]] : []),
    "How they lead wins some followers and loses others, and each way falls its own way.")); });
  hudEl.querySelectorAll("[data-plr]").forEach((el) => { const r = P.rungs.find((x) => x.sphere === el.dataset.plr); setTip(el, () => tipBox(`${ic(SPH_ICON[r.sphere] || "home")} ${esc(r.sphere_name)}`, esc(r.question),
    [["Their standing", esc(cap(r.word))], ["Rung", `${r.rung + 1} of 5`]].concat(fairRows(P, r.sphere)), "Standing rises with years of showing up and with what they do there.")); });
  hudEl.querySelectorAll("[data-plt]").forEach((el) => { const t = P.town.find((x) => x.sphere === el.dataset.plt); setTip(el, () => tipBox(`${ic(SPH_ICON[t.sphere] || "home")} ${esc(t.sphere_name)}`, "",
    [["Share of the town's hours", pct(t.hours)], ["Its way here", `${pip(t.lead)} ${esc(t.lead_name)}`]].concat(fairRows(P, t.sphere)), "How their town spends its days, and the way each part of life is done there.")); });
}

function renderHud(L) {
  if (!L || !L.w) { hudEl.innerHTML = ""; return; }
  const lc = labelColors(L.label);
  // point 5: each title held is a row (its life domain, its name, a facet, how long), the empty domains a row of faint signs
  const titles = KINDS.filter(([k]) => (L.titles || []).some((x) => x.kind === k)).map(([k, word]) => {
    const t = L.titles.find((x) => x.kind === k), ex = lettersOf(t.expects), nm = t.named || [];
    const label = nm.length ? sockWord(nm[0]) + (nm.length > 1 ? ` +${nm.length - 1}` : "") : word;
    const fc = nm.length && (nm[0].facets || []).length ? `<span class="fc">${esc(facetWord(nm[0].facets[nm[0].facets.length - 1]))}</span>` : "";
    return `<div class="trow${t.clash ? " clash" : ""}" data-sock="${k}" style="--sc:${ex.length ? `var(--c${ex[0]})` : "var(--gold)"};--yrs:${clamp(t.years / 30) * 100}%"><span class="o">${ic(KIND_ICON[k])}</span><span class="tx"><span class="tn">${esc(label)}</span>${fc}</span><span class="ty">${t.clash ? ic("bolt") : ""}${Math.floor(t.years)}y</span></div>`;
  }).join("") + ((empty) => empty.length ? `<div class="tempty">${empty.map(([k, word]) => `<span data-sock="${k}">${ic(KIND_ICON[k])}</span>`).join("")}<span class="muted">not yet: ${empty.map(([, w]) => w.toLowerCase()).join(", ")}</span></div>` : "")(KINDS.filter(([k]) => !(L.titles || []).some((x) => x.kind === k)));
  const cast = L.cast || [];
  const near = cast.filter((p) => p.alive && !/^(old |former )|^ex$/.test(p.role)).sort((a, b) => b.seen - a.seen);
  const far = cast.filter((p) => p.alive && /^(old |former )|^ex$/.test(p.role)).sort((a, b) => b.seen - a.seen);
  const gone = cast.filter((p) => !p.alive);
  const shown = near.slice(0, 12).concat(far.slice(0, 3), gone.slice(-3));
  const extra = cast.length - shown.length;
  const people = shown.map((p) => { const g = ROLE_GROUP[baseRole(p.role)] || "other"; return `<span class="av${p.alive ? "" : " gone"}${p.alive && far.includes(p) ? " far" : ""}" data-pid="${p.id}" style="--ac:${GROUP_COL[g]}">${esc(p.name[0])}</span>`; }).join("") + (extra > 0 ? `<span class="av more">+${extra}</span>` : "");
  const circle = L.circle ? CIRCLE_LAYERS.map(([k, word]) => { const xs = L.circle.filter((p) => p.layer === k && p.alive); return xs.length ? `<div class="crow"><span class="cl">${word}</span><span class="people">${xs.slice(0, k === 4 ? 14 : 10).map((p) => `<span class="av" data-cid="${p.id}" style="--ac:${p.read ? `var(--c${p.read[0]})` : "var(--muted)"}">${esc(p.name[0])}</span>`).join("")}${xs.length > (k === 4 ? 14 : 10) ? `<span class="muted">+${xs.length - (k === 4 ? 14 : 10)}</span>` : ""}</span></div>` : ""; }).join("") : "";
  const reach = L.reach ? L.reach.map((r) => `<div class="mt" data-reach="${r.ring}"><span class="ml">${ic(r.icon)} ${esc(r.word)}</span><i><b style="width:${(clamp(r.felt) * 100).toFixed(0)}%;background:var(--arcane)"></b></i><span class="mv">${esc(r.level_word)}</span></div>`).join("") : "";
  const AW = L.around_words || {};
  const around = Object.entries(L.around || {}).map(([k, v]) => { const g = good(k, v); return `<span class="chip ${g > 0 ? "up" : g < 0 ? "down" : ""}" data-a="${esc(k)}">${ic(g > 0 ? "sun" : g < 0 ? "rain" : "compass")}${esc(cap(k))}: <span class="w">${esc(AW[k] || (v > 0 ? "up" : "down"))}</span> <span class="pc">(${aroundPct(v)})</span></span>`; }).join("");
  const states = (L.states || []).map((x, i) => `<span class="st g${x.good}${x.shadow !== undefined ? " shd" : ""}" data-st="${i}">${ic(x.icon)}${esc(cap(x.word))}</span>`).join("");
  const statuses = (L.statuses || []).map((d, i) => `<span class="perk stat" data-rs="${i}">${ic(roleIconOf(d))}${esc(cap(shortSay(d.say)))}</span>`).join("");
  const pk = L.perks || [], cut = !perksOpen && pk.length > PERK_SHOW + 2 ? PERK_SHOW : pk.length;
  const perks = pk.slice(0, cut).map((d, i) => `<span class="perk${d.state && d.state !== "held" ? " " + d.state : ""}" data-perk="${i}" style="--pc:${d.ways ? `var(--c${d.ways[0]})` : "var(--gold)"}">${ic(roleIconOf(d))}${esc(cap(d.name))}</span>`).join("")
    + (pk.length > PERK_SHOW + 2 ? `<button class="perk more" id="perkMore">${perksOpen ? "Fewer" : `+${pk.length - cut} more`}</button>` : "");
  // v22 next look: a compact crest on top that fits 800 px (identity, states, wheel, four meters, means, the goal they live
  // for now), the fuller record below it in the same panel (dreams and plans, titles, perks, people, around them)
  const g0 = (L.goals || []).slice().sort((a, b) => ({ passion: 0, plan: 1, dream: 2 }[a.kind] ?? 3) - ({ passion: 0, plan: 1, dream: 2 }[b.kind] ?? 3) || b.strength - a.strength)[0];
  hudEl.innerHTML = `<button class="ghost hud-close" id="hudClose" aria-label="Close status">${ic("x")}</button>
    <div class="crestbox"><div class="cpips">${lc.length ? pips(lc) : pip("W", "dim")}</div><div class="gn">${esc(L.guild || "Still forming")}</div>
      <div class="ep" id="crestMotto">${!L.label ? "colors still forming" : esc(L.meaning || "")}</div>
      ${L.label && L.becoming ? `<div class="vo">${esc(cap(L.becoming))}</div>` : ""}${L.season_x ? `<div class="season" id="seasonChip">${ic("gate")} ${esc(seasonWords(L.season_x))}</div>` : ""}</div>
    ${states ? `<div class="states">${states}</div>` : ""}
    <div class="wheelw"><svg class="wheel" id="hudWheel" viewBox="-6 -2 212 206" role="img" aria-label="Spider graph of the five colors: where they are, where they want to be, what holds them">${spiderSVG(spOf(L, { id: "hw", hits: true }))}</svg><span class="wkey" id="wKey" tabindex="0" aria-label="How to read the wheel">?</span></div>
    <div class="meters">${RINGS.filter((r) => r[0] !== "want" || !L.young).map((r) => meterHTML(r, L)).join("")}</div>
    <div class="means5">${MEANS.map(([k, icn, , col]) => { const v = clamp(L.res[k]); return `<div class="mean" data-r="${k}" style="--mc:${col}">${k === "health" && L.health ? healthCol(L.health) : `<span class="col"><i style="height:${(v * 100).toFixed(0)}%"></i></span>`}${ic(icn)}<small>${esc(cap(k))}</small></div>`; }).join("")}</div>
    ${needsRowHTML(L)}
    ${voiceRowHTML(L)}
    ${g0 ? `<div class="nowgoal" data-gj="${g0.j}">${ic(GOAL_ICON[g0.kind] || "moon")}<span class="k">${esc(cap(g0.kind))}</span><span class="nm">${esc(g0.name)}</span></div>` : ""}
    <button class="ghost sheetbtn" id="openSheet">${ic("ci-diary")} The whole character</button>
    <div class="hmore">
    ${goalsHTML(L)}
    <div class="hsec"><h4>Titles</h4><div class="trows">${titles}</div>${statuses ? `<div class="perks stats">${statuses}</div>` : ""}</div>
    ${perks ? `<div class="hsec"><h4>Perks${pk.length > PERK_SHOW + 2 ? ` <span class="cnt">${pk.length}</span>` : ""}</h4><div class="perks">${perks}</div></div>` : ""}
    ${circle ? `<div class="hsec"><h4>People</h4><div class="circle">${circle}</div></div>` : `<div class="hsec"><h4>People</h4><div class="people">${people || `<span class="empty">Nobody met yet</span>`}</div></div>`}
    ${L.foot ? `<div class="hsec"><h4>Footprints</h4>${footHTML(L.foot)}</div>` : ""}
    ${placesHTML(L)}
    ${reach ? `<div class="hsec"><h4>Reach</h4><div class="mts">${reach}</div></div>` : ""}
    ${around ? `<div class="hsec"><h4>Around them</h4><div class="chips">${around}</div></div>` : ""}
    ${L.temper ? `<div class="hsec"><h4>Temperament</h4><div class="tmpr">${TEMPER.map(([k, lb, icn, top]) => `<div class="tm" data-tm="${k}">${ic(icn)}<div><div class="bar"><b style="width:${(clamp(L.temper[k] / top) * 100).toFixed(1)}%"></b></div>${lb}</div></div>`).join("")}</div></div>` : ""}
    </div>`;
  setTip($("wKey"), () => tipBox(`${ic("wheel")} How to read the wheel`, "", SP_KEY.map(([k, w, d]) => [`<i class="spk k-${k}"></i> ${w}`, esc(d)]), "Hover a color for its numbers."));
  if (L.label && L.meaning) setTip($("crestMotto"), () => tipBox(`${pips(lc)} ${esc(L.guild)}`, esc(L.meaning), L.magic ? [["In Magic: The Gathering", esc(L.magic)]] : [], NAME_NOTE));
  $("hudClose").addEventListener("click", () => closeHud());
  if ($("seasonChip")) setTip($("seasonChip"), () => seasonTip(L.season_x));
  const bindHits = () => hudEl.querySelectorAll("#hudWheel .hit").forEach((h) => setTip(h, () => tipColor(L, +h.dataset.c)));
  bindHits(); bindSpKey(hudEl);
  $("openSheet").addEventListener("click", (e) => { e.stopPropagation(); openSheet(); });
  hudEl.querySelectorAll("[data-nd]").forEach((el) => setTip(el, () => needTip(el.dataset.nd, L)));
  if ($("voiceRow")) {            // item 3: the row's numbers on hover, and the wheel's arrows toward where the voice pushes
    const vr = $("voiceRow"), wh = $("hudWheel"), V = L.voice_row;
    setTip(vr, () => voiceRowTip(L));
    const show = (on) => { if (!wh || !V.steer) return; wh.innerHTML = spiderSVG(spOf(L, { id: "hw", hits: true, voice: on ? V.toward.map((x) => x * 0.15) : null })); bindHits(); };
    vr.addEventListener("mouseenter", () => show(true)); vr.addEventListener("mouseleave", () => show(false));
    vr.addEventListener("focus", () => show(true)); vr.addEventListener("blur", () => show(false));
  }
  // point 2: the colors move to where they are now slowly, week by week when the weeks are known
  const fr = hudFrames.splice(0), last = hudLast; hudLast = { t: Math.round(L.age * 52), w: L.w, want: L.w.map((v, i) => Math.max(0.01, v + L.demand[i])) };
  if (last && !IL.on && (fr.length || last.w.some((v, i) => Math.abs(v - L.w[i]) > 0.002))) {
    const frames = [last].concat(fr.filter((_, i) => fr.length < 120 || i % Math.ceil(fr.length / 120) === 0), [hudLast]);
    animSpider($("hudWheel"), frames, clamp(frames.length * 45, 900, 2600), spOf(L, { id: "hw", hits: true }), bindHits);
  }
  hudEl.querySelectorAll("[data-ring]").forEach((el) => { const m = RINGS.find((x) => x[0] === el.dataset.ring); setTip(el, () => tipBox(`<span style="color:${m[3]}">${ic(m[2])}</span> ${m[1]}`, "", [["Now", m[0] === "want" ? `${ringPct("want", L)} of the way to breaking through` : m[0] === "stress" ? `${ringPct("stress", L)} of the most they can bear` : ringPct(m[0], L)]], m[4] + (m[0] === "want" && L.young ? " Only from young adulthood." : ""))); });
  hudEl.querySelectorAll("[data-r]").forEach((el) => { const r = MEANS.find((x) => x[0] === el.dataset.r); setTip(el, () => r[0] === "health" && L.health ? healthTip(L, r) : tipBox(`${ic(r[1])} ${cap(r[0])}`, "", [["Now", pct(L.res[r[0]])]], r[2])); });
  hudEl.querySelectorAll("[data-sock]").forEach((el) => {
    const k = el.dataset.sock, t = (L.titles || []).find((x) => x.kind === k);
    const nm = (t && t.named) || [];
    const as = nm.map((x) => `${esc(sockWord(x))}${(x.facets || []).map((f) => ", " + esc(shortSay(f.say))).join("")}${x.ways ? " " + pips(lettersOf(x.ways)) : ""} <span class="muted">${yrsWord(x.years)}</span>`).join("<br>");
    const way = nm.length && nm[0].profile ? [["Their way", esc(nm[0].profile)]] : [];
    const brings = nm.length && nm[0].meets && nm[0].meets.length ? [["It brings", nm[0].meets.map(([w, g]) => `<span class="${g > 0 ? "up" : "down"}">${g > 0 ? "+" : "−"}${esc(w)}</span>`).join(", ")]] : [];
    setTip(el, () => t ? tipBox(`${ic(KIND_ICON[k])} ${cap(k)}`, t.clash ? "In a clash: it asks for one thing, they want another." : "", (as ? [["As", as]] : []).concat(way, brings, [["Held", yrsWord(t.years)], ["Invested", investWord(t.invested)], ["It expects", pips(lettersOf(t.expects))]]), "")
      : tipBox(`${ic(KIND_ICON[k])} ${cap(k)}`, "Not held yet", [], ""));
  });
  hudEl.querySelectorAll("[data-pid]").forEach((el) => setTip(el, () => personTip(+el.dataset.pid)));
  bindPlaces(L);
  hudEl.querySelectorAll("[data-cid]").forEach((el) => setTip(el, () => circleTip((L.circle || []).find((p) => p.id === +el.dataset.cid))));
  hudEl.querySelectorAll("[data-reach]").forEach((el) => { const r = (L.reach || []).find((x) => x.ring === el.dataset.reach); if (r) setTip(el, () => tipBox(`${ic(r.icon)} Reach: ${esc(r.word)}`, "",
    [["Standing", esc(r.level_word)], ["They feel", `${fpct(r.felt)} able to change it`], ["Reality, roughly", esc(r.hint || "unclear")]],
    "How far their acts can move it: the close circle always answers; the town a little; institutions and the state only through office, fame, wealth or invention.")); });
  hudEl.querySelectorAll("[data-a]").forEach((el) => { const k = el.dataset.a; setTip(el, () => aroundTip(k, L.around[k])); });
  hudEl.querySelectorAll("[data-tm]").forEach((el) => { const t = TEMPER.find((x) => x[0] === el.dataset.tm); setTip(el, () => tipBox(`${ic(t[2])} ${TEMPER_NAME[t[0]]}`, t[4], [["Now", temperWord(t[0], L.temper[t[0]])]], "")); });
  hudEl.querySelectorAll("[data-st]").forEach((el) => { const x = L.states[+el.dataset.st]; setTip(el, () => x.reads ? stTip(x) : tipBox(`${ic(x.icon)} ${esc(cap(x.word))}`, "", [[esc(x.name), stateValue(x)]], "")); });
  if (L.foot) footTips(hudEl, L.foot);
  hudEl.querySelectorAll("[data-gj]").forEach((el) => { const g = (L.goals || []).find((x) => x.j === +el.dataset.gj); if (g) setTip(el, () => goalTip({ kind: g.kind, colors: g.colors, domain: g.domain, source: g.source, horizon: g.horizon }, g)); });
  const ap = $("addPlan"); if (ap) { ap.addEventListener("click", (e) => { e.stopPropagation(); send("p"); }); setTip(ap, () => tipBox(`${ic("quill")} Make a plan`, "", [], "Set them a plan: a year, five years or a lifetime, in a life domain or in some colors. You see how sure they feel, and how plans like it usually go. Key p.")); }
  hudEl.querySelectorAll("[data-perk]").forEach((el) => { const d = L.perks[+el.dataset.perk]; setTip(el, () => roleTip(d)); });
  const pm = $("perkMore"); if (pm) pm.addEventListener("click", (e) => { e.stopPropagation(); perksOpen = !perksOpen; try { localStorage.setItem("chroma.perksOpen", perksOpen ? "1" : ""); } catch (_) {} renderHud(L); });
  hudEl.querySelectorAll("[data-rs]").forEach((el) => { const d = L.statuses[+el.dataset.rs]; setTip(el, () => roleTip(d)); });
}

function goalBG(cs) { return cs.length > 1 ? `linear-gradient(90deg, ${cs.map((c) => `var(--c${c})`).join(", ")})` : cs.length ? `var(--c${cs[0]})` : "var(--arcane)"; }
function goalRow(g, mine) {
  const cs = lettersOf(g.colors), col = cs.length ? `var(--c${cs[0]})` : "var(--arcane)";
  const fill = g.kind === "plan" ? Math.max(0.03, g.progress) : g.strength;
  const val = g.kind === "plan" ? `${g.by_player ? `<span class="mine">${ic("quill")}</span>` : ""}${fpct(g.felt)}` : pips(cs);
  return `<div class="drm ${g.kind}" data-gj="${g.j}" style="--gc:${col};--gbg:${g.kind === "plan" ? "linear-gradient(90deg, var(--gold3), var(--gold2))" : goalBG(cs)}">
    <span class="gi">${ic(GOAL_ICON[g.kind])}</span><div style="min-width:0"><div class="gn">${esc(cap(g.name))}</div><div class="gbar"><b style="width:${(clamp(fill) * 100).toFixed(0)}%"></b></div></div><span class="gv">${val}</span>${mine || ""}</div>`;
}
function goalsHTML(L) {
  const gs = L.goals;
  if (!gs) return "";
  const canPlan = hud && hud.mode === "play" && !L.young;
  return `<div class="hsec"><h4>Dreams and plans</h4><div class="drms">${gs.length ? gs.map((g) => goalRow(g)).join("") : `<span class="empty">No dreams yet</span>`}</div>${canPlan ? `<button class="ghost addplan" id="addPlan">${ic("quill")} Make a plan</button>` : ""}</div>`;
}

/* ---------------- making a plan (key p; engine v7 foresee.py) ---------------- */
const planEl = document.createElement("div"); planEl.className = "help plan"; planEl.hidden = true; document.body.appendChild(planEl);
planEl.addEventListener("click", (e) => { if (e.target === planEl) send("x"); });
function renderPlan(h) {
  const p = h && h.plan;
  if (!p || busy) { planEl.hidden = true; planEl.innerHTML = ""; return; }
  const L = h.life || {}, name = esc(L.name || "them");
  let body = "";
  if (p.step === "horizon") {
    const plans = (L.goals || []).filter((g) => g.kind === "plan");
    body = `<p class="muted" style="margin:0">A plan pulls on what ${name} does until it comes true, runs out of time, or is let go. Within…</p>
      <div class="opts">${p.horizons.map(([k, , t]) => `<button class="ch" data-v="${k}"><b>${esc(cap(t))}</b></button>`).join("")}</div>
      ${plans.length ? `<div class="muted" style="font-size:var(--fs-1)">Plans held now</div><div class="held">${plans.map((g, i) => goalRow(g, `<button class="ghost xbtn" data-v="d${i + 1}">${ic("x")} drop</button>`)).join("")}</div>` : ""}`;
  } else if (p.step === "what") {
    body = `<p class="muted" style="margin:0">${esc(cap(p.horizon === "life" ? "a lifetime" : "within " + (p.horizon === "year" ? "a year" : "five years")))}: a plan to…</p>
      <div class="opts">${p.domains.map(([k, d, t]) => `<button class="ch" data-v="${k}" ${(p.held || []).includes(d) ? `disabled data-held title="${name} already has this"` : ""}>${ic(KIND_ICON[d])} <b>${esc(cap(t))}</b></button>`).join("")}</div>
      <p class="muted" style="margin:6px 0">…or a pursuit in these ways:</p>
      <div class="colorpick">${COLORS.map((c) => `<button class="cbtn" data-c="${c}" aria-pressed="false">${pip(c)}<span>${CNAME[c]}</span></button>`).join("")}</div>
      <div class="inrow" style="margin-top:10px"><button class="primary" id="planCols">${ic("push")} This pursuit</button></div>`;
  } else {
    const v = p.preview || {};
    body = v.blocked ? `<p>${esc(v.blocked)}.</p>` : `<h3 style="margin:4px 0 0;font:600 var(--fs-3) var(--display)">${ic("target")} The plan to ${esc(v.name)}</h3>
      <div class="bigfelt"><b>${fpct(v.felt)}</b><div><div>how sure ${name} feels</div><div class="muted">plans like it come true <span class="hintw">${esc(v.hint)}</span></div></div></div>
      <table class="kv"><tr><td>Due</td><td>at ${Math.floor(v.due_age)}</td></tr><tr><td>Fit with who they are</td><td>${fitWord(v.fit)}</td></tr>${v.left_out && v.left_out.length ? `<tr><td>The feeling leaves out</td><td>${esc(v.left_out.join(", "))}</td></tr>` : ""}</table>
      <p class="muted" style="font-size:var(--fs-1)">They will hold your plan: it does not fade, and they will not drop it on their own. Keeping a plan builds self-control; giving it up wears it down.</p>`;
  }
  planEl.hidden = false;
  planEl.innerHTML = `<div class="box paper"><h2>${ic("quill")} A plan for ${name}</h2>${body}
    <div class="center" style="margin-top:12px;display:flex;gap:10px;justify-content:center">${p.step === "confirm" && !(p.preview || {}).blocked ? `<button class="primary" id="planOk">${ic("check")} Make the plan</button>` : ""}<button class="ghost" id="planX">${ic("x")} ${p.step === "horizon" ? "Close" : "Cancel"}</button></div></div>`;
  planEl.querySelectorAll("[data-v]").forEach((b) => b.addEventListener("click", () => send(b.dataset.v)));
  planEl.querySelectorAll(".cbtn").forEach((b) => b.addEventListener("click", () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true")));
  const pc = $("planCols"); if (pc) pc.addEventListener("click", () => { const cs = [...planEl.querySelectorAll('.cbtn[aria-pressed="true"]')].map((b) => b.dataset.c).join(""); if (cs) send(cs); else toast("Pick at least one color."); });
  const ok = $("planOk"); if (ok) ok.addEventListener("click", () => send(""));
  $("planX").addEventListener("click", () => send("x"));
  planEl.querySelectorAll(".drm").forEach((el) => { const g = (L.goals || []).find((x) => x.j === +el.dataset.gj); if (g) setTip(el, () => goalTip({ kind: g.kind, colors: g.colors, horizon: g.horizon, source: g.source, domain: g.domain }, g)); });
}

