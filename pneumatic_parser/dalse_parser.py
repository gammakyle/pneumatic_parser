from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
import requests
from ftfy import fix_encoding
from csv import writer
import re
from exporter import *

def parse_dalse(_url, _HEADERS): #функция принимающая адрес из коллекции dalse
    key_stopper = 0 #ключ для остановки парсинга
    _num_page = 1 #номер страницы
    _standard = "" #стандарт
    while (key_stopper !=1): #пока страницы существуют
        if _num_page==1: #если номер страницы 1 то 
            _url_now = _url #устанавливаем текущую ссылку как переданную
        else:
            _url_now = _url+";"+str(_num_page) #иначе как ссылку с параметром страницы
        _webpage = requests.get(_url_now, headers=_HEADERS) #формирование страницы
        _soup = BeautifulSoup(_webpage.content, "html.parser")  #выделение заголовков для BS
        _dom = etree.HTML(str(_soup))  #строим dom дерево
        try:
            for _num_card in range (1,51): #просматриваем части карточки от 1 до 51
                try:
                    _link_down = ('/html/body/div[6]/div/div[3]/div/div[%d]/div/table/tbody/tr/td[2]/span/a/@href' %_num_card)
                    _url_link_down = fix_encoding("http://dalse.ru"+_dom.xpath(_link_down)[0])
                    print(_url_link_down)
                except:
                    return 1
                try:
                    _webpage_down = requests.get(_url_link_down, headers=_HEADERS)
                    _soup_down = BeautifulSoup(_webpage_down.content, "html.parser")
                    f = open('Output.txt', 'w')
                    f.write(str(_soup_down))
                    f.close()
                    _dom_down = etree.HTML(str(_soup_down))
                    _name_object = ("festo") #имена везде фесто, они на этом специализируются
                    _standard = 1 #стандарт изготовления
                    _piston_diameter = 1 #диаметр поршня
                    _stroke_length = 1 #длина хода
                    _operating_pressure = 1 #рабочее давление
                    _operating_temperature = 1 #рабочая температура
                    _type_cylinder = 1 #тип цилиндра
                    _type_movie = 1 #тип перемещения
                    _left_value = None #минимальная рабочая температура
                    _right_value = None #максимальная рабочая температура
                    _stem_thread = 1 #разъем подключения
                    try:
                        try:
                            _standard = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[6]/td[2]')[0].text).replace("\n", "").replace("\t", "") #находим вхождение стандарта
                            _key = "ISO" #ключевое слово для поиска
                            if _key in _standard: #если оно найдено в строке стандарта
                                _words = _standard.split()  #разделяем слова
                                _standard = ' '.join(_words[:2]) #удаляем все слова после второго
                            else:
                                _standard = "1" #иначе выводим исключение
                        except:
                            pass
                        try:
                            _piston_diameter = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[2]/td[2]')[0].text).replace("\n", "").replace("\t", "") #находим диаметр поршня
                            for _word in _piston_diameter.split(): #для каждого слова разделенного пробелами
                                if _word.isdigit(): #если оно является числом, то 
                                    _piston_diameter = _word #записываем его как диаметр
                                    break
                        except:
                            pass
                        try:
                            _stroke_length = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[1]/td[2]')[0].text).replace("\n", "").replace("\t", "") #находим длину поршня
                            for _word in _stroke_length.split(): #для каждого слова разделенного пробелами
                                if _word.isdigit(): #если оно число то
                                    _stroke_length = _word #щаписываем как длину поршня
                                    break
                        except:
                            pass
                        try:
                            _type_cylinder = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[10]/td[2]')[0].text).replace("\n", "").replace("\t", "") #определяем тип штока
                            if "дносторонний шток" in _type_cylinder: #если в строке есть вхождение как "дносторонний шток"
                                _type_cylinder = "1" #помечаем как одностороннего действия
                            else: 
                                _type_cylinder = "2"  #иначе как двустороннего
                        except:
                            pass
                        try:
                            _type_movie = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[12]/td[2]')[0].text).replace("\n", "").replace("\t", "") #находим тип действия
                            if "двустороннего действия" in _type_movie: #если находим ключевое слово
                                _type_movie = "2" #то помечаем как двустороннего действия
                            else:
                                _type_movie = "1"  #иначе одностороннего 
                        except:
                            pass
                        try:
                            _operating_pressure = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[11]/td[2]')[0].text).replace("\n", "").replace("\t", "") #находим рабочее давление
                            _numbers = re.findall(r'\d+', _operating_pressure)   #находим все числа в строке
                            if _numbers: 
                                _operating_pressure = re.search(r'\d+$', _numbers[-1]).group() #находим последнее число и заносим в список 
                        except:
                            pass
                        try:
                            _left_value, _right_value = None, None
                            _operating_temperature = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[16]/td[2]')[0].text).replace("\n", "").replace("\t", "")
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
                        try:
                            _stem_thread = fix_encoding(_dom_down.xpath('/html/body/div[6]/div/div[3]/table/tbody/tr[3]/td[2]')[0].text).replace("\n", "").replace("\t", "") #получаем информацию о типе разъема, попутно исправляя кодировку
                            _stem_thread = _stem_thread.replace(',', '.') #переводим запятые в точки
                            _stem_thread = _stem_thread.replace(' ', '') #очищаем от лишних пробелов
                        except:
                            pass
                    except:
                        pass
                    _name_object = re.sub("^\s+|\n|\r|\s+$", '', _name_object) #очищаем от переносов и т.д.
                    List_of_data = [_name_object, _standard, _type_cylinder, _type_movie, _piston_diameter, _stroke_length, _operating_pressure, _left_value, _right_value, _stem_thread, _url_link_down]
                    to_csv(List_of_data) #выводи в функцию экспорта
                except:
                    pass
        except:
            key_stopper=1 #"обнуление" ключа остановки
        _num_page += 1 #прибавление номера страницы
