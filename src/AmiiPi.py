import time
import sqlite3

import Interface
import StartScreen
import FilterSelection
import InitialSelection

db = sqlite3.connect('../assets/amiibo.db')
c = db.cursor()

if __name__ == "__main__":
    Interface.gpio_config()
    term = Interface.get_terminal()
    StartScreen.start_screen(term)
    term.animate = False
    while True:
        filter_result = FilterSelection.filter_selection(term)
        initial_result = InitialSelection.initial_selection(term)

        if initial_result == -1:
            continue
        elif initial_result == 26:
            pass
        elif initial_result == 27:
            pass
        else:
            match filter_result:
                case 0:
                    sql = 'SELECT DISTINCT "characters" FROM "amiibos" WHERE "characters" LIKE "' + chr(65 + initial_result) + '%";'
                case 1:
                    sql = 'SELECT DISTINCT "game_series" FROM "amiibos" WHERE "game_series" LIKE "' + chr(65 + initial_result) + '%";'
                case 2:
                    sql = 'SELECT DISTINCT "game" FROM "usages" WHERE "game" LIKE "' + chr(65 + initial_result) + '%";'

            db_result = c.execute(sql)
            print(db_result)
