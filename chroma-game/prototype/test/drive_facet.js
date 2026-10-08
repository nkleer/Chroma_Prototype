// titles volume 2 on the page: play until a socket shows a facet (newlywed, single parent...), then hover it
const { chromium } = require(process.env.PW || 'playwright');
const { startLife } = require('./start.js');   // the tarot start screen (release row G8)
const [url, dir, preset, width] = [process.argv[2], process.argv[3], process.argv[4] || '3', parseInt(process.argv[5] || '1280')];
(async () => {
  const b = await chromium.launch(); const phone = width < 600;
  const p = await b.newPage({ viewport: { width, height: phone ? 844 : 860 }, colorScheme: 'dark', hasTouch: phone, isMobile: phone });
  const logs = []; p.on('pageerror', e => logs.push('pageerror: ' + e.message));
  await p.goto(url); await p.waitForSelector('.tarot', { timeout: 120000 });
  await startLife(p, preset, 'Lale');
  await p.waitForSelector('#tMain, .opt, #goOn', { timeout: 60000 });
  const idle = async () => { await p.waitForTimeout(120); await p.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => {}); await p.waitForTimeout(120); };
  let found = null;
  for (let i = 0; i < 400 && !found; i++) {
    const s = await p.evaluate(() => ({ cp: !!document.querySelector('.opt'), res: !!document.querySelector('#goOn'), over: !!document.querySelector('.epi, #again') }));
    if (s.over) break;
    if (s.res) await p.click('#goOn'); else if (s.cp) await p.click('#evLet'); else await p.click('#tMain');
    await idle();
    found = await p.evaluate(() => { const f = document.querySelector('.sock .fc'); return f ? [f.textContent, f.closest('.sock').querySelector('.tn').textContent, document.querySelector('.who .age b').textContent] : null; });
  }
  console.log('facet', JSON.stringify(found));
  const s2 = await p.evaluate(() => !!document.querySelector('.opt') || !!document.querySelector('#goOn'));
  if (s2) { await p.click('#evPeek').catch(() => {}); await p.waitForTimeout(300); }
  if (found) {
    if (phone) { const t = await p.$('#tHud'); if (t) { await t.click(); await p.waitForTimeout(400); } }
    const so = await p.$('.sock .fc'); await so.scrollIntoViewIfNeeded(); 
    if (!phone) { await (await so.evaluateHandle(e => e.closest('.sock'))).hover(); await p.waitForTimeout(350); }
    await p.screenshot({ path: `${dir}/facet${phone ? '-phone' : ''}.png` });
  }
  console.log('sw', await p.evaluate(() => document.documentElement.scrollWidth), logs.join('\n')); await b.close();
})();
