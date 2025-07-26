from base_graph import DeliveryGraph
from dijkstra import DijkstraAlgorithm
from traffic import apply_real_traffic_data

LOCATIONS = {
    "Warehouse": (26.1227, -80.1371),
    "A": (26.1222, -80.1431),
    "B": (26.1226, -80.1385),
    "C": (26.1250, -80.1300),
    "D": (26.1197, -80.1302),
    "Customer1": (26.1137, -80.1393),
    "Customer2": (26.1100, -80.1450),
    "Customer3": (26.1177, -80.1401),
    "Customer4": (26.1161, -80.1355),
    "Customer5": (26.1150, -80.1330),
    "Customer6": (26.1145, -80.1320),
    "Customer7": (26.1130, -80.1310),
    "Customer8": (26.1120, -80.1300),
    "Customer9": (26.1110, -80.1290),
    "Customer10": (26.1100, -80.1280),
}

ROADS = [
    ("Warehouse", "A"),
    ("Warehouse", "B"),
    ("A", "C"),
    ("B", "C"),
    ("C", "D"),
    ("D", "Customer1"),
    ("A", "Customer2"),
    ("B", "Customer3"),
    ("B", "Customer4"),
    ("C", "Customer5"),
    ("C", "Customer6"),
    ("D", "Customer7"),
    ("D", "Customer8"),
    ("A", "Customer9"),
    ("B", "Customer10"),
]

def main():
    graph = DeliveryGraph()

    for from_node, to_node in ROADS:
        graph.add_edge(
            from_node,
            to_node,
            base_weight=1,
            from_coords=LOCATIONS[from_node],
            to_coords=LOCATIONS[to_node],
        )

    print("🚦 Applying traffic weights from TomTom...")
    apply_real_traffic_data(graph, LOCATIONS)

    dijkstra = DijkstraAlgorithm()

    for i in range(1, 11):
        target = f"Customer{i}"
        cost, path = graph.run_algorithm(dijkstra, "Warehouse", target)
        print(f"🛵 Delivery {i}: {' -> '.join(path)} | ETA: {cost:.2f} min")

if __name__ == "__main__":
    main()
