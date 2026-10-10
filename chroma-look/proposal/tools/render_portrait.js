const fs = require('fs'); const { execSync } = require('child_process'); const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { painter } = require('/mnt/project-files/chroma-art/kit/engrave'); const { SCENES } = require('./scenes_portrait');
const OUT = process.argv[2]; const CROP = { x: 293, y: 40, w: 294, h: 420 };
(async () => {
  const b = await chromium.launch(); const DPR = 2;
  const p = await b.newPage({ viewport: { width: 880, height: 500 }, deviceScaleFactor: DPR });
  for (const n of Object.keys(SCENES)) {
    const P = painter(); SCENES[n](P); const f = `${OUT}/${n}`;
    await p.setContent(`<html><body style="margin:0">${P.finish(n, { only: 'eng' })}</body></html>`);
    const eng = await p.locator('svg').first().screenshot();
    await p.setContent(`<html><body style="margin:0">${P.finish(n, { engHref: 'data:image/png;base64,' + eng.toString('base64') })}</body></html>`);
    await p.locator('svg').first().screenshot({ path: f + '-2x.png' });
    execSync(`convert ${f}-2x.png -crop ${CROP.w * DPR}x${CROP.h * DPR}+${CROP.x * DPR}+${CROP.y * DPR} +repage -filter Lanczos -resize 350x500! ${f}.png && rm ${f}-2x.png`);
    execSync(`convert ${f}.png -define webp:target-size=38000 -define webp:pass=6 ${f}.webp`);
    console.log(n, (fs.statSync(f + '.webp').size / 1024).toFixed(1) + ' KB');
  }
  await b.close();
})();
