
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

def do_not_connect():
    import network
    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid="Glukko",password='Juhannusyona')
    print('AP network config:', ap_if.ifconfig())
    ap_if.active(True)
#    ap_if.active(False)
    print('AP network config:', ap_if.ifconfig())

do_not_connect()

    
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






