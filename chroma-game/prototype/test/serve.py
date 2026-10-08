import http.server, sys, functools, os
CSP = os.environ.get("CSP", "")
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".wasm": "application/wasm", ".py": "text/plain", ".whl": "application/zip"}
    def end_headers(self):
        if CSP and self.path.split("?")[0] in ("/", "/page.html"):
            self.send_header("Content-Security-Policy", CSP)
        super().end_headers()
    def log_message(self, *a): pass
os.chdir(sys.argv[2])
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
