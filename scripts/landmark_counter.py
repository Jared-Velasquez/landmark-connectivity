import argparse
import math
import os
import sys
from typing import List, Tuple
from itertools import product
import matplotlib.pyplot as plt

from py_factor_graph.utils.logging_utils import logger
from py_factor_graph.factor_graph import FactorGraphData

def landmark_counter(args) -> None:
    pass

def main(args):
    parser = argparse.ArgumentParser(
        description="This script is used to analyze PyFG datasets for the connectivity between landmarks and agents."
    )
    parser.add_argument(
        "-d",
        "--dataset",
        type=str,
        required=True,
        help="PyFG filepath to analyze connectivity of landmarks and agents from"
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        required=True,
        help="directory where results are saved",
    )

    args = parser.parse_args()
    landmark_counter(args)

if __name__ == "__main__":
    main(sys.argv[1:])