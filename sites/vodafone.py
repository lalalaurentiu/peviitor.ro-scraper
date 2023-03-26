from time import sleep
import json
from scraper_peviitor import ScraperSelenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Inițializăm un obiect ScraperSelenium cu URL-ul dorit și obiectul Chrome
scraper = ScraperSelenium("https://jobs.vodafone.com/careers?query=Romania&pid=563018675157116&domain=vodafone.com&sort_by=relevance", Chrome())
# Accesăm URL-ul
scraper.get()

# Așteptăm să apară butonul de cookie-uri și apoi îl accesăm
scraper.wait(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
cookieBtn = scraper.find_element(By.ID, "onetrust-accept-btn-handler")
scraper.click(cookieBtn)

# Extragem numărul total de rezultate de pe pagină
results = scraper.find_element(By.XPATH, '//*[@id="pcs-body-container"]/div[2]/div[1]/div/span/span/strong').text
results = results.replace(" open jobs.", "")
step = 10

# Generăm o listă cu numerele de click-uri necesare pentru a accesa toate job-urile
butonCountClick = [i for i in range(step, int(results), step)]

print(len(butonCountClick))

# Parcurgem butoanele și le accesăm succesiv, apoi așteptăm ca paginile să se încarce complet
for click in range(len(butonCountClick)):
    scraper.wait(EC.presence_of_element_located((By.CLASS_NAME, 'show-more-positions')))
    button = scraper.find_element(By.CLASS_NAME, 'show-more-positions')
    scraper.driver.execute_script("arguments[0].scrollIntoView();", button)
    scraper.click(button)
    sleep(3)

# Extragem toate job-urile de pe pagină și le parcurgem succesiv, accesând fiecare în parte și extrăgând titlul și locația
jobs = scraper.find_elements(By.CLASS_NAME, "position-card")
idx = 0

print(len(jobs))

finalJobs = dict()
for job in jobs:
    try:
        scraper.driver.execute_script("arguments[0].scrollIntoView();", job)
        scraper.click(job)
        title = scraper.find_elements(By.CLASS_NAME, "position-title")[idx].text
        location = "Romania"
        print(title)
        finalJobs[idx] = {"title": title, "location": location, "link": scraper.driver.current_url}
    except Exception as e:
        print(e)
        break
    idx += 1
    sleep(1)

# Salvăm job-urile într-un fișier JSON
with open("vodafone.json", "w") as f:
    json.dump(finalJobs, f)
