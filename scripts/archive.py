import os
from shutil import make_archive, rmtree


def archive(folder: str, cbz: bool) -> None:
    make_archive(folder, 'zip', folder)

    if cbz:
        new_name = folder + '.cbz'
        if os.path.exists(new_name):
            os.remove(new_name)
        os.rename(folder + '.zip', new_name)

    if os.path.exists(folder):
        rmtree(folder)


if __name__ == "__main__":
    from downloader import download
    from scrapper import scrapper

    title, urls = scrapper("509176")
    print(urls)
    download(title, urls)

    archive(title, True)