import time

import requests
import scraper.utils as utils
from scraper.address_scraper import *
from bs4 import BeautifulSoup
import re
import json
from database.process_data import insert_data
from tqdm import tqdm


def next_page(referer):
    request = requests.get(referer, headers=utils.get_header(referer=referer))

    try:
        soup = BeautifulSoup(request.text, 'html.parser')

        if soup.find(class_='pagination').find_all('a')[-1]['href']:
            return soup.find(class_='pagination').find_all('a')[-1]['href']
        return None
    except Exception as e:
        print(e)
        print(referer)


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
    for country in tqdm(list_id_country[11:]):
        print("[+] " + country.split("/")[-1].split('.')[0] )
        processing(country)
        time.sleep(2)


if __name__ == '__main__':
    get_data()