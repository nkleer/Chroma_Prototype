"""Release's v25 readers on the shipped set (records/v25/scope.md, "The shipped settings"; records/v25/jobs.md).

With CHROMA_SHIP=v25 and this folder on PYTHONPATH, every Python process lays the v25 switches of engine.SHIP_V25 over
engine.DEFAULT when the engine loads, and sets engine.SHIP_V25_BATCH's flags on batch when batch loads (a flag named in
CHROMA_BATCH_OFF stays off). The outer world stays as each reader sets it, as v24's rows were read; the realm stays
DEFAULT's "earth". Old readers that copy DEFAULT then play v25 as shipped with no change to them. Inert without
CHROMA_SHIP. Each patch appends a line to CHROMA_SHIP_LOG when that is set, so a job can show the hook ran."""
import os

if os.environ.get("CHROMA_SHIP") == "v25":
    import importlib.abc
    import importlib.machinery
    import sys

    BATCH = dict(AIMS=True, FOOT=True, WORLD_ANSWERS=True, FIELDS=True, LAND=True, NATIONAL=True, CLASH_MOMENTS=True,
                 SEEK_MOMENTS=True)   # engine.SHIP_V25_BATCH on 225679d; checked against the engine when it loads
    KEEP = ("world", "realm")

    def _log(what):
        p = os.environ.get("CHROMA_SHIP_LOG")
        if p:
            with open(p, "a") as f:
                f.write(f"{os.getpid()} {what} {sys.argv[0] if sys.argv else ''}\n")

    def _patch(name, m):
        if name == "engine":
            ship = getattr(m, "SHIP_V25", None)
            if ship is None or getattr(m, "SHIP_V25_BATCH", None) != BATCH:
                raise SystemExit("ship_hook: this engine has no SHIP_V25, or its SHIP_V25_BATCH is not the hook's")
            m.DEFAULT.update({k: v for k, v in ship.items() if k not in KEEP})
            _log("engine DEFAULT += SHIP_V25 (" + ",".join(k for k in ship if k not in KEEP) + ")")
        elif name == "batch":
            off = {x.strip() for x in os.environ.get("CHROMA_BATCH_OFF", "").split(",") if x.strip()}
            for k, v in BATCH.items():
                if k not in off:
                    setattr(m, k, v)
            _log("batch flags " + ",".join(k for k in BATCH if k not in off))

    class _Ship(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name not in ("engine", "batch"):
                return None
            spec = importlib.machinery.PathFinder.find_spec(name, path)
            if spec is None or spec.loader is None or not hasattr(spec.loader, "exec_module"):
                return spec
            run = spec.loader.exec_module

            def exec_module(module, run=run, name=name):
                run(module)
                _patch(name, module)
            spec.loader.exec_module = exec_module
            return spec

    sys.meta_path.insert(0, _Ship())
