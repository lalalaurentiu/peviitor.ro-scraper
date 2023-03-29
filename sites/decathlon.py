from scraper_peviitor import Scraper, Rules, ScraperSelenium
from selenium import webdriver
import json
import uuid
import time

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

finalJobs = list()
idx = 0

#Pentru fiecare h3 extrag titlul si linkul
for elemen in elements:
    link = elemen.find('a')
    title = link.text

    #Deschid link-ul jobului in browser
    linkScrap = ScraperSelenium(link['href'], webdriver.Chrome())
    linkScrap.get()
    time.sleep(3)

    #Iau dom-ul jobului si il pun in scraper
    scraper.soup = linkScrap.getDom()

    #inchid browser-ul
    linkScrap.close()

    #Iau locatia jobului
    city = rules.getTag('span', {'data-ui': 'job-location'})

    location = city.text.split(',')[0]
    print(location)

    country = "Romania"
    finalJobs.append({
        'id': str(uuid.uuid4()),
        'job_title': title,
        'job_link': link['href'],
        'company': 'Decathlon',
        'country': country,
        'city': location,
    })

    time.sleep(3)

with open('decathlon.json', 'w') as file:
    json.dump(finalJobs, file, indent=4)