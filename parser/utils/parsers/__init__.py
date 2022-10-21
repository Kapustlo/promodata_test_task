import logging
from typing import Generator, Any
from dataclasses import dataclass

from .base import Parser
from .serializers import (
    CategorySerializer,
    ProductSerializer
)

logger = logging.getLogger(__name__)


class CategoryParser(Parser):
    @property
    def data(self) -> Generator[dict[str, Any], None, None]:
        logger.info('Starting category parsing')

        soup = self.get_soup('/catalog')

        items = soup.select('#catalog-menu a')

        for item in items:
            try:
                yield CategorySerializer(item).data
            except Exception as e:
                logger.error(f'Failed to parse category: {e}')

        logger.info('Finished parsing categories')


@dataclass
class ProductParser(Parser):
    prefix: str = ''

    @property
    def uri(self) -> str:
        return f'{self.prefix}/catalog'

    def get_product_data(self, uri):
        soup = self.get_soup(uri)

        product = soup.select_one('#content')

        assert product is not None

        data = ProductSerializer(product).data

        return data

    def get_page_data(self, page):
        logger.info(f'Parsing products at page: {page}')

        soup = self.get_soup(f'{self.uri}?PAGEN_1={page}')

        current_page = int(soup.select_one('.navigation-current').text)

        if current_page != page:
            logger.info(f'Reached last product page: {page}')

            return None

        products = soup.select('.catalog-item')

        for product in products:
            link = product.select_one('a.name')

            if not link or not link.has_attr('href'):
                continue

            try:
                yield self.get_product_data(link['href'])
            except Exception as e:
                logger.error(f'Failed to parse product: {e}')

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
