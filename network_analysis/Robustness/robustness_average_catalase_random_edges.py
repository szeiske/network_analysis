import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

# Function to load a graph from a SIF file
def load_sif(file_path):
    G = nx.Graph()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 3:
                    source = parts[0]
                    interaction = parts[1]  
                    target = parts[2]
                    G.add_edge(source, target, interaction=interaction)
        print(f"Graph successfully loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        print(f"Error loading the SIF file: {e}")
        exit()
    return G

# Function for randomly selecting and removing edges
def random_edge_attack(graph, num_edges):
    largest_component_sizes = []
    efficiency_list = []
    G_copy = graph.copy()

    # Random selection of edges
    random_edges = random.sample(list(G_copy.edges), min(num_edges, len(G_copy.edges)))

    for edge in random_edges:
        if G_copy.has_edge(*edge):
            G_copy.remove_edge(*edge)

            # Calculate largest component
            if len(G_copy) > 0:
                largest_component = len(max(nx.connected_components(G_copy), key=len))
                largest_component_sizes.append(largest_component)

                # Calculate global efficiency
                efficiency_list.append(nx.global_efficiency(G_copy))
            else:
                largest_component_sizes.append(0)
                efficiency_list.append(0)

    return largest_component_sizes, efficiency_list

# Load graph from SIF file
file_path = r"../network_analysis/PPI/catalase.sif"
G = load_sif(file_path)

# Check if the graph contains nodes
if len(G) > 0:
    num_random_edges = 160  
    num_runs = 50           
    largest_sizes_all = []
    efficiency_all = []

    # Multiple runs
    for _ in range(num_runs):
        largest_sizes, efficiency = random_edge_attack(G, num_random_edges)
        largest_sizes_all.append(largest_sizes)
        efficiency_all.append(efficiency)

    # Calculate average values
    avg_largest_sizes = np.mean(largest_sizes_all, axis=0)
    avg_efficiency = np.mean(efficiency_all, axis=0)

    # Visualize results
    x = list(range(1, num_random_edges + 1))
    plt.figure(figsize=(10, 5))

    # Plot largest component
    plt.subplot(1, 2, 1)
    plt.plot(x, avg_largest_sizes, label="Avg Largest Component Size", color='blue')
    plt.xlabel("Number of Edges Removed")
    plt.ylabel("Size of Largest Component")
    plt.title("Average Largest Component Size")
    plt.legend()

    # Plot efficiency
    plt.subplot(1, 2, 2)
    plt.plot(x, avg_efficiency, label="Avg Global Efficiency", color='orange')
    plt.xlabel("Number of Edges Removed")
    plt.ylabel("Global Efficiency")
    plt.title("Average Global Efficiency")
    plt.legend()

    plt.tight_layout()
    plt.show()
else:
    print("The graph contains no nodes.")

