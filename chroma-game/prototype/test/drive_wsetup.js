const { chromium } = require(process.env.PW || 'playwright');
// Release row W41 in the browser: Build your own with the world's setup (the times, technology), a life lived a few
// years, the world it leaves kept in this browser, then a second life in that earlier world. Needs a build whose engine
// has the world (P["world"]). Screenshots of each world step, the opening lines and the World panel of both lives.
//   node test/drive_wsetup.js <url> <shots dir> <width> <height>
const [url, dir, W, H] = process.argv.slice(2);
const { idleOf, nextOf } = require('./start.js');
(async () => {
  const phone = +W < 600, logs = [], out = {};
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +W, height: +H }, hasTouch: phone, isMobile: phone });
  await ctx.addInitScript(() => { try { localStorage.setItem('chroma.pace', 'off'); } catch (_) {} });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/CERT|net::/.test(m.text())) logs.push('console: ' + m.text()); });
  const shot = (n) => page.screenshot({ path: `${dir}/ws${phone ? 'p' : 'd'}-${n}.png` });
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const vis = (sel) => page.evaluate((q) => [...document.querySelectorAll(q)].some((e) => e.offsetParent !== null), sel);
  async function build(name, answers) {
    await page.waitForSelector('.tarot', { timeout: 120000 }); await page.waitForTimeout(600);
    const card = '.tarot[data-k="7"]';
    await page.click(card);
    for (let i = 0; i < 3 && !(await page.$('#txt')); i++) { await page.waitForTimeout(500); const b = await page.$('#begin'); if (b) await b.click(); else await page.click(card); }
    await page.waitForSelector('#txt', { timeout: 30000 });
    await page.fill('#txt', name); await page.click('#go');
    const seen = [];
    for (let s = 0; s < 16; s++) {
      await page.waitForFunction(() => [...document.querySelectorAll('.ch:not(:disabled), #txt:not(:disabled), #go:not(:disabled), #tMain, .opt')].some((e) => e.offsetParent !== null), null, { timeout: 600000 });
      await page.waitForTimeout(250);
      if (await vis('#tMain, .opt, #goOn')) break;
      const st = await page.evaluate(() => ({ q: (document.querySelector('.setup h2') || {}).innerText || '', ttl: (document.querySelector('.setup .ttl') || {}).innerText || '', ch: [...document.querySelectorAll('.ch')].map((b) => b.innerText.replace(/\s+/g, ' ')) }));
      seen.push(st.q.replace(' ?', ''));
      const a = Object.keys(answers).find((k) => st.q.startsWith(k));
      if (a) { out[name + ':' + a] = st; await shot(`${name}-${a.replace(/\W+/g, '')}`); }
      if (a && (await vis('.ch'))) { const i = st.ch.findIndex((x) => x.startsWith(answers[a])); await (await page.$$('.ch'))[i < 0 ? 0 : i].click(); continue; }
      if (await vis('.ch')) await (await page.$$('.ch'))[0].click(); else await page.click('#go');
    }
    out[name + ':steps'] = seen;
    await page.waitForFunction(() => [...document.querySelectorAll('#tMain, .opt, #goOn')].some((e) => e.offsetParent !== null), null, { timeout: 180000 });
  }
  async function live(toAge) {
    for (let i = 0; i < 400; i++) {
      const a = await page.evaluate(() => hud && hud.life ? hud.life.age : 0);
      if (a >= toAge) break;
      const s = await page.evaluate(() => { const w = document.getElementById('evwrap'); return { open: !w.hidden || !!document.querySelector('#goOn') }; });
      if (!s.open && a < toAge - 1.5) { const y = await page.$('.steps4 button[data-key="y"]:not([disabled])'); if (y) { await y.click(); await idle(); continue; } }
      await next();
    }
  }
  const lines = () => page.evaluate(() => [...document.querySelectorAll('#feed .en')].map((e) => e.innerText.replace(/\s+/g, ' ')).filter((x) => /born in|moves to|remembers|old wound|been here before|old hurt|done this before|good memory/.test(x)).slice(0, 8));
  await page.goto(url);
  await build('Lale', { 'The times': 'Restless', 'Technology': 'Ahead' });
  await live(9);
  out.lale_lines = await lines();
  await settle();
  async function settle() { for (let i = 0; i < 3; i++) { if (await vis('#goOn')) { await page.click('#goOn'); await idle(); } else if (await vis('#evPeek')) { await page.click('#evPeek'); await page.waitForTimeout(300); } } }
  await page.keyboard.press('g'); await page.waitForTimeout(700); await shot('lale-world');
  out.lale_world = await page.evaluate(() => (document.querySelector('.worldp, #sheet, .sheet') || document.body).innerText.replace(/\s+/g, ' ').slice(0, 500));
  await page.keyboard.press('Escape'); await page.waitForTimeout(300);
  // the world Lale leaves (a finished life sends it by itself; here it is asked for at 9)
  await page.evaluate(() => worker.postMessage({ cmd: 'world_out' }));
  await page.waitForFunction(() => { try { return !!JSON.parse(localStorage.getItem('chroma.world.last') || 'null'); } catch (_) { return false; } }, null, { timeout: 60000 });
  out.kept = await page.evaluate(() => localStorage.getItem('chroma.world.last'));
  out.kept_bytes = await page.evaluate(async () => { const m = JSON.parse(localStorage.getItem('chroma.world.last')); const w = await WDB.get(m.key); return w ? w.length : 0; });
  // a new life in that world
  await page.evaluate(() => { send('n'); });
  await page.waitForTimeout(800);
  if (await vis('#nlGo')) await page.click('#nlGo');
  await build('Mira', { 'Which world': 'The world Lale left behind' });
  out.mira_name = await page.evaluate(() => hud.life && hud.life.name);
  await live(3);
  out.mira_lines = await lines();
  await settle();
  await page.keyboard.press('g'); await page.waitForTimeout(700); await shot('mira-world');
  out.mira_world = await page.evaluate(() => (document.querySelector('.worldp, #sheet, .sheet') || document.body).innerText.replace(/\s+/g, ' ').slice(0, 500));
  out.sideways = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  console.log(JSON.stringify(out, null, 1));
  console.log(logs.length ? logs.slice(0, 10).join('\n') : 'no page errors');
  await browser.close();
})();
