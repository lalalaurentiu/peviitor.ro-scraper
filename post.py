import requests
import json

clean = "https://API.peviitor.ro/v4/clean/"
cleanContentType = "application/x-www-form-urlencoded"

update = "https://api.peviitor.ro/v4/update/"
updateContentType = "application/json"

apikey = "182b157-bb68-e3c5-5146-5f27dcd7a4c8"

# r = requests.post(update, headers={"apikey": apikey, "Content-Type": cleanContenttype}, data={"company": "allianz"})
# print(r.status_code)

with open('sites/json/allianz.json', 'r') as outfile:
    data = json.load(outfile)
    r = requests.post(update, headers={"apikey": apikey, "Content-Type": updateContentType}, data=json.dumps(data))

    print(len(data))