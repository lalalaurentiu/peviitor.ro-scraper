from googlesearch import search
keyword = "careers"
lst = search(keyword, lang="ro", num_results=10 )
import json

sites = dict()

for i in lst:
    print(i)
    
    try:
        url = i.split("https://")[1].split("/")[0].split(".")
        domain = i.split("https://")[1].split("/")[0]
    except:
        url = i.split("http://")[1].split("/")[0].split(".")
        domain = i.split("http://")[1].split("/")[0]
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
    
with open(f"gsites.json", "w") as f:
    json.dump(sites, f)