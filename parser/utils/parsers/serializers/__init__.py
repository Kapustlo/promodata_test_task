import logging

from .base import BaseSerializer

logger = logging.getLogger(__name__)


class CategorySerializer(BaseSerializer):
    @property
    def data(self):
        element = self.element

        name = element.text

        class_names = element['class'] if element.has_attr('class') else []

        link = element.get('href', '')

        sid = parent_id = None

        items = None

        items = tuple(
            filter(
                bool,
                link.split('/')
            )
        )
    
        if element.has_attr('id'):
            sid = items[1]
        else:
            sid = items[-1]

            parent_id = items[-2]

        return {
            'id': sid,
            'parent_id': parent_id,
            'name': name,
            'url': link
        }


class ProductSerializer(BaseSerializer):

    def _map_variant(self, variant):
        tds = variant.select('td')

        article = barcode = volume = ''

        in_stock = None

        for i, td in enumerate(tds):
            if i + 1 == len(tds):
                in_stock = bool(td.select('.buybuttonarea'))

            try:
                value = td.select('b')[1].text
            except IndexError:
                continue

            if i == 0:
                article = value
            elif i == 1:
                barcode = value
            elif i == 2:
                volume = value

        if not article:
            logger.error(f'Failed to get article {tds}')

        if not barcode:
            logger.error(f'Failed to get barcode {tds}')

        try:
            price = variant.select_one('.catalog-price').text
        except Exception as e:
            if in_stock:
                logger.error(f'Failed to get price {tds} | {e}')

            price = ''

        return {
            'article': article,
            'barcode': barcode,
            'price': price,
            'volume': volume,
            'in_stock': in_stock
        }

    @property
    def data(self):
        element = self.element

        variants = element.select('.b-catalog-element-offer')

        variants = list(map(self._map_variant, variants))

        try:
            country = element.select_one('.catalog-element-offer-left p').text.split(':')[-1].strip()
        except Exception as e:
            country = ''

            logger.error(f'Faield to get country: {e}')

        try:
            name = element.select_one('h1').text
        except Exception as e:
            name = ''

            logger.error(f'Failed to get product name: {e}')

        images = element.select('.catalog-element-offer-pictures img')

        images = [image.get('src', '') for image in images]

        filled_images = filter(bool, images)

        if not len(list(filled_images)):
            logger.warning(f'No images for product: {name}')
            
        bread = element.select_one('.breadcrumb-navigation')

        tree = ''

        if bread:
            lis = bread.select('li')

            for i, li in enumerate(lis):
                if i == 0 or i % 2 != 0:
                    continue

                tree += f'/{li.text}'
        else:
            logger.error(f'Failed to find breadcrumbs for {name}')

        return {
            'variants': variants,
            'country': country,
            'name': name,
            'images': images,
            'tree': tree
        }
