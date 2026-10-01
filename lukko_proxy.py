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
            URL1 = "http://89.27.95.8:7981"
            URL2 = "http://192.168.1.117"
            if os.system('ping -c 1 192.168.1.117')==0:
                  URL1,URL2=URL2,URL1
            if not viritetty:
                aikaleima=int(time.time())
                try:
                    os.system(f"curl -s -m 10 {URL1}/au")
                    viritetty = True
                    response_data = {
                    "message": "VIRITETTY1!",
                    "error": ""
                    }
                except:
                    os.system(f"curl -s  -m 10 {URL2}/au")
                    viritetty = True
                    response_data = {
                    "message": "VIRITETTY2!",
                    "error": ""
                    }
            else:
                try:
                    os.system(f"curl -s  -m 10  {URL1}/ki")
                    viritetty = False
                    response_data = {
                    "message": "AVATTU1!",
                    "error": ""
                    }
                except:
                    os.system(f"curl -s  -m 10  {URL2}/ki")
                    viritetty = False
                    response_data = {
                    "message": "AVATTU2!",
                    "error": ""
                    }
          except:
                viritetty = False
                response_data = {
                        "message": "VIRHE",
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

