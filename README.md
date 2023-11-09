# causal-gg-wp
A small set of tools for causal Graph Generation where Weights are Probabilistic.


## Generating a causal graph.

The script in `tools/gen_graph.py` generates a random causal graph as a linear structural equation model with `n` nodes. 

The nodes are assumed to be in topological order and each edge from a node to a subsequent node exists with probability `p`. Each edge that exists is assigned a weight uniformly from [`min_weight_value`, `max_weight_value`] and a noise radius uniformly from [`min_noise_radius`, `max_noise_radius`]. 

The output matrices for the edge weights and noise radii are written in a timestamped directory under `graphs/`, in the format specified (`csv`, `npy` or both), alongside a JSON file with the arguments used to generate them. 

Here is a list of the script arguments:

    --n: Number of nodes (default: 5)
    --p: Probability of edge presence (default: 0.5)
    --min_weight_value: Minimum value for edge weight (default: -10)
    --max_weight_value: Maximum value for edge weight (default: 10)   
    --min_noise_radius: Minimum noise radius (default: 0.001)
    --max_noise_radius: Maximum noise radius (default: 0.1)
    --output_format: Output format. Can be csv, npy or both (default: csv)


## Generating a dataset based on a causal graph.

The script in `tools/gen_data.py` generates a set of `num_points` data points based on a graph previously produced with `tools/gen_graph.py` and located in `input_dir`.

For each datapoint, variables associated with source nodes are assigned values drawn uniformly from [`min_source_val`, `max_source_val`], while the values of the rest of the variables are calculated
based on the `weights` matrix of the causal graph specification, with an added noise term per edge drawn from a normal distribution with a radius based on the `noise` matrix of the causal graph
specification.


Here is a list of the script arguments:

    --num_points: Nnumber of datapoints you want to generate (default is 20)
    --input_dir: Directory where your causal graph specification is located (required)
    --min_source_val: the minimum value for source nodes (default is 0)
    --max_source_val: the maximum value for source nodes (default is 10)
