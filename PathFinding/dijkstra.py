import heapq

import osmnx as ox
import shapely
from flask import jsonify
from matplotlib import pyplot as plt


def dijkstra(graph, start_lat , start_lon ,end_lat , end_lon):

    start = ox.distance.nearest_nodes(graph, Y=start_lon, X=start_lat)
    end = ox.distance.nearest_nodes(graph, Y=end_lon, X=end_lat)

    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: (None , None) for node in graph.nodes}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        if current_node == end:
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

    path_edges.reverse()
    path_nodes.reverse()
    return path_nodes ,path_edges, distances[end] , distances , predecessors


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
    #ax.set_xlim(min_x - x_margin , max_x + x_margin )
   # ax.set_ylim(min_y - y_margin , max_y + y_margin )

    plt.show()


def flatten_path(graph , path_edges):
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