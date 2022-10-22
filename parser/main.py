import csv
import logging
from pathlib import Path

from . import argparser
from .settings import Settings
from .utils.parsers import CategoryParser, ProductParser
from .utils import setup

logger = logging.getLogger(__name__)


def run(settings: Settings):
    setup.init(settings)

    allowed_categories = set(settings.categories)

    client = CategoryParser(
        delay_range=settings.delay_range_s,
        headers=settings.headers,
        max_retries=settings.max_retries
    )

    filter_fn = lambda cat: cat['id'] in allowed_categories or not len(allowed_categories)

    categories = filter(filter_fn, client.data)

    logger.info('Parsing categories')

    out_path = Path(settings.output_directory)

    if not out_path.exists():
        out_path.mkdir()

    category_file = open(out_path / 'categories.csv', 'w')

    product_file = open(out_path / 'products.csv', 'w')

    category_writer = csv.writer(category_file, delimiter=';')

    product_writer = csv.writer(product_file, delimiter=';')

    try:
        for i, category in enumerate(categories):
            logger.debug(category)

            url = category['url']

            logger.info('url')

            if url.endswith('/'):
                url = url[:-1]

            logger.info(f'Parsing products from category {url}')

            pclient = ProductParser(
                prefix=url,
                delay_range=settings.delay_range_s,
                headers=settings.headers,
                max_retries=settings.max_retries
            )

            if not i:
                category_writer.writerow(category.keys())

            category_writer.writerow(category.values())

            for k, item in enumerate(pclient.data):
                logger.debug(item)

                for j, variant in enumerate(item.pop('variants')):
                    data = {
                        **item,
                        **variant
                    }

                    data['sku_images'] = ','.join(data.pop('sku_images'))

                    if not k and not j:
                        product_writer.writerow(data.keys())

                    product_writer.writerow(data.values())

    finally:
        category_file.close()

        product_file.close()


def main():
    args = argparser.parse_args()

    settings = Settings(args.config)

    restarted = 0

    while True:
        try:
            run(settings)

            break
        except Exception as e:
            if not settings.restart or restarted >= settings.restart['restart_count']:
                raise e

            restarted += 1
