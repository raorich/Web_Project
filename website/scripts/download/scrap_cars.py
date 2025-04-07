import json
import sys

from pprint import pprint
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scrapping_utils import WebScrapper

BASE_URL: str = 'https://classiccars.com/'

series_soup = WebScrapper(BASE_URL).get_soup()

pprint(series_soup)