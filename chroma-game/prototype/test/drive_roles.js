// titles and perks in the browser: play to about 35, then the HUD sockets, statuses and perks, a marked story line, and an option row
const { chromium } = require(process.env.PW || 'playwright');
const { startLife } = require('./start.js');   // the tarot start screen (release row G8)
const url = process.argv[2]; const tag = process.argv[3] || 'r';
const width = parseInt(process.argv[4] || '1280'); const height = parseInt(process.argv[5] || '860');
const dir = process.argv[6]; const preset = process.argv[7] || '3'; const until = parseFloat(process.argv[8] || '35');
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600;
  const page = await browser.newPage({ viewport: { width, height }, colorScheme: 'dark', hasTouch: phone, isMobile: phone });
  const logs = [];
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') logs.push('console ' + m.type() + ': ' + m.text()); });
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 120000 }).catch(() => logs.push('no menu'));
  const idle = async () => { await page.waitForTimeout(150); await page.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => logs.push('timeout idle')); await page.waitForTimeout(200); };
  await startLife(page, preset, 'Lale');
  await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 60000 }); await idle();
  const state = () => page.evaluate(() => ({ cp: !!document.querySelector('.opt'), res: !!document.querySelector('#goOn') }));
  const next = async () => { const s = await state(); if (s.res) await page.click('#goOn'); else if (s.cp) await page.click('#evLet'); else await page.click('#tMain'); await idle(); };
  let rows = 0;
  for (let i = 0; i < 120; i++) {
    await next();
    const age = await page.evaluate(() => parseFloat((document.querySelector('.who .age b') || {}).textContent || '0'));
    const s = await state();
    if (s.cp && !rows) { rows = await page.evaluate(() => document.querySelectorAll('.opt .rb').length); if (rows) { await page.screenshot({ path: `${dir}/${tag}-opt.png` }); if (!phone) { const rb = await page.$('.opt .rb'); const b = await rb.evaluateHandle(e => e.closest('.opt')); await b.hover(); await page.waitForTimeout(350); await page.screenshot({ path: `${dir}/${tag}-opttip.png` }); await page.mouse.move(5, 5); } } }
    if (age >= until) break;
  }
  const s2 = await state(); if (s2.cp || s2.res) { await page.click('#evPeek').catch(() => {}); await page.waitForTimeout(300); }
  const info = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
    socks: [...document.querySelectorAll('.sock.on .tn')].map(e => e.textContent), stats: [...document.querySelectorAll('.perk.stat')].map(e => e.textContent),
    perks: [...document.querySelectorAll('.perk:not(.stat)')].map(e => e.textContent + (e.className.includes('rusty') ? '(r)' : '')),
    omarks: document.querySelectorAll('.mk-o').length, roleLines: document.querySelectorAll('.en.role').length,
    roleText: [...document.querySelectorAll('.en.role')].slice(-6).map(e => e.innerText.replace(/\n/g, ' ').slice(0, 90)) }));
  console.log(JSON.stringify(info, null, 1));
  if (phone) { const t = await page.$('#tHud'); if (t) { await t.click(); await page.waitForTimeout(400); } }
  await page.screenshot({ path: `${dir}/${tag}-hud.png` });
  if (!phone) {
    const so = await page.$('.sock.on'); if (so) { await so.hover(); await page.waitForTimeout(300); await page.screenshot({ path: `${dir}/${tag}-socktip.png` }); }
    const pk = await page.$('.perk:not(.stat)'); if (pk) { await pk.hover(); await page.waitForTimeout(300); await page.screenshot({ path: `${dir}/${tag}-perktip.png` }); }
    let rl = []; for (const e of await page.$$('.en.role')) if (await e.isVisible()) rl.push(e);   // a role line in a folded year: open that year
    if (!rl.length) { const all = await page.$$('.en.role'); if (all.length) { const last = all[all.length - 1]; await last.evaluate((e) => { const y = e.closest('.yr.closed'); if (y) y.querySelector('.yh').click(); }); await page.waitForTimeout(250); rl = [last]; } }
    if (rl.length) { const m = await rl[rl.length - 1].$('.mk-o'); await (m || rl[rl.length - 1]).scrollIntoViewIfNeeded(); await (m || rl[rl.length - 1]).hover(); await page.waitForTimeout(350); await page.screenshot({ path: `${dir}/${tag}-linetip.png` }); }
  }
  console.log(logs.join('\n'));
  await browser.close();
})();
