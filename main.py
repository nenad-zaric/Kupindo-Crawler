import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from slugify import slugify

root = os.getcwd()


def spider(url, max_page=3):
    page = 1
    while page <= max_page:
        url = url + str(page)
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'lxml')
        item_links = soup.findAll('a', {'class': 'item_link'})
        for link in item_links:
            title = link['title']
            href = link['href']
            print(title)
            get_item_info(href, title)
        page += 1


def get_item_info(href, title):
    title = slugify(title)
    res = requests.get(href).text
    soup = BeautifulSoup(res, 'lxml')
    descript = soup.find('div', {'id': 'opis'}).text
    image = soup.find('a', {'id': 'glavna_slika'})
    image_link = 'http:'+image['href']
    try:
        os.makedirs(f'./files/{title}')
    except FileExistsError:
        pass
    with open(f'./files/{title}/{title}.txt', 'ab+') as f:
        for line in descript:
            f.write(line.encode('utf-16'))
    urllib.request.urlretrieve(image_link, f'./files/{title}/{title}.jpg')


spider('https://www.kupindo.com/Mobilni-telefoni/Mobilni-telefoni/artikli/136_strana_', 5)
