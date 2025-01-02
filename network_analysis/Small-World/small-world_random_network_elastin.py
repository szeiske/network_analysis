import networkx as nx

# Number of nodes and edges (elastin)
N = 464
E = 4447

# Generate random network
G_random = nx.gnm_random_graph(N, E)

# Check if network is connected
if nx.is_connected(G_random):
    # Calculate the average shortest path length and the clustering coefficient
    L_rand = nx.average_shortest_path_length(G_random)
    C_rand = nx.average_clustering(G_random)
    
    # Display the results
    print(f"Average shortest path length (L_rand): {L_rand}")
    print(f"Average clustering coefficient (C_rand): {C_rand}")
else:
    print("The network is not connected.")


