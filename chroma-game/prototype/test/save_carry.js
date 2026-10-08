const { chromium } = require(process.env.PW || 'playwright');
// v22.1: a life saved by the live v22 page loads in v22.1. On the old page a life is played for a few choices (autosave on,
// as by default), its autosave slot is read and the save (key s, shown as text outside the viewer) is kept as a file; on the new page the slot is put back and
// Continue is clicked, and the saved file is loaded with key o. Both must come back at the same name and age, with the
// same last story line, and play on with no page error.
//   node test/save_carry.js <old url> <new url> <shots dir> [preset] [steps]
const { startLife, idleOf, nextOf } = require('./start.js');
const [oldUrl, newUrl, dir, preset, S] = [process.argv[2], process.argv[3], process.argv[4], process.argv[5] || '1', +(process.argv[6] || 12)];
(async () => {
  const browser = await chromium.launch();
  const logs = [], fails = [];
  const open = async (url) => { const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, acceptDownloads: true }); const p = await ctx.newPage();
    p.on('pageerror', (e) => logs.push(url.slice(-20) + ' pageerror: ' + e.message)); await p.goto(url); return p; };
  const last = (p) => p.evaluate(() => { const ls = [...document.querySelectorAll('#chron p, #chron .ln, #chron div')].map((e) => e.textContent.trim()).filter(Boolean); return ls.slice(-1)[0] || ''; });
  const where = (p) => p.evaluate(() => ({ name: hud.life && hud.life.name, age: hud.life && hud.life.age, mode: hud.mode }));
  // 1. the old page: a life with some choices
  const a = await open(oldUrl);
  await a.evaluate(() => { try { localStorage.removeItem('chroma.autosave'); } catch (_) {} });
  await startLife(a, preset, 'Lale');
  const idleA = idleOf(a, logs), nextA = nextOf(a, idleA); let chose = 0;
  for (let k = 0; k < 400 && chose < S; k++) {
    await idleA();
    if (await a.$('#evLet') && await a.isVisible('#evLet')) { const os = await a.$$('#evOpts .opt:not(.onone)'); if (os.length && chose % 2) { await os[os.length - 1].click(); await a.waitForTimeout(200); const pi = await a.$('#pushIt'); if (pi) await pi.click(); } else await a.click('#evLet'); chose++; continue; }
    await nextA();
  }
  await idleA();
  const slot = await a.evaluate(() => localStorage.getItem('chroma.autosave'));
  const wa = await where(a);
  // outside the claude.ai viewer the page shows the save as text to copy into a file (saveToFile, showSaveText)
  await a.keyboard.press('s'); const txt = await a.waitForSelector('#saveText', { timeout: 20000 }).then((h) => h.inputValue()).catch(() => '');
  const file = txt ? `${dir}/carry.json` : null; if (txt) require('fs').writeFileSync(file, txt); else fails.push('the old page gave no save text');
  if (!slot) fails.push('the old page left no autosave');
  // 2. the new page: Continue from the old autosave
  const b = await open(newUrl);
  await b.evaluate((s) => { localStorage.setItem('chroma.autosave', s); localStorage.setItem('chroma.pace', 'off'); }, slot); await b.reload();
  await b.waitForSelector('#mContinue', { timeout: 120000 }).catch(() => fails.push('no Continue on the new page'));
  await b.click('#mContinue').catch(() => {});
  await b.waitForFunction(() => hud && hud.mode === 'play' && hud.life && hud.life.age > 0 && !busy, null, { timeout: 600000 }).catch(() => fails.push('the new page did not come back from Continue'));
  const wb = await where(b);
  if (wb.name !== wa.name || Math.abs((wb.age || 0) - (wa.age || 0)) > 0.05) fails.push(`Continue came back at ${JSON.stringify(wb)}, saved at ${JSON.stringify(wa)}`);
  const idleB = idleOf(b, logs), nextB = nextOf(b, idleB);
  for (let i = 0; i < 6; i++) {                       // play on a little: a moment is let be, otherwise live on
    await idleB(); await b.waitForTimeout(900);
    if (await b.$('#evLet') && await b.isVisible('#evLet')) { await b.click('#evLet'); continue; }
    if (await b.evaluate(() => document.getElementById('evwrap').hidden)) await nextB(); else { const g = await b.$('#goOn'); if (g) await g.click().catch(() => {}); }
  }
  // 3. the new page: load the old page's file (key o)
  let wc = null;
  if (file) {
    const c = await open(newUrl); await c.waitForSelector('.tarot', { timeout: 120000 });
    const fc = c.waitForEvent('filechooser', { timeout: 20000 }).catch(() => null);
    await c.click('#mLoad').catch(async () => { await c.keyboard.press('o'); });
    const ch = await fc; if (ch) await ch.setFiles(file); else fails.push('no file chooser for load on the new page');
    await c.waitForFunction(() => hud && hud.mode === 'play' && hud.life && hud.life.age > 0 && !busy, null, { timeout: 600000 }).catch(() => fails.push('the new page did not come back from the file'));
    wc = await where(c);
    if (wc.name !== wa.name || Math.abs((wc.age || 0) - (wa.age || 0)) > 0.05) fails.push(`the file came back at ${JSON.stringify(wc)}, saved at ${JSON.stringify(wa)}`);
    await c.screenshot({ path: `${dir}/carry-loaded.png` });
  }
  console.log(JSON.stringify({ saved: wa, continued: wb, loaded: wc, slotBytes: slot ? slot.length : 0 }));
  console.log('fails:', JSON.stringify(fails)); console.log('logs:', JSON.stringify(logs.slice(0, 6)));
  const ok = !fails.length && !logs.some((l) => l.includes('pageerror'));
  console.log(`save_carry: ${ok ? 'PASS' : 'FAIL'}`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
