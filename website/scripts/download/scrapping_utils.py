import requests
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException as selTimeout
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
            print(f'Requesting url: {self.url}')
            try:
                response: requests.Response = requests.get(self.url, headers=self.headers, cookies=self.cookies)
                response.raise_for_status()
                self.response = response
                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
                self.soup = soup
                break
            except requests.exceptions.RequestException as e:
                print(f"Error al realizar la solicitud: {e}")
                t -= 1
                if t <= 0: break
                time.sleep(5)
                
    def get_soup(self) -> BeautifulSoup:
        return self.soup
    
    def get_response(self) -> requests.Response:
        return self.response

    @staticmethod
    def normalizeGetText(text):
        return ' '.join(text.strip().split())

class WebScrapperSelenium():

    LOCATOR_MAP = {
        "id": By.ID,
        "class": By.CLASS_NAME
    }
    
    def __init__(self, url: str, element_name = "", locator = "", timeout = 10, headless = False):
        self.url: str = url
        self.soup = None 
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        else:
            options.add_argument('window-size=1200x600')  
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.timeout = timeout
        self.element_name = element_name
        self.locator = locator
        self.read_url()

    def read_url(self):
        while True:
            print(f'Requesting url: {self.url}')
            try:
                self.driver.get(self.url)
                locator_value = WebScrapperSelenium.LOCATOR_MAP.get(self.locator,None)

                if locator_value:
                    try:
                        WebDriverWait(self.driver, self.timeout).until(
                            EC.presence_of_element_located((locator_value, self.element_name))
                        )
                    except selTimeout as e:
                        print("Timeout esperando el contenido")
                        self.driver.quit()
                        break
                else:
                    time.sleep(5)

                html = self.driver.page_source
                soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
                self.soup = soup
                self.driver.quit()
                break
            except requests.exceptions.RequestException as e:
                print(f"Error al realizar la solicitud: {e}")
                self.driver.quit()
                break

    def get_soup(self) -> BeautifulSoup:
        return self.soup
    
class GenerateCSV():

    def __init__(self, filename: str, data: list[dict]):
        self.filename = filename
        self.data = data

    def generate(self):
        df =  pd.DataFrame(self.data)
        df.to_csv(f'{self.filename}.csv', index=False)

