import os
import json
from scraper_peviitor import loadingData

path = os.path.dirname(os.path.abspath(__file__))
apikey = os.environ.get('apikey')

for site in os.listdir(path):
    company = site.split('.')[0]
    # with open(os.path.join(path, site), 'r') as f:
    #     print(json.load(f))
    print(company)