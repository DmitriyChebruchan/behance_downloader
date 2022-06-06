from page_loader.page_loader.page_loader import page_loader


def test_page_loader_no_adress_to_put():
    file = open('./tests/fixtures/results/fixture_google_com.txt', 'r')
    expected_result = file.read()

    address = 'http://google.com'
    file_name = page_loader(None, address)
    file = open(file_name, 'r')
    result = file.read()
    assert result == expected_result


test_page_loader_no_adress_to_put()
