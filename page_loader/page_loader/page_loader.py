#!/usr/bin/env python3
import requests
import os
import logging
from bs4 import BeautifulSoup
from progress.bar import Bar
from urllib.parse import urlparse
from page_loader.additionals.replacers import url_to_file_name, replace_links
from page_loader.additionals.additional_files_downloader import\
    download_supporting_files
from page_loader.additionals.additional_functions import \
    quantity_related_formats, read_file, write_in_file


def create_file(address, url):
    url = url_to_file_name(url)
    name_of_file = os.path.join(address, url)
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


def dict_files_related(address, web_site):
    result = {'imgs': [],
              'scripts': [],
              'css_link': []}
    soup = BeautifulSoup(read_file(address), 'html.parser')

    result['imgs'] = list_of_tags(soup, 'img', 'src')
    result['scripts'] = [tag['src'] for tag in soup.find_all('script',
                                                             src=True)]
    result['link'] = [tag['href'] for tag in soup.find_all('link')]

    for key in result:
        logging.info('List before filtering {}'.format(str(result[key])))
        result[key] = list(filter(lambda el: checker_local_source(el,
                                                                  web_site),
                                  result[key]))
        logging.info('List after filtering {}\n'.format(str(result[key])))

    logging.info('List of parsed imgs:\n{}'.format(result['imgs']))
    logging.info('List of parsed scripts:\n{}'.format(result['scripts']))
    logging.info('List of parsed links:\n{}'.format(result['link']))
    return result


def checker_local_source(address, web_site):
    if address[:4] != 'http':
        return True

    site_host = urlparse(web_site).hostname
    address_host = urlparse(address).hostname
    logging.info('Site-host is {}, address_host is {}'.format(site_host,
                                                              address_host))
    return True if address_host == site_host else False


def list_of_tags(soup, the_tag, first_attr, second_attr, value):
    result = [[tag.get(first_attr), tag.get(second_attr)] for tag in soup.find_all(the_tag)]
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


def download_additional_files(file_name, dir, address_of_site):
    dict_of_files = dict_files_related(file_name, address_of_site)
    logging.info('dict of files is {}'.format(str(dict_of_files)))

    # dict with new names
    dict_of_new_names = {}
    for key, value in dict_of_files.items():
        dict_of_new_names[key] = [name_generator(dir, x) for x in value]

    # dict with urls
    dict_of_files_urls_names = {}
    for key, value in dict_of_files.items():
        logging.info('List of elements in {} list is \n{}'.format(str(key),
                                                                  str(value)))
        dict_of_files_urls_names[key] = list(map(lambda x:
                                                 url_generator(address_of_site,
                                                               x), value))

    # combined dict of new names and urls
    combined_dict = {}
    for key in dict_of_new_names:
        combined_dict[key] = [dict_of_new_names[key],
                              dict_of_files_urls_names[key]]

    # download files
    quantity = quantity_related_formats(file_name)
    bar = Bar('Processing', max=quantity)
    for key, lists in combined_dict.items():
        download_supporting_files(*lists, key)
        bar.next()
    bar.finish()

    # replacing links in HTML file
    replace_links(file_name, combined_dict, dict_of_files)



def download(address_of_site, address_to_put=None):
    print('Sending request.')
    r = requests.get(address_of_site)
    status_code = r.status_code
    if status_code != 200:
        raise Warning('Status_code is {}'.format(status_code))

    logging.info('reply received')

    if address_to_put is None:
        address_to_put = os.getcwd()

    # creating HTML file
    file_name = create_file(address_to_put, address_of_site)
    print(file_name + ' file for links created.')
    soup = BeautifulSoup(r.text, 'html.parser')
    links = list_of_tags(soup, 'a', 'href', 'title', 'Link to project')
    print(str(len(links)) + ' links collected, filtering links.')

    links = filter_incorrect_rights(links)
    result = ""

    i = 1
    while i < len(links) + 1:
        result = result + str(i) + ". " + str(links[i - 1]) + '\n'
        i = i + 1
    print(result)
    
    write_in_file(file_name, result)
    print('Links were added to file.')


def filter_incorrect_rights(links):
    updated_list = []
    quantity = len(links)
    bar = Bar('Processing', max=quantity)
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
    correct_img = 'https://a5.behance.net/2277ca0ee5896a498f5d6b1e4afd27cbb8b71435/img/project/cc/by.svg?cb=264615658'
    result = bool(list(filter(lambda x: x == correct_img, srcs)))
    return result


def list_of_tags(soup, the_tag, first_attr, second_attr, value):
    result = [[tag.get(first_attr), tag.get(second_attr)] for tag in soup.find_all(the_tag)]
    result = list(filter(lambda x: x[0] != '', result))
    result = list(filter(lambda x: x[1] == value, result))
    result = list(map(lambda x: x[0], result))
    return result