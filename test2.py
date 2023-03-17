import re
import json
import requests
from bs4 import BeautifulSoup
import time

pat1 = re.compile(r"/&foo(\=[^&]*)?(?=&|$)|^foo(\=[^&]*)?(&|$)/^ ", re.IGNORECASE | re.DOTALL)

pat2 = re.compile(r"#(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)

jobs = dict()
with open("jobs.txt", "r") as f:
    urls = f.read().splitlines()
    
    for i in urls:
        try:
            domain = i.split("https://")[1].split("/")[0]
            url = i.split("....")[0]
            print(url)
            description = i.split("....")[1]
            if domain not in jobs:

                jobs[domain] = [{
                    "url": url,
                    "description": description
                }]

            else:
                jobs[domain].append({
                    "url": url,
                    "description": description
                })
            print(i.split("https://")[1].split("/")[0])
            # print(pat1.sub(" ", i.split("https://")[1].split("/")[-1].replace("?", "").replace("=", " ").replace("-", " ")))
        except :
            pass

with open("jobs.json", "w") as f:
    json.dump(jobs, f)

# import json
# with open("jobs.json", "r") as f:
#     jobs = json.load(f)
#     for k, v in jobs.items():
#         print(k, v)

