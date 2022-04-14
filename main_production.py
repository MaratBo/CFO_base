import copy
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup as bs
import requests
import re
import time
from dotenv import load_dotenv
import os
from record import connect




load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT')
REGION_LIST = ['lipetskaya_oblast', 'belgorodskaya_oblast', 'ivanovskaya_oblast', 'tulskaya_oblast',
               'smolenskaya_oblast', 'tverskaya_oblast', 'orlovskaya_oblast', 'bryanskaya_oblast', 'kaluzhskaya_oblast',
               'ryazanskaya_oblast', 'kostromskaya_oblast', 'tambovskaya_oblast', 'kurskaya_oblast',
               'vladimirskaya_oblast', 'yaroslavskaya_oblast',
               ]

REGIONS = {'lipetskaya_oblast': None,
           'tambovskaya_oblast': None,
           'belgorodskaya_oblast': None,
           'smolenskaya_oblast': None,
           'orlovskaya_oblast': None,
           'bryanskaya_oblast': None,
           'kurskaya_oblast': None,
           'ivanovskaya_oblast': None,
           'vladimirskaya_oblast': None,
           'kostromskaya_oblast': None,
           'yaroslavskaya_oblast': None,
           'tulskaya_oblast': None,
           'ryazanskaya_oblast': None,
           'kaluzhskaya_oblast': None,
           'tverskaya_oblast': None,
           'chukotskiy_ao': None
           }
day_base = {'base': None}

URL_BEGIN = 'https://auto.ru/'
URL_END = '/dilery/cars/used/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
day_time = ''

def main(list_regions: list) -> list:
    date = str(datetime.datetime.today().date())
    copy_base = copy.deepcopy(REGIONS)
    copy_day_base = copy.deepcopy(day_base)
    for geo in list_regions:
        url = URL_BEGIN + geo + URL_END
        r = requests.get(url, HEADERS).text
        soup = bs(r, 'html.parser')
        try:
            count = soup.find('span', class_='ButtonWithLoader__content').text
            numb = re.sub('\D', '', count)
            print(geo, numb)
            REGIONS[geo] = int(numb)
        except AttributeError:
            REGIONS[geo] = None
            print(f'{geo} not accessable')
        connect(date, geo, day_time, int(numb))
        time.sleep(4800)

    answer = [copy_base, copy_day_base]
    #medium_check(answer)
    #return answer


def make_text(copy_list: list):
    copy_base = copy_list[0]
    copy_day_base = copy_list[1]
    all_base_count = [val for val in REGIONS.values()]
    sum_base_count = sum(all_base_count)
    day_base['base'] = sum_base_count
    try:
        diff_in_total_base = day_base['base'] - copy_day_base['base']
    except TypeError:
        diff_in_total_base = 0
    regions_with_max_dif = count_diff_for_regions(copy_base, REGIONS)
    if regions_with_max_dif:
        message_info = f'База ЦФО: {sum_base_count} ({diff_in_total_base})\n' \
                       f'{regions_with_max_dif}'
        return message_info
    return f'База ЦФО: {sum_base_count} ({diff_in_total_base})'


def count_diff_for_regions(copy: dict, last_dict: dict) -> str:
    text = ''
    for geo in last_dict:
        try:
            absolut_diff = copy[geo] - last_dict[geo]
            dif = (absolut_diff/last_dict[geo]*100)
            if dif > 10:
                signal_attention = f'{geo} +{absolut_diff}'
                text += signal_attention + '\n'
            elif dif < -10:
                signal_attention = f'{geo} {absolut_diff}'
                text += signal_attention + '\n'
            else:
                pass
        except TypeError:
            pass
    return text


atempt = 0


def medium_check(answer: list) -> None:
    global atempt
    atempt += 1
    print(atempt)
    time.sleep(15)
    try:
        check_none = [k for k, v in REGIONS.items() if v is None]
        if check_none:
            print(f'restart main {check_none}')
            main(check_none)
        else:
            print(f'to message {answer}')
            message_bot(answer)
    except TypeError:
        pass


def message_bot(answer: list) -> None:
    value = answer
    check_none = [k for k, v in REGIONS.items() if v is not None]
    if len(check_none) == 16:
        text = make_text(value)
        URL_BOT = ('https://api.telegram.org/bot{token}/sendMessage'.format(token=TOKEN))
        data = {'chat_id': CHAT_ID,
                'text': text
                }
        #requests.post(URL_BOT, data=data)
        print(data['text'])
    else:
        none_list = [k for k, v in REGIONS.items() if v is None]
        print(f'else {none_list}')
        main(none_list)


if __name__ == '__main__':
    while True:
        time_now = datetime.datetime.now() + timedelta(hours=3)
        h = time_now.hour
        m = time_now.minute
        d = time_now.date().strftime("%d")
        print(f'check time {h}:{m}')
        if m in range(0, 59) and h == 8:
            day_time = 'morning'
            print(f'morning start {d}-{h}:{m}')
            value = main(REGION_LIST)
            time.sleep(36000)
        elif m in range(0, 59) and h == 17:
            day_time = 'evening'
            print(f'evening start {d}-{h}:{m}')
            value = main(REGION_LIST)
            time.sleep(54000)
        else:
            time.sleep(3300)