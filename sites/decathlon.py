from scraper_peviitor import Scraper, Rules, ScraperSelenium
from selenium import webdriver
import json

#Folosesc selenium deoarece joburile sunt incarcate prin ajax
scraper = ScraperSelenium('https://cariere-decathlon.ro', webdriver.Chrome())
scraper.get()

#Iau dom-ul randat de browser
dom = scraper.getDom()


scraper = Scraper()
#incarc dom-ul in scraper
scraper.soup = dom

#Folosesc clasa Rules pentru a extrage joburile
rules = Rules(scraper)

#Iau toate h3-urile cu clasa whr-title
elements = rules.getTags('h3', {'class': 'whr-title'})

finalJobs = dict()
idx = 0

#Pentru fiecare h3 extrag titlul si linkul
for elemen in elements:
    link = elemen.find('a')
    title = link.text
    location = "Romania"
    finalJobs[idx] = {
        'title': title,
        'location': location,
        'link': link['href']
    }

    idx += 1

with open('decathlon.json', 'w') as file:
    json.dump(finalJobs, file, indent=4)