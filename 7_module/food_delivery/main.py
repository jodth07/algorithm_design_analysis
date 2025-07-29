import json
from core.delivery_graph import DeliveryGraph
from core.dijkstra import DijkstraAlgorithm
from core.node_with_address import NodeWithAddress
from core.location import Address, Coordinate
from visualize.map_generator import generate_map

def main():
    # Load grouped graph structure
    with open("data/graph_with_grouped_edges.json") as f:
        data = json.load(f)

    graph = DeliveryGraph()

    # Create warehouse node
    wh_data = data["warehouse"]
    wh_address = Address(**wh_data["address"])
    wh_coord = Coordinate(wh_data["lat"], wh_data["lon"])
    warehouse_node = NodeWithAddress("Warehouse", wh_address, wh_coord)
    graph.add_node(warehouse_node)

    # Create all delivery nodes
    node_map = {"Warehouse": warehouse_node}
    for node_data in data["nodes"]:
        addr = Address(**node_data["address"])
        coord = Coordinate(node_data["lat"], node_data["lon"])
        node = NodeWithAddress(node_data["name"], addr, coord)
        graph.add_node(node)
        node_map[node.name] = node

    # Add only allowed edges
    for edge in data["edges"]:
        u = node_map[edge["from"]]
        v = node_map[edge["to"]]
        graph.add_edge(u, v)

    # Print all edges
    print("\n📦 All Edges:")
    for edge in graph.get_all_edges():
        print(f"{edge.u_node.name} -> {edge.v_node.name} | weight: {edge.weight:.2f}")

    # Choose a destination (last node in list)
    last_dest_name = data["nodes"][-1]["name"]
    algorithm = DijkstraAlgorithm()
    cost, path = graph.run_algorithm(algorithm, "Warehouse", last_dest_name)

    print(f"\n🚚 Delivery to {last_dest_name}:")
    print(f"Path: {' -> '.join(path)}")
    print(f"ETA: {cost:.2f} minutes")

    # Optional: generate map with highlighted path
    generate_map(graph, path, output_path="deliveries_map.html")
    print("🗺️ Map saved to 'deliveries_map.html'.")

if __name__ == "__main__":
    main()
