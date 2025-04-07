import requests
import time

from typing import Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd


class WebScrapper():

    def __init__(self, url: str, headers: dict = None, cookies: dict = None, retry: int = 1):
        self.url: str = url
        self.headers: str = headers
        self.cookies: str = cookies
        self.soup = None 
        self.response = None
        self.retry = retry 
        self.read_url()

    def read_url(self):
        t = self.retry
        while True:
            if t <= 0: break
            print(f'Requesting url: {self.url}')
            response : requests.Response = requests.get(self.url)
            try:
                #response: requests.Response = requests.get(self.url, headers=self.headers, cookies=self.cookies)
                response: requests.Response = requests.get(self.url)
                response.raise_for_status()
                self.response = response
                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
                self.soup = soup
                break
            except requests.exceptions.RequestException as e:
                print(f"Error al realizar la solicitud: {e}")
                time.sleep(5)
                t -= 1


    def get_soup(self) -> BeautifulSoup:
        return self.soup
    
    def get_response(self) -> requests.Response:
        return self.response

    @staticmethod
    def normalizeGetText(text):
        return ' '.join(text.strip().split())
    
class GenerateCSV():

    def __init__(self, filename: str, data: list[dict]):
        self.filename = filename
        self.data = data

    def generate(self):
        df =  pd.DataFrame(self.data)
        df.to_csv(f'{self.filename}.csv', index=False)

