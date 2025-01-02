import networkx as nx
import matplotlib.pyplot as plt

# Reading SIF-file
def load_sif(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                source, target = parts[0], parts[2]
                G.add_edge(source, target)
    return G

file1 = r"../network_analysis/PPI/elastin.sif"
file2 = r"../network_analysis/PPI/catalase.sif"

network1 = load_sif(file1)
network2 = load_sif(file2)

# calculate clustering coefficient
cluster1 = nx.clustering(network1)
cluster2 = nx.clustering(network2)

# average clustering coefficient
avg_cluster1 = nx.average_clustering(network1)
avg_cluster2 = nx.average_clustering(network2)

print(f"Average clustering coefficient (Elastin 464): {avg_cluster1:.4f}")
print(f"Average clustering coefficient (Catalase 151): {avg_cluster2:.4f}")

# Scatter plot representation
plt.figure(figsize=(10, 6))

# Elastin 464 nodes
x1 = range(len(cluster1))
y1 = list(cluster1.values())
plt.scatter(x1, y1, color='orange', alpha=0.7, label='Elastin 464')

# Katalase 151 nodes
x2 = range(len(cluster2))
y2 = list(cluster2.values())
plt.scatter(x2, y2, color='turquoise', alpha=0.7, label='Catalase 151')

# Axis labels and title
plt.xlabel('Node index')
plt.ylabel('clustering coefficient')
plt.title('Scatter plot of the clustering coefficients')
plt.legend()
plt.tight_layout()
plt.show()
