from scraper_peviitor import Scraper, Rules, ScraperSelenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import json

#folosim selenium deoarece joburile sunt incarcate prin ajax
scraper = ScraperSelenium("https://alliancewd.wd3.myworkdayjobs.com/ro-RO/renault-group-careers?locationCountry=f2e609fe92974a55a05fc1cdc2852122&workerSubType=62e55b3e447c01871e63baa4ca0f9391&workerSubType=62e55b3e447c01140817bba4ca0f9891", Chrome())
scraper.get()

#asteptam sa se incarce Siteul
time.sleep(10)

#se creaza o instanta a clasei Scraper
page = Scraper()
rules = Rules(page)

finaljobs = dict()
idx = 0

#se extrag joburile
while True:
    try:
        #se extrage dom-ul
        dom = scraper.getDom()
        #se seteaza dom-ul pentru scraperul de pe pagina
        page.soup = dom
        #se cauta joburile care au clasa css-19uc56f
        elements = rules.getTags("a", {"class":"css-19uc56f"})

        #pentru fiecare job, se extrage titlul, locatia si link-ul
        for element in elements:
            print(element.text)
            title = element.text
            location = "Romania"
            link = "https://alliancewd.wd3.myworkdayjobs.com" + element["href"]
            finaljobs[idx] = {"title": title, "location": location, "link": link}
            idx += 1

        #se cauta butonul de next
        nextBtn = scraper.find_element(By.XPATH, "//button[@aria-label='next']")
        #se da click pe butonul de next
        scraper.driver.execute_script("arguments[0].scrollIntoView();", nextBtn)
        scraper.click(nextBtn)
        time.sleep(5)
        print("Next")
    except:
        print("No more pages")
        break

#se salveaza joburile in fisierul renault.json
with open("renault.json", "w") as f:
    json.dump(finaljobs, f, indent=4)

