from page_loader.page_loader.page_loader import download
import tempfile
import pook
import os


# tests if folder to put file in is None
@pook.on
def test_page_loader_no_adress_to_put():

    address = 'https://guides.hexlet.io/'

    # fixture result HTML
    file = open('./tests/fixtures/results/result_1/guides_hexlet_io.html', 'r')
    expected_result = file.read()

    # pook responce for HTML-file
    pook.get(
        address,
        reply=200,
        response_json=expected_result
    )

    # running the program
    file_name = download(address, None)
    result = open(file_name, 'r').read()
    os.removedirs(os.getcwd() + '/guides-hexlet-io-_files')
    os.remove(os.getcwd() + '/guides-hexlet-io-.html')
    assert result == expected_result


test_page_loader_no_adress_to_put()


# tests if folder to put file in is tempfolder
@pook.on
def test_page_loader_with_adress_to_put():

    address = 'https://guides.hexlet.io/'

    # fixture HTML result
    file = open('./tests/fixtures/results/result_1/guides_hexlet_io.html', 'r')
    expected_result = file.read()

    # pook responce
    pook.get(
        address,
        reply=200,
        response_json=expected_result
    )

    # creating temp folder
    folder = tempfile.TemporaryDirectory()
    folders_name = folder.name

    # running the program
    file_name = download(address, folders_name)
    result = open(file_name, 'r').read()

    assert result == expected_result


test_page_loader_no_adress_to_put()
