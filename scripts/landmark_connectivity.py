import argparse
import math
import os
import sys
from typing import Dict, List, Tuple
from itertools import product
import matplotlib.pyplot as plt

from py_factor_graph.utils.logging_utils import logger
from py_factor_graph.factor_graph import FactorGraphData
from py_factor_graph.io.pyfg_file import read_from_pyfg_file
from py_factor_graph.utils.name_utils import (
    get_robot_idx_from_char, 
    get_robot_char_from_number
)

def append_frequency_to_csv(frequency: Dict[str, List[int]], num_robots: int, csv_fp: str) -> None:
    """Append the frequency of each robot seeing each landmark to a CSV file.

    Args:
        frequency (Dict[str, List[int]]): frequency of each robot seeing each landmark
        csv_fp (str): filepath to save the CSV file

    Returns:
        None
    """
    with open(csv_fp, "w") as f:
        f.write("landmark_symbol")
        for i in range(num_robots):
            f.write(f",{get_robot_char_from_number(i)}_count")
        f.write("\n")

        for landmark, freq in frequency.items():
            f.write(landmark)
            for count in freq:
                f.write(f",{count}")
            f.write("\n")


def landmark_counter(pyfg_filepath: str, output_dir: str) -> None:
    """Analyze the connectivity between landmarks and agents in a PyFG dataset.

    Args:
        pyfg_filepath (str): filepath to the PyFG dataset
        output_dir (str): directory to save the results
    
    Returns:
        None
    """

    assert pyfg_filepath.endswith(".pyfg"), logger.critical(
        "Dataset must be in PyFG format."
    )

    if (not os.path.isdir(output_dir)):
        os.makedirs(output_dir)
    
    pyfg_data: FactorGraphData = read_from_pyfg_file(pyfg_filepath)
    robot_landmark_frequency: Dict[str, List[int]] = {}

    logger.info(f"Counting frequency of connectivity between robots and landmarks in {pyfg_filepath}")

    # For each landmark, initialize array where each element corresponds to the frequency of a robot seeing a landmark
    for i in range(pyfg_data.num_landmarks):
        landmark = f"L{i}"
        robot_landmark_frequency[landmark] = [0] * pyfg_data.num_robots

    range_measurements = pyfg_data.range_measurements
    for measure in range_measurements:
        # Skip over inter-robot range measurements
        if measure.association[1][0] != "L":
            continue

        landmark = measure.association[1]
        robot = measure.association[0]

        robot_idx = get_robot_idx_from_char(robot[0])
        robot_landmark_frequency[landmark][robot_idx] += 1

    # Save the frequency of each robot seeing each landmark to a CSV file
    base = os.path.basename(pyfg_filepath)
    frequency_csv_file = os.path.join(output_dir, f"{os.path.splitext(base)[0]}_landmark_connectivity.csv")

    append_frequency_to_csv(robot_landmark_frequency, pyfg_data.num_robots, frequency_csv_file)


def landmark_connectivity(args) -> None:
    """Recursively scan directory for PyFG files and analyze connectivity between landmarks and agents.

    Args:
        args (Namespace): command line arguments
    
    Returns:
        None
    """

    dataset_dir = args.dataset
    output_dir = args.output_dir

    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith(".pyfg"):
                pyfg_filepath = os.path.join(root, file)
                landmark_counter(pyfg_filepath, output_dir)

def main(args):
    parser = argparse.ArgumentParser(
        description="This script is used to analyze PyFG datasets for the connectivity between landmarks and agents."
    )
    parser.add_argument(
        "-d",
        "--dataset",
        type=str,
        required=True,
        help="Filepath of directory that contains PyFG files to analyze connectivity from",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        required=True,
        help="directory where results are saved",
    )

    args = parser.parse_args()
    landmark_connectivity(args)

if __name__ == "__main__":
    main(sys.argv[1:])