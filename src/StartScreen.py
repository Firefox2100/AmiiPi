from luma.core.virtual import terminal
import time


def start_screen(term: terminal):
    term.clear()
    term.println("       AmiiPi       ")
    term.newline()
    term.println("A Python tool for RPI")
    term.println("with OLED hat to work")
    term.println("    with Amiibos")
    time.sleep(2)


if __name__ == "__main__":
    import Interface
    Interface.gpio_config()
    term = Interface.get_terminal()
    start_screen(term)

    while True:
        time.sleep(1)
