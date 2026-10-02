from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import os

import socket

class ReusableHTTPServer(HTTPServer):
    # TÄMÄ RIVI KORJAA "Address already in use" -ONGELMAN:
    allow_reuse_address = True

# Tilanseuranta ja aikaleima
viritetty = False
aikaleima=0

class LukkoProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global viritetty,aikaleima
        if self.path == "/avaa" or self.path == "/":
          if (int(time.time())-aikaleima)>20: viritetty=False
          try:
              if not viritetty:
                aikaleima=int(time.time())
                os.system('ssh -X tnoko@$(cat ~/KOTIKONE) -p 7732 "curl Lukko/au"')
                viritetty = True
                response_data = {
                    "message": "VIRITETTYYY!",
                    "error": ""
                    }
              else:
                os.system('ssh -X tnoko@$(cat ~/KOTIKONE) -p 7732 "curl Lukko/ki"')
                viritetty = False
                response_data = {
                    "message": "AVATTUUU!",
                    "error": ""
                    }
          except:
                viritetty = False
                response_data = {
                        "message": "VIRHEE",
                        "error": ""
                    }
        response_bytes = json.dumps(response_data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

HOST = "0.0.0.0"
PORT = 9094

httpd = ReusableHTTPServer((HOST, PORT), LukkoProxyHandler)
print(f"Palvelin käynnissä portissa {PORT}...")
httpd.serve_forever()

