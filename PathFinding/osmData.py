import osmnx as ox
import networkx as nx
import os

from osmnx.distance import add_edge_lengths


def get_graph(place_name = "Wroclaw , Poland" , city_name = "Wroclaw"):
    if os.path.exists(f'data/{city_name}_bike_graph.graphml'):
        G = ox.load_graphml(f'data/{city_name}_bike_graph.graphml')

    else:
        print("graph not found , loading")
        G = ox.graph_from_place(place_name , network_type = "bike")
        add_edge_lengths(G)
        ox.save_graphml(G,f'data/{city_name}_bike_graph.graphml')

    return G