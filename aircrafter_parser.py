from bs4 import BeautifulSoup
from lxml import etree
import requests
from ftfy import fix_encoding
from csv import writer
import re
from exporter import *

def parse_aircrafter(_url, _HEADERS):
    webpage = requests.get(_url, headers=_HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    #print(soup)
    #print(dom.xpath('//*[@id="contenttb"]/table/tbody/tr[2]/td/div/table/tbody/tr[1]/th')[0])

    _counter_diameters = fix_encoding("Диаметр поршня:" + dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[5]/tbody/tr[6]/td[2]/p/span')[0].text)
    _count_nums = len(re.findall(r'\b\d+\b', _counter_diameters)) #количество диаметров поршня

    for i in range(0, _count_nums):
        _name_object = fix_encoding("Наименование:" + "Aircrafter company")
        _standard = fix_encoding("Стандарт:" + dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[1]/tbody/tr[2]/td/p/span')[0].text)
        _piston_diameter = fix_encoding(dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[14]/tbody/tr['+str(i+2)+']/td[1]')[0].text)
        _stroke_length = fix_encoding("Длина хода:" + dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[5]/tbody/tr[7]/td[2]/p/span')[0].text)
        _operating_pressure = fix_encoding("Рабочее давление:" + dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[5]/tbody/tr[8]/td[2]/p/span')[0].text)
        _operating_temperature = fix_encoding("Температура эксплутации:" + dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[5]/tbody/tr[9]/td[2]/p/span')[0].text)
        _stem_thread = fix_encoding("Резьба на штоке:" + dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[14]/tbody/tr['+str(i+2)+']/td[3]')[0].text)
        List_of_data = [_name_object, _standard, _piston_diameter, _stroke_length, _operating_pressure, _operating_temperature, _stem_thread, _url]
        to_csv(List_of_data)

