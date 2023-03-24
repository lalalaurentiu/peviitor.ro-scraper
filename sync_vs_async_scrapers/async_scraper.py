#
#
#
#
# ASYNC SCRAPER ...
#
#
#
#
# 
#
#
import aiohttp
import asyncio
#
import csv
import pandas as pd
#
from bs4 import BeautifulSoup
#
import time
#
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
async def get_page(session, url: str):
    """
    This is my first async function. This function make a session.get...
    """

    lst_async_data = []
    async with session.get(url) as response:
        text = await response.text()
        
        soup = BeautifulSoup(text, 'lxml')
        title = soup.title

        if title:
            print(f"TITLE - {title.text} --- URL {url}")

            lst_async_data.append(url)
            lst_async_data.append(title.text)

        else: 
            print('Title not found...')
    return lst_async_data
#
#
async def get_all(session, links: list):
    """ 
    This async function make a list with tasks for scraping.
    """ 

    tasks = []
    for url in links: 
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    return results
#
#
async def main(links: list):
    """ 
    The main function with all logic in it.
    """

    async with aiohttp.ClientSession() as session:
        data = await get_all(session, links)
        return data


# 
if __name__ == "__main__":

    # start count time
    tic = time.perf_counter()

    links = return_links_from_db()

    results = asyncio.run(main(links))

    # end count time
    toc = time.perf_counter()
    print(f"Sync Scrape-Script for {len(links)} links is done in {toc - tic:0.4f} seconds")