"""
DSA - Ch5Ep2
Introduction to Docker & Dockerfile

Simple script to read a file and print to the console.
This script demonstrates how to add files and run a command using docker.


"""
import logging
from logging import DEBUG, INFO
import sys
from os import path
import pandas as pd


# setup logging and logger
logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=INFO,
                    stream=sys.stdout)
logger: logging.Logger = logging


def run(filename='./deb-airports.csv'):
    """
    Read airports csv with pandas and output rows to console
    """
    if path.exists(filename):
        # read csv using pandas
        df = pd.read_csv(filename, header=0)
        # print all columns and sample 100 rows
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', 30, 'display.width', 500):
            print(df.sample(100))
    else:
        logger.error(f"Could not find the input file: {filename}")


if __name__ == "__main__":
    run()
