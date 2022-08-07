import networkx as nx
import matplotlib.pyplot as plt
import track_addresses_top_10 as track
import get_scam_eth_addresses_in_blacklist

MINLEN = 5

addresses = get_scam_eth_addresses_in_blacklist.get_addresses()

graph = track.get_transactions(addresses[0])
for _ in range(len(addresses)):
    if _ == 0:
        continue
    else:
        graph += track.get_transactions(addresses[_])

G = nx.DiGraph()
G.add_edges_from(graph, minlen=MINLEN)
plt.tight_layout()
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=100)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black')
nx.draw_networkx_labels(G, pos)
nx.draw(G, pos)

plt.show()
