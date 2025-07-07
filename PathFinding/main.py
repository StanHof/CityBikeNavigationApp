import networkx as nx

from dijkstra import dijkstra, drawPath, flatten_path, dijkstramultiend, find_stations, find_full_path, \
    geojson_linestring_from_path
from osmData import get_graph , fetch_nextbike_data

if __name__ == '__main__':
    bike_graph = get_graph("Wroclaw , Poland", "Wroclaw" , "bike")
    walk_graph = get_graph("Wroclaw , Poland", "Wroclaw" , "walk")
    stations = fetch_nextbike_data(148)
    Piekna = (51.08438311741168, 17.051030838427085)
    Sepa  = (51.11869783573391, 17.05239010407301)
    culto = (51.10335007024191, 17.029353584572345)

    paths = find_full_path(bike_graph , walk_graph, stations , Piekna[0] , Piekna[1], Sepa[0], Sepa[1])
    print(paths[0])

    print(geojson_linestring_from_path(bike_graph, paths[0]['bike_path']['path_edges']))