#!/usr/bin/python3
import os.path
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import argparse
from compiler import KSONCompiler

parser = argparse.ArgumentParser(description='Convert KSON to JSON')
parser.add_argument('filename', type=str,
                    help='KSON file to convert to JSON')
parser.add_argument('--verbose', action='store_true', default=False,
                    help='A boolean switch')
parser.add_argument('--indent', type=int, default=None,
                    help='Indentation for formatting JSON')

args = parser.parse_args()


def main():
    with open(args.filename) as f:
        kson = f.read()
        json = KSONCompiler(verbose=args.verbose).run(kson, indent=args.indent)
        print(json)


if __name__ == '__main__':
    main()
