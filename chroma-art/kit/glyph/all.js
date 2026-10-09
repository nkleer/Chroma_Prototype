const FILES = ['glyphs', 'glyphs_tags', 'glyphs_needs', 'glyphs_acts', 'glyphs_opts_a', 'glyphs_opts_b', 'glyphs_o1', 'glyphs_o2', 'glyphs_o3', 'glyphs_o4', 'glyphs_o5', 'glyphs_o6', 'glyphs_o7', 'glyphs_p1', 'glyphs_p2', 'glyphs_w42'];
module.exports = { GLYPHS: FILES.flatMap((f) => require(`./${f}`).GLYPHS) };
