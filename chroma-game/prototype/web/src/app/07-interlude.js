/* ---------------- menu, setup ---------------- */
/* ---------------- points 1 and 2 (Emren 20:39): between two moments, a slow interlude of everyday life. The routine of
   these years (routine.py, read through who they are), the season and age going by, and the colors moving week by week.
   The next moment waits until it ends; Skip (or Enter) ends it at once. ---------------- */
const IL_PACE = { slow: { wk: 120, min: 7000, max: 16000, line: 2700 }, short: { wk: 45, min: 3200, max: 7000, line: 1500 } };
const PACE_WORD = { slow: "slow", short: "short", off: "off" };
let ilPace = "slow"; try { ilPace = localStorage.getItem("chroma.pace") || "slow"; } catch (_) {}
const SEASON = (t) => { const k = ((t % 52) + 52) % 52; return k < 9 || k >= 48 ? "winter" : k < 22 ? "spring" : k < 35 ? "summer" : "autumn"; };
const SEASON_ICON = { winter: "ci-candle", spring: "ci-sapling", summer: "sun", autumn: "leaf" };
const interEl = document.createElement("div"); interEl.className = "inter"; interEl.hidden = true; stageEl.appendChild(interEl);
const IL = { on: false };
let lastSent = "";
function ilPic(L, age) {
  const w = worldCard(L); if (w != null) return w;
  const held = new Set((L.titles || []).map((t) => t.kind));
  const pool = age < 5 ? ["family", "home", "play"] : age < 18 ? ["school", "friends", "play", "family"] :
    [held.has("career") ? "work" : "home", held.has("children") ? "children" : "friends", held.has("partner") ? "partner" : "leisure",
      held.has("faith") ? "faith" : held.has("community") ? "community" : "nature", age >= 66 && !held.has("career") ? "leisure" : "home"];
  const k = pool[Math.floor(age) % pool.length];
  return PICS.domain[k] || PICS.tier.everyday || "";
}
function ilStart(L) {
  const P = IL_PACE[ilPace] || IL_PACE.slow;
  Object.assign(IL, { on: true, frames: [], lines: [], seen: new Set(), shown: 0, t0: performance.now(), last: 0, ended: false, tEnd: 0, k: 0, kt: performance.now(),
    picAge: -1, drawn: 0, base: spOf(L, { id: "il", labels: true }), L });
  // v22 next look: no second wheel. Where the crest is in view its own wheel moves week by week; on narrow screens (the
  // crest is in a drawer) the interlude keeps a small wheel of its own. The season and the year run as a strip.
  IL.side = !$("hudWheel") || $("hudWheel").offsetParent === null || narrow() || window.innerWidth <= 1040;   // one wheel on screen: the crest's when it shows
  IL.hbase = IL.side ? null : spOf(L, { id: "hw", hits: true });
  hudEl.classList.toggle("ilon", !IL.side);
  IL.frames.push(hudLast || { t: Math.round(L.age * 52), w: L.w, want: L.w.map((v, i) => Math.max(0.01, v + L.demand[i])) });
  interEl.innerHTML = `<div class="ilcard">
    <div class="ilpic" id="ilPic"></div>
    <div class="ilmain"><div class="ilkick">${ic("ci-cup")} Everyday life <span class="ilage" id="ilAge"></span></div><div class="illines" id="ilLines"></div></div>
    ${IL.side ? `<div class="ilside"><svg class="wheel" id="ilWheel" viewBox="-6 -2 212 206" aria-hidden="true"></svg></div>` : ""}
    <div class="ilfoot"><div class="ilseason" aria-hidden="true">${[["winter", 9], ["spring", 13], ["summer", 13], ["autumn", 13], ["winter", 4]].map(([s, w], i) => `<span class="sb ${s}" style="flex:${w}">${i === 4 ? "" : `${ic(SEASON_ICON[s])}<em>${cap(s)}</em>`}</span>`).join("")}<i class="ilmark" id="ilMark"></i><b class="ilprog" id="ilBar"></b></div><button class="ghost" id="ilSkip">${ic("step")} Skip</button></div></div>`;
  interEl.hidden = false; interEl.classList.remove("out");
  $("ilSkip").addEventListener("click", ilFinish);
  setTip($("ilSkip"), () => tipBox(`${ic("step")} Skip`, "", [], `Go straight to what comes next. The pace of these interludes is set under ${ic("hourglass")} (key i).`));
  void P; IL.raf = requestAnimationFrame(ilTick);
}
function ilFeed(h) {
  if (!IL.on || !h.life) return;
  for (const f of h.trace || []) IL.frames.push(frameOf(f));
  const r = h.routine;
  if (r && r.lines) for (const x of r.lines) if (!IL.seen.has(x)) { IL.seen.add(x); IL.lines.push({ text: x, age: r.age }); }
  IL.L = h.life;
  if (!h.busy && !IL.ended) {
    const P = IL_PACE[ilPace] || IL_PACE.slow, now = performance.now();
    IL.ended = true;
    IL.tEnd = Math.max(IL.t0 + clamp(IL.frames.length * P.wk, P.min, P.max), now + 900);
    IL.tEnd = Math.max(IL.tEnd, IL.t0 + Math.min(IL.lines.length, 4) * P.line + 600);
  }
}
function ilTick(now) {
  if (!IL.on) return;
  try { ilStep(now); } catch (e) { console.error(e); ilFinish(); }      // a fault in the telling never holds up the life
}
function ilStep(now) {
  const P = IL_PACE[ilPace] || IL_PACE.slow, N = IL.frames.length, dt = Math.max(0, now - IL.kt); IL.kt = Math.max(IL.kt, now);
  const rate = IL.ended ? Math.max(0, N - 1 - IL.k) / Math.max(60, IL.tEnd - now) : 1 / P.wk;
  IL.k = clamp(IL.k + rate * dt, 0, Math.max(0, N - 1));
  if (now - IL.drawn > 40 && N) {
    IL.drawn = now;
    const k = Math.floor(IL.k), f = IL.k - k, A = IL.frames[k], B = IL.frames[Math.min(N - 1, k + 1)];
    const lerp = (a, b) => a.map((v, i) => v + (b[i] - v) * f);
    const svg = IL.side ? $("ilWheel") : $("hudWheel");
    if (svg) svg.innerHTML = spiderSVG({ ...(IL.side ? IL.base : IL.hbase), ...bandsOf(f < 0.5 ? A : B), w: lerp(A.w, B.w), want: lerp(A.want, B.want) });
    const t = A.t + (B.t - A.t) * f, age = t / 52, wkn = ((t % 52) + 52) % 52;
    const mk = $("ilMark"); if (mk) mk.style.left = `${(wkn / 52 * 100).toFixed(2)}%`;
    const ag = $("ilAge"); if (ag) ag.innerHTML = `· age ${Math.floor(age)}, <span id="ilWk">week ${Math.floor(wkn) + 1}</span>`;   // #ilWk kept for the drivers
    if (Math.floor(age) !== IL.picAge) {
      IL.picAge = Math.floor(age);
      const src = ilPic(IL.L, age), box = $("ilPic");
      if (box && src && (!box.dataset.src || box.dataset.src !== src)) {
        box.dataset.src = src;
        const img = document.createElement("img"); img.alt = ""; img.src = src; img.decoding = "async"; img.onerror = () => img.remove();
        box.querySelectorAll("img").forEach((x) => { x.classList.add("gone"); setTimeout(() => x.remove(), 1400); });
        box.prepend(img);
      }
    }
    const bar = $("ilBar"); if (bar) bar.style.width = `${(IL.ended ? clamp((now - IL.t0) / Math.max(1, IL.tEnd - IL.t0)) : Math.min(0.9, (now - IL.t0) / (P.max * 1.4))) * 100}%`;
  }
  if (IL.shown < IL.lines.length && now - IL.last >= P.line) {
    IL.last = now;
    const box = $("ilLines");
    if (box) {
      const p = document.createElement("p"); p.innerHTML = rich(IL.lines[IL.shown].text); box.appendChild(p);
      const all = box.querySelectorAll("p:not(.gone)");
      if (all.length > 4) { all[0].classList.add("gone"); setTimeout(() => all[0].remove(), 900); }
    }
    IL.shown++;
  }
  if (IL.ended && now >= IL.tEnd) return ilFinish();
  IL.raf = requestAnimationFrame(ilTick);
}
function ilFinish() {
  if (!IL.on) return;
  IL.on = false; cancelAnimationFrame(IL.raf); hudEl.classList.remove("ilon");
  interEl.classList.add("out"); setTimeout(() => { if (!IL.on) { interEl.hidden = true; interEl.innerHTML = ""; } }, 500);
  hideTip();
  if (!hud) return;
  hudLast = null; hudFrames = [];
  if (hud.life && hud.life.w) renderHud(hud.life);
  renderTable(hud); renderTransport(); lockInputs(busy);
  if (stick.bottom) chronEl.scrollTop = chronEl.scrollHeight;
}
function ilWanted(h) {
  return busy && h.mode === "play" && h.job === "run" && !h.replay && ilPace !== "off" && !["w", "m"].includes(lastSent) && sentFrom !== "cp" && h.life && h.life.w && !IL.on;
}

