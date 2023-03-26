from bs4 import BeautifulSoup
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Scraper:
    def __init__(self, url: str = None):
        self.session = self.getSession()
        self._url = url
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        self._soup = None  
        self.getSoup()  

    def getSession(self):
        session = requests.Session()
        return session
    
    def getSoup(self):
        try:
            document = self.session.get(self.url,headers=self.user_agent ,timeout=10)
            self._soup = BeautifulSoup(document.text, "html.parser")
        except Exception as e:
            print(e)  
            return [] 

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        self.getSoup()

    @property
    def soup(self):
        return self._soup
    
    @soup.setter
    def soup(self, soup):
        self._soup = BeautifulSoup(soup, "html.parser")


class ScraperSelenium:
    def __init__(self, url: str, driver: webdriver):
        self._url = url
        self.driver = driver

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def get(self):
        self.driver.get(self.url)

    def find_element(self, by: By, value: str):
        return self.driver.find_element(by, value)
    
    def find_elements(self, by: By, value: str):
        return self.driver.find_elements(by, value)
    
    def click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
    
    def getDom(self):
        return self.driver.page_source
    
    def wait(self, condition, timeout=10):
        return WebDriverWait(self.driver, timeout).until(condition)
    
    def close(self):
        self.driver.close()


class Rules:
    def __init__(self, scraper : Scraper):
        self.scraper = scraper
    
    def getTags(self,tag : str , attrs : dict = None):
        self.anchors = self.scraper._soup.find_all(tag, attrs=attrs)
        return set(self.anchors)
    
    def getTag(self,tag : str , attrs : dict = None):
        self.anchor = self.scraper._soup.find(tag, attrs=attrs)
        return self.anchor
    
    def getXpath(self, xpath : str):
        dom = etree.HTML(str(self.scraper.soup))
        self.xpath = dom.xpath(xpath)
        return self.xpath
    