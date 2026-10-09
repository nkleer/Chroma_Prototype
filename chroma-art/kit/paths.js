// Shared-folder paths for the Node scripts, read from chroma-env/paths.py (backend plan item 6), so every path still has
// one home. The root is CHROMA_ROOT when it is set, otherwise the tree this file sits in, as for paths.py.
//   const { P, path } = require('../paths');   // from kit/glyph
//   path('art_old_icons', 'icons.json')        // an absolute path
const { execFileSync } = require('child_process');
const nodePath = require('path');
const ROOT = process.env.CHROMA_ROOT || nodePath.resolve(__dirname, '..', '..');
const P = JSON.parse(execFileSync('python3', ['-B', '-c',
  'import json, sys; sys.path.insert(0, sys.argv[1]); from paths import P; print(json.dumps(P))', nodePath.join(ROOT, 'chroma-env')],
  { encoding: 'utf8', env: { ...process.env, CHROMA_ROOT: ROOT } }));
const path = (name, ...parts) => {
  if (!(name in P)) throw new Error(`chroma-env/paths.py has no name "${name}"`);
  return nodePath.join(P[name], ...parts);
};
module.exports = { P, path };
