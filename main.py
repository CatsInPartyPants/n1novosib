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

""" url2 = 'https://novosibirsk.n1.ru/view/73746777/'

flat_html = requests.get(url=url2, headers=headers)
soup = BeautifulSoup(flat_html.text, 'lxml')
tree = html.fromstring(flat_html.content)
area = soup.find(attrs={
    'class':'card-living-content-params-list__value',
     'data-test':'offer-card-param-total-area'})
floor = soup.find(attrs={
    'class':'card-living-content-params-list__value', 
    'data-test' : 'offer-card-param-floor'})

material = soup.find(attrs={
    'class':'card-living-content-params-list__value',
    'data-test':'offer-card-param-house-material-type'})
delivery = tree.xpath('/html/body/div[1]/div[3]/div/section/div/div[1]/div/div[2]/section/div[2]/div[1]/div/div/div[2]/ul/li[1]/span[2]//text()')
god = delivery[0].encode('utf8')

print(god)
print(area.text)
print(floor.text)
print(material.text) """

    

     
            