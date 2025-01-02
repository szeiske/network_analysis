import networkx as nx
import matplotlib.pyplot as plt

# File path to SIF file 
file_path = r"../network_analysis/PPI/elastin.sif"

# Important nodes to be removed
important_nodes = [
    "9606.ENSP00000346839", "9606.ENSP00000226218", "9606.ENSP00000254301",
    "9606.ENSP00000275493", "9606.ENSP00000379350", "9606.ENSP00000452786",
    "9606.ENSP00000376345", "9606.ENSP00000362680", "9606.ENSP00000398632",
    "9606.ENSP00000211998", "9606.ENSP00000428056", "9606.ENSP00000353408",
    "9606.ENSP00000261405", "9606.ENSP00000262407", "9606.ENSP00000306099",
    "9606.ENSP00000363827", "9606.ENSP00000341189", "9606.ENSP00000316029",
    "9606.ENSP00000384675", "9606.ENSP00000261023", "9606.ENSP00000263967",
    "9606.ENSP00000489597", "9606.ENSP00000264033", "9606.ENSP00000336829",
    "9606.ENSP00000327336", "9606.ENSP00000221930", "9606.ENSP00000380948",
    "9606.ENSP00000263923", "9606.ENSP00000498441", "9606.ENSP00000264498", 
    "9606.ENSP00000296930", "9606.ENSP00000265171", "9606.ENSP00000284981", 
    "9606.ENSP00000296585", "9606.ENSP00000260356", "9606.ENSP00000374455", 
    "9606.ENSP00000282588", "9606.ENSP00000220003", "9606.ENSP00000384169", 
    "9606.ENSP00000282412", "9606.ENSP00000260227", "9606.ENSP00000295148",
    "9606.ENSP00000369897", "9606.ENSP00000320663", "9606.ENSP00000274625",
    "9606.ENSP00000363089"
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
        print(f"Error loading the SIF file: {e}")
        exit()
    return G

# Targeted attack function
def targeted_attack(graph, target_nodes):
    largest_component_sizes = []
    efficiency_list = []
    G_copy = graph.copy()

    for node in target_nodes:
        if node in G_copy:
            G_copy.remove_node(node)
            
            # Calculate the largest component
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

# Load the graph from the SIF file
G = load_sif(file_path)

# Check for missing nodes
missing_nodes = [node for node in important_nodes if node not in G]
if missing_nodes:
    print(f"Missing nodes: {missing_nodes}")

# Perform the analysis
if len(G) > 0:
    largest_sizes_mcc, efficiency_mcc = targeted_attack(G, important_nodes)

    # Visualize the results
    x = list(range(1, len(important_nodes) + 1))
    plt.figure(figsize=(10, 5))

    # Plot largest component
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

