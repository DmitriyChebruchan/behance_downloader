from page_loader.page_loader.page_loader import page_loader

def test_page_loader():
    result = page_loader()
    assert result == 'text'

test_page_loader()