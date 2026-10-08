// A life in the browser steered toward politics (Emren 10-07: member of parliament and minister reachable in v22): at
// each moment push the option whose success gains a politics-pack title or perk (summits first), else let them choose.
// Screenshots of the first politics moment, the review and the sheet; prints what was pushed and the titles held.
//   node test/drive_politics.js <shots dir> [port] [preset] [width]
const { chromium } = require(process.env.PW || 'playwright');
const { startLife } = require('./start.js');
const dir = process.argv[2] || '.', port = process.argv[3] || '8121', preset = process.argv[4] || '3', W = +(process.argv[5] || 1360);
// the politics pack's titles and perks, from engine_pin/packs/politics/roles.py (ROLES_POLITICS)
const POL = ["campaign organiser", "constituency caseworker", "political adviser", "member of parliament", "minister", "party leader", "head of government", "party official", "lobbyist", "policy analyst", "speechwriter", "pollster", "campaign volunteer", "polling-station volunteer", "mayor", "local party officer", "council candidate", "parliamentary candidate", "mayoral candidate", "former member of parliament", "canvassing", "rousing a crowd", "debating", "fundraising", "coalition building", "handling the press", "constituency casework", "drafting policy", "knowing the rules of the house", "counting the votes", "reading the polls", "writing speeches", "knowing every street", "party nomination", "parliamentary nomination", "the party whip", "registered lobbyist", "a movement behind you", "a parliamentary pass", "a following in the party", "a safe seat", "a reform with your name on it", "a name for straight talk", "a name as a fixer", "allies in the party", "donors", "a loyal campaign team", "friends across the aisle", "officials who trust you", "a campaign war chest", "a list of supporters"];
const TOP = ['head of government', 'minister', 'member of parliament', 'party leader', 'mayor', 'parliamentary candidate'];
(async () => {
  const browser = await chromium.launch();
  const phone = W < 600;
  const ctx = await browser.newContext({ viewport: { width: W, height: phone ? 860 : 880 }, hasTouch: phone, isMobile: phone });
  const page = await ctx.newPage();
  const logs = [];
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/CERT|net::/.test(m.text())) logs.push('console: ' + m.text()); });
  const shot = (n) => page.screenshot({ path: `${dir}/pol-${n}.png` });
  await page.goto(`http://127.0.0.1:${port}/page.html`);
  await startLife(page, preset, 'Mara');
  const t0 = Date.now(); let n = 0, shotCp = false; const pushed = [];
  while (Date.now() - t0 < (+process.env.LS_MS || 2400000)) {
    await page.waitForFunction(() => hud && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 600000 });
    const st = await page.evaluate(([pol, top]) => {
      const cp = hud.cp; let best = null;
      if (cp) for (const o of cp.options || []) for (const x of o.roles_fx || []) {
        if (x.when === 'ok' && x.gain && pol.includes(x.name) && o.n != null) {
          const r = top.includes(x.name) ? top.indexOf(x.name) : top.length;
          if (!best || r < best.r) best = { r, n: o.n, name: x.name };
        }
      }
      return { mode: hud.mode, cp: !!cp, res: !!hud.res, best, age: hud.life ? hud.life.age : 0 };
    }, [POL, TOP]);
    if (st.mode === 'over') break;
    if (st.mode !== 'play') { await page.waitForTimeout(300); continue; }
    n++;
    if (st.best) { pushed.push([Math.floor(st.age), st.best.name]); if (!shotCp) { await page.waitForTimeout(400); await shot('moment'); shotCp = true; } }
    await page.evaluate((s) => send(s.best ? String(s.best.n) : s.cp || s.res ? '' : 'd'), st);
    await page.waitForTimeout(100);
  }
  await page.waitForTimeout(1500); await shot('review');
  const held = await page.evaluate(() => [...document.querySelectorAll('.review .perk, .review .ttl, .review li')].map((e) => e.textContent.trim()).filter(Boolean).slice(0, 40));
  console.log('pushed', JSON.stringify(pushed));
  console.log('review titles', JSON.stringify(held));
  console.log('mode', await page.evaluate(() => hud && hud.mode), 'steps', n, 'secs', Math.round((Date.now() - t0) / 1000));
  console.log('scrollWidth', await page.evaluate(() => document.documentElement.scrollWidth));
  console.log(logs.join('\n') || 'no page errors');
  await browser.close();
})();
