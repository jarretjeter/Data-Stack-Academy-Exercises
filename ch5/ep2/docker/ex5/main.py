"""
DSA - Ch5Ep2
Advanced Dockerfile

Demonstrate saving state with docker volume.
This script saves history of each run using a sqlite3 databases.
Docker image uses a VOLUME to save the sqlite database in between runs.
"""

import logging
import argparse
import sys
import os
from logging import DEBUG, INFO
from datetime import datetime
from os import path
import pandas as pd
from sqlalchemy import create_engine, text, insert, inspect
from sqlalchemy import MetaData, Table, Column, Integer, String
from tabulate import tabulate


# setup logging and logger
logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=INFO,
                    stream=sys.stderr)
logger: logging.Logger = logging


class HistoryStore(object):
    """Store and retrieve cmd run history to/from a sqllite3 database"""

    def __init__(self, dbfile):
        super(object, self).__init__()
        # create sqlalchemy sqlite3 engine and metdata
        # save the database file to dbfile = /data/history.db
        engine = create_engine(f"sqlite+pysqlite:///{dbfile}", future=True)
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        # get the metadata for the main history table
        try:
            metadata.reflect(only=['history'], extend_existing=True, autoload_replace=True)
        except Exception:
            pass
        self.engine = engine
        self.metadata = metadata
        self.conn = conn
        # initialize tables if not done so already
        if not inspect(engine).has_table("history"):
            self.init_db()

    def close(self):
        conn = self.conn
        conn.close()

    def init_db(self, drop_and_replace=False):
        """
        create and initialize sqlite history table 
        """
        logger.info("initializing database...")
        metadata = self.metadata
        # drop tables first
        if drop_and_replace:
            logger.info("dropping all tables")
            metadata.drop_all()
        # history table definition
        history_table = Table("history",
            metadata, 
            Column('id', Integer, primary_key=True),
            Column('cmd', String(256)),
            Column('exec_time', String(50))
        )
        # create all tables
        logger.info("creating history table")
        metadata.create_all(checkfirst=True)

    def insert(self, cmd=None, exec_time=None):
        """
        Insert a single row into history table associated with this run.

        Insert:
            - cmd:         full command line args for this run
            - exec_time:   timestamp of this run
        """
        engine = self.engine
        metadata = self.metadata
        conn = self.conn
        # get history table
        history_table = Table("history", metadata, autoload_with=engine)
        # assign default values to cmd and exec_time if not provided
        cmd = ' '.join(sys.argv) if cmd is None else cmd
        exec_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') if exec_time is None else exec_time
        logger.info(f"inserting record into history table. cm='{cmd}' exec_time='{exec_time}'")
        # create a connection & insert a row into history table
        conn.execute(insert(history_table, 
            [{
                'cmd': cmd,
                'exec_time': exec_time,
            }]))
        conn.commit()

    def history(self, limit=10, print_result=True):
        """
        Get the most recent rows of history table. limit = number of rows printed
        """
        conn = self.conn
        logger.info(f"getting lats {limit} rows of history")
        result = conn.execute(
            text(f"select id, cmd, exec_time from history order by id desc limit {limit}")
        )
        # create a dataframe result
        df = pd.DataFrame(data=[row for row in result.mappings()])
        df = df.set_index('id')
        # print in table format using tabulate pypi module
        if print_result:
            print(tabulate(df[::-1], headers='keys', tablefmt='presto'))        # df[::-1] prints the dataframe in reverse order
        return df[::-1]

    def stats(self, print_result=True):
        """
        Query the history table and return following stats:
            - num_runs:             total number of runs
            - last_exec_time:      timestamp for the last execution time
        """
        logger.info("getting history stats")
        conn = self.conn
        # select query to get stats
        result = conn.execute(
            text("select count(id), max(exec_time) from history")
        )
        # take the first row and return the columns as a namedtuple
        row = result.all()[0]
        num_runs, last_exec_time = row[0], row[1]
        if print_result:
            logger.info("history stats:")
            logger.info("{:>20s} = {}".format("number of runs", num_runs))
            logger.info("{:>20s} = {}".format("last exec time", last_exec_time))
        return num_runs, last_exec_time


def set_args():
    """
    Define cmdline args
    """
    # add reading environment variables as default args
    default_inputfile = os.getenv("INPUT_FILE", "./deb-airports.csv")
    default_num_rows = int(os.getenv("NUM_ROWS", 10))
    logger.info(f"env vars: $NUM_ROWS={default_num_rows} $INPUT_FILE={default_inputfile}")

    parser = argparse.ArgumentParser(description="Airports Docker Parser")
    parser.add_argument('action', choices=('print', 'version', 'history'), help='what to do?')
    parser.add_argument('-i', '--input', default=default_inputfile, help='source input file')
    parser.add_argument('-d', '--dbfile', default='history.db', help='database file path')
    parser.add_argument('-n', '--num-rows', type=int, default=default_num_rows, help='number of rows to print')
    parser.add_argument('-fs', '--filter-state', help='filter airports by state')
    args, _ = parser.parse_known_args()
    return args


def run():
    """
    Read airports csv with pandas and output rows to console
    """
    # read cmdline args
    args = set_args()
    logger.info(f"action: {args.action}")

    # create sqlite3 history object
    history = HistoryStore(args.dbfile)

    # get latest stats from the history table and print to logs
    # this command prints a brief summary of previous runs
    history.stats(print_result=True)
    # record this run into history
    history.insert()

    if args.action == 'version':
        print("Airport Docker Processor - v1.1")
    elif args.action == 'history':
        history.history(print_result=True)
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
