#!/usr/bin/env python3
import requests
import os
from bs4 import BeautifulSoup


def url_to_file_name(url):
    url = url.replace('https://', '')
    url = url.replace('http://', '')
    url = url.replace('.', '-') + '.html'
    url = url.replace('/', '-')
    return url


def create_file(address, url):
    url = url_to_file_name(url)
    name_of_file = os.path.join(address, url)
    f = open(name_of_file, "w")
    f.close()
    return name_of_file


# placing prettified text in HTML file
def write_in_file(file_name, text):
    soup = BeautifulSoup(text, 'html.parser').prettify()
    with open(file_name, 'w') as output_file:
        output_file.write(soup)


# returns text of file
def read_file(address):
    with open(address, 'r') as f:
        return f.read()


def has_imgs(address):
    text = read_file(address)
    soup = BeautifulSoup(text, 'html.parser')
    tag = bool(soup.img)
    return tag


def list_imgs_related(address):
    text = read_file(address)
    soup = BeautifulSoup(text, 'html.parser')
    src = [tag['src'] for tag in soup.find_all('img')]
    return src


def img_name_generator(dir, old_name):
    new_name = old_name.split("/")[-1:][0]
    new_name = '/'.join([dir, new_name])
    return new_name


def img_downloader(img_name, img_url):
    img_data = requests.get(img_url).content
    with open(img_name, 'wb') as handler:
        handler.write(img_data)


def img_replaced_src(new_src, old_src, soup):
    tag = soup.select('img[src="' + old_src + '"]')
    tag[0]['src'] = new_src
    return soup


def replace_url_of_imgs(file_name, updated_img_list_names, old_img_list_names):
    with open(file_name, 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')

    for new_src, old_src in zip(updated_img_list_names, old_img_list_names):
        soup = img_replaced_src(new_src, old_src, soup)

    with open(file_name, 'w') as output_file:
        output_file.write(str(soup))


def download(address_of_site, address_to_put=None):

    r = requests.get(address_of_site)

    if address_to_put is None:
        address_to_put = os.getcwd()

    # creating HTML file
    file_name = create_file(address_to_put, address_of_site)
    write_in_file(file_name, r.text)

    # check if file contains img
    if has_imgs(file_name):
        list_of_imgs = list_imgs_related(file_name)

        dir = file_name[:-5] + "_files"
        # os.mkdir(dir)
        updated_img_list_names = [img_name_generator(dir, x)
                                  for x in list_of_imgs]

        urls_to_imgs = list(map(lambda x: address_of_site + x, list_of_imgs))

        # downloading images in dir
        for img_name, img_url in zip(updated_img_list_names, urls_to_imgs):
            img_downloader(img_name, img_url)

        replace_url_of_imgs(file_name, updated_img_list_names, list_of_imgs)
    return file_name
