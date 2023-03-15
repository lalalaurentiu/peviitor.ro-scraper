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
    try:
        req = requests.get(path + "robots.txt", timeout=5)
        data = req.text
    except Exception as e:
        print(e)
        return ""
    
    return data

#cauta dupa sitemap.xml
def getSiteMapxml(url):
    try: 
        document = requests.get(url)
        soup = BeautifulSoup(document.text, 'lxml')
        links = soup.find_all('loc')
    except Exception as e:
        print(e)
        return []
    return links

#cauta dupa sitemap
def getSiteMapLinks(document):
    links = re.findall(r'[Ss]itemap: (.*)' , document)
    return links


# with open("gsites.json", "r") as f:
#     sites = json.load(f)

# #
# for i in sites.keys():
#     print(i)
#     robots = getRobots("https://" + i)
#     sitemap = getSiteMapLinks(robots)
#     with open(f"robots.txt", "a") as f:
#         for i in sitemap:
#             f.write(i + "\n")
#             print(i)
#     sleep(5)
    
sites = {}
# with open("robots.txt", "r") as f:
#     robots = f.readlines()
#     jobsKewords = ["jobs", "careers", "job", "career"]
#     for i in robots:
#         roDocument = re.findall(r'/[Rr]o[-_][E]n(.*)/' , i)
#         print(roDocument)
#         # lines = getSiteMapxml(i.strip("\n"))
        # for line in lines:
        #     domain = line.text.split("https://")[1].split("/")[0]
        #     print(sites)
        #     if domain not in sites:
        #         sites[domain] = [line.text]
        #     else:
        #         sites[domain].append(line.text)
        # sleep(5)

sitemapUrl = "https://www.deloitte.com/sitemap_index.xml"

lines = getSiteMapxml(sitemapUrl)
for line in lines:
    roDocument = re.findall(r'(.*)[Rr]o.*[Ee]n(.*)|(.*)[Rr]o(.*)' , line.text)
    if roDocument:
        print(line)
# with open(f"sites.json", "w") as f:
#     json.dump(sites, f)