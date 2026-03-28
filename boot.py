import time,machine


def do_connect():
    import network
    hukassa=True
    while hukassa:
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        a=sta_if.scan()
        for n in range(len(a)):
            print(a[n])
            if b'Jorpakko'in a[n]:
                hukassa=False
                break
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print('connecting to network...')
    sta_if.connect('Jorpakko', 'Juhannusyona')
    time.sleep(1)
    if not sta_if.isconnected(): time.sleep(6)
    if not sta_if.isconnected(): machine.reset()
    print('IF network config:', sta_if.ifconfig())

do_connect() 

def do_not_connect():
    import network
    ap_if = network.WLAN(network.AP_IF)
    print('AP network config:', ap_if.ifconfig())
    ap_if.active(False)
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






