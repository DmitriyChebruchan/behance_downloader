from bs4 import BeautifulSoup
import logging


# returns text of file
def read_file(address):
    with open(address, 'r') as f:
        return f.read()


def normalize_address(string):
    result = string
    return result


def quantity_related_files(address):
    text = read_file(address)
    soup = BeautifulSoup(text, 'html.parser')

    scripts = soup.find_all("script", src=True)
    css_links = soup.find_all("link", rel='stylesheet')
    imgs = soup.find_all("img")

    quantity = len(scripts + css_links + imgs)
    return quantity


def name_generator(dir, old_name):
    updated_name = old_name.split("/")[-1:][0]
    new_name = '/'.join([dir, updated_name])
    return new_name


# placing prettified text in HTML file
def write_in_file(file_name, text):
    soup = BeautifulSoup(text, 'html.parser').prettify()
    with open(file_name, 'w') as output_file:
        output_file.write(soup)
    logging.info('HTML file created')
    logging.info('HTML file is \n{}'.format(soup))
