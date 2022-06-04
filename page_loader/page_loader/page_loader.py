#!/usr/bin/env python3
import requests
import os


def normalise_url(url):
    url = url.replace('https://', '')
    url = url.replace('.', '-') + '.html'
    url = url.replace('/', '-')
    return url


def create_file(address, url):
    url = normalise_url(url)
    name_of_file = os.path.join(address, url)
    f = open(name_of_file, "w")
    f.close()
    return name_of_file


def write_in_file(file_name, text):
    with open(file_name, 'w') as output_file:
        output_file.write(text)


def page_loader(address_to_put=None, address_of_site='https://google.com'):

    r = requests.get(address_of_site)

    if address_to_put is None:
        address_to_put = os.getcwd()
        file_name = create_file(address_to_put, address_of_site)
    else:
        file_name = address_to_put
    write_in_file(file_name, r.text)
    print(file_name)
    return
