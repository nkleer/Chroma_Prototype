// The drivers' push for v23's Living HUD (plan step 7a, decision 1). With the Living HUD's cards piece mounted, #table
// carries data-hold="on" and a pointer pushes a card only when held: each .opt carries data-hold="<ms>" (0 for their own
// pick, about 450 for a way they would go with, up to about 1600 for one far against who they are). Without it (Living
// off, the classic look, a page before v23) a click pushes as before.
//   const { holdOpt, pushOpt, keyOpt, holdOn } = require('./hold.js');
//   await holdOpt(page, '.opt[data-i="2"]');            // desktop: the mouse holds the card (or clicks it, with no hold)
//   await holdOpt(page, handle, { touch: true });      // phone (a context with hasTouch): a finger held on the card
//   await pushOpt(page, handle, { touch: true });      // holdOpt, then "Push them to this" when a tap only read the card
//   await keyOpt(page, handle);                        // its printed number on the keyboard, past the two-digit wait
// holdOpt returns { held, ms }: held is false when it clicked (or tapped) instead, ms the card's data-hold.
// Options: touch; timeout and force (as for a click); midway, an async function called halfway through a hold (a shot).
const holdOn = (page) => page.evaluate(() => { const t = document.getElementById('table'); return !!t && t.dataset.hold === 'on'; });
module.exports.holdOn = holdOn;

const handleOf = async (page, x, timeout) => (typeof x === 'string' ? page.waitForSelector(x, { state: 'attached', timeout: timeout || 30000 }) : x);

module.exports.holdOpt = async (page, x, opts = {}) => {
  const h = await handleOf(page, x, opts.timeout);
  if (!(await holdOn(page))) {                        // no hold on this page: a click pushes (desktop) or reads (phone), as before
    if (opts.touch) await h.tap({ timeout: opts.timeout, force: opts.force }); else await h.click({ timeout: opts.timeout, force: opts.force });
    return { held: false, ms: 0 };
  }
  const v = await h.getAttribute('data-hold');
  const ms = v != null && v !== '' && isFinite(+v) ? Math.max(0, +v) : 1600;   // a card the piece left bare: the longest hold
  const wait = async () => {
    if (opts.midway && ms > 0) { await page.waitForTimeout(Math.round(ms / 2)); await opts.midway(); await page.waitForTimeout(ms - Math.round(ms / 2) + 250); }
    else await page.waitForTimeout(ms + 250);
  };
  if (opts.touch) {                                   // a finger: CDP touch events, so the page sees pointerType "touch"
    // a tap's own checks first (they scroll the card clear of the bar pinned over the lower cards on a phone), then the
    // finger goes down at the card's centre, which must be the card's
    await h.tap({ trial: true, timeout: opts.timeout, force: opts.force });
    const b = await h.boundingBox(); if (!b) throw new Error('holdOpt: the card has no box (hidden or detached)');
    const pt = { x: b.x + b.width / 2, y: b.y + b.height / 2 };
    if (!opts.force && !(await h.evaluate((el, p) => { const e = document.elementFromPoint(p.x, p.y); return !!e && el.contains(e); }, pt))) throw new Error('holdOpt: something covers the card at its centre');
    const cdp = await page.context().newCDPSession(page);
    try {
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [pt] });
      try { await wait(); } finally { await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); }
    } finally { await cdp.detach().catch(() => {}); }
  } else {                                            // the mouse: to the card's centre (waiting as a click would), down, held, up
    await h.hover({ timeout: opts.timeout, force: opts.force });
    await page.mouse.down();
    try { await wait(); } finally { await page.mouse.up(); }
  }
  return { held: true, ms };
};

// A push that works on every page and in both ways of pointing: holdOpt, then, when that only read the card (a tap on a
// phone, with no hold or with the hold not taken), "Push them to this". Returns holdOpt's result with pushIt: true when
// the button was used.
module.exports.pushOpt = async (page, x, opts = {}) => {
  const r = await module.exports.holdOpt(page, x, opts);
  await page.waitForTimeout(200);
  const p = await page.$('#pushIt');
  if (p && await p.isVisible() && await page.evaluate(() => !choosing && !busy)) { await p.click({ timeout: opts.timeout }); return { ...r, pushIt: true }; }
  return { ...r, pushIt: false };
};

// The card's printed number on the keyboard (13-state.js): a lone "1" waits 450 ms for a second digit when a moment has
// ten or more options, so this waits 600 ms after the last digit before anything else reads the page. A folded card's
// number only opens its fold, so a card handed here must be on show. Returns the number pressed.
module.exports.keyOpt = async (page, x, opts = {}) => {
  const h = await handleOf(page, x, opts.timeout);
  const num = await h.getAttribute('data-num');
  if (!num || !/^[0-9]+$/.test(num)) throw new Error('keyOpt: the card has no number (data-num ' + num + ')');
  for (const d of num) await page.keyboard.press(d);
  await page.waitForTimeout(600);
  return +num;
};
