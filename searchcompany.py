from googlesearch import search
keyword = "cariera"
lst = search(keyword, lang="ro", num_results=100 )
import json

sites = dict()

for i in lst:
    url = i.split("https://")[1].split("/")[0].split(".")
    domain = i.split("https://")[1].split(".")[1]
    subdomain = url[0]
    if len(url) >= 3:
        if domain not in sites:
            sites[domain] = dict(
                url = i,
                domain = url[-1],
                subdomain = url[0],
            )
        else:
            pass
    
with open(f"{keyword}.json", "w") as f:
    json.dump(sites, f)