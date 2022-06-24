import requests
import logging


def download_supporting_files(addresses, urls, format):
    logging.info('List of files for download: \n' + str(addresses))
    option = {'imgs': img_downloader,
              'scripts': script_downloader,
              'css_link': css_downloader}
    for name, url in zip(addresses, urls):
        line = 'File {} with format {} will be downloaded from url {}'.format(
            name, format, url)
        logging.info(line)
        if option.get(format) is None:
            logging('Format of file is not correct.')
            return
        option.get(format)(name, url)


def img_downloader(name, url):
    logging.info('File {} is planned to be downloaded from {}'.format(
        name, url))

    # checking if url works
    try:
        data = requests.get(url).content
    except TypeError:
        raise Warning('Url {} can not return data'.format(url))

    # writing files
    with open(name, 'wb') as handler:
        handler.write(data)
    logging.info('IMG file {} was downloaded'.format(name))


def script_downloader(name, url):
    logging.info('File {} is planned to be downloaded from {}'.format(
        name, url))

    # checking if url works
    try:
        data = requests.get(url).content
    except TypeError:
        raise Warning('Url {} can not return data'.format(url))

    with open(name, 'w') as handler:
        handler.write(data)

    logging.info('Script file {} was downloaded'.format(name))


def css_downloader(name, url):
    logging.info('File {} is planned to be downloaded from {}.'.format(
        name, url))
    try:
        data = requests.get(url).content
    except TypeError:
        raise Warning('Url {} can not return data'.format(url))

    # checking for cerrect reply
    status_code = data.status_code
    if status_code != 200:
        raise Warning('Status_code is {}'.format(status_code))

    with open(name, 'w') as handler:
        handler.write(data)
    logging.info('CSS file {} was downloaded'.format(name))
