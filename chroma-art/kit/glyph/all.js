// Every glyph file, in sprite order. build_icons.js and page2.js read this list, so a new file is added here only.
const FILES = ['glyphs', 'glyphs_tags', 'glyphs_needs', 'glyphs_acts', 'glyphs_opts_a', 'glyphs_opts_b', 'glyphs_o1', 'glyphs_o2', 'glyphs_o3', 'glyphs_o4', 'glyphs_o5', 'glyphs_o6', 'glyphs_o7', 'glyphs_p1', 'glyphs_p2', 'glyphs_w42', 'glyphs_shadow'];
module.exports = { FILES, GLYPHS: FILES.flatMap((f) => require(`./${f}`).GLYPHS) };
