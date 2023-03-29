from bs4 import BeautifulSoup
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Scraper:
    """
    O clasă utilizată pentru a realiza scraping web.

    Atribute
    ----------
    url : str
        URL-ul website-ului de pe care se va face scraping-ul.
    soup : obiect BeautifulSoup
        Un obiect care reprezintă codul HTML parsat al website-ului.

    Metode
    -------
    __init__(url: str)
        Inițializează un nou obiect Scraper cu URL-ul dat.
    getSoup()
        Descarcă codul HTML de la URL și creează un obiect BeautifulSoup.
    """

    def __init__(self, url: str = None):
        """
        Inițializează un nou obiect Scraper cu URL-ul dat.

        Parametri
        ----------
        url : str, opțional
            URL-ul website-ului de pe care se va face scraping-ul.
        """

        self.session = self.getSession()
        self._url = url
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        self._soup = None  
        self.getSoup()  

    def getSession(self):
        """
        Creează o sesiune nouă HTTP pentru a face request-uri.

        Returnează
        ----------
        session : obiect requests.Session
            Sesiunea HTTP.
        """

        session = requests.Session()
        return session
    
    def getSoup(self):
        """
        Descarcă codul HTML de la URL și creează un obiect BeautifulSoup.

        Returnează
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup creat.
        """

        try:
            document = self.session.get(self.url,headers=self.user_agent ,timeout=10)
            self._soup = BeautifulSoup(document.text, "html.parser")
        except Exception as e:
            print(e)  
            return [] 

    @property
    def url(self):
        """
        Proprietate ce permite obținerea URL-ului obiectului Scraper.

        Returnează
        ----------
        url : str
            URL-ul obiectului Scraper.
        """

        return self._url

    @url.setter
    def url(self, url):
        """
        Proprietate ce permite setarea URL-ului obiectului Scraper.

        Parametri
        ----------
        url : str
            URL-ul de setat.
        """

        self._url = url
        self.getSoup()

    @property
    def soup(self):
        """
        Proprietate ce permite obținerea obiectului BeautifulSoup al obiectului Scraper.

        Returnează
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup al obiectului Scraper.
        """

        return self._soup
    
    @soup.setter
    def soup(self, soup):
        """
        Proprietate ce permite setarea obiectului BeautifulSoup al obiectului Scraper.

        Parametri
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup de setat.
        """

        self._soup = BeautifulSoup(soup, "html.parser")



class ScraperSelenium:
    def __init__(self, url: str, driver: webdriver):
        """
        Constructorul clasei.
        :param url: adresa URL a paginii web pe care se va lucra
        :param driver: instanța webdriver utilizată pentru a automatiza browserul web
        """
        self._url = url
        self.driver = driver

    @property
    def url(self):
        """
        Proprietatea url pentru a accesa valoarea adresei URL.
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Setează valoarea adresei URL.
        :param url: adresa URL pe care o vom seta
        """
        self._url = url

    def get(self):
        """
        Deschide adresa URL în browser.
        """
        self.driver.get(self.url)

    def find_element(self, by: By, value: str):
        """
        Găsește primul element pe care îl găsește după criteriile de căutare specificate.
        :param by: metoda de căutare (ex. By.ID, By.CLASS_NAME, etc.)
        :param value: valoarea căutată
        :return: primul element găsit după criteriile de căutare specificate
        """
        return self.driver.find_element(by, value)
    
    def find_elements(self, by: By, value: str):
        """
        Găsește toate elementele care se potrivesc cu criteriile de căutare specificate.
        :param by: metoda de căutare (ex. By.ID, By.CLASS_NAME, etc.)
        :param value: valoarea căutată
        :return: o listă de elemente găsite după criteriile de căutare specificate
        """
        return self.driver.find_elements(by, value)
    
    def click(self, element):
        """
        Face click pe elementul specificat.
        :param element: elementul pe care se face click
        """
        self.driver.execute_script("arguments[0].click();", element)
    
    def getDom(self):
        """
        Returnează conținutul DOM al paginii web curente.
        :return: conținutul DOM al paginii web curente
        """
        return self.driver.page_source
    
    def wait(self, condition, timeout=10):
        """
        Așteaptă până când o condiție specificată devine adevărată.
        :param condition: condiția care trebuie să devină adevărată
        :param timeout: timpul maxim de așteptare în secunde (implicit 10)
        """
        return WebDriverWait(self.driver, timeout).until(condition)
    
    def close(self):
        """
        Închide browserul web.
        """
        self.driver.close()


class Rules:
    def __init__(self, scraper : Scraper):
        """
        Constructorul clasei.
        :param scraper: instanța Scraper utilizată pentru a extrage informații de pe o pagină web
        """
        self.scraper = scraper
    
    def getTags(self,tag : str , attrs : dict = None):
        """
        Returnează toate tagurile care corespund cu criteriile specificate.
        :param tag: tagul pe care se face căutarea
        :param attrs: un dicționar cu atributele tagului căutat (ex. {'class': 'foo', 'id': 'bar'})
        :return: un set de taguri găsite după criteriile de căutare specificate
        """
        self.anchors = self.scraper.soup.find_all(tag, attrs=attrs)
        return set(self.anchors)
    
    def getTag(self,tag : str , attrs : dict = None):
        """
        Returnează primul tag care corespunde cu criteriile specificate.
        :param tag: tagul pe care se face căutarea
        :param attrs: un dicționar cu atributele tagului căutat (ex. {'class': 'foo', 'id': 'bar'})
        :return: primul tag găsit după criteriile de căutare specificate
        """
        self.anchor = self.scraper.soup.find(tag, attrs=attrs)
        return self.anchor
    
    def getXpath(self, xpath : str):
        """
        Returnează elementele care corespund cu expresia XPath specificată.
        :param xpath: expresia XPath utilizată pentru căutare
        :return: o listă de elemente găsite folosind expresia XPath specificată
        """
        dom = etree.HTML(str(self.scraper.soup))
        self.xpath = dom.xpath(xpath)
        return BeautifulSoup(etree.tostring(self.xpath[0]), "html.parser")
    
    