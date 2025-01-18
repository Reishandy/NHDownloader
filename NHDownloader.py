import argparse
from os import cpu_count
from re import match, fullmatch
from typing import List

from rich.console import Console
from rich.status import Status
from httpx import Client

from scripts.scrapper import scrapper
from scripts.downloader import download, get_download_size
from scripts.archive import archive

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="NHDownloader",
        usage="NHDownloader.py [ID/LINK] [-c] [-o OUTPUT] [-h] [-v]",
        description="This is a simple program to download doujin from nhentai.net"
    )
    parser.add_argument("-v", "--version", action="version", version="Version: 1.0")

    parser.add_argument("id", nargs='+', help="id or link of the doujin to be downloaded")
    parser.add_argument("-o", "--output", nargs='+', help="specify the output file name")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-z", "--zip", action="store_true", help="zip the file")
    group.add_argument("-c", "--cbz", action="store_true", help="save the file to .cbz format")

    args = parser.parse_args()
    n_ids = args.id
    outputs = args.output if args.output is not None else [''] * len(n_ids)

    if len(n_ids) != len(outputs):
        console.print("NHDownloader: error: the number of ids and outputs must match")
        exit(2)

    for n_id, output in zip(n_ids, outputs):
        n_id = get_id(n_id)
        zip_: bool = args.zip
        cbz: bool = args.cbz

        if output and not is_valid_filename(output):
            console.print(f"NHDownloader: error: argument -o/--output: not a valid file name: {output}")
            exit(2)

        download_doujin(n_id, output, cbz, zip_)

    console.print(f"[green]>[/green] Done")


def download_doujin(n_id: str, output: str, cbz: bool, zip_: bool) -> None:
    title: str
    image_urls: List[str]
    # Using multi thread for faster download
    num_workers: int = 2 * cpu_count() + 1

    with Status("Fetching data", console=console):
        try:
            title, image_urls = scrapper(n_id)

            with Client() as client:
                total_size: int = get_download_size(image_urls, client)
        except Exception:
            console.print("Failed to fetch data", style="bold red")
            exit(3)

    console.print(f"[green]>[/green] [white]{title}[/white] [green]@[/green] {len(image_urls)} pages [green]@[/green] "
                  f"{total_size / 1_000_000} MB")

    # Download images
    download(title if output == "" else output, image_urls, total_size, num_workers, console)

    # Package to zip / cbz
    if zip_ or cbz:
        archive(title if output == "" else output, cbz)


def get_id(n_id: str) -> str:
    if fullmatch(r'^\d+$', n_id):
        return n_id
    elif fullmatch(r'^https://(www\.)?nhentai\.net/g/\d+/?$', n_id):
        return n_id.split("/")[4]
    else:
        return ""


def is_valid_filename(filename: str) -> bool:
    pattern: str = r'^[^<>:"/\\|?*\.\s]+$'
    return bool(match(pattern, filename))


if __name__ == "__main__":
    main()
