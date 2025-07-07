import heapq
import json
import math

import osmnx as ox
import shapely
from flask import jsonify
from matplotlib import pyplot as plt
import requests
from shapely.geometry import linestring

R_EARTH_KM = 6371
BIKE_SPEED = 3.5
WALK_SPEED = 1.3
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


def dijkstramultiend(graph, start_lat, start_lon, end_points_dict):  # Now accepts a dictionary
    """
    Returns a dictionary of paths from a single start point to multiple end points,
    with names as keys, using Dijkstra's algorithm.

    param graph: MultiDirection Graph with edges (e.g., from osmnx).
    param start_lat: Start latitude (float).
    param start_lon: Start longitude (float).
    param end_points_dict: A dictionary where keys are desired path names (str) and has a {'lat': float, 'lng': float}.
    return: A dictionary {path_name: {'path_nodes': list, 'path_edges': list, 'distance': float}}
            Includes paths only for reachable end points.
    """

    start_node = ox.distance.nearest_nodes(graph, Y=start_lat, X=start_lon)

    # Map end node IDs back to their original names and coordinates
    target_nodes_map = {}  # {node_id: {'name': 'Name', 'coords': (lat, lng)}}
    for name, coords in end_points_dict.items():
        node_id = ox.distance.nearest_nodes(graph, Y=coords['lat'], X=coords['lng'])
        target_nodes_map[node_id] = {'name': name, 'coords': coords}

    remaining_target_nodes = set(target_nodes_map.keys())

    distances = {node: float('infinity') for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {node: (None, None) for node in graph.nodes}  # Stores (predecessor_node, edge_key)
    priority_queue = [(0, start_node)]

    while priority_queue and remaining_target_nodes:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue


        if current_node in remaining_target_nodes:
            remaining_target_nodes.remove(current_node)
            if not remaining_target_nodes:  # If all paths are found end early
                break

        for neighbor, edge_keys_and_data in graph[current_node].items():
            for edge_key, attributes in edge_keys_and_data.items():
                if "length" not in attributes:
                    continue

                distance = attributes["length"]
                new_distance = current_distance + distance

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = (current_node, edge_key)  # Store (u, v, key)
                    heapq.heappush(priority_queue, (new_distance, neighbor))

    paths_output = {}
    # Iterate through the target_nodes_map to reconstruct paths for all requested end points
    for target_node_id, target_info in target_nodes_map.items():
        path_name = target_info['name']
        original_coords = target_info['coords']

        if distances[target_node_id] == float('infinity'):
            paths_output[path_name] = {'path_nodes': [], 'path_edges': [], 'distance': float('infinity')}
            continue

        current = target_node_id
        path_nodes = []
        path_edges = []


        while current is not None:
            path_nodes.append(current)
            pred_info = predecessors[current]
            if pred_info[0] is not None:
                prev_node, edge_id = pred_info
                path_edges.append((prev_node, current, edge_id))
                current = prev_node
            else:
                current = None
        path_edges.reverse()
        path_nodes.reverse()

        paths_output[path_name] = {
            'path_nodes': path_nodes,
            'path_edges': path_edges,
            'distance': distances[target_node_id]
        }
    return paths_output


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
def find_stations(user_lat , user_lng , bike_stations , n , radius_km = 0.5  , include_bikes = False):

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

    #Filtering stations to avoid calculating distance for every station and to exclude bikes that aren't parked in a station
    filtered_stations = []
    for station in bike_stations:
        if not include_bikes and station['bike']:
            continue
        s_lat = station['lat']
        s_lng = station['lng']

        if min_lat < s_lat < max_lat and \
            min_lng < s_lng < max_lng :



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

    result = {}
    stations_with_distances.sort(key=lambda s: s['distance'])
    stations_with_distances =  stations_with_distances[:n]
    for station in stations_with_distances:
        result[station['name']] = {'lat':station['lat'] , 'lng': station['lng']}
    return result

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
def geojson_linestring_from_path(graph , path_edges):
    coordinates = []
    if not path_edges:
        return {"type": linestring, "coordinates": coordinates}
    first_edge_u = path_edges[0][0]
    first_edge_v = path_edges[0][1]
    first_edge_data = graph.get_edge_data(first_edge_u, first_edge_v, path_edges[0][2])
    print(first_edge_data)
    if 'geometry' in first_edge_data and isinstance(first_edge_data['geometry'], shapely.geometry.LineString):
        for lng , lat in first_edge_data['geometry'].coords:
            coordinates.append([lng, lat])
    else:
        coordinates.append([graph.nodes[first_edge_u]['x'], graph.nodes[first_edge_u]['y']])

    for i , (u , v , key) in enumerate(path_edges):
        edge_data = graph.get_edge_data(u, v, key)
        if 'geometry' in edge_data and isinstance(edge_data['geometry'], shapely.geometry.LineString):
            for lng , lat in edge_data['geometry'].coords:
                if not coordinates or coordinates[-1] != [lat, lng]:
                    coordinates.append([lng, lat])
        else:
            v_node = graph.nodes[v]
            coordinates.append([v_node['x'] , v_node['y']])
    return {
        "type": "Feature",
        "geometry": {
            "coordinates": coordinates,
            "type": "LineString"
        }
    }


def find_full_path(bike_graph , walk_graph , bike_stations , start_lat , start_lng , end_lat , end_lng):

    """
    finds best path for citybikes between start_lat start_lng and end_lat end_lng,
    Looks for 3 stations near end and start, calculates walking distance to each station then
    finds bike paths between each combination of stations and sums up the total distance for each combination (walk to station + bike + walk from station)

    :param bike_graph: MultiDirection Graph with edges (bike network osmnx graph)
    :param walk_graph: MultiDirection Graph with edges (walk network osmnx graph)
    :param bike_stations: Nextbike api response (fetch_nextbike_data)
    :param start_lat: starting latitude float
    :param start_lng: starting longitude float
    :param end_lat: ending latitude float
    :param end_lng: ending longitude float
    :return: list of best paths from each station near starting point
    [{
            'start_station' : name of start station string,
            'end_station' : name of end station string,
            'total_distance_time' : sum of all distances in seconds,
            'walk_to_start_station': path from dijkstramultiend {path_name: {'path_nodes': list, 'path_edges': list, 'distance': float}}
            'bike_path': value['bike_path'],
            'walk_to_end_station': walk_paths_end[value['end_station']],
        }]
    """
    #find closest stations to start and finish
    start_stations = find_stations(start_lat, start_lng, bike_stations, 3, 0.5 , True)
    end_stations = find_stations(end_lat, end_lng, bike_stations, 3, 0.5)
    print(start_stations)
    print(end_stations)
    #calculate paths from start point to start stations and end point to end stations
    walk_paths_start = dijkstramultiend(walk_graph, start_lat, start_lng, start_stations)
    walk_paths_end =  dijkstramultiend(walk_graph, end_lat, end_lng, end_stations)
    #save station in dict {station_name: {'lat': <latitude of station> ,'lng' <longitude of station> , 'total_distance_time' , <time to walk to station>}
    for station in walk_paths_start.keys():
        start_stations.update({station: {'lat' : start_stations[station]['lat'],
                                         'lng' : start_stations[station]['lng'],
                                         'total_distance_time' : walk_paths_start[station]["distance"] / WALK_SPEED}})
    for station in walk_paths_end.keys():
        end_stations.update({station: {'lat' : end_stations[station]['lat'],
                                       'lng' : end_stations[station]['lng'],
                                       'total_distance_time' : walk_paths_end[station]["distance"] / WALK_SPEED}})
    for start_station in start_stations.values():
        #find path from current starting station to each end station
        paths_to_end_stations = dijkstramultiend(bike_graph,
                                                 start_station['lat'],
                                                 start_station['lng'], end_stations)
        best_station = ""
        best_distance = float('inf')
        best_path = None
        #find the best combination of stations based on sum of walking distances to stations and biking distance
        for key , value in paths_to_end_stations.items():
            distance = end_stations[key]['total_distance_time'] + start_station['total_distance_time'] + value['distance'] / BIKE_SPEED
            if distance < best_distance:
                best_station = key
                best_distance = distance
                best_path = value
        start_station['total_distance_time'] = best_distance
        start_station['end_station'] = best_station
        start_station['bike_path'] = best_path
    result = []
    print(walk_paths_end)
    for key , value in start_stations.items():
        if value['end_station'] == '' or key == '':
            continue
        result.append({
            'start_station' : key,
            'end_station' : value['end_station'],
            'total_distance_time' : value['total_distance_time'],
            'walk_to_start_station': walk_paths_start[key],
            'bike_path': value['bike_path'],
            'walk_from_end_station': walk_paths_end[value['end_station']],
        })
    result.sort(key = lambda x : x['total_distance_time'])
    return result

