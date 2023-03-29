from scraper_peviitor import ScraperSelenium, Scraper, Rules
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

#Folosim selenium deoarece anchorele cu nu au atributul href
scraper = ScraperSelenium("https://medicover.mingle.ro/en/apply", webdriver.Chrome())
scraper.get()

#Caut toate anchorele cu clasa btn-apply
anchors = scraper.find_elements(By.CLASS_NAME, "btn-apply")

#Instantiez un nou scraper pentru a extrage datele de pe pagina jobului
anchorPageScraper = Scraper()
rules = Rules(anchorPageScraper)

finalJobs = dict()
idx = 0

while idx < len(anchors):
    #Scroll pana la ancorela curenta si apoi fac click pe ea
    anchor = anchors[idx]
    scraper.driver.execute_script("arguments[0].scrollIntoView();", anchor)
    time.sleep(1)
    scraper.click(anchor)

    time.sleep(1)
    #Incarc dom-ul paginii jobului in scraper
    anchorPageScraper.soup = scraper.getDom()

    #Extrag titlul ,locatia si linkul
    title = rules.getTag("title").text
    location = "Romania"
    link = scraper.driver.current_url
    print(title)

    #Adaug jobul in dictionar
    finalJobs[idx] = {"title": title, "location": location, "link": link}

    #Inapoi la pagina principala
    scraper.driver.back()
    time.sleep(1)

    #Caut toate ancorele din nou
    anchors = scraper.find_elements(By.CLASS_NAME, "btn-apply")
    idx += 1
    
#Salvez joburile in fisierul medicover.json
with open("medicover.json", "w") as f:
    json.dump(finalJobs, f, indent=4)



