from bs4 import BeautifulSoup
import lxml
import requests
import re
from time import sleep
import json

#cauta dupa robots.txt
def getRobots(url):
    if url.endswith('/'):
        path = url
    else:
        path = url + '/'
    req = requests.get(path + "robots.txt", data=None)
    data = req.text
    
    return data

#cauta dupa sitemap.xml
def getSiteMapxml(url):
    document = requests.get(url)
    soup = BeautifulSoup(document.text, 'lxml')
    links = soup.find_all('loc')
    return links

#cauta dupa sitemap
def getSiteMapLinks(document):
    document = document.replace("\n", "")
    links = document.split("Sitemap: ")[1:]
    return links


with open("gsites.json", "r") as f:
    sites = json.load(f)

#
for i in sites.keys():
    print(i)
    robots = getRobots("https://" + i)
    sitemap = getSiteMapLinks(robots)
    with open(f"robots.txt", "a") as f:
        for i in sitemap:
            f.write(i + "\n")
    sleep(5)
    
    



# sites = {}
# with open("robots.txt", "r") as f:
#     robots = f.read()



#     for i in getSiteMapLinks(robots):
#         lines = getSiteMapxml(i)
#         for line in lines:
#             domain = line.text.split("https://")[1].split("/")[0]
#             print(sites)
#             if domain not in sites:
#                 sites[domain] = [line.text]
#             else:
#                 sites[domain].append(line.text)
#         sleep(5)
        
# with open(f"sites.json", "w") as f:
#     json.dump(sites, f)