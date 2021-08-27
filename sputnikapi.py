import requests
import json


adress = 'Архангельск ' + 'Троицкий, 51'
url = f'http://search.maps.sputnik.ru/search?q={adress}'
res = requests.get(url=url)

final = json.loads(res.text)

print(final['result'][0]['position']['lat'],final['result'][0]['position']['lon'])
