from . import argparser
from .settings import Settings
from .utils.parsers import CategoryParser, ProductParser
from .utils import setup


def main():
    args = argparser.parse_args()

    settings = Settings()

    setup.init(settings)

    items = CategoryParser().data

    for item in items:
        print(item)
