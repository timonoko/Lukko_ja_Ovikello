from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import time

import socket

class ReusableHTTPServer(HTTPServer):
    # TÄMÄ RIVI KORJAA "Address already in use" -ONGELMAN:
    allow_reuse_address = True

LUKKO_URL = "http://89.27.95.8:7981"

# Tilanseuranta ja aikaleima
viritetty = False
viimeisin_painallus = 0
VIRITYS_AIIKA_SEK = 10  # Aikaa toiselle painallukselle

class LukkoProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global viritetty, viimeisin_painallus
        nykyhetki = time.time()
        
        # Tarkistetaan onko aiempi viritys vanhentunut
        if viritetty and (nykyhetki - viimeisin_painallus > VIRITYS_AIIKA_SEK):
            viritetty = False

        if self.path == "/avaa" or self.path == "/":
            if not viritetty:
                # ESI-PAINALLUS: Viritetään turvakytkin
                viritetty = True
                viimeisin_painallus = nykyhetki
                
                response_data = {
                    "message": "VIRITETTY! Paina 10s sisällä",
                    "error": ""
                }
            else:
                # TOINEN PAINALLUS: Suoritetaan varsinainen avaus!
                viritetty = False
                try:
                    subprocess.run(["curl", "-s", f"{LUKKO_URL}/au"], check=True, timeout=5)
                    time.sleep(0.5)
                    subprocess.run(["curl", "-s", f"{LUKKO_URL}/ki"], check=True, timeout=20)
                    
                    response_data = {
                        "message": "OVI AVATTU!",
                        "error": ""
                    }
                except Exception as e:
                    response_data = {
                        "message": "VIRHE",
                        "error": f"Lukko ei vastannut: {e}"
                    }

        # Lähetetään vastaus kellolle
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

