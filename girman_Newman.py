import networkx as nx
from networkx.algorithms.community import girvan_newman
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

start_time = time.time()


# Creating a graph with approximately 1000 edges
G = nx.gnm_random_graph(n=100, m=2000)  # 50 nodes and approximately 1000 edges


# Apply Girvan-Newman algorithm 
communities = girvan_newman(G)
partition = tuple(sorted(c) for c in next(communities))

# Visualize 
partitioned_graph = nx.Graph()
partitioned_graph.add_nodes_from(G.nodes, partition=[[i] for i, nodes in enumerate(partition) for _ in nodes])
partitioned_graph.add_edges_from(G.edges)


pos = nx.spring_layout(partitioned_graph)

fig, ax = plt.subplots()


# Draw the graph
nx.draw(partitioned_graph, pos, with_labels=True, font_weight='bold', node_size=800, ax=ax)


graph_title = "Partitioned Graph (Girvan-Newman Algorithm)"
plt.title(graph_title, fontsize=14, y=1.05)  # Adjust the 'y' value to position the title


button_text = 'Efficiency'
button_ax = plt.axes([0.7, 0.01, 0.2, 0.05])  # [left, bottom, width, height]
button = Button(button_ax, button_text, color='#D8D252', hovercolor='#D86A52')


def on_button_click(event):
    button.label.set_text('O(m^2n)')



button.on_clicked(on_button_click)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

plt.tight_layout() 
plt.show()
