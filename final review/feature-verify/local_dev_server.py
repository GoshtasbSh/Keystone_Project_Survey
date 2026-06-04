"""Faithful local dev server for KeyStone — bypasses `vercel dev`'s broken
Python toolchain. Serves the static surfaces per vercel.json rewrites and
dispatches /api/<name> to the REAL api/<name>.py handler classes, using the
project .venv interpreter (which has all deps). Read-only on disk; the api
handlers talk to the same Supabase/.env as production.

Run with the project's venv python:
  .venv/bin/python /tmp/keystone_local_server.py 3002
"""
import importlib.util
import mimetypes
import os
import pathlib
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = pathlib.Path("/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project")
API_DIR = ROOT / "api"
FIELD = ROOT / "keystone_field_web"
STATIC = ROOT / "static"

# ── load .env into os.environ (so api handlers see SUPABASE_* etc.) ──────
for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    os.environ.setdefault(k.strip(), v.strip())

sys.path.insert(0, str(API_DIR))

_MOD_CACHE = {}


def load_api(name):
    if name in _MOD_CACHE:
        return _MOD_CACHE[name]
    path = API_DIR / (name + ".py")
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("api_" + name.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _MOD_CACHE[name] = mod
    return mod


def serve_file(self, fs_path: pathlib.Path) -> bool:
    if fs_path.is_dir():
        fs_path = fs_path / "index.html"
    if not fs_path.exists():
        # cleanUrls: try appending .html
        alt = fs_path.with_suffix(".html")
        if alt.exists():
            fs_path = alt
        else:
            return False
    ctype = mimetypes.guess_type(str(fs_path))[0] or "application/octet-stream"
    data = fs_path.read_bytes()
    self.send_response(200)
    self.send_header("Content-Type", ctype)
    self.send_header("Content-Length", str(len(data)))
    self.send_header("Cache-Control", "no-store")
    self.end_headers()
    self.wfile.write(data)
    return True


def resolve_static(path: str):
    """Map a request path to a file per vercel.json rewrites."""
    if path in ("/", "/field", "/field/"):
        return FIELD / "index.html"
    if path in ("/login", "/keystone_field_web/login"):
        return FIELD / "login.html"
    if path in ("/admin", "/keystone_field_web/admin"):
        return FIELD / "admin.html"
    if path in ("/manifest.json",):
        return FIELD / "manifest.json"
    if path in ("/sw.js",):
        return FIELD / "sw.js"
    if path in ("/dashboard", "/dashboard/"):
        return STATIC / "index.html"
    if path.startswith("/dashboard/"):
        return STATIC / path[len("/dashboard/"):]
    if path.startswith("/static/"):
        return STATIC / path[len("/static/"):]
    if path.startswith("/keystone_field_web/"):
        return FIELD / path[len("/keystone_field_web/"):]
    if path.startswith("/field/"):
        return FIELD / path[len("/field/"):]
    # bare asset (e.g. /js/dashboard.js referenced relatively) — try static then field
    cand = STATIC / path.lstrip("/")
    if cand.exists():
        return cand
    return FIELD / path.lstrip("/")


class Proxy(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _dispatch_api(self):
        name = urlparse(self.path).path[len("/api/"):].strip("/")
        name = name.split("/")[0]
        mod = load_api(name)
        if mod is None or not hasattr(mod, "handler"):
            self.send_error(404, "no api/%s" % name)
            return
        H = mod.handler
        inst = H.__new__(H)
        inst.rfile = self.rfile
        inst.wfile = self.wfile
        inst.headers = self.headers
        inst.path = self.path
        inst.command = self.command
        inst.client_address = self.client_address
        inst.connection = self.connection
        inst.server = self.server
        inst.request_version = self.request_version
        inst.requestline = self.requestline
        inst.protocol_version = "HTTP/1.1"
        inst.close_connection = True
        method = getattr(inst, "do_" + self.command, None)
        if method is None:
            self.send_error(405)
            return
        try:
            method()
        except Exception as e:  # noqa: BLE001
            sys.stderr.write("[api/%s] %s: %s\n" % (name, type(e).__name__, e))
            try:
                self.send_error(500, str(e))
            except Exception:
                pass

    def _handle(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self._dispatch_api()
            return
        fs = resolve_static(parsed.path)
        if not serve_file(self, fs):
            self.send_error(404, "not found: %s" % parsed.path)

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.command, self.path))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3002
    srv = ThreadingHTTPServer(("127.0.0.1", port), Proxy)
    print("KeyStone local server on http://localhost:%d" % port, flush=True)
    srv.serve_forever()
