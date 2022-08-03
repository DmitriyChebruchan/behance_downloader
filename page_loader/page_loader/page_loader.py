#!/usr/bin/env python3
import json
import requests
import os
import logging
from bs4 import BeautifulSoup
from progress.bar import Bar
from urllib.parse import urlparse
from page_loader.additionals.replacers import url_to_file_name
from page_loader.additionals.additional_functions import read_file


def create_file(address, url):
    file_name = url_to_file_name(url)
    name_of_file = os.path.join(address, file_name)
    f = open(name_of_file, "w")
    f.close()
    return name_of_file


def has_related_files(address):
    text = read_file(address)
    soup = BeautifulSoup(text, 'html.parser')

    scripts = soup.find_all("script", src=True)
    css_links = soup.find_all("link", rel='stylesheet')
    imgs = soup.find_all("img")

    tag = any([scripts, css_links, imgs])
    return tag


# generates new name for file based on dir to put and old name
def name_generator(dir, old_name):
    last_name_part = old_name.split("/")[-1]
    folder = dir.split("/")[-1]
    new_name = '/'.join([folder, last_name_part])
    return new_name


def list_of_tags(soup, the_tag, first_attr, second_attr, value):
    result = [[tag.get(first_attr), tag.get(second_attr)] for tag in
              soup.find_all(the_tag)]
    result = list(filter(lambda x: x[0] != '', result))
    result = list(filter(lambda x: x[1] == value, result))
    result = list(map(lambda x: x[0], result))
    return result


def url_generator(web_site, name):
    logging.info('web site is {}'.format(web_site))
    logging.info('name of file is {}'.format(name))

    if name[:4] == 'http':
        logging.info('result of combination is {}'.format(name))
        return name
    if name[0] == '/':
        site = urlparse(web_site).scheme + "://" + urlparse(web_site).hostname
        logging.info('host name is {}'.format(site))
        logging.info('result of combination is {}'.format(site + name))
        return site + name
    else:
        logging.info('result of combination is {}'.format(web_site + name))
        return web_site + name


def download(address_of_site, address_to_put=None):
    print('Sending request.')
    r = requests.get(address_of_site)

    status_code = r.status_code
    if status_code != 200:
        raise Warning('Status_code is {}'.format(status_code))

    logging.info('reply received')

    if address_to_put is None:
        address_to_put = os.getcwd()

    # collecting links
    soup = BeautifulSoup(r.text, 'html.parser')
    links = list_of_tags(soup, 'a', 'href', 'title', 'Link to project')
    print(str(len(links)) + ' links collected, filtering links.')

    links = filter_incorrect_rights(links)

    # show result
    result = result_generator(links)
    print('result is \n{}'.format(result))

    # creating file
    file_name = create_file(address_to_put, address_of_site)
    print('{} file for links created. \n{} links added'.format(str(file_name),
                                                               len(links)))

    # saving in file
    if links == []:
        print('No links collected.')
        return
    append_JSON_file(links, file_name)
    print('Links were added to file.')


def append_JSON_file(information, file):
    list_of_el = read_JSON_file(file)
    if list_of_el == '':
        list_of_el = []
    list_of_el.append(information)
    write_JSON_file(file, list_of_el)


def read_JSON_file(file):
    with open(file, 'r') as f:
        return json.load(f)


def write_JSON_file(file, information):
    with open(file, "w") as f:
        json.dump(information, f, indent=4, separators=(',', ': '))
# def download(*args):
#     driver = webdriver.Chrome()
#     driver.get('https://www.behance.net')

#     elems = driver.find_elements_by_xpath("//a[@title='Link to project']")
#     links = []

#     for elem in elems:
#         links.append(elem.get_attribute('title'))
#         print('Title : ' +elem.get_attribute('title'))

#     print(links)
#     return


def result_generator(links):
    result = ""
    i = 1
    while i < len(links) + 1:
        result = result + str(i) + ". " + str(links[i - 1]) + '\n'
        i = i + 1
    return result


def filter_incorrect_rights(links):
    updated_list = []

    bar = Bar('Processing', max=len(links))
    for el in links:
        if rights_checker(el):
            updated_list.append(el)
        bar.next()
    bar.finish()
    return updated_list


def rights_checker(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    srcs = [tag.get('src') for tag in soup.find_all('img')]
    correct_img = 'https://a5.behance.net/2277ca0ee5896a498f5d6b1e4' + \
        'afd27cbb8b71435/img/project/cc/by.svg?cb=264615658'
    result = bool(list(filter(lambda x: x == correct_img, srcs)))
    return result
