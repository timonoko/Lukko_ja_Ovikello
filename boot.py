import time


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Jorpakko', 'Juhannusyona')
        while not sta_if.isconnected():
            pass
    print('IF network config:', sta_if.ifconfig())

do_connect() 

def do_AP_connect():
    import network
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.4.2'))
    ap.config(essid="Glukko",password='Juhannusyona',authmode=network.AUTH_WPA_WPA2_PSK)
    time.sleep(1)
    print('AP network config:', ap.ifconfig())

do_AP_connect()

    
import gc
gc.collect()

import esp
esp.osdebug(None)

import os

def ls():
    print(os.listdir())


if not "do_webrepl" in os.listdir():
    import lukko2

os.remove("do_webrepl")

import webrepl
webrepl.start()






