// Prototype for idea 4 (their own tarot card): one character at four ages, the same arch behind them.
const KIT = '/mnt/project-files/chroma-art/kit/';
const K = require(KIT + 'props'); const Q = require(KIT + 'props2'); const LV = require(KIT + 'props_love');
const { DAWN, WARM } = K;
const S = {};
const base = (P) => {
  const FL = 394;
  Q.room(P, { wall: .56, floor: .66, floorY: FL, night: .3 });
  const ax = 352, aw = 176, ay = 70, ah = 300;
  LV.archWindow(P, ax, ay, aw, ah, { t: .82, frame: 14, bars: 0, transom: 0, outside: () => {
    for (let i = 0; i < 9; i++) P.tone(P.rect(ax, ay + i * 34, aw, ah), .34 - i * .036, { a: 'h', line: 0 });
    P.wash(P.rect(ax, ay + 120, aw, ah - 120), DAWN, .4);
    // far hills and a low sun
    P.tone(`M${ax} ${ay + 236}Q${ax + 60} ${ay + 214} ${ax + 110} ${ay + 230}T${ax + aw} ${ay + 222}V${ay + ah}H${ax}Z`, .62, { a: 'a' });
    P.lit(P.circ(ax + 118, ay + 214, 13), '#efb27a', .6, .8);
  } });
  P.light(440, 300, 220, DAWN, .1, .45);
  P.beam(`M372 ${FL}L508 ${FL}L560 470L320 470Z`, DAWN, .4, .18);
  P.stroke('M0 424H880M0 456H880', .6, 'opacity=".5"');
};
const rim = [-1.4, -1.6];
S['child'] = (P) => { base(P); P.figure({ x: 440, y: 394, h: 138, f: 1, child: true, hair: 'short', wear: 'none', arms: [[14, 10], [-10, 8]] }, rim); };
S['youth'] = (P) => { base(P); P.figure({ x: 440, y: 394, h: 214, f: 1, hair: 'short', wear: 'none', build: .94, arms: [[10, 8], [-6, 8]], legs: [[6, 0], [-6, 0]] }, rim); };
S['adult'] = (P) => { base(P); P.figure({ x: 440, y: 394, h: 232, f: 1, hair: 'short', wear: 'coat', arms: [[8, 6], [-8, 6]] }, rim); };
S['elder'] = (P) => { base(P);
  P.figure({ x: 436, y: 394, h: 212, f: 1, hair: 'short', wear: 'coat', lean: 9, bow: 10, build: 1.04, arms: [[20, 12], [-4, 6]], legs: [[8, 4], [-6, 0]] }, rim);
  P.ink('M478 394L476 286h4L482 394Z'); P.stroke('M478 287q1 -9 11 -7', 3.2); };
module.exports = { SCENES: S };
