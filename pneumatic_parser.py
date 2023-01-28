from bs4 import BeautifulSoup
from lxml import etree
import requests
from ftfy import fix_encoding
from csv import writer


_name_object = ""
_stroke_length = ""
_piston_diameter = ""
_operating_pressure = ""
_operating_temperature = ""
_stem_thread = ""
_standard = ""
_url = ""
  

for i in range(0,10):

    _url = "http://aircrafter.ru/index.php?page=shop.product_details&flypage=flypage.tpl&product_id=24&category_id=56&option=com_virtuemart&Itemid=55" #url
    
    HEADERS = ({'User-Agent': #агент для зпхода в браузер
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})
    
    webpage = requests.get(_url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    #print(soup)
    #print(dom.xpath('//*[@id="contenttb"]/table/tbody/tr[2]/td/div/table/tbody/tr[1]/th')[0])
    _name_object = fix_encoding("Наименование:" + "name")
    _standard = fix_encoding("Стандарт:" + dom.xpath('//*[@id="table1"]/tbody/tr[3]/td[3]/div[1]/p/span/text()')[0])
    _stroke_length = fix_encoding("Длина хода:" + dom.xpath('//*[@id="table2"]/tbody/tr[5]/td[2]/p/big/span[2]')[0].text)
    _piston_diameter = fix_encoding("Диаметр поршня:" + dom.xpath('//*[@id="table2"]/tbody/tr[6]/td[2]/p/span')[0].text)
    _operating_pressure = fix_encoding("Рабочее давление:" + dom.xpath('//*[@id="table2"]/tbody/tr[8]/td[2]/p/span')[0].text)
    _operating_temperature = fix_encoding("Температура эксплутации:" + dom.xpath('//*[@id="table2"]/tbody/tr[9]/td[2]/p/span/text()[1]')[0])
    _stem_thread = fix_encoding("Резьба на штоке:" + dom.xpath('//*[@id="table63"]/tbody/tr[2]/td[3]')[0].text)
    _url = ("Ссылка:" + _url)

    List = [_name_object, _stroke_length, _piston_diameter, _operating_pressure, _operating_temperature, _stem_thread, _standard, _url]

    with open('pneumatic_armature_parser_table.csv', 'a', encoding="utf-8") as f_object:
        writer_object = writer(f_object, delimiter=";", lineterminator='\n')
        writer_object.writerow(List)
        f_object.close()