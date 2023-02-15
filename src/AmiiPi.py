import time
from luma.core.virtual import terminal

import Interface
import StartScreen
import FilterSelection


if __name__ == "__main__":
    Interface.gpio_config()
    term = Interface.get_terminal()
    StartScreen.start_screen(term)
    term.animate = False
    FilterSelection.filter_selection(term)
