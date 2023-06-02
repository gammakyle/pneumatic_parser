from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
import requests
from ftfy import fix_encoding
from csv import writer
import re
import gc
from exporter import *

def parse_indestriation(_url, _HEADERS): #функция принимающая адрес из коллекции индустриэйшн 
    key_stopper = 0 #ключ для остановки парсинга
    _num_page = 1 #номер страницы
    _standard = "" #стандарт
    while (key_stopper !=1): #пока страницы существуют
        _url_now = _url.replace('#',str(_num_page)) #теккуюий адрес - адрес с номером страницы
        _webpage = requests.get(_url_now, headers=_HEADERS) #формирование страницы
        _soup = BeautifulSoup(_webpage.content, "html.parser") #выделение заголовков для BS
        _dom = etree.HTML(str(_soup)) #строим dom дерево
        try:
            for _num_card in range (1,49): #просматриваем части карточки от 1 до 49
                if(_num_card != 7 and _num_card !=42): #исключаем карточки 7 и 42 - это реклама
                    try:
                        _link_down = ('/html/body/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[4]/div[1]/div[%d]/div/div[1]/a/@href' %_num_card)
                        _url_link_down = fix_encoding(_dom.xpath(_link_down)[0])
                    except:
                        pass
                    print(_url_link_down)
                    try:
                        _webpage_down = requests.get(_url_link_down, headers=_HEADERS)
                        _soup_down = BeautifulSoup(_webpage_down.content, "html.parser")
                        _dom_down = etree.HTML(str(_soup_down))
                        _name_object = fix_encoding(_dom_down.xpath('/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div[1]/div[3]/div/div[2]/div[3]/div[2]/div/a')[0].text).replace("\t", "")
                        _standard = 1 #стандарт изготовления
                        _piston_diameter = 1 #диаметр поршня
                        _type_cylinder = 1 #тип цилиндра
                        _type_movie = 1 #тип передвижения
                        _stroke_length = 1 #длина хода
                        _operating_pressure = 1 #рабочее давление
                        _operating_temperature = 1 #рабочая температура
                        _left_value, _right_value = None, None #минимальная и максимальная рабочая температура
                        _stem_thread = 1 #разъем подключения
                        try:
                            #стандарт
                            for i in range(3,50):
                                for j in range (10):
                                    try:
                                        if("Группа" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))): #если нашли "группа" в ячейках таблицы то 
                                            _standard = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "") #берем показатель из второго столбца
                                            if "ISO" in _standard: #если была найдена подстрока ИСО то
                                                index = _standard.find("ISO") #записываем индекс этого символа
                                                if _standard[index+3] != " ": #если через три символа после начала нет пробела
                                                    _standard = _standard.replace("ISO", "ISO ") #то пробел ставим
                                    except:
                                        pass
                                if _standard == 1:
                                    for i in range(3,50): #если группу не нашли, то можем попробовать найти локальный стандарт 
                                        for j in range (10): 
                                            try:
                                                if("тандарт" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))): #если находим стандарт то
                                                    _standard = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "") #берем показатель из второго столбца
                                                    if "IDO" in _standard: #если находим стандарт ИДО
                                                        index = _standard.find("IDO") #находим индекс начального символа 
                                                        if _standard[index+3] != " ": #если пробела через три символа нету то 
                                                            _standard = _standard.replace("IDO", "IDO ") #добавляем пробел после начала стандарта
                                            except:
                                                pass
                            #тип цилиндра
                            for i in range(3,50):
                                for j in range (10):
                                    try:
                                        if("ип шток" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))): #далее по образцу как в предыдущих
                                            _type_cylinder = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div/a")[0].text).replace("\n", "").replace("\t", "")                                                   
                                            if "дносторонy" in _type_cylinder: #если нашли подстроку определяющую как односторонний шток, то пишем как 1
                                                _type_cylinder = "1"
                                            else:
                                                _type_cylinder = "2" 
                                    except:
                                        pass
                            #принцип действия
                            for i in range(3,50):
                                for j in range (10):
                                    try:
                                        if("ип действ" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _type_movie = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div/a")[0].text).replace("\n", "").replace("\t", "")
                                            if "вусторонн" in _type_movie:
                                                _type_movie = "1"
                                            else:
                                                _type_movie = "2" 
                                    except:
                                        pass
                                    
                            #диаметр поршня
                            for i in range(3,50):
                                for j in range (10):
                                    try:
                                        if("Диаметр поршня" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _piston_diameter = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "")
                                    except:
                                        pass
                            for i in range(3,50):
                                for j in range (10): 
                                    try:
                                        if("Диаметр поршня" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _piston_diameter = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div/a")[0].text).replace("\n", "").replace("\t", "")
                                    except:
                                        pass
                            #длина хода
                            for i in range(3,50):
                                for j in range (10):
                                    try:
                                        if("Ход" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _stroke_length = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "")
                                    except:
                                        pass
                            #рабочее давление
                            for i in range(3,50):
                                for j in range (10):
                                    try:
                                        if("Максимальное рабочее давление" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _operating_pressure = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "")
                                    except:
                                        pass
                            #температура эксплутации
                            _left_value, _right_value = None, None
                            for i in range(3,50):
                                for j in range (10):
                                    try:
                                        if("емператур" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _operating_temperature = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "")
                                            _operating_temperature = _operating_temperature.replace('°', '') #убираем лишние символы 
                                            _operating_temperature = _operating_temperature.replace('C', '')
                                            _operating_temperature = _operating_temperature.replace('+', '')
                                            for _word in _operating_temperature.split():
                                                if _word.lstrip('-').isdigit():  # удаляем знак минуса и проверяем, является ли слово числом
                                                    if _left_value is None:
                                                        _left_value = int(_word)  # записываем числа без знака
                                                    else:
                                                        _right_value = int(_word)

                                                        if '-' in _operating_temperature[_operating_temperature.index(_word)-1]:  # если знак отрицательный, меняем знак числа на противоположный
                                                            _right_value *= -1
                                                        break
                                    except:
                                        pass
                            #резьба на штоке
                            for i in range(3,50):
                                '''
                                for j in range (10):
                                    try:
                                        if("Монтажные отверстия" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _stem_thread = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "")
                                    except:
                                        pass
                                for j in range (10):
                                    try:
                                        if("Монтажные отверстия" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _stem_thread = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "")
                                    except:
                                        pass
                                '''
                                for j in range (10):
                                    try:
                                        if("езьба" in (fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[1]/span")[0].text).replace("\n", ""))):
                                            _stem_thread = fix_encoding(_dom_down.xpath("/html/body/div[3]/div[2]/itemproduct/div[2]/div[1]/div["+str(j)+"]/div[2]/div["+str(i)+"]/div[2]/div")[0].text).replace("\n", "").replace("\t", "")
                                    except:
                                        pass  
                        except:                                  
                            pass
                        _name_object = re.sub("^\s+|\n|\r|\s+$", '', _name_object)
                        _piston_diameter = _piston_diameter.replace(' мм', '') #убираем лишние символы, заменяем запятые
                        _stroke_length = _stroke_length.replace(' мм', '')
                        _operating_pressure = _operating_pressure.replace(' бар', '')
                        _operating_pressure = _operating_pressure.replace(' Бар', '')
                        _stem_thread = _stem_thread.replace(',', '.')
                        _stem_thread = _stem_thread.replace(' мм', '')
                        print(_left_value)
                        print(_right_value)

                        List_of_data = [_name_object, _standard, _type_cylinder, _type_movie, _piston_diameter, _stroke_length, _operating_pressure, _left_value, _right_value, _stem_thread, _url_link_down]
                        to_csv(List_of_data) #добавляем в список на добавление в таблицу 
                    except:
                        pass
        except:
             key_stopper=1 
        _num_page += 1
        gc.collect()