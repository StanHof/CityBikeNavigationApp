import networkx as nx

from dijkstra import dijkstra, drawPath, flatten_path, dijkstramultiend, find_stations
from osmData import get_graph , fetch_nextbike_data

if __name__ == '__main__':
##   bike_graph = get_graph("Wroclaw , Poland", "Wroclaw" , "bike")
##   walk_graph = get_graph("Wroclaw , Poland", "Wroclaw" , "walk")
##   destinations = [[51.1167970437751, 17.051813373787155],[51.11995684091037, 17.05625795237023]]
##   paths = dijkstramultiend(bike_graph, 51.08504095037575, 17.049182766084556, destinations)
##   drawPath(paths[0][0], bike_graph)
##   drawPath(paths[1][0], bike_graph)

    stations = fetch_nextbike_data(148)

    print((find_stations(51.084207573294925, 17.04947732183435 , stations , 3 , 0.5)))
