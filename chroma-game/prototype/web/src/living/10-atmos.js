"use strict";
/* ---------------- the Living HUD: the sky and the ink (v23 row V1; plan: the Living HUD in v23, step 3) ----------------
   Ported from the showcase's atmos.js (frozen 10-18 10:11 UTC), its runtime part only: the gallery's demos, the weather
   sigils (the plan keeps the panels and their words as they are), the GPU bench and the shaders' sources are left out.
   The sky (W1 "The sky is their mind"). The page's still night (.sky, .glow and the turning sigil, hidden while this sky
   stands) becomes a moving one, in a fixed layer behind #app, under every panel. The game's arcane night (the night tokens,
   faint violet, blue and plum nebula glows, a fine star field) carries five layers, one per colour, each as strong as
   that colour's share of the person (CH.grammar: the leading colours carry the sky, the rest show as traces):
     White  a warm dawn rim along the lower horizon, and a few stars settling into a calm gilt lattice (a rose window)
     Blue   crisp constellations joined by hairlines, and a cool refracted shimmer drifting through the gas
     Black  silver-plum smoke turning slowly inward, a few motes falling toward its eye, a deeper velvet vignette
     Red    a hearth: a band of ember light along the floor of the sky, sparks rising from it, one great brushstroke of
            ember light shedding embers, and warm meteors (rate: Red's share)
     Green  slow aurora curtains that breathe, and a few lights rising like fireflies
   With the game's light and shadow switch on (hud.life.shadow), a colour whose shadow shows takes its shadow form,
   subtly: White's lattice freezes, Blue's lines double, Black's vignette eats the edges, Red's brush flings droplets and
   its meteors burst, Green's aurora and lights slow to stillness. Over the five, the inner weather: strain is wind
   (streaks, a veil, smeared stars, pale silver meteors), peace is still clear air (the haze thins, the stars stop
   shimmering), satisfaction warms or cools the light, and the times outside (hud.life.world_era, with the outer world on)
   tint the far horizon. The life sends these about every two years of play, so the sky eases toward each new state over
   about half the time between them while time runs, and in about 0.6 s otherwise.
   The sky knows where the panels are (CLEAR: hidden panels do not count): its figures gather in the widest open stretch,
   or, when the panels leave only thin margins (the page at most sizes), keep the whole sky's proportions behind them.
   Hovering or tapping the open sky (the margins and gaps, wherever the pointer reaches #app or the page itself) gives its
   reading in the page's own #tip.
   The ink (B1 "Wet ink to dry ink"): how wet it is follows the age (soaking at 4, about half at 25, nearly dry by 45),
   raised by the readiness to change and an open window of change (CH.ink.wetOf, which living/90-game.js uses for S.wet);
   the eased wetness goes to --wet on <html> and to the SVG filter #chs-ink. A press or a slow drag on the open sky drops
   ink of the person's two leading colours: a wide watercolour bloom on a wet page, a small crisp pen mark on a dry one.
   A window of change opening, or an outcome that moves the colours a point or more, sends one slow ripple across the
   sky that wets its ink again. CH.ink.bloom(x, y, colours, {on: el}) lays the same ink on a parchment panel.
   Renderer: WebGL with failIfMajorPerformanceCaveat (a machine without fast graphics refuses it, with a console.warn),
   else a Canvas2D painting of the same sky from textures baked once. localStorage "chroma.living.gl" = "force" takes
   WebGL even on a software renderer (so the shader path can be tested), "off" takes the painting. The field is drawn at
   a third of the CSS size (a quarter in the painting), only as many pictures a second as its motion needs; the sparks at
   1.5 device pixels a CSS pixel at most, the ink at 2. Motion is the ink look's: full, calm (slower, fewer sparks, fewer
   pictures) or off (one still frame for each state, always the same for the same state). */
(() => {
  const CH = window.CH;
  if (!CH) return;
  const clamp = CH.clamp, smooth = CH.smooth, TAU = Math.PI * 2, SVGNS = "http://www.w3.org/2000/svg";
  const frac = (v) => v - Math.floor(v);
  const mod = (a, n) => a - n * Math.floor(a / n);
  // the wind's slant: it blows to the right, rising a little (radians above level); the veil's streaks lean a little more
  const WIND = 0.14, VEIL = 0.21;

  /* ---------- the five-colour grammar: one strength per colour, shared with every module that moves particles ---------- */
  // A colour's effects are as strong as its share of the person, eased so that the leading colours carry the sky: 4% shows
  // nothing, a tenth shows faintly, an even fifth at about a third, and 42% or more is whole. A Red-led life (37% Red, the
  // rest about 16% each) is mostly Red's sky, the others still show as traces.
  const strengthOf = (v) => Math.pow(clamp(((v || 0) - 0.04) / 0.38), 1.25);
  // align (White): motes settle into symmetry and a lattice; laminar (Blue): slow, smooth, exact flow; inward (Black): a
  // gravity toward the centre; spark (Red): fast to flare, fast to fade, turbulence; grow (Green): slow breath, branching.
  CH.grammar = (w) => {
    const a = Array.isArray(w) ? w : w && Array.isArray(w.w) ? w.w : [0.2, 0.2, 0.2, 0.2, 0.2];
    const s = a.map(strengthOf);
    return { align: s[0], laminar: s[1], inward: s[2], spark: s[3], grow: s[4] };
  };
  // Light and shadow (only when the game's shadows switch is on): how much of each colour shows its shadow form now, 0..1.
  // The game sends S.shadow.cols[i] = {show, part, ...} (05-hud.js reads the same); plain arrays are read too.
  function shadowOf(S) {
    const sh = S && S.shadow, out = [0, 0, 0, 0, 0];
    if (!sh) return out;
    const cols = Array.isArray(sh) ? sh : sh.cols;
    if (!Array.isArray(cols)) return out;
    cols.forEach((x, i) => {
      if (i > 4 || x == null) return;
      if (typeof x === "number") out[i] = clamp(x);
      else if (Array.isArray(x)) out[i] = clamp(x[0] || 0);
      else if (x.show) out[i] = clamp(0.45 + 0.55 * clamp(x.part ?? 0.5));
    });
    return out;
  }
  /* B1: how wet the ink is at a state, 0 dry .. 1 soaking. The age carries it (a child's page bleeds and blooms, an elder's
     lines are crisp and set: soaking at 4, about half at 25, nearly dry by 45), the readiness to change (plasticity x
     self-control) keeps a page wet, and an open window of change wets it again; past 55 the page dries a little further,
     window or not. A host may send its own as S.inkWet. living/90-game.js takes this for S.wet, so every piece agrees. */
  function wetOf(S) {
    if (!S) return 0.5;
    if (typeof S.inkWet === "number") return clamp(S.inkWet);
    const age = typeof S.age === "number" ? S.age : 30, rd = S.dyn && typeof S.dyn.readiness === "number" ? S.dyn.readiness : 0.3;
    const youth = 1 - smooth(clamp((age - 4) / 40));
    const win = S.dyn && S.dyn.window ? 0.3 * clamp(S.dyn.openness ?? 1) : 0;
    const elder = 1 - 0.3 * smooth(clamp((age - 55) / 15));
    return clamp((0.75 * youth + 0.45 * clamp(rd) + win) * elder);
  }
  const rgbStr = (a) => a.map((v) => Math.round(clamp(v, 0, 255))).join(",");
  const rgb01 = (hex) => CH.rgb(hex).map((v) => v / 255);
  // the person's two leading colours (their inks), strongest first
  const topTwo = (w) => CH.COLORS.map((c, i) => [c, (w && w[i]) || 0]).sort((a, b) => b[1] - a[1]).slice(0, 2).map((x) => x[0]);

  /* ---------- the eased numbers: every target the sky follows, one slot each ---------- */
  // L layer strengths, SH shadows, the weather, the wetness, the times outside (three colours), the meteor rates (Red's
  // warm ones, the strain's silver ones) and the focus (the middle and half size of the widest open stretch, sky units)
  const K = { L: 0, SH: 5, STRAIN: 10, PEACE: 11, CONTENT: 12, WET: 13, ERA: 14, E0: 15, E1: 18, E2: 21, RATE: 24, SRATE: 25, FOC: 26, N: 30 };
  // A critically damped spring per number (no overshoot, a soft start and a soft landing): about 600 ms from one state to
  // the next, so scrubbing the age reads as weather changing, not a cut. Returns whether anything still moves.
  function settle(X, V, T, dt, st) {
    const om = 2 / st, x = om * dt, e = 1 / (1 + x + 0.48 * x * x + 0.235 * x * x * x);
    let moving = false;
    for (let i = 0; i < X.length; i++) {
      const ch = X[i] - T[i], tmp = (V[i] + om * ch) * dt;
      V[i] = (V[i] - om * tmp) * e; X[i] = T[i] + (ch + tmp) * e;
      if (Math.abs(X[i] - T[i]) > 1e-4) moving = true;
    }
    return moving;
  }

  /* ---------- the shaders ---------- */
  const VERT = "attribute vec2 aP; varying vec2 vUv; void main() { vUv = aP * 0.5 + 0.5; gl_Position = vec4(aP, 0.0, 1.0); }";
  // value noise with a quintic fade, and its sums (fbm); hash without sine, so it holds up far from the origin
  const NOISE = `
float hash(vec2 p) { vec3 p3 = fract(vec3(p.xyx) * 0.1031); p3 += dot(p3, p3.yzx + 33.33); return fract((p3.x + p3.y) * p3.z); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}
const mat2 M = mat2(1.6, 1.2, -1.2, 1.6);
float fbm3(vec2 p) { float s = 0.0, a = 0.5; for (int i = 0; i < 3; i++) { s += a * noise(p); p = M * p + 1.7; a *= 0.5; } return s / 0.875; }
float fbm4(vec2 p) { float s = 0.0, a = 0.5; for (int i = 0; i < 4; i++) { s += a * noise(p); p = M * p + 1.7; a *= 0.5; } return s / 0.9375; }
float fbm5(vec2 p) { float s = 0.0, a = 0.5; for (int i = 0; i < 5; i++) { s += a * noise(p); p = M * p + 1.7; a *= 0.5; } return s / 0.96875; }
mat2 rot(float a) { float c = cos(a), s = sin(a); return mat2(c, s, -s, c); }
float blob(vec2 d, vec2 s) { d /= s; return exp(-dot(d, d)); }
`;
  // The gas, baked into a texture now and then (it only drifts, so it need not be drawn every frame): the folded clouds,
  // their bright filaments and the raw fold (for the band of unresolved stars), over a box a little larger than the sky,
  // so the field can carry it on the wind for a while by sampling it further along. The wind (strain) draws it out into
  // long streaks along its slant (uStretch < 1).
  const NEB_FRAG = `${NOISE}
uniform vec4 uBox;
uniform vec2 uCen;
uniform float uT, uDrift, uStretch;
varying vec2 vUv;
void main() {
  vec2 uv = mix(uBox.xy, uBox.zw, vUv);
  vec2 p = rot(-${WIND.toFixed(3)}) * (uv - uCen); p.x *= uStretch; p = uCen + rot(${WIND.toFixed(3)}) * p;
  vec2 q = p * 1.15 - vec2(uDrift * 0.55, 0.0);
  vec2 w = vec2(fbm3(q + vec2(0.0, uT * 0.004)), fbm3(q + vec2(5.2, 1.3) + vec2(uT * 0.003, 0.0)));
  float n = fbm5(q * 1.3 + 1.8 * w + vec2(3.1, 7.7));
  float fil = pow(1.0 - abs(2.0 * fbm3(q * 2.2 + 2.6 * w) - 1.0), 7.0);
  gl_FragColor = vec4(smoothstep(0.30, 0.88, n), fil, n, 1.0);
}`;
  // The field: the night and its gas (from the baked texture), the five colour layers, the weather and the ripple, at a
  // third of the CSS size. Each colour layer is skipped while it is too faint to see.
  const FIELD_FRAG = `${NOISE}
uniform vec2 uRes;
uniform vec4 uNebBox;
uniform sampler2D uNebA, uNebB;
uniform vec2 uOffA, uOffB;
uniform float uNebMix;
uniform float uT, uDrift, uSwirl, uInflow, uAur, uCaus;
uniform float uL[5];
uniform float uSh[5];
uniform vec4 uWx;
uniform vec4 uFoc;
uniform vec3 uE0, uE1, uE2;
uniform vec2 uEra;
uniform vec4 uRip;
varying vec2 vUv;

vec3 gas(sampler2D t, vec2 p) { return texture2D(t, (p - uNebBox.xy) / (uNebBox.zw - uNebBox.xy)).rgb; }
// turbulence: the folded sum of noise, creased where it crosses its middle (Red's low heat haze)
float turb(vec2 p) { float s = 0.0, a = 0.5; for (int i = 0; i < 4; i++) { s += a * abs(2.0 * noise(p) - 1.0); p = M * p + 1.7; a *= 0.5; } return s / 0.9375; }
// a caustic network: light folded through moving glass gathers into bright threads (after joltz0r's tileable water caustic)
float caustic(vec2 p, float t) {
  vec2 i = p; float c = 1.0;
  for (int n = 0; n < 4; n++) {
    float tt = t * (1.0 - 3.5 / float(n + 1));
    i = p + vec2(cos(tt - i.x) + sin(tt + i.y), sin(tt - i.y) + cos(tt + i.x));
    c += 1.0 / length(vec2(p.x / (sin(i.x + tt) / 0.005), p.y / (cos(i.y + tt) / 0.005)));
  }
  c /= 4.0; c = 1.17 - pow(c, 1.4);
  return pow(abs(c), 8.0);
}
// Black's smoke in a slow inward spiral: the field turns (uSwirl) and zooms in (ph), so its shapes fall toward the eye;
// two copies half a cycle apart cross-fade, so the fall never ends and never jumps
float smoke(vec2 d, float r, float ph, float off) {
  vec2 p = rot(uSwirl + 1.25 * log(r + 0.06)) * d * exp2(ph) * 1.9;
  return fbm4(p + off);
}

void main() {
  float asp = uRes.x / uRes.y;
  vec2 uv = vec2(vUv.x * asp, vUv.y);
  float strain = uWx.x, peace = uWx.y, content = uWx.z;
  float LW = uL[0], LU = uL[1], LB = uL[2], LR = uL[3], LG = uL[4];
  // the focus: the widest open stretch of sky (all of it when nothing covers it), where the signature shapes gather
  vec2 F = uFoc.xy; float fh = 2.0 * uFoc.w, fb = F.y - uFoc.w;

  // B1, the re-wetting ripple: a slow ring out from its centre; in its band the sky is seen through a film of water
  float ring = 0.0, crest = 0.0, damp = 0.0;
  if (uRip.w > 0.001) {
    vec2 rd = uv - uRip.xy; float dd = length(rd), x = (dd - uRip.z) / 0.055, xc = (dd - uRip.z - 0.014) / 0.009;
    ring = exp(-x * x) * uRip.w;
    crest = exp(-xc * xc) * uRip.w;
    damp = smoothstep(uRip.z + 0.03, uRip.z - 0.35, dd) * uRip.w;
    uv -= rd / (dd + 1e-3) * ring * 0.035;
  }

  // the game's arcane night (01-base.css .sky): darker along the bottom third, a little bluer toward the top
  vec3 col = mix(vec3(0.027, 0.024, 0.051), vec3(0.050, 0.040, 0.105), smoothstep(0.2, 1.0, vUv.y));

  // the nebula: the baked gas, carried by the wind; lit by the game's three glows (violet from the top right, blue from the
  // bottom left, plum from the bottom right). Peace thins its haze (clear air), and unsettled air turns milky.
  vec3 g = mix(gas(uNebA, uv - uOffA), gas(uNebB, uv - uOffB), uNebMix);
  float cloud = g.r, fil = g.g, n = g.b;
  float haze = 1.35 - 0.75 * peace;
  float gV = blob(uv - vec2(0.74 * asp, 1.06), vec2(0.62 * asp, 0.66));
  float gB = blob(uv - vec2(0.02 * asp, -0.06), vec2(0.52 * asp, 0.64));
  float gM = blob(uv - vec2(0.98 * asp, -0.04), vec2(0.40 * asp, 0.52));
  vec3 neb = vec3(0.30, 0.22, 0.66) * gV + vec3(0.15, 0.30, 0.54) * 0.85 * gB + vec3(0.46, 0.17, 0.40) * 0.6 * gM;
  col += neb * (0.05 + 0.24 * cloud + 0.34 * fil * (0.3 + cloud)) * haze;
  col += vec3(0.034, 0.030, 0.050) * (1.0 - peace) * (0.45 + 0.9 * cloud);
  // a faint band of unresolved stars across the sky, from the bottom left to the top right
  float band = blob(vec2(dot(uv - vec2(0.5 * asp, 0.5), normalize(vec2(-0.42, 1.0))), 0.0), vec2(0.20, 1.0));
  col += vec3(0.20, 0.18, 0.32) * band * (0.04 + 0.08 * n) * haze;

  // BLACK: silver-plum smoke turning slowly inward round an eye in the open sky. Where it gathers the night deepens into
  // velvet; its thin folds catch a low silver-plum light, and a dim plum glow wells between the arms. Depth and gravity,
  // never menace: it stays within its own reach.
  if (LB > 0.06) {
    float bs = clamp(fh, 0.42, 1.0);
    vec2 d = (uv - F) / bs * vec2(1.0, 1.12); float r = length(d);
    if (r < 0.75) {                                         // the smoke's reach: nothing of it shows further out
    float f = fract(uInflow), wa = 1.0 - abs(2.0 * f - 1.0);
    float sm = mix(smoke(d, r, fract(f + 0.5), 17.3), smoke(d, r, f, 3.1), wa);
    float reach = smoothstep(0.04, 0.26, r) * (1.0 - smoothstep(0.42, 0.75, r));
    float body = smoothstep(0.42, 0.74, sm) * reach;
    float k = smoothstep(0.06, 0.12, LB) * LB;
    col = mix(col, vec3(0.016, 0.010, 0.034), body * 0.45 * k);
    float fold = smoothstep(0.47, 0.56, sm) * (1.0 - smoothstep(0.56, 0.68, sm)) * reach;
    col += vec3(0.62, 0.55, 0.70) * fold * 0.24 * k;
    col += vec3(0.22, 0.12, 0.26) * (1.0 - smoothstep(0.22, 0.5, sm)) * reach * 0.26 * k;
    col *= 1.0 - 0.3 * k * exp(-r * r / 0.015);
    }
  }

  // GREEN: two aurora curtains across the open sky, folding slowly: a sharp bright hem, fine rays rising from it and fading
  // up through teal into violet; brighter where a fold turns toward us; they breathe. In shadow (stuck in their ways) they
  // slow to stillness and the light grows heavy and mossy.
  if (LG > 0.06) {
    float x = vUv.x, sG = uSh[4], acc = 0.0, hi = 0.0, amp = max(fh, 0.5);
    float b0 = fb + fh * mix(0.40, 0.63, fh);
    for (int k = 0; k < 2; k++) {
      float fk = float(k), ph = uAur * (1.0 + 0.35 * fk) + fk * 3.0;
      float a1 = x * 4.0 + ph * 0.9, a2 = x * 9.5 - ph * 0.6 + fk * 1.3;
      float wan = 0.5 * sin(x * 7.3 + fk * 7.0 + ph * 0.23) + 0.5 * sin(x * 3.1 - fk * 4.0 - ph * 0.13);
      float base = b0 + amp * (0.13 * fk + 0.055 * sin(a1) + 0.03 * sin(a2) + 0.025 * wan);
      float slope = min(1.0, abs(0.22 * cos(a1) + 0.285 * cos(a2)));
      float dy = vUv.y - base;
      if (dy < -0.06) continue;                              // well below this curtain's hem: none of its light
      float hem = dy < 0.0 ? exp(-dy * dy / 0.0005) : exp(-dy / (0.16 + 0.05 * fk + 0.06 * sG));
      float rays = 0.55 + 0.45 * noise(vec2(x * 96.0 + fk * 31.0, ph * 1.3 + dy * 0.6));
      rays *= 0.7 + 0.3 * noise(vec2(x * 24.0 - ph * 0.7, dy * 2.2 + fk));
      float along = smoothstep(0.16, 0.60, 0.5 + 0.32 * sin(x * 11.9 + fk * 4.0 - ph * 0.5) + 0.18 * sin(x * 5.3 - fk * 2.0 + ph * 0.21));
      float breath = 0.7 + 0.3 * sin(uT * 0.21 * (1.0 - 0.85 * sG) + fk * 2.4);
      float c = hem * mix(1.0, rays, smoothstep(-0.012, 0.03, dy)) * along * (0.65 + 0.8 * slope) * breath * (1.0 - 0.3 * fk);
      acc += c; hi += c * smoothstep(0.02, 0.24, dy);
    }
    float tip = clamp(hi / max(acc, 1e-3), 0.0, 1.0);
    vec3 ac = mix(vec3(0.42, 1.0, 0.52), vec3(0.28, 0.74, 0.78), smoothstep(0.0, 0.8, tip));
    ac = mix(ac, vec3(0.56, 0.38, 0.80), smoothstep(0.6, 1.0, tip) * 0.5);
    ac = mix(ac, vec3(0.40, 0.56, 0.34), sG * 0.5);
    col += ac * acc * 0.74 * smoothstep(0.06, 0.12, LG) * LG;
  }

  // BLUE: clear, cool, refracted. Broad lenses of clear blue light drift slowly; through them runs a fine caustic network
  // (light folded through glass), exact and slow. In shadow (indecisive) a second network wavers beside the first and
  // never settles.
  if (LU > 0.06) {
    float k = smoothstep(0.06, 0.12, LU) * LU;
    float lens = smoothstep(0.30, 0.80, fbm3(uv * 0.8 + vec2(-uCaus * 0.05, 3.0)));
    vec2 cp = rot(0.35) * uv * 2.7 + vec2(uCaus * 0.12, -uCaus * 0.07);
    float ca = caustic(mod(cp * 6.2831853 / 3.0, 6.2831853) - 250.0, uCaus * 1.4 + 23.0);
    if (uSh[1] > 0.01) {
      vec2 o = vec2(sin(uT * 0.9), cos(uT * 0.67)) * 0.34 * uSh[1];
      ca = max(ca, 1.25 * uSh[1] * caustic(mod((cp + o) * 6.2831853 / 3.0, 6.2831853) - 250.0, uCaus * 1.4 + 23.0));
    }
    float hue = 0.5 + 0.5 * sin(uv.x * 4.1 + 1.3) * cos(uv.y * 3.7 - 0.6);
    vec3 glint = mix(vec3(0.62, 0.86, 1.0), mix(vec3(0.55, 0.95, 0.95), vec3(0.72, 0.70, 1.0), hue), 0.35);
    ca = smoothstep(0.03, 0.8, ca);
    col += vec3(0.06, 0.14, 0.32) * lens * 0.53 * k;
    col += glint * ca * (0.25 + 0.75 * lens) * 0.49 * k;
  }

  // RED: warmth, not fire. The hearth: a band of ember light along the whole floor of the sky (the lowest fifth, so it
  // shows across any width, a phone's too), deep red (#8c2f1f) at its top warming to a bright ember (#f38c6b) at the very
  // floor; its upper edge is lifted unevenly by the heat, and in it the coals glow and dim, each at its own pace (fast to
  // flare, fast to fade). Above it the gas glows faintly warm, as an emission nebula does. Nothing flame-shaped climbs:
  // the brushstroke of ember light and the embers are drawn crisp in the sparks layer.
  if (LR > 0.06) {
    float k = smoothstep(0.06, 0.12, LR) * LR, sR = uSh[3];
    float flick = 0.86 + 0.14 * sin(uT * 2.1) * sin(uT * 1.37 + 1.0);
    // the band's upper edge (heights of the sky from the floor): about a fifth, rising and falling along its length
    float top = 0.22 + 0.06 * (noise(vec2(vUv.x * 4.0 - uDrift * 1.5, uT * 0.05)) - 0.5) + 0.025 * sin(vUv.x * 9.0 + uT * 0.21);
    float h = clamp(1.0 - vUv.y / top, 0.0, 1.0);          // 1 at the floor, 0 at the band's edge
    // the coals: folded noise drifting slowly sideways and up; where it creases it glows hot. Their light pulses quickly.
    vec3 deep = vec3(0.55, 0.18, 0.12), bright = vec3(0.95, 0.55, 0.42), hot = vec3(1.0, 0.80, 0.55);
    if (h > 0.0) {
      vec2 rp = vec2(uv.x * 3.2 - uDrift * 1.3, vUv.y * 5.0 - uT * 0.06);
      float tb = turb(rp + 0.45 * vec2(sin(rp.y * 1.7 + uT * 0.31), cos(rp.x * 1.3 - uT * 0.23)));
      float coal = pow(1.0 - tb, 3.0) * (0.75 + 0.25 * sin(uT * 3.1 + rp.x * 2.3));
      vec3 hearth = mix(deep, bright, h * h) * h;
      col += hearth * 0.35 * k * flick * (1.0 + 0.3 * sR);
      col += mix(bright, hot, coal) * coal * pow(h, 0.9) * 0.22 * k * flick * (1.0 + 0.6 * sR);
    }
    // in shadow (reckless) the heat climbs higher: a faint haze above the band
    col += deep * smoothstep(top + 0.25 * sR, top * 0.6, vUv.y) * 0.08 * sR * k;
    // the warm gas above, faint, most toward the floor
    float em = smoothstep(1.0, 0.1, vUv.y);
    col += vec3(0.82, 0.21, 0.14) * (0.004 + 0.025 * cloud + 0.10 * fil * (0.3 + cloud)) * em * haze * k;
  }

  // WHITE: dawn along the lower horizon: a bright gold edge and a rising glow through rose; and a fan of even rays from
  // below the open sky's floor (radial order). It breathes; in shadow (rigid) it stops breathing and the rays harden.
  if (LW > 0.06) {
    float k = smoothstep(0.06, 0.12, LW) * LW;
    float y = vUv.y, sW = uSh[0];
    float breathe = 1.0 + 0.10 * sin(uT * 0.31) * (1.0 - sW);
    vec3 gold = mix(vec3(0.90, 0.86, 0.74), vec3(1.0, 0.82, 0.50), 0.3 + 0.7 * content);
    vec3 rose = mix(vec3(0.60, 0.55, 0.66), vec3(0.86, 0.56, 0.50), 0.3 + 0.7 * content);
    vec3 dawn = gold * exp(-y / 0.022) * 0.33 + mix(rose, gold, 0.45) * exp(-y / (0.11 + 0.10 * LW)) * 0.185;
    dawn = mix(dawn, vec3(dot(dawn, vec3(0.3, 0.5, 0.2))) * vec3(0.86, 0.94, 1.12), 0.55 * sW);
    vec2 dd = uv - vec2(F.x, fb - 0.30 * fh);
    float ang = atan(dd.x, dd.y), yy = (uv.y - fb) / max(fh, 0.2);
    float rays = pow(abs(cos(ang * 6.0)), 30.0 + 50.0 * sW) * smoothstep(0.9, 0.02, yy) * smoothstep(1.35, 0.2, abs(ang)) * step(0.0, yy + 0.02);
    dawn += mix(gold, vec3(0.86, 0.92, 1.0), sW) * rays * 0.09 * (1.0 + 2.2 * sW);
    col += dawn * k * breathe;
  }

  // the times outside: the far horizon, faintly, in the era's colours laid side by side
  if (uEra.y > 0.004) {
    float x = vUv.x; vec3 ec = uE0;
    if (uEra.x > 2.5) ec = x < 0.5 ? mix(uE0, uE1, smoothstep(0.05, 0.5, x)) : mix(uE1, uE2, smoothstep(0.5, 0.95, x));
    else if (uEra.x > 1.5) ec = mix(uE0, uE1, smoothstep(0.15, 0.85, x));
    col += ec * exp(-vUv.y / 0.09) * 0.18 * uEra.y;
  }

  // strain is wind: a veil of long slanting streaks blowing across, faster than the gas
  if (strain > 0.004) {
    vec2 wv = rot(-${VEIL.toFixed(3)}) * uv;
    vec2 vp = vec2(wv.x * 0.75 - uDrift * 2.8, wv.y * 4.6 + 0.4 * sin(wv.x * 1.3 + uT * 0.05));
    float v = smoothstep(0.50, 0.84, fbm3(vp + vec2(0.0, 0.7 * noise(vp * 0.3 + uT * 0.04))));
    col += vec3(0.16, 0.15, 0.22) * v * 1.4 * strain;
  }

  // satisfaction is the warmth of the light: a warm cast and a warm rim along the horizon when content, a cool cast and a
  // cool rim when not (never darker)
  col *= mix(vec3(0.86, 0.95, 1.16), vec3(1.16, 1.02, 0.84), content);
  col += mix(vec3(0.030, 0.060, 0.110), vec3(0.150, 0.088, 0.036), content) * exp(-vUv.y / 0.06) * 0.55;

  // the ripple's water film: a glint along the ring and a damp sheen behind it
  col += vec3(0.50, 0.60, 0.90) * ring * 0.10 + vec3(0.72, 0.80, 1.0) * crest * 0.11 + vec3(0.10, 0.12, 0.20) * damp * 0.12;

  // the vignette: Black deepens it into velvet; in shadow (ruthless) it eats a little more of the light at the edges
  vec2 vd = (vUv - 0.5) * vec2(1.0, 1.1);
  float vr = length(vd), sB = uSh[2];
  col *= 1.0 - smoothstep(0.32 - 0.06 * sB, 0.90, vr) * min(0.62, 0.30 + 0.22 * LB + 0.09 * sB);

  // a little noise against banding in the dark gradients
  col += (hash(gl_FragCoord.xy + fract(uT) * 61.0) - 0.5) / 255.0;
  gl_FragColor = vec4(max(col, 0.0), 1.0);
}`;
  // The picture on the screen: the last field dissolving into the newest, so a field drawn 30 or 15 times a second still moves smoothly
  const COPY_FRAG = `uniform sampler2D uA, uB; uniform float uMix; varying vec2 vUv;
void main() { gl_FragColor = vec4(mix(texture2D(uA, vUv).rgb, texture2D(uB, vUv).rgb, uMix), 1.0); }`;

  // which renderer this browser asks for: "force" takes WebGL even where it would be slow (software WebGL, for the shader
  // path's own test), "off" takes the Canvas2D painting; anything else asks for fast WebGL only
  const glWish = () => { try { return localStorage.getItem("chroma.living.gl") || ""; } catch (_) { return ""; } };
  // Build the field's WebGL programs on a canvas; null when WebGL is missing, would be slow (failIfMajorPerformanceCaveat:
  // a machine without fast graphics, headless browsers too) or a shader will not compile. Each is told as a warning: the
  // painting then stands in, and nothing is wrong with the page.
  function makeGL(canvas) {
    const wish = glWish();
    if (wish === "off") return null;
    let gl = null;
    try { gl = canvas.getContext("webgl", { alpha: false, antialias: false, depth: false, stencil: false, premultipliedAlpha: false, powerPreference: "low-power", failIfMajorPerformanceCaveat: wish !== "force" }); } catch (_) { gl = null; }
    if (!gl) { console.warn("living: sky without fast WebGL, painted with Canvas2D"); return null; }
    const hp = gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_FLOAT);
    const prec = hp && hp.precision > 0 ? "highp" : "mediump";
    const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { console.warn("living: sky shader, painted with Canvas2D:", gl.getShaderInfoLog(s)); return null; } return s; };
    const vs = sh(gl.VERTEX_SHADER, VERT);
    const prog = (src, names) => {
      const fs = sh(gl.FRAGMENT_SHADER, `precision ${prec} float;\n${src}`);
      if (!vs || !fs) return null;
      const pr = gl.createProgram(); gl.attachShader(pr, vs); gl.attachShader(pr, fs); gl.bindAttribLocation(pr, 0, "aP"); gl.linkProgram(pr);
      if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) { console.warn("living: sky program, painted with Canvas2D:", gl.getProgramInfoLog(pr)); return null; }
      const u = {}; names.forEach((k) => { u[k] = gl.getUniformLocation(pr, k); });
      return { pr, u };
    };
    const NEB = prog(NEB_FRAG, ["uBox", "uCen", "uT", "uDrift", "uStretch"]);
    const FLD = prog(FIELD_FRAG, ["uRes", "uNebBox", "uNebA", "uNebB", "uOffA", "uOffB", "uNebMix", "uT", "uDrift", "uSwirl", "uInflow", "uAur", "uCaus", "uL", "uSh", "uWx", "uFoc", "uE0", "uE1", "uE2", "uEra", "uRip"]);
    const CPY = prog(COPY_FRAG, ["uA", "uB", "uMix"]);
    if (!NEB || !FLD || !CPY) return null;
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);   // one triangle covers the screen
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    // a texture with a framebuffer to draw into: the baked gas and the field's last two pictures
    const target = (w, h) => {
      const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
      const fb = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fb);
      gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      return { t, fb, w, h };
    };
    const drop = (x) => { if (x) { gl.deleteTexture(x.t); gl.deleteFramebuffer(x.fb); } };
    let timer = null; try { timer = gl.getExtension("EXT_disjoint_timer_query"); } catch (_) { timer = null; }
    return { gl, NEB, FLD, CPY, target, drop, timer };
  }

  /* ---------- sprites: a star's light drawn once into a little canvas and stamped every frame ---------- */
  const TINT = ["255,246,232", "242,227,166", "170,206,250", "214,200,232", "255,176,140", "164,228,180", "226,230,255"];   // warm white, W U B R G, cool white
  function spriteOf(rgb, size, kind) {
    const c = document.createElement("canvas"); c.width = c.height = size; const g = c.getContext("2d"), h = size / 2;
    if (kind === "spike") {   // four points, tapered: the game's spark (04-line.js cosmos) and Blue's crisp light
      const gr = g.createRadialGradient(h, h, 0, h, h, h);
      gr.addColorStop(0, `rgba(255,255,255,0.95)`); gr.addColorStop(0.25, `rgba(${rgb},0.45)`); gr.addColorStop(1, `rgba(${rgb},0)`);
      g.fillStyle = gr; const t = size * 0.035;
      [0, Math.PI / 2].forEach((a) => { g.save(); g.translate(h, h); g.rotate(a); g.beginPath(); g.moveTo(0, -h); g.lineTo(t, 0); g.lineTo(0, h); g.lineTo(-t, 0); g.closePath(); g.fill(); g.restore(); });
      return c;
    }
    const gr = g.createRadialGradient(h, h, 0, h, h, h);
    if (kind === "core") { gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.16, `rgba(${rgb},0.95)`); gr.addColorStop(0.38, `rgba(${rgb},0.30)`); gr.addColorStop(0.7, `rgba(${rgb},0.06)`); gr.addColorStop(1, `rgba(${rgb},0)`); }
    else { gr.addColorStop(0, `rgba(${rgb},0.5)`); gr.addColorStop(0.3, `rgba(${rgb},0.16)`); gr.addColorStop(1, `rgba(${rgb},0)`); }
    g.fillStyle = gr; g.fillRect(0, 0, size, size); return c;
  }
  let SPR = null;
  const sprites = () => SPR || (SPR = { core: TINT.map((t) => spriteOf(t, 32, "core")), halo: TINT.map((t) => spriteOf(t, 64, "halo")), spike: spriteOf(TINT[6], 64, "spike"), spikeW: spriteOf(TINT[1], 64, "spike"), silver: spriteOf("236,240,255", 32, "core") });

  /* ---------- the Canvas2D painting's textures (the sky without WebGL) ---------- */
  // Without WebGL each layer of the shader is frozen into a small texture, the first time that layer shows, and every
  // frame only moves the textures about. Their noise tiles: the lattice wraps every px by py cells, so a texture can slide
  // for ever without a seam. The lattice's values come from CH.rng, like every other chance in the Living HUD.
  let LAT = null;
  function pnoise(x, y, px, py, o) {
    if (!LAT) { LAT = new Float32Array(65536); const r = CH.rng(4242); for (let i = 0; i < 65536; i++) LAT[i] = r(); }
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const u = xf * xf * xf * (xf * (xf * 6 - 15) + 10), v = yf * yf * yf * (yf * (yf * 6 - 15) + 10);
    const x0 = ((xi % px) + px) % px, x1 = (x0 + 1) % px, y0 = ((yi % py) + py) % py, y1 = (y0 + 1) % py;
    const r0 = ((y0 + o) & 255) << 8, r1 = ((y1 + o) & 255) << 8, c0 = (x0 + o * 3) & 255, c1 = (x1 + o * 3) & 255;
    const a = LAT[r0 + c0], b = LAT[r0 + c1], c = LAT[r1 + c0], d = LAT[r1 + c1];
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function pfbm(x, y, px, py, oct, seed) {
    let s = 0, a = 0.5, n = 0;
    for (let i = 0; i < oct; i++) { s += a * pnoise(x, y, px, py, seed + i * 53); n += a; x *= 2; y *= 2; px *= 2; py *= 2; a *= 0.5; }
    return s / n;
  }
  function pturb(x, y, px, py, oct, seed) {   // the folded sum: creased where the noise crosses its middle
    let s = 0, a = 0.5, n = 0;
    for (let i = 0; i < oct; i++) { s += a * Math.abs(2 * pnoise(x, y, px, py, seed + i * 53) - 1); n += a; x *= 2; y *= 2; px *= 2; py *= 2; a *= 0.5; }
    return s / n;
  }
  const sstep = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  const bl = (dx, dy, sx, sy) => Math.exp(-((dx / sx) ** 2 + (dy / sy) ** 2));
  // the caustic network of the shader, for one point and moment
  function causticAt(px, py, t) {
    let ix = px, iy = py, c = 1;
    for (let n = 0; n < 4; n++) {
      const tt = t * (1 - 3.5 / (n + 1)), nx = px + Math.cos(tt - ix) + Math.sin(tt + iy), ny = py + Math.sin(tt - iy) + Math.cos(tt + ix);
      ix = nx; iy = ny;
      c += 1 / Math.hypot(px / (Math.sin(ix + tt) / 0.005), py / (Math.cos(iy + tt) / 0.005));
    }
    c /= 4; c = 1.17 - Math.pow(c, 1.4);
    return sstep(0.03, 0.8, Math.pow(Math.abs(c), 8));
  }
  // light to be added ('lighter'): the colour scaled to its brightest channel, the brightness kept in alpha
  function addPx(o, r, g, b) { const m = Math.max(r, g, b, 1e-6); o[0] = r / m; o[1] = g / m; o[2] = b / m; o[3] = Math.min(1, m); }

  // A texture is baked a few rows at a time, inside a small share of each frame (all the skies on the page share it), so
  // a layer never stalls the page: it fades in once its texture is whole. With motion off there is no fading: the sky
  // bakes in a larger share of a few frames and its one still picture shows when every texture it needs is whole.
  // fn(x, y, out) writes r, g, b, a (0..1, straight).
  function job(w, h, fn) { return { w, h, fn, y: 0, c: null, im: null, ready: false }; }
  let bakeStamp = -1, bakeUntil = 0;
  function work(j, all, stamp, budget) {
    if (j.ready) return true;
    if (!j.im) { j.c = document.createElement("canvas"); j.c.width = j.w; j.c.height = j.h; j.im = j.c.getContext("2d").createImageData(j.w, j.h); }
    const now = performance.now();
    if (!all) { if (stamp !== bakeStamp) { bakeStamp = stamp; bakeUntil = now + (budget || 2.5); } if (now >= bakeUntil) return false; }
    const d = j.im.data, o = [0, 0, 0, 0];
    while (j.y < j.h) {
      for (let x = 0, i = j.y * j.w * 4; x < j.w; x++, i += 4) {
        o[0] = o[1] = o[2] = 0; o[3] = 1; j.fn(x, j.y, o);
        d[i] = o[0] * 255 + 0.5; d[i + 1] = o[1] * 255 + 0.5; d[i + 2] = o[2] * 255 + 0.5; d[i + 3] = o[3] * 255 + 0.5;
      }
      j.y++;
      if (!all && (j.y & 3) === 0 && performance.now() >= bakeUntil) break;
    }
    if (j.y < j.h) return false;
    j.c.getContext("2d").putImageData(j.im, 0, 0); j.im = null; j.fn = null; j.ready = true;
    return true;
  }
  // the textures every sky shares, whatever its size (Black's smoke, Red's heat haze, Green's curtain)
  const SHARED2D = {};
  const JOBS = {
    // BLACK: the smoke at the start of its fall, over d in [-2, 2] (heights from the eye). One texture both darkens and
    // lights: its alpha is the velvet body (the night under it deepens), its colour the silver-plum folds and the plum
    // between the arms. The painting turns it and shrinks it toward the eye, two copies cross-fading, as the shader does,
    // and masks it to its reach.
    smoke() {
      const S = 300;
      return Object.assign(job(S, S, (x, y, o) => {
        const dx = ((x + 0.5) / S) * 4 - 2, dy = ((y + 0.5) / S) * 4 - 2, r = Math.hypot(dx, dy), a = 1.25 * Math.log(r + 0.06);
        const c = Math.cos(a), s = Math.sin(a), sm = pfbm((c * dx - s * dy) * 1.9 + 40, (s * dx + c * dy) * 1.9 + 40, 256, 256, 4, 11);
        const reach = sstep(0.02, 0.22, r) * (1 - sstep(1.7, 2, r));
        const body = sstep(0.42, 0.74, sm) * reach, f = sstep(0.47, 0.56, sm) * (1 - sstep(0.56, 0.68, sm)) * reach, p = (1 - sstep(0.22, 0.5, sm)) * reach;
        const lr = f * 0.149 + p * 0.0572, lg = f * 0.132 + p * 0.0312, lb = f * 0.168 + p * 0.0676, al = Math.max(0.45 * body, lb, 1e-4);
        o[0] = lr / al; o[1] = lg / al; o[2] = lb / al; o[3] = al;
      }), { S });
    },
    // RED: the heat haze, a tile four cells each way (1.67 by 2.35 heights of sky) that repeats both ways, so it rises for
    // ever; coloured by the warm ramp, deep red through orange to gold where it is hottest. The hearth masks it, low.
    wisp() {
      const Ww = 260, Wh = 366;
      return Object.assign(job(Ww, Wh, (x, y, o) => {
        const s = ((x + 0.5) / Ww) * 4, q = ((y + 0.5) / Wh) * 4;
        const wx = pnoise(s, q, 4, 4, 5), wy = pnoise(s + 1.7, q + 2.3, 4, 4, 9);
        const tb = pturb(s + 0.9 * wx, q + 0.9 * wy, 4, 4, 4, 21);
        const v = clamp(Math.pow(1 - tb, 3.6) * 1.9 * 0.8);
        const m1 = sstep(0.15, 0.6, v), m2 = sstep(0.7, 1, v), k = Math.pow(v, 1.2);
        let r = 0.50 + 0.48 * m1, g = 0.14 + 0.36 * m1, b = 0.08 + 0.16 * m1;
        r += (1.0 - r) * m2; g += (0.80 - g) * m2; b += (0.52 - b) * m2;
        addPx(o, r * k, g * k, b * k);
      }), { Ww, Wh });
    },
    // GREEN: one curtain laid straight, half again as wide as the sky (it tiles): its sharp hem near the bottom, the fine
    // rays rising from it, green at the hem through teal into violet at the top; lit in stretches along its length
    curtain() {
      const Aw = 512, M = 40, Ah = 128, top = 0.55, bot = -0.05;
      return Object.assign(job(Aw + M, Ah, (x, y, o) => {
        const xs = ((x % Aw) + 0.5) / Aw, dy = top - ((y + 0.5) / Ah) * (top - bot);
        const hem = dy < 0 ? Math.exp((-dy * dy) / 0.0005) : Math.exp(-dy / 0.16);
        let rays = 0.55 + 0.45 * pnoise(xs * 96, 0.3 + dy * 0.6, 96, 256, 3);
        rays *= 0.7 + 0.3 * pnoise(xs * 24, dy * 2.2, 24, 256, 7);
        const along = sstep(0.30, 0.72, pnoise(xs * 3, 0.5, 3, 256, 13));
        const c = hem * (1 + (rays - 1) * sstep(-0.012, 0.03, dy)) * along;
        const tip = sstep(0.02, 0.24, dy), m = sstep(0, 0.8, tip), mv = sstep(0.6, 1, tip) * 0.5;
        let r = 0.42 - 0.14 * m, g = 1.0 - 0.26 * m, b = 0.52 + 0.26 * m;
        r += (0.56 - r) * mv; g += (0.38 - g) * mv; b += (0.80 - b) * mv;
        addPx(o, r * c * 0.5, g * c * 0.5, b * c * 0.5);
      }), { Aw, M, Ah, hemY: (top / (top - bot)) * Ah, span: top - bot });
    },
  };

  /* ---------- B1: the shared ink filter ---------- */
  // #chs-ink lets whatever ink it is put on (filter: url(#chs-ink)) bleed: the edge wanders a little (a gentle displacement,
  // at most about three pixels) and a soft halo of the same ink spreads round it; both grow with the wet, and the letter
  // body itself stays whole and legible. It lives in its own small svg at the end of <body>, there while the sky stands.
  function ensureFilter(id) {
    let f = document.getElementById(id);
    if (f) return f;
    let svg = document.getElementById("chs-atmos-defs");
    if (!svg) {
      svg = document.createElementNS(SVGNS, "svg"); svg.id = "chs-atmos-defs"; svg.setAttribute("aria-hidden", "true"); svg.setAttribute("focusable", "false");
      svg.setAttribute("width", "0"); svg.setAttribute("height", "0"); svg.style.cssText = "position:absolute;width:0;height:0;overflow:hidden";
      document.body.appendChild(svg);
    }
    const el = (tag, attrs, kids) => { const e = document.createElementNS(SVGNS, tag); Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v)); (kids || []).forEach((k) => e.appendChild(k)); return e; };
    f = el("filter", { id, x: "-10%", y: "-40%", width: "120%", height: "180%", "color-interpolation-filters": "sRGB" }, [
      el("feTurbulence", { type: "fractalNoise", baseFrequency: "0.035", numOctaves: "3", seed: "7", result: "n" }),
      el("feDisplacementMap", { in: "SourceGraphic", in2: "n", scale: "1.6", xChannelSelector: "R", yChannelSelector: "G", result: "d" }),
      el("feGaussianBlur", { in: "d", stdDeviation: "1.5", result: "halo" }),
      el("feComponentTransfer", { in: "halo", result: "bleed" }, [el("feFuncA", { type: "linear", slope: "0.27", intercept: "0" })]),
      el("feMerge", {}, [el("feMergeNode", { in: "bleed" }), el("feMergeNode", { in: "d" })]),
    ]);
    svg.appendChild(f);
    return f;
  }
  // the bleed for a wetness: a broader, slower grain and a wider, fuller halo the wetter the ink
  function setFilterWet(f, wet) {
    const [t, d, b, ct] = f.children;
    t.setAttribute("baseFrequency", (0.035 - 0.02 * wet).toFixed(4));
    d.setAttribute("scale", (0.3 + 2.6 * wet).toFixed(2));
    b.setAttribute("stdDeviation", (0.4 + 2.2 * wet).toFixed(2));
    ct.firstChild.setAttribute("slope", (0.55 * wet).toFixed(3));
  }
  let primary = null;   // the page's one sky while it stands (CH.ink reads its wetness and inks)

  /* ---------- B1: the ink. One engine lays marks on the night sky (the bright hues as pigment on the dark) or on a
     parchment panel (the engraving inks, multiplied); wetness sets everything about a mark. ---------- */
  const mixRGB = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
  // a mark's inks: its body, its denser edge, and the darker tide line it dries to
  function inkCols(c, palette) {
    if (/^#/.test(c)) { const b = CH.rgb(c); return { body: b, rim: b.map((v) => v * 0.78), tide: b.map((v) => v * 0.6) }; }
    const L = CH.COLORS.includes(c) ? c : "W";
    if (palette === "parch") { const d = CH.rgb(CH.HUE.ink[L]); return { body: d, rim: d.map((v) => v * 0.82), tide: d.map((v) => v * 0.62) }; }
    const b = CH.rgb(CH.HUE.bright[L]), d = CH.rgb(CH.HUE.ink[L]);
    return { body: b, rim: mixRGB(b, d, 0.3), tide: b.map((v) => v * 0.6) };
  }
  // seeded tiles: the pigment's uneven settling (soft, low frequency) and the dried pigment's grain (fine)
  let MOTTLE = null, GRAIN = null;
  function mottleTile() {
    if (MOTTLE) return MOTTLE;
    const N = 128, c = document.createElement("canvas"); c.width = c.height = N; const g = c.getContext("2d"), im = g.createImageData(N, N);
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const v = pfbm(x / 32, y / 32, 4, 4, 3, 77), i = (y * N + x) * 4;
      im.data[i + 3] = Math.round(255 * Math.pow(sstep(0.32, 0.78, v), 1.4));
    }
    g.putImageData(im, 0, 0); return (MOTTLE = c);
  }
  function grainTile() {
    if (GRAIN) return GRAIN;
    const c = document.createElement("canvas"); c.width = c.height = 96; const g = c.getContext("2d"), r = CH.rng(77);
    for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(0,0,0,${(0.12 + 0.4 * r()).toFixed(2)})`; g.fillRect(r() * 96, r() * 96, 0.6 + r() * 0.8, 0.6 + r() * 0.8); }
    return (GRAIN = c);
  }
  // a context's pattern of a tile, made once
  const PATS = new WeakMap();
  const patOf = (g, tile) => { let m = PATS.get(g); if (!m) PATS.set(g, (m = new Map())); let p = m.get(tile); if (!p) m.set(tile, (p = g.createPattern(tile, "repeat"))); return p; };
  // how large ink spreads on a page of this size: by its area, so a small sky (a medallion, a phone) takes smaller drops
  const inkScale = (w, h) => clamp(Math.sqrt(w * h) / 1000, 0.3, 1.2);
  const CANFILTER = (() => { try { return typeof document.createElement("canvas").getContext("2d").filter === "string"; } catch (_) { return false; } })();

  // makeInk(palette, rngSeed): marks and how they are laid, spread, dried and drawn. The caller owns the canvases and the clock.
  function makeInk(palette, seed) {
    const marks = [], R = CH.rng(seed);
    const EN = 56, SMAX = 90, PEN = 0.22;     // outline points of a drop; the most points of a stroke; below this wetness, ink is a pen line
    // how far a drop may spread on this page (CSS px; s is the page's ink scale, inkScale below: 1 on a 1000 x 1000 page)
    const reach = (wet, s) => (12 + 112 * wet) * s;
    function base(kind, x, y, cols, wet, clock, still) {
      const c = cols && cols.length ? cols : ["W", "U"];
      const b = {
        kind, x, y, born: clock, dryFrom: clock, last: clock, pen: wet < PEN,
        tau: 0.12 + 0.4 * wet + 1.9 * wet * wet,        // spreading time constant: fast and short on a dry page, slow when wet
        dryIn: 0.35 + 6.5 * wet,                         // how long the pigment stays wet once it has spread
        amp: 0.07 + 0.15 * wet, soft: wet, seed: R() * 200,
        k1: inkCols(c[0], palette), k2: inkCols(c[1] || c[0], palette), still: !!still,
        pts: new Float32Array((kind === "drop" ? EN : SMAX * 2 + 4) * 2), n: 0, dry: 0, fade: 1,
      };
      // set ink stays: a dry mark holds about twelve seconds as a crisp stain; a wet one dries into the same lasting stain
      b.hold = b.tau * 2 + b.dryIn + 6 + 6 * (1 - wet); b.fadeT = 4 + 3 * wet;
      marks.push(b);
      while (marks.length > 48) marks.shift();
      // with motion off, only the eight newest still marks are kept
      let nStill = 0; for (let i = marks.length - 1; i >= 0; i--) if (marks[i].still && ++nStill > 8) marks.splice(i, 1);
      return b;
    }
    function drop(x, y, cols, wet, clock, still, s) {
      const b = base("drop", x, y, cols, wet, clock, still);
      b.Rmax = b.pen ? (2.6 + 10 * wet) * (0.85 + 0.3 * R()) * clamp(0.6 + 0.4 * s, 0.7, 1.1) : reach(wet, s) * (0.85 + 0.3 * R());
      b.R = b.still ? b.Rmax : 0.5; b.rr = new Float32Array(EN);
      // two or three backruns (where water creeps back into the drying pigment, it pushes out fringed fingers and leaves a
      // pale fan behind them), and the second ink charged into one side, wet into wet
      b.lobes = []; if (!b.pen) for (let i = 0, n = 2 + (R() < 0.35 ? 1 : 0); i < n; i++) b.lobes.push({ a: R() * TAU, w: 0.32 + 0.25 * R(), amp: 0.6 + 0.4 * R() });
      b.charge = { a: R() * TAU, d: 0.38 + 0.2 * R(), r: 0.5 + 0.2 * R() };
      return b;
    }
    function stroke(x, y, cols, wet, clock, still, s, press) {
      const b = base("stroke", x, y, cols, wet, clock, still);
      b.w = b.pen ? 1 : reach(wet, s) * 0.22;        // a wash stroke's half width when spread; a pen line's width comes per point
      b.P = [{ x, y, t: clock, s: 0, p: press ?? 0.6 }];
      b.nx = new Float32Array(SMAX); b.ny = new Float32Array(SMAX); b.rl = new Float32Array(SMAX); b.rr = new Float32Array(SMAX);
      return b;
    }
    function strokeTo(b, x, y, clock, press) {
      const q = b.P[b.P.length - 1], d = Math.hypot(x - q.x, y - q.y);
      if (b.P.length >= SMAX) return false;
      b.P.push({ x, y, t: clock, s: q.s + d, p: press ?? 0.6 }); b.last = clock; b.dryFrom = clock;
      b.hold = clock - b.born + b.tau * 2 + b.dryIn + 6 + 6 * (1 - b.soft);
      return true;
    }
    // Each frame, a mark's outline is measured once: how far each part has spread, pushed in and out by noise (broad lobes,
    // a ragged middle and a fine fringe when wet), the backrun fingers pushed further out where water crept back; read
    // around the drop or along the stroke, so it never jumps. shape(b, mul) lays the outline at any fraction of that spread.
    function measure(b, clock) {
      if (b.kind === "drop") {
        const gr = b.R / b.Rmax, late = b.still ? 1 : smooth(clamp((clock - b.born - b.tau) / (1.6 * b.tau + 0.4)));
        for (let i = 0; i < EN; i++) {
          const a = (i / EN) * TAU, nx = Math.cos(a), ny = Math.sin(a);
          const n1 = CH.noise(b.seed + nx * 1.25 + 10, b.seed + ny * 1.25 + gr * 0.7);
          const n2 = CH.noise(b.seed + nx * 3.1 + 40, b.seed + ny * 3.1 + gr * 1.5);
          const n3 = CH.noise(b.seed + nx * 7.3 + 70, b.seed + ny * 7.3);
          let f = 1 + b.amp * ((n1 - 0.5) * 1.5 + (n2 - 0.5) * 0.55 + (n3 - 0.5) * (0.12 + 0.3 * b.soft));
          for (const L of b.lobes) {
            const da = Math.abs(mod(a - L.a + Math.PI, TAU) - Math.PI) / L.w;
            if (da < 1) f += 0.14 * b.soft * L.amp * late * (1 - da * da) * (0.35 + CH.noise(b.seed + a * 9 / TAU * 6, 3.3) * 1.1);
          }
          b.rr[i] = b.R * f;
        }
        return;
      }
      const P = b.P, n = P.length, end = P[n - 1].s;
      if (b.pen) {
        // a pen line: as wide as the pressure (and the slowness) lays it, thin where the nib lands and lifts
        for (let i = 0; i < n; i++) {
          const A = P[Math.max(0, i - 1)], B = P[Math.min(n - 1, i + 1)], dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy) || 1;
          b.nx[i] = -dy / L; b.ny[i] = dx / L;
          const s = P[i].s, taper = Math.min(1, 0.25 + 0.75 * smooth(clamp(s / 10)), 0.2 + 0.8 * smooth(clamp((end - s) / 10)));
          const hw = 0.5 * (1.2 + 1.5 * P[i].p) * taper * (b.still ? 1 : 1 - Math.exp(-(clock - P[i].t) / 0.05));
          b.rl[i] = b.rr[i] = Math.max(0.25, hw);
        }
        return;
      }
      // a wash: the brush lands thin and lifts thin, spreads sideways from each point as it is laid, and pools where it slowed
      const tl = 1.6 * b.w;
      for (let i = 0; i < n; i++) {
        const A = P[Math.max(0, i - 1)], B = P[Math.min(n - 1, i + 1)], dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy) || 1;
        b.nx[i] = -dy / L; b.ny[i] = dx / L;
        const s = P[i].s, taper = Math.min(0.12 + 0.88 * smooth(clamp(s / tl)), 0.1 + 0.9 * smooth(clamp((end - s) / tl)));
        const pool = 0.7 + 0.6 * P[i].p;
        const r = taper * pool * (b.still ? b.w : b.w * (1 - Math.exp(-(clock - P[i].t) / b.tau)));
        const f = (side) => 1 + b.amp * ((CH.noise(b.seed + s * 0.03, side) - 0.5) * 1.8 + (CH.noise(b.seed + s * 0.11, side + 3) - 0.5) * (0.35 + 0.9 * b.soft));
        b.rl[i] = Math.max(0.4, r * f(1.3)); b.rr[i] = Math.max(0.4, r * f(6.7));
      }
    }
    function shape(b, mul) {
      const e = b.pts; let m = 0;
      if (b.kind === "drop") {
        for (let i = 0; i < EN; i++) { const a = (i / EN) * TAU; e[m++] = b.x + Math.cos(a) * b.rr[i] * mul; e[m++] = b.y + Math.sin(a) * b.rr[i] * mul; }
        b.n = EN; return;
      }
      const P = b.P, n = P.length;
      for (let i = 0; i < n; i++) { e[m++] = P[i].x + b.nx[i] * b.rl[i] * mul; e[m++] = P[i].y + b.ny[i] * b.rl[i] * mul; }
      // the ends come to a point (a brush lifts, it leaves no round cap)
      const tipOf = (i, dir) => { const q = P[i]; const tx = b.ny[i] * dir, ty = -b.nx[i] * dir, rr = (b.rl[i] + b.rr[i]) * 0.5 * mul; e[m++] = q.x + tx * rr * 0.9; e[m++] = q.y + ty * rr * 0.9; };
      tipOf(n - 1, 1);
      for (let i = n - 1; i >= 0; i--) { e[m++] = P[i].x - b.nx[i] * b.rr[i] * mul; e[m++] = P[i].y - b.ny[i] * b.rr[i] * mul; }
      tipOf(0, -1);
      b.n = m / 2;
    }
    function trace(g, b) {   // a smooth closed curve through the outline's points
      const e = b.pts, N = b.n;
      const px = (i) => e[(i % N) * 2], py = (i) => e[(i % N) * 2 + 1];
      g.beginPath();
      g.moveTo((px(0) + px(1)) / 2, (py(0) + py(1)) / 2);
      for (let i = 1; i <= N; i++) g.quadraticCurveTo(px(i), py(i), (px(i) + px(i + 1)) / 2, (py(i) + py(i + 1)) / 2);
      g.closePath();
    }
    // the tide line is broken: each stretch of the outline holds one of four strengths, in runs; the faintest is gone
    const runOf = (b, i) => Math.max(0, Math.min(3, Math.floor((CH.noise(b.seed + i * 0.23, 7.1) - 0.28) * 7)));
    function traceRun(g, b, q) {
      const e = b.pts, N = b.n, mx = (i) => (e[(i % N) * 2] + e[((i + 1) % N) * 2]) / 2, my = (i) => (e[(i % N) * 2 + 1] + e[((i + 1) % N) * 2 + 1]) / 2;
      g.beginPath();
      for (let i = 0; i < N; i++) if (runOf(b, i) === q) { g.moveTo(mx(i + N - 1), my(i + N - 1)); g.quadraticCurveTo(e[i * 2], e[i * 2 + 1], mx(i), my(i)); }
    }
    const rgba = (c, a) => `rgba(${rgbStr(c)},${a.toFixed(3)})`;
    // a mark's extent from its middle (drops) and its fill: radial for a drop (pale in the middle), along the stroke for a wash
    function radius(b) { let m = 0; for (let i = 0; i < EN; i++) m = Math.max(m, b.rr[i]); return m; }
    function bodyFill(g, b, stops, which) {
      let gr;
      if (b.kind === "drop") { const Rm = radius(b) * 1.02; gr = g.createRadialGradient(b.x, b.y, 0, b.x, b.y, Math.max(1, Rm)); }
      else { const A = b.P[0], B = b.P[b.P.length - 1]; gr = g.createLinearGradient(A.x, A.y, B.x + 0.01, B.y); }
      stops.forEach(([o, a, k]) => gr.addColorStop(o, rgba((k === 2 ? b.k2 : b.k1)[which], a)));
      return gr;
    }
    function bbox(b) { const e = b.pts; let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (let i = 0; i < b.n; i++) { const x = e[i * 2], y = e[i * 2 + 1]; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } return [x0 - 2, y0 - 2, x1 - x0 + 4, y1 - y0 + 4]; }

    // The wet wash of a mark, on the soft sheet: a faint bleed just past the edge; inside, the body pale in the middle and
    // denser toward the edge (pigment carried outward as the water spreads); the second ink charged in from one side; a
    // band of denser pigment hugging the outline; the pale fans the backruns leave.
    function wetWash(g, b, a) {
      shape(b, 1.08); trace(g, b); g.globalAlpha = 0.10 * a * b.soft; g.fillStyle = rgba(b.k1.body, 1); g.fill();
      shape(b, 1);
      const bx = bbox(b), sz = b.kind === "drop" ? radius(b) : b.w;
      g.save(); trace(g, b); g.clip();
      g.globalAlpha = a;
      g.fillStyle = bodyFill(g, b, b.kind === "drop" ? [[0, 0.20, 1], [0.55, 0.25, 1], [0.85, 0.34, 1], [1, 0.44, 1]] : [[0, 0.36, 1], [0.7, 0.30, 1], [1, 0.24, 2]], "body");
      g.fillRect(bx[0], bx[1], bx[2], bx[3]);
      if (b.kind === "drop" && b.k2 !== b.k1) {
        const ch = b.charge, Rm = radius(b), cxp = b.x + Math.cos(ch.a) * Rm * ch.d, cyp = b.y + Math.sin(ch.a) * Rm * ch.d;
        const gr = g.createRadialGradient(cxp, cyp, 0, cxp, cyp, Rm * ch.r);
        gr.addColorStop(0, rgba(b.k2.body, 0.42)); gr.addColorStop(0.6, rgba(b.k2.body, 0.22)); gr.addColorStop(1, rgba(b.k2.body, 0));
        g.fillStyle = gr; g.fillRect(bx[0], bx[1], bx[2], bx[3]);
      }
      // the pigment the spreading water carries outward: a soft denser band inside the edge (the sheet is blurred after)
      g.lineJoin = "round"; g.lineWidth = Math.max(2, sz * 0.14); g.strokeStyle = rgba(b.k1.rim, 0.30); trace(g, b); g.stroke();
      // backruns: inside each finger, a pale fan where the creeping water pushed the pigment out to its fringe
      if (b.kind === "drop" && b.lobes.length) {
        g.globalCompositeOperation = "destination-out";
        const Rm = radius(b);
        for (const L of b.lobes) {
          const px = b.x + Math.cos(L.a) * Rm * 0.72, py = b.y + Math.sin(L.a) * Rm * 0.72, gr = g.createRadialGradient(px, py, 0, px, py, Rm * 0.36);
          gr.addColorStop(0, `rgba(0,0,0,${(0.55 * b.soft * L.amp).toFixed(3)})`); gr.addColorStop(1, "rgba(0,0,0,0)");
          g.fillStyle = gr; g.fillRect(px - Rm * 0.4, py - Rm * 0.4, Rm * 0.8, Rm * 0.8);
        }
        g.globalCompositeOperation = "source-over";
      }
      g.restore();
    }
    // a backrun (a bloom): where water crept back into the drying pigment it pushed the pigment out of a pale pool and left
    // it in a frilled, cauliflower edge round that pool; the pool sits in the finger, and the mark's own edge clips it
    function bloomPool(b, L, Rm) { return { x: b.x + Math.cos(L.a) * Rm * 0.74, y: b.y + Math.sin(L.a) * Rm * 0.74, r: Rm * (0.22 + 0.08 * L.amp) }; }
    function backrunEdge(g, b, L, P) {
      const n = 48;
      g.beginPath();
      for (let i = 0; i < n; i++) {
        const th = (i / n) * TAU, c = Math.cos(th), sn = Math.sin(th);
        const f = 1 + 0.26 * (CH.noise(b.seed + c * 1.4 + 31, sn * 1.4 + L.a * 3) - 0.5) + 0.2 * (CH.noise(b.seed + c * 7.5 + 61, sn * 7.5 + L.a) - 0.5);
        const x = P.x + c * P.r * f, y = P.y + sn * P.r * f;
        if (i) g.lineTo(x, y); else g.moveTo(x, y);
      }
      g.closePath();
    }
    // The dried stain, crisp: the settled body (lighter than when wet, as watercolour dries), a thin dense band at the edge,
    // and once it is mostly dry the broken, darker tide line where the last water left its pigment.
    function dryStain(g, b, a) {
      shape(b, 1);
      const bx = bbox(b), sz = b.kind === "drop" ? radius(b) : b.w, Rm = b.kind === "drop" ? radius(b) : 0;
      g.save(); trace(g, b); g.clip();
      g.globalAlpha = a;
      g.fillStyle = bodyFill(g, b, b.kind === "drop" ? [[0, 0.12, 1], [0.6, 0.16, 1], [0.9, 0.23, 1], [1, 0.30, 1]] : [[0, 0.25, 1], [0.7, 0.21, 1], [1, 0.16, 2]], "body");
      g.fillRect(bx[0], bx[1], bx[2], bx[3]);
      if (b.kind === "drop" && b.k2 !== b.k1) {
        const ch = b.charge, cxp = b.x + Math.cos(ch.a) * Rm * ch.d, cyp = b.y + Math.sin(ch.a) * Rm * ch.d;
        const gr = g.createRadialGradient(cxp, cyp, 0, cxp, cyp, Rm * ch.r);
        gr.addColorStop(0, rgba(b.k2.body, 0.26)); gr.addColorStop(1, rgba(b.k2.body, 0));
        g.fillStyle = gr; g.fillRect(bx[0], bx[1], bx[2], bx[3]);
      }
      // edge darkening: the pigment gathered where the water's edge dried, a faint band and a thin dense line just inside
      g.lineJoin = "round";
      g.lineWidth = Math.max(3, sz * 0.12); g.strokeStyle = rgba(b.k1.rim, 0.14); trace(g, b); g.stroke();
      g.lineWidth = 2.4; g.strokeStyle = rgba(b.k1.rim, 0.42); trace(g, b); g.stroke();
      // the backruns' pale fans and their ragged edges, once the stain has mostly dried
      const t = smooth(clamp((b.dry - 0.6) / 0.4));
      if (b.kind === "drop" && b.lobes.length && t > 0.01) {
        for (const L of b.lobes) {
          const P = bloomPool(b, L, Rm), k = b.soft * L.amp * t, gr = g.createRadialGradient(P.x, P.y, 0, P.x, P.y, P.r * 1.1);
          gr.addColorStop(0, `rgba(0,0,0,${(0.55 * k).toFixed(3)})`); gr.addColorStop(0.75, `rgba(0,0,0,${(0.4 * k).toFixed(3)})`); gr.addColorStop(1, "rgba(0,0,0,0)");
          g.globalCompositeOperation = "destination-out"; g.fillStyle = gr; g.fillRect(P.x - P.r * 1.2, P.y - P.r * 1.2, P.r * 2.4, P.r * 2.4);
          g.globalCompositeOperation = "source-over";
          backrunEdge(g, b, L, P); g.lineWidth = 1.1; g.strokeStyle = rgba(b.k1.rim, 0.42 * k); g.stroke();
        }
      }
      g.restore();
      // the tide line, broken, darker, where the last water left its pigment
      if (t > 0.01) {
        g.lineCap = "round"; g.strokeStyle = rgba(b.k1.tide, 1);
        for (let q = 1; q < 4; q++) { traceRun(g, b, q); g.lineWidth = [0, 0.8, 1.1, 1.5][q]; g.globalAlpha = a * t * [0, 0.45, 0.7, 0.92][q]; g.stroke(); }
      }
    }
    // A pen mark on a dry page: a solid dot with a one-pixel darker rim, or one solid tapered line; nothing spreads.
    function penMark(g, b, a) {
      shape(b, 1); trace(g, b);
      g.globalAlpha = a;
      if (b.kind === "drop") { g.fillStyle = rgba(b.k1.body, 0.9); g.fill(); g.lineWidth = 1; g.strokeStyle = rgba(b.k1.tide, 0.95); g.stroke(); }
      else { g.fillStyle = bodyFill(g, b, [[0, 0.92, 1], [1, 0.92, 2]], "body"); g.fill(); }
    }
    // Advance every mark (spread, dry, fade; the ripple re-wets those it reaches), then draw them: wet washes on the soft
    // sheet (painted small, blurred once, laid on), dried stains and pen marks crisp on the visible canvas.
    let sheetAt = null;   // the part of the soft sheet the last wet washes covered (sheet pixels), cleared next time
    function draw(o) {
      const { g, sg, sc, sc2, W, H, k, clock, dtc, rp, page } = o;
      g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = "source-over"; g.globalAlpha = 1; g.clearRect(0, 0, g.canvas.width, g.canvas.height);
      if (!marks.length) return false;
      for (let i = marks.length - 1; i >= 0; i--) {
        const b = marks[i];
        if (rp && !rp.hit.has(b) && Math.hypot(b.x - rp.x, b.y - rp.y) < rp.R) {
          rp.hit.add(b);
          // a mark takes water from two ripples at most: re-wetted by every outcome of a long life, it would spread over the
          // whole sky and never dry
          if ((b.wets = (b.wets || 0) + 1) <= 2) {
            if (b.kind === "drop") b.Rmax *= b.pen ? 1.3 : 1.16; else if (!b.pen) b.w *= 1.16;
            b.dryFrom = clock; b.soft = Math.max(b.soft, b.pen ? b.soft : 0.65); b.amp = Math.min(0.42, b.amp * 1.25);
            b.dryIn = Math.max(b.dryIn, b.pen ? 0.6 : 3.2); b.hold = Math.max(b.hold, clock - b.born + b.dryIn + 6); b.tau = Math.max(b.tau, b.pen ? b.tau : 0.9);
          }
        }
        if (b.still) { if (b.kind === "drop") b.R = b.Rmax; b.dry = 1; b.fade = 1; }
        else {
          // a drop spreads quickly at first and then ever more slowly (each moment covers a share of what is left)
          if (b.kind === "drop") b.R += (b.Rmax - b.R) * (1 - Math.exp(-dtc / b.tau));
          b.dry = b.pen ? 1 : smooth(clamp((clock - b.dryFrom - b.tau * 0.7) / b.dryIn));
          b.fade = 1 - smooth(clamp((clock - b.born - b.hold) / b.fadeT));
          if (b.fade <= 0.002) { marks.splice(i, 1); continue; }
        }
        measure(b, clock);
      }
      // 1. the wet washes on the soft sheet (only the part of it they cover is cleared, settled, blurred and laid on)
      let wetN = 0, wx0 = 1e9, wy0 = 1e9, wx1 = -1e9, wy1 = -1e9;
      const ss = sc.width / W, prev = sheetAt;
      sg.setTransform(1, 0, 0, 1, 0, 0); sg.globalCompositeOperation = "source-over"; sg.globalAlpha = 1;
      if (prev) sg.clearRect(prev[0], prev[1], prev[2], prev[3]); else sg.clearRect(0, 0, sc.width, sc.height);
      sg.setTransform(ss, 0, 0, ss, 0, 0);
      for (const b of marks) {
        if (b.pen) continue; const a = (1 - b.dry) * b.fade;
        if (a > 0.01) { wetWash(sg, b, a); wetN++; const q = bbox(b), m = 0.12 * Math.max(q[2], q[3]); wx0 = Math.min(wx0, q[0] - m); wy0 = Math.min(wy0, q[1] - m); wx1 = Math.max(wx1, q[0] + q[2] + m); wy1 = Math.max(wy1, q[1] + q[3] + m); }
      }
      g.setTransform(k, 0, 0, k, 0, 0);
      sheetAt = null;
      if (wetN) {
        // the region, in sheet pixels, with room for the blur
        const bl = 0.6 + 1.6 * page, pad = Math.ceil(bl * 3) + 2;
        const rx = Math.max(0, Math.floor(wx0 * ss) - pad), ry = Math.max(0, Math.floor(wy0 * ss) - pad);
        const rw = Math.min(sc.width, Math.ceil(wx1 * ss) + pad) - rx, rh = Math.min(sc.height, Math.ceil(wy1 * ss) + pad) - ry;
        if (rw > 0 && rh > 0) {
          sheetAt = [rx, ry, rw, rh];
          // the pigment settles unevenly: one pass of a soft seeded tile thins it here and there
          sg.setTransform(1, 0, 0, 1, 0, 0); sg.globalCompositeOperation = "destination-out"; sg.globalAlpha = 0.42;
          sg.fillStyle = patOf(sg, mottleTile()); sg.fillRect(rx, ry, rw, rh);
          sg.globalCompositeOperation = "source-over"; sg.globalAlpha = 1;
          // the wet edge feathers: the small sheet is blurred once (more on a wetter page), then laid on at full size
          let src = sc;
          if (CANFILTER && sc2) {
            const x2 = sc2.getContext("2d"); x2.setTransform(1, 0, 0, 1, 0, 0); x2.globalCompositeOperation = "source-over"; x2.globalAlpha = 1;
            x2.clearRect(rx, ry, rw, rh); x2.filter = `blur(${bl.toFixed(2)}px)`; x2.drawImage(sc, rx, ry, rw, rh, rx, ry, rw, rh); x2.filter = "none"; src = sc2;
          }
          g.imageSmoothingEnabled = true; g.drawImage(src, rx, ry, rw, rh, rx / ss, ry / ss, rw / ss, rh / ss);
        }
      }
      // 2. dried stains, crisp, and their grain
      let stainN = 0, ux0 = 1e9, uy0 = 1e9, ux1 = -1e9, uy1 = -1e9;
      for (const b of marks) {
        if (b.pen) continue; const a = b.dry * b.fade;
        if (a > 0.01) { dryStain(g, b, a); stainN++; const q = bbox(b); ux0 = Math.min(ux0, q[0]); uy0 = Math.min(uy0, q[1]); ux1 = Math.max(ux1, q[0] + q[2]); uy1 = Math.max(uy1, q[1] + q[3]); }
      }
      if (stainN) {
        // over the stains only: the pigment's uneven settling, then its grain
        const r = [Math.max(0, ux0 - 4), Math.max(0, uy0 - 4), Math.min(W, ux1 + 4), Math.min(H, uy1 + 4)];
        g.save(); g.globalCompositeOperation = "destination-out"; g.globalAlpha = 0.24; g.fillStyle = patOf(g, mottleTile()); g.fillRect(r[0], r[1], r[2] - r[0], r[3] - r[1]);
        g.globalAlpha = 0.2; g.fillStyle = patOf(g, grainTile()); g.fillRect(r[0], r[1], r[2] - r[0], r[3] - r[1]); g.restore();
      }
      // 3. pen marks
      for (const b of marks) if (b.pen && b.fade > 0.01) penMark(g, b, b.fade);
      g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
      return true;
    }
    // does any mark still change quickly (spreading, being drawn)? Otherwise drying and fading are slow enough to redraw
    // a few times a second
    const busy = (clock) => marks.some((b) => !b.still && clock - b.last < b.tau * 2.5 + 0.4);
    return { marks, drop, stroke, strokeTo, draw, reach, busy, PEN };
  }

  /* ---------- B1: ink laid on a parchment panel (CH.ink.bloom(x, y, colours, {on: el})) ---------- */
  // An overlay canvas over the element, fixed to the window and following it while it has ink, pointer-transparent, in the
  // engraving inks, multiplied into the parchment (pigment on paper, never light). It goes away when its ink has faded.
  const overlays = new Map();
  function parchOverlay(el) {
    let o = overlays.get(el);
    if (o) return o;
    const c = document.createElement("canvas"); c.className = "chs-ink-over"; c.setAttribute("aria-hidden", "true");
    const sc = document.createElement("canvas"), sc2 = document.createElement("canvas");
    document.body.appendChild(c);
    o = { el, c, g: c.getContext("2d"), sc, sg: sc.getContext("2d"), sc2, ink: makeInk("parch", 9001 + overlays.size), clock: 0, off: null, W: 1, H: 1, k: 1 };
    const place = () => {
      const r = el.getBoundingClientRect(), lw = el.offsetWidth || r.width, lh = el.offsetHeight || r.height, vs = lw ? r.width / lw : 1;
      const k = Math.min(2, window.devicePixelRatio || 1) * vs, w = Math.max(1, Math.round(lw * k)), h = Math.max(1, Math.round(lh * k));
      if (c.width !== w || c.height !== h) { c.width = w; c.height = h; }
      const sw = Math.max(2, Math.round(lw / 3)), sh = Math.max(2, Math.round(lh / 3));
      if (sc.width !== sw || sc.height !== sh) { sc.width = sc2.width = sw; sc.height = sc2.height = sh; }
      const br = getComputedStyle(el).borderRadius;
      c.style.cssText = `left:${r.left}px;top:${r.top}px;width:${r.width}px;height:${r.height}px;border-radius:${br === "0px" ? "0" : `calc(${br} * ${vs.toFixed(4)})`}`;
      o.W = lw; o.H = lh; o.k = k; o.vs = vs; o.r = r;
    };
    o.place = place; place();
    o.off = CH.frame((now, dt) => {
      if (!el.isConnected) { o.ink.marks.length = 0; }
      const sp = CH.speed(); o.clock += dt * (sp || 1);
      if (o.ink.marks.length) place();
      const any = o.ink.draw({ g: o.g, sg: o.sg, sc, sc2, W: o.W, H: o.H, k: o.k, clock: o.clock, dtc: sp ? dt * sp : 0, rp: null, page: CH.ink.wet() });
      if (!any) { o.off(); c.remove(); overlays.delete(el); }
    });
    overlays.set(el, o);
    return o;
  }

  CH.ink = {
    // how wet the ink is now (eased), 0 dry .. 1 soaking
    wet: () => {
      if (primary) return primary.wetNow();
      const v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--wet")); return isFinite(v) ? v : 0.5;
    },
    // how wet the ink is at a state (the age, the readiness, an open window): the formula every module can share
    wetOf,
    // drop a bloom at a point on the screen (client pixels), in the given inks (letters "W".."G" or hex colours); without
    // colours, the person's two leading inks. With {on: el}, the ink is laid on that panel (parchment) instead of the sky.
    bloom: (x, y, colours, opt) => {
      if (opt && opt.on) {
        const o = parchOverlay(opt.on); o.place();
        const cols = colours && colours.length ? colours : primary ? primary.inks() : ["W", "U"];
        const wet = CH.ink.wet(), still = CH.speed() === 0;
        o.ink.drop((x - o.r.left) / o.vs, (y - o.r.top) / o.vs, cols, wet, o.clock, still, inkScale(o.W, o.H));
        return;
      }
      if (primary) primary.bloomClient(x, y, colours);
    },
    filter: "url(#chs-ink)",
  };
  // the parchment overlays go with the sky (living/90-game.js takes the sky down when the Living HUD is turned off)
  function dropOverlays() { overlays.forEach((o) => { o.ink.marks.length = 0; o.off(); o.c.remove(); }); overlays.clear(); }

  /* ---------- the layout of the open sky: where the panels leave it visible ---------- */
  // opts.clear: an array of {x, y, w, h} (host CSS px, the gaps where the sky shows), a function returning one, or a CSS
  // selector of the panels that cover it (read from the page on resize and now and then). Without it, all the sky is open.
  function freeRects(W, H, covers) {
    const xs = [0, W], ys = [0, H];
    covers.forEach((c) => { xs.push(clamp(c.x, 0, W), clamp(c.x + c.w, 0, W)); ys.push(clamp(c.y, 0, H), clamp(c.y + c.h, 0, H)); });
    const ux = [...new Set(xs.map((v) => Math.round(v)))].sort((a, b) => a - b), uy = [...new Set(ys.map((v) => Math.round(v)))].sort((a, b) => a - b);
    const cov = (x, y) => covers.some((c) => x > c.x && x < c.x + c.w && y > c.y && y < c.y + c.h);
    // free runs in each row band, then runs with the same span joined down the bands
    let open = [];
    for (let j = 0; j + 1 < uy.length; j++) {
      const y0 = uy[j], y1 = uy[j + 1]; if (y1 - y0 < 1) continue;
      let run = null; const runs = [];
      for (let i = 0; i + 1 < ux.length; i++) {
        const x0 = ux[i], x1 = ux[i + 1]; if (x1 - x0 < 1) continue;
        if (!cov((x0 + x1) / 2, (y0 + y1) / 2)) { if (run && run.x + run.w === x0) run.w = x1 - run.x; else runs.push((run = { x: x0, y: y0, w: x1 - x0, h: y1 - y0 })); } else run = null;
      }
      runs.forEach((r) => { const up = open.find((o) => o.x === r.x && o.w === r.w && o.y + o.h === r.y); if (up) up.h += r.h; else open.push(r); });
    }
    return open.filter((r) => r.w >= 8 && r.h >= 8);
  }

  /* ---------- mount: one sky in a host ---------- */
  const FS_GL = 1 / 3, FS_2D = 0.25;
  // the sparks' pixel ratio at most: one and a half device pixels a CSS pixel keeps the hairlines (the lattice, the star
  // chart, the constellations) sharp on a sharp screen at a little over half the pixels of a full ratio of 2
  const SPARK_DPR = 1.5;
  function mount(host, opts) {
    opts = opts || {};
    const motionOf = () => CH.motion();
    host.classList.add("chs-atmos");
    const stage = opts.stage || document;             // where the panels named by opts.clear are found
    // the open sky under the pointer: the page itself, #app and main between the panels, or the sky's own layers
    const isSky = opts.isSky || ((t) => t === stage || host.contains(t));

    // the layers: the field, the sparks and the ink. The sparks and the ink are sized here (fitLayer, from measure), not by
    // CH.canvas: the sparks at no more than SPARK_DPR device pixels a CSS pixel (soft sprites and faint hairlines), and the
    // ink canvas and its two small sheets only while there is ink. Until the first drop, and again once the last mark has
    // faded, they hold a single pixel each, so a sky nobody inks costs no memory for it.
    let fieldC = document.createElement("canvas"); fieldC.className = "chs-atmos-field"; host.appendChild(fieldC);
    const layer = (cls) => { const c = document.createElement("canvas"); c.className = cls; c.width = c.height = 1; c._k = 1; host.appendChild(c); return c; };
    const sparks = layer("chs-atmos-sparks"), sx = sparks.getContext("2d");
    const crisp = layer("chs-atmos-ink"), cx = crisp.getContext("2d");
    crisp.style.visibility = "hidden";
    const softC = document.createElement("canvas"), softC2 = document.createElement("canvas"), softX = softC.getContext("2d");
    softC.width = softC.height = softC2.width = softC2.height = 1;
    let inkLive = false;                              // the ink canvas and its sheets hold their full size
    let G = makeGL(fieldC);
    // a canvas that gave a WebGL context (refused shaders) gives no 2D one: the painting takes a fresh canvas in its place
    if (!G) { const c = document.createElement("canvas"); c.className = fieldC.className; fieldC.replaceWith(c); fieldC = c; }
    let f2 = G ? null : fieldC.getContext("2d");
    host.dataset.renderer = G ? "webgl" : "canvas";
    if (G) {
      fieldC.addEventListener("webglcontextlost", (e) => { e.preventDefault(); G = null; gt = null; }, false);
      fieldC.addEventListener("webglcontextrestored", () => { G = makeGL(fieldC); gt = null; dirty = true; force = true; }, false);
    }

    // the eased numbers (X), their speeds (V) and targets (T); the sky's own clock and the motions it has accumulated
    const X = new Float32Array(K.N), V = new Float32Array(K.N), T = new Float32Array(K.N);
    let eraN = 0, first = true, dirty = true, force = true, lastS = null, lastWin = false, inks = ["W", "U"];
    let clock = 0, drift = 0, swirl = 0, inflow = 0, aur = 0, caus = 0, nowS = 0;
    let rip = null, lastRip = -99;                    // the re-wetting ripple: {t0, x, y, hit}
    const STILL = { clock: 47.3, drift: 0, swirl: 0.6, inflow: 0.37, aur: 2.8, caus: 1.9 };   // the one still frame (motion off)

    // size: CSS pixels of the layout, the sparks' pixel ratio (device ratio x any CSS scale above), the size unit (1 at
    // 1440x900), the open sky (gaps and the widest one, the focus) and the catalogues built for them
    let W = 1, H = 1, kk = 1, su = 1, inkS = 1, built = "";
    let lay = { gaps: [{ x: 0, y: 0, w: 1, h: 1 }], focus: { x: 0, y: 0, w: 1, h: 1 }, full: true, sig: "" };
    let stars = [], dust = null, lattice = null, consts = [], embers = [], rising = [], motes = [], flies = [], brush = null;
    function readLayout() {
      const c = opts.clear;
      let rects = null;
      try {
        if (typeof c === "function") rects = c(host);
        else if (Array.isArray(c)) rects = c;
        else if (typeof c === "string") {
          const hr = host.getBoundingClientRect(), vs = host.offsetWidth ? hr.width / host.offsetWidth : 1;
          // a panel hidden by visibility or faded out (the end screen hides the play panels that way) covers nothing
          const shown = (e) => (e.checkVisibility ? e.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }) : getComputedStyle(e).visibility !== "hidden");
          const covers = [...(stage.querySelectorAll ? stage.querySelectorAll(c) : [])].filter(shown).map((e) => e.getBoundingClientRect()).filter((r) => r.width > 2 && r.height > 2)
            .map((r) => ({ x: (r.left - hr.left) / vs, y: (r.top - hr.top) / vs, w: r.width / vs, h: r.height / vs }));
          rects = freeRects(W, H, covers);
        }
      } catch (e) { console.warn("living: sky's open stretches unread, the whole sky stands in", e); rects = null; }
      rects = (rects || []).filter((r) => r && r.w >= 8 && r.h >= 8);
      // A stretch of open sky is worth gathering the figures in (Black's eye, White's window, Red's brushstroke, Blue's
      // figures) only if it can hold one. When the panels leave nothing but thin margins between them, the figures keep
      // the whole sky's proportions behind the panels instead (the gaps and the glass are windows onto one sky); crowded
      // into a sliver they would show nowhere.
      const holds = (r) => r.h >= Math.max(90, 0.16 * H) && r.w >= Math.max(140, 0.22 * W);
      const full = !rects.length || !rects.some(holds);
      if (full) rects = [{ x: 0, y: 0, w: W, h: H }];
      const focus = rects.reduce((a, r) => (r.w * Math.min(r.h, 0.6 * r.w) > a.w * Math.min(a.h, 0.6 * a.w) ? r : a), rects[0]);
      const sig = full ? "whole" : rects.map((r) => [r.x, r.y, r.w, r.h].map(Math.round).join(",")).join(";");
      return { gaps: rects, focus, full, sig };
    }
    function relayout() {
      const L = readLayout();
      const changed = L.sig !== lay.sig;
      lay = L;
      const f = lay.focus;
      T[K.FOC] = (f.x + f.w / 2) / H; T[K.FOC + 1] = 1 - (f.y + f.h / 2) / H; T[K.FOC + 2] = f.w / 2 / H; T[K.FOC + 3] = f.h / 2 / H;
      if (first || CH.speed() === 0) for (let i = 0; i < 4; i++) { X[K.FOC + i] = T[K.FOC + i]; V[K.FOC + i] = 0; }
      return changed;
    }
    // a layer's size: the host's CSS size times the device's pixel ratio (at most cap) and any CSS scale above the sky
    // (none on the game page, where the sky is fixed to the window); one pixel while it is not in use
    function fitLayer(c, cap, on) {
      const r = host.getBoundingClientRect(), vs = W > 1 && r.width ? r.width / W : 1, k = Math.min(cap, window.devicePixelRatio || 1) * vs;
      const w = on ? Math.max(1, Math.round(W * k)) : 1, h = on ? Math.max(1, Math.round(H * k)) : 1;
      if (c.width !== w || c.height !== h) { c.width = w; c.height = h; }
      c._k = k;
    }
    function inkSize(on) {
      inkLive = on;
      fitLayer(crisp, 2, on);
      const sw = on ? Math.max(2, Math.round(W / 3)) : 1, sh = on ? Math.max(2, Math.round(H / 3)) : 1;
      if (softC.width !== sw || softC.height !== sh) { softC.width = softC2.width = sw; softC.height = softC2.height = sh; }
      inkForce = true;
    }
    function measure() {
      const w = host.offsetWidth, h = host.offsetHeight;
      if (!w || !h) return;                            // hidden: keep the last size
      W = w; H = h;
      fitLayer(sparks, SPARK_DPR, true); inkSize(inkLive);
      kk = sparks._k;
      su = clamp(Math.min(W, H) / 900, 0.42, 1.3);
      inkS = inkScale(W, H);
      const fs = G ? FS_GL : FS_2D;                    // the field renders at a third of the CSS size (a quarter in the Canvas2D painting)
      const fw = Math.max(2, Math.round(W * fs)), fh = Math.max(2, Math.round(H * fs));
      if (fieldC.width !== fw || fieldC.height !== fh) { fieldC.width = fw; fieldC.height = fh; gt = null; }
      relayout();
      const key = `${Math.round(W)}x${Math.round(H)}@${kk.toFixed(3)}|${lay.sig}`;
      if (key !== built) { built = key; build(); tx = {}; seen = {}; }
      dirty = true; force = true; inkForce = true;
    }

    /* the catalogues: every star, node and mote has its place from a seeded stream, so the same sky draws the same way.
       pick() puts a thing in the open sky: in a gap chosen by its area (among gaps at least so big), at a point inside it */
    function pickGap(r, minW, minH) {
      const ok = lay.gaps.filter((g) => g.w >= minW && g.h >= minH);
      const list = ok.length ? ok : [lay.focus];
      const tot = list.reduce((s, g) => s + g.w * g.h, 0); let u = r * tot;
      for (const g of list) { u -= g.w * g.h; if (u <= 0) return g; }
      return list[list.length - 1];
    }
    function build() {
      const r = CH.rng(20261017);
      // bright stars, drawn one by one (they twinkle and drift at their own depth); fainter dust is baked into one sheet
      const nB = Math.round(clamp((W * H) / 7200, 45, 220));
      stars = [];
      for (let i = 0; i < nB; i++) {
        const m = 0.25 + 0.75 * Math.pow(r(), 2.2);
        const cr = r(), c = cr < 0.13 ? 1 + Math.floor(r() * 5) : cr < 0.6 ? 0 : 6;
        stars.push({ x: r(), y: r(), m, z: 0.45 + 0.55 * r(), f: 0.5 + 2.4 * r(), p: r() * TAU, c, wt: r() });
      }
      stars.sort((a, b) => a.c - b.c);
      // the dust: a sheet of faint stars as wide as the sky, stamped twice side by side as the wind carries it
      const nD = Math.round(clamp((W * H) / 1100, 120, 1500));
      dust = document.createElement("canvas"); dust.width = Math.max(1, Math.round(W * kk)); dust.height = Math.max(1, Math.round(H * kk));
      const g = dust.getContext("2d");
      for (let i = 0; i < nD; i++) {
        const x = r() * dust.width, y = r() * dust.height, a = 0.10 + 0.45 * Math.pow(r(), 1.6), rr = (0.28 + 0.42 * r()) * kk, cr = r();
        g.fillStyle = `rgba(${cr < 0.1 ? TINT[1 + Math.floor(r() * 5)] : cr < 0.55 ? TINT[0] : TINT[6]},${a.toFixed(3)})`;
        g.beginPath(); g.arc(x, y, rr, 0, TAU); g.fill();
      }
      // White's lattice: three rings of a rose window rising from below the open sky's floor (3, 5 and 7 nodes); the
      // nodes light from the inner ring out, centre first, so a partly grown lattice is still symmetric
      const F = lay.focus, u = Math.min(F.h, F.w * 0.78);
      lattice = { ax: F.x + F.w / 2, ay: F.y + F.h + 0.10 * u, u, rings: [0.36, 0.55, 0.76], nodes: [] };
      [3, 5, 7].forEach((n, ri) => {
        const order = [...Array(n).keys()].sort((a, b) => Math.abs(a - (n - 1) / 2) - Math.abs(b - (n - 1) / 2) || a - b);
        order.forEach((j) => {
          const ang = -Math.PI / 2 + (j - (n - 1) / 2) * (ri === 0 ? 0.52 : ri === 1 ? 0.36 : 0.27);
          const off = (0.12 + 0.2 * r()) * u, oa = r() * TAU;
          lattice.nodes.push({ ring: ri, j, ang, hx: Math.cos(oa) * off, hy: Math.sin(oa) * off * 0.7, p: r() * TAU });
        });
      });
      // Blue's constellations: six small figures, each four to seven stars joined in a chain with one branch, each in an
      // open stretch big enough to hold it, shrunk to fit
      consts = [];
      const sc0 = (0.75 + 0.25 * su) * Math.max(0.7, su);
      for (let j = 0; j < 6; j++) {
        let x = 0, y = 0, a = r() * TAU;
        const pts = [[0, 0]], m = 4 + Math.floor(r() * 4);
        for (let s = 1; s < m; s++) { a += (r() - 0.5) * 1.7; const L = 24 + r() * 38; x += Math.cos(a) * L; y += Math.sin(a) * L * 0.8; pts.push([x, y]); }
        const edges = pts.slice(1).map((_, s) => [s, s + 1]);
        if (m > 4) { const b = 1 + Math.floor(r() * (m - 3)); const ba = a + 1.4 + r(); pts.push([pts[b][0] + Math.cos(ba) * 30, pts[b][1] + Math.sin(ba) * 30]); edges.push([b, pts.length - 1]); }
        const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]), bw = Math.max(...xs) - Math.min(...xs) + 8, bh = Math.max(...ys) - Math.min(...ys) + 8;
        const mx = (Math.max(...xs) + Math.min(...xs)) / 2, my = (Math.max(...ys) + Math.min(...ys)) / 2;
        const gp = pickGap(r(), 120 * su, 70 * su);
        const sc = Math.min(sc0, (0.78 * gp.h) / bh, (0.9 * gp.w) / bw);
        const fx = lay.full ? 0.08 + 0.84 * frac(j * 0.618 + 0.13 + r() * 0.12) : 0.1 + 0.8 * frac(j * 0.618 + 0.13 + r() * 0.12), fy = lay.full ? 0.10 + 0.70 * r() : 0.3 + 0.4 * r();
        const ax = gp.x + gp.w * fx, ay = clamp(gp.y + gp.h * fy, gp.y + (bh * sc) / 2 + 4, gp.y + gp.h - (bh * sc) / 2 - 4);
        consts.push({ ax, ay, gx: gp.x, gw: gp.w, sc, pts: pts.map(([px, py]) => [px - mx, py - my]), edges, m: pts.map(() => 0.55 + 0.45 * r()) });
      }
      // Red's brushstroke across the open sky (its spine here; its picture is painted the first time Red shows, brushPic),
      // the embers it sheds (each at a place along it, a little above its upper edge) and the sparks rising from the
      // hearth; Black's motes; Green's lights: the most each can have, and the colour's strength says how many show
      brush = brushOf(lay.focus, r);
      embers = []; for (let i = 0; i < 18; i++) embers.push({ s: 0.1 + 0.86 * r(), d: 0.3 + 2.2 * Math.pow(r(), 1.4), T: 4 + r() * 5, p: r(), f: 0.5 + r() * 1.3, ph: r() * TAU, m: 0.35 + 0.65 * r(), dx: r() - 0.5 });
      rising = []; for (let i = 0; i < 22; i++) { const gp = pickGap(r(), 40, 40); rising.push({ x: gp.x + gp.w * (0.02 + 0.96 * r()), base: gp.y + gp.h * 1.01, gh: gp.h, gx: gp.x, gw: gp.w, T: 7 + r() * 6, p: r(), w: 0.6 + r() * 1.4, h: 0.22 + 0.3 * r(), s: 0.6 + 0.8 * r() }); }
      motes = []; for (let i = 0; i < 28; i++) motes.push({ a: r() * TAU, T: 26 + r() * 22, p: r(), s: 0.5 + r() * 0.7 });
      flies = []; for (let i = 0; i < 20; i++) { const gp = pickGap(r(), 40, 40); flies.push({ x: gp.x + gp.w * (0.04 + 0.92 * r()), y: gp.y + gp.h * (0.55 + 0.42 * r()), gh: gp.h, f: 0.6 + 0.8 * r(), p: r() * TAU, q: r() }); }
      meteors.length = 0; bits.length = 0;
    }

    /* RED's brushstroke: one great sweep of ember light across the open sky (Red's texture is the brushstroke), laid as a
       brush is laid: it lands blunt and full at the lower left, runs full through its body, and lifts toward the upper
       right, where it thins and its bristles run dry and part into separate strands. Its spine is a gentle S through the
       open stretch (seeded, so the same sky draws it the same way), sampled at even steps along its length; each step
       keeps its place, its direction, the normal toward the sky above the stroke, and the stroke's width there. */
    function brushOf(F0, r) {
      // on a tall sky (a phone held upright) the stroke keeps a landscape box across the width, a little below the middle,
      // so it still sweeps across the sky rather than climbing it
      const F = F0.h > 0.8 * F0.w ? { x: F0.x, y: F0.y + 0.56 * F0.h - 0.4 * F0.w, w: F0.w, h: 0.8 * F0.w } : F0;
      const jit = () => (r() - 0.5) * 0.05;
      const C = [[0.08, 0.80], [0.33, 0.40], [0.58, 0.64], [0.92, 0.20]].map(([a, b]) => [F.x + (a + jit()) * F.w, F.y + (b + jit()) * F.h]);
      const N = 400, raw = [];
      let len = 0;
      for (let i = 0; i <= N; i++) {
        const t = i / N, u = 1 - t, b0 = u * u * u, b1 = 3 * u * u * t, b2 = 3 * u * t * t, b3 = t * t * t;
        const x = b0 * C[0][0] + b1 * C[1][0] + b2 * C[2][0] + b3 * C[3][0], y = b0 * C[0][1] + b1 * C[1][1] + b2 * C[2][1] + b3 * C[3][1];
        if (i) len += Math.hypot(x - raw[i - 1][0], y - raw[i - 1][1]);
        raw.push([x, y, len]);
      }
      const Wm = clamp(0.075 * Math.min(F.w, F.h), 8, 56), M = 200, at = [], wob = r() * 10;
      for (let i = 0, j = 0; i < M; i++) {
        const want = (i / (M - 1)) * len;
        while (j < N - 1 && raw[j + 1][2] < want) j++;
        const a = raw[j], b = raw[j + 1], f = b[2] > a[2] ? clamp((want - a[2]) / (b[2] - a[2])) : 0;
        at.push([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]);
      }
      const pts = at.map((p, i) => {
        const A = at[Math.max(0, i - 1)], B = at[Math.min(M - 1, i + 1)], dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy) || 1, s = i / (M - 1);
        // the width: the brush lands on a slant (the bristles start one after another, below), swells to full through
        // its body as it is pressed, its pressure wavering a little, and thins over the long second half as it lifts
        const press = smooth(clamp(s / 0.24)), lift = Math.pow(1 - smooth(clamp((s - 0.32) / 0.68)), 0.85);
        const w = Wm * Math.min(0.72 + 0.28 * press, lift) * (1 + 0.08 * Math.sin(s * 11 + wob));
        return { x: p[0], y: p[1], tx: dx / L, ty: dy / L, nx: dy / L, ny: -dx / L, s, w };
      });
      // the droplets a reckless brush flings past where it lifts (shown only in Red's shadow)
      const T = pts[M - 1], spat = [];
      for (let i = 0; i < 14; i++) { const d = Wm * (0.4 + 2.6 * r()), sd = (r() - 0.5) * Wm * (0.6 + 0.04 * d); spat.push({ x: T.x + T.tx * d + T.nx * sd, y: T.y + T.ty * d + T.ny * sd, r: 0.8 + 2.2 * r() * r(), m: 0.4 + 0.6 * r() }); }
      return { pts, Wm, len, cyc: 5 + 3 * r(), cp: r(), seed: Math.floor(r() * 1e6), spat, pic: null };
    }
    // The brushstroke's picture, painted once for this layout (the first time Red shows) and laid on each frame as light:
    // a soft warm glow round it, a faint wash for its body, then the bristles one by one with dark streaks between them
    // (each strand of ink has its own brightness, starts a little after or before its neighbours where the brush landed,
    // and runs dry at its own place, the edge strands first, breaking into dashes and then gone), and a fine ember grain
    // in the drying tail. It is soft light, so it is painted at no more than 1.25 pixels a CSS pixel.
    function brushPic() {
      const B = brush;
      if (B.pic) return B.pic;
      const pr = Math.min(kk, 1.25), pad = B.Wm * 2.4 + 16, P = B.pts, M = P.length, R = CH.rng(B.seed);
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      P.forEach((p) => { x0 = Math.min(x0, p.x - pad); y0 = Math.min(y0, p.y - pad); x1 = Math.max(x1, p.x + pad); y1 = Math.max(y1, p.y + pad); });
      const c = document.createElement("canvas");
      c.width = Math.max(1, Math.round((x1 - x0) * pr)); c.height = Math.max(1, Math.round((y1 - y0) * pr));
      const g = c.getContext("2d");
      g.setTransform(pr, 0, 0, pr, -x0 * pr, -y0 * pr);
      g.globalCompositeOperation = "lighter"; g.lineJoin = "round"; g.lineCap = "butt";
      // the outline, up one side and back down the other (dx moves it sideways)
      // the outline, up one side and back down the other (dx moves it sideways); it starts on the slant the brush landed on
      // (the upper edge touched first, the lower edge a little further along)
      const i0 = Math.round(0.054 * (M - 1)), outline = (grow, dx) => {
        g.beginPath();
        for (let i = 0; i < M; i++) { const p = P[i], hw = p.w * 0.5 * grow; g.lineTo(p.x + p.nx * hw + dx, p.y + p.ny * hw); }
        for (let i = M - 1; i >= i0; i--) { const p = P[i], hw = p.w * 0.5 * grow; g.lineTo(p.x - p.nx * hw + dx, p.y - p.ny * hw); }
        g.closePath();
      };
      // 1. the glow: the outline's blurred shadow only (the shape itself is drawn far off the canvas), a warm ember light
      g.save(); g.shadowColor = "rgba(236,112,72,0.34)"; g.shadowBlur = B.Wm * 1.3 * pr; g.shadowOffsetX = 30000; g.fillStyle = "#000"; outline(1.3, -30000 / pr); g.fill(); g.restore();
      // 2. the body's faint wash, from where the first bristle touched
      g.fillStyle = "rgba(240,128,92,0.09)"; outline(1, 0); g.fill();
      // 3. the bristles
      const NB = 26;
      for (let b = 0; b < NB; b++) {
        const o = (b + 0.5) / NB - 0.5 + (R() - 0.5) * 0.015, ao = Math.abs(o) * 2;
        const bright = R() < 0.18 ? 0.15 + 0.2 * R() : 0.45 + 0.55 * R();          // now and then a starved strand
        const from = 0.004 + 0.05 * (0.5 - o) + 0.02 * R(), dryAt = clamp(0.5 + 0.38 * R() - 0.3 * ao, 0.22, 0.92), sd = R() * 100;
        const col = ao < 0.35 ? "255,222,186" : ao < 0.75 ? "246,160,122" : "222,104,76";
        const runs = []; let run = null;
        for (let i = 0; i < M; i++) {
          const p = P[i]; let on = p.w > 0.9 && p.s >= from;
          if (on && p.s > dryAt) on = CH.noise(sd + (p.s * B.len) / 11, b * 3.7) > 0.28 + 0.66 * ((p.s - dryAt) / (1 - dryAt));
          if (on) { if (!run) runs.push((run = [])); run.push(p); } else run = null;
        }
        runs.forEach((rn) => {
          if (rn.length < 2) return;
          g.beginPath(); rn.forEach((p, k) => { const d = o * p.w * 0.96; if (k) g.lineTo(p.x + p.nx * d, p.y + p.ny * d); else g.moveTo(p.x + p.nx * d, p.y + p.ny * d); });
          const wa = rn.reduce((s, p) => s + p.w, 0) / rn.length;
          g.lineWidth = Math.max(0.6, (wa / NB) * 0.95); g.strokeStyle = `rgba(${col},${(0.08 + 0.3 * bright).toFixed(3)})`; g.stroke();
        });
      }
      // 4. the ember grain: fine bright specks, most in the drying tail
      for (let i = 0; i < 70; i++) {
        const s = 1 - Math.pow(R(), 1.6) * 0.7, p = P[Math.round(s * (M - 1))], o = (R() - 0.5) * 1.1, rr = 0.45 + 0.7 * R();
        if (p.w < 1.5) continue;
        g.fillStyle = `rgba(255,${200 + Math.round(40 * R())},160,${(0.2 + 0.4 * R()).toFixed(2)})`;
        g.beginPath(); g.arc(p.x + p.nx * o * p.w, p.y + p.ny * o * p.w, rr, 0, TAU); g.fill();
      }
      B.pic = { c, x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
      return B.pic;
    }

    /* ---------- update: a new state of the life ---------- */
    // How fast the sky follows (the springs' time, settle): about 0.6 s from one state to the next, as in the showcase;
    // while time runs, the life sends its weather only now and then (about every two years of play), so the sky takes
    // about half the time between two changes to reach each new one, and the weather drifts instead of stepping.
    let layoutAt = -9, easeT = 0.2, changedAt = -1, gapE = 0, livingNow = false;
    const Tp = new Float32Array(K.N);
    function update(S, how) {
      if (!S || !S.w) return;
      lastS = S;
      const quiet = !!(how && how.quiet);
      const g = CH.grammar(S.w);
      const L = [g.align, g.laminar, g.inward, g.spark, g.grow], sh = shadowOf(S);
      for (let i = 0; i < 5; i++) { T[K.L + i] = L[i]; T[K.SH + i] = sh[i]; }
      T[K.STRAIN] = clamp((S.stress || 0) / 1.5);
      T[K.PEACE] = clamp(S.peace ?? 0.6);
      T[K.CONTENT] = clamp(S.content ?? 0.6);
      T[K.WET] = wetOf(S);
      // the times outside: up to three letters, laid along the far horizon
      const letters = CH.lettersOf(S.world_era && S.world_era.letters);
      eraN = Math.min(3, letters.length); T[K.ERA] = eraN ? 1 : 0;
      for (let j = 0; j < 3; j++) { const c = letters[Math.min(j, Math.max(0, eraN - 1))]; if (c) rgb01(CH.HUE.bright[c]).forEach((v, i) => { T[K.E0 + j * 3 + i] = v; }); }
      // meteors: Red's share times a half arrive warm; the strain (S.stress as the game has it, 0..1.5) sends pale silver ones
      T[K.RATE] = g.spark * 0.5;
      T[K.SRATE] = S.stress || 0;
      inks = topTwo(S.w);
      // panels named by a selector may have come or gone: read them again, now and then
      if (typeof opts.clear === "string" && nowS - layoutAt > 0.5) { layoutAt = nowS; if (relayout()) { built = ""; measure(); } }
      // the springs' time from how far apart the changes come (the focus aside: it follows the panels, not the life)
      let moved = false;
      for (let i = 0; i < K.FOC; i++) if (Math.abs(T[i] - Tp[i]) > 1e-4) { moved = true; break; }
      if (moved) {
        const t = performance.now() / 1000, gap = changedAt < 0 ? 0 : t - changedAt;
        changedAt = t; gapE = gapE ? 0.6 * gapE + 0.4 * Math.min(gap, 8) : gap;
        Tp.set(T);
      }
      easeT = livingNow ? clamp(gapE / 6, 0.2, 1.4) : 0.2;
      // a first state, the one after a load and the years before the player takes over (how.quiet) jump straight there
      if (first || quiet || motionOf() === "off") { X.set(T); V.fill(0); }
      // a window of change opening wets the page again: one slow ripple (not more than one every few seconds)
      const win = !!(S.dyn && S.dyn.window);
      if (win && !lastWin && !first && !quiet) ripple();
      // in motion the eased numbers carry the sky to the new state, so a new age asks for no picture of its own (with
      // motion off, every change draws its one still frame anyway); only a first state, a quiet jump, a new size or a lost
      // and restored GL context force one
      if (first || quiet) force = true;
      lastWin = win; first = false; dirty = true;
      if (motionOf() === "off") ink.marks.forEach((b) => { b.still = true; });
    }
    // time runs between moments (the "living" event): the sky eases over the gaps between the life's messages
    function setLiving(on) { livingNow = !!on; if (!livingNow) { easeT = 0.2; gapE = 0; changedAt = -1; } }

    function ripple(x, y) {
      if (clock - lastRip < 2.5 && rip) return;
      lastRip = clock; rip = { t0: clock, x: x ?? 0.5, y: y ?? 0.5, hit: new Set() };
      dirty = true;
    }

    /* ---------- B1: the sky's ink ---------- */
    const ink = makeInk("night", 5150);
    // pointer: a press on the open sky drops ink; dragging slowly from it lays a stroke (a fast flick lays none, and a
    // stroke broken by a flick starts again where the pointer slows). A press on a panel or a control never drips here:
    // a panel's own module may lay ink on it with CH.ink.bloom(x, y, colours, {on: panel}).
    // inkDrag: the last touch laid a stroke (the sky's reading stays shut for it; it opens on a hover or a plain tap)
    let down = null, inkDrag = false;
    const isControl = (t) => t && t.closest && t.closest("button, a, input, select, textarea, label, summary, [role=button], [role=slider], [contenteditable=true], [data-noink]");
    const pressOf = (e, v) => (e.pointerType === "pen" && e.pressure > 0 ? clamp(e.pressure) : clamp(1 - v / 900, 0.25, 1));
    function onDown(e) {
      if (e.button > 0 || isControl(e.target)) return;
      if (!isSky(e.target)) return;
      const [x, y] = CH.local(host, e);
      if (x < 0 || y < 0 || x > W || y > H) return;
      down = { id: e.pointerId, mx: x, my: y, mt: performance.now(), v: 0, st: null }; inkDrag = false;
      ink.drop(x, y, inks, clamp(X[K.WET]), clock, motionOf() === "off", inkS);
      dirty = true;
    }
    function onMove(e) {
      if (!down || e.pointerId !== down.id) return;
      const [x, y] = CH.local(host, e), t = performance.now();
      const dm = Math.hypot(x - down.mx, y - down.my), dtm = Math.max(8, t - down.mt);
      down.v = down.v * 0.6 + 0.4 * (dm / dtm) * 1000;     // pointer speed, CSS px a second, lightly smoothed
      if (down.v >= 650) { down.st = null; down.mx = x; down.my = y; down.mt = t; return; }
      const wet = clamp(X[K.WET]), step = wet < ink.PEN ? 3 : Math.max(4, ink.reach(wet, inkS) * 0.1), p = pressOf(e, down.v);
      if (!down.st) { if (dm < step) return; down.st = ink.stroke(down.mx, down.my, inks, wet, clock, motionOf() === "off", inkS, p); }
      const q = down.st.P[down.st.P.length - 1];
      if (Math.hypot(x - q.x, y - q.y) >= step && !ink.strokeTo(down.st, x, y, clock, p)) down.st = ink.stroke(q.x, q.y, inks, wet, clock, motionOf() === "off", inkS, p);
      down.mx = x; down.my = y; down.mt = t; dirty = true;
    }
    const onUp = (e) => { if (down && e.pointerId === down.id) { inkDrag = e.pointerType !== "mouse" && !!down.st; down = null; } };
    // a drag that lays ink selects no text in the panels it crosses
    const onSelect = (e) => { if (down) e.preventDefault(); };
    stage.addEventListener("pointerdown", onDown, { passive: true });
    stage.addEventListener("selectstart", onSelect);
    stage.addEventListener("pointermove", onMove, { passive: true });
    window.addEventListener("pointerup", onUp, { passive: true });
    window.addEventListener("pointercancel", onUp, { passive: true });
    let inkShown = false;
    let inkAt = -9, inkAcc = 0, inkForce = true;
    function drawInk(dtc, now) {
      const rp = ripState();
      // every frame while a stroke is being laid or the ripple crosses; thirty times a second while ink spreads (slowly:
      // the eye cannot tell); ten times a second while it only dries and fades
      inkAcc += dtc;
      if (!rp && !inkForce && !down && inkShown && now - inkAt < (ink.busy(clock) ? 0.032 : 0.1)) return;
      if (!ink.marks.length && !inkShown) { inkAcc = 0; if (inkLive) inkSize(false); return; }
      if (!inkLive) inkSize(true);
      inkAt = now;
      const any = ink.draw({ g: cx, sg: softX, sc: softC, sc2: softC2, W, H, k: crisp._k || kk, clock, dtc: inkAcc, rp: rp && { x: rp.x, y: rp.y, R: rp.R, hit: rip.hit }, page: clamp(X[K.WET]) });
      inkAcc = 0; inkForce = false;
      // the ink canvas is composited only while there is ink
      if (any !== inkShown) { inkShown = any; crisp.style.visibility = any ? "visible" : "hidden"; }
    }

    /* ---------- B1: --wet and the filter follow the eased wetness ---------- */
    // --wet on <html> is inherited by every element, so each change restyles the whole page: late in a life, with a long
    // story, that took 0.4 to 1.3 s a time on a slow phone (b7 life_adult_p, 10-18). It moves only after the wetness has
    // drifted 0.08 from what it last said (the story's own --h-wet moves in tenths for the same reason); the filter,
    // which restyles nothing, follows the eased value
    const filterEl = ensureFilter("chs-ink");
    const wetHost = document.documentElement;
    let wetSet = -1, wetSaid = -1;
    function pushWet() {
      const w = X[K.WET];
      if (Math.abs(w - wetSet) < 0.004) return;
      wetSet = w;
      if (primary === inst && (wetSaid < 0 || Math.abs(w - wetSaid) >= 0.08)) { wetSaid = w; wetHost.style.setProperty("--wet", w.toFixed(3)); }
      setFilterWet(filterEl, w);
    }

    /* ---------- the sparks: stars, lattice, constellations, embers, motes, lights, meteors ---------- */
    const meteors = [], bits = [], metR = CH.rng(31337);
    function ripState() {
      if (!rip) return null;
      const u = (clock - rip.t0) / 4.2;
      if (u >= 1) { rip = null; return null; }
      const D = Math.hypot(W, H) * 0.62;
      return { u, x: rip.x * W, y: rip.y * H, R: D * (1 - Math.pow(1 - u, 2.2)), s: smooth(clamp(u / 0.08)) * Math.pow(1 - u, 1.4) };
    }
    function drawSparks(dtc, still) {
      const S = sprites(), g = sx, p = motionOf() === "calm" ? 0.5 : 1, LW = X[K.L], LU = X[K.L + 1], LB = X[K.L + 2], LR = X[K.L + 3], LG = X[K.L + 4];
      const shW = X[K.SH], shU = X[K.SH + 1], shR = X[K.SH + 3], shG = X[K.SH + 4];
      const strain = X[K.STRAIN], peace = X[K.PEACE], content = X[K.CONTENT], rp = ripState(), k = sparks._k || kk;
      g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = "source-over"; g.globalAlpha = 1;
      g.clearRect(0, 0, sparks.width, sparks.height);
      const ox = drift * H;                                    // the wind's carry, CSS px at depth 1
      const boost = (x, y) => { if (!rp) return 0; const d = (Math.hypot(x - rp.x, y - rp.y) - rp.R) / (34 * su); return Math.exp(-d * d) * rp.s * 0.9; };

      // the dust sheet, carried slowly (it is far); clear, still air shows much more of it, milky air hides it
      if (dust) {
        const dx = ((ox * 0.32 * k) % dust.width + dust.width) % dust.width;
        g.globalAlpha = clamp(0.36 + 0.62 * peace - 0.18 * strain, 0.15, 1);
        g.drawImage(dust, dx, 0, dust.width, dust.height, 0, 0, sparks.width, sparks.height);
        g.drawImage(dust, dx - dust.width, 0, dust.width, dust.height, 0, 0 - 0, sparks.width, sparks.height);
      }
      g.setTransform(k, 0, 0, k, 0, 0);
      g.globalCompositeOperation = "lighter";

      // the bright stars: in still, clear air they are pin-sharp and steady; in unsettled air they swell, haze and
      // shimmer; in wind the brightest smear into short streaks along it (so the wind shows in a still frame); their light
      // is warmer the more content they are
      const tw = clamp(0.08 + 0.45 * (1 - peace) + 0.35 * strain, 0, 0.85), twr = 1 + 0.8 * strain;
      const haloA = 0.42 * (1.25 - 0.8 * peace) + 0.15 * strain, coreK = 1.25 - 0.45 * peace;
      const sLen = (2 + 10 * strain) * su, ca = Math.cos(-WIND), sa = Math.sin(-WIND), warmK = 0.2 + 0.65 * content;
      for (let i = 0; i < stars.length; i++) {
        const s = stars[i];
        let x = (s.x * W + ox * s.z) % W; if (x < 0) x += W;
        const y = s.y * H;
        const a = Math.min(1, s.m * (0.75 + 0.25 * peace) * (1 - tw * (1 - 0.55 * s.m) * (0.5 + 0.5 * Math.sin(clock * s.f * twr + s.p))) + boost(x, y));
        if (a < 0.02) continue;
        const c = s.c === 0 || s.c === 6 ? (s.wt < warmK ? 0 : 6) : s.c;
        const r = (0.55 + 1.35 * s.m) * coreK * 2.1;
        if (s.m > 0.5 && strain > 0.02) {
          // the streak: the halo drawn long and thin along the wind, trailing upwind of the star
          const L = sLen * (0.6 + 0.6 * s.m) * s.z, hr = r * 0.9;
          g.setTransform(ca * k, sa * k, -sa * k, ca * k, x * k, y * k); g.globalAlpha = a * Math.min(1, 0.25 + 1.2 * strain);
          g.drawImage(S.halo[c], -L - hr, -hr * 0.45, L + hr * 2, hr * 0.9);
          g.setTransform(k, 0, 0, k, 0, 0);
        }
        g.globalAlpha = a; g.drawImage(S.core[c], x - r, y - r, r * 2, r * 2);
        if (s.m > 0.62) { const hr = r * (2.6 + 1.6 * (1 - peace)); g.globalAlpha = a * haloA * s.m; g.drawImage(S.halo[c], x - hr, y - hr, hr * 2, hr * 2); }
        // the brightest few wear the four-pointed spark; Blue's clear light makes it longer and crisper
        if (s.m > 0.88) { const z = (5 + 9 * LU) * su * (0.7 + 0.3 * s.m); g.globalAlpha = a * (0.25 + 0.6 * LU); g.drawImage(S.spike, x - z, y - z, z * 2, z * 2); }
      }

      // WHITE: the lattice. Its stars ease from where they were scattered onto the nodes as White grows; once settled, gilt
      // arcs join neighbouring nodes that are both lit, ring by ring, through where the stars are now (so no line hangs in
      // empty sky). It breathes slowly; in shadow (rigid) it freezes and its lines harden.
      if (LW > 0.02 && lattice) {
        const Lt = lattice, ax = Lt.ax, ay = Lt.ay, settleK = smooth(clamp((LW - 0.1) / 0.75));
        const nAct = 15 * clamp(LW * 1.2), breath = 1 + 0.014 * Math.sin(clock * 0.42) * (1 - shW);
        const pos = Lt.nodes.map((nd) => {
          const on = clamp(nAct - Lt.nodes.indexOf(nd)); if (on <= 0) return null;
          const R = Lt.rings[nd.ring] * Lt.u * breath, nx = ax + Math.cos(nd.ang) * R, ny = ay + Math.sin(nd.ang) * R;
          const wob = (1 - settleK) * 6 * Math.sin(clock * 0.3 + nd.p) * (1 - shW);
          return { x: nx + nd.hx * (1 - settleK) + wob, y: ny + nd.hy * (1 - settleK), on, nd, R };
        });
        g.globalCompositeOperation = "lighter";
        g.strokeStyle = "rgba(244,214,140,1)"; g.lineWidth = (shW > 0.2 ? 1.5 : 1) / k;
        for (let ri = 0; ri < 3; ri++) {
          const ring = pos.filter((q) => q && q.nd.ring === ri).sort((a, b) => a.nd.ang - b.nd.ang);
          for (let j = 0; j + 1 < ring.length; j++) {
            const A = ring[j], B = ring[j + 1];
            if (B.nd.j - A.nd.j !== 1) continue;
            const al = 0.34 * settleK * settleK * Math.min(A.on, B.on) * LW * (1 + 0.6 * shW);
            if (al < 0.01) continue;
            // the settled arc's control point (the ring bowed between the two nodes), carried with the stars as they settle
            const da = B.nd.ang - A.nd.ang, mid = (A.nd.ang + B.nd.ang) / 2, R = A.R, cr = R / Math.cos(da / 2);
            const sax = ax + Math.cos(A.nd.ang) * R, say = ay + Math.sin(A.nd.ang) * R, sbx = ax + Math.cos(B.nd.ang) * R, sby = ay + Math.sin(B.nd.ang) * R;
            const qx = ax + Math.cos(mid) * cr + ((A.x - sax) + (B.x - sbx)) / 2, qy = ay + Math.sin(mid) * cr + ((A.y - say) + (B.y - sby)) / 2;
            g.globalAlpha = al; g.beginPath(); g.moveTo(A.x, A.y); g.quadraticCurveTo(qx, qy, B.x, B.y); g.stroke();
          }
        }
        // the faint whole rings of the rose window, the settled stars' guide, only once the lattice has mostly settled
        const guide = smooth(clamp((settleK - 0.5) / 0.5));
        if (guide > 0.01) {
          g.globalAlpha = 0.08 * guide * LW;
          for (let ri = 0; ri < 3; ri++) { g.beginPath(); g.arc(ax, ay, Lt.rings[ri] * Lt.u * breath, Math.PI * 1.06, Math.PI * 1.94); g.stroke(); }
        }
        pos.forEach((q, i) => {
          if (!q) return;
          const tws = shW > 0.2 ? 1 : 0.85 + 0.15 * Math.sin(clock * 0.9 + i);
          const a = q.on * (0.5 + 0.5 * LW) * tws + boost(q.x, q.y), r = 2.8 + 1.4 * LW;
          g.globalAlpha = Math.min(1, a); g.drawImage(S.core[1], q.x - r, q.y - r, r * 2, r * 2);
          const hr = r * 3; g.globalAlpha = a * 0.4; g.drawImage(S.halo[1], q.x - hr, q.y - hr, hr * 2, hr * 2);
          if (q.nd.ring === 0 && q.nd.j === 1) { const z = 9 * su * (0.6 + 0.4 * LW); g.globalAlpha = a * 0.5; g.drawImage(S.spikeW, q.x - z, q.y - z, z * 2, z * 2); }
        });
      }

      // BLUE: the fine geometry of a star chart: a few meridians and parallels around a pole beyond the top right corner,
      // in cool hairlines, with ticks along one parallel. Exact and quiet; it turns with the sky.
      if (LU > 0.05) {
        const px = W * 0.86 + ox * 0.15, py = -H * 0.42, Rm = Math.hypot(W, H) * 1.5, rot = 0.05 * Math.sin(clock * 0.02);
        g.globalCompositeOperation = "lighter"; g.strokeStyle = "rgba(150,196,245,1)"; g.lineWidth = 1 / k;
        g.globalAlpha = 0.13 * LU * LU;
        g.beginPath();
        for (let i = 0; i < 9; i++) { const a = Math.PI * 0.5 + (i - 4) * 0.13 + rot; g.moveTo(px + Math.cos(a) * H * 0.5, py + Math.sin(a) * H * 0.5); g.lineTo(px + Math.cos(a) * Rm, py + Math.sin(a) * Rm); }
        [0.78, 1.02, 1.26].forEach((f) => { g.moveTo(px + Math.cos(Math.PI * 0.12) * H * f, py + Math.sin(Math.PI * 0.12) * H * f); g.arc(px, py, H * f, Math.PI * 0.12, Math.PI * 0.95); });
        g.stroke();
        g.globalAlpha = 0.16 * LU * LU; g.beginPath();
        for (let i = 0; i < 40; i++) { const a = Math.PI * 0.14 + i * 0.02 + rot, r0 = H * 1.02, l = i % 5 ? 4 : 8; g.moveTo(px + Math.cos(a) * r0, py + Math.sin(a) * r0); g.lineTo(px + Math.cos(a) * (r0 + l), py + Math.sin(a) * (r0 + l)); }
        g.stroke();
      }

      // BLUE: constellations in the open sky, the first ones to show where Blue is faint, all six where it leads; hairlines
      // between their stars, stopping short of each star as on a star chart. In shadow (indecisive) a second image wavers
      // beside them and never settles.
      if (LU > 0.02) {
        for (let j = 0; j < consts.length; j++) {
          const vis = clamp(LU * 6.2 - j * 0.95); if (vis <= 0) continue;
          const C = consts[j];
          const bx = C.gx + mod(C.ax - C.gx + ox * 0.8, C.gw), by = C.ay;
          const copies = shU > 0.05 ? 2 : 1;
          for (let cp = 0; cp < copies; cp++) {
            const dx = cp ? Math.sin(clock * 0.8 + j) * 4 * shU : 0, dy = cp ? Math.cos(clock * 0.61 + j * 2) * 3 * shU : 0, cA = cp ? 0.55 * shU : 1;
            const P = C.pts.map(([x, y]) => [bx + x * C.sc + dx, by + y * C.sc + dy]);
            g.globalCompositeOperation = "source-over"; g.strokeStyle = "rgba(171,207,241,1)"; g.lineWidth = 1 / k;
            g.globalAlpha = 0.46 * vis * cA;
            g.beginPath();
            C.edges.forEach(([a, b]) => { const A = P[a], B = P[b], L = Math.hypot(B[0] - A[0], B[1] - A[1]); if (L < 10) return; const ux = (B[0] - A[0]) / L, uy = (B[1] - A[1]) / L;
              g.moveTo(A[0] + ux * 4, A[1] + uy * 4); g.lineTo(B[0] - ux * 4, B[1] - uy * 4); });
            g.stroke();
            g.globalCompositeOperation = "lighter";
            P.forEach(([x, y], i) => { const a = Math.min(1, (0.5 + 0.5 * C.m[i]) * vis * cA + boost(x, y)), r = 1.9 + 1.5 * C.m[i];
              g.globalAlpha = a; g.drawImage(S.core[2], x - r, y - r, r * 2, r * 2);
              if (C.m[i] > 0.8) { const z = 6 * su + 4 * LU; g.globalAlpha = a * 0.55; g.drawImage(S.spike, x - z, y - z, z * 2, z * 2); } });
          }
        }
      }

      // BLACK: motes falling slowly inward toward the eye, faster as they near it (gravity), turning with the smoke; they
      // fall within the open stretch the eye sits in
      if (LB > 0.02) {
        const F = lay.focus, n = Math.round(motes.length * LB * p), cxm = F.x + F.w / 2, cym = F.y + F.h / 2, Rx = Math.max(F.w, F.h) * 0.55, Ry = Math.min(Rx * 0.82, F.h * 0.62 + 20);
        for (let i = 0; i < n; i++) {
          const m = motes[i], u = frac(clock / m.T + m.p), r = 1 - u * u, a = m.a + swirl * 1.6 + u * 1.9;
          const x = cxm + Math.cos(a) * r * Rx, y = cym + Math.sin(a) * r * Ry, al = Math.pow(Math.sin(Math.PI * u), 1.5) * (0.4 + 0.5 * LB);
          const rr = (1.8 + 1.8 * m.s) * (1 - 0.45 * u);
          g.globalAlpha = al; g.drawImage(S.core[3], x - rr, y - rr, rr * 2, rr * 2);
          const hr = rr * 3; g.globalAlpha = al * 0.35; g.drawImage(S.halo[3], x - hr, y - hr, hr * 2, hr * 2);
        }
      }

      // RED: the brushstroke of ember light across the open sky (its picture is painted once, brushPic), as strong as Red's
      // share. In motion it breathes quickly, and now and then a flare runs along it from where the brush landed to where
      // it lifted (fast to flare, fast to fade). In shadow (reckless) the brush has flung its ink past its end: droplets
      // overshoot and scatter beyond the tip.
      if (LR > 0.02 && brush) {
        const B = brush, vis = smooth(clamp((LR - 0.02) / 0.1)) * LR, pic = brushPic();
        const fl = still ? 1 : 0.9 + 0.1 * Math.sin(clock * 2.1) * Math.sin(clock * 1.37 + 1);
        g.globalCompositeOperation = "lighter";
        g.globalAlpha = Math.min(1, vis * fl); g.drawImage(pic.c, pic.x, pic.y, pic.w, pic.h);
        const run = still ? 1 : frac(clock / B.cyc + B.cp) / 0.16;
        if (run < 1) {
          const q = B.pts[Math.round(smooth(run) * (B.pts.length - 1))], a = Math.sin(Math.PI * run) * vis, hr = q.w * 1.5 + 8, cr = q.w * 0.4 + 3;
          g.globalAlpha = a * 0.6; g.drawImage(S.halo[4], q.x - hr, q.y - hr, hr * 2, hr * 2);
          g.globalAlpha = a * 0.55; g.drawImage(S.core[0], q.x - cr, q.y - cr, cr * 2, cr * 2);
        }
        if (shR > 0.05) B.spat.forEach((d) => { const a = shR * vis * d.m, r = d.r * 1.6; g.globalAlpha = a; g.drawImage(S.core[4], d.x - r, d.y - r, r * 2, r * 2); });
        // the embers the stroke sheds: from just above its upper edge each drifts up and back along it, flaring and fading
        // quickly; in a still frame each glows where it always rests, so the stroke is never bare
        const n = Math.round(embers.length * LR * p);
        for (let i = 0; i < n; i++) {
          const e = embers[i], q = B.pts[Math.round(e.s * (B.pts.length - 1))], u = frac(clock / e.T + e.p);
          const off = q.w * 0.5 * (1 + e.d) + 2, lift = u * (18 + 26 * e.m) * su;
          const x = q.x + q.nx * off - q.tx * u * 14 * su + e.dx * 8 * su, y = q.y + q.ny * off - lift;
          const flare = Math.pow(Math.max(0, Math.sin(clock * e.f * (1 + 0.6 * strain) + e.ph)), 8);
          const env = smooth(clamp(u / 0.12)) * Math.pow(1 - u, 1.1);
          const a = Math.min(1, (0.25 + 0.75 * env) * (0.55 + 0.45 * flare) * (0.6 + 0.4 * e.m) * (0.55 + 0.45 * LR) * 1.3), r = 1.2 + 1.3 * e.m + 1.2 * flare;
          if (a < 0.02) continue;
          g.globalAlpha = a; g.drawImage(S.core[4], x - r, y - r, r * 2, r * 2);
          const hr = r * 3.2; g.globalAlpha = a * 0.4; g.drawImage(S.halo[4], x - hr, y - hr, hr * 2, hr * 2);
        }
      }

      // RED: sparks rising slowly from the hearth along the floor of the open sky, carried sideways by the wind; each
      // flickers fast and fades as it climbs. In shadow (reckless) they climb higher and scatter wider.
      if (LR > 0.02) {
        const n = Math.round(rising.length * LR * p), wind = 1 + 1.2 * strain;
        for (let i = 0; i < n; i++) {
          const q = rising[i], u = frac(clock * wind / q.T + q.p);
          const env = smooth(clamp(u / 0.08)) * Math.pow(1 - u, 1.3);
          const fl = 0.6 + 0.4 * Math.sin(clock * 11 * q.w + q.p * 40) * Math.sin(clock * 7.3 * q.w + q.p * 17);
          const hgt = q.h * (1 + 0.6 * shR) * q.gh, sway = (Math.sin(clock * 0.9 * q.w + q.p * 9) * Math.min(18, q.gw * 0.2) + (q.p - 0.5) * 80 * shR * u) * su;
          const x = q.gx + mod(q.x - q.gx + sway + ox * 0.9 * u * 3, q.gw);
          const y = q.base - hgt * (1 - Math.pow(1 - u, 1.6));
          const a = env * fl * (0.5 + 0.5 * LR), r = (1.0 + 1.3 * q.s) * (1 - 0.4 * u);
          if (a < 0.02) continue;
          g.globalAlpha = a; g.drawImage(S.core[4], x - r, y - r, r * 2, r * 2);
          const hr = r * 3.4; g.globalAlpha = a * 0.35; g.drawImage(S.halo[4], x - hr, y - hr, hr * 2, hr * 2);
        }
      }

      // GREEN: a few lights rising slowly through the open sky and breathing; in shadow (stuck) they slow to stillness
      if (LG > 0.02) {
        const n = Math.round(flies.length * LG * p), go = 1 - 0.85 * shG;
        for (let i = 0; i < n; i++) {
          const f = flies[i], t = clock * go, cyc = frac(t * 0.0075 * f.f + f.q);
          const x = f.x + Math.sin(t * 0.23 * f.f + f.p) * 26 * su, y = f.y - cyc * 0.34 * f.gh;
          const breath = 0.25 + 0.75 * Math.pow(0.5 + 0.5 * Math.sin(t * 0.75 * f.f + f.p * 2), 2) * (1 - 0.55 * shG);
          const a = Math.pow(Math.sin(Math.PI * cyc), 0.8) * breath * (0.45 + 0.6 * LG), r = 1.7 + 1.3 * breath;
          g.globalAlpha = Math.min(1, a); g.drawImage(S.core[5], x - r, y - r, r * 2, r * 2);
          const hr = r * 3.6; g.globalAlpha = a * 0.45; g.drawImage(S.halo[5], x - hr, y - hr, hr * 2, hr * 2);
        }
      }

      // Meteors, two kinds. Red's (rate: Red's share x 0.5) are warm; the strain's (rate: S.stress) are pale silver, so a
      // strained life does not borrow Red's colour. In motion they arrive at random; in a still frame a fixed few of each
      // hang where they always do, so the same age always shows the same sky.
      const rates = [X[K.RATE], X[K.SRATE]];
      if (still) {
        meteors.length = 0; bits.length = 0;
        for (let kind = 0; kind < 2; kind++) {
          const n = Math.min(3, Math.floor(rates[kind] * 2.2 + 0.5));
          for (let i = 0; i < n; i++) { const r = CH.rng(900 + i + kind * 50); const m = newMeteor(r, kind); m.age = m.life * 0.42; meteors.push(m); }
        }
      } else if (dtc > 0) for (let kind = 0; kind < 2; kind++) if (metR() < dtc * rates[kind] * 8 * p / 60) meteors.push(newMeteor(metR, kind));
      for (let i = meteors.length - 1; i >= 0; i--) {
        const m = meteors[i]; m.age += still ? 0 : dtc;
        const u = m.age / m.life;
        if (u >= 1) {
          // in shadow (reckless) a warm meteor does not just fade: it bursts, and its sparks overshoot and scatter
          if (shR > 0.05 && m.kind === 0) for (let j = 0, nb = 4 + Math.round(8 * shR); j < nb; j++) bits.push({ x: m.x + m.vx * m.age, y: m.y + m.vy * m.age, vx: m.vx * 0.3 + (metR() - 0.5) * 260 * shR * su, vy: m.vy * 0.3 + (metR() - 0.5) * 260 * shR * su, age: 0, life: 0.45 + 0.5 * metR() });
          meteors.splice(i, 1); continue;
        }
        const env = u < 0.14 ? smooth(u / 0.14) : Math.pow(1 - (u - 0.14) / 0.86, 1.7);
        const hx = m.x + m.vx * m.age, hy = m.y + m.vy * m.age, sp = Math.hypot(m.vx, m.vy), L = m.len * (0.3 + 0.7 * Math.min(1, u * 3));
        const tx = hx - (m.vx / sp) * L, ty = hy - (m.vy / sp) * L;
        const gr = g.createLinearGradient(hx, hy, tx, ty);
        if (m.kind === 0) { gr.addColorStop(0, "rgba(255,236,206,1)"); gr.addColorStop(0.25, "rgba(255,170,120,0.6)"); gr.addColorStop(1, "rgba(243,140,107,0)"); }
        else { gr.addColorStop(0, "rgba(236,240,255,1)"); gr.addColorStop(0.3, "rgba(200,210,240,0.5)"); gr.addColorStop(1, "rgba(170,185,230,0)"); }
        g.strokeStyle = gr; g.lineCap = "round";
        g.globalAlpha = env * 0.28; g.lineWidth = 3.2 * Math.max(0.7, su); g.beginPath(); g.moveTo(hx, hy); g.lineTo(tx, ty); g.stroke();
        g.globalAlpha = env * 0.95; g.lineWidth = 1.1; g.beginPath(); g.moveTo(hx, hy); g.lineTo(tx, ty); g.stroke();
        const r = 2.4, spr = m.kind === 0 ? S.core[4] : S.silver; g.globalAlpha = env; g.drawImage(spr, hx - r * 1.6, hy - r * 1.6, r * 3.2, r * 3.2);
      }
      for (let i = bits.length - 1; i >= 0; i--) {
        const b = bits[i]; b.age += dtc; if (b.age >= b.life) { bits.splice(i, 1); continue; }
        b.vy += 240 * su * dtc; b.x += b.vx * dtc; b.y += b.vy * dtc;
        const a = Math.pow(1 - b.age / b.life, 1.5), r = 1.4;
        g.globalAlpha = a; g.drawImage(S.core[4], b.x - r, b.y - r, r * 2, r * 2);
      }
      g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    }
    // a meteor starts in the widest open stretch of sky and crosses it
    function newMeteor(r, kind) {
      const F = lay.focus, dir = r() < 0.5 ? 1 : -1, ang = 0.32 + r() * 0.38, v = (360 + r() * 420) * Math.max(0.6, su);
      return { kind, x: F.x + (0.08 + 0.84 * r()) * F.w, y: F.y + (0.04 + 0.5 * r()) * F.h, vx: dir * Math.cos(ang) * v, vy: Math.sin(ang) * v * (lay.full ? 1 : 0.6), len: (70 + r() * 110) * Math.max(0.55, su), life: 0.55 + r() * 0.5, age: 0 };
    }

    /* ---------- the field in WebGL: the gas baked now and then, the field 30 (or 15) times a second, dissolved ---------- */
    const Lv = new Float32Array(5), Shv = new Float32Array(5);
    let gt = null;                    // the GL targets for this size: gas A/B, field A/B and their bookkeeping
    const NEB_MARGIN = 0.22;          // the gas box reaches this far (heights) past the left edge, so the wind can carry it
    const stretchOf = (st) => 1 / (1 + 1.6 * st);   // the wind draws the gas out: half as wide again at a strong strain
    // where to sample a bake made at drift d0 and stretch s, for the drift now: the wind's carry undone through the stretch
    function nebOffset(n, d) {
      const a = 0.4783 * (d - n.d0), c = Math.cos(WIND), s = Math.sin(WIND), is = 1 / n.s;
      return [a * (c * c * is + s * s), a * s * c * (is - 1)];
    }
    function glTargets() {
      if (gt && gt.w === fieldC.width && gt.h === fieldC.height) return gt;
      if (gt) [gt.nA, gt.nB, gt.fA, gt.fB].forEach((t) => G.drop(t));
      const w = fieldC.width, h = fieldC.height, asp = w / h;
      const box = [-NEB_MARGIN, -0.07, asp + 0.03, 1.07];
      const nw = Math.max(2, Math.round((box[2] - box[0]) * h)), nh = Math.max(2, Math.round((box[3] - box[1]) * h));
      gt = { w, h, box, nA: G.target(nw, nh), nB: G.target(nw, nh), fA: G.target(w, h), fB: G.target(w, h),
        neb: [null, null], nebI: 0, nebAt: -99, fld: 0, fldAt: -99, fldInt: 1 / 30, fldPrevValid: false, lastX: new Float32Array(K.N), mixing: false, gpu: [], q: [] };
      return gt;
    }
    function bakeNeb(tm, nowT) {
      const { gl, NEB } = G, t = glTargets(), i = 1 - t.nebI, tgt = i ? t.nB : t.nA, s = stretchOf(X[K.STRAIN]);
      gl.bindFramebuffer(gl.FRAMEBUFFER, tgt.fb); gl.viewport(0, 0, tgt.w, tgt.h); gl.useProgram(NEB.pr);
      gl.uniform4f(NEB.u.uBox, t.box[0], t.box[1], t.box[2], t.box[3]); gl.uniform2f(NEB.u.uCen, 0.5 * (t.w / t.h), 0.5);
      gl.uniform1f(NEB.u.uT, tm.clock % 3600); gl.uniform1f(NEB.u.uDrift, tm.drift % 1000); gl.uniform1f(NEB.u.uStretch, s);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      t.neb[i] = { d0: tm.drift % 1000, dRaw: tm.drift, s, at: nowT }; t.nebI = i; t.nebAt = nowT;
    }
    function renderField(tm, nowT, intoNewest) {
      const { gl, FLD } = G, t = glTargets(), i = 1 - t.fld, tgt = i ? t.fB : t.fA;
      gl.bindFramebuffer(gl.FRAMEBUFFER, tgt.fb); gl.viewport(0, 0, t.w, t.h); gl.useProgram(FLD.pr);
      for (let j = 0; j < 5; j++) { Lv[j] = X[K.L + j]; Shv[j] = X[K.SH + j]; }
      const nb = t.neb[t.nebI], na = t.neb[1 - t.nebI] || nb, nm = na === nb ? 1 : smooth(clamp((nowT - nb.at) / 0.9));
      // each bake is carried by the wind that has blown since it was made
      const oB = nebOffset(nb, nb.d0 + (tm.drift - nb.dRaw)), oA = nebOffset(na, na.d0 + (tm.drift - na.dRaw));
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, (1 - t.nebI ? t.nB : t.nA).t);
      gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, (t.nebI ? t.nB : t.nA).t);
      gl.uniform1i(FLD.u.uNebA, 0); gl.uniform1i(FLD.u.uNebB, 1);
      gl.uniform2f(FLD.u.uOffA, oA[0], oA[1]); gl.uniform2f(FLD.u.uOffB, oB[0], oB[1]); gl.uniform1f(FLD.u.uNebMix, nm);
      gl.uniform4f(FLD.u.uNebBox, t.box[0], t.box[1], t.box[2], t.box[3]);
      gl.uniform2f(FLD.u.uRes, t.w, t.h);
      gl.uniform1f(FLD.u.uT, tm.clock % 3600); gl.uniform1f(FLD.u.uDrift, tm.drift % 1000); gl.uniform1f(FLD.u.uSwirl, tm.swirl % TAU);
      gl.uniform1f(FLD.u.uInflow, tm.inflow % 64); gl.uniform1f(FLD.u.uAur, tm.aur % 1000); gl.uniform1f(FLD.u.uCaus, tm.caus % 1000);
      gl.uniform1fv(FLD.u.uL, Lv); gl.uniform1fv(FLD.u.uSh, Shv);
      gl.uniform4f(FLD.u.uWx, X[K.STRAIN], X[K.PEACE], X[K.CONTENT], X[K.WET]);
      gl.uniform4f(FLD.u.uFoc, X[K.FOC], X[K.FOC + 1], X[K.FOC + 2], X[K.FOC + 3]);
      gl.uniform3f(FLD.u.uE0, X[K.E0], X[K.E0 + 1], X[K.E0 + 2]); gl.uniform3f(FLD.u.uE1, X[K.E1], X[K.E1 + 1], X[K.E1 + 2]); gl.uniform3f(FLD.u.uE2, X[K.E2], X[K.E2 + 1], X[K.E2 + 2]);
      gl.uniform2f(FLD.u.uEra, eraN, X[K.ERA]);
      const rp = ripState(), asp = W / H;
      if (rp) gl.uniform4f(FLD.u.uRip, rip.x * asp, 1 - rip.y, rp.R / H, rp.s); else gl.uniform4f(FLD.u.uRip, 0, 0, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      t.fld = i; t.fldPrevValid = !intoNewest && t.fldAt > -50; t.fldAt = nowT;
    }
    function copyField(mix) {
      const { gl, CPY } = G, t = glTargets();
      gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, fieldC.width, fieldC.height); gl.useProgram(CPY.pr);
      const cur = t.fld ? t.fB : t.fA, prev = t.fld ? t.fA : t.fB;
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, (t.fldPrevValid ? prev : cur).t);
      gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, cur.t);
      gl.uniform1i(CPY.u.uA, 0); gl.uniform1i(CPY.u.uB, 1); gl.uniform1f(CPY.u.uMix, t.fldPrevValid ? mix : 1);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
    // the GPU's own time for this sky's passes, where the browser can measure it (EXT_disjoint_timer_query)
    function gpuBegin() { const e = G.timer, t = gt; if (!e || !t || t.q.length > 3) return null; const q = e.createQueryEXT(); e.beginQueryEXT(e.TIME_ELAPSED_EXT, q); return q; }
    function gpuEnd(q) { if (!q) return; const e = G.timer; e.endQueryEXT(e.TIME_ELAPSED_EXT); gt.q.push(q); }
    function gpuPoll() {
      const e = G && G.timer, t = gt; if (!e || !t) return;
      while (t.q.length) {
        const q = t.q[0]; if (!e.getQueryObjectEXT(q, e.QUERY_RESULT_AVAILABLE_EXT)) break;
        if (!G.gl.getParameter(e.GPU_DISJOINT_EXT)) { t.gpu.push(e.getQueryObjectEXT(q, e.QUERY_RESULT_EXT) / 1e6); if (t.gpu.length > 300) t.gpu.shift(); }
        e.deleteQueryEXT(q); t.q.shift();
      }
    }
    // one frame of the field. force: draw the newest state at once (a still frame, a new size, a jump of state)
    let rateNow = 30;
    function drawFieldGL(tm, nowT, forceNow) {
      const t = glTargets();
      gpuPoll(); const q = gpuBegin();
      // the gas: baked again every couple of seconds, at once when the wind's stretch has changed, or before the wind has
      // carried the last bake beyond its margin; at most four bakes a second, each dissolved into over a moment
      const nb = t.neb[t.nebI], st = stretchOf(X[K.STRAIN]);
      const carried = nb ? nebOffset(nb, nb.d0 + (tm.drift - nb.dRaw)) : [0, 0];
      const due = !nb || forceNow && Math.abs(nb.s - st) > 0.002 || nowT - t.nebAt > 2.4 || Math.abs(nb.s - st) > 0.012 || carried[0] > NEB_MARGIN * 0.7 || Math.abs(carried[1]) > 0.05;
      if (due && (!nb || forceNow || nowT - t.nebAt > 0.25)) { bakeNeb(tm, nowT); if (forceNow || !nb) t.neb[1 - t.nebI] = t.neb[t.nebI]; }
      // The field: only as many pictures as its motion needs. While something in it changes quickly (the ripple crossing,
      // or the eased numbers moving visibly since the last picture, as when the age is scrubbed) 30 a second (60 for the
      // ripple), each dissolved into from the last, frame by frame. Otherwise the sky only drifts, so 15 a second in full
      // motion (up to 25 as the wind rises and streams the veil; its streaks are long and level, so a few pixels between
      // pictures do not show) and 10 to 15 in calm, each shown once as it is drawn; on the frames between, the field's
      // canvas is not touched at all, so nothing above it is repainted for it.
      const sp = CH.speed();
      let moved = 0;
      for (let i = 0; i < K.N; i++) moved = Math.max(moved, Math.abs(X[i] - t.lastX[i]));
      const fast = !!rip || moved > 0.02, gust = smooth(clamp((X[K.STRAIN] - 0.3) / 0.5));
      rateNow = rip ? 60 : fast ? 30 : sp < 1 ? Math.round(10 + 5 * gust) : Math.round(15 + 10 * gust);
      const iv = 1 / rateNow;
      let drew = false;
      if (forceNow || nowT - t.fldAt >= iv - 0.004) { renderField(tm, nowT, forceNow); t.fldInt = iv; t.lastX.set(X); drew = true; }
      if (fast && !forceNow) copyField(clamp((nowT - t.fldAt) / t.fldInt));
      else if (drew || t.mixing) copyField(1);
      t.mixing = fast && !forceNow;
      gpuEnd(q);
    }
    // The Canvas2D painting of the same sky, for when WebGL is missing: the shader's layers baked into textures (above, and
    // here the ones that depend on this sky's size) and moved by the same clocks, painted at a quarter of the CSS size.
    let tx = {}, seen = {}, sync = false, missing = false, shown = false, stamp = 0, tmB = null, tmpC = null;
    function texture(key, shared, make, forceIt) {
      const M = shared ? SHARED2D : tx;
      const j = M[key] || (M[key] = make());
      if (!work(j, !!forceIt, stamp, sync ? 10 : 2.5)) { missing = true; return null; }
      if (!(key in seen)) seen[key] = clock;
      return j;
    }
    const fadeOf = (key) => (sync ? 1 : clamp((clock - seen[key]) / 0.8));
    function scratch(w, h) {
      if (!tmpC) tmpC = document.createElement("canvas");
      if (tmpC.width !== w || tmpC.height !== h) { tmpC.width = w; tmpC.height = h; }
      const s = tmpC.getContext("2d"); s.setTransform(1, 0, 0, 1, 0, 0); s.globalCompositeOperation = "source-over"; s.globalAlpha = 1; s.clearRect(0, 0, w, h);
      return s;
    }
    // fill a whole canvas with a texture repeated across, slid by ox and stretched to sw by sh: one fill, so it also works
    // as a mask ('destination-in' clears whatever a drawn image does not cover)
    const pats = new WeakMap();
    function tileFill(c, img, ox, sw, sh) {
      let m = pats.get(c); if (!m) pats.set(c, (m = new Map()));
      let p = m.get(img); if (!p) m.set(img, (p = c.createPattern(img, "repeat")));
      c.save(); c.translate(mod(ox, sw), 0); c.scale(sw / img.width, sh / img.height); c.fillStyle = p;
      c.fillRect(-img.width, 0, img.width * (2 + c.canvas.width / sw), img.height * (c.canvas.height / sh + 0.01)); c.restore();
    }
    // the game's three glows (violet top right, blue bottom left, plum bottom right) at a point of the sky (heights, y up)
    function glowAt(ux, vy, asp, o) {
      const gV = bl(ux - 0.74 * asp, vy - 1.06, 0.62 * asp, 0.66), gB = bl(ux - 0.02 * asp, vy + 0.06, 0.52 * asp, 0.64), gM = bl(ux - 0.98 * asp, vy + 0.04, 0.40 * asp, 0.52);
      o[0] = 0.30 * gV + 0.1275 * gB + 0.276 * gM; o[1] = 0.22 * gV + 0.255 * gB + 0.102 * gM; o[2] = 0.66 * gV + 0.459 * gB + 0.24 * gM;
    }
    const JOBS2 = {
      // the night: the game's gradient, its glows at their faintest and the band of unresolved stars
      night(w, h) {
        const asp = w / h, q = [0, 0, 0];
        return job(w, h, (x, y, o) => {
          const ux = (x + 0.5) / h, vy = 1 - (y + 0.5) / h, t = sstep(0.2, 1, vy);
          glowAt(ux, vy, asp, q);
          const d = (ux - 0.5 * asp) * -0.387 + (vy - 0.5) * 0.922, band = Math.exp(-((d / 0.2) ** 2)) * 0.08;
          o[0] = 0.027 + 0.023 * t + q[0] * 0.05 + 0.20 * band; o[1] = 0.024 + 0.016 * t + q[1] * 0.05 + 0.18 * band; o[2] = 0.051 + 0.054 * t + q[2] * 0.05 + 0.32 * band;
        });
      },
      glow(w, h) { const asp = w / h; return job(w, h, (x, y, o) => { glowAt((x + 0.5) / h, 1 - (y + 0.5) / h, asp, o); o[0] = Math.min(1, o[0]); o[1] = Math.min(1, o[1]); o[2] = Math.min(1, o[2]); }); },
      // the gas, folded twice (as the shader's), as much as there is at each point; it wraps across the sky's width
      cloud(w, h) {
        const P = Math.max(1, Math.round(1.5 * (w / h))), k = P / w;
        return job(w, h, (x, y, o) => {
          const s = (x + 0.5) * k, t = (y + 0.5) * k;
          const wx = pfbm(s, t, P, 256, 3, 1), wy = pfbm(s + 2.6, t + 0.65, P, 256, 3, 2);
          const n = pfbm(s + 1.6 * wx, t + 1.6 * wy, P, 256, 5, 3);
          const fil = Math.pow(1 - Math.abs(2 * pfbm(2 * s + 2.6 * wx, 2 * t + 2.6 * wy, 2 * P, 256, 3, 4) - 1), 7);
          const cl = sstep(0.30, 0.88, n);
          o[0] = o[1] = o[2] = 1; o[3] = clamp((0.24 * cl + 0.34 * fil * (0.3 + cl)) / 0.7);
        });
      },
      // BLUE at one moment: the drifting lens of clear light and the caustic network through it, together (they wrap
      // across the sky's width: a whole number of the network's tiles fits it); three moments cross-fade as it shimmers
      blue(w, h, t) {
        const P = Math.max(1, Math.round(0.8 * (w / h))), k = P / w, nT = Math.max(1, Math.round(w / (1.5 * h))), tp = w / nT;   // a little coarser than the shader's, so its threads survive the small size
        return job(w, h, (x, y, o) => {
          const lens = sstep(0.30, 0.80, pfbm((x + 0.5) * k, (y + 0.5) * k + 3, P, 256, 3, 41));
          const ca = causticAt(((x + 0.5) / tp) * TAU - 250, ((y + 0.5) / tp) * TAU - 250, t) * (0.25 + 0.75 * lens) * 0.46;
          addPx(o, (0.030 * lens + 0.63 * ca) / 0.6, (0.070 * lens + 0.855 * ca) / 0.6, (0.16 * lens + ca) / 0.6);
        });
      },
      // White's fan of even rays from below the middle of the horizon; hard is the rigid shadow's sharper fan
      fan(w, h, hard) {
        const asp = w / h, e = hard ? 80 : 30;
        return job(w, h, (x, y, o) => {
          const ux = (x + 0.5) / h - 0.5 * asp, vy = 1 - (y + 0.5) / h, ang = Math.atan2(ux, vy + 0.30);
          o[0] = 1; o[1] = 0.84; o[2] = 0.6;
          o[3] = Math.pow(Math.abs(Math.cos(ang * 6)), e) * sstep(0.9, 0.02, vy) * sstep(1.35, 0.2, Math.abs(ang)) * (vy > -0.02 ? 1 : 0);
        });
      },
      // the wind's veil: long streaks across the sky; it wraps across the width
      veil(w, h) {
        const k = 2 / w;
        return job(w, h, (x, y, o) => {
          const s = (x + 0.5) * k, t = ((y + 0.5) / h) * 4.6;
          const v = sstep(0.5, 0.84, pfbm(s, t + 0.4 * Math.sin(Math.PI * s) + 0.7 * pnoise(s, t * 0.3, 2, 256, 31), 2, 256, 3, 33));
          o[0] = 0.727; o[1] = 0.682; o[2] = 1; o[3] = v;
        });
      },
    };
    // one stage of the painting onto g, all at the moments in tm: 0 the night and the gas, 1 Black, 2 Green, 3 Blue, 4 Red,
    // 5 White, the times outside, the wind and the ripple, 6 the warmth, the haze and the vignette
    function paint2D(g, tm, s, w, h) {
      const w2 = Math.max(2, w >> 1), h2 = Math.max(2, h >> 1), t = tm.clock;
      const LW = X[K.L], LU = X[K.L + 1], LB = X[K.L + 2], LR = X[K.L + 3], LG = X[K.L + 4];
      const fcx = X[K.FOC] * h, fcy = (1 - X[K.FOC + 1]) * h, fhN = 2 * X[K.FOC + 3], fbot = fcy + X[K.FOC + 3] * h;   // the focus, in this canvas's pixels
      g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1;
      if (s === 0) {
        // the night, and the gas carried by the wind (its colour stays where the glows are: the gas is lit by them)
        g.globalCompositeOperation = "copy"; g.drawImage(texture("night", false, () => JOBS2.night(w, h), true).c, 0, 0);
        const glow = texture("glow", false, () => JOBS2.glow(w2, h2)), cloud = glow && texture("cloud", false, () => JOBS2.cloud(w2, h2));
        if (cloud) {
          const c = scratch(w2, h2);
          c.drawImage(glow.c, 0, 0); c.globalCompositeOperation = "destination-in"; tileFill(c, cloud.c, tm.drift * 0.478 * h2, w2, h2);
          g.globalCompositeOperation = "lighter"; g.globalAlpha = Math.min(1, (1.35 - 0.75 * X[K.PEACE]) * 0.42 * fadeOf("cloud")); g.drawImage(tmpC, 0, 0, w2, h2, 0, 0, w, h);
        }
        return;
      }
      if (s === 1) {
        // BLACK: the smoke turning and falling inward round the eye, two copies half a fall apart cross-fading, masked to
        // its reach; its body deepens the night, its folds catch the silver-plum light; the very eye is deeper still
        if (LB > 0.06) {
          const sk = texture("smoke", true, JOBS.smoke);
          if (sk) {
            const bs = clamp(fhN, 0.42, 1), a = LB * fadeOf("smoke"), f = frac(tm.inflow), wa = 1 - Math.abs(2 * f - 1), unit = (h * bs * 4) / sk.S;
            const c = scratch(w, h);
            const copy = (ph, turn, al) => {
              if (al < 0.01) return;
              const z = unit * Math.pow(2, -ph), co = Math.cos(-tm.swirl + turn) * z, sn = Math.sin(-tm.swirl + turn) * z;
              c.setTransform(co, sn / 1.12, -sn, co / 1.12, fcx, fcy); c.globalAlpha = al; c.drawImage(sk.c, -sk.S / 2, -sk.S / 2);
            };
            copy(frac(f + 0.5), 2.4, 1 - wa); copy(f, 0, wa);
            if (!tx.reach || tx.reachCtx !== c) { tx.reachCtx = c; tx.reach = c.createRadialGradient(0, 0, 0, 0, 0, 1); [[0, 0.1], [0.06, 0.6], [0.35, 1], [0.56, 1], [0.8, 0.35], [1, 0]].forEach(([p, v]) => tx.reach.addColorStop(p, `rgba(0,0,0,${v})`)); }
            c.globalCompositeOperation = "destination-in"; c.globalAlpha = 1; c.setTransform(0.75 * h * bs, 0, 0, (0.75 * h * bs) / 1.12, fcx, fcy); c.fillStyle = tx.reach; c.fillRect(-1, -1, 2, 2);
            g.globalCompositeOperation = "source-over"; g.globalAlpha = Math.min(1, a); g.drawImage(tmpC, 0, 0);
            if (!tx.eye) { tx.eye = g.createRadialGradient(0, 0, 0, 0, 0, 1); [[0, 1], [0.35, 0.6], [0.7, 0.13], [1, 0]].forEach(([p, v]) => tx.eye.addColorStop(p, `rgba(3,2,8,${v})`)); }
            g.setTransform(0.3 * h * bs, 0, 0, 0.27 * h * bs, fcx, fcy); g.globalAlpha = 0.3 * a; g.fillStyle = tx.eye; g.fillRect(-1, -1, 2, 2);
            g.setTransform(1, 0, 0, 1, 0, 0);
          }
        }
        return;
      }
      if (s === 2) {
        // GREEN: two curtains along their own folding hems in the open sky (each laid in slanted columns, so the hem is one
        // unbroken line), brighter where a fold turns toward us; they breathe; in shadow they slow and their light hangs longer
        if (LG > 0.06) {
          const cu = texture("curtain", true, JOBS.curtain);
          if (cu) {
            const sG = X[K.SH + 4], a0 = LG * fadeOf("curtain") * 1.25, tpp = cu.Aw / (1.5 * w), amp = Math.max(fhN, 0.5);
            const b0 = (1 - X[K.FOC + 1] + X[K.FOC + 3]) - fhN * (0.40 + 0.23 * fhN);   // the hem's height from the top, in heights
            const cw = Math.max(2, Math.min(Math.ceil(w / 16), Math.floor(cu.M / tpp))), n = Math.ceil(w / cw), ys = new Float32Array(n + 1);
            g.globalCompositeOperation = "lighter";
            for (let kk2 = 0; kk2 < 2; kk2++) {
              const ph = tm.aur * (1 + 0.35 * kk2) + kk2 * 3, breath = 0.7 + 0.3 * Math.sin(t * 0.21 * (1 - 0.85 * sG) + kk2 * 2.4);
              const vs = ((cu.span * h) / cu.Ah) * (1 + 0.3 * kk2 + 0.4 * sG), scroll = ph * 0.225 * w * tpp + kk2 * 173;
              const baseAt = (xm) => b0 - amp * (0.13 * kk2 + 0.055 * Math.sin(xm * 4 + ph * 0.9) + 0.03 * Math.sin(xm * 9.5 - ph * 0.6 + kk2 * 1.3) + 0.05 * (CH.noise(xm * 2.6 + kk2 * 7, ph * 0.2) - 0.5));
              for (let i = 0; i <= n; i++) ys[i] = h * baseAt((i * cw) / w);
              for (let i = 0; i < n; i++) {
                const xm = ((i + 0.5) * cw) / w, a1 = xm * 4 + ph * 0.9, a2 = xm * 9.5 - ph * 0.6 + kk2 * 1.3;
                const slope = Math.min(1, Math.abs(0.22 * Math.cos(a1) + 0.285 * Math.cos(a2)));
                const al = a0 * (0.65 + 0.8 * slope) * breath * (1 - 0.3 * kk2);
                if (al < 0.004) continue;
                g.globalAlpha = Math.min(1, al);
                g.setTransform(1, (ys[i + 1] - ys[i]) / cw, 0, 1, i * cw, ys[i] - cu.hemY * vs);
                g.drawImage(cu.c, mod(i * cw * tpp + scroll, cu.Aw), 0, cw * tpp, cu.Ah, 0, 0, cw, cu.Ah * vs);
              }
            }
            g.setTransform(1, 0, 0, 1, 0, 0);
          }
        }
        return;
      }
      if (s === 3) {
        // BLUE: the lens drifts with its caustic network in it; three moments of the network cross-fade (it shimmers),
        // and in shadow a second network wavers beside the first
        if (LU > 0.06) {
          const u = tm.caus * 0.064, wt = [0, 1, 2].map((j) => Math.max(0, 1 - Math.abs(mod(u - j / 3 + 0.5, 1) - 0.5) * 3));
          const ms = [0, 1, 2].map((j) => (j === 0 || wt[j] > 0 ? texture("blue" + j, false, () => JOBS2.blue(w, h, 23 + 1.15 * j)) : null));
          if (ms[0]) {
            const lx = mod(tm.caus * 0.0625 * h, w), fl = fadeOf("blue0");
            for (let j = 1; j < 3; j++) if (!ms[j]) { wt[0] += wt[j]; wt[j] = 0; }
            g.globalCompositeOperation = "lighter";
            const put = (img, ox, oy, al) => { if (al < 0.004) return; g.globalAlpha = Math.min(1, al); g.drawImage(img, ox, oy); g.drawImage(img, ox - w, oy); };
            for (let j = 0; j < 3; j++) put(ms[j] && ms[j].c, lx, 0, wt[j] * 0.56 * LU * fl);
            const sU = X[K.SH + 1];
            if (sU > 0.01) put(ms[0].c, mod(lx + Math.sin(t * 0.9) * 0.08 * h * sU, w), Math.cos(t * 0.67) * 0.08 * h * sU, 0.75 * sU * 0.6 * LU * fl);
          }
        }
        return;
      }
      if (s === 4) {
        // RED: the warm gas (faint); the hearth, a band along the whole floor, bright ember at the floor deepening to red at
        // its top; and in it the coals (two layers of the folded tile shimmering at different speeds, masked to the band);
        // at half size
        if (LR > 0.06) {
          const flick = 0.86 + 0.14 * Math.sin(t * 2.1) * Math.sin(t * 1.37 + 1);
          const cl = texture("cloud", false, () => JOBS2.cloud(w2, h2));
          if (cl) {
            const e = scratch(w2, h2);
            if (!tx.em || tx.emCtx !== e) { tx.emCtx = e; tx.em = e.createLinearGradient(0, h2, 0, 0); tx.em.addColorStop(0, "rgba(209,54,36,1)"); tx.em.addColorStop(0.55, "rgba(209,54,36,0.5)"); tx.em.addColorStop(1, "rgba(209,54,36,0)"); }
            e.fillStyle = tx.em; e.fillRect(0, 0, w2, h2); e.globalCompositeOperation = "destination-in"; tileFill(e, cl.c, tm.drift * 0.478 * h2, w2, h2);
            g.globalCompositeOperation = "lighter"; g.globalAlpha = Math.min(1, 0.1 * LR * (1.35 - 0.75 * X[K.PEACE]) * fadeOf("cloud")); g.drawImage(tmpC, 0, 0, w2, h2, 0, 0, w, h);
          }
          const c = scratch(w2, h2), top = h2 * 0.78;
          if (!tx.band || tx.bandCtx !== c) {
            tx.bandCtx = c;
            tx.band = c.createLinearGradient(0, h2, 0, top); [[0, "243,140,107,1"], [0.3, "200,88,62,0.62"], [0.65, "140,47,31,0.26"], [1, "140,47,31,0"]].forEach(([o, v]) => tx.band.addColorStop(o, `rgba(${v})`));
            tx.bandMask = c.createLinearGradient(0, h2, 0, top - h2 * 0.04); tx.bandMask.addColorStop(0, "rgba(0,0,0,1)"); tx.bandMask.addColorStop(0.55, "rgba(0,0,0,0.7)"); tx.bandMask.addColorStop(1, "rgba(0,0,0,0)");
          }
          const wp = texture("wisp", true, JOBS.wisp);
          if (wp) {
            const tw = (4 / 3.2) * h2, th = (4 / 5) * h2;
            const layer = (sp, fx, fy, al) => {
              const ox = mod(tm.drift * 0.54 * h2 * sp + fx * tw, tw), oy = mod(-t * 0.0412 * h2 * sp + fy * th, th);
              c.globalAlpha = al;
              for (let x = ox - tw; x < w2; x += tw) for (let y = oy - th; y < h2; y += th) if (y + th > top - h2 * 0.05) c.drawImage(wp.c, x, y, tw, th);
            };
            c.globalCompositeOperation = "lighter"; layer(1, 0, 0, 0.5 * fadeOf("wisp")); layer(0.62, 0.5, 0.37, 0.3 * fadeOf("wisp"));
            c.globalCompositeOperation = "destination-in"; c.globalAlpha = 1; c.fillStyle = tx.bandMask; c.fillRect(0, 0, w2, h2);
          }
          c.globalCompositeOperation = "lighter"; c.globalAlpha = 0.58; c.fillStyle = tx.band; c.fillRect(0, top, w2, h2 - top);
          g.globalCompositeOperation = "lighter"; g.globalAlpha = Math.min(1, 0.6 * LR * flick * (1 + 0.3 * X[K.SH + 3])); g.drawImage(tmpC, 0, 0, w2, h2, 0, 0, w, h);
        }
        return;
      }
      if (s === 5) {
        // WHITE: dawn along the lower horizon (a bright gold edge, a glow rising through rose) and the fan of even rays from
        // below the open sky's floor; it breathes, and in shadow stops breathing while the rays harden
        if (LW > 0.06) {
          const sW = X[K.SH], br = 1 + 0.10 * Math.sin(t * 0.31) * (1 - sW), m = 0.3 + 0.7 * X[K.CONTENT];
          const gold = [0.90 + 0.10 * m, 0.86 - 0.04 * m, 0.74 - 0.24 * m], rose = [0.60 + 0.26 * m, 0.55 + 0.01 * m, 0.66 - 0.16 * m];
          const mixd = gold.map((v, i) => rose[i] + (v - rose[i]) * 0.45);
          const ramp = (col, L) => { const gr = g.createLinearGradient(0, h, 0, h - 4.5 * L * h), rgb = col.map((v) => Math.round(v * 255)).join(","); [0, 1, 2, 3, 4.5].forEach((y) => gr.addColorStop(y / 4.5, `rgba(${rgb},${Math.exp(-y).toFixed(4)})`)); return gr; };
          g.globalCompositeOperation = "lighter";
          g.globalAlpha = Math.min(1, 0.40 * LW * br); g.fillStyle = ramp(gold, 0.022); g.fillRect(0, h - 0.1 * h, w, 0.1 * h);
          const L = 0.11 + 0.10 * LW;
          g.globalAlpha = Math.min(1, 0.22 * LW * br); g.fillStyle = ramp(mixd, L); g.fillRect(0, h - 4.5 * L * h, w, 4.5 * L * h);
          const fan = texture("fan", false, () => JOBS2.fan(w, h, false));
          if (fan) {
            // the fan is baked for the whole sky; it is laid scaled into the open stretch, its apex below that stretch's floor
            const sc = clamp(fhN, 0.2, 1), fa = 0.09 * (1 + sW) * LW * br * fadeOf("fan");
            g.setTransform(sc, 0, 0, sc, fcx - 0.5 * w * sc, fbot - h * sc);
            g.globalAlpha = Math.min(1, fa * (1 - sW)); g.drawImage(fan.c, 0, 0);
            if (sW > 0.01) { const fh2 = texture("fanH", false, () => JOBS2.fan(w, h, true)); if (fh2) { g.globalAlpha = Math.min(1, fa * sW); g.drawImage(fh2.c, 0, 0); } }
            g.setTransform(1, 0, 0, 1, 0, 0);
          }
        }
        // the times outside along the far horizon
        if (X[K.ERA] > 0.01) {
          const key = [eraN, ...[K.E0, K.E1, K.E2].map((o) => [0, 1, 2].map((i) => Math.round(X[o + i] * 40)).join(","))].join("|");
          if (key !== tx.eraKey) {
            tx.eraKey = key; const e = document.createElement("canvas"); e.width = w; e.height = Math.max(2, Math.round(h * 0.34)); const eg = e.getContext("2d");
            const hz = eg.createLinearGradient(0, 0, w, 0), col = (o) => `rgb(${[0, 1, 2].map((i) => Math.round(X[o + i] * 255)).join(",")})`;
            if (eraN >= 3) { hz.addColorStop(0.05, col(K.E0)); hz.addColorStop(0.5, col(K.E1)); hz.addColorStop(0.95, col(K.E2)); } else if (eraN === 2) { hz.addColorStop(0.15, col(K.E0)); hz.addColorStop(0.85, col(K.E1)); } else { hz.addColorStop(0, col(K.E0)); hz.addColorStop(1, col(K.E0)); }
            eg.fillStyle = hz; eg.fillRect(0, 0, w, e.height);
            const vf = eg.createLinearGradient(0, e.height, 0, 0); [0, 1, 2, 3, 3.78].forEach((y) => vf.addColorStop(y / 3.78, `rgba(0,0,0,${Math.exp(-y).toFixed(3)})`));
            eg.globalCompositeOperation = "destination-in"; eg.fillStyle = vf; eg.fillRect(0, 0, w, e.height); tx.eraC = e;
          }
          g.globalCompositeOperation = "lighter"; g.globalAlpha = 0.18 * X[K.ERA]; g.drawImage(tx.eraC, 0, h - tx.eraC.height);
        }
        // strain is wind: the veil of long slanting streaks blowing across, faster than the gas
        const strain = X[K.STRAIN];
        if (strain > 0.004) {
          const vt = texture("veil", false, () => JOBS2.veil(w2, h2));
          if (vt) {
            const ox = mod(tm.drift * 3.73 * h, w);
            g.save(); g.translate(w / 2, h / 2); g.rotate(-VEIL); g.scale(1.3, 1.3); g.translate(-w / 2, -h / 2);
            g.globalCompositeOperation = "lighter"; g.globalAlpha = Math.min(1, 0.33 * strain * fadeOf("veil")); g.drawImage(vt.c, ox, 0, w, h); g.drawImage(vt.c, ox - w, 0, w, h);
            g.restore();
          }
        }
        // the ripple's water film: a glint along the ring
        const rp = ripState();
        if (rp) {
          const cxp = (rp.x * w) / W, cyp = (rp.y * h) / H, R = (rp.R * h) / H;
          g.globalCompositeOperation = "lighter"; g.strokeStyle = "rgba(128,153,230,1)"; g.lineWidth = h * 0.08; g.globalAlpha = 0.12 * rp.s;
          g.beginPath(); g.arc(cxp, cyp, R, 0, TAU); g.stroke();
          g.strokeStyle = "rgba(184,204,255,1)"; g.lineWidth = Math.max(1, h * 0.012); g.globalAlpha = 0.16 * rp.s;
          g.beginPath(); g.arc(cxp, cyp, R + h * 0.014, 0, TAU); g.stroke();
        }
        return;
      }
      // unsettled air is milky; the warmth of the light (satisfaction: a warm or cool cast, and a warm or cool rim along
      // the horizon) and the vignette (Black deepens it into velvet; in shadow, ruthless, it eats a little more at the edges)
      const ct = X[K.CONTENT], pe = X[K.PEACE], sB = X[K.SH + 2];
      g.globalCompositeOperation = "lighter"; g.globalAlpha = 1;
      g.fillStyle = `rgb(${Math.round(0.034 * (1 - pe) * 255 * 0.9)},${Math.round(0.030 * (1 - pe) * 255 * 0.9)},${Math.round(0.05 * (1 - pe) * 255 * 0.9)})`; g.fillRect(0, 0, w, h);
      const rimC = [0.030 + 0.12 * ct, 0.060 + 0.028 * ct, 0.110 - 0.074 * ct].map((v) => Math.round(v * 0.55 * 255)).join(",");
      const rim = g.createLinearGradient(0, h, 0, h * 0.76); [0, 1, 2, 4].forEach((y) => rim.addColorStop(y / 4, `rgba(${rimC},${Math.exp(-y).toFixed(3)})`));
      g.fillStyle = rim; g.fillRect(0, h * 0.76, w, h * 0.24);
      const vg = Math.min(0.62, 0.30 + 0.22 * LB + 0.09 * sB), a = 0.32 - 0.06 * sB, b = 0.90;
      const tint = [0.86 + 0.30 * ct, 0.95 + 0.07 * ct, 1.16 - 0.32 * ct], tm2 = Math.max(...tint), tn = tint.map((v) => v / tm2);
      const gr = g.createRadialGradient(0, 0, 0, 0, 0, 1);
      [0, a, a + (b - a) * 0.25, a + (b - a) * 0.5, a + (b - a) * 0.75, b, 1].forEach((p) => { const f = 1 - sstep(a, b, p) * vg; gr.addColorStop(Math.min(1, p), `rgb(${tn.map((v) => Math.round(v * f * 255)).join(",")})`); });
      g.globalCompositeOperation = "multiply"; g.globalAlpha = 1; g.fillStyle = gr;
      g.setTransform(w, 0, 0, h / 1.1, 0.5 * w, 0.5 * h); g.fillRect(-0.5, -0.55, 1, 1.1); g.setTransform(1, 0, 0, 1, 0, 0);
      g.globalCompositeOperation = "source-over";
    }
    // The pictures: three canvases, the one before, the one now and the one being painted, a stage or two a frame (each
    // stage is about one full-size drawing). What shows is the picture before dissolving into the one now as the next is
    // painted, so the sky moves smoothly however few pictures a second the machine can afford.
    const STAGES = 7;
    let bufs = null, iPrev = 0, iCur = 1, iBack = 2, stageI = 0;
    function drawField2D(tm, all) {
      const w = fieldC.width, h = fieldC.height;
      sync = !!all && CH.speed() === 0;
      if (!bufs || bufs[0].width !== w || bufs[0].height !== h) {
        bufs = [0, 1, 2].map(() => { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; });
        all = true;
      }
      if (all) {
        const b = bufs[iBack].getContext("2d");
        missing = false;
        for (let s = 0; s < STAGES; s++) paint2D(b, tm, s, w, h);
        // the still picture waits for its textures (only the very first frame shows what there is, so it is never empty)
        if (sync && missing && shown) return false;
        iPrev = iCur = iBack; iBack = (iCur + 1) % 3; stageI = 0;
      } else {
        const c0 = performance.now(), b = bufs[iBack].getContext("2d");
        do {
          if (stageI === 0) tmB = tm;
          paint2D(b, tmB, stageI, w, h);
          if (++stageI === STAGES) { stageI = 0; iPrev = iCur; iCur = iBack; iBack = 3 - iPrev - iCur; break; }
        } while (performance.now() - c0 < 0.5);
      }
      f2.setTransform(1, 0, 0, 1, 0, 0);
      f2.globalCompositeOperation = "copy"; f2.globalAlpha = 1; f2.drawImage(bufs[iPrev], 0, 0);
      shown = true;
      const k = all ? 1 : stageI / STAGES;
      if (k > 0.002 && iCur !== iPrev) { f2.globalCompositeOperation = "source-over"; f2.globalAlpha = k; f2.drawImage(bufs[iCur], 0, 0); }
      f2.globalCompositeOperation = "source-over"; f2.globalAlpha = 1;
      return !(sync && missing);
    }

    /* ---------- the frame: ease the numbers, advance the clocks, draw ---------- */
    const costs = [], parts = [];   // the cost of each of the last 1500 frames (ms), and of its field, sparks and ink
    function frame(now, dt) {
      nowS = now;
      // the panels may come and go between states too (a moment opens and waits): read them again once a second
      if (typeof opts.clear === "string" && now - layoutAt > 1) { layoutAt = now; if (relayout()) { built = ""; measure(); } }
      const sp = CH.speed();
      if (sp === 0) {
        // motion off: no animation at all; one still frame per change, always the same for the same state
        if (!dirty) return;
        const c0 = performance.now();
        X.set(T); V.fill(0); rip = null;
        const tm = STILL;
        clock = tm.clock; drift = tm.drift; swirl = tm.swirl; stamp = now;
        const done = G ? (drawFieldGL(tm, now, true), true) : f2 ? drawField2D(tm, true) : true;
        inkForce = true; drawSparks(0, true); drawInk(0, now); pushWet();
        dirty = !done;   // the Canvas2D still waits for its textures: try again next frame
        force = false;
        costs.push(performance.now() - c0); parts.push([0, 0, 0]); if (costs.length > 1500) { costs.shift(); parts.shift(); }
        return;
      }
      const c0 = performance.now();
      settle(X, V, T, dt, easeT);
      const d = dt * sp;
      clock += d;
      // the clocks of motion: wind carries the gas and the stars (strain makes it blow), Black's smoke turns and falls
      // inward, the aurora folds (slowing to stillness in Green's shadow), the shimmer drifts
      drift += d * (0.0022 + 0.05 * Math.pow(X[K.STRAIN], 1.4));
      swirl += d * (0.010 + 0.014 * X[K.L + 2]);
      inflow += d * (0.012 + 0.02 * X[K.L + 2]);
      aur += d * 0.06 * (1 - 0.85 * X[K.SH + 4]);
      caus += d * 0.05;
      const tm = { clock, drift, swirl, inflow, aur, caus };
      stamp = now;
      if (G) drawFieldGL(tm, now, force); else if (f2) drawField2D(tm, force);
      force = false;
      const c1 = performance.now();
      drawSparks(d, false);
      const c2 = performance.now();
      drawInk(d, now);
      pushWet();
      dirty = false;
      const c3 = performance.now();
      costs.push(c3 - c0); parts.push([c1 - c0, c2 - c1, c3 - c2]); if (costs.length > 1500) { costs.shift(); parts.shift(); }
    }

    /* ---------- W1's reading: what the sky shows of them, on hover (or a tap) wherever no panel covers the sky ---------- */
    // Each colour that shows at all (a twentieth of the person or more), strongest first, with what it paints and its real
    // share; then the weather (satisfaction, peace and strain, as the character sheet has them), the ink's wetness, the times
    // outside and any shadow. It opens over the open sky only (isSky: the panels keep their own tips) in the page's one #tip:
    // a mouse reads it by hovering, a finger or pen by tapping, and a tapped reading closes by itself after 3.2 s, as the
    // page's own tapped tips do. It belongs to the pointer, as the life line's does (showTipAt), so the page's hover
    // handling leaves it alone; it closes only while it is still the one showing. It stays shut while a press lays ink and
    // after a drawn stroke, so drawing is never covered.
    const weather = () => { const S = lastS || {}; return [clamp(S.content ?? 0), clamp(S.peace ?? 0), clamp((S.stress || 0) / 1.5)]; };
    const LOOKS = { W: "dawn and a rose window", U: "constellations, clear light", B: "smoke turning inward", R: "a hearth, a brushstroke", G: "aurora and rising lights" };
    function reading() {
      const S = lastS;
      if (!S || !S.w) return "";
      const who = CH.esc(S.name || (CH.life && CH.life.name) || "them");
      const rows = CH.COLORS.map((c, i) => [c, S.w[i] || 0]).sort((a, b) => b[1] - a[1]).filter(([, v]) => v >= 0.05).map(([c, v]) => [CH.NAME[c], `${LOOKS[c]} · ${CH.pct(v)}`]);
      const v = weather(), sh = shadowOf(S);
      let foot = `Strain ${CH.pct(v[2])} blows wind through it; peace ${CH.pct(v[1])} clears the haze; satisfaction ${CH.pct(v[0])} warms the light. The ink is ${CH.pct(wetOf(S))} wet.`;
      const era = S.world_era && CH.lettersOf(S.world_era.letters);
      if (era && era.length) foot += ` The far horizon takes the colours of the times outside${S.world_era.name ? ` (${CH.esc(S.world_era.name)})` : ""}.`;
      CH.COLORS.forEach((c, i) => { if (sh[i] > 0.3) foot += ` ${CH.NAME[c]}'s sky shows its shadow: ${CH.SHADOW[c]}.`; });
      return CH.tipBox("The sky is their mind", `Each colour paints its own sky, as strongly as it lives in ${who}.`, rows, foot);
    }
    let tipHtml = "", tipShut = 0, readAt = 0, readHtml = "";
    const readingNow = () => { const t = performance.now(); if (!readHtml || t - readAt > 250) { readAt = t; readHtml = reading(); } return readHtml; };
    const tipMine = () => !!tipHtml && tipOwner === "line" && tipEl.innerHTML === tipHtml;
    function readOpen(e) {
      if (down || inkDrag || !isSky(e.target)) return false;
      const html = readingNow(); if (!html) return false;
      showTipAt(html, e.clientX, e.clientY); tipHtml = tipEl.innerHTML;
      return true;
    }
    function readClose() { clearTimeout(tipShut); if (tipMine()) CH.hideTip(); tipHtml = ""; }
    const onHover = (e) => { if (e.pointerType === "mouse" && !readOpen(e) && tipHtml) readClose(); };
    const onTap = (e) => { if (e.pointerType !== "mouse") setTimeout(() => { if (readOpen(e)) { clearTimeout(tipShut); tipShut = setTimeout(readClose, 3200); } }, 0); };
    const onOut = (e) => { if (!e.relatedTarget && tipHtml) readClose(); };     // the pointer left the window
    stage.addEventListener("pointermove", onHover, { passive: true });
    stage.addEventListener("pointerup", onTap, { passive: true });
    stage.addEventListener("pointerout", onOut, { passive: true });

    /* ---------- wiring ---------- */
    measure();
    const ro = "ResizeObserver" in window ? new ResizeObserver(() => measure()) : null;
    if (ro) ro.observe(host);
    // the page changed a CSS scale above the sky (ResizeObserver does not see transforms): measure again
    const offResize = CH.on("resize", measure);
    const offFrame = CH.frame(frame, host);
    const offMotion = CH.on("motion", (m) => {
      host.dataset.motion = m;
      if (m === "off") { ink.marks.forEach((b) => { b.still = true; }); meteors.length = 0; bits.length = 0; }
      // back in motion, a still mark left while motion was off starts to fade like any dried bloom
      else ink.marks.forEach((b) => { if (b.still) { b.still = false; b.born = clock - b.hold; b.dryFrom = clock - 99; } });
      dirty = true; force = true; inkForce = true;
    });
    host.dataset.motion = CH.motion();

    const inst = {
      update,
      setLiving,
      destroy() {
        offFrame(); offMotion(); offResize(); if (ro) ro.disconnect();
        stage.removeEventListener("pointerdown", onDown); stage.removeEventListener("pointermove", onMove);
        window.removeEventListener("pointerup", onUp); window.removeEventListener("pointercancel", onUp); stage.removeEventListener("selectstart", onSelect);
        stage.removeEventListener("pointermove", onHover); stage.removeEventListener("pointerup", onTap); stage.removeEventListener("pointerout", onOut);
        readClose();
        if (primary === inst) primary = null;
        dropOverlays();
        const defs = document.getElementById("chs-atmos-defs"); if (defs) defs.remove();
        wetHost.style.removeProperty("--wet");
        if (G && gt) [gt.nA, gt.nB, gt.fA, gt.fB].forEach((t) => G.drop(t));
        if (G) { const lose = G.gl.getExtension("WEBGL_lose_context"); if (lose) lose.loseContext(); }
        [fieldC, sparks, crisp].forEach((c) => c.remove());
        host.classList.remove("chs-atmos");
      },
      // B1 hooks for a host: drop a bloom at a point in the host (CSS px) or on the screen, send the ripple yourself
      bloom: (x, y, cols) => { ink.drop(x, y, cols && cols.length ? cols : inks, clamp(X[K.WET]), clock, motionOf() === "off", inkS); dirty = true; },
      bloomClient: (x, y, cols) => { const [lx, ly] = CH.local(host, { clientX: x, clientY: y }); inst.bloom(lx, ly, cols); },
      ripple: () => { lastRip = -99; ripple(); },
      relayout: () => { built = ""; measure(); },
      wetNow: () => X[K.WET],
      inks: () => inks.slice(),
      layout: () => ({ gaps: lay.gaps.map((g) => Object.assign({}, g)), focus: Object.assign({}, lay.focus), full: lay.full }),
      // what the last frames cost (ms, performance.now() around this sky's draw): mean, median, 95th percentile, the worst,
      // the mean of each part, the field's rate and, where the browser can measure it, the GPU's time; reset starts over
      stats: (reset) => {
        if (reset) { costs.length = 0; parts.length = 0; if (gt) gt.gpu.length = 0; return { n: 0 }; }
        const a = costs.slice().sort((p, q) => p - q), n = a.length;
        const part = (i) => parts.reduce((s, v) => s + v[i], 0) / Math.max(1, parts.length);
        const gpu = gt && gt.gpu.length ? gt.gpu.reduce((s, v) => s + v, 0) / gt.gpu.length : null;
        return n ? { n, mean: a.reduce((s, v) => s + v, 0) / n, p50: a[n >> 1], p95: a[Math.floor(n * 0.95)], max: a[n - 1], field: part(0), sparks: part(1), ink: part(2), renderer: G ? "webgl" : "canvas", fieldHz: G ? rateNow : null, gpu, gpuTimer: !!(G && G.timer), ease: easeT } : { n: 0, renderer: G ? "webgl" : "canvas" };
      },
    };
    primary = inst;
    if (opts.state) update(opts.state);
    return inst;
  }

  /* ---------------- the piece: the sky on the game page ---------------- */
  // A fixed layer behind #app (before it, so every panel stays above). The figures keep clear of these panels; hidden
  // ones count for nothing, so the moment window counts only while it shows.
  const CLEAR = "header.bar, #line, #stage, #hud, #transport, #evwrap .ev";
  // before any life (the start screen) the sky is an even life's: every colour at a fifth, settled and content
  const EVEN = { w: [0.2, 0.2, 0.2, 0.2, 0.2], age: 20, content: 0.6, peace: 0.6, stress: 0 };
  let sky = null, host = null, offs = [];
  function takeDown() {
    offs.forEach((f) => f()); offs = [];
    if (sky) sky.destroy();
    if (host) host.remove();
    sky = null; host = null;
    delete document.body.dataset.lvSky;
  }
  CH.piece("sky", {
    order: 10,
    mount(ctx) {
      const app = document.getElementById("app");
      if (!app) return false;
      host = document.createElement("div"); host.className = "lv-sky"; host.setAttribute("aria-hidden", "true");
      app.before(host);
      // the open sky under the pointer: the page itself, #app and main between the panels, or the sky's own layers
      const main = app.querySelector(":scope > main");
      const isSky = (t) => t === document.documentElement || t === document.body || t === app || (!!main && t === main) || host.contains(t);
      try { sky = mount(host, { stage: document, clear: CLEAR, isSky, state: ctx.state() || EVEN }); } catch (e) { takeDown(); throw e; }
      document.body.dataset.lvSky = "on";                // today's night, glow and sigil step aside (10-atmos.css)
      offs = [
        CH.on("living", (on) => { if (sky) sky.setLiving(on); }),
        // an outcome that moves their colours a point or more sends one ripple through the sky (dw is in points of 100)
        CH.on("outcome", (x) => {
          if (!sky || !x || x.quiet || CH.speed() === 0) return;
          const moved = ((x.res && x.res.dw) || []).reduce((t, v) => t + Math.abs(v || 0), 0);
          if (moved >= 1) sky.ripple();
        }),
      ];
    },
    update(S, how) { if (sky) sky.update(S, how); },
    destroy: takeDown,
    // the sky's own reading of what it shows, for the release's cost and layout checks
    stats: (reset) => (sky ? sky.stats(reset) : null),
    layout: () => (sky ? sky.layout() : null),
  });
})();
