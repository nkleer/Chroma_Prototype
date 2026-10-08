// Shared start for the browser drivers (release row G8): the tarot start screen of version 21 replaced the old menu cards
// (.pc). startLife() waits for the spread, reads the card (desktop: hover picks it, the click begins; touch: the first tap
// reads it, the second begins), names the character and waits for the first state of the life. The everyday interlude is
// switched off so a driver steps quickly; pass { pace: "slow" } to keep it.
//   const { startLife } = require('./start.js'); await startLife(page, '3', 'Lale');
module.exports.startLife = async (page, preset = '1', name = 'Lale', opts = {}) => {
  await page.waitForSelector('.tarot', { timeout: opts.timeout || 120000 });
  await page.evaluate((pace) => { try { localStorage.setItem('chroma.pace', pace); } catch (_) {} ilPace = pace; }, opts.pace || 'off');
  await page.waitForTimeout(600);
  const card = `.tarot[data-k="${preset}"]`;
  await page.click(card);
  for (let i = 0; i < 3 && !(await page.$('#txt')); i++) {
    await page.waitForTimeout(500);
    if (await page.$('#txt')) break;
    const b = await page.$('#begin'); if (b) await b.click(); else await page.click(card);
  }
  await page.waitForSelector('#txt', { timeout: 30000 });
  await page.fill('#txt', name); await page.click('#go');
  // an adult start with the world on a loaded machine can pass 3 minutes
  await page.waitForFunction(() => [...document.querySelectorAll('#tMain, .opt, #goOn')].some((e) => e.offsetParent !== null), null, { timeout: 600000 })
    .catch(async (e) => { await page.screenshot({ path: (process.env.SHOTS || '/tmp') + '/start-stuck.png' }).catch(() => {});
      console.log('start stuck:', await page.evaluate(() => document.body.innerText.replace(/\s+/g, ' ').slice(0, 300)).catch(() => '')); throw e; });
};
// The page is idle when no job runs (the transport shows Pause only while the life is being lived), no choice is in its
// "trying" beat (version 22: the window holds the chosen option about half a second before the outcome) and the window
// is not closing.
module.exports.idleOf = (page, logs = []) => async () => {
  await page.waitForTimeout(150);
  await page.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => logs.push('timeout idle'));
  await page.waitForTimeout(150);
};
// One step on from wherever the page is, as a player would: Go on after an outcome, let them choose at a moment (the
// event window covers the transport since version 14), else live on.
module.exports.nextOf = (page, idle) => async () => {
  if (await page.evaluate(() => document.getElementById('evwrap').classList.contains('peek'))) { await page.click('#evback'); await page.waitForTimeout(200); }
  const s = await page.evaluate(() => ({ res: !!document.querySelector('#goOn') && !document.getElementById('evwrap').hidden,
    cp: !!document.querySelector('#evLet') && !document.getElementById('evwrap').hidden }));
  try { if (s.res) await page.click('#goOn'); else if (s.cp) await page.click('#evLet'); else await page.click('#tMain', { timeout: 30000 }); }
  catch (e) {   // say what covers the page before failing
    const why = await page.evaluate(() => [...document.querySelectorAll('dialog[open], .modal:not([hidden]), #evwrap, #tMain, .dlg:not([hidden])')]
      .map((el) => `${el.tagName}#${el.id}.${el.className} hidden=${el.hidden} vis=${el.offsetParent !== null} ${(el.innerText || '').replace(/\s+/g, ' ').slice(0, 160)}`));
    console.log('nextOf stuck:', JSON.stringify(why));
    if (process.env.SHOTS) await page.screenshot({ path: `${process.env.SHOTS}/stuck-${Date.now()}.png` });
    throw e;
  }
  if (idle) await idle();
};
// Before touching the sheet, the line or the transport: an outcome is closed with Go on, and a moment is set aside with
// "Look at the life" (the event window is modal since version 14; nextOf comes back to the moment).
module.exports.settleOf = (page, idle) => async () => {
  for (let i = 0; i < 3; i++) {
    const s = await page.evaluate(() => { const w = document.getElementById('evwrap');
      return { ev: !w.hidden && !w.classList.contains('peek'), res: !!document.querySelector('#goOn'), cp: !!document.querySelector('#evPeek') }; });
    if (!s.ev) return;
    if (s.res) { await page.click('#goOn'); if (idle) await idle(); continue; }
    if (s.cp) { await page.click('#evPeek'); await page.waitForTimeout(300); }
    return;
  }
};
