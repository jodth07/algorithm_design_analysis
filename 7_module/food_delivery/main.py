import json
import random
from core.delivery_graph import DeliveryGraph
from core.dijkstra import DijkstraAlgorithm
from core.node_with_address import NodeWithAddress
from core.location import Address, Coordinate
from visualize.map_generator import generate_map

from dotenv import load_dotenv
load_dotenv(verbose=True)


def main():
    # Load data
    with open("data/addresses_distributed.json") as f:
        data = json.load(f)

    graph = DeliveryGraph()

    # Create warehouse
    warehouse_data = data["warehouse"]
    warehouse_address = Address(**warehouse_data["address"])
    warehouse_coord = Coordinate(warehouse_data["lat"], warehouse_data["lon"])
    warehouse_node = NodeWithAddress(warehouse_data["name"], warehouse_address, warehouse_coord)
    graph.add_node(warehouse_node)

    # Build delivery nodes and group them
    all_nodes = []
    for d in data["deliveries"]:
        addr = Address(**d["address"])
        coord = Coordinate(d["lat"], d["lon"])
        node = NodeWithAddress(d["name"], addr, coord)
        all_nodes.append(node)
        graph.add_node(node)

    # Split into 5 groups
    groups = [all_nodes[i::5] for i in range(5)]

    # Connect Group 0 to warehouse
    for node in groups[0]:
        graph.add_edge(warehouse_node, node)

    # Connect each group[i] to random nodes in group[i-1]
    for i in range(1, 5):
        for node in groups[i]:
            parent = random.choice(groups[i - 1])
            graph.add_edge(parent, node)

    # Show all edges
    print("\n📦 All Edges:")
    for edge in graph.get_all_edges():
        print(f"{edge.u_node.name} -> {edge.v_node.name} | weight: {edge.weight:.2f}")

    # Run Dijkstra for each node and select one with depth ≥ 2
    algorithm = DijkstraAlgorithm()
    eligible_paths = []
    for target in groups[4]:
        cost, path = graph.run_algorithm(algorithm, warehouse_node.name, target.name)
        if len(path) >= 3:
            eligible_paths.append((target.name, cost, path))

    if not eligible_paths:
        print("❌ No eligible delivery paths of depth ≥ 2 found.")
        return

    # Pick a random valid path
    target_name, total_eta, selected_path = eligible_paths[0]

    print(f"\n🚚 Selected Delivery Path to: {target_name}")
    print(" → ".join(selected_path))
    print(f"ETA: {total_eta:.2f} minutes")

    # Prepare nodes for map
    # path_nodes = [graph.get_node(name) for name in selected_path]
    # generate_map_with_edges(path_nodes, "deliveries_map.html")

    # Example: pick a single destination (e.g., Customer 1)
    # last_customer = list(delivery_nodes.values())[-1]
    # cost, path = graph.run_algorithm(algorithm, warehouse_node.name, last_customer.name)

    generate_map(graph, path=selected_path, output_path="deliveries_map.html")
    print("\n🗺️ Map saved to deliveries_map.html")


if __name__ == "__main__":
    main()
