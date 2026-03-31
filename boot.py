import time,machine
from machine import Timer


def timeout_reboot(t):
    print("Wi-Fi connection hung for too long! Rebooting...")
    machine.reset()

def do_connect():
    import network
    timer = Timer(-1)
    timer.init(period=20000, mode=Timer.ONE_SHOT, callback=timeout_reboot)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Jorpakko', 'Juhannusyona')
    while not sta_if.isconnected(): time.sleep(1)
    print('IF network config:', sta_if.ifconfig())
    timer.deinit()

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






