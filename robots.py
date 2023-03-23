from bs4 import BeautifulSoup
import lxml
import requests
import re
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
        document = requests.get(url, timeout=10)
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


with open("gsites.json", "r") as f:
    sites = json.load(f)

#

sitemapsLst = []
for i in sites.keys():
    print(i)
    robots = getRobots("https://" + i)
    sitemap = getSiteMapLinks(robots)
    for i in sitemap:
        sitemapsLst.append(i)
        print(i)

disponibleJobs = []

for i in sitemapsLst:
    lines = getSiteMapxml(i)
    for line in lines:
        roDocument = re.findall(r'/(.*)[Jj]ob(.*)' , line.text)

        if roDocument and ".xml" not in line.text:
            jobDetail = line.text
            print(jobDetail)
            with open(f"sites.txt", "a") as f:
                f.writelines(jobDetail + "\n")
        elif roDocument and ".xml" in line.text:
            xml = getSiteMapxml(line.text)
            for job in xml:
                roDocument = re.findall(r'/(.*)[Jj]ob(.*)' , job.text)
                if roDocument:
                    jobDetail = job.text
                    print(jobDetail)
                    with open(f"sites.txt", "a") as f:
                        f.writelines(jobDetail + "\n")



