from luma.core.virtual import terminal
import time
import RPi.GPIO as GPIO

import Interface

filter_menu = [
    "1. Characters",
    "2. Game Series",
    "3. Games"
    ]


def filter_selection(term: terminal) -> int:
    selected = 0
    stay = True

    term.clear()
    term.println("Sorted by:")
    term.newline()

    y = term._cy

    for i in range(0, 3):
        term.println("  " + filter_menu[i])

    term._cy = y
    term._cx = 0
    term.puts(">")
    term.flush()
    
    while stay:
        if GPIO.event_detected(Interface.stick_up):
            selected = (selected - 1) % 3
            term._cx = 0
            term.puts(" ")
            
            term._cy = y + selected * term._ch
            term._cx = 0
            term.puts(">")

        if GPIO.event_detected(Interface.stick_down):
            selected = (selected + 1) % 3
            term._cx = 0
            term.puts(" ")
            
            term._cy = y + selected * term._ch
            term._cx = 0
            term.puts(">")
        
        if GPIO.event_detected(Interface.stick_press):
            return selected

        term.flush()
        time.sleep(0.1)


if __name__ == "__main__":
    Interface.gpio_config()
    term = Interface.get_terminal()
    term.animate = False
    filter_selection(term)
