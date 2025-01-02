import networkx as nx
import matplotlib.pyplot as plt

# File path to SIF file 
file_path = r"../network_analysis/PPI/catalase.sif"

# Important nodes to be removed
important_nodes = [
    "9606.ENSP00000349543", "9606.ENSP00000391601", "9606.ENSP00000349016",
    "9606.ENSP00000295030", "9606.ENSP00000288774", "9606.ENSP00000482609",
    "9606.ENSP00000299601", "9606.ENSP00000356405", "9606.ENSP00000262306",
    "9606.ENSP00000348089", "9606.ENSP00000453801", "9606.ENSP00000221265",
    "9606.ENSP00000478121", "9606.ENSP00000374280", "9606.ENSP00000355013"
]

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
        print(f"Error loading SIF file: {e}")
        exit()
    return G

# Target node function
def targeted_attack(graph, target_nodes):
    largest_component_sizes = []
    efficiency_list = []
    G_copy = graph.copy()

    for node in target_nodes:
        if node in G_copy:
            G_copy.remove_node(node)
            
            # Calculate largest component size
            if len(G_copy) > 0:
                largest_component = len(max(nx.connected_components(G_copy), key=len))
                largest_component_sizes.append(largest_component)
                
                # Calculate global efficiency
                efficiency_list.append(nx.global_efficiency(G_copy))
            else:
                largest_component_sizes.append(0)
                efficiency_list.append(0)
        else:
            print(f"Node {node} not found in the graph.")
    
    return largest_component_sizes, efficiency_list

# Load graph from the SIF file
G = load_sif(file_path)

# Check for missing nodes
missing_nodes = [node for node in important_nodes if node not in G]
if missing_nodes:
    print(f"Missing nodes: {missing_nodes}")

# Perform analysis
if len(G) > 0:
    largest_sizes_mcc, efficiency_mcc = targeted_attack(G, important_nodes)

    # Visualize results
    x = list(range(1, len(important_nodes) + 1))
    plt.figure(figsize=(10, 5))

    # Plot largest component size
    plt.subplot(1, 2, 1)
    plt.plot(x, largest_sizes_mcc, label="Largest Connected Component Size", color='blue')
    plt.xlabel("Number of Nodes Removed")
    plt.ylabel("Size of Largest Component")
    plt.title("Largest Component Size During Attack")
    plt.legend()

    # Plot efficiency
    plt.subplot(1, 2, 2)
    plt.plot(x, efficiency_mcc, label="Global Efficiency", color='green')
    plt.xlabel("Number of Nodes Removed")
    plt.ylabel("Global Efficiency")
    plt.title("Global Efficiency During Attack")
    plt.legend()

    plt.tight_layout()
    plt.show()
else:
    print("The graph contains no nodes.")
