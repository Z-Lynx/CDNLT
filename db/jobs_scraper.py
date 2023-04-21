import sys
import os
scraper_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(scraper_path)

import time
from db.address_scraper import *
from bs4 import BeautifulSoup
import re
import json
from db.database_utils import insert_data
from tqdm import tqdm


def next_page(referer):
    request = requests.get(referer, headers=utils.get_header(referer=referer))

    try:
        soup = BeautifulSoup(request.text, 'html.parser')

        if soup.find(class_='pagination').find_all('a')[-1]['href']:
            return soup.find(class_='pagination').find_all('a')[-1]['href']
        return None
    except Exception as e:
        return None


def processing(referer):
    while True:
        id_number = re.search(r'\d+', referer).group(0)
        page_num = re.findall(r'trang-(\d+)', referer)
        if not page_num:
            page_num = "0"
        else:
            page_num = page_num[0]
        data_one = 'a:2:{s:4:"PAGE";s:' + str(len(page_num)) + ':"'+page_num+'";s:8:"LOCATION";s:' + str(len(id_number)) + ':"'+id_number+'";}'

        data = {
            'dataOne': data_one,
            'dataTwo': 'a:0:{}',
        }

        response = requests.post('https://careerbuilder.vn/search-jobs', headers=utils.get_header(referer=referer), data=data)
        response.encoding = 'ISO-8859-1'

        list_data_response = json.loads(response.text)['data']
        for data_response in list_data_response:
            insert_data(data_response)

        referer = next_page(referer)
        if referer == "javascript:void(0);" or referer is None:
            break


def get_data():
    list_id_country = get_id_address()
    for country in tqdm(list_id_country):
        try:
            print("\n\n[+] " + country.split("/")[-1].split('.')[0])
            processing(country)
            time.sleep(2)
        except Exception as e:
            print("\n\n[+] Máy Chủ " + country.split("/")[-1].split('.')[0] + " Sập !!")


if __name__ == '__main__':
    get_data()
    # Debug
    pass