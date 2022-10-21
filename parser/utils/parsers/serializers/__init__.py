from .base import BaseSerializer


class CategorySerializer(BaseSerializer):
    @property
    def data(self):
        element = self.element

        name = element.get('title')

        class_names = element['class'] if element.has_attr('class') else []

        link = element.get('link', '')

        sid = parent_id = None

        items = None

        items = link.split('/')

        try:
            depth = int(class_names[0].split('-')[-1])
        except Exception:
            depth = None

        if depth is not None:
            for i, item in enumerate(items):
                if i == depth:
                    parent_id = item
                elif i + 1 == depth:
                    sid = item

        return {
            'id': sid,
            'parent_id': parent_id,
            'name': name,
            'url': link
        }


class ProductSerializer(BaseSerializer):

    def _map_variant(self, variant):
        tds = variant.select('td')

        article = barcode = price = volume = ''

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
        except Exception:
            country = ''

        try:
            name = element.select_one('h1').text
        except Exception:
            name = ''

        images = element.select('.catalog-element-offer-pictures img')

        images = [image.get('src', '') for image in images]

        bread = element.select_one('.breadcrumb-navigation')

        tree = ''

        if bread:
            lis = bread.select('li')

            for i, li in enumerate(lis):
                if i == 0 or i % 2 != 0:
                    continue

                tree += f'/{li.text}'

        return {
            'variants': variants,
            'country': country,
            'name': name,
            'images': images,
            'tree': tree
        }
