import json
import sys
import time

from pprint import pprint
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scrapping_utils import WebScrapperSelenium, WebScrapper, GenerateCSV

BASE_URL: str = 'https://www.chrono24.es/'

CLASS_COOKIES: str = 'wt-main-content'
LOCATOR: str = 'class'

series_soup = WebScrapperSelenium(urljoin(BASE_URL,'search/browse.htm'), element_name = CLASS_COOKIES, locator = LOCATOR).get_soup()

#extract cells
div_cell = "flickity-slider"
divs = series_soup.find_all("div",div_cell)[1]

#for each brand get the url filter
urls_to_check = {}
for div in divs:
    next_url = div.find('a','rcard').get('href')
    name = div.find('h3').getText().strip().replace('/n','')
    urls_to_check.setdefault(name,urljoin(BASE_URL,next_url))

#for each watch get the data
final_data = []
for category, url in urls_to_check.items():
    category_soup = WebScrapperSelenium(url, element_name =  CLASS_COOKIES, locator = LOCATOR).get_soup()
    if category_soup is None:
        time.sleep(5)
        continue

    watches_soup = category_soup.find_all("div", "js-article-item-container")[:20]
    
    for watch in watches_soup:
        inside_watch_url = watch.find("a").get('href','')
        watch_soup = WebScrapperSelenium(urljoin(BASE_URL, inside_watch_url), element_name =  CLASS_COOKIES, locator = LOCATOR).get_soup()
        if watch_soup is None:
            time.sleep(5)
            continue
        ####### HEADER & SUBHEADER #######
        headers = watch_soup.find("h1").find_all('span')
        headers[1].extract()
        header = WebScrapper.normalizeGetText(headers[0].getText())
        subheader = WebScrapper.normalizeGetText(headers[1].getText())
        ##################################

        ####### CASE & DOCUMENTATION #######

        price_div = watch_soup.find("div", class_="detail-page-price")
        documentation = price_div.find_previous()
        condition = documentation.find_previous()
        documentation = WebScrapper.normalizeGetText(documentation.getText())
        condition = WebScrapper.normalizeGetText(condition.getText())

        ##################################

        ####### IMGS #######

        image_div = watch_soup.find_all("div", class_="watch-image-carousel-image")
        images_url = [WebScrapper.normalizeGetText(ima.get('data-zoom-image','')) for ima in image_div]

        ##################################

        ####### MORE DETAILS #######
        tbody_details = watch_soup.find("section", class_="js-details-and-security-tabs").find("tbody")
        all_tr = tbody_details.find_all("tr")

        translate_key = {
            "Precio" : "Price",
            "(Reloj) Modelo": "Model",
            "Estado" : "Condition",
            "Año de fabricación" : "Year"
        }
        details = {
            "Price" : {
                "value": "",
                "done" : False
            },
            "Model" : {
                "value": "",
                "done" : False
            },
            "Condition" : {
                "value": "",
                "done" : False
            },
            "Year" : {
                "value": "",
                "done" : False
            }
        }
        for tr in all_tr:
            if all(v.get("done") for v in details.values()):
                break
            all_td = tr.find_all("td")
            if len(all_td) < 2: continue
            td_key = all_td[0].getText()
            if td_key in translate_key:
                details[translate_key.get(td_key)]["value"] = WebScrapper.normalizeGetText(all_td[1].getText())
                details[translate_key.get(td_key)]["done"] = True
        
        ##################################

        row = {}
        row["Header"] = header
        row["SubHeader"]  =  subheader
        row["Brand"] =  category
        row["Documentation"] =  documentation
        row["Case"] =  condition
        row["Price"] =  details.get("Price",{}).get("value")
        row["Model"] =  details.get("Model",{}).get("value")
        row["Condition"] =  details.get("Condition",{}).get("value")
        row["Year"] =  details.get("Year",{}).get("value")
        row["Imgs"] =  images_url

        final_data.append(row)
        
#Save_File
GenerateCSV("Watches_data", final_data).generate()