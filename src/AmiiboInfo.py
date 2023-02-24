from luma.core.virtual import terminal
import time
import RPi.GPIO as GPIO

import Interface
import Proxmark3

def amiibo_info(term: terminal, amiibo_data: tuple, pm3: Proxmark3.Proxmark3):
    term.clear()
    term.println(amiibo_data[0])
    term.newline()
    term.println(amiibo_data[1])
    term.println(amiibo_data[2])

    while True:
        if GPIO.event_detected(Interface.stick_press):
            term.clear()
            term.newline()
            term.newline()
            term.println("Loading dump file...")
            pm3.pm3_load(amiibo_data[1] + "_" + amiibo_data[2] + ".bin")
            term.println("Done!")
            time.sleep(0.5)
            term.clear()
            term.println(amiibo_data[0])
            term.newline()
            term.println(amiibo_data[1])
            term.println(amiibo_data[2])
        
        if GPIO.event_detected(Interface.key1):
            term.clear()
            term.newline()
            term.newline()
            term.println("Randomizing UID...")
            pm3.randomize_uid(amiibo_data[1] + "_" + amiibo_data[2] + ".bin")
            term.println("Done!")
            time.sleep(0.5)
            term.clear()
            term.println(amiibo_data[0])
            term.newline()
            term.println(amiibo_data[1])
            term.println(amiibo_data[2])
        
        if GPIO.event_detected(Interface.key2):
            term.clear()
            term.newline()
            term.newline()
            term.println("Saving to dump...")
            pm3.write_back(amiibo_data[1] + "_" + amiibo_data[2] + ".bin")
            term.println("Done!")
            time.sleep(0.5)
            term.clear()
            term.println(amiibo_data[0])
            term.newline()
            term.println(amiibo_data[1])
            term.println(amiibo_data[2])
        
        if GPIO.event_detected(Interface.key3):
            return
