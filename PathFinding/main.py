import networkx as nx

from dijkstra import dijkstra, drawPath, flatten_path
from osmData import get_graph

if __name__ == '__main__':
    G = get_graph("Wroclaw , Poland" , "Wroclaw")
    path_nodes , path_edges , _ , _ , _ = dijkstra(G , 17.05135677397479, 51.08435837981736 , 17.052404990026247, 51.11801761202622)
    #drawPath(path_nodes, G)
    print(len(path_edges))
    flatten_path(G, path_edges)