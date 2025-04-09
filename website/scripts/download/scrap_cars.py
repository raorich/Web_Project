import json
import sys

from pprint import pprint
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scrapping_utils import WebScrapper

BASE_URL: str = 'https://classiccars.com/'

cookies = {
    '_cctkn_': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1bmlxdWVfbmFtZSI6IkFub255bW91cyBVc2VyIiwianRpIjoiZDVjZDRkYTAtNmEwOC00ZTU2LTg3OTEtNzljMTFhMzhjMjMwIiwiaWF0IjoiMTc0NTI1OTI4NC45MzY5NCIsImlzcyI6IkNsYXNzaWNDYXJzLmNvbSIsImF1ZCI6IkFueSIsImV4cCI6MTc0NTI1OTI4NCwibmJmIjoxNzQ0MDQ5Njg0fQ.8o9lJy7wNF411YnuwNc5TczrIobmd0MqhIo9HZYy7Vk',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-ES,es;q=0.9,ca-ES;q=0.8,ca;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

series_soup = WebScrapper(BASE_URL, headers=headers, cookies=cookies).get_soup()

slick_list = series_soup.find("div", id="FSBOslider").find_all("div", class_="fsbo-slider")
pprint(series_soup)