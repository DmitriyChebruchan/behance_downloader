from bs4 import BeautifulSoup


def replace_links(file_name, combined_dict, dict_of_files):
    for key, lists in combined_dict.items():
        if key != 'link':
            replace_src_of_element(file_name, lists[0], dict_of_files[key], key)
        else:
            replace_href_of_element(file_name, lists[0], dict_of_files[key])


def url_to_file_name(url):
    url = url.replace('https://', '')
    url = url.replace('http://', '')
    url = url.replace('.', '-') + '.html'
    url = url.replace('/', '-')
    return url


def replaced_src(new_src, old_src, soup, file_format):
    options = {'imgs': 'img',
               'scripts': 'script',
               'link': 'link'}
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
