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


def has_related_files(address):
    text = read_file(address)
    soup = BeautifulSoup(text, 'html.parser')

    scripts = soup.find_all("script", src=True)
    css_links = soup.find_all("link", rel='stylesheet')
    imgs = soup.find_all("img")

    tag = any([scripts, css_links, imgs])
    return tag


def name_generator(dir, old_name):
    updated_name = old_name.split("/")[-1:][0]
    new_name = '/'.join([dir, updated_name])
    return new_name


def dict_files_related(address):
    result = {'imgs': [],
              'scripts': [],
              'css_link': []}
    soup = BeautifulSoup(read_file(address), 'html.parser')

    result['imgs'] = list_of_tags(soup, 'img', 'src')
    result['scripts'] = [tag['src'] for tag in soup.find_all('script',
                                                             src=True)]
    result['css_link'] = [tag['href']
                          for tag in soup.find_all('link', rel="stylesheet")]
    return result


def list_of_tags(soup, the_tag, attr):
    return [tag[attr] for tag in soup.find_all(the_tag)]


def replaced_src(new_src, old_src, soup, file_format):
    options = {'imgs': 'img',
               'scripts': 'script',
               'css_link': 'link'}
    tag = soup.select(options.get(file_format) + '[src="' + old_src + '"]')
    tag[0]['src'] = new_src
    return soup


def replaced_href(new_src, old_src, soup):
    tag = soup.select('link[href="' + old_src + '"]')
    tag[0]['href'] = new_src
    return soup


def replace_src_of_element(file_name, updated_files_list_names,
                           old_img_list_names, key):
    with open(file_name, 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')

    for new_src, old_src in zip(updated_files_list_names, old_img_list_names):
        soup = replaced_src(new_src, old_src, soup, key)

    with open(file_name, 'w') as output_file:
        output_file.write(str(soup))


def replace_href_of_element(file_name, updated_files_list_names,
                            old_img_list_names):
    with open(file_name, 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')

    for new_src, old_src in zip(updated_files_list_names, old_img_list_names):
        soup = replaced_href(new_src, old_src, soup)

    with open(file_name, 'w') as output_file:
        output_file.write(str(soup))


def img_downloader(name, url):
    data = requests.get(url).content
    with open(name, 'wb') as handler:
        handler.write(data)


def script_downloader(name, url):
    data = requests.get(url).content.decode("utf-8")
    with open(name, 'w') as handler:
        handler.write(data)
    return


def css_downloader(name, url):
    data = requests.get(url).content.decode("utf-8")
    with open(name, 'w') as handler:
        handler.write(data)
    return


def download_supporting_files(addresses, urls, format):
    option = {'imgs': img_downloader,
              'scripts': script_downloader,
              'css_link': css_downloader}

    for name, url in zip(addresses, urls):
        option.get(format)(name, url)


def download_additional_files(file_name, dir, address_of_site):
    dict_of_files = dict_files_related(file_name)

    # dict with new names
    dict_of_new_names = {}
    for key, value in dict_of_files.items():
        dict_of_new_names[key] = [name_generator(dir, x) for x in value]

    # dict with urls
    dict_of_files_urls_names = {}
    for key, value in dict_of_files.items():
        dict_of_files_urls_names[key] = list(map(lambda x: address_of_site + x,
                                                 value))

    # combined dict
    combined_dict = {}
    for key in dict_of_new_names:
        combined_dict[key] = [dict_of_new_names[key],
                              dict_of_files_urls_names[key]]

    # downloadi_supporting_files
    for key, lists in combined_dict.items():
        download_supporting_files(*lists, key)

    # replacing links in HTML file
    replace_links(file_name, combined_dict, dict_of_files)


def replace_links(file_name, combined_dict, dict_of_files):
    for key, lists in combined_dict.items():
        if key != 'css_link':
            replace_src_of_element(file_name, lists[0], dict_of_files[key], key)
        else:
            replace_href_of_element(file_name, lists[0], dict_of_files[key])


def download(address_of_site, address_to_put=None):

    r = requests.get(address_of_site)

    if address_to_put is None:
        address_to_put = os.getcwd()

    # creating HTML file
    file_name = create_file(address_to_put, address_of_site)
    write_in_file(file_name, r.text)

    # creating folder
    dir = file_name[:-5] + "_files"
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

    # check if file contains additional files for download
    if has_related_files(file_name):
        download_additional_files(file_name, dir, address_of_site)

    return file_name
