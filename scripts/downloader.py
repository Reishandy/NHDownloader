import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from httpx import Client
from rich.progress import Progress, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console


def download(output: str, image_urls: List[str], total_size: int, num_workers: int, console: Console) -> None:
    if not os.path.exists(output):
        os.makedirs(output)

    with Client() as client:
        progress = Progress(
            TextColumn("[green]>[/green] {task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            console=console,
        )
        download_task = progress.add_task("download", total=total_size, filename="Downloading images")

        with progress:
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                for i, url in enumerate(image_urls, start=1):
                    extension: str = url.split("/")[5].split('.')[1]
                    filename: str = os.path.join(output, f"{i}.{extension}")
                    filename = os.path.abspath(filename)
                    executor.submit(download_image, url, filename, progress, download_task, client)


def get_download_size(image_urls: List[str], client, workers: int) -> int:
    total: int = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(get_single_image_size, url, client) for url in image_urls}
        for future in as_completed(futures):
            total += future.result()

    return total


def get_single_image_size(url: str, client) -> int:
    return int(client.head(url).headers.get('Content-Length', 0))


def download_image(url: str, filename: str, progress, task_id, client) -> None:
    response = client.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as out_file:
        for chunk in response.iter_bytes(1024):
            out_file.write(chunk)
            progress.update(task_id, advance=len(chunk))


if __name__ == "__main__":
    from scrapper import scrapper
    title, urls = scrapper("509176")
    print(urls)
    download(title, urls)