from re import sub
from typing import List

from httpx import Client
from bs4 import BeautifulSoup


def scrapper(n_id: str) -> tuple:
    url: str = "https://nhentai.net/g/" + n_id
    with Client(follow_redirects=True) as client:
        response = client.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find(class_="pretty")
    author_element = soup.find(class_="before")
    thumb_containers = soup.find_all('div', class_='thumb-container')

    title = f"{title_element.text} {author_element.text}"
    title = sub(r'[\\/<>:*?"| ]', '_', title)

    image_urls: List[str] = []
    for container in thumb_containers:
        img = container.find('img')
        if img and 'data-src' in img.attrs:
            image_urls.append(img['data-src'])

    url_format = determine_url_format(image_urls[0])

    convert_galleries_link(image_urls, url_format)

    return title, image_urls


def convert_galleries_link(image_urls: List[str], url_format: str) -> None:
    for i in range(len(image_urls)):
        url: List[str] = image_urls[i].split('/')
        url_id: str = url[4]
        extension: str = url[5].split('.')[1]

        url_new = f"{url_format}{url_id}/{i+1}.{extension}"
        image_urls[i] = url_new


def determine_url_format(url: str) -> str:
    url_split: List[str] = url.split('/')
    url_id: str = url_split[4]
    extension: str = url_split[5].split('.')[1]

    for j in range(1, 10):
        if j == 1:
            url_new = f"https://i.nhentai.net/galleries/{url_id}/1.{extension}"
        else:
            url_new = f"https://i{j}.nhentai.net/galleries/{url_id}/1.{extension}"

        if check_url_validity(url_new):
            return url_new.split(url_id)[0]
    

def check_url_validity(url: str) -> bool:
    with Client() as client:
        try:
            response = client.get(url)
        except:
            return False
    return response.status_code == 200


if __name__ == "__main__":
    # print(scrapper("509176"))
    # print(scrapper("509304"))
    print(scrapper("548815"))
