import osmnx as ox
import networkx as nx
import os
from flask import jsonify
import json
import requests
from osmnx.distance import add_edge_lengths


def get_graph(place_name = "Wroclaw , Poland" , city_name = "Wroclaw" , network_type = "bike"):
    if os.path.exists(f'data/{city_name}_{network_type}_graph.graphml'):
        G = ox.load_graphml(f'data/{city_name}_{network_type}_graph.graphml')

    else:
        print("graph not found , loading")
        G = ox.graph_from_place(place_name , network_type = network_type)
        add_edge_lengths(G)
        ox.save_graphml(G,f'data/{city_name}_{network_type}_graph.graphml')

    return G

def fetch_nextbike_data(city_id):
    try:
        response = requests.get(f"https://api.nextbike.net/maps/nextbike-live.json?city={city_id}")
        response.raise_for_status()
        data = response.json()["countries"][0]["cities"][0]["places"]
        return data
    except requests.exceptions.RequestException as e:
        print(f"Nextbike api fetch error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSONdecoding error: {e}")
        return None

