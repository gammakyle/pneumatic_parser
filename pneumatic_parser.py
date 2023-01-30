from bs4 import BeautifulSoup
from lxml import etree
import requests
from ftfy import fix_encoding
from aircrafter_parser import *
from substring_search import *

_name_object = ""
_stroke_length = ""
_piston_diameter = ""
_operating_pressure = ""
_operating_temperature = ""
_stem_thread = ""
_standard = ""
_url = ""
  

#-------------------------------------#
_HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
#-------------------------------------#

#-------------------------------------#
_datafile = open("data_pages.txt", "r")
while True:
    _url_line = _datafile.readline()
    _url_line = _url_line.strip()
    print(_url_line)
    if not _url_line:
        break
    _url_type = search_substring(_url_line)
    if _url_type == "aircrafter":
        parse_aircrafter(_url_line,_HEADERS)     
    if _url_type == "pneumax":
        _pre_csv_construction = "pneumax - in developing"
    if _url_type == "dalse":
        _pre_csv_construction = "dalse - in developing"
    if _url_type == "industriation":
        _pre_csv_construction = "industriation - in developing"
_datafile.close
#-------------------------------------# substring searching


#-------------------------------------#
