

print('Testing  24')

try:
  import usocket as socket
except:
  import socket
import network,time

import machine,uping

# print prints only to Python client
from machine import UART
uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1, timeout=1000)
uart.write(b'Uart works  #6')

releet=['-',0,0,0,0,'*']

def rele(r,o):
    global releet
    releet[r]=o
    uart.write(b'%c%c%c%c'%(0xA0,r,o,0xA0+o+r))
    time.sleep(0.2)

AU=False
OVIKELLO=False
RING=False
reset_laskuri=0


def onko_kanny():
    for x in ('192.168.1.198','192.168.4.2','192.168.4.3',
        '192.168.4.4','192.168.4.5','192.168.4.6','192.168.4.7',
        '192.168.4.8'):
        wdt.feed()
        p=uping.ping(x,count=1,timeout=300)
        if p[1]!=0: return True
    return False

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
    menu="<h1>LUKKO</h1> "
    menu+=""" <p> 
    <a href="/au"> <button class=" """+butt+""" " >AU-</button></a>
    <a href="/ki"> <button class="button">KI</button></a> <p>
    """+hit+ring+"""
    <p><p> """
    for x in range(3,5):
        menu=menu+"""
    <p> """ +str(x)+":"+str(releet[x])+ """ <a href="/r%ion"> <button class="button button2">ON</button></a>
     <a href="/r%ioff"> <button class="button">OFF</button></a>
    """%(x,x)
    sta_if = network.WLAN(network.STA_IF)
    this_ip=sta_if.ifconfig()[0]
    html = """<html><head><title>LUKKO</title>
     <meta http-equiv="refresh" content="3;url=http://"""+this_ip+"""/">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <link rel="icon" href="data:,">
     <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #bd4141; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #5d9868;}</style>
     </head>
      <body>
     """ + menu + """
      <p> 
     """ + this_ip + """
      <p>    
     """ + str(reset_laskuri) + """
      <p>    
     </body>
   </html>"""
    return html


def mysleep(x):
        global wdt
        for y in range(5*x):
            wdt.feed()
            time.sleep(0.2)

def auki():
    print('AUKI')
    tuuletin=releet[3]
    rele(3,0)
    rele(1,1)
    rele(2,0)
    mysleep(2)
    rele(1,0)
    mysleep(2)
    rele(2,1)
    mysleep(1)
    rele(1,0)
    rele(2,0)
    rele(3,tuuletin)

def tick():
    rele(1,1)
    rele(2,0)
    time.sleep(0.1)
    rele(1,0)
    time.sleep(0.1)
    rele(2,1)
    time.sleep(0.1)
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
        while hic<100:
            while BUTTON.value()==LO:
                wdt.feed()
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



def savee(lista):
    with open('jemma.txt','w') as f:
        for x in lista:
           f.write(x+"="+str(eval(x))+"\n")

def save_vars():
    savee(["OVIKELLO","releet","AU"])
           
def macreset():
    save_vars()
    conn.close()
    machine.reset()

def loadee():
    with open('jemma.txt','r') as f:
        exec(f.read())

try: loadee()
except: pass

from machine import WDT
wdt=WDT() 
    
for x in range(1,5): rele(x,releet[x])
   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print('KAYNNISTYS!')

while True:
    reset_laskuri+=1
    wdt.feed()
    if reset_laskuri%200==0:
        AU=0
        print('reset_laskuriii:',reset_laskuri)
    if reset_laskuri%1000==0: 
        p=uping.ping('192.168.1.11',count=1,timeout=100)
        if p[1]==0: macreset()
    if reset_laskuri%30100==0: 
        p=uping.ping('192.168.1.63',count=1,timeout=100)
        if p[1]==0: macreset()
    s.settimeout(0.2)
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        s.settimeout(5.0)
        if request.find('/ovikello') == 6:
                OVIKELLO=True
                save_vars()
                tick()
        if request.find('/kerran') == 6:
                OVIKELLO=False
                save_vars()
        if request.find('/ki') == 6:
            if AU:
                auki()
                AU=False
                save_vars()
        if request.find('/au') == 6:
            reset_laskuri=0
            AU=not AU
            save_vars()
        if request.find('/kanny') == 6:
            if onko_kanny():
                auki()
                save_vars()
            else:
                print('Ei Kännyä')
        for r in range(1,5):
            if request.find('/r'+str(r)+'on') == 6:
                rele(r,1)
                save_vars()
            if request.find('/r'+str(r)+'off') == 6:
                rele(r,0)
                save_vars()
        if request.find('/r5off') == 6:
            for x in range(1,5): rele(x,0)
        if request.find('/ring') == 6:
            RING=False
        if request.find('/reset') == 6:
            macreset()
        if request.find('/webrepl') == 6:
            with open("do_webrepl","w") as fu:
                fu.write("hello")
            macreset()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError:
        nummer=buttoni()
        if nummer>0:
            print("Ringejä=",nummer)
            RING=True
            if OVIKELLO:
                OVIKELLO=False
                auki()
            elif nummer==7:
                auki()
 

