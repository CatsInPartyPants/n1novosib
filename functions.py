import requests
from bs4 import BeautifulSoup


url = 'https://novosibirsk.n1.ru/kupit/kvartiry/?page='
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
    result = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')
    #находим все адреса на странице
    print('[INFO] собираем все адреса доступные на главной странице.')
    for item in soup.find_all(attrs={'class' : 'link-text'}):
        adress = item.text.split(',')
        adress = adress[1] + adress[2]
        if adress not in houses:
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
        for item in soup.find_all(attrs={'class' : 'card-living-content-params__more-offers'}):
            house_urls.append(domain + item.get('href'))
    print('[INFO] Ссылки "Все квартиры в доме собраны')
    return dict(zip(houses, house_urls))


result = house_search(url=url, headers=headers)
print(result)
