const { chromium } = require(process.env.PW || 'playwright');
const { startLife, nextOf, settleOf } = require('./start.js');   // the tarot start screen (release row G8)
const url = process.argv[2]; const tag = process.argv[3] || 'v7';
const width = parseInt(process.argv[4] || '1280'); const height = parseInt(process.argv[5] || '860');
const dir = process.argv[6]; const preset = process.argv[7] || '3';
(async () => {
  const browser = await chromium.launch();
  const phone = width < 600;
  const page = await browser.newPage({ viewport: { width, height }, colorScheme: 'dark', hasTouch: phone, isMobile: phone });
  const logs = [];
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') logs.push('console ' + m.type() + ': ' + m.text()); });
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await page.waitForSelector('.tarot', { timeout: 90000 }).catch(() => logs.push('no menu'));
  const idle = async () => { await page.waitForTimeout(150); await page.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => logs.push('timeout idle')); await page.waitForTimeout(200); };
  const next = nextOf(page);   // the event window covers #tMain at a moment or an outcome (G8)
  const settle = settleOf(page, idle);
  await startLife(page, preset, 'Lale');
  await page.waitForSelector('#tMain, .opt, #goOn', { timeout: 60000 }); await idle();
  const state = () => page.evaluate(() => ({ cp: !!document.querySelector('.opt'), res: !!document.querySelector('#goOn'), voice: !!document.querySelector('.insight'), plan: !document.querySelector('.plan').hidden }));
  // live on to a checkpoint that has an inner voice
  for (let i = 0; i < 30; i++) { const s = await state(); if (s.cp && s.voice) break; await next(); await idle(); }
  await page.waitForTimeout(900);
  await page.screenshot({ path: `${dir}/${tag}-1voice.png` });
  console.log('voice:', await page.evaluate(() => document.querySelector('.insight')?.innerText));
  if (!phone) {
    const tug = await page.$('#tug'); if (tug) { await tug.hover(); await page.waitForTimeout(300); await page.screenshot({ path: `${dir}/${tag}-2tug.png` }); }
    const hc = await page.$('.mtg .hh'); if (hc) { const card = await hc.evaluateHandle((e) => e.closest('.mtg')); await card.asElement().hover({ position: { x: 30, y: 150 }, force: true }); await page.waitForTimeout(400); await page.screenshot({ path: `${dir}/${tag}-3cardtip.png` }); }
  }
  await page.mouse.move(5, 5);
  await page.keyboard.press('Enter'); await idle();
  await page.waitForTimeout(700);
  await page.screenshot({ path: `${dir}/${tag}-4resolution.png` });
  console.log('res:', JSON.stringify(await state()), await page.evaluate(() => document.querySelector('#table')?.innerText.replace(/\s+/g, ' ').slice(0, 400)));
  if (!phone) { const ch = await page.$('#table .chg'); if (ch) { await ch.hover(); await page.waitForTimeout(300); await page.screenshot({ path: `${dir}/${tag}-5chgtip.png` }); } }
  // go on, a few more moments, pushing one
  for (let i = 0; i < 6; i++) {
    const s = await state();
    if (s.cp) { if (i === 2) { await page.keyboard.press('3'); } else { await page.keyboard.press('Enter'); } }
    else await next();
    await idle();
  }
  // the plan dialog: plans are for adults, so live on a while first
  for (let i = 0; i < 40; i++) {
    const adult = await page.evaluate(() => !!document.getElementById('addPlan'));
    if (adult) break;
    const s = await state();
    if (s.cp) await page.keyboard.press('Enter'); else if (s.res) await next(); else { const d = await page.$('.steps4 button[data-key="y"]:not([disabled])'); if (d) await d.click(); else await next(); }
    await idle();
  }
  // the plan dialog
  await settle();
  if (phone) { await page.click('#tHud'); await page.waitForTimeout(400); }
  await page.screenshot({ path: `${dir}/${tag}-6hud.png` });
  const ap = await page.$('#addPlan');
  if (ap) {
    await ap.click(); await idle(); await page.waitForTimeout(300);
    await page.screenshot({ path: `${dir}/${tag}-7plan1.png` });
    await page.click('.plan .ch[data-v="2"]'); await idle();
    await page.screenshot({ path: `${dir}/${tag}-8plan2.png` });
    const free = await page.$(".plan .ch:not([disabled])"); if (free) await free.click(); await idle();
    await page.screenshot({ path: `${dir}/${tag}-9plan3.png` });
    await page.click('#planOk'); await idle();
    await page.waitForTimeout(500);
  } else logs.push('no addPlan button');
  if (phone) { const hc = await page.$('#hudClose'); if (hc) await hc.click().catch(() => {}); await page.waitForTimeout(300); if (await page.$('#tHud')) { await page.click('#tHud'); await page.waitForTimeout(400); } }
  await page.screenshot({ path: `${dir}/${tag}-10hudplan.png` });
  const gr = await page.$('.drm.plan'); if (gr && !phone) { await gr.hover(); await page.waitForTimeout(300); await page.screenshot({ path: `${dir}/${tag}-11goaltip.png` }); }
  if (phone) { const hc = await page.$('#hudClose'); if (hc) await hc.click().catch(() => {}); }
  for (let i = 0; i < 10; i++) { const s = await state(); if (s.cp) await page.keyboard.press('Enter'); else await next(); await idle(); }
  await page.screenshot({ path: `${dir}/${tag}-12later.png` });
  const info = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, goals: document.querySelectorAll('.goal').length, rchips: document.querySelectorAll('.rchips').length, goalEntries: document.querySelectorAll('.en.goal').length, mode: document.getElementById('app').dataset.mode }));
  console.log(JSON.stringify(info));
  console.log(logs.slice(0, 20).join('\n'));
  await browser.close();
})();
