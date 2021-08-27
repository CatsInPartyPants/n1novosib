import requests
from bs4 import BeautifulSoup
import json
from lxml import html
import time


url = 'https://novosibirsk.n1.ru/kupit/kvartiry/?limit=30'
headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", 
"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def house_search(url, headers):
    #возвращает словарь "адрес : url на все квартиры в доме"
    houses = []
    urls = []
    house_urls = []
    domain = 'https://novosibirsk.n1.ru'
    payload = '&deal_type=sell&rubric=flats&limit=1000' # payload необходим, чтобы в будущем все ссылки выводились на одной странице
    result = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')
    #находим все адреса на странице
    print('[INFO] собираем все адреса доступные на главной странице.')
    for item in soup.find_all(attrs={'class' : 'link-text'}):
        adress = item.text.split(',')
        adress = adress[1] + adress[2]
        houses.append(adress)    
    print('[INFO] адреса собраны.')
    
    #находим все ссылки на конкретные квартиры
    print('[INFO] Собираем ссылки квартир на главной странице.')
    for page in soup.find_all(attrs = {'class': 'link', 'target': '_blank'}):
        if page.get('href') not in urls:
            urls.append(domain + page.get('href'))
    print('[INFO] ссылки квартир на главной странице собраны.')
   
    #на странице конкретной квартиры находим ссылку на все квартиры в доме
    print('[INFO] Начинаем поиск ссылок "Все квартиры в доме".')
    for _url in urls:
        finder = requests.get(_url)
        soup = BeautifulSoup(finder.text, 'lxml')
        for item in soup.find_all(attrs={
            'class' : 'card-living-content-params__more-offers'}):
            house_urls.append(domain + item.get('href') + payload)
    print('[INFO] Ссылки "Все квартиры в доме собраны')
    return dict(zip(houses, house_urls))


def data_into_json(res):
    #функция записывает данные в файл json возвращаемые функцией house_search
    with open('houses.json', 'w', encoding='utf8') as file:
        json.dump(res, file, ensure_ascii=False, indent=4)
    print('[INFO] файл json с данными сформирован')


def get_flats_info(file):
    #функция ищет данные по всем квартирам в доме, записывает эти данные в БД
    adress_flat_urls = []
    domain = 'https://novosibirsk.n1.ru'
    with open(file, encoding = 'utf8') as f:
        data = json.load(f)
    for adress, url in data.items():
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        for page in soup.find_all(attrs = {'class': 'link', 'target': '_blank'}):
            adress_flat_urls.append(domain + page.get('href'))
        for flat_url in adress_flat_urls:
            time.sleep(1)
            flat_html = requests.get(url=flat_url, headers=headers)
            soup = BeautifulSoup(flat_html.text, 'lxml')
            tree = html.fromstring(flat_html.content)
            area = soup.find(attrs={
                'class':'card-living-content-params-list__value',
                'data-test':'offer-card-param-total-area'})
            area = area.text
            area = [s for s in area.split()]
            area = area[0]
            area = ''.join(c if c != ',' else '.' for c in area) # переводим в вид формата float
            
            floor = soup.find(attrs={
                'class':'card-living-content-params-list__value',
                'data-test' : 'offer-card-param-floor'})
            material = soup.find(attrs={
                'class':'card-living-content-params-list__value',
                'data-test':'offer-card-param-house-material-type'})
            delivery = tree.xpath('/html/body/div[1]/div[3]/div/section/div/div[1]/div/div[2]/section/div[2]/div[1]/div/div/div[2]/ul/li[1]/span[2]//text()')
            god = delivery[0].split(' ')
            
            price = soup.find(attrs={'class':'price'})
            price = price.text
            price = [s for s in price.split() if s.isnumeric()] #переводим цену квартиры из строки в число, убираем лишние знаки
            price = ''.join(str(i) for i in price) #переводим цену квартиры из строки в число, убираем лишние знаки
            
            part_price = soup.find(attrs={'class':'part-price'})
            part_price = part_price.text            
            part_price = [s for s in part_price.split() if s.isdigit()] #переводим цену за метр квартиры из строки в число, убираем лишние знаки            
            part_price = ''.join(str(i) for i in part_price) #переводим цену за метр квартиры из строки в число, убираем лишние знаки


            adress_to_bd = 'Новосибирск ' + adress
            sputnik_api = f'http://search.maps.sputnik.ru/search?q={adress_to_bd}'
            position_html = requests.get(url=sputnik_api)
            position = json.loads(position_html.text)
            try:
                position_to_bd = (position['result'][0]['position']['lat'],position['result'][0]['position']['lon'])
            except IndexError:
                position_to_bd = 'Not defined'

            print('--------------------------------------------------------')
            print('[INFO] Следующие данные будут записаны в базу данных')
            flat_url_to_bd = flat_url
            print(flat_url_to_bd) # Урл адрес, который будет записан в БД                  
            print(adress_to_bd) # физический Адрес объекта, который будет записан в БД           
            try:
                year_to_bd = str((f'{god[0]} кв. {god[2]} года')) 
                print(year_to_bd) # Год и квартал будет записан в БД если квартал есть               
            except IndexError:
                year_to_bd = str((f'{god[0]}  год'))
                print(year_to_bd) # Год  будет записан в БД если квартал не указан
            area_to_bd = float(area)          
            print(area_to_bd) # Площадь будет записана в БД
            floor_to_bd = floor.text            
            print(floor_to_bd) # Этаж будет записан в БД
            material_to_bd = material.text           
            print(material_to_bd) # Материал дома будет записан в БД
            price_to_bd = int(price)          
            print(price_to_bd) # Цена будет записана в бд
            part_price_to_bd = int(part_price)         
            print(part_price_to_bd) # Цена за метр будет записана в БД 
            print(position_to_bd)      
            print('--------------------------------------------------------')

        