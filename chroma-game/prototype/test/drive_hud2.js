const { chromium } = require(process.env.PW || 'playwright');
const { startLife, nextOf, settleOf } = require('./start.js');   // the tarot start screen (release row G8)
const url = process.argv[2]; const tag = process.argv[3] || 'd';
const width = parseInt(process.argv[4] || '1280'); const height = parseInt(process.argv[5] || '860');
const dir = process.argv[6]; const toEnd = process.argv[7] === 'end';
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600;
  const page = await browser.newPage({ viewport: { width, height }, colorScheme: 'dark', hasTouch: phone, isMobile: phone });
  const logs = [];
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') logs.push('console ' + m.type() + ': ' + m.text()); });
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 90000 }).catch(() => logs.push('no menu'));
  console.log('boot ms', Date.now() - t0);
  await page.waitForTimeout(700);
  await page.screenshot({ path: `${dir}/${tag}-1menu.png` });
  const idle = async () => { await page.waitForTimeout(150); await page.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => logs.push('timeout idle')); await page.waitForTimeout(150); };
  const next = nextOf(page);   // the event window covers #tMain at a moment or an outcome (G8)
  const settle = settleOf(page, idle);
  await startLife(page, '1', 'Lale');
  await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 60000 });
  await idle();
  for (let i = 0; i < 5; i++) { await next(); await idle(); }
  await page.waitForTimeout(700);
  await page.screenshot({ path: `${dir}/${tag}-2cp.png` });
  if (!phone) {
    const c = await page.$('.mtg:nth-child(2)'); if (c) { await c.hover({ position: { x: 22, y: 120 }, force: true }); await page.waitForTimeout(400); await page.screenshot({ path: `${dir}/${tag}-3cardtip.png` }); }
  } else {
    const c = await page.$('.mtg:nth-child(2)'); if (c) { await c.tap(); await page.waitForTimeout(400); await page.screenshot({ path: `${dir}/${tag}-3cardtap.png` }); }
  }
  await page.keyboard.press('Escape');
  await page.keyboard.press('2'); await idle();
  for (let i = 0; i < 8; i++) { await next(); await idle(); }
  await settle(); await page.click('.steps4 button[data-key="d"]').catch(() => {}); await idle();
  for (let i = 0; i < 6; i++) { await next(); await idle(); }
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${dir}/${tag}-4later.png` });
  // hover marked words in the story
  await settle();
  const kinds = ['a', 'p', 't', 'v', 'm', 'r', 'x', 'k'];
  for (const k of kinds) {
    const els = await page.$$(`#feed .yr:not(.closed) .mk-${k}`);
    const el = els[els.length - 1];
    if (!el) { logs.push('no marker ' + k); continue; }
    await el.evaluate((e) => e.scrollIntoView({ block: 'center' })); await page.waitForTimeout(150);
    if (phone) await el.tap({ force: true }); else await el.hover({ force: true });
    await page.waitForTimeout(250);
    const tip = await page.evaluate(() => { const t = document.getElementById('tip'); return t.hidden ? '' : t.innerText.replace(/\s+/g, ' ').slice(0, 160); });
    console.log('mk', k, '=>', tip);
    if (k === 'a') await page.screenshot({ path: `${dir}/${tag}-5mk-act.png` });
  }
  // hover the life line
  if (!phone) {
    const box = await page.$eval('#line', (e) => { const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
    await page.mouse.move(box.x + box.w * 0.12, box.y + box.h * 0.45); await page.waitForTimeout(250);
    await page.screenshot({ path: `${dir}/${tag}-6line.png` });
    const g = await page.$('.river .gl[data-age]'); if (g) { await g.hover(); await page.waitForTimeout(250); await page.screenshot({ path: `${dir}/${tag}-7glyph.png` }); await g.click(); await page.waitForTimeout(600); }
  } else {
    await page.click('#tHud'); await page.waitForTimeout(400); await page.screenshot({ path: `${dir}/${tag}-6hud.png` }); await page.click('#hudClose'); await page.waitForTimeout(400); await page.screenshot({ path: `${dir}/${tag}-6hudclosed.png` });
  }
  if (toEnd) {
    for (let i = 0; i < 400; i++) {
      const over = await page.evaluate(() => document.getElementById('app').dataset.mode === 'over');
      if (over) break;
      const ev = await page.evaluate(() => !document.getElementById('evwrap').hidden);
      const d = !ev && await page.$('.steps4 button[data-key="d"]:not([disabled])');
      if (d) await d.click(); else await next();
      await idle();
    }
    await page.waitForTimeout(2600);
    await page.screenshot({ path: `${dir}/${tag}-8review.png` });
  }
  const info = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, years: document.querySelectorAll('.yr').length, ents: document.querySelectorAll('.en').length, marks: document.querySelectorAll('.river .gl').length, age: document.querySelector('.who .age')?.textContent, mode: document.getElementById('app').dataset.mode }));
  console.log(JSON.stringify(info));
  console.log(logs.slice(0, 20).join('\n'));
  await browser.close();
})();
