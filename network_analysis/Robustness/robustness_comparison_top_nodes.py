import networkx as nx
import networkx as nx
import matplotlib.pyplot as plt


file_path_1 = r"../network_analysis/PPI/elastin.sif"
file_path_2 = r"../network_analysis/PPI/catalase.sif"

# Important nodes to be removed
important_nodes_1 = [
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

important_nodes_2 = [
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
    efficiency_list = []
    G_copy = graph.copy()

    for node in target_nodes:
        if node in G_copy:
            G_copy.remove_node(node)
            
            # Calculate global efficiency
            if len(G_copy) > 0:
                efficiency_list.append(nx.global_efficiency(G_copy))
            else:
                efficiency_list.append(0)
        else:
            print(f"Node {node} not found in the graph.")
    
    return efficiency_list

# Load both graphs
G1 = load_sif(file_path_1)
G2 = load_sif(file_path_2)

# Perform analysis
if len(G1) > 0 and len(G2) > 0:
    efficiency_mcc_1 = targeted_attack(G1, important_nodes_1)
    efficiency_mcc_2 = targeted_attack(G2, important_nodes_2)

    # Calculate percentages
    total_nodes_1 = len(G1)
    total_nodes_2 = len(G2)
    percentage_x_1 = [i / total_nodes_1 * 100 for i in range(1, len(important_nodes_1) + 1)]
    percentage_x_2 = [i / total_nodes_2 * 100 for i in range(1, len(important_nodes_2) + 1)]
    
    # Plot
    plt.figure(figsize=(10, 6))

    # Plot for the first graph (elastin 464 nodes)
    plt.plot(percentage_x_1, efficiency_mcc_1, label="Global Efficiency (elastin_464)", color='blue')

     # Plot for the second graph (catalase 151 nodes)
    plt.plot(percentage_x_2, efficiency_mcc_2, label="Global Efficiency (catalase_151)", color='orange')

    # Axes and title
    plt.xlabel("Percentage of Nodes Removed (%)")
    plt.ylabel("Global Efficiency")
    plt.title("Effect of Node Removal on Global Efficiency")
    plt.legend()

    plt.tight_layout()
    plt.show()

else:
     print("One or both graphs contain no nodes.")
