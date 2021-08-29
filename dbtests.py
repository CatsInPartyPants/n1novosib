import sqlite3

def average_price():
    # Показывает среднюю цену квадратного метра во всех проверенных домах
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Flats WHERE _Date = '2021-08-28'")
    items = c.fetchall()
    all_flats1 = len(items)
    price_first = 0    
    for item in items:
        price_first += item[7] / all_flats1
    price_first = ("%.2f" % price_first)
    
    c.execute("SELECT * FROM Flats WHERE _Date = '2021-08-29'")
    items = c.fetchall()
    all_flats2 = len(items)
    price_second = 0    
    for item in items:
        price_second += item[7] / all_flats2
    price_second = ("%.2f" % price_second)
    
    print(f'28 августа 2021 года проверено {all_flats1} квартир. 29 августа 2021 года - {all_flats2}. Средняя цена одного метра по всем домам 28 августа составила {price_first} рублей. 29 августа - {price_second} рублей.')
        
    conn.commit()
    conn.close()

def average_price_house(adress):
    #принимает адрес - показывает среднюю цену квадратного метра в доме
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f"""SELECT * FROM Flats WHERE _Date = '2021-08-28' AND Adress = '{adress}'""")
    items = c.fetchall()
    all_flats1 = len(items)
    price_first = 0    
    for item in items:
        price_first += item[7] / all_flats1
    price_first = ("%.2f" % price_first)
    
    c.execute(f"""SELECT * FROM Flats WHERE _Date = '2021-08-29' AND Adress = '{adress}'""")
    items = c.fetchall()
    all_flats2 = len(items)
    price_second = 0
        
    for item in items:
        price_second += item[7] / all_flats2
    price_second = ("%.2f" % price_second)
    
    print(f'28 августа 2021 года проверено {all_flats1} квартир по адресу {adress}. 29 августа 2021 года - {all_flats2}. Средняя цена одного метра 28 августа составила {price_first} рублей. 29 августа - {price_second} рублей.\n')
        
    conn.commit()
    conn.close()

def average_price_all():
    adresses = []
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f"""SELECT * FROM Flats""")
    items = c.fetchall()     
    for item in items:
        adresses.append(item[1])
    adresses = set(adresses)
    
    for adress in adresses:
        average_price_house(adress)
        
def searching_flat_for_client():
    #ищет квартиру площадью не меньше 25 кв метров по цене до 3 миллионов
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f"""SELECT * FROM Flats WHERE Area >= 25.0 AND Price <= 3000000""")
    items = c.fetchall()     
    for item in items:
        print(item)
    


average_price()

average_price_all()

searching_flat_for_client()





