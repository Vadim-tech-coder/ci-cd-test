import multiprocessing
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import List
import threading
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests


URL = ['https://api.thecatapi.com/v1/images/search' for _ in range(150)]
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

def get_cat(url: str, idx: int, retries: int = 3) -> None:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}
    for attempt in range(1, retries + 1):
        try:
            time.sleep(0.2)
            with requests.get(url, headers=headers, verify=False, timeout=10) as response:
                if response.status_code != 200:
                    print(f"Failed to fetch metadata for image #{idx}, status: {response.status_code}")
                    continue
                data = response.json()
                if not data or 'url' not in data[0]:
                    print(f"Empty or invalid data for image #{idx}: {data}")
                    continue
                image_url = data[0]['url']

                with requests.get(image_url, headers=headers, verify=False, timeout=10) as img_resp:
                    if img_resp.status_code != 200:
                        print(f"Failed to download image #{idx}, status {img_resp.status_code}")
                        continue
                    image_content = img_resp.content

                    write_to_disk(image_content, idx)
                    print(f"Image #{idx} downloaded and saved", flush=True)
            return  # успешно, выходим из цикла
        except Exception as e:
            print(f"Request error for image #{idx} on attempt {attempt}: {repr(e)}", flush=True)
        if attempt < retries:
            time.sleep(1)  # пауза перед повтором
        else:
            print(f"Giving up on image #{idx} after {retries} attempts")



def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(content)

def threadpool_work() -> None:
    pool = ThreadPool(processes=5)
    start = time.time()
    urls_and_indices = [(url, i) for i, url in enumerate(URL)]
    pool.starmap(get_cat, urls_and_indices)
    pool.close()
    pool.join()
    end = time.time()
    duration = end - start
    print('Multithreading with ThreadPool done in {:.4f} seconds'.format(duration))



def pool_work() -> None:
    """
    Данная фукнция обрабатывает запросы к API и БД в многопоточном режиме через Pool.
    """
    pool = multiprocessing.Pool(processes=5)
    start = time.time()
    urls_and_indices = [(url, i) for i, url in enumerate(URL)]
    result = pool.starmap(get_cat, urls_and_indices)
    pool.close()
    pool.join()
    end = time.time()
    duration = end - start
    print('Multithreading with Pool done in {:.4}'.format(duration))


if __name__ == '__main__':
    threadpool_work()
    pool_work()