import random
import argparse
import numpy as np
from datetime import datetime
import os
import json


""" Parse command line arguments, generate a random adjacency matrix and print it out. """


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5, help="Number of nodes.")
    parser.add_argument(
        "--p", type=float, default=0.5, help="Probability of edge presence."
    )
    parser.add_argument(
        "--min_weight_value",
        type=float,
        default=-10,
        help="Minimum value for edge weight.",
    )
    parser.add_argument(
        "--max_weight_value",
        type=float,
        default=10,
        help="Maximum value for edge weight.",
    )
    parser.add_argument(
        "--min_noise_radius",
        type=float,
        default=0.001,
        help="Minimum noise radius.",
    )
    parser.add_argument(
        "--max_noise_radius",
        type=float,
        default=0.1,
        help="Maximum noise radius.",
    )
    parser.add_argument(
        "--output_format",
        type=str,
        default="csv",
        help="Output format. Can be csv, npy or both.",
    )
    args = parser.parse_args()

    edge_matrix, noise_matrix = generate_matrix(
        args.n,
        args.p,
        args.min_weight_value,
        args.max_weight_value,
        args.min_noise_radius,
        args.max_noise_radius,
    )

    save_matrix(edge_matrix, noise_matrix, args)


""" Generate a random adjacency matrix with the given parameters. Represent it as a matrix of edge weights and a matrix of edge noise radii. """


def generate_matrix(
    n: int,
    p: float,
    min_weight_value: float,
    max_weight_value: float,
    min_noise_radius: float,
    max_noise_radius: float,
) -> np.ndarray:
    edge_matrix = np.array(
        [
            [
                0
                if i >= j
                else random.uniform(min_weight_value, max_weight_value)
                if random.random() < p
                else 0
                for j in range(n)
            ]
            for i in range(n)
        ]
    )

    noise_matrix = [
        [
            0
            if i >= j
            else random.uniform(min_noise_radius, max_noise_radius)
            if edge_matrix[i][j] != 0
            else 0
            for j in range(n)
        ]
        for i in range(n)
    ]

    return edge_matrix, noise_matrix


""" Save the adjacency matrix in a file of the given format, where the file name is an underscore-separated list of
    the parameters used to generate the matrix, followed by the current timestamp. """


def save_matrix(
    edge_matrix: np.ndarray,
    noise_matrix: np.ndarray,
    args: argparse.Namespace,
) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    dir_name = f"../graphs/{timestamp}/"

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if args.output_format == "csv" or args.output_format == "both":
        np.savetxt(dir_name + "weights.csv", edge_matrix, delimiter=",")
        np.savetxt(dir_name + "noise.csv", noise_matrix, delimiter=",")
    if args.output_format == "npy" or args.output_format == "both":
        np.save(dir_name + "weights.npy", edge_matrix)
        np.save(dir_name + "noise.npy", noise_matrix)

    with open(dir_name + "args.json", "w") as f:
        json.dump(vars(args), f, indent=4)


if __name__ == "__main__":
    main()
