// Renders the portrait cards ("their own tarot card"): one setting per lead colour x four ages.
// node render_portraits.js [name ...]      names like portrait-w-child; none = all 20
// env: KIT (the drawing kit, default /mnt/project-files/chroma-art/kit, read only), OUT (default: this folder), DPR (default 3), FULL=1 also writes the whole 880x500 stage to OUT/full/ for checking,
//      SHEET=0 skips the contact sheet.
// Card art is the portrait window x 293..587, y 40..460 of the 880x500 stage (render_card.js), saved at 420x600:
// <name>.webp (kept under 45 KB with the webp target-size trick) and a PNG preview in OUT/png/ for the contact sheet.
const fs = require('fs'), path = require('path'); const { execSync } = require('child_process');
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/node22/lib/node_modules/playwright'); } })();
const { painter } = require(path.join(process.env.KIT || '/mnt/project-files/chroma-art/kit', 'engrave'));
const { SCENES, ORDER } = require(path.join(__dirname, 'scenes_portrait'));
const OUT = process.env.OUT || __dirname; const PNG = path.join(OUT, 'png'), FULL = path.join(OUT, 'full');
fs.mkdirSync(PNG, { recursive: true }); if (process.env.FULL) fs.mkdirSync(FULL, { recursive: true });
const names = process.argv.slice(2).length ? process.argv.slice(2) : ORDER;
const CROP = { x: 293, y: 40, w: 294, h: 420 }, DPR = +(process.env.DPR || 3), LIMIT = 45000;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 880, height: 500 }, deviceScaleFactor: DPR });
  for (const n of names) {
    if (!SCENES[n]) { console.log('no scene', n); continue; }
    const P = painter(); SCENES[n](P);
    const tmp = path.join(OUT, n + '-big.png'), webp = path.join(OUT, n + '.webp'), png = path.join(PNG, n + '.png');
    // two passes, as render_card.js: the engraving once as an image, then the outlines, washes and figures over it
    await p.setContent(`<html><body style="margin:0">${P.finish(n, { only: 'eng' })}</body></html>`);
    const eng = await p.locator('svg').first().screenshot();
    await p.setContent(`<html><body style="margin:0">${P.finish(n, { engHref: 'data:image/png;base64,' + eng.toString('base64') })}</body></html>`);
    const shot = path.join(OUT, n + '-3x.png');
    await p.locator('svg').first().screenshot({ path: shot });
    if (process.env.FULL) execSync(`convert ${shot} -filter Lanczos -resize 880x500 ${path.join(FULL, n + '.png')}`);
    execSync(`convert ${shot} -crop ${CROP.w * DPR}x${CROP.h * DPR}+${CROP.x * DPR}+${CROP.y * DPR} +repage -filter Lanczos -resize 420x600! ${tmp} && rm ${shot}`);
    // the target-size search can overshoot on light pictures: step the target down until the file is under the limit
    let size = 0;
    for (const t of [42000, 38000, 34000, 30000, 26000, 22000]) {
      execSync(`convert ${tmp} -define webp:target-size=${t} -define webp:pass=6 ${webp}`);
      size = fs.statSync(webp).size; if (size < LIMIT) break;
    }
    fs.renameSync(tmp, png);
    console.log(n, (size / 1024).toFixed(1) + ' KB');
  }
  await b.close();
  // contact sheet: rows W U B R G, columns child youth adult elder, at the size the game shows a card (175x250)
  if (process.env.SHEET !== '0') {
    const all = ORDER.map((n) => path.join(PNG, n + '.png'));
    if (all.every((f) => fs.existsSync(f))) {
      execSync(`montage ${all.join(' ')} -tile 4x5 -geometry 175x250+6+6 -background '#2a2116' ${path.join(OUT, 'contact.png')}`);
      console.log('contact sheet', path.join(OUT, 'contact.png'));
    }
  }
})();
