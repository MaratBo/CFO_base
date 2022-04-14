import requests
from bs4 import BeautifulSoup as bs
import re



URL_BEGIN = 'https://auto.ru/'
URL_END = '/dilery/cars/used/'
answer = []
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}


def re_round(data: list):
    print('dealer page')
    for geo in data:
        url = URL_BEGIN + geo + URL_END
        r = requests.get(url, HEADERS).text
        soup = bs(r, 'html.parser')
        sum_dealer_base = 0
        place = soup.findAll('a', class_='Link DealerListItem__search_results')
        print(place)
        # for i in place:
        #     print(i)
        #     numb = re.sub('\D', '', i.text)
        #     sum_dealer_base += int(numb)
        #     print(f'{numb}')





#print(new_dict)




re_round(['tambovskaya_oblast'])

