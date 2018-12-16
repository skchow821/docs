import sys
import argparse
import logging

def parse_arguments():
    parser = argparse.ArgumentParser(description='What am I?')
    parser.add_argument('-n', '--opt_number', dest='opt_number', action='store_const', const=10, default=5, help='help me')
    parser.add_argument('--opt_bool', dest='opt_bool', action='store_true', required=True)
    parser.add_argument('--count_lvl', dest='count_lvl', action='count')
    parser.add_argument('--create_list', dest='create_list', nargs=3, metavar='list_item')
    return parser.parse_args()

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s, %(module)s, %(funcName)s, %(message)s")

def main():
    setup_logging()
    logging.debug('Debug Log')
    args = parse_arguments()

if __name__ == '__main__':
    main()
