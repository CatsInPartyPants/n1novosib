import schedule
import time
from functions import get_flats_info


schedule.every().day.at("18:00").do(get_flats_info('houses.json'))

while True:
    schedule.run_pending()
    time.sleep(15)