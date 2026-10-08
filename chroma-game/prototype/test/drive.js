// A scripted life on the page: a preset and a name, then lines sent as the keyboard would send them ("" lives on to
// the next moment or lets them choose, a number pushes, w m y d step). Prints the story so far and saves a shot.
// Usage: PW=<playwright> node test/drive.js URL OUT.png '["2","Lale","","3",""]' [width]
const { chromium } = require(process.env.PW || 'playwright');
const { startLife, idleOf } = require('./start.js');
const url = process.argv[2]; const shot = process.argv[3] || 'shot.png';
const script = JSON.parse(process.argv[4] || '["2","Lale","",""]');
const width = parseInt(process.argv[5] || '1280');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  const logs = [];
  page.on('console', m => { if (m.type() === 'error') logs.push('console error: ' + m.text()); });
  page.on('pageerror', e => logs.push('pageerror: ' + e.message));
  const idle = idleOf(page, logs);
  const t0 = Date.now();
  await page.goto(url);
  await startLife(page, script[0], script[1]);
  console.log('started ms', Date.now() - t0);
  await idle();
  for (const step of script.slice(2)) {
    const t1 = Date.now();
    await page.evaluate((s) => send(s), step);
    await idle();
    console.log('step', JSON.stringify(step), 'ms', Date.now() - t1);
  }
  const text = await page.$eval('#feed', el => el.innerText);
  console.log(text.slice(-4000));
  await page.screenshot({ path: shot });
  console.log(logs.slice(0, 30).join('\n') || 'no page errors');
  await browser.close();
})();
