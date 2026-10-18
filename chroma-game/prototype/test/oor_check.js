const { chromium } = require(process.env.PW || 'playwright');
// Next version (N7 leftovers): "Out of reach" folds into one row; its cards are drawn only when open; a number key on a
// folded card opens the fold and focuses that card (a second press pushes); the reading of a focused card stays open
// when the mouse leaves another card. v23: the first fold tried is then opened again by the number and its card pushed by
// holding it (the Living HUD's hold; a click on a page without it), and the push must go through. One life at 1280x800
// (preset 1).
//   node test/oor_check.js <url> <shots dir> [moments]
const { startLife, idleOf, nextOf } = require('./start.js');
const { holdOpt } = require('./hold.js');
const [url, dir, M] = [process.argv[2], process.argv[3], +(process.argv[4] || 12)];
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await page.evaluate(() => { try { localStorage.removeItem('chroma.oorOpen'); } catch (_) {} });
  await startLife(page, '1', 'Mira');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const fails = []; let seen = 0, keyed = 0, focusKept = 0, moments = 0, heldFold = '', reclose = false;
  const strip = () => page.evaluate(() => { const s = document.getElementById('evStrip'); return s && !s.classList.contains('idle') ? (s.querySelector('.dt, b, h3, h4') || s).textContent.trim().slice(0, 40) : ''; });
  for (let k = 0; k < 3000 && moments < M; k++) {
    await idle();
    const at = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !!(w && !w.hidden && document.getElementById('evLet') && !document.querySelector('#goOn')); });
    if (!at) { if (await page.evaluate(() => hud && hud.mode !== 'play')) break; try { await next(); } catch (e) { logs.push('next ' + e.message.slice(0, 80)); break; } continue; }
    moments++;
    const st = await page.evaluate(() => ({ fold: !!document.getElementById('evOOR'), open: document.getElementById('evOOR') && document.getElementById('evOOR').getAttribute('aria-expanded'),
      drawn: document.querySelectorAll('#evOORg .opt').length, oor: hud.cp.options.filter((o) => o.status === 'out of reach' && o.means.length).length,
      nums: [...document.querySelectorAll('#evOpts .opt')].map((b) => +b.dataset.num) }));
    if (reclose && st.fold && st.open === 'true') {   // the fold left open by the pushed fold card is closed by its row first
      reclose = false; await page.click('#evOOR'); await page.waitForTimeout(250);
      Object.assign(st, await page.evaluate(() => ({ open: document.getElementById('evOOR').getAttribute('aria-expanded'), drawn: document.querySelectorAll('#evOORg .opt').length })));
    }
    if (st.oor && !st.fold) fails.push(`age? ${st.oor} out of reach but no fold`);
    if (!st.oor && st.fold) fails.push('fold with nothing in it');
    if (st.fold && st.open === 'false' && st.drawn) fails.push('folded cards drawn');
    if (st.fold && seen < 3) {
      seen++;
      if (seen === 1) await page.screenshot({ path: `${dir}/fold-closed.png` });
      // a number key on a folded card: opens and focuses it, pushes nothing
      const n = await page.evaluate(() => { const want = hud.cp.options.filter((o) => o.status === 'out of reach' && o.means.length); return [...CPNUM].find(([k, o]) => want.includes(o))[0]; });
      if (n < 10) {
        await page.mouse.move(2, 2); await page.keyboard.press(String(n)); await page.waitForTimeout(300);
        const r = await page.evaluate((n) => ({ open: document.getElementById('evOOR').getAttribute('aria-expanded'), focus: document.activeElement && document.activeElement.dataset ? document.activeElement.dataset.num : null, still: !!document.getElementById('evLet') }), n);
        if (r.open !== 'true' || +r.focus !== n || !r.still) fails.push(`key ${n} on a folded card: ${JSON.stringify(r)}`); else keyed++;
        const s1 = await strip(); if (!s1) fails.push('focused card shows no reading');
        if (seen === 1) await page.screenshot({ path: `${dir}/fold-open-key.png` });
        // the mouse crosses another card and leaves it: the focused card's reading stays
        const other = await page.$('#evOpts .opt:not(.pass)');
        const bb = await other.boundingBox(); await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2, { steps: 3 }); await page.waitForTimeout(250);
        await page.mouse.move(2, 2, { steps: 3 }); await page.waitForTimeout(300);
        const s2 = await strip(); if (!s2) fails.push('reading closed when the mouse left another card'); else focusKept++;
        // close the fold by its row: the cards go, focus goes to the row
        await page.click('#evOOR'); await page.waitForTimeout(250);
        const c = await page.evaluate(() => ({ open: document.getElementById('evOOR').getAttribute('aria-expanded'), drawn: document.querySelectorAll('#evOORg .opt').length }));
        if (c.open !== 'false' || c.drawn) fails.push('fold did not close: ' + JSON.stringify(c));
        const stored = await page.evaluate(() => localStorage.getItem('chroma.oorOpen'));
        if (stored) fails.push('closed fold remembered as open');
        if (!heldFold) {                                // the number opens the fold again; its card is held (or clicked) to push it
          await page.keyboard.press(String(n)); await page.waitForTimeout(600);
          const b = await page.$(`#evOORg .opt[data-num="${n}"]`);
          if (!b) fails.push(`key ${n} did not open the fold again`);
          else {
            const key = await page.evaluate(() => lastCpKey);
            const r = await holdOpt(page, b, { midway: seen === 1 ? () => page.screenshot({ path: `${dir}/fold-hold.png` }) : null });
            await idle();
            const stuck = await page.evaluate((k) => lastCpKey === k && !!document.getElementById('evLet') && !document.getElementById('evwrap').hidden, key);
            heldFold = r.held ? `held ${r.ms} ms` : 'clicked'; reclose = true;
            if (stuck) fails.push(`the fold card ${n} was not pushed (${heldFold})`);
            else continue;                              // its outcome: the next step goes on from there
          }
        }
      }
    }
    await page.click('#evLet', { timeout: 15000 }).catch((e) => logs.push('let ' + e.message.slice(0, 60)));
  }
  console.log(`moments ${moments}; folds tried ${seen}; key opened ${keyed}; focus kept ${focusKept}; fold card pushed: ${heldFold || 'no'}`);
  console.log('fails:', JSON.stringify(fails)); console.log('logs:', JSON.stringify(logs));
  const ok = moments > 0 && seen > 0 && !fails.length && !logs.some((l) => l.startsWith('pageerror'));
  console.log(`oor_check: ${ok ? 'PASS' : 'FAIL'}`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
