import re

def search_substring(_url_line):
    to_find = re.compile("aircrafter|pneumax|dalse|industriation")
    _url_type = to_find.search(_url_line)
    return(_url_type.group())