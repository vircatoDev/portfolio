#!/usr/bin/env python3
"""Serve the portfolio on this computer only. No third-party dependencies."""
import argparse
import functools
import http.server
from pathlib import Path
import threading
import webbrowser

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--open', action='store_true', help='Open the site in your browser')
args = parser.parse_args()
root = Path(__file__).resolve().parent / 'dist'

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

handler = functools.partial(NoCacheHandler, directory=str(root))
try:
    server = http.server.ThreadingHTTPServer(('127.0.0.1', args.port), handler)
except OSError as error:
    parser.exit(1, f'Cannot start on port {args.port}: {error}\nTry: python3 serve.py --port 8766\n')
url = f'http://127.0.0.1:{args.port}/'
print(f'Portfolio is ready: {url}\nPress Ctrl+C to stop.', flush=True)
if args.open:
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('\nServer stopped.')
finally:
    server.server_close()
