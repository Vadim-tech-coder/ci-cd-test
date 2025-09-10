from pathlib import Path
import aiohttp
import aiofiles
import asyncio

from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup
from typing import Set

OUT_PATH = Path(__file__).parent / 'result'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
DEPTH = 3
START_URLS = {'http://distep.ru', }

async def write_to_file(link: str):
    file_path = "{}/links.txt".format(OUT_PATH)
    async with aiofiles.open(file_path, mode='a') as f:
        await f.write(link + "\n")


async def process_url(client: aiohttp.ClientSession, url: str, depth: int, visited: Set[str]):
    if depth <= 0 or url in visited:
        return None

    visited.add(url)

    try:
        async with client.get(url) as response:
            if response.status != 200:
                return {
                    'url': url,
                    'depth': depth,
                    'status': f'HTTP {response.status}'
                }
            result = await response.read()
            soup = BeautifulSoup(result, 'html.parser')

            base_netloc = urlsplit(url).netloc.replace('www.', '')
            links = soup.find_all('a')
            external_links = set()

            for link in links:
                href = link.get('href')
                if href:
                    href = urljoin(url, href)
                    if href.startswith(('http://', 'https://')):
                        href_netloc = urlsplit(href).netloc.replace('www.', '')
                        if href_netloc != base_netloc:
                            external_links.add(href)
                            await write_to_file(href)

            sub_results = []
            if depth > 1:
                tasks = [process_url(client, link, depth - 1, visited) for link in external_links if link not in visited]
                if tasks:
                    sub_results = await asyncio.gather(*tasks, return_exceptions=True)

            return {
                'url': url,
                'depth': depth,
                'external_links_count': len(external_links),
                'sub_results': sub_results,
                'status': 'completed'
            }
    except Exception as e:
        return {
            'url': url,
            'depth': depth,
            'status': f'error: {str(e)}'
        }


async def crawler():
    connector = aiohttp.TCPConnector(limit=10, ssl=False, force_close = True)
    visited = set()
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(100),
        connector=connector
    ) as client:
        tasks = [process_url(client, url, DEPTH, visited) for url in START_URLS]
        results = await asyncio.gather(*tasks)
        return results



def main():
    results = asyncio.run(crawler())
    print(results)


if __name__ == '__main__':
    main()