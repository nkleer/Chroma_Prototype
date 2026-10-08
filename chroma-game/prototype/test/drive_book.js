const { chromium } = require(process.env.PW || 'playwright');
const dir = process.argv[2] || '.';  // node test/drive_book.js <shots dir>, with test/serve.py or any static server on 8121
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1360, height: 880 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); } catch (_) {} });
  const page = await ctx.newPage();
  const logs = [];
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/CERT|net::/.test(m.text())) logs.push('console: ' + m.text()); });
  const shot = (n) => page.screenshot({ path: `${dir}/${n}.png` });
  await page.goto('http://127.0.0.1:' + (process.env.PORT || 8121) + '/page.html');
  await page.waitForSelector('.tarot', { timeout: 90000 }); await page.waitForTimeout(800);
  await page.hover('.tarot[data-k="3"]'); await page.click('.tarot[data-k="3"]');
  await page.waitForSelector('#txt'); await page.fill('#txt', 'Noor'); await page.click('#go');
  const t0 = Date.now(); let n = 0;
  while (Date.now() - t0 < 1500000) {   // a whole life from 20: about 10 to 20 minutes since the trying beat (v22)
    await page.waitForFunction(() => hud && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 360000 });   // a 20-year past with the world can pass 2 minutes on a loaded machine
    const st = await page.evaluate(() => ({ mode: hud.mode, cp: !!hud.cp, res: !!hud.res, age: hud.life && hud.life.age, book: !!hud.book }));
    if (st.mode === 'over') break;
    if (st.mode !== 'play') { await page.waitForTimeout(300); continue; }
    n++;
    if (n === 6) { await page.evaluate(() => pageKey('b')); await page.waitForTimeout(500); await shot('b1-book-midlife'); await page.evaluate(() => closeBook()); }
    await page.evaluate((s) => send(s.cp || s.res ? '' : 'd'), st);
    await page.waitForTimeout(150);
  }
  await page.waitForTimeout(1200);
  await shot('b2-review');
  await page.evaluate(() => { const r = document.querySelector('.review'); if (r) r.scrollTop = 9999; }); await page.waitForTimeout(300); await shot('b3-review-bottom');
  await page.click('#rvBook'); await page.waitForTimeout(600); await shot('b4-book');
  await page.evaluate(() => { const b = document.querySelector('.bookp'); if (b) b.scrollTop = 9999; }); await page.waitForTimeout(300); await shot('b5-book-bottom');
  const bk = await page.evaluate(() => ({ lives: book.order.length, seen: Object.keys(book.seen).length, size: (localStorage.getItem('chroma.book') || '').length, cat: (localStorage.getItem('chroma.bookcat') || '').length }));
  console.log('book', JSON.stringify(bk));
  await page.evaluate(() => closeBook());
  // a new life from the review: the menu should offer the Book
  await page.click('#again'); await page.waitForSelector('.tarot', { timeout: 60000 }); await page.waitForTimeout(600); await shot('b6-menu-with-book');
  // phone: the Book at 400 wide
  await page.setViewportSize({ width: 400, height: 860 }); await page.waitForTimeout(300);
  await page.click('#mBook'); await page.waitForTimeout(600); await shot('b7-book-phone');
  console.log('scrollWidth', await page.evaluate(() => document.documentElement.scrollWidth));
  console.log('steps', n, 'secs', Math.round((Date.now() - t0) / 1000));
  console.log(logs.join('\n') || 'no page errors');
  await browser.close();
})();
