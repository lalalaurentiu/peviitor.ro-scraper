from ..scraper_peviitor import Scraper, Rules
import time

scraper = Scraper('https://jobs.kaufland.com/Romania/search/?q=&locationsearch=&locale=ro_RO')
rules = Rules(scraper)

pages = rules.getAnchors({'rel': 'nofollow'})
pagesLink = "https://jobs.kaufland.com/Romania/search/"

j = []
jobsLink = "https://jobs.kaufland.com/Romania/job/"

for page in pages:
    pageLink = pagesLink + page['href']
    print(pageLink)
    scraper.url = pageLink
    rules = Rules(scraper)
    jobs = rules.getAnchors({'class': 'jobTitle-link'})
    j.extend(jobs)


    time.sleep(1)

for job in j:
    print(job)