import pytest

from parser.utils.parsers import CategoryParser, ProductParser


@pytest.fixture
def data():
    client = CategoryParser()

    return list(client.data)


@pytest.fixture
def pdata():
    client = ProductParser()

    return list(client.get_page_data(1))


def test_category_parser_returns_more_than_0_results(data):
    assert len(data) > 0


def test_data_contains_id(data):
    item = data[0]

    assert item['id'] is not None


def test_product_parser_returns_more_than_0_results(pdata):
    assert len(pdata) > 0


def test_product_data_is_present(pdata):
    item = pdata[0]

    assert item['country'] != ''

    assert len(item['sku_images']) > 0

    assert len(item['variants']) > 0
