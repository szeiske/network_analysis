import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


file_path = r"../network_analysis/PPI/elastin.graphml"

# Load the network
G = nx.read_graphml(file_path)

# Calculate the node degree
degree_sequence = [deg for _, deg in G.degree()]
degree_count = Counter(degree_sequence)

# Degree distribution
x, y = zip(*degree_count.items())
x = np.array(x)
y = np.array(y)

# Function for fitting a power law
def fit_power_law(x, y):
    log_x = np.log(x)
    log_y = np.log(y)
    slope, intercept = np.polyfit(log_x, log_y, 1)
    return slope, intercept

# Calculate the power-law fit
slope, intercept = fit_power_law(x, y)
power_law_fit = np.exp(intercept) * x**slope

# Plot of the degree distribution with power-law comparison
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Degree Distribution', alpha=0.6)
plt.plot(x, power_law_fit, color='red', linestyle='--', label=f'Power-Law-Fit (k^-{abs(slope):.2f})')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Degree (k)')
plt.ylabel('Number of nodes with degree k')
plt.title('Log-log plot of the degree distribution with power-law comparison')
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()

# Display the fit parameters
print(f"Fit to power law: Slope (exponent) = {-slope:.2f}")
print(f"y = exp({intercept:.2f}) * x^{slope:.2f}")
