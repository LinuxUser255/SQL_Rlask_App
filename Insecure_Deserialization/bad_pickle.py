#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import base64
import pickle

# bad pickle
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if cookies.get('username'):
            username = pickle.loads(base64.b64decode(cookies.get('username').value))
        else:
            username = 'Linux Chad'
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Arch</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1> I use Arch btw- %s</h1>" % username, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer(('0.0.0.0', 1337), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
