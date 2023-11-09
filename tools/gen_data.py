import argparse
import numpy as np
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_points", type=int, default=20, help="Number of datapoints."
    )
    parser.add_argument("--input_dir", type=str, required=True, help="Input directory.")
    parser.add_argument(
        "--min_source_val",
        type=float,
        default=0,
        help="Minimum value for source nodes.",
    )
    parser.add_argument(
        "--max_source_val",
        type=float,
        default=10,
        help="Maximum value for source nodes.",
    )
    args = parser.parse_args()

    weights = np.loadtxt(args.input_dir + "/weights.csv", delimiter=",")
    noise = np.loadtxt(args.input_dir + "/noise.csv", delimiter=",")

    data = gen_data(weights, noise, args)

    save_data(data, args)


""" Generate the data based on the graph specification. """


def gen_data(
    weights: np.ndarray, noise: np.ndarray, args: argparse.Namespace
) -> np.ndarray:
    num_vars = weights.shape[0]

    data = np.zeros((args.num_points, num_vars))
    data[:, 0] = np.random.uniform(
        args.min_source_val, args.max_source_val, args.num_points
    )
    for j in range(1, num_vars):
        # Determine that this variable is a source if all incoming weights are zero.
        if np.all(weights[:, j] == 0):
            data[:, j] = np.random.uniform(
                args.min_source_val, args.max_source_val, args.num_points
            )
            continue

        # Calculate the value of the jth variable based on the values of the previous variables (incoming edges).
        for i in range(j):
            data[:, j] += weights[i, j] * data[:, i] + np.random.normal(0, noise[i, j])

    return data


""" Save the data to the output directory."""


def save_data(data: np.ndarray, args: argparse.Namespace):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    output_dir = "../datasets/" + args.input_dir.split("/")[-1]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    np.savetxt(output_dir + f"/data_{timestamp}.csv", data, delimiter=",")


if __name__ == "__main__":
    main()
