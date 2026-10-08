// many perks on the HUD: play to an age, then the Perks section folded and unfolded
const { chromium } = require(process.env.PW || 'playwright');
const { startLife } = require('./start.js');   // the tarot start screen (release row G8)
const [url, dir, until, width] = [process.argv[2], process.argv[3], parseFloat(process.argv[4] || '50'), parseInt(process.argv[5] || '1280')];
(async () => {
  const b = await chromium.launch(); const phone = width < 600;
  const p = await b.newPage({ viewport: { width, height: phone ? 844 : 860 }, colorScheme: 'dark', hasTouch: phone, isMobile: phone });
  const logs = []; p.on('pageerror', e => logs.push('pageerror: ' + e.message));
  await p.goto(url); await p.waitForSelector('.tarot', { timeout: 120000 });
  await startLife(p, '3', 'Lale');
  await p.waitForSelector('#tMain, .opt, #goOn', { timeout: 60000 });
  const idle = async () => { await p.waitForTimeout(120); await p.waitForFunction(() => !document.getElementById('tPause') && !busy && !choosing && !document.getElementById('evwrap').classList.contains('leaving'), null, { timeout: 300000 }).catch(() => {}); await p.waitForTimeout(120); };
  for (let i = 0; i < 400; i++) {
    const s = await p.evaluate(() => ({ cp: !!document.querySelector('.opt'), res: !!document.querySelector('#goOn') }));
    if (s.res) await p.click('#goOn'); else if (s.cp) await p.click('#evLet'); else await p.click('#tMain');
    await idle();
    const age = await p.evaluate(() => parseFloat((document.querySelector('.who .age b') || {}).textContent || '0'));
    const n = await p.evaluate(() => document.querySelectorAll('.perk[data-perk]').length + ((document.getElementById('perkMore') || {}).textContent || ''));
    if (age >= until && String(n).includes('more')) break;
  }
  const s2 = await p.evaluate(() => !!document.querySelector('.opt') || !!document.querySelector('#goOn'));
  if (s2) { await p.click('#evPeek').catch(() => {}); await p.waitForTimeout(300); }
  if (phone) { const t = await p.$('#tHud'); if (t) { await t.click(); await p.waitForTimeout(400); } }
  const pm = await p.$('#perkMore');
  console.log('before', await p.evaluate(() => [document.querySelectorAll('.perk[data-perk]').length, (document.getElementById('perkMore') || {}).textContent, document.querySelector('.who .age b').textContent]));
  if (pm) { await pm.scrollIntoViewIfNeeded(); await p.screenshot({ path: `${dir}/perks-folded${phone ? '-phone' : ''}.png` }); await pm.click(); await p.waitForTimeout(300);
    const pm2 = await p.$('#perkMore'); if (pm2) await pm2.scrollIntoViewIfNeeded(); await p.screenshot({ path: `${dir}/perks-open${phone ? '-phone' : ''}.png` }); }
  console.log('after', await p.evaluate(() => [document.querySelectorAll('.perk[data-perk]').length, (document.getElementById('perkMore') || {}).textContent]), 'sw', await p.evaluate(() => document.documentElement.scrollWidth), logs.join('\n'));
  await b.close();
})();
