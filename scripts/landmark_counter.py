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


def landmark_counter(args) -> None:
    data_fp = args.dataset
    output_dir = args.output_dir

    assert data_fp.endswith(".pyfg"), logger.critical(
        "Dataset must be in PyFG format."
    )

    if (not os.path.isdir(output_dir)):
        os.makedirs(output_dir)
    
    pyfg_data: FactorGraphData = read_from_pyfg_file(data_fp)
    robot_landmark_frequency: Dict[str, List[int]] = {}

    # For each landmark, initialize array where each element corresponds to the frequency of a robot seeing a landmark
    for i in range(pyfg_data.num_landmarks):
        landmark = f"L{i}"
        robot_landmark_frequency[landmark] = [0] * pyfg_data.num_robots

    range_measurements = pyfg_data.range_measurements
    for measure in range_measurements:
        landmark = measure.association[1]
        robot = measure.association[0]

        robot_idx = get_robot_idx_from_char(robot[0])
        robot_landmark_frequency[landmark][robot_idx] += 1
    
    # Print the frequency of each robot seeing each landmark
    # for landmark, frequency in robot_landmark_frequency.items():
    #    print(f"Landmark {landmark}: {frequency}")

    # Save the frequency of each robot seeing each landmark to a CSV file
    base = os.path.basename(data_fp)
    frequency_csv_file = os.path.join(output_dir, f"{os.path.splitext(base)[0]}_landmark_connectivity.csv")

    append_frequency_to_csv(robot_landmark_frequency, pyfg_data.num_robots, frequency_csv_file)

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