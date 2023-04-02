import requests
import scraper.utils as utils
from bs4 import BeautifulSoup
import re


def processing_data(data):
    soup = BeautifulSoup(data, 'html.parser')

    list_jobs_country = soup.find('ul', class_='list-jobs-by-country')
    list_id_country = []
    for country in list_jobs_country.find_all('a'):
        list_id_country.append(country['href'])

    return list_id_country


def get_id_address():
    request = requests.get("https://careerbuilder.vn/tim-viec-lam.html", headers=utils.get_header(referer='https://careerbuilder.vn/tim-viec-lam.html'))

    if request.status_code == 200:
        return processing_data(request.text)
    return None


if __name__ == '__main__':
    get_id_address()