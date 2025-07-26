from graph import Graph
from dijkstra import dijkstra
from traffic import apply_real_traffic_data

LOCATIONS = {
    "Warehouse": (26.1227, -80.1371),
    "A": (26.1222, -80.1431),
    "B": (26.1226, -80.1385),
    "C": (26.1250, -80.1300),
    "D": (26.1197, -80.1302),
    "Customer": (26.1137, -80.1393),
}

ROADS = [
    ("Warehouse", "A"),
    ("Warehouse", "B"),
    ("A", "C"),
    ("B", "C"),
    ("C", "D"),
    ("D", "Customer"),
    ("A", "Customer"),
    ("B", "Customer"),
]


def main():
    graph = Graph()

    # Add edges with dummy weights
    for from_loc, to_loc in ROADS:
        graph.add_edge(
            from_loc,
            to_loc,
            base_weight=1,
            from_coords=LOCATIONS[from_loc],
            to_coords=LOCATIONS[to_loc],
        )

    print("🚗 Getting real-time traffic data from TomTom...")
    apply_real_traffic_data(graph, LOCATIONS)

    cost, path = dijkstra(graph, "Warehouse", "Customer")

    print(f"\n📦 Best Route: {' -> '.join(path)}")
    print(f"⏱ ETA with traffic: {cost:.2f} minutes\n")


if __name__ == "__main__":
    main()
