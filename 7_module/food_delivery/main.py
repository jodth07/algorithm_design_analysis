import json
from core.delivery_graph import DeliveryGraph
from core.dijkstra import DijkstraAlgorithm
from core.node_with_address import NodeWithAddress
from core.location import Address, Coordinate
from visualize.map_generator import generate_map

from dotenv import load_dotenv
load_dotenv(verbose=True)

def main():
    # Load updated JSON
    with open("data/addresses_distributed.json") as f:
        data = json.load(f)

    graph = DeliveryGraph()

    # Create warehouse node
    warehouse_data = data["warehouse"]
    warehouse_address = Address(**warehouse_data["address"])
    warehouse_coord = Coordinate(warehouse_data["lat"], warehouse_data["lon"])
    warehouse_node = NodeWithAddress(warehouse_data["name"], warehouse_address, warehouse_coord)
    graph.add_node(warehouse_node)

    # Create delivery nodes
    delivery_nodes = {}
    for d in data["deliveries"]:
        addr = Address(**d["address"])
        coord = Coordinate(d["lat"], d["lon"])
        node = NodeWithAddress(d["name"], addr, coord)
        delivery_nodes[node.name] = node
        graph.add_node(node)

        # Add edges (undirected)
        graph.add_edge(warehouse_node, node)

    # Print all edges
    print("\n📦 All Edges:")
    for edge in graph.get_all_edges():
        print(f"{edge.u_node.name} -> {edge.v_node.name} | weight: {edge.weight}")


    # All nodes (including warehouse and deliveries)
    all_nodes = [warehouse_node] + list(delivery_nodes.values())
    edges = graph.get_all_edges()

    generate_map(all_nodes, edges, "deliveries_map.html")

    # Run Dijkstra to each customer
    algorithm = DijkstraAlgorithm()
    for name, node in delivery_nodes.items():
        cost, path = graph.run_algorithm(algorithm, warehouse_node.name, name)
        print(f"\nDelivery to {name}:")
        print(f"Path: {' -> '.join(path)}")
        print(f"ETA: {cost:.2f} units")

if __name__ == "__main__":
    main()
