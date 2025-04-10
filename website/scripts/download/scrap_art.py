import json
import sys
import time

from pprint import pprint
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scrapping_utils import WebScrapperSelenium, WebScrapper, GenerateCSV

#ArtsyPro
#ArtsyPro123

#generateTokken
"""
curl -v -X POST "https://api.artsy.net/api/tokens/xapp_token?client_id=c0031a32cfa5b8c0d57c&client_secret=a214536fbb0e8deece112a0eb121abf7"
"""

BASE_URL: str = 'https://api.artsy.net/api/artworks'
TOKKEN = "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6IiIsInN1YmplY3RfYXBwbGljYXRpb24iOiIxMDYyNTc3Zi1jZmM1LTQ2NzEtOGE1Ni1hMDRkNzViNDU2N2YiLCJleHAiOjE3NDQ4ODk5NTUsImlhdCI6MTc0NDI4NTE1NSwiYXVkIjoiMTA2MjU3N2YtY2ZjNS00NjcxLThhNTYtYTA0ZDc1YjQ1NjdmIiwiaXNzIjoiR3Jhdml0eSIsImp0aSI6IjY3ZjdhZGUzYjYwODhkMDAxMDFkMTA0NSJ9.LYFAW4_hKiBF3hT4nzNiHzw5xncwiPNe7zVxrz1fMc8"
HEADERS = {
    'X-XAPP-Token': TOKKEN,
}
series_soup = WebScrapper(BASE_URL, headers=HEADERS).get_soup()

pprint(series_soup)
sys.exit()

curl -v "https://api.artsy.net/api/artworks" -H "X-XAPP-Token: eyJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6IiIsInN1YmplY3RfYXBwbGljYXRpb24iOiIxMDYyNTc3Zi1jZmM1LTQ2NzEtOGE1Ni1hMDRkNzViNDU2N2YiLCJleHAiOjE3NDQ4ODk5NTUsImlhdCI6MTc0NDI4NTE1NSwiYXVkIjoiMTA2MjU3N2YtY2ZjNS00NjcxLThhNTYtYTA0ZDc1YjQ1NjdmIiwiaXNzIjoiR3Jhdml0eSIsImp0aSI6IjY3ZjdhZGUzYjYwODhkMDAxMDFkMTA0NSJ9.LYFAW4_hKiBF3hT4nzNiHzw5xncwiPNe7zVxrz1fMc8"


