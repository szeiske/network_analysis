import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


file_path_1 = r"../network_analysis/PPI/elastin.graphml"
file_path_2 = r"../network_analysis/PPI/catalase.graphml"

# Load the networks
G1 = nx.read_graphml(file_path_1)
G2 = nx.read_graphml(file_path_2)

# Calculate the degree of the nodes for both networks
degree_sequence_1 = [deg for _, deg in G1.degree()]
degree_sequence_2 = [deg for _, deg in G2.degree()]

# Calculate the degree distributions
degree_count_1 = Counter(degree_sequence_1)
degree_count_2 = Counter(degree_sequence_2)

# Convert to x, y for both degree distributions
x1, y1 = zip(*degree_count_1.items())
x2, y2 = zip(*degree_count_2.items())
x1 = np.array(x1)
y1 = np.array(y1)
x2 = np.array(x2)
y2 = np.array(y2)

# Function for fitting a power law
def fit_power_law(x, y):
    log_x = np.log(x)
    log_y = np.log(y)
    slope, intercept = np.polyfit(log_x, log_y, 1)
    return slope, intercept

# Calculate the power-law fit for both networks
slope_1, intercept_1 = fit_power_law(x1, y1)
slope_2, intercept_2 = fit_power_law(x2, y2)

power_law_fit_1 = np.exp(intercept_1) * x1**slope_1
power_law_fit_2 = np.exp(intercept_2) * x2**slope_2

# Plot the degree distributions of both networks in a single plot
plt.figure(figsize=(10, 6))

# Plot for the first network (Elastin)
plt.scatter(x1, y1, color='blue', label='Degree distribution Elastin', alpha=0.6)

# Plot for the second network (Katalase)
plt.scatter(x2, y2, color='green', label='Degree distribution Catalase', alpha=0.6)

# Power-law fit for both networks
plt.plot(x1, power_law_fit_1, color='lightblue', linestyle='--', label=f'Power-Law-Fit Elastin (k^-{abs(slope_1):.2f})')
plt.plot(x2, power_law_fit_2, color='lightgreen', linestyle='--', label=f'Power-Law-Fit Catalase (k^-{abs(slope_2):.2f})')

# Axis labels and title
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Degree (k)')
plt.ylabel('Number of nodes with degree k')
plt.title('Comparison of degree distributions: Elastin vs. Catalase')
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Display the overall plot
plt.show()

# Display the fit parameters for both networks
print(f"Elastin: Fit to power law: Slope (exponent) = {-slope_1:.2f}")
print(f"Elastin: y = exp({intercept_1:.2f}) * x^{slope_1:.2f}")
print(f"Catalase: Fit to power law: Slope (exponent) = {-slope_2:.2f}")
print(f"Catalase: y = exp({intercept_2:.2f}) * x^{slope_2:.2f}")
