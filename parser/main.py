from . import argparser
from .settings import Settings
from .utils.parsers import CategoryParser, ProductParser


def main():
    args = argparser.parse_args()
    
    settings = Settings()
