from bs4 import BeautifulSoup
import logging


# returns text of file
def read_file(address):
    with open(address, 'r') as f:
        return f.read()


def normalize_address(string):
    result = string
    return result


def quantity_related_formats(address):
    text = read_file(address)
    soup = BeautifulSoup(text, 'html.parser')

    scripts = soup.find_all("script", src=True)
    links = soup.find_all("link")
    imgs = soup.find_all("img")

    quantity = len(list(filter(lambda x: x != [], [scripts, links, imgs])))
    return quantity


def quantity_related_files(address):
    text = read_file(address)
    soup = BeautifulSoup(text, 'html.parser')

    scripts = soup.find_all("script", src=True)
    links = soup.find_all("link")
    imgs = soup.find_all("img")

    quantity = len(scripts + links + imgs)
    return quantity


def name_generator(dir, old_name):
    updated_name = old_name.split("/")[-1:][0]
    new_name = '/'.join([dir, updated_name])
    return new_name


# placing prettified text file
def write_in_file(file_name, text):
    with open(file_name, 'w') as output_file:
        output_file.write(str(text))
    logging.info('File created')
