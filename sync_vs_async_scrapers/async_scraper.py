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
import aiohttp
import asyncio
#
import csv
import pandas as pd
#
import re
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
        exp = r'(<title>).*(<title>)'
        match = re.search(exp,text)
        title = match.group(0) if match else 'No title found'

        print(title)

        lst_async_data.append(url)
        lst_async_data.append(title)
    
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

    # count time

    links = return_links_from_db()

    results = asyncio.run(main(links))

    # time to check time

    print(len(results))