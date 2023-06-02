from bs4 import BeautifulSoup
from lxml import etree
import requests
from ftfy import fix_encoding
from csv import writer
import re
from exporter import *

def parse_aircrafter(_url, _HEADERS):   #функция принимающая адрес из коллекции aircrafter
    _webpage = requests.get(_url, headers=_HEADERS)   #формирование страницы
    _soup = BeautifulSoup(_webpage.content, "html.parser")   #выделение заголовков для BS
    for e in _soup.findAll('br'):   #для всех заголовков br
        e.extract()     #убираем вхождения, чтобы в дальнейшем облегчить работу
    _dom = etree.HTML(str(_soup))   #строим dom дерево


    _counter_diameters = fix_encoding("Диаметр поршня:" + _dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[5]/tbody/tr[6]/td[2]/p/span')[0].text) #находим количество диаметров поршня
    _count_nums = len(re.findall(r'\b\d+\b', _counter_diameters)) #очищаем и находим количество диаметров поршня
    _standard = 1 #стандарт изготовления
    _type_movie = 1 #тип перемещения
    _piston_diameter = 1 #диаметр поршня
    _stroke_length = 1 #длина хода
    _operating_pressure = 1 #рабочее давление
    _operating_temperature = 1 #рабочая температура
    _min_temperature = 1 #минимальная рабочая температура
    _max_temperature = 1 #максимальная рабочая температура
    _stem_thread = 1 #разъем подключения
    _name_object = fix_encoding("Aircrafter") #наименование - статичное, ведем разборку страниц aircrafter
    try: #пробуем. Если страница имеет несоответствия, то пропускаем 
        _standard = fix_encoding(_dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[1]/tbody/tr[2]/td/p/span')[0].text) #находим стандарт
        _iso_index = _standard.find("ISO") #ищем тип стандарта - ISO. нахожим индекс, на котором он начинается
        _space_index = _standard.find(" ", _iso_index) #находим пробел после стандарта, чтобы обрезать в дальнейшем
        _bracket_index = _standard.find(")", _iso_index) #находим скобки, для обнаружения вложенных стандартов
        if _bracket_index != -1 and _bracket_index < _space_index: #если скобки есть и они раньше пробела, то 
            word_end_index = _bracket_index #конец вхождения помечаем как индекс скобки
        else: #инача
            word_end_index = _space_index #конец вхождения помечаем как пробел
        _first_word = _standard[_iso_index:word_end_index] #находим начало слова
        if _bracket_index != -1 and _bracket_index > _space_index: # Если индекс закрывающей скобки не равен -1 и больше индекса пробела
            _second_word = _standard[_space_index+1:_bracket_index] #то она находится в первых двух словах, и мы берем второе слово
        else: #Если закрывающая скобка не найдена или находится после первого слова
            _second_word = _standard[_space_index+1:] # то мы берем все слова после первого
        _standard = _first_word + " " + _second_word #Объединяем первое слово и второе в одну строку
        _standard = _standard.replace('"', '') #Удаляем кавычки, точки и запятые из строки
        _standard = _standard.replace('.', '')
        _standard = _standard.replace(',', '')
        _words = _standard.split() #Разбиваем строку на слова при помощи метода split(),
        del _words[2:]
        _standard = ' '.join(_words[:2]) #используя пробелы в качестве разделителей
        _standard = _standard.strip()
        if 'ISO' not in _standard: #если после обработки не осталось ничего подходящего, помечаем как ошибку
            _standard = '1'
    except:
        pass 
    try:
        _operating_pressure = fix_encoding(_dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[5]/tbody/tr[8]/td[2]/p/span')[0].text) 
        #Получаем текст элемента веб-страницы, создавая новую переменную _operating_pressure с помощью функции
        #fix_encoding(), которая исправляет ошибки кодировки в полученном тексте. Мы используем xpath для получения
        #конкретного элемента, на который ссылается адрес в xpath-выражении.
        _numbers_list = re.findall(r'\d+', _operating_pressure)    #Используем регулярное выражение, чтобы выделить из полученной строки все числа, находящиеся в ней
        if _numbers_list:    # Находим максимальное число из всех чисел, находящихся в строке, и обновляем переменную
            _operating_pressure = max([int(num) for num in _numbers_list])    # со значением этого максимального числа
    except:
        pass
    try:
        _operating_temperature = fix_encoding(_dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[5]/tbody/tr[9]/td[2]/p/span')[0].text)
        _numbers = []
        for _word_t in _operating_temperature.split(): # Ищем числа в каждом слове, используя регулярное выражение, и добавляем их в список
            for _match_t in re.findall(r'-?\d+', _word_t):
                _numbers.append(int(_match_t))
        _left_t = [] #Создаем два пустых списка для дальнейшего использования
        _right_t = []

        for i in range(len(_numbers)):
            if i % 2 == 0:  #если индекс числе делиться на два без остатка
                _right_t.append(_numbers[i])  # добавляем число с четным индексом в _right_t
            else:
                _left_t.append(_numbers[i])  # добавляем число с нечетным индексом в _left_t
    except:
        pass
    try:
        _span_elements = _soup.find_all('span', {'style': 'font-size: x-small;'}) #Ищем все элементы <span> на странице, у которых стиль "font-size: x-small"
        _span_texts = [span.text for span in _span_elements] #Создаем новый список _span_text, в котором каждый элемент - это текст из найденных элементов <span>
        for text in _span_texts: #Обходим каждый элемент списка _span_text и ищем, содержатся ли в нем "M1" или "M2"
            if "M1" in text:
                _type_movie = "1"
            elif "M2" in text:
                _type_movie = "2"
            start_index = 5
            end_index = start_index + 3
            _piston_diameter_tmp = text[start_index:end_index] #Затем мы находим диаметр поршня, используя заранее известные индексы начала и конца в строке text.
            if _piston_diameter_tmp.startswith("0"): #Мы также проверяем, не начинается ли диаметр с нуля, и если да, то удаляем его.
                _piston_diameter_tmp = _piston_diameter_tmp[1:]
            _piston_diameter = _piston_diameter_tmp
            try:
                for m in range (10): # Пробуем получить значение диаметра поршня из таблицы с помощью xpath-выражения, используя переменную
                    try:
                        _tmp_diameter = fix_encoding(_dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[14]/tbody/tr['+str(m+1)+']/td[1]')[0].text)
                        if _piston_diameter == _tmp_diameter: # Если значение диаметра из таблицы соответствует переменной _piston_diameter, то мы получаем значение # резьбы стержня из таблицы, используя тот же метод xpath и сохраняем его в переменную _stem_thread. 
                            _stem_thread = fix_encoding(_dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[14]/tbody/tr['+str(m+1)+']/td[3]')[0].text)
                            if "M" in _stem_thread: # Если резьба уже имеет формат "M", мы сохраняем ее без изменений, иначе мы получаем значение из другого поля
                                _stem_thread=_stem_thread
                            else:
                                _stem_thread = fix_encoding(_dom.xpath('//*[@id="vmMainPage"]/table/tbody/tr[3]/td/table[14]/tbody/tr['+str(m+1)+']/td[14]')[0].text)
                    except:
                        pass
            except:
                pass
            start_index = 9 #Определяем переменную start_index со значением 9 и end_index, равный start_index плюс 4.
            end_index = start_index + 4
            _stroke_length_tmp = text[start_index:end_index] #Затем мы извлекаем составляющие строки, начиная с индекса start_index и заканчивая индексом end_index
            if _stroke_length_tmp.startswith("0"): #Если сочетание символов, начинающееся с _stroke_length_tmp, начинается с "0", мы удаляем начальный "0" и сохраняем новое значение в _stroke_length_tmp
                _stroke_length_tmp = _stroke_length_tmp[1:] #Затем мы заменяем все запятые в резьбе стержня на точки (с помощью метода replace()).
            _stroke_length = _stroke_length_tmp
            _stroke_length = _stroke_length.lstrip('0') #Наконец, мы удаляем все нули слева (если они есть) и сохраняем значение в переменную _stroke_length.
            _stem_thread = _stem_thread.replace(',', '.') 
            for k in range(len(_left_t)): #После этого мы запускаем цикл for для переменной k, проходя по диапазону от 0 до длины списка _left_t. 
                List_of_data = [_name_object, _standard, "1", _type_movie, _piston_diameter, _stroke_length, _operating_pressure, _right_t[k], _left_t[k], _stem_thread, _url]
                to_csv(List_of_data) #передаем для цилиндра одностороннего действия
                List_of_data = [_name_object, _standard, "2", _type_movie, _piston_diameter, _stroke_length, _operating_pressure, _right_t[k], _left_t[k], _stem_thread, _url]
                to_csv(List_of_data)#передаем для цилиндра двустороннего действия
    except:
        pass



