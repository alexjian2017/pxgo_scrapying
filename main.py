from pxgo.pxgo import Pxgo
from pxgo.constant import *
from database import DataToMySQL
import time

with Pxgo() as bot:

    bot_db = DataToMySQL()
    date = bot.get_date()
    bot.get_first_page()
    bot.get_second_page()
    # bot.large_category('5134', bot_db, date)
    for track_id in TRACKING_ID:
        bot.large_category(track_id, bot_db, date)
    bot_db.close()

    time.sleep(5)
