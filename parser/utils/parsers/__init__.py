from typing import Generator, Any

from .base import Parser
from .serializers import (
    CategorySerializer,
    ProductSerializer
)


class CategoryParser(Parser):
    @property
    def data(self) -> Generator[dict[str, Any], None, None]:
        soup = self.get_soup('/catalog')

        items = soup.select('.catalog-left a[title]')

        for item in items:
            try:
                yield CategorySerializer(item).data
            except Exception:
                pass


class ProductParser(Parser):
    def get_product_data(self, uri):
        soup = self.get_soup(uri)

        product = soup.select_one('#content')

        assert product is not None

        data = ProductSerializer(product).data

        return data

    def get_page_data(self, page):
        soup = self.get_soup(f'/catalog?PAGEN_1={page}')

        current_page = int(soup.select_one('.navigation-current').text)

        if current_page != page:
            return None

        products = soup.select('.catalog-item')

        for product in products:
            link = product.select_one('a.name')

            if not link or not link.has_attr('href'):
                continue

            try:
                yield self.get_product_data(link['href'])
            except Exception as e:
                raise e

    @property
    def data(self) -> Generator[dict[str, Any], None, None]:
        page = 1

        while True:
            pdata = self.get_page_data(page)

            if pdata is None:
                break

            for item in pdata:
                if not item:
                    continue

                yield item
