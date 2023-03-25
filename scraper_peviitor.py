from bs4 import BeautifulSoup
import requests
from lxml import etree

class Scraper:
    def __init__(self, url: str):
        self.session = self.getSession()
        self._url = url
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        self.soup = None  
        self.getSoup()  
        
    def getSession(self):
        session = requests.Session()
        return session
    
    def getSoup(self):
        try:
            document = self.session.get(self.url,headers=self.user_agent ,timeout=10)
            self.soup = BeautifulSoup(document.text, "html.parser")
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

   
class Rules:
    def __init__(self, scraper : Scraper):
        self.scraper = scraper
    
    def getTags(self,tag : str , attrs : dict = None):
        self.anchors = self.scraper.soup.find_all(tag, attrs=attrs)
        return set(self.anchors)
    
    def getTag(self,tag : str , attrs : dict = None):
        self.anchors = self.scraper.soup.find(tag, attrs=attrs)
        return self.anchors
    
    def getXpath(self, xpath : str):
        dom = etree.HTML(str(self.scraper.soup))
        self.xpath = dom.xpath(xpath)
        return self.xpath
    