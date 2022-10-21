from argparse import ArgumentParser

__author__ = 'Kapustlo'

argparser = ArgumentParser(description='zootovary.ru parser')

argparser.add_argument(
    '--config',
    dest='config',
    type=str,
    default='./config.json',
    required=False,
    help='Config path'
)
