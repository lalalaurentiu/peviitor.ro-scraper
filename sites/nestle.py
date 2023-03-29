from scraper_peviitor import Scraper, Rules
import time
import json

#Se creeaza o instanta a clasei Scraper
scraper = Scraper("https://www.nestle.ro/jobs/search-jobs?keyword=Romania&country=&location=&career_area=All")
rules = Rules(scraper)

finalJobs = dict()
idx = 0

#Se extrag joburile
while True:
    #Se cauta joburile care au clasa jobs-title
    elements = rules.getTags("div", {"class":"jobs-title"})

    #Pentru fiecare job, se extrage titlul, locatia si link-ul
    for element in elements:
        title = element.find("a").text.replace("\t", "").replace("\r", "").replace("\n", "").replace("  ", "")
        location = "Romania"
        link = element.find("a")["href"]
        print(title)
        finalJobs[idx] = {"title": title, "location": location, "link": link}
        idx += 1

    #Se cauta butonul de next
    domain = "https://www.nestle.ro/jobs/search-jobs"
    try:
        #Daca exista butonul de next, se extrage link-ul si se pune in url-ul scraper-ului
        nextPage = rules.getTag("div", {"class":"pager__item--next"})
        nextPageLink = nextPage.find("a")["href"]
        scraper.url = domain + nextPageLink
    except:
        break

    time.sleep(3)

#Se salveaza joburile in fisierul nestle.json
with open("nestle.json", "w") as f:
    json.dump(finalJobs, f, indent=4)


