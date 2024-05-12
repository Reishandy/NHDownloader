import argparse
from re import match, fullmatch
from typing import List
from os import path

from scripts.scrapper import scrapper
from scripts.downloader import download
from scripts.archive import archive


# activate venv
script_dir = path.dirname(path.realpath(__file__))

# Construct the path to the virtual environment
venv_dir = path.join(script_dir, '.venv')
activate_this_file = path.join(venv_dir, 'bin', 'activate_this.py')

with open(activate_this_file) as file_:
    exec(file_.read(), {'__file__': activate_this_file})


def main():
    parser = argparse.ArgumentParser(
        prog="NHDownloader",
        usage="NHDownloader.py [ID/LINK] [-c] [-o OUTPUT] [-h] [-v]",
        description="This is a simple program to download doujin from nhentai.net"
    )
    parser.add_argument("-v", "--version", action="version", version="Version: 1.0")

    parser.add_argument("id", help="id or link of the doujin to be downloaded")
    parser.add_argument("-o", "--output", help="specify the output file name")

    archive = parser.add_mutually_exclusive_group()
    archive.add_argument("-z", "--zip", action="store_true", help="zip the file")
    archive.add_argument("-c", "--cbz", action="store_true", help="save the file to .cbz format")

    args = parser.parse_args()
    n_id: str = get_id(args.id)
    output: str = args.output if args.output is not None else ""
    zip_: bool = args.zip
    cbz: bool = args.cbz

    if n_id == "":
        print(f"NHDownloader: error: invalid ID or Link: {args.id}")
        exit(1)

    if output != "" and not is_valid_filename(output):
        print(f"NHDownloader: error: argument -o/--output: not a valid file name: {output}")
        exit(2)

    download_doujin(n_id, output, cbz, zip_)


def download_doujin(n_id: str, output: str, cbz: bool, zip_: bool) -> None:
    title: str
    image_urls: List[str]

    print("Fetching data... ", end="", flush=True)
    try:
        title, image_urls = scrapper(n_id)
        print(f"{title} @ {len(image_urls)} pages")
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        exit(3)

    # Download images
    download(title if output == "" else output, image_urls)

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
