import datetime
import re
import os
import requests
import hashlib

from urllib.request import Request, urlopen
from pathlib import Path

#----------------------------------------------------------------
# L o g g e r
#----------------------------------------------------------------
import logging
log_format = '%(asctime)s - {%(filename)s:%(lineno)d} - %(levelname)s: %(message)s'
logger = logging
logger.basicConfig(format=log_format, datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

#----------------------------------------------------------------
# F i l  e s
#----------------------------------------------------------------

def request_url_get(url, name='', force=True):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
        'AppleWebKit/537.11 (KHTML, like Gecko) '
        'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    req = Request(url=url, headers=headers)
    
    return urlopen(req).read() 


def create_file_dir(file):
    outdir = os.path.dirname(file)

    if not os.path.exists(outdir): 
        output_dir = Path(outdir)

        print("Creating folder: {}".format(outdir))
        output_dir.mkdir(parents=True, exist_ok=True)

#----------------------------------------------------------------
# S t r i n g s
#----------------------------------------------------------------

def convert_na(text):
    if text == 'NA':
        return ''
    
    return text


def strip_accents(text):
    
    rep = {
        "Á": 'A', 
        "É": 'E',
        "Í": 'I',
        "Ó": 'O',
        "Ú": 'U'
    }

    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile('|'.join(rep.keys()))

    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

    return text


# https://stackoverflow.com/questions/15325182/how-to-filter-rows-in-pandas-by-regex
def regex_filter(val, regex):
    if val:
        mo = re.search(regex, val, re.IGNORECASE)
        if mo:
            return True

    return False    


#----------------------------------------------------------------
# D a t e
#----------------------------------------------------------------

# replacing excel dates
# see: https://stackoverflow.com/questions/14271791/converting-date-formats-python-unusual-date-formats-extract-ymd
def get_fixed_date(text):
    if not is_date_in_excel_format(text):
        return text
    
    match = re.search(r'(\d{5})', text)
    m = match.group().replace(' ', '').replace(',', '')
    delta = datetime.timedelta(int(m)-2)
    date = datetime.date(1900, 1, 1) + delta
    date = str(date.strftime('%d/%m/%Y'))
    
    return date


def is_date_in_excel_format(text):
    return re.search(r'(\d{5})', text)


def interpolate_date(string, year, month, day):
    string = re.sub(r'{{Y}}', year, string)
    string = re.sub(r'{{y}}', str(year)[-2:], string)
    string = re.sub(r'{{m}}', month, string)
    string = re.sub(r'{{d}}', day, string)

    return string

#----------------------------------------------------------------
# C o n t e x t
#----------------------------------------------------------------

def genders():
    return ['M', 'F', 'MASCULINO', 'FEMENINO']


def mx_states():
    # see https://en.wikipedia.org/wiki/Template:Mexico_State-Abbreviation_Codes
    return {
        'AGUASCALIENTES': 'AGU',
        'BAJA CALIFORNIA': 'BCN',
        'BAJA CALIFORNIA SUR': 'BCS',
        'CAMPECHE': 'CAM',
        'CHIAPAS': 'CHP',
        'CHIHUAHUA': 'CHH',
        'COAHUILA': 'COA',
        'COLIMA': 'COL',
        'CIUDAD DE MÉXICO': 'CMX',
        'CIUDAD DE MEXICO': 'CMX',
        'DISTRITO FEDERAL': 'CMX',
        'DURANGO': 'DUR',
        'GUANAJUATO': 'GUA',
        'GUERRERO': 'GRO',
        'HIDALGO': 'HID',
        'JALISCO': 'JAL',
        'MEXICO': 'MEX',
        'MICHOACAN': 'MIC',
        'MORELOS': 'MOR',
        'NAYARIT': 'NAY',
        'NUEVO LEON': 'NLE',
        'OAXACA': 'OAX',
        'PUEBLA': 'PUE',
        'QUERETARO': 'QUE',
        'QUINTANA ROO': 'ROO',
        'SAN LUIS POTOSI': 'SLP',
        'SINALOA': 'SIN',
        'SONORA': 'SON',
        'TABASCO': 'TAB',
        'TAMAULIPAS': 'TAM',
        'TLAXCALA': 'TLA',
        'VERACRUZ': 'VER',
        'YUCATAN': 'YUC',
        'ZACATECAS': 'ZAC'
    }


def es_months():
    return {
        'enero': '01',
        'febrero': '02',
        'marzo': '03',
        'abril': '04',
        'mayo': '05',
        'junio': '06',
        'julio': '07',
        'agosto': '08',
        'septiembre': '09',
        'octubre': '10',
        'noviembre': '11',
        'diciembre': '12'
    }    


def world_countries():
    return [
        'ESTADOS UNIDOS',
        'REPUBLICA CHECA'
    ]


def is_mx_state(state):
    state = strip_accents(state.upper())

    return state in mx_states().keys()


def get_iso_from_state(state):
    state = strip_accents(state.upper())
    
    return mx_states().get(state, state)


def is_known_country(country):
    country = strip_accents(country.upper())

    return country in world_countries()