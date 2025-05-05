import requests
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException as selTimeout
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
                #if "JavaScript is disabled" in self.soup.find_all("h1"): raise requests.exceptions.RequestException("Javascript error")
                t = self.retry
                break
            except requests.exceptions.RequestException as e:
                print(f"Error al realizar la solicitud: {e}")
                t -= 1
                if t <= 0: break
                time.sleep(10)
                
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
    
    def __init__(self, url: str, element_name = "", locator = "", timeout = 10, headless = False, base_path = None, cookies = []):
        self.url: str = url
        self.soup = None 
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        else:
            options.add_argument('window-size=1200x600')  
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)

        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })

        self.timeout = timeout
        self.element_name = element_name
        self.locator = locator
        self.base_path = base_path
        self.cookies = cookies
        self.read_url()

    def read_url(self):
        while True:
            print(f'Requesting url: {self.url}')
            try:
                if self.base_path and self.cookies:
                    self.driver.get(self.base_path)
                    for cookie in self.cookies:
                        self.driver.add_cookie(cookie)

                self.driver.get(self.url)
                locator_value = WebScrapperSelenium.LOCATOR_MAP.get(self.locator,None)

                if locator_value:
                    try:
                        WebDriverWait(self.driver, self.timeout).until(
                            EC.presence_of_element_located((locator_value, self.element_name))
                        )
                    except selTimeout as e:
                        print("Timeout esperando el contenido")
                        #self.driver.quit()
                        time.sleep(10)
                        continue
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

