"""This module describes parser for each entity"""

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
    # Category uri products belong to.
    # If not set, all products will be parsed
    prefix: str = ''

    @property
    def uri(self) -> str:
        uri = '/catalog'

        if not self.prefix.startswith('/'):
            uri += '/'

        uri = f'{uri}{self.prefix}'

        if not uri.endswith('/'):
            uri = f'{uri}/'

        return uri

    def get_product_data(self, uri) -> dict[str, Any]:
        soup = self.get_soup(uri)

        product = soup.select_one('#content')

        assert product is not None

        data = ProductSerializer(product).data

        return data

    def __map_product(self, product):
        link = product.select_one('a.name')

        if not link or not link.has_attr('href'):
            return None

        try:
            return self.get_product_data(link['href'])
        except Exception as e:
            logger.error(f'Failed to parse product: {e}')

    def get_page_data(self, page) -> dict[str, Any]:
        logger.info(f'Parsing products at page: {page}')

        soup = self.get_soup(f'{self.uri}?PAGEN_1={page}')

        current_page = soup.select_one('.navigation-current')

        if current_page:
            current_page = int(current_page.text)

        products = soup.select('.catalog-item')

        return {
            'next': current_page + 1 if current_page else None,
            'page': current_page,
            'results': filter(bool, map(self.__map_product, products))
        }

    @property
    def data(self) -> Generator[dict[str, Any], None, None]:
        page = 1

        while True:
            pdata = self.get_page_data(page)

            results = pdata['results']

            next_page = pdata['next']

            for item in results:
                if not item:
                    continue

                yield item

            if not next_page:
                break
