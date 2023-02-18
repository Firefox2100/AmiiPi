from luma.core.virtual import terminal
import time
import RPi.GPIO as GPIO

import Interface

def initial_selection(term: terminal) -> int:
    menu_list = [
        " A  B  C  D  E  F  G ",
        " H  I  J  K  L  M  N ",
        " O  P  Q  R  S  T  U ",
        " V  W  X  Y  Z  #  * "
    ]

    char_list = []
    for i in range(65, 91):
        char_list.append(chr(i))

    char_list.append("#")
    char_list.append("*")
    selected_x = 0
    selected_y = 0
    update = True
    stay = True

    term.clear()
    term.println("Select Initial:")
    for item in menu_list:
        term.println(item)

    term._cy = term._ch
    term._cx = 0
    new_x = 0
    new_y = 0

    while stay:
        if GPIO.event_detected(Interface.stick_up):
            new_y = (selected_y - 1) % 4
            new_x = selected_x
            update = True
        if GPIO.event_detected(Interface.stick_down):
            new_y = (selected_y + 1) % 4
            new_x = selected_x
            update = True
        if GPIO.event_detected(Interface.stick_left):
            new_x = (selected_x - 1) % 7
            new_y = selected_y
            update = True
        if GPIO.event_detected(Interface.stick_right):
            new_x = (selected_x + 1) % 7
            new_y = selected_y
            update = True
        if GPIO.event_detected(Interface.stick_press):
            return selected_x + selected_y * 7
        if GPIO.event_detected(Interface.key3):
            return -1

        if update:
            term._cx = selected_x * 3 * term._cw
            term._cy = (selected_y + 1) * term._ch
            term.puts(" " + char_list[selected_x + selected_y * 7] + " ")

            term._cx = new_x * 3 * term._cw
            term._cy = (new_y + 1) * term._ch
            term.puts("[" + char_list[new_x + new_y * 7] + "]")
            term.flush()
            selected_x = new_x
            selected_y = new_y

        time.sleep(0.1)


if __name__ == "__main__":
    Interface.gpio_config()
    term = Interface.get_terminal()
    term.animate = False
    initial_selection(term)