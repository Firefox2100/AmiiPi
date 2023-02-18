import time
import sqlite3

import Interface
import StartScreen
import FilterSelection
import InitialSelection
import ListSelection
import AmiiboInfo
import Proxmark3

db = sqlite3.connect('../assets/amiibo.db')
c = db.cursor()

if __name__ == "__main__":
    Interface.gpio_config()
    term = Interface.get_terminal()

    pm3 = Proxmark3.Proxmark3()
    
    StartScreen.start_screen(term)
    term.animate = False
    while True:
        filter_result = FilterSelection.filter_selection(term)
        initial_result = InitialSelection.initial_selection(term)

        if initial_result == -1:
            continue
        elif initial_result == 26:
            if filter_result == 0:
                sql = 'SELECT DISTINCT "characters" FROM "amiibos" ORDER BY "characters";'
            elif filter_result == 1:
                sql = 'SELECT DISTINCT "game_series" FROM "amiibos" ORDER BY "game_series";'
            elif filter_result == 2:
                sql = 'SELECT DISTINCT "game" FROM "usages" ORDER BY "game";'

            db_result = c.execute(sql).fetchall()

            for i in range(0, len(db_result)):
                if db_result[i][0] >= 65:
                    db_result = db_result[0:i]
                    break
        elif initial_result == 27:
            if filter_result == 0:
                sql = 'SELECT DISTINCT "characters" FROM "amiibos";'
            elif filter_result == 1:
                sql = 'SELECT DISTINCT "game_series" FROM "amiibos";'
            elif filter_result == 2:
                sql = 'SELECT DISTINCT "game" FROM "usages";'

            db_result = c.execute(sql).fetchall()
        else:
            if filter_result == 0:
                sql = 'SELECT DISTINCT "characters" FROM "amiibos" WHERE "characters" LIKE "' + chr(65 + initial_result) + '%";'
            elif filter_result == 1:
                sql = 'SELECT DISTINCT "game_series" FROM "amiibos" WHERE "game_series" LIKE "' + chr(65 + initial_result) + '%";'
            elif filter_result == 2:
                sql = 'SELECT DISTINCT "game" FROM "usages" WHERE "game" LIKE "' + chr(65 + initial_result) + '%";'

            db_result = c.execute(sql).fetchall()
        
        while True:
            list_result = ListSelection.list_selection(term, db_result)

            if list_result == -1:
                break
            else:
                name_selection = db_result[list_result][0]

                sql = 'SELECT "name", "head", "tail" FROM "amiibos"'

                if filter_result == 0:
                    sql += 'WHERE "characters" IS "' + name_selection + '";'
                elif filter_result == 1:
                    sql += 'WHERE "game_series" IS "' + name_selection + '";'
                elif filter_result == 2:
                    sql += 'WHERE "name" IN (SELECT DISTINCT "amiibo" FROM "usages" WHERE "game" IS "' + name_selection + '";'
                
                amiibo_result = c.execute(sql).fetchall()
            
            while True:
                amiibo_selected = ListSelection.list_selection(term, amiibo_result)

                if amiibo_selected == -1:
                    break
                else:
                    AmiiboInfo.amiibo_info(term, amiibo_result[amiibo_selected])
