
print('Testing  24')

try:
  import usocket as socket
except:
  import socket
import network,time

# print prints only to Python client
from machine import UART
uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1, timeout=1000)
uart.write(b'Uart works  #6')

releet=['-',0,0,0,0,'*']

def rele(r,o): 
    releet[r]=o
    uart.write(b'%c%c%c%c'%(0xA0,r,o,0xA0+o+r))
    time.sleep(0.2)

for x in range(1,5): rele(x,0)

AU=False
OVIKELLO=False
RING=False

def web_page():
    if AU:
        butt="button button2"
    else:
        butt="button"
    if OVIKELLO:
        hit="""<a href="/kerran"> <button class="button button2" >KERRAN</button></a>"""
    else:  
        hit="""<a href="/ovikello"> <button class="button" >OVIKELLO</button></a>"""
    if RING:
        ring="""<p><a href="/ring"> <button class="button" >RING</button></a>"""
    else:
        ring=" "
    menu=""" <p> 
    <a href="/au"> <button class=" """+butt+""" " >AU-</button></a>
    <a href="/ki"> <button class="button">KI</button></a> <p>
    """+hit+ring+"""
    <p><p> """
    for x in range(3,5):
        menu=menu+"""
    <p> """ +str(x)+":"+str(releet[x])+ """ <a href="/r%ion"> <button class="button button2">ON</button></a>
     <a href="/r%ioff"> <button class="button">OFF</button></a></p>
    """%(x,x)
    html = """
     <html><head> 
     <title>LUKKO</title>
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <link rel="icon" href="data:,">
     <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #bd4141; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #5d9868;}</style>
     </head>
      <body>
     <h1>LUKKO</h1> 
     """ + menu + """
      <p> =====================
    
     </body>
   </html>"""
    return html

def auki():
    rele(1,1)
    rele(2,0)
    time.sleep(2)
    rele(1,0)
    time.sleep(2)
    rele(2,1)
    time.sleep(1)
    rele(1,0)
    rele(2,0)
    
from machine import Pin

BUTTON=Pin(2, Pin.IN)  
HI=1; LO=0

def buttoni():
    nummer=0
    if BUTTON.value()==LO:
        loc=0
        hic=0
        while hic<50:
            while BUTTON.value()==LO:
                time.sleep(0.010)
                loc=loc+1
                hic=0
            if loc > 100: nummer=5
            elif loc > 3:
                loc=0
                nummer=nummer+1
            time.sleep(0.010)
            hic=hic+1 
    return nummer


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    s.settimeout(0.2)
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        s.settimeout(5.0)
        if request.find('/ovikello') == 6:
                OVIKELLO=True
        if request.find('/kerran') == 6:
                OVIKELLO=False
        if request.find('/ki') == 6:
            if AU:
                auki()
            OVIKELLO=False
        AU=False
        if request.find('/au') == 6:
            AU=True
        for r in range(1,5):
            if request.find('/r'+str(r)+'on') == 6: rele(r,1)
            if request.find('/r'+str(r)+'off') == 6: rele(r,0)
        if request.find('/r5off') == 6:
            for x in range(1,5): rele(x,0)
        if request.find('/ring') == 6:
            RING=False
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError:
        nummer=buttoni()
        if nummer>0:
#            print("RIING")
            RING=True
            if OVIKELLO:
                OVIKELLO=False
                auki()
            elif nummer==7:
                auki()
 

