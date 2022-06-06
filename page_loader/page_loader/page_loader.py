#!/usr/bin/env python3
import requests
import os


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


def write_in_file(file_name, text):
    with open(file_name, 'w') as output_file:
        output_file.write(text)


def download(address_of_site='https://google.com', address_to_put=None):

    r = requests.get(address_of_site)

    if address_to_put is None:
        address_to_put = os.getcwd()

    file_name = create_file(address_to_put, address_of_site)
    write_in_file(file_name, r.text)
    print(file_name)
    return file_name
