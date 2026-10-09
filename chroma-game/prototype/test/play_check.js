const { chromium } = require(process.env.PW || 'playwright');
// Stage 1 of the v22 update, played lives on the page: at each moment of one life (preset 1, 1280x800) the player in
// turn pushes an option that is not their own, leans toward a color with the light steer (the colored buttons beside
// "Let them choose") and lets them choose. Checks: the five lean buttons at every moment; a lean or a push goes through
// to an outcome; the voice row names the voice once it has spoken five times; counts the thread lines (F5), the era tags
// (P3) and the world notes on options (WL3) and in the story (WL1, WL4); no page error.
//   node test/play_check.js <url> <shots dir> [moments]
const { startLife, idleOf, nextOf } = require('./start.js');
const [url, dir, M] = [process.argv[2], process.argv[3], +(process.argv[4] || 24)];
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await startLife(page, '1', 'Mira');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const fails = []; const n = { moments: 0, pushed: 0, leaned: 0, let: 0, thread: 0, era: 0, wcause: 0 }; let voice = '';
  for (let k = 0; k < 4000 && n.moments < M; k++) {
    await idle();
    const at = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !!(w && !w.hidden && document.getElementById('evLet') && !document.querySelector('#goOn')); });
    if (!at) { if (await page.evaluate(() => hud && hud.mode !== 'play')) break; try { await next(); } catch (e) { logs.push('next ' + e.message.slice(0, 80)); break; } continue; }
    n.moments++;
    const s = await page.evaluate(() => ({ lc: document.querySelectorAll('[data-lc]').length, thread: !!document.getElementById('cpThread'),
      era: document.querySelectorAll('.mk2.era').length, wcause: document.querySelectorAll('.mk2.wcause').length }));
    if (s.lc !== 5) fails.push(`moment ${n.moments}: ${s.lc} lean buttons`);
    n.thread += s.thread ? 1 : 0; n.era += s.era ? 1 : 0; n.wcause += s.wcause ? 1 : 0;
    if ([2, 9, 16].includes(n.moments)) await page.screenshot({ path: `${dir}/play-moment-${n.moments}.png` });
    const how = n.moments % 3;
    try {
      if (how === 1) {                               // push an open option that is not their own
        const cards = await page.$$('#evOpts .opt:not(.onone):not(.own):not(.far):not(.ghost)');
        if (cards.length) { await cards[cards.length - 1].click(); n.pushed++; } else { await page.click('#evLet'); n.let++; }
      } else if (how === 2) {
        await page.click(`[data-lc="${'WUBRG'[n.moments % 5]}"]`); n.leaned++;
      } else { await page.click('#evLet'); n.let++; }
    } catch (e) { fails.push(`moment ${n.moments}: ${e.message.slice(0, 80)}`); }
    await idle();
    voice = await page.evaluate(() => { const v = document.getElementById('voiceRow'); return v ? v.textContent.replace(/\s+/g, ' ').trim() : ''; });
  }
  const story = await page.evaluate(() => ({ x: document.querySelectorAll('.mk-X, [data-mk="X"]').length, text: document.body.innerText.length }));
  await page.screenshot({ path: `${dir}/play-end.png` });
  if (n.pushed + n.leaned >= 8 && !/voice/i.test(voice)) fails.push(`no voice named after ${n.pushed} pushes and ${n.leaned} leans: "${voice}"`);
  console.log(JSON.stringify(n), 'voice row:', JSON.stringify(voice.slice(0, 80)), 'world marks:', story.x);
  console.log('fails:', JSON.stringify(fails.slice(0, 6))); console.log('logs:', JSON.stringify(logs.slice(0, 6)));
  const ok = n.moments >= Math.min(M, 12) && !fails.length && !logs.some((l) => l.startsWith('pageerror'));
  console.log(`play_check: ${ok ? 'PASS' : 'FAIL'}`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
