from log_parser import LogParser
from timeit import default_timer as timer
import sys
import argparse


def main():
    start = timer()

    parser = argparse.ArgumentParser(description='Parse log file')
    parser.add_argument(dest='filename', metavar='filename',
                        action='store', nargs=1)
    parser.add_argument('-t', '--top', metavar='top', required=False,
                        dest='top', action='store',
                        help='get top n ips and urls', default=3)
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='verbose mode')

    args = parser.parse_args()

    try:
        parser = LogParser(args.filename.pop(), args.top,args.verbose)
        parser.parse()
    except Exception as e:
        print(e)
        sys.exit(1)
    end = timer()
    if args.verbose:
        print("Time taken: ", end - start)
