// The engine under the browser's own Python (Pyodide 0.27.7, 32-bit wasm: numpy's np.intp is int32), run in Node.
// CPython tests cannot see what fails only there, such as an int64 index array numpy will not cast to int32 'safe'.
// Runs test/wasm_check.py in the prototype folder (mounted at /w); it lists every such spot and must find none.
//   node test/wasm_check.js <pyodide package dir (pyodide.js, python_stdlib.zip ...)> <numpy wheel> [lives] [age]
const path = require('path'), fs = require('fs');
const [pdir, wheel, lives, age] = process.argv.slice(2);
const { loadPyodide } = require(path.resolve(pdir, 'pyodide.js'));
(async () => {
  const py = await loadPyodide({ indexURL: path.resolve(pdir) + '/' });
  await py.loadPackage(path.resolve(wheel));
  py.FS.mkdir('/w'); py.FS.mount(py.FS.filesystems.NODEFS, { root: path.resolve(__dirname, '..') }, '/w');
  py.setStdout({ batched: (s) => console.log(s) }); py.setStderr({ batched: (s) => console.error(s) });
  py.globals.set('ARGS', [lives || '2', age || '30']);
  py.runPython("import os, sys; os.chdir('/w'); sys.path.insert(0, '/w'); sys.argv = ['wasm_check.py'] + list(ARGS)");
  try { py.runPython(fs.readFileSync(path.join(__dirname, 'wasm_check.py'), 'utf8')); } catch (e) { console.log(String(e).slice(-3000)); process.exitCode = 1; }
})();
