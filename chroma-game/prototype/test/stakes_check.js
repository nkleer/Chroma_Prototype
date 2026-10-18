const { chromium } = require(process.env.PW || 'playwright');
// Stakes on the card: plays one life on the page; at each moment counts the stakes chips (.mk2.stake), the lasting-change
// chips per card (at most 2) and page errors; screenshots two moments. node stakes_check.js <url> <dir> <width> [moments]
const { startLife, idleOf, nextOf } = require('./start.js');
const [url, dir, W, M] = [process.argv[2], process.argv[3], +process.argv[4], +(process.argv[5] || 14)];
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: W, height: 860 } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await startLife(page, '3', 'Lale');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const n = { moments: 0, stake: 0, people: 0, fails: 0, over2: 0, flag: 0 }; let shots = 0; const seen = [];
  for (let k = 0; k < 4000 && n.moments < M; k++) {
    await idle();
    const at = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !!(w && !w.hidden && document.getElementById('evLet') && !document.querySelector('#goOn')); });
    if (!at) { if (await page.evaluate(() => hud && hud.mode !== 'play')) break; try { await next(); } catch (e) { logs.push('next ' + e.message.slice(0, 80)); break; } continue; }
    n.moments++;
    const s = await page.evaluate(() => {
      const cards = [...document.querySelectorAll('#evOpts .opt')];
      return { flag: !!(hud.cp && hud.cp.stake_card), stake: document.querySelectorAll('#evOpts .mk2.stake').length,
        people: [...document.querySelectorAll('#evOpts .mk2.stake:not(.iffail)')].map((e) => e.textContent.trim()),
        fails: [...document.querySelectorAll('#evOpts .mk2.stake.iffail')].map((e) => e.textContent.trim()),
        over2: cards.filter((c) => c.querySelectorAll('.mk2.rb:not(.iffail)').length > 2).length,
        wide: document.documentElement.scrollWidth > window.innerWidth + 1 };
    });
    n.flag += s.flag; n.stake += s.stake; n.people += s.people.length; n.fails += s.fails.length; n.over2 += s.over2;
    if (s.wide) logs.push(`moment ${n.moments}: page wider than the screen`);
    seen.push(...s.people.slice(0, 2), ...s.fails.slice(0, 1));
    if (s.stake && shots < 2) { await page.screenshot({ path: `${dir}/stakes-${W}-${++shots}.png` }); }
    if (shots === 1 && s.stake) {                    // the reading strip and the tooltip for a card with stakes
      const c = await page.$('#evOpts .opt:has(.mk2.stake)'); if (c) { await c.hover(); await page.waitForTimeout(300);
        const strip = await page.evaluate(() => { const d = document.querySelector('.facts'); return d ? d.innerText.replace(/\s+/g, ' ') : ''; });
        seen.push('STRIP: ' + strip.slice(0, 400)); }
    }
    try { await page.click('#evLet'); } catch (e) { logs.push(`moment ${n.moments}: ${e.message.slice(0, 80)}`); }
    await idle();
  }
  console.log(JSON.stringify(n)); console.log(seen.slice(0, 24).join('\n')); console.log(logs.length ? logs.join('\n') : 'no page errors');
  await browser.close();
})();
