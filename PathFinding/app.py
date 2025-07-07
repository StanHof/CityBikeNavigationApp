import shapely
from flask import Flask , request, jsonify
import osmnx as ox
from matplotlib import pyplot as plt
from flask_cors import CORS
from dijkstra import dijkstra, drawPath, flatten_path, find_full_path, geojson_linestring_from_path
from osmData import get_graph, fetch_nextbike_data

app = Flask(__name__)
CORS(app)
bike_graph = get_graph("Wroclaw , Poland", "Wroclaw" , "bike")
walk_graph = get_graph("Wroclaw , Poland", "Wroclaw" , "walk")
nextbike_station_data = fetch_nextbike_data(148)
Piekna = (51.08438311741168, 17.051030838427085)
Sepa = (51.11869783573391, 17.05239010407301)
culto = (51.10335007024191, 17.029353584572345)
@app.route("/navigate" , methods=['GET'])
def navigate():
    try:
        start_lat = request.args.get('start_lat' , type=float)
        start_lng = request.args.get('start_lng' , type=float)
        end_lat = request.args.get('end_lat' , type=float)
        end_lng = request.args.get('end_lng' , type=float)
        if None in [start_lat, end_lat, start_lng, end_lng]:
            return jsonify({'error': 'Invalid parameters none'}) , 400
        print([start_lat, start_lng, end_lat, end_lng])
    except (TypeError , ValueError):
        return jsonify({'error':'Invalid parameters Typeerro'}), 400
    try:
        orig_node = ox.distance.nearest_nodes(bike_graph,X=start_lat,Y=start_lng)
        dest_node = ox.distance.nearest_nodes(bike_graph, X=end_lat, Y=end_lng)

        orig_coords = (bike_graph.nodes[orig_node]['y'], bike_graph.nodes[orig_node]['x'])
        dest_coords = (bike_graph.nodes[dest_node]['y'], bike_graph.nodes[dest_node]['x'])

        dist_orig = ox.distance.great_circle(start_lng, start_lat, orig_coords[0] , orig_coords[1])
        dist_dest = ox.distance.great_circle(end_lng, end_lat, dest_coords[0] , dest_coords[1])

        if dist_orig > 500 or dist_dest > 500:
            return jsonify({'error': 'Path outside of bounds'}) , 400

        path_nodes, path_edges, distance , _ , _  = dijkstra(bike_graph , start_lat , start_lng , end_lat , end_lng)
       # drawPath(path_nodes , G)
        if path_nodes and distance != float('inf'):
            flattened_path = flatten_path(bike_graph , path_edges)
        else:
            return jsonify({'error': 'Path not found'}) , 400

        response_data = {
            "path_coords": flattened_path,
            "total_distance": distance,
        }
        response_data = {
      "type": "Feature",
      "properties": {"total_distance": distance},
      "geometry": {
        "coordinates":flattened_path,
        "type": "LineString"
      }


}
        return jsonify(response_data)

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}) , 500
@app.route("/full_navigate", methods=['GET'])
def full_navigate():
    try:
        start_lat = request.args.get('start_lat', type=float)
        start_lng = request.args.get('start_lng', type=float)
        end_lat = request.args.get('end_lat', type=float)
        end_lng = request.args.get('end_lng', type=float)
        print(start_lat, start_lng, end_lat, end_lng)
        if None in [start_lat, end_lat, start_lng, end_lng]:
            return jsonify({'error': 'Invalid parameters none'}) , 400
        if not nextbike_station_data:
            return jsonify({'error': 'Could not get nextbike data. Try again later'}) , 500
        if not bike_graph:
            return jsonify({'error': 'Could not get graph. Try again later'}) , 500
        if not walk_graph:
            return jsonify({'error': 'Could not get graph. Try again later'}) , 500
        full_paths = find_full_path(bike_graph , walk_graph, nextbike_station_data , start_lat , start_lng, end_lat, end_lng)
        print(full_paths)
        if not full_paths:
            return jsonify({'error': 'Could not find paths'}) , 400
        best_path = full_paths[0]
        print(best_path)
        response_data = {
            "start_station_name": best_path['start_station'],
            "end_station_name": best_path['end_station'],
            "walk_to_start_station_distance_m": best_path['walk_to_start_station']['distance'],
            "walk_from_end_station_distance_m": best_path['walk_from_end_station']['distance'],
            "bike_distance_m": best_path['bike_path']['distance'],
            "segments":
                {
                    "walk_to_start" : geojson_linestring_from_path(walk_graph , best_path['walk_to_start_station']['path_edges']),
                    "bike_path" : geojson_linestring_from_path(bike_graph , best_path['bike_path']['path_edges']),
                    "walk_to_end" : geojson_linestring_from_path(walk_graph , best_path['walk_from_end_station']['path_edges'])
                }
        }
        return jsonify(response_data)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}) , 500

if __name__ == "__main__":
    app.run(debug=True)

