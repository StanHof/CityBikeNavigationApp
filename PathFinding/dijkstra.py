import heapq

import osmnx as ox


def dijkstra(graph, start_lat , start_lon ,end_lat , end_lon):

    start = ox.distance.nearest_nodes(graph, Y=start_lat, X=start_lon)
    end = ox.distance.nearest_nodes(graph, Y=end_lat, X=end_lon)

    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: None for node in graph.nodes}
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
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))
    path = []
    current = end

    while current is not None:
        path.append(current)

        current = predecessors[current]

    path.reverse()
    return path , distances[end] , distances , predecessors


