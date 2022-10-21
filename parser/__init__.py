from argparse import ArgumentParser

__author__ = 'Kapustlo'

parser = ArgumentParser(description='zootovary.ru parser')

parser.add_argument(
    '--config',
    dest='config',
    type=str,
    default='./config.json',
    required=False,
    help='Config path'
)
