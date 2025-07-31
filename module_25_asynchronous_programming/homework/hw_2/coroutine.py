import asyncio
import json
import time
from pathlib import Path
import aiohttp
import aiofiles

URL = 'https://api.thecatapi.com/v1/images/search'
CATS_WE_WANT = 150
OUT_PATH = Path(__file__).parent / 'cats_coro'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

semaphore = asyncio.Semaphore(3)  # ограничиваем число одновременных запросов

async def get_cat(client: aiohttp.ClientSession, idx: int, retries=3):
    async with semaphore:
        for attempt in range(1, retries + 1):
            try:
                headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}
                async with client.get(URL, headers=headers) as response:
                    if response.status != 200:
                        print(f"Failed to fetch metadata for image #{idx}, status: {response.status}")
                        continue
                    result = await response.read()
                    data = json.loads(result.decode())
                    if not data or 'url' not in data[0]:
                        print(f"Empty or invalid data for image #{idx}: {data}")
                        continue
                    image_url = data[0]['url']

                async with client.get(image_url, headers=headers) as img_resp:
                    if img_resp.status != 200:
                        print(f"Failed to download image #{idx}, status {img_resp.status}")
                        continue
                    image_content = await img_resp.read()

                await write_to_disk(image_content, idx)
                print(f"Image #{idx} downloaded and saved")
                return  # успешно, выходим из цикла

            except Exception as e:
                print(f"Error processing image #{idx} on attempt {attempt}: {repr(e)}")
                if attempt < retries:
                    await asyncio.sleep(1)  # пауза перед повтором
                else:
                    print(f"Giving up on image #{idx} after {retries} attempts")
                    return


async def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)

async def get_all_cats():
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        results = await asyncio.gather(*tasks)
        return results

def main():
    start = time.time()
    res = asyncio.run(get_all_cats())
    end = time.time()
    duration = end - start
    print("Total images processed:", len([r for r in res if r is None or r is not None]), 'in {:.4} seconds'.format(duration))

if __name__ == '__main__':
    main()
