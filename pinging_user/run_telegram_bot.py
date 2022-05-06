import time
from telegram_definition import init_telegram_bot, update_database

init_telegram_bot()
while(True):
    update_database()
    time.sleep(3600)