from functions import *




url = 'https://novosibirsk.n1.ru/kupit/kvartiry/?limit=30'
headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", 
"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

# две функции ниже нужны для того, чтобы сформировать первоначальный файл 
# для выборки зданий с начальной страницы 
#result = house_search(url=url, headers=headers) 
#data_into_json(result)

get_flats_info('houses.json')       