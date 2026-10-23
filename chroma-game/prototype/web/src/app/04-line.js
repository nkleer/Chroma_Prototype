/* ---------------- part 1: the whole life as a line (the end is unknown: fog) ---------------- */
const SPAN = 100;
function curve(pts, first) {
  let d = (first ? "M" : "L") + pts[0][0].toFixed(1) + " " + pts[0][1].toFixed(1);
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    const c1x = p1[0] + (p2[0] - p0[0]) / 6, c1y = p1[1] + (p2[1] - p0[1]) / 6, c2x = p2[0] - (p3[0] - p1[0]) / 6, c2y = p2[1] - (p3[1] - p1[1]) / 6;
    d += `C${c1x.toFixed(1)} ${c1y.toFixed(1)} ${c2x.toFixed(1)} ${c2y.toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d;
}
let lineGeo = null;
/* ---------------- part 1: the whole life as a line (the end is unknown: fog) ----------------
   parts/line.js, the zoomed life line after the approved mockup (Emren, 10-07): the lived years fill about three quarters
   of the strip, the years ahead are folded into the starry fog, identity runs as a thin band under the river, the events
   sit in a row under it. Replaces function drawLine() in app.js. Uses SPAN, curve, trunc, cosmos, lineGeo (keep
   `let lineGeo = null;`), and the shared helpers; cosmos(), the motes, scheduleLine and the ResizeObserver are unchanged. */

// One mapping for everything (river, band, glyphs, ticks, hover, clicks, fog). The lived years [0, now] take 74% of the
// inner width (a small child less: from 30% at birth, easing up to 74% at 8, so a first year is not absurdly wide); the
// years ahead, to SPAN, share the rest on a softened square root, so the near decades get more room than the far ones.
// When the life is over the lived span fills the whole width. A is the inverse of X.
function lnScale(W, pad, now, over) {
  const x0 = pad, xE = W - pad, t = clamp(now / 8);
  const f = over ? 1 : now <= 0 ? 0 : 0.3 + 0.44 * t * t * (3 - 2 * t);
  const xN = x0 + f * (xE - x0), fw = xE - xN, fy = Math.max(1e-6, SPAN - now);
  const E = 0.03, rE = Math.sqrt(E), K = Math.sqrt(1 + E) - rE;
  const X = (a) => a <= now ? (now > 0 ? x0 + (Math.max(0, a) / now) * (xN - x0) : x0)
    : over ? xE : xN + ((Math.sqrt(Math.min(1, (a - now) / fy) + E) - rE) / K) * fw;
  const A = (x) => {
    if (x <= xN || over || fw <= 0) return now > 0 && xN > x0 ? clamp((x - x0) / (xN - x0)) * now : 0;
    const q = Math.min(1, (x - xN) / fw) * K + rE;
    return now + (q * q - E) * fy;
  };
  return { X, A, x0, xN, xE };
}
// Rows from the strip's height: the river on top, the identity band right under it, the event glyphs, the age labels.
// 92 px on a desktop, 64 px on a phone (there the glyphs shrink to dots).
function lnLayout(H) {
  const sm = H < 80, tickY = H - (sm ? 4 : 6), gr = sm ? 2.8 : clamp(H * 0.082, 6.5, 9);
  const gy = tickY - 13 - gr, bandH = sm ? 3 : 3.5, bandY = gy - (sm ? 6.5 : gr + 4) - bandH;
  const top = sm ? 4 : 6, bot = bandY - (sm ? 2 : 3);
  return { sm, tickY, gr, gy, bandH, bandY, top, bot, mid: (top + bot) / 2, maxT: bot - top };
}
function lnF(v) { return (+v).toFixed(1); }
// The river: five stacked color bands whose thickness swells with satisfaction (r[6]), out of a point at birth.
function lnRiver(L, R, now, X, ly) {
  const eq = [0.2, 0.2, 0.2, 0.2, 0.2], norm = (s) => { const t = s.reduce((p, q) => p + q, 0) || 1; return s.map((v) => v / t); };
  const rows = R.map((r) => [r[0], norm(r.slice(1, 6)), clamp(r[6] || 0)]);
  if (!rows.length) { if (!(now > 0.05)) return ""; rows.push([now, eq, clamp(L.content == null ? 0.6 : L.content)]); }
  else {
    const last = rows[rows.length - 1];
    if (now - last[0] >= 0.25) rows.push([now, last[1], last[2]]);
    else if (now > last[0] && rows.length > 1) last[0] = now;       // too close for a smooth joint: stretch the last row
  }
  const T = (c) => ly.maxT * (0.42 + 0.58 * c), a1 = rows[0][0], s1 = rows[0][1], t1 = T(rows[0][2]);
  const pts = [[0, eq, 0.5]];
  for (const f of [0.06, 0.18, 0.36, 0.6, 0.82]) if (a1 * f > 0.04) pts.push([a1 * f, eq.map((v, k) => v + (s1[k] - v) * f), Math.max(0.5, t1 * Math.sqrt(f))]);
  for (const r of rows) pts.push([r[0], r[1], T(r[2])]);
  const edges = pts.map((p) => { let y = ly.mid - p[2] / 2; const e = [y]; for (let c = 0; c < 5; c++) { y += p[2] * p[1][c]; e.push(y); } return e; });
  const xs = pts.map((p) => X(p[0]));
  let layers = "";
  COLORS.forEach((c, k) => {
    const up = xs.map((x, i) => [x, edges[i][k]]), lo = xs.map((x, i) => [x, edges[i][k + 1]]).reverse();
    layers += `<path class="lay" fill="url(#lg${c})" d="${curve(up, true)}${curve(lo, false)}Z"/>`;
  });
  // drawn once, shown twice: the soft glow under the crisp bands
  return `<defs><g id="lnLays">${layers}</g></defs><use class="glowl" href="#lnLays"/><use class="lays" href="#lnLays"/><path class="sheen" d="${curve(xs.map((x, i) => [x, edges[i][0]]), true)}"/>`;
}
// Identity chapters as a thin band under the river: who they were, year by year, each identity blending into the next.
function lnBand(R, now, X, ly) {
  const runs = [];
  R.forEach((r, i) => {
    const a0 = i ? r[0] : 0, a1 = i + 1 < R.length ? R[i + 1][0] : now, l = r[8] || "";
    if (runs.length && runs[runs.length - 1].l === l) runs[runs.length - 1].a1 = a1; else runs.push({ l, a0, a1 });
  });
  if (!runs.length && now > 0.05) runs.push({ l: "", a0: 0, a1: now });
  if (!runs.length) return "";
  const xa = X(0), xb = Math.max(xa + 1, X(now)), off = (x) => clamp((x - xa) / (xb - xa)).toFixed(4);
  let stops = "";
  for (const u of runs) {
    const cs = lettersOf(u.l), parts = cs.length ? cs : [""], x0 = X(u.a0), w = Math.max(0, X(Math.min(u.a1, now)) - x0) / parts.length;
    parts.forEach((c, j) => {
      const p0 = x0 + w * j, e = Math.min(w * 0.3, 9), col = c ? `stop-color:var(--c${c});stop-opacity:0.95` : "stop-color:#d6cdf5;stop-opacity:0.2";
      stops += `<stop offset="${off(p0 + e)}" style="${col}"/><stop offset="${off(p0 + w - e)}" style="${col}"/>`;
    });
  }
  const y = ly.bandY, h = ly.bandH;
  return `<defs><linearGradient id="bandG" gradientUnits="userSpaceOnUse" x1="${lnF(xa)}" x2="${lnF(xb)}" y1="0" y2="0">${stops}</linearGradient></defs>` +
    `<rect class="bandglow" x="${lnF(xa)}" y="${lnF(y - 1)}" width="${lnF(xb - xa)}" height="${lnF(h + 2)}" rx="${lnF(h / 2 + 1)}" fill="url(#bandG)"/>` +
    `<rect class="band" x="${lnF(xa)}" y="${lnF(y)}" width="${lnF(xb - xa)}" height="${lnF(h)}" rx="${lnF(h / 2)}" fill="url(#bandG)"/>`;
}
// Events of the life at their ages, the most telling one where they crowd. A phone shows dots.
function lnGlyphs(byAge, now, X, ly, W) {
  const cand = [...byAge.entries()].map(([a, xs]) => [a, xs.slice().sort((p, q) => MARK_PRI[q.tag] - MARK_PRI[p.tag])]).sort((p, q) => MARK_PRI[q[1][0].tag] - MARK_PRI[p[1][0].tag] || p[0] - q[0]);
  const gr = ly.gr, gy = ly.gy, gap = ly.sm ? 8 : gr * 2 + 1.5, placed = [];
  let s = "";
  for (const [a, xs] of cand) {
    const x = clamp(X(clamp(a + 0.5, 0, now)), gr + 3, W - gr - 3);
    if (placed.some((px) => Math.abs(px - x) < gap)) continue;
    placed.push(x);
    const top1 = xs[0], cls = (MARK_PRI[top1.tag] >= 8 ? " big" : "") + (["death", "loss"].includes(top1.tag) ? " dark" : "") + (top1.tag === "choice" && !top1.ok ? " bad" : "");
    s += ly.sm
      ? `<g class="gl dot${cls}" data-age="${a}"><circle class="hit" cx="${lnF(x)}" cy="${lnF(gy)}" r="8"/><circle cx="${lnF(x)}" cy="${lnF(gy)}" r="${MARK_PRI[top1.tag] >= 8 ? 3.4 : gr}"/></g>`
      : `<g class="gl${cls}" data-age="${a}"><circle cx="${lnF(x)}" cy="${lnF(gy)}" r="${lnF(gr)}"/>${useIc(iconFor(top1), `x="${lnF(x - gr * 0.62)}" y="${lnF(gy - gr * 0.62)}" width="${lnF(gr * 1.24)}" height="${lnF(gr * 1.24)}"`)}</g>`;
  }
  return s;
}
// Age labels: in the lived part a readable step (1, 2, 5, 10 or 20 years, at least 46 px apart, 44 on a phone); in the fog the
// decades ahead, folded and fading with distance (thinned to every 20 or 50 years when they would crowd).
function lnTicks(now, over, S, ly, nx) {
  const { X, x0, xN } = S, ppy = now > 0 ? (xN - x0) / now : 0, gap = ly.sm ? 44 : 46, half = (a) => String(a).length * 3.3 + 1;
  const nowA = Math.floor(now + 1e-6), nowHalf = half(nowA);
  const step = [1, 2, 5, 10, 20, 25, 50].find((k) => k * ppy >= gap) || 100;
  let lived = "", grid = "", ahead = "";
  if (now > 0) for (let a = 0; a <= now + 1e-6; a += step) {
    const x = X(a);
    grid += `<line class="grid" x1="${lnF(x)}" x2="${lnF(x)}" y1="${lnF(ly.top)}" y2="${lnF(ly.bot)}"/>`;
    if (a === nowA || Math.abs(nx - x) < nowHalf + half(a) + 6) continue;
    lived += `<text class="tick known" x="${lnF(x)}" y="${ly.tickY}">${a}</text>`;
  }
  if (!over) {
    const fg = 26, px = (a) => Math.min(X(a), S.xE - half(a) + 8), far = (a) => now > 0 ? px(a) - nx >= nowHalf + half(a) + 8 : true;
    let as = [];
    for (const k of [10, 20, 50]) {
      as = []; for (let a = (Math.floor(now / k) + 1) * k; a <= SPAN; a += k) if (far(a)) as.push(a);
      if (as.every((a, i) => !i || px(a) - px(as[i - 1]) >= fg)) break;
    }
    for (const a of as) {
      const t = (a - now) / Math.max(1, SPAN - now);
      ahead += `<text class="tick fut" x="${lnF(px(a))}" y="${ly.tickY}" style="opacity:${(0.85 - 0.6 * t).toFixed(2)}">${a}</text>`;
    }
  }
  return { lived, grid, ahead, nowA };
}
// The hover: crosshair on the nearest river row and its tooltip, over the lived part only. The tip goes under the strip,
// so it never covers the year being read. Kept across redraws while the pointer rests on the river.
function lnHoverShow() {
  const G = lineGeo, h = lnHoverShow.at, cross = $("cross");
  if (!G || !h || !cross) return;
  const age = clamp(G.A(h.x), 0, G.now), R = G.R;
  let html, cx;
  if (R.length) {
    let best = R[0]; for (const row of R) if (Math.abs(row[0] - age) < Math.abs(best[0] - age)) best = row;
    cx = G.X(best[0]);
    const cs = lettersOf(best[8]);
    html = tipBox(`Age ${Math.round(best[0])}`, cs.length ? `${pips(cs)} ${esc((hud.life.guilds || {})[best[8]] || best[8])}` : "Colors still forming",
      [], bars(COLORS.map((c, i) => [CNAME[c], best[1 + i] / 0.6, `var(--c${c})`, pct(best[1 + i])]).concat([["Satisfaction", best[6], "var(--sat)", pct(best[6])], ["Peace", best[7], "var(--peace)", pct(best[7])]])) + "<p>The river swells when life is satisfying. Click to read that year.</p>");
  } else {
    cx = G.X(age);
    html = tipBox(`Age ${Math.round(age)}`, "Colors still forming", [], "The river takes its colors as the years leave their marks. Click to read that year.");
  }
  cross.setAttribute("x1", lnF(cx)); cross.setAttribute("x2", lnF(cx)); cross.setAttribute("visibility", "visible");
  showTipAt(html, h.cx, h.bottom);
  if (parseFloat(tipEl.style.top) < h.bottom) tipEl.style.top = h.bottom + 6 + "px";
}
function lnHoverOff() {
  if (!lnHoverShow.at) return;
  lnHoverShow.at = null;
  const cross = $("cross"); if (cross) cross.setAttribute("visibility", "hidden");
  if (tipOwner === "line") hideTip();
}
// Listeners live on the persistent svg (one set, delegated), so a redraw every few hundred ms costs no rebinding.
function lnWire() {
  if (lnWire.on) return;
  lnWire.on = true;
  const svgX = (e, r) => (e.clientX - r.left) * ((lineGeo ? lineGeo.W : r.width) / (r.width || 1));
  riverEl.addEventListener("pointermove", (e) => {
    if (!e.target || e.target.id !== "lineHov") { lnHoverOff(); return; }
    const r = riverEl.getBoundingClientRect();
    lnHoverShow.at = { x: svgX(e, r), cx: e.clientX, bottom: r.bottom };
    lnHoverShow();
  });
  riverEl.addEventListener("pointerleave", lnHoverOff);
  riverEl.addEventListener("click", (e) => {
    const G = lineGeo; if (!G || !e.target || !e.target.closest) return;
    const g = e.target.closest(".gl[data-age]");
    if (g) { const a = +g.dataset.age, xs = G.byAge.get(a) || []; hideTip(); openYear(a, xs[0] && xs[0]._i); return; }
    if (e.target.id === "lineHov") { const x = svgX(e, riverEl.getBoundingClientRect()); lnHoverOff(); hideTip(); openYear(Math.round(clamp(G.A(x), 0, G.now))); }
  });
}
function drawLine() {
  const W = Math.max(260, lineEl.clientWidth), H = Math.max(48, lineEl.clientHeight);
  const L = hud && hud.life, over = !!(hud && hud.mode === "over"), lived = !!(L && L.w);
  const now = lived ? Math.max(0, +L.age || 0) : 0, pad = W < 600 ? 12 : 16;
  const S = lnScale(W, pad, now, over), X = S.X, ly = lnLayout(H), nx = X(now);
  const R = (lived && L.river) || [];
  const byAge = new Map();
  for (const it of MARKS) { const a = Math.floor(it.age); if (!byAge.has(a)) byAge.set(a, []); byAge.get(a).push(it); }
  const tk = lnTicks(now, over, S, ly, nx);
  let s = `<defs>${COLORS.map((c) => `<linearGradient id="lg${c}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="var(--c${c})" stop-opacity="0.96"/><stop offset="1" stop-color="var(--c${c})" stop-opacity="0.74"/></linearGradient>`).join("")}</defs>`;
  s += tk.grid;
  if (lived && !over) s += `<path class="path" d="M${lnF(nx)} ${lnF(ly.mid)}L${lnF(S.xE)} ${lnF(ly.mid)}"/>`;
  if (lived) s += lnRiver(L, R, now, X, ly) + lnBand(R, now, X, ly);
  s += tk.lived;
  const y1 = ly.top - 3, y2 = ly.bandY + ly.bandH + 3;
  s += `<line class="cross" id="cross" x1="0" x2="0" y1="${lnF(y1)}" y2="${lnF(y2)}" visibility="hidden"/>`;
  s += `<rect class="hov" id="lineHov" x="${lnF(S.x0)}" y="0" width="${lnF(lived ? Math.max(0, nx - S.x0) : 0)}" height="${lnF(y2 + 1)}"/>`;
  s += lnGlyphs(byAge, now, X, ly, W);
  // now: a gold line and a glowing bead on the river (drawn above the fog), at the end of a life the candle
  const nowLine = `<line class="nowg" x1="${lnF(nx)}" x2="${lnF(nx)}" y1="${lnF(y1)}" y2="${lnF(y2)}"/><line class="nowl" x1="${lnF(nx)}" x2="${lnF(nx)}" y1="${lnF(y1)}" y2="${lnF(y2)}"/>` +
    `<text class="nowt" x="${lnF(Math.min(nx, W - 6 - String(tk.nowA).length * 3.4))}" y="${ly.tickY}">${tk.nowA}</text>`;
  if (lived && over) {
    const cr = ly.sm ? 7 : 9;
    s += nowLine + `<g class="gl end"><circle cx="${lnF(nx)}" cy="${lnF(ly.mid)}" r="${cr}"/>${useIc(GI.tag.death || "candle", `x="${lnF(nx - cr * 0.68)}" y="${lnF(ly.mid - cr * 0.68)}" width="${lnF(cr * 1.36)}" height="${lnF(cr * 1.36)}"`)}</g>`;
  }
  riverEl.setAttribute("viewBox", `0 0 ${W} ${H}`);
  riverEl.innerHTML = s;
  // above the fog: the identity thread going on into the unwritten years from who they are now, the decades ahead, now
  let ah = tk.ahead;
  if (lived && !over) {
    const xe = S.xE, y = lnF(ly.bandY + ly.bandH / 2), lc = lettersOf(L.label), c0 = lc.length ? `var(--c${lc[lc.length - 1]})` : "#d6cdf5";
    ah = `<defs><linearGradient id="aheadG" gradientUnits="userSpaceOnUse" x1="${lnF(nx)}" x2="${lnF(xe)}" y1="0" y2="0"><stop offset="0" style="stop-color:${c0};stop-opacity:0.85"/><stop offset="0.2" style="stop-color:#d6cdf5;stop-opacity:0.3"/><stop offset="1" style="stop-color:#d6cdf5;stop-opacity:0.06"/></linearGradient></defs>` +
      `<line class="thread" x1="${lnF(nx)}" x2="${lnF(xe)}" y1="${y}" y2="${y}" stroke="url(#aheadG)"/><line class="threadsh" x1="${lnF(nx)}" x2="${lnF(xe)}" y1="${y}" y2="${y}"/>` + ah +
      nowLine + `<circle class="nowhalo" cx="${lnF(nx)}" cy="${lnF(ly.mid)}" r="${ly.sm ? 6 : 8.5}"/><circle class="nowdot" cx="${lnF(nx)}" cy="${lnF(ly.mid)}" r="${ly.sm ? 2.8 : 3.6}"/>`;
  }
  aheadEl.setAttribute("viewBox", `0 0 ${W} ${H}`);
  aheadEl.innerHTML = ah;
  cosmos(W, H);
  fogEl.style.left = Math.max(0, nx - 30) + "px";
  lineEl.classList.toggle("clear", over);
  lineEl.classList.toggle("nofogword", !over && S.xE - nx < 150);     // too little fog for the word UNWRITTEN
  lineGeo = { X, A: S.A, pad, W, now, R, byAge };
  lnWire();
  riverEl.querySelectorAll(".gl[data-age]").forEach((g) => {
    const xs = byAge.get(+g.dataset.age) || [];
    setTip(g, () => tipBox(`Age ${g.dataset.age}`, "", xs.slice(0, 5).map((it) => [ic(iconFor(it)), esc(trunc(plainText(it.text), 110))]), "Click to read it in the story."));
  });
  if (lnHoverShow.at) { if (lived && lnHoverShow.at.x <= nx) lnHoverShow(); else lnHoverOff(); }
}
const trunc = (s, n) => s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, "") + "…" : s;
// The unwritten years as a cosmic fabric (Emren 10-07 01:57, N2a): stars, some twinkling, constellations in the five
// colors that come and go like lives that could be, and four-pointed sparks. Drawn once per size, anchored to the right
// edge of the line, so the fog uncovers the same sky as the life moves on.
function cosmos(W, H) {
  const el = $("cosmos");
  if (!el || (cosmos.w === W && cosmos.h === H)) return;
  cosmos.w = W; cosmos.h = H;
  let seed = 20261007; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const hue = ["W", "U", "B", "R", "G"], f = (v) => v.toFixed(1);
  let s = "";
  const n = Math.round((W * H) / 700);
  for (let i = 0; i < n; i++) {
    const x = rnd() * W, y = rnd() * H, r = 0.3 + Math.pow(rnd(), 3) * 1.2, tw = rnd() < 0.4, c = rnd() < 0.16 ? `var(--c${hue[Math.floor(rnd() * 5)]})` : "#ece6ff";
    s += `<circle${tw ? ' class="tw"' : ""} cx="${f(x)}" cy="${f(y)}" r="${r.toFixed(2)}" style="fill:${c};opacity:${(0.25 + rnd() * 0.6).toFixed(2)}${tw ? `;animation-delay:-${(rnd() * 8).toFixed(1)}s;animation-duration:${(2.5 + rnd() * 5).toFixed(1)}s` : ""}"/>`;
  }
  const k = Math.max(3, Math.round(W / 220));
  for (let j = 0; j < k; j++) {
    let x = W * (0.12 + 0.85 * rnd()), y = H * (0.2 + 0.6 * rnd());
    const pts = [[x, y]];
    for (let m = 0, mm = 3 + Math.floor(rnd() * 3); m < mm; m++) { x += 14 + rnd() * 34; y = clamp(y + (rnd() - 0.5) * 40, 8, H - 8); pts.push([x, y]); }
    const c = hue[j % 5], d = (rnd() * 14).toFixed(1);
    s += `<g class="con" style="--cc:var(--c${c});animation-delay:-${d}s"><polyline points="${pts.map((p) => f(p[0]) + "," + f(p[1])).join(" ")}"/>${pts.map((p) => `<circle cx="${f(p[0])}" cy="${f(p[1])}" r="1.3"/>`).join("")}</g>`;
  }
  for (let j = 0, m = Math.max(4, Math.round(W / 130)); j < m; j++) {
    const x = W * (0.08 + 0.9 * rnd()), y = H * (0.12 + 0.76 * rnd()), z = 2.5 + rnd() * 3.5, q = z * 0.22;
    s += `<path class="spark" style="animation-delay:-${(rnd() * 9).toFixed(1)}s;animation-duration:${(6 + rnd() * 6).toFixed(1)}s" d="M${f(x)} ${f(y - z)}L${f(x + q)} ${f(y - q)}L${f(x + z)} ${f(y)}L${f(x + q)} ${f(y + q)}L${f(x)} ${f(y + z)}L${f(x - q)} ${f(y + q)}L${f(x - z)} ${f(y)}L${f(x - q)} ${f(y - q)}Z"/>`;
  }
  el.setAttribute("viewBox", `0 0 ${W} ${H}`); el.style.width = W + "px";
  el.innerHTML = s;
}
(function motes() { for (let i = 0; i < 14; i++) { const b = document.createElement("b"); b.style.left = (8 + Math.random() * 88) + "%"; b.style.top = (10 + Math.random() * 78) + "%"; b.style.animationDelay = (Math.random() * 6).toFixed(2) + "s"; b.style.animationDuration = (4 + Math.random() * 5).toFixed(2) + "s"; fogEl.appendChild(b); } })();
let lineTimer = 0;
function scheduleLine() { if (lineTimer) return; lineTimer = requestAnimationFrame(() => { lineTimer = 0; drawLine(); }); }
new ResizeObserver(() => scheduleLine()).observe(lineEl);

/* ---------------- header and tools ---------------- */
$("brandPips").innerHTML = COLORS.map((c) => pip(c)).join("");
const SETTING_ICON = { earth: "globe", tribal: "flame", magic: "star", ...GI.setting, custom: "sliders" };
// 5.5: the name is who they have settled into, from the colors of the last four years
const NAME_NOTE = "The name comes from their colors over the last four years: a color joins above 22% and leaves below 18%.";
const SETTING_NAME = { earth: "Modern Earth", tribal: "Tribal", magic: "A world of magic" };
function renderWho(L) {
  if (!L) { whoEl.innerHTML = ""; return; }
  const lc = labelColors(L.label);
  whoEl.innerHTML = `<span class="nm">${esc(L.name)}</span><span class="age"><b>${Math.floor(L.age)}</b><small>${esc(L.stage || "")}</small></span>` +
    `<span class="crest">${lc.length ? pips(lc) : pip("W", "dim")}<span class="gn">${esc(L.guild || "Still forming")}</span></span>`;
  setTip(whoEl.querySelector(".crest"), () => tipBox(`${pips(lc)} ${esc(L.guild || "Still forming")}`, L.label ? esc(L.meaning || "") : "Too young for a formed identity yet.",
    L.label ? [["Colors", lc.map((c) => CNAME[c]).join(", ")]].concat(L.magic ? [["In Magic: The Gathering", esc(L.magic)]] : []) : [],
    L.label ? NAME_NOTE : "An identity forms once enough has happened to them."));
  if (L.voice) {
    const vs = COLORS.map((c, i) => [c, L.voice[i]]).sort((a, b) => b[1] - a[1]);
    document.documentElement.style.setProperty("--t1", `var(--c${vs[0][0]})`);
    document.documentElement.style.setProperty("--t2", `var(--c${vs[1][0]})`);
  }
}
// v22 next look (Emren chose it 10-07 10:19): three labelled doors (Character, Book, World) and one Table menu for every
// setting; the menu stays open across state updates until it is closed
let menuOpen = false;
function renderTools(h) {
  const L = h && h.life;
  if (!L || !["play", "over"].includes(h.mode)) { toolsEl.innerHTML = ""; menuOpen = false; return; }
  const story = ["quiet", "normal", "every week"][L.detail];
  const row = (attr, icon, label, val, extra = "") => `<button class="mrow2" ${attr} role="menuitem"${extra}>${ic(icon)}<span class="t">${label}</span>${val != null ? `<span class="v">${val}</span>` : ""}</button>`;
  toolsEl.innerHTML = `
    <span class="savednote" id="savedNote" aria-live="polite">${autoOn ? `${ic("check")}<span>Saved after the last choice</span>` : ""}</span>
    <button class="tbtn hud-toggle" id="tHud" aria-pressed="${hudEl.classList.contains("open")}">${ic("wheel")}<span class="t">Status</span></button>
    <button class="tbtn door" data-page="c">${ic("ci-diary")}<span class="t">Character</span><kbd>c</kbd></button>
    <button class="tbtn door" data-page="b">${ic("ci-bookshelf")}<span class="t">Book</span><kbd>b</kbd></button>${h.world || L.world_era ? `
    <button class="tbtn door" data-page="g">${ic("ci-globe")}<span class="t">World</span><kbd>g</kbd></button>` : ""}
    <button class="tbtn door" id="tMenu" aria-haspopup="menu" aria-expanded="${menuOpen}">${ic("sliders")}<span class="t">Table</span></button>
    <div class="tpop" id="tPop" role="menu" aria-label="Table settings"${menuOpen ? "" : " hidden"}>
      <div class="pk">How the life is told</div>
      ${row('data-key="f"', "flag", "Moments", L.freq)}
      ${row(`data-key="k" aria-pressed="${!!L.asks}"`, "heart", "When it matters to them", L.asks ? "asks more" : "off")}
      ${row('data-key="v"', "eye", "Story detail", story)}
      ${row('data-page="i"', "hourglass", "Interlude", PACE_WORD[ilPace])}
      ${row(`data-key="l" aria-pressed="${!!L.ledger}"`, "book", "Numbers under the story", L.ledger ? "on" : "off")}
      <div class="pk">This life</div>
      ${row(`data-page="a" aria-pressed="${autoOn}"`, "check", "Autosave after each choice", autoOn ? "on" : "off")}
      ${row(`data-page="s" id="tSave"${h.mode !== "play" ? " disabled" : ""}`, "ci-sealed-scroll", "Save to a file", "s")}
      ${row('data-page="o"', "ci-open-chest", "Load a life", "o")}
      ${row('data-page="n"', "new", "New life", "n")}
      ${row('id="tHelp"', "help", "Keys", "h")}
    </div>`;
  const tipsT = { f: () => tipBox(`${ic("flag")} Checkpoints: ${L.freq}`, "", [], "How often the life stops for you to steer: rare, normal, often or every moment. Key f."),
    k: () => tipBox(`${ic("heart")} When it matters: ${L.asks ? "on" : "off"}`, "", [], "When on, a moment that touches what matters to them now (the next step of an aim, a need they lack, the people in their life) comes to you more often. Key k."),
    v: () => tipBox(`${ic("eye")} Story: ${story}`, "", [], "How much of daily life the story tells: quiet, normal or every week. Key v."),
    l: () => tipBox(`${ic("book")} Ledger ${L.ledger ? "on" : "off"}`, "", [], "Show the engine's numbers under the story. Key l."),
    i: () => tipBox(`${ic("hourglass")} Interlude: ${PACE_WORD[ilPace]}`, "", [], "The everyday life between two moments: slow, short or off. Key i."),
    c: () => tipBox(`${ic("ci-diary")} Character sheet`, "", [], "Everything about them on one page. Key c."),
    b: () => tipBox(`${ic("ci-bookshelf")} The Book of Moments`, "", [], "What all your lives have met: moments (rare ones starred), identities, deeds and titles. Key b."),
    s: () => tipBox(`${ic("ci-sealed-scroll")} Save`, autoOn ? "Autosave is on" : "Autosave is off", [], `Save this life to a file. Key s.<br>${autoOn ? "After every moment and every choice the life is also kept in one slot in this browser, overwritten each time; Continue on the start screen opens it." : "Nothing is kept in this browser between choices."} Key a turns autosave ${autoOn ? "off" : "on"}.`),
    o: () => tipBox(`${ic("ci-open-chest")} Load`, "", [], "Load a saved life from its file. Key o."),
    n: () => tipBox(`${ic("new")} New life`, "", [], "Leave this life and choose a new start; you can save it first. Key n."),
    g: () => tipBox(`${ic("ci-globe")} The world`, L.world_era ? esc(cap(L.world_era.name)) : "", [], "What is publicly true now and what has happened, by age and era. Key g.") };
  tipsT.a = () => tipBox(`${ic("check")} Autosave ${autoOn ? "on" : "off"}`, "", [], "After every moment and every choice the life is kept in one slot in this browser, overwritten each time; Continue on the start screen opens it. Key a.");
  const inMenu = (b) => !!b.closest("#tPop");
  toolsEl.querySelectorAll("[data-key]").forEach((b) => { b.addEventListener("click", (e) => { e.stopPropagation(); send(b.dataset.key); }); if (!inMenu(b)) setTip(b, tipsT[b.dataset.key]); });
  toolsEl.querySelectorAll("[data-page]").forEach((b) => { b.addEventListener("click", (e) => { e.stopPropagation(); const k = b.dataset.page; if (!["i", "a"].includes(k)) setMenu(false); pageKey(k); }); if (!inMenu(b)) setTip(b, tipsT[b.dataset.page]); });
  $("tHelp").addEventListener("click", (e) => { e.stopPropagation(); setMenu(false); openHelp(); });
  $("tMenu").addEventListener("click", (e) => { e.stopPropagation(); hideTip(); setMenu(!menuOpen); });
  $("tPop").addEventListener("click", (e) => e.stopPropagation());
  setTip($("savedNote"), () => tipsT.s());
  setTip($("tHud"), () => tipBox(`${ic("wheel")} Status`, "", [], "Colors, mood, means, titles and people."));
  $("tHud").addEventListener("click", (e) => { e.stopPropagation(); hideTip(); hudEl.classList.toggle("open"); $("tHud").setAttribute("aria-pressed", hudEl.classList.contains("open")); });
}
function setMenu(on) {
  menuOpen = !!on; const p = $("tPop"), b = $("tMenu"); if (menuOpen) hideTip();
  if (p) p.hidden = !menuOpen; if (b) b.setAttribute("aria-expanded", menuOpen);
  if (menuOpen && p) { const f = p.querySelector("button:not([disabled])"); if (f && !touchUI) f.focus({ preventScroll: true }); }
}
function closeHud() { hudEl.classList.remove("open"); hideTip(); const t = $("tHud"); if (t) t.setAttribute("aria-pressed", "false"); }
document.addEventListener("click", (e) => {
  if (hudEl.classList.contains("open") && !e.target.closest("#hud, #tHud")) closeHud();
  if (menuOpen && !e.target.closest("#tPop, #tMenu")) setMenu(false);
});

