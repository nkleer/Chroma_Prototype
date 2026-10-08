const { chromium } = require(process.env.PW || 'playwright');
// v22.1 glitch fix: the reading of a card that has keyboard focus stays open when the mouse crosses another card and
// leaves it (v22 closed it). At each moment of one life at 1280x800 (preset 1): Tab to the first card (its reading
// opens), the mouse crosses the last card and leaves to the corner, then the reading must show the focused card again;
// with nothing focused and the mouse gone, it goes idle. No page error.
//   node test/focus_check.js <url> <shots dir> [moments]
const { startLife, idleOf, nextOf } = require('./start.js');
const [url, dir, M] = [process.argv[2], process.argv[3], +(process.argv[4] || 10)];
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  const logs = []; page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url);
  await startLife(page, '1', 'Mira');
  const idle = idleOf(page, logs), next = nextOf(page, idle);
  const reading = () => page.evaluate(() => { const s = document.getElementById('evStrip'); return s && !s.classList.contains('idle') ? s.textContent.replace(/\s+/g, ' ').trim().slice(0, 60) : ''; });
  const fails = []; let moments = 0, kept = 0, idled = 0;
  for (let k = 0; k < 3000 && moments < M; k++) {
    await idle();
    const at = await page.evaluate(() => { const w = document.getElementById('evwrap'); return !!(w && !w.hidden && document.getElementById('evLet') && !document.querySelector('#goOn')); });
    if (!at) { if (await page.evaluate(() => hud && hud.mode !== 'play')) break; try { await next(); } catch (e) { logs.push('next ' + e.message.slice(0, 80)); break; } continue; }
    const cards = await page.$$('#evOpts .opt:not(.onone)');
    if (cards.length >= 2) {
      moments++;
      await page.mouse.move(2, 2); await page.waitForTimeout(200);
      await cards[0].focus(); await page.waitForTimeout(200);
      const r0 = await reading(); if (!r0) fails.push(`moment ${moments}: the focused card shows no reading`);
      const bb = await cards[cards.length - 1].boundingBox();
      await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2, { steps: 3 }); await page.waitForTimeout(250);
      const r1 = await reading();
      await page.mouse.move(2, 2, { steps: 3 }); await page.waitForTimeout(300);
      const r2 = await reading();
      if (r2 && r2 === r0) kept++; else fails.push(`moment ${moments}: after the mouse left the other card the reading was "${r2}" (focused card "${r0}", hovered "${r1}")`);
      if (moments === 1) await page.screenshot({ path: `${dir}/focus-kept.png` });
      await page.evaluate(() => document.activeElement && document.activeElement.blur()); await page.waitForTimeout(200);
      if (!(await reading())) idled++; else fails.push(`moment ${moments}: the reading stayed with nothing focused or hovered`);
    }
    await page.click('#evLet', { timeout: 15000 }).catch((e) => logs.push('let ' + e.message.slice(0, 60)));
  }
  console.log(`moments ${moments}; reading kept for the focused card ${kept}; idle with nothing focused ${idled}`);
  console.log('fails:', JSON.stringify(fails.slice(0, 6))); console.log('logs:', JSON.stringify(logs));
  const ok = moments > 0 && !fails.length && !logs.some((l) => l.startsWith('pageerror'));
  console.log(`focus_check: ${ok ? 'PASS' : 'FAIL'}`);
  await browser.close(); process.exit(ok ? 0 : 1);
})();
