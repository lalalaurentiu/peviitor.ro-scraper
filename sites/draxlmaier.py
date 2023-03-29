from scraper_peviitor import Scraper, Rules, ScraperSelenium
import time
import json

#Cream o instanta a clasei Scraper
scraper = Scraper("https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/125/?q=&sortColumn=referencedate&sortDirection=desc")
rules = Rules(scraper)

#Cautam numarul de joburi
jobsnumbers = int(rules.getXpath('//*[@id="job-table"]/div[1]/div/div/div/span[1]/b[2]').text)

#Cream o lista cu numerele de joburi de 25 in 25
jobsPerPage = [i for i in range(0 , jobsnumbers, 25) ]

#Cream un dictionar in care vom salva joburile
finaljobs = dict()
idx = 0

#Pentru fiecare numar din lista, extragem joburile
for jobs in jobsPerPage:
    #Daca numarul de joburi este intre 0 si 25, atunci luam decat pagina 1
    if jobs == 0:
        pageLink = 'https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/?q=&sortColumn=referencedate&sortDirection=desc'
    #Daca numarul de joburi este mai mare decat 25, atunci luam pagina corespunzatoare
    else:
        pageLink = f"https://d-career.org/Draexlmaier/go/DRÄXLMAIER-Job-Opportunities-in-Romania-%28Romanian%29/4196801/{jobs}/?q=&sortColumn=referencedate&sortDirection=desc"

    #Punem link-ul in url-ul scraper-ului
    scraper.url = pageLink

    #Cautam joburile care au clasa jobTitle-link
    elements = rules.getTags("a", {"class":"jobTitle-link"})

    #Pentru fiecare job, extragem titlul, locatia si link-ul
    for element in elements:
        title = element.text
        location = "Romania"
        link = "https://d-career.org" + element["href"]
        finaljobs[idx] = {"title": title, "location": location, "link": link}
        print(element.text)
        idx += 1
    time.sleep(3)

#Salvam joburile in fisierul draxlmaier.json
with open("draxlmaier.json", "w") as f:
    json.dump(finaljobs, f, indent=4)