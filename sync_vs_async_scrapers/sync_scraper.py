#
#
#
#
#
# SYNC SCRAPER ---> 
#
#
#
#
#
# import needed libraries
from requests_html import HTMLSession
#
import pandas as pd 
import csv
#
import time # for count speed of this script
#
#
def return_links_from_db() -> list:
    """
    This function return all links from .txt file. This links will be use for scraping.
    """

    links_from_tdt_file = []
    with open('jobs_for_Sync_Async.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()

        for link in data:
            links_from_tdt_file.append(link.strip())

    # return list with links
    return links_from_tdt_file
#
#
def make_requests(links: list) -> None:
    """ 
    This function make requests with library "requests-html".
    """

    lst_with_data = []
    for link in links:
        
        # HTML session with requests-html
        session = HTMLSession()

        resp = session.get(link)
        resp.html.render(sleep=4, keep_page=True)

        local_lst = []

        h1_element = resp.html.find('h1', first=True).text
        if h1_element:
            local_lst.append(link)
            local_lst.append(h1_element)
        else:
            print('No h1 element found...')

        # add to big list
        lst_with_data.append(local_lst)

        print(local_lst)
        time.sleep(0.5)
        #local_lst.clear()

        print(f'Link ---> {link} <--- gata')
    print(lst_with_data)
    # save to csv file
    headers = ['link', 'h1_element']
    df = pd.DataFrame(lst_with_data, columns=headers)
    df.to_csv("jobs_sync_scraped.csv", encoding="utf8")

    return 'Done'
#
#
def main():
    """ 
    Try do discover logic of this small code. 
    ... and try to count execute time.
    """

    tic = time.perf_counter()

    links_to_scrape = return_links_from_db()[:10]
    print(make_requests(links_to_scrape))

    toc = time.perf_counter()
    print(f"Sync Scrape-Script for 10 links is done in {toc - tic:0.4f} seconds")
#
#
if __name__ == "__main__":
    main()
