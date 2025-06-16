import shapely
from flask import Flask , request, jsonify
import osmnx as ox
from matplotlib import pyplot as plt
from flask_cors import CORS
from dijkstra import dijkstra, drawPath, flatten_path
from osmData import get_graph

app = Flask(__name__)
CORS(app)
G = get_graph("Wroclaw , Poland" , "Wroclaw")
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
        orig_node = ox.distance.nearest_nodes(G,X=start_lat,Y=start_lng)
        dest_node = ox.distance.nearest_nodes(G, X=end_lat, Y=end_lng)

        orig_coords = (G.nodes[orig_node]['y'], G.nodes[orig_node]['x'])
        dest_coords = (G.nodes[dest_node]['y'], G.nodes[dest_node]['x'])

        dist_orig = ox.distance.great_circle(start_lng, start_lat, orig_coords[0] , orig_coords[1])
        dist_dest = ox.distance.great_circle(end_lng, end_lat, dest_coords[0] , dest_coords[1])

        if dist_orig > 500 or dist_dest > 500:
            return jsonify({'error': 'Path outside of bounds'}) , 400

        path_nodes, path_edges, distance , _ , _  = dijkstra(G , start_lat , start_lng , end_lat , end_lng)
       # drawPath(path_nodes , G)
        if path_nodes and distance != float('inf'):
            flattened_path = flatten_path(G , path_edges)
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

if __name__ == "__main__":
    app.run(debug=True)

