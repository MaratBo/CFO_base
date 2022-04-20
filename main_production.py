import datetime
from datetime import timedelta
from bs4 import BeautifulSoup as bs
import requests
import re
import time
from dotenv import load_dotenv
import os
from record import connect, record_cfo_base
from counter import count_dif, get_previous_value


load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT')
REGION_LIST = ['lipetskaya_oblast', 'belgorodskaya_oblast', 'ivanovskaya_oblast', 'tulskaya_oblast',
               'smolenskaya_oblast', 'tverskaya_oblast', 'orlovskaya_oblast', 'bryanskaya_oblast', 'kaluzhskaya_oblast',
               'ryazanskaya_oblast', 'kostromskaya_oblast', 'tambovskaya_oblast', 'kurskaya_oblast',
               'vladimirskaya_oblast', 'yaroslavskaya_oblast',
               ]

URL_BEGIN = 'https://auto.ru/'
URL_END = '/cars/used/?seller_group=COMMERCIAL'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
day_time = ''


def main(list_regions: list) -> None:
    """parsing data"""
    date = str(datetime.datetime.today().date())
    global not_access
    not_access = 0
    count_success = 0
    for geo in list_regions:
        url = URL_BEGIN + geo + URL_END
        r = requests.get(url, HEADERS).text
        soup = bs(r, 'html.parser')
        try:
            count = soup.find('span', class_='ButtonWithLoader__content').text
            numb = re.sub('\D', '', count)
            count_success += 1
            print(geo, numb)
        except AttributeError:
            numb = get_previous_value(geo, date, day_time)
            print(f'{geo} not accessible')
            not_access += 1
        connect(date, geo, day_time, int(numb))
        print(f'успешно пройдено {count_success}'
              f'неуспешных {not_access}')
        time.sleep(363)
    record_cfo_base(date, day_time)


def message_bot() -> None:
    if not_access == 0:
        CHAT_ID = os.getenv('CHAT')
    else:
        CHAT_ID = os.getenv('CHAT_test')
    text = count_dif(day_time)
    URL_BOT = ('https://api.telegram.org/bot{token}/sendMessage'.format(token=TOKEN))
    data = {'chat_id': CHAT_ID,
            'text': text
            }
    requests.post(URL_BOT, data=data)
    print(data['text'])


if __name__ == '__main__':
    while True:
        time_now = datetime.datetime.now() + timedelta(hours=3)
        h = time_now.hour
        m = time_now.minute
        d = time_now.date().strftime("%d")
        print(f'check time {h}:{m}')
        if m in range(0, 59) and h == 7:
            day_time = 'morning'
            print(f'morning start {d}-{h}:{m}')
            main(REGION_LIST)
            message_bot()
            time.sleep(28800)
        elif m in range(0, 59) and h == 17:
            day_time = 'evening'
            print(f'evening start {d}-{h}:{m}')
            main(REGION_LIST)
            message_bot()
            time.sleep(36000)
        else:
            time.sleep(2400)
