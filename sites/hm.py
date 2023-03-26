from time import sleep
import json
from scraper_peviitor import Scraper, Rules, ScraperSelenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

scraper = ScraperSelenium("https://career.hm.com/search/?l=cou%3Aro", Chrome())
scraper.get()

cookieBtn = scraper.wait(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))

cookieBtn = scraper.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
scraper.click(cookieBtn)

scraper.wait(EC.presence_of_element_located((By.CLASS_NAME, "load-more-heading")))

totalResults = int(
    scraper.find_element(By.CLASS_NAME, "load-more-heading").get_attribute("data-total")
)

step = int(
    scraper.find_element(By.CLASS_NAME, "load-more-heading").get_attribute("data-items-shown")
)

butonCountClick = [i for i in range(step, totalResults, step)]

print(len(butonCountClick))

button = scraper.find_element(By.CLASS_NAME, "load_more_cta")

for click in range(len(butonCountClick)):
    scraper.click(button)
    sleep(3)

dom = scraper.getDom()

scraper.close()

scraper = Scraper()
scraper.soup = dom
rules = Rules(scraper)

jobs = rules.getTags("a", {"class": "jobs-card--link"})
idx = 0
finaljobs = dict()
for job in jobs:
    print(job["href"])
    scraper.url = job["href"]
    rules = Rules(scraper)
    title = rules.getTag("div", {"class": "text--title-large"}).text.replace("\n", "").replace("\t", "").replace("Stores", "")
    location = "Romania"
    finaljobs[idx] = {"title": title, "location": location, "link": job["href"]}
    idx += 1
    print(title)
    sleep(3)


with open("hm.json", "w") as f:
    json.dump(finaljobs, f)






