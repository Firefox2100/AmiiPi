from luma.core.virtual import terminal
import time
import RPi.GPIO as GPIO

import Interface

horizontal_threshold = 7

def display_list(term: terminal, menu:list[str]):
    term.clear()
    for item in menu:
        if len(item) > 19:
            term.puts("  " + item[0:17] + "..")
        else:
            term.puts("  " + item)

        term._cy += term._ch
        term._cx = 0


def list_selection(term: terminal, data: list[tuple]) -> int:
    view_point = 0
    selected = 0
    horizontal_start = 0
    horizontal_counter = 0
    stay = True

    menu = []
    for item in data:
        menu.append(item[0])

    menu_length = len(menu)

    term.clear()
    if menu_length > 6:
        display_list(term, menu[0:6])
    else:
        display_list(term, menu)
    
    term._cx = 0
    term._cy = 0
    term.putch(">")

    term.flush()
    
    while stay:
        if GPIO.event_detected(Interface.stick_up):
            if selected == 0:
                # Reset view to bottom
                term.clear()
                selected = menu_length - 1
                if menu_length > 6:
                    display_list(term, menu[-6:])
                    view_point = menu_length - 6
                    term._cy = (selected - view_point) * term._ch
                    term._cx = 0
                    term.putch(">")
                else:
                    display_list(term, menu)
                    view_point = 0
                    term._cy = selected * term._ch
                    term._cx = 0
                    term.putch(">")
            elif selected == view_point:
                # Scroll up
                term.clear()
                view_point -= 1
                selected -= 1

                display_list(term, menu[view_point: view_point + 6])
                term._cy = (selected - view_point) * term._ch
                term._cy = 0
                term._cx = 0
                term.putch(">")
            else:
                term._cx = 0
                if len(menu[selected]) <= 19:
                    term.putch(" ")
                else:
                    term.puts("  " + menu[selected][0:17] + "..")
                selected -= 1

                term._cx = 0
                term.putch(" ")

                term._cy = (selected - view_point) * term._ch
                term._cx = 0
                term.putch(">")
            
            horizontal_counter = 0
            horizontal_start = 0
            term.flush()

        if GPIO.event_detected(Interface.stick_down):
            if selected == menu_length - 1:
                # Reset view to top
                term.clear()
                selected = 0
                view_point = 0
                if menu_length > 6:
                    display_list(term, menu[0: 6])
                    term._cy = 0
                    term._cx = 0
                    term.putch(">")
                else:
                    display_list(term, menu)
                    term._cy = 0
                    term._cx = 0
                    term.putch(">")
            elif selected == view_point + 5:
                # Scroll down
                term.clear()
                selected += 1
                view_point += 1

                display_list(term, menu[view_point: view_point + 6])
                term._cy = (selected - view_point) * term._ch
                term._cx = 0
                term.putch(">")
            else:
                term._cx = 0
                if len(menu[selected]) <= 19:
                    term.putch(" ")
                else:
                    term.puts("  " + menu[selected][0:17] + "..")

                selected += 1

                term._cy = (selected - view_point) * term._ch
                term._cx = 0
                term.putch(">")
            
            horizontal_counter = 0
            horizontal_start = 0
            term.flush()
        
        if GPIO.event_detected(Interface.stick_press):
            return selected

        if GPIO.event_detected(Interface.key3):
            return -1
        
        if horizontal_counter == horizontal_threshold:
            horizontal_counter = 0
            term._cy = (selected - view_point) * term._ch
            term._cx = 2 * term._cw

            if horizontal_start == (len(menu[selected]) - 19):
                horizontal_start = 0
                term.puts(menu[selected][0: 17] + "..")
            elif horizontal_start == (len(menu[selected]) - 20):
                horizontal_start += 1
                term.puts(menu[selected][-19:])
            else:
                horizontal_start += 1
                term.puts(menu[selected][horizontal_start: horizontal_start + 17] + "..")
            
            term.flush()

        if len(menu[selected]) > 19:
            horizontal_counter += 1
        
        time.sleep(0.1)


if __name__ == "__main__":
    Interface.gpio_config()
    term = Interface.get_terminal()
    term.word_wrap = False
    term.animate = False

    dummy_list_1 = []
    dummy_list_2 = []
    dummy_list_3 = []

    for i in range(0,10):
        dummy_list_1.append(("List " + str(i), ))
    
    for i in range(0, 3):
        dummy_list_2.append(("List " + str(i), ))

    for i in range(0, 10):
        dummy_list_3.append(("Super super super long List " + str(i), ))

    list_selection(term, dummy_list_1)

    while True:
        time.sleep(1)
