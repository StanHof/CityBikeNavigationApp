from flask import Flask
import osmnx as ox
from matplotlib import pyplot as plt

from dijkstra import dijkstra
from osmData import get_graph

if __name__ == '__main__':
   # app.run()
    G = get_graph("Wroclaw , Poland" , 'Wroclaw')
    start_lat , start_lon = 51.1090, 17.0310
    end_lat , end_lon = 51.1150, 17.0450
    orig_node = ox.distance.nearest_nodes(G, Y=start_lat, X=start_lon)
    dest_node = ox.distance.nearest_nodes(G, Y=end_lat, X=end_lon)
    print("finding path")
    path_nodes , total_distances , distances , predecessors = dijkstra(G , start_lat, start_lon , end_lat , end_lon)
    print(path_nodes)

