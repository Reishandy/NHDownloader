import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from httpx import Client
from tqdm import tqdm


def download(output: str, image_urls: List[str]) -> None:
    if not os.path.exists(output):
        os.makedirs(output)

    with Client() as client:
        # Using multi thread for faster download
        num_workers: int = 2 * os.cpu_count() + 1
        print("Fetching download size... ", end="", flush=True)
        total_size: int = get_download_size(image_urls, client, num_workers)
        print(f"{total_size / 1_000_000} MB")

        progress = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading images")
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for i, url in enumerate(image_urls, start=1):
                extension: str = url.split("/")[5].split('.')[1]
                filename: str = os.path.join(output, f"{i}.{extension}")
                executor.submit(download_image, url, filename, progress, client)

        progress.close()


def get_download_size(image_urls: List[str], client, workers: int) -> int:
    total: int = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(get_single_image_size, url, client) for url in image_urls}
        for future in as_completed(futures):
            total += future.result()

    return total


def get_single_image_size(url: str, client) -> int:
    return int(client.head(url).headers.get('Content-Length', 0))


def download_image(url: str, filename: str, progress, client) -> None:
    response = client.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as out_file:
        for chunk in response.iter_bytes(1024):
            out_file.write(chunk)
            progress.update(len(chunk))

    progress.update_to(progress.n + 1)


if __name__ == "__main__":
    from scrapper import scrapper
    title, urls = scrapper("509030")
    print(urls)
    download(title, urls)
