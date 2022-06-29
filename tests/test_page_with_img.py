from page_loader.page_loader.page_loader import download
import pook
import os
import shutil


# tests if folder to put file in is None
@pook.on
def test_page_loader_with_img():

    address = 'https://guides.hexlet.io/something_more'

    # fixture response HTML
    file = open('./tests/fixtures/results/result_2/index.html', 'r')
    expected_response = file.read()
    # pook responce for HTML-file
    pook.get(
        address,
        reply=200,
        response_json=expected_response
    )

    # fixture result HTML
    file = open('./tests/fixtures/results/result_2/index_pretty.html', 'r')
    expected_result = file.read()

    # fixture result picture of dog
    address_1 = address + 'picture/dog.jpeg'
    expected_resp_0 = "./tests/fixtures/results/result_2/picture/dog.jpeg"
    pook.get(
        address_1,
        reply=200,
        response_json={'address': expected_resp_0}
    )

    # running the program
    file_name = download(address, None)
    result = open(file_name, 'r').read()
    print(result)

    path_to_folder = os.getcwd() + '/guides-hexlet-io-something_more_files'
    shutil.rmtree(path_to_folder)
    os.remove(os.getcwd() + '/guides-hexlet-io-something_more.html')
    assert result == expected_result


test_page_loader_with_img()


# download or file with 2 imgs
@pook.on
def test_page_loader_with_2_imgs():

    address = 'https://guides.hexlet.io/something_more'

    # fixture response HTML
    file = open('./tests/fixtures/results/result_2/index.html', 'r')
    expected_response = file.read()
    # pook responce for HTML-file
    pook.get(
        address,
        reply=200,
        response_json=expected_response
    )

    # fixture result HTML
    file = open('./tests/fixtures/results/result_2/index_pretty.html', 'r')
    expected_result = file.read()

    # fixture result picture of dog
    address_1 = address + 'picture/dog.jpeg'
    expected_resp_1 = "./tests/fixtures/results/result_3/picture/dog.jpeg"
    pook.get(
        address_1,
        reply=200,
        response_json={'address': expected_resp_1}
    )

    # fixture result picture of monkey
    address_1 = "https://guides.hexlet.io/Users/dmitrijcebrucan/"\
        + "python-project-lvl3/tests/fixtures/results/result_3/"\
        + "picture/monkey.jpeg"
    expected_resp_2 = "./tests/fixtures/results/result_3/picture/monkey.jpeg"
    pook.get(
        address_1,
        reply=200,
        response_json={'address': expected_resp_2}
    )

    # running the program
    file_name = download(address, None)
    result = open(file_name, 'r').read()

    path_to_folder = os.getcwd() + '/guides-hexlet-io-something_more_files'
    shutil.rmtree(path_to_folder)
    os.remove(os.getcwd() + '/guides-hexlet-io-something_more.html')
    assert result == expected_result


test_page_loader_with_2_imgs()
