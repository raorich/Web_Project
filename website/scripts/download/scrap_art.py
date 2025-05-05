import json
import sys
import time
import random

from pprint import pprint
from urllib.parse import urljoin

from scrapping_utils import WebScrapper, WebScrapperSelenium, GenerateCSV

#NOT USED
#https://metmuseum.github.io/
#https://collectionapi.metmuseum.org/public/collection/v1/objects
#BASE_URL: str = 'https://collectionapi.metmuseum.org/'
#ALL_OBJECTS: str = '/public/collection/v1/objects'

cookies = {
    'currency': '43700947.EUR',
    'country': '43700947.ES',
    'bsId': 'szp4gqw_D6vABpZZwouxKRk2tf4aSwk0EgRStu2ejFQ%3D.eyJpZCI6MzUxNjg3MTE2OH0%3D',
    'AWSSGLB': '3133404583',
    'campaign_id': '61',
    'SGSID': '9tsappav5u4jkg4vf5j05b2fri',
    'aws-waf-token': '14b6cc54-d072-443b-8e2b-20fe1ab2fb61:CQoAsE12R+EfAgAA:PFpXXlBAG2/d0qOZT8jrjUbcuuHkSjeshWaUsl1G9A8q6A2iE9enNKeZUP3OnKg7Vr2pW2QZx9ys4k6kOpuUcmqrTwIZciVbzxfy5Fzawb76uRJPCCftXXeIXUSzMoEQuvxTWHs9hKMCOmBUPPsAN8vnyZ0ardw5I8FXDgxa+akdDQcbzbEcVtogMDQlUQB0GM1Wt/Cep2NSu8SmgsFEq5tzGAOY6XU=',
    'AWSALB': 'A13ES1XYtIMerPaqlqd5nuqEr5LlS6CE6i36E7JMGeo7IzN+QT4DteHnF4stnbx6IjjklYy5eHK3mYWFmFgqYB+iWHDEwbUj8uEBMx00lmkylWhkqG9zH36KRgk4',
    'AWSALBCORS': 'A13ES1XYtIMerPaqlqd5nuqEr5LlS6CE6i36E7JMGeo7IzN+QT4DteHnF4stnbx6IjjklYy5eHK3mYWFmFgqYB+iWHDEwbUj8uEBMx00lmkylWhkqG9zH36KRgk4',
}

cookies = [
    {'name': 'currency', 'value': '43700947.EUR', 'domain': 'www.singulart.com'},
    {'name': 'country', 'value': '43700947.ES', 'domain': 'www.singulart.com'},
    {'name': 'bsId', 'value': 'szp4gqw_D6vABpZZwouxKRk2tf4aSwk0EgRStu2ejFQ%3D.eyJpZCI6MzUxNjg3MTE2OH0%3D', 'domain': 'www.singulart.com'},
    {'name': 'AWSSGLB', 'value': '3133404583', 'domain': 'www.singulart.com'},
    {'name': 'campaign_id', 'value': '61', 'domain': 'www.singulart.com'},
    {'name': 'SGSID', 'value': '9tsappav5u4jkg4vf5j05b2fri', 'domain': 'www.singulart.com'},
    {'name': 'aws-waf-token', 'value': '14b6cc54-d072-443b-8e2b-20fe1ab2fb61:CQoAsE12R+EfAgAA:PFpXXlBAG2/d0qOZT8jrjUbcuuHkSjeshWaUsl1G9A8q6A2iE9enNKeZUP3OnKg7Vr2pW2QZx9ys4k6kOpuUcmqrTwIZciVbzxfy5Fzawb76uRJPCCftXXeIXUSzMoEQuvxTWHs9hKMCOmBUPPsAN8vnyZ0ardw5I8FXDgxa+akdDQcbzbEcVtogMDQlUQB0GM1Wt/Cep2NSu8SmgsFEq5tzGAOY6XU=', 'domain': 'www.singulart.com'},
    {'name': 'AWSALB', 'value': 'A13ES1XYtIMerPaqlqd5nuqEr5LlS6CE6i36E7JMGeo7IzN+QT4DteHnF4stnbx6IjjklYy5eHK3mYWFmFgqYB+iWHDEwbUj8uEBMx00lmkylWhkqG9zH36KRgk4', 'domain': 'www.singulart.com'},
    {'name': 'AWSALBCORS', 'value': 'A13ES1XYtIMerPaqlqd5nuqEr5LlS6CE6i36E7JMGeo7IzN+QT4DteHnF4stnbx6IjjklYy5eHK3mYWFmFgqYB+iWHDEwbUj8uEBMx00lmkylWhkqG9zH36KRgk4', 'domain': 'www.singulart.com'},
]

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-ES,es;q=0.9,ca-ES;q=0.8,ca;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'currency=43700947.EUR; country=43700947.ES; bsId=szp4gqw_D6vABpZZwouxKRk2tf4aSwk0EgRStu2ejFQ%3D.eyJpZCI6MzUxNjg3MTE2OH0%3D; AWSSGLB=3133404583; campaign_id=61; SGSID=9tsappav5u4jkg4vf5j05b2fri; aws-waf-token=14b6cc54-d072-443b-8e2b-20fe1ab2fb61:CQoAsE12R+EfAgAA:PFpXXlBAG2/d0qOZT8jrjUbcuuHkSjeshWaUsl1G9A8q6A2iE9enNKeZUP3OnKg7Vr2pW2QZx9ys4k6kOpuUcmqrTwIZciVbzxfy5Fzawb76uRJPCCftXXeIXUSzMoEQuvxTWHs9hKMCOmBUPPsAN8vnyZ0ardw5I8FXDgxa+akdDQcbzbEcVtogMDQlUQB0GM1Wt/Cep2NSu8SmgsFEq5tzGAOY6XU=; AWSALB=A13ES1XYtIMerPaqlqd5nuqEr5LlS6CE6i36E7JMGeo7IzN+QT4DteHnF4stnbx6IjjklYy5eHK3mYWFmFgqYB+iWHDEwbUj8uEBMx00lmkylWhkqG9zH36KRgk4; AWSALBCORS=A13ES1XYtIMerPaqlqd5nuqEr5LlS6CE6i36E7JMGeo7IzN+QT4DteHnF4stnbx6IjjklYy5eHK3mYWFmFgqYB+iWHDEwbUj8uEBMx00lmkylWhkqG9zH36KRgk4',
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
    'viewport-width': '1323',
}

BASE_URL = "https://www.singulart.com/"


objects_url = []
for i in range(4,5):
    #soup_html = WebScrapper(urljoin(BASE_URL,f"es/nuestras-obras-de-arte?minPrice=7500&page={i}"), headers=headers, cookies=cookies).get_soup()
    soup_html = WebScrapperSelenium(urljoin(BASE_URL,f"es/nuestras-obras-de-arte?minPrice=7500&page={i}"), element_name = "search-page-results", locator = "id", base_path=BASE_URL, cookies=cookies).get_soup()
    for object in soup_html.find_all('div', class_="artworks-grid__item"):
        objects_url.append(object.find('a', class_="artwork-item__link").get('href'))

final_data = []

for object_url in objects_url:
    try:
        object_soup = WebScrapperSelenium(urljoin(BASE_URL,object_url), element_name = "artwork-layout", locator = "class", base_path=BASE_URL, cookies=cookies).get_soup()
        #object_soup = WebScrapper(urljoin(BASE_URL,object_url), headers=headers, cookies=cookies, retry=5).get_soup()

        title = WebScrapper.normalizeGetText(object_soup.find("h1",class_="artwork-info__title").getText())
        artist = WebScrapper.normalizeGetText(object_soup.find("h2",class_="artwork-info__name").getText())
        specifications = WebScrapper.normalizeGetText(object_soup.find("h3",class_="artwork-info__specifications").getText())
        #year, country, technique = specifications.split(' • ')

        dimensions = WebScrapper.normalizeGetText(object_soup.find("div",class_="artwork-info__specifications").getText())

        price = WebScrapper.normalizeGetText(object_soup.find("span",class_="artwork-price__value").getText())

        image_div = object_soup.find_all("picture", class_="artwork-gallery__picture")
        images_url = [WebScrapper.normalizeGetText(ima.find('img', class_="artwork-gallery__image").get('src','')) for ima in image_div]

        row = {}
        row["Header"] = title
        row["Price"] =  price.replace(".","").replace("€","").strip()
        row["Artist"] =  artist
        #row["Technique"] =  technique.strip()
        #row["Country"] =  country.strip()
        row["Dimensions"] = dimensions
        row["Specifications"] = specifications
        #row["Year"] =  year.strip()
        row["Imgs"] =  images_url
        final_data.append(row)
    except Exception as e:
        break


GenerateCSV("Art_data_to_upload", final_data).generate()


