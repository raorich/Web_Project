import json
import sys

from pprint import pprint
from urllib.parse import urljoin

from scrapping_utils import WebScrapper, GenerateCSV

BASE_URL: str = 'https://classiccars.com/'

FEATURED_LIST = 'classic-cars/featured-listings?ps=60'

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

#GET FEATURED CARS URL
href_list = set()
for page in range(1,5):
    url_plus_page = f"{FEATURED_LIST}&p={page}" if page > 1 else FEATURED_LIST
    series_soup = WebScrapper(urljoin(BASE_URL,url_plus_page), headers=headers, cookies=cookies).get_soup()

    #pprint(series_soup)
    cars_div = series_soup.find_all("div", class_="search-result-item w100 featured")
    for car in cars_div:
        href_list.add(car.find("a").get('href',''))

'''
name -> header
description -> Exterior Color + transmission + (algo del engine)
category -> "car"
starting_price -> price (lleva les ',' llevar '(OBO)', llevar $, "Contact Seller" = 400.000 600.000
reserve_price  -> price
auction_end_time -> x
store -> x
images -> pillar las images

brand -> "Make"
restoration -> Restoration History: 
transmission -> transmission
model -> Model
Engine condition -> "Engine History" + "Engine Condition" 
year -> Year

href_list.add('/listings/view/1894134/1948-plymouth-2-dr-sedan-for-sale-in-vonore-tennessee-37885')
'''

final_data = []
for href in href_list:
    car_soup = WebScrapper(urljoin(BASE_URL,href), headers=headers, cookies=cookies).get_soup()

    ####### IMGS #######

    image_div = car_soup.find("div",class_="swiper-wrapper").find_all("img", class_=["u-photo", "img-fluid"])
    images_url = [WebScrapper.normalizeGetText(ima.get('data-src','')) for ima in image_div]
    images_url = [x for x in images_url if x.strip()]
    
    ##################################

    ####### MORE DETAILS #######
    
    car_detail = car_soup.find("div", class_="vehicle-details").find("ul")
    
    header =  WebScrapper.normalizeGetText(car_detail.find("li", class_=["p-name"]).find("span").getText())

    # PRECIO
    data_soup = car_detail.find("li", class_=["p-price"])
    if data_soup:
        list_span = data_soup.find_all("span")
        price = ""
        if len(list_span) >= 2:
            price  =  WebScrapper.normalizeGetText(list_span[1].getText())

    # EXTERIOR COLOR
    data_soup = car_detail.find("li", class_=["p-color"])
    exterior_color = ""
    if data_soup:
        list_span = data_soup.find_all("span")
        if len(list_span) >= 2:
            exterior_color  =  WebScrapper.normalizeGetText(list_span[1].getText())

    # TRANSMISSION
    data_soup = car_detail.find("li", class_=["p-transmission"])
    transmission = ""
    if data_soup:
        list_span = data_soup.find_all("span")
        if len(list_span) >= 2:
            transmission  =  WebScrapper.normalizeGetText(list_span[1].getText())

    # MODEL
    data_soup = car_detail.find("li", class_=["p-model"])
    model = ""
    if data_soup:
        list_span = data_soup.find_all("span")
        if len(list_span) >= 2:
            model  =  WebScrapper.normalizeGetText(list_span[1].getText())

    # BRAND
    data_soup = car_detail.find("li", class_=["p-manufacturer"])
    brand = ""
    if data_soup:
        list_span = data_soup.find_all("span")
        if len(list_span) >= 2:
            brand  =  WebScrapper.normalizeGetText(list_span[1].getText())

    # YEAR
    data_soup = car_detail.find("li", class_=["dt-start"])
    year = ""
    if data_soup:
        list_span = data_soup.find_all("span")
        if len(list_span) >= 2:
            year  =  WebScrapper.normalizeGetText(list_span[1].getText())

    # ENGINE CONDITION
    data_soup = car_detail.find("li", class_=["p-condition"])
    engine_condition = ""
    if data_soup:
        list_span = data_soup.find_all("span")
        if len(list_span) >= 2:
            engine_condition  =  WebScrapper.normalizeGetText(list_span[1].getText())

    # RESTORATION
    restoration = ""
    for featured in car_detail.find_all("li", class_=["p-feature"]):
        list_span = featured.find_all("span")
        if not len(list_span) >= 2: continue
        if "restoration" in list_span[0].getText().lower():
            restoration  =  WebScrapper.normalizeGetText(list_span[1].getText())
            break
    
    # ENGINE HISTORY
    engine_history = ""
    for featured in car_detail.find_all("li", class_=["border-btm"]):
        list_span = featured.find_all("span")
        if not len(list_span) >= 2: continue
        if "engine history" in list_span[0].getText().lower():
            engine_history  =  WebScrapper.normalizeGetText(list_span[1].getText())
            break

    ##################################

    row = {}
    row["Header"] = header
    row["Price"] =  price
    row["Exterior Color"] =  exterior_color
    row["Transmission"] =  transmission
    row["Restoration"] =  restoration
    row["Model"] =  model
    row["Brand"] =  brand
    row["Engine Condition"] =  f"{engine_history} - {engine_condition}"
    row["Year"] =  year
    row["Imgs"] =  images_url
    final_data.append(row)
    
GenerateCSV("Cars_data_to_upload", final_data).generate()
sys.exit()