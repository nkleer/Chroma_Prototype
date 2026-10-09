// Chroma's own icons: solid ink glyphs on a 48-unit grid, single colour (currentColor), cut like a woodcut.
// A glyph is drawn in layers; each layer has filled shapes and "cuts" (lines or shapes carved out of that layer only),
// done with a mask, so a cut shows whatever is behind the icon.
const r = (n) => Math.round(n * 100) / 100;
const rad = (a) => a * Math.PI / 180;

const P = {
  rect: (x, y, w, h, rx = 0) => rx ? `M${r(x + rx)} ${r(y)}H${r(x + w - rx)}A${rx} ${rx} 0 0 1 ${r(x + w)} ${r(y + rx)}V${r(y + h - rx)}A${rx} ${rx} 0 0 1 ${r(x + w - rx)} ${r(y + h)}H${r(x + rx)}A${rx} ${rx} 0 0 1 ${r(x)} ${r(y + h - rx)}V${r(y + rx)}A${rx} ${rx} 0 0 1 ${r(x + rx)} ${r(y)}Z`
    : `M${r(x)} ${r(y)}h${r(w)}v${r(h)}h${r(-w)}Z`,
  circ: (x, y, rr) => `M${r(x - rr)} ${r(y)}a${rr} ${rr} 0 1 0 ${r(2 * rr)} 0a${rr} ${rr} 0 1 0 ${r(-2 * rr)} 0Z`,
  poly: (pts) => 'M' + pts.map(([x, y]) => `${r(x)} ${r(y)}`).join('L') + 'Z',
  // a stroke as a filled capsule from A to B, width w
  cap(x1, y1, x2, y2, w) {
    const dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy) || 1e-6, nx = -dy / d * w / 2, ny = dx / d * w / 2, h = w / 2;
    return `M${r(x1 + nx)} ${r(y1 + ny)}L${r(x2 + nx)} ${r(y2 + ny)}A${h} ${h} 0 0 0 ${r(x2 - nx)} ${r(y2 - ny)}L${r(x1 - nx)} ${r(y1 - ny)}A${h} ${h} 0 0 0 ${r(x1 + nx)} ${r(y1 + ny)}Z`;
  },
  // a thick arc (degrees, 0 = right, clockwise) with round ends
  arc(cx, cy, rr, a0, a1, w) {
    const h = w / 2, ro = rr + h, ri = rr - h, pt = (a, q) => [cx + Math.cos(rad(a)) * q, cy + Math.sin(rad(a)) * q];
    const large = Math.abs(a1 - a0) > 180 ? 1 : 0, [o0, o1, i1, i0] = [pt(a0, ro), pt(a1, ro), pt(a1, ri), pt(a0, ri)];
    return `M${r(o0[0])} ${r(o0[1])}A${r(ro)} ${r(ro)} 0 ${large} 1 ${r(o1[0])} ${r(o1[1])}A${h} ${h} 0 0 1 ${r(i1[0])} ${r(i1[1])}A${r(ri)} ${r(ri)} 0 ${large} 0 ${r(i0[0])} ${r(i0[1])}A${h} ${h} 0 0 1 ${r(o0[0])} ${r(o0[1])}Z`;
  },
  // a leaf or lens from A to B, half-width w at the middle
  lens(x1, y1, x2, y2, w) {
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, d = Math.hypot(x2 - x1, y2 - y1), nx = -(y2 - y1) / d * w * 2, ny = (x2 - x1) / d * w * 2;
    return `M${r(x1)} ${r(y1)}Q${r(mx + nx)} ${r(my + ny)} ${r(x2)} ${r(y2)}Q${r(mx - nx)} ${r(my - ny)} ${r(x1)} ${r(y1)}Z`;
  },
  star(cx, cy, ro, ri, n = 5, rot = -90) {
    const pts = []; for (let i = 0; i < 2 * n; i++) { const a = rad(rot + i * 180 / n), q = i % 2 ? ri : ro; pts.push([cx + Math.cos(a) * q, cy + Math.sin(a) * q]); }
    return P.poly(pts);
  },
};

function glyph(name, draw) {
  const layers = [{ fills: [], cuts: [] }];
  const g = {
    fill(d, rule) { layers[layers.length - 1].fills.push(`<path d="${d}" fill="currentColor"${rule ? ` fill-rule="${rule}"` : ''}/>`); return g; },
    hole(...ds) { return g.fill(ds.join(''), 'evenodd'); },          // a shape with holes (outer path first)
    cut(d, w = 2.2) { layers[layers.length - 1].cuts.push(`<path d="${d}" fill="none" stroke="#000" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`); return g; },
    cutFill(d) { layers[layers.length - 1].cuts.push(`<path d="${d}" fill="#000"/>`); return g; },
    layer() { layers.push({ fills: [], cuts: [] }); return g; },
  };
  draw(g, P);
  const id = `ci-${name.replace(/[^a-z0-9]+/gi, '-').toLowerCase()}`;
  let defs = '', body = '';
  layers.forEach((l, i) => {
    if (!l.fills.length) return;
    if (l.cuts.length) {
      const m = `${id}-m${i}`;
      defs += `<mask id="${m}" maskUnits="userSpaceOnUse" x="0" y="0" width="48" height="48"><rect width="48" height="48" fill="#fff"/>${l.cuts.join('')}</mask>`;
      body += `<g mask="url(#${m})">${l.fills.join('')}</g>`;
    } else body += l.fills.join('');
  });
  // masks live beside the symbols in the sprite's defs, not inside them
  return { id, name, defs, svg: `<symbol id="${id}" viewBox="0 0 48 48">${body}</symbol>` };
}

module.exports = { glyph, P };
