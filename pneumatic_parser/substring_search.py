import re

def search_substring(_url_line): #функция обнаружения типа страницы
    to_find = re.compile("aircrafter|pneumax|dalse|industriation") #создаем лист образцов, на которых может работать парсер
    _url_type = to_find.search(_url_line) #если находится один из образцов записываемтся в тип ссылки
    return(_url_type.group()) #возвращаем тип сайта