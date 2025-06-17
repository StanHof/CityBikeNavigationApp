import heapq
import json
import math

import osmnx as ox
import shapely
from flask import jsonify
from matplotlib import pyplot as plt
import requests

R_EARTH_KM = 6371

def dijkstra(graph, start_lat , start_lon ,end_lat , end_lon):

    start = ox.distance.nearest_nodes(graph, Y=start_lon, X=start_lat)
    end = ox.distance.nearest_nodes(graph, Y=end_lon, X=end_lat)

    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: (None , None) for node in graph.nodes}
    priority_queue = [(0, start)]
    i = 0
    while priority_queue:
        i += 1
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        if current_node == end:
            print("chuj")
            break
        for neighbor , edge_data in graph[current_node].items():
            for edge_id , attributes in edge_data.items():
                if "length" not in attributes:
                    continue
                distance = attributes["length"]
                new_distance = current_distance + distance

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = (current_node , edge_id)
                    heapq.heappush(priority_queue, (new_distance, neighbor))
    path_nodes = []
    path_edges = []
    current = end

    while current is not None:
        path_nodes.append(current)
        pred_info = predecessors[current]
        if pred_info is not None:
            prev_node , edge_id = pred_info
            path_edges.append((prev_node , current , edge_id))
            current = prev_node
        else:
            current = None
    #todo add multilple end points path searches
    path_edges.reverse()
    path_nodes.reverse()
    print(i)
    return path_nodes ,path_edges, distances[end] , distances , predecessors


def dijkstramultiend(graph, start_lat, start_lon, end_points): #latlng format
    """
    Returns list of path between start and end points using dijkstra's algorithm.

    param graph: MultiDirection Graph with edges
    param start_lat: Start latitude float
    param start_lon: Start longitude float
    param end_points: List end points that we want to find paths to (lat lng format float)
    return: returns an array of paths in [nodes, edges, distance] format
    """

    start = ox.distance.nearest_nodes(graph, Y=start_lat, X=start_lon)
    end_nodes = []
    for point in end_points:
        end_nodes.append( ox.distance.nearest_nodes(graph, Y=point[0], X=point[1]))
    end_nodes_copy = end_nodes
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: (None, None) for node in graph.nodes}
    priority_queue = [(0, start)]
    i = 0
    while priority_queue:
        i += 1
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        if current_node in end_points:
            end_points.remove(current_node)
            if not end_points:
                break

        for neighbor, edge_data in graph[current_node].items():
            for edge_id, attributes in edge_data.items():
                if "length" not in attributes:
                    continue
                distance = attributes["length"]
                new_distance = current_distance + distance

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = (current_node, edge_id)
                    heapq.heappush(priority_queue, (new_distance, neighbor))
    paths = []
    for point in end_nodes_copy:
        current = point
        path_nodes = []
        path_edges = []
        while current is not None:
            path_nodes.append(current)
            pred_info = predecessors[current]
            if pred_info is not None:
                prev_node, edge_id = pred_info
                path_edges.append((prev_node, current, edge_id))
                current = prev_node
            else:
                current = None
        # todo add multilple end points path searches
        path_edges.reverse()
        path_nodes.reverse()
        paths.append([path_nodes, path_edges])
    return paths


def drawPath(path , graph):
    path_x = [graph.nodes[node]['x'] for node in path]
    path_y = [graph.nodes[node]['y'] for node in path]

    min_x , min_y=min(path_x), min(path_y)
    max_x , max_y=max(path_x) , max(path_y)

    x_margin = (max_x - min_x) * 0.05
    y_margin = (max_y - min_y) * 0.05

    fig , ax = ox.plot_graph(graph, close=False, show=False, bgcolor='k' , edge_color='gray' , node_size=0 , edge_linewidth=0.5)
    ax.plot(path_x, path_y , color="cyan",linewidth=6,solid_capstyle="round",zorder=2)
    ax.scatter(graph.nodes[path[0]]['x'] , graph.nodes[path[0]]['y'] , color='red', s=50, marker='o', zorder=3)
    ax.scatter(graph.nodes[path[-1]]['x'], graph.nodes[path[-1]]['y'], color='red', s=50, marker='o', zorder=3)
    ax.set_xlim(min_x - x_margin , max_x + x_margin )
    ax.set_ylim(min_y - y_margin , max_y + y_margin )

    plt.show()


def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R_EARTH_KM * c
    return distance
def find_stations(user_lat , user_lng , bike_stations , n , radius_km = 0.5 ):

    """
    finds n closest stations in a radius of radius_km, filters out stations by a radius x radius bbox first

    :param user_lat: user latitude float

    :param user_lng: user longitude float
    :param bike_stations: array of bike stations from fetch_nextbike_data
    :param n: max amount of stations that the function will return
    :param radius_km: maximum distance in km between user latlng and bike stations
    :return:
    """
    KM_PER_DEGREE_LAT = 111.32
    KM_PER_DEGREE_LNG = 111.32 * math.cos(math.radians(user_lat)) #Calculating how many km for each lat/lng degree to define a bounding box
    stations_with_distances = []
    delta_lat_degree = radius_km / KM_PER_DEGREE_LAT
    delta_lng_degree = radius_km / KM_PER_DEGREE_LNG
    min_lat = user_lat - delta_lat_degree
    max_lat = user_lat + delta_lat_degree
    min_lng = user_lng - delta_lng_degree
    max_lng = user_lng + delta_lng_degree
    print(f"{min_lat}, {max_lat}")
    print(f"{min_lng}, {max_lng}")

    #Filtering stations to avoid calculating distance for every station
    filtered_stations = []
    for station in bike_stations:
        s_lat = station['lat']
        s_lng = station['lng']

        if min_lat < s_lat < max_lat and \
            min_lng < s_lng < max_lng:
            filtered_stations.append(station)
    #calculating Euclidean distance for each station in filtered stations
    for station in filtered_stations:
        station_lat = station['lat']
        station_lng = station['lng']

        delta_lat_km = (station_lat - user_lat) * KM_PER_DEGREE_LAT
        delta_lng_km = (station_lng - user_lng) * KM_PER_DEGREE_LNG
        distance_km = math.sqrt((delta_lat_km ** 2) + (delta_lng_km ** 2))

        if distance_km <= radius_km:
            station_copy = station.copy()
            station_copy['distance'] = distance_km
            stations_with_distances.append(station_copy)

    if len(stations_with_distances) < n:
        return stations_with_distances
    stations_with_distances.sort(key=lambda s: s['distance'])
    return stations_with_distances

def flatten_path(graph , path_edges):
    """
    flattens path to an array of coordinates
    :param graph: MultiDirection Graph with edges
    :param path_edges: List edges between start and end points
    :return: returns flattened path in list [lng , lat]
    """
    flattened_path = []
    path_edges.pop(0)
    for u , v ,key in path_edges:
        edge_data = graph.get_edge_data(u, v , key)

        if 'geometry' in edge_data and isinstance(edge_data['geometry'], shapely.geometry.LineString):
            for lon, lat in edge_data['geometry'].coords:
                flattened_path.append([lon , lat])
        else:
            node_u = graph.nodes[u]
            node_v = graph.nodes[v]
            if (flattened_path[-1] != node_u['x'], node_u['y']) or not flattened_path:
                flattened_path.append([node_u['x'] , node_u['y']])
            flattened_path.append([node_v['x'], node_v['y']])
    return flattened_path