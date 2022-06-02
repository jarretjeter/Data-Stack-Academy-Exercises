"""
DSA - Ch5Ep2
Advanced Dockerfile

Simple script to read a file and print to the console.
This script takes cmdline args to demonstrate how docker ENTRYPOINT and CMD 
work together.

"""

import logging
from logging import DEBUG, INFO
import sys
from os import path
import argparse
import pandas as pd


# setup logging and logger
logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=INFO,
                    stream=sys.stderr)
logger: logging.Logger = logging


def set_args():
    """
    Define cmdline args
    """
    parser = argparse.ArgumentParser(description="Airports Docker Parser")
    parser.add_argument('action', choices=('print', 'version'), help='what to do?')
    parser.add_argument('-i', '--input', default='./deb-airports.csv', help='source input file')
    parser.add_argument('-n', '--num-rows', type=int, help='number of rows to print')
    parser.add_argument('-fs', '--filter-state', help='filter airports by state')
    args, _ = parser.parse_known_args()
    return args


def run():
    """
    Read airports CSV with pandas and output rows to console
    """
    # read cmdline args
    args = set_args()
    logger.info(f"action: {args.action}")

    if args.action == 'version':
        print("Airport Docker Processor - v1.1")
    elif args.action == 'print':
        filename = args.input
        if path.exists(filename):
            logger.info(f"reading csv file: {filename}")

            # read csv using pandas
            df = pd.read_csv(filename, header=0)

            # filter by state if -fs arg is specified
            if args.filter_state is not None:
                df = df[df['state'].eq(str(args.filter_state))]
                
            # print all columns and rows
            with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', 30, 'display.width', 500):
                # print all row if -n is not specified in args
                if args.num_rows is None:
                    print(df)
                else:
                    print(df.sample(args.num_rows))
        else:
            logger.error(f"Could not find the input file: {filename}")


if __name__ == "__main__":
    run()
