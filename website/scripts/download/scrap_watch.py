import json
import sys

from pprint import pprint
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scrapping_utils import WebScrapper

BASE_URL: str = 'https://www.chrono24.es/search/browse.htm'

series_soup = WebScrapper(BASE_URL).get_soup()

pprint(series_soup)