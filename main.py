
import argparse
import logging
import os
import subprocess
import sys

# local
from pdb import help

import helpers
import stats

# main global chia executable name
CHIA="chia"
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()

    if args.stats:
        stats.runStatsFromUser()

    if not helpers.is_tool(CHIA):
        logging.error("Unable to find CHIA executable entry point.")
        sys.exit(-1)

# entry point
if __name__ == '__main__':
    main()
