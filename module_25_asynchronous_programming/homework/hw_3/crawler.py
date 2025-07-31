from pathlib import Path

import aiohttp
import aiofiles
import asyncio

from urllib.parse import urlsplit
from bs4 import BeautifulSoup

OUT_PATH = Path(__file__).parent / 'result'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
DEPTH = 3
URL  = {'http://distep.ru', }

async def crawler():
    connector = aiohttp.TCPConnector(limit=10, ssl=False, force_close = True)
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(100),
        connector=connector
    ) as client:
        tasks = [get_url(client, url, DEPTH) for url in URL]
        return await asyncio.gather(*tasks)


async def get_url(client: aiohttp.ClientSession, url, depth):
    async with client.get(url) as response:
        result = await response.read()
        soup = BeautifulSoup(result, 'html.parser')

        base = urlsplit(url).netloc.replace("www.", "")
        links = soup.find_all('a')
        if links:
            for link in links:
                format_link = link.get('href')
                if format_link:
                    if format_link.startswith('http') and base not in format_link:
                        print(format_link)
                        URL.add(format_link)
                        await write_to_file(format_link)

    depth -= 1
    if depth > 0:
        tasks = [get_url(client, url, depth) for url in URL]
        return await asyncio.gather(*tasks)
    else:
        return await asyncio.sleep(3)

async def write_to_file(link: str):
    file_path = "{}/links.txt".format(OUT_PATH)
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(link + "\n")

def main():
    asyncio.run(crawler())

if __name__ == '__main__':
    main()