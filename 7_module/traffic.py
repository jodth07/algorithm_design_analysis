import random
import os
import requests

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY", "OwbhpxYl78cxB2yOxt6WKaTERtTGlWRt")


def simulate_traffic(graph):
    for edge in graph.get_all_edges():
        traffic_factor = random.uniform(0.7, 2.0)
        edge.weight = round(edge.base_weight * traffic_factor, 2)


def get_travel_time_tomtom(origin_coords, destination_coords):
    from_lat, from_lon = origin_coords
    to_lat, to_lon = destination_coords

    url = (
        f"https://api.tomtom.com/routing/1/calculateRoute/"
        f"{from_lat},{from_lon}:{to_lat},{to_lon}/json"
        f"?traffic=true&travelMode=car&key={TOMTOM_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "routes" not in data:
        raise Exception(f"TomTom API error: {data}")

    summary = data["routes"][0]["summary"]
    travel_time_sec = summary["travelTimeInSeconds"]
    return round(travel_time_sec / 60, 2)  # minutes


def apply_real_traffic_data(graph, coord_map):
    for edge in graph.get_all_edges():
        from_coords = coord_map[edge.from_node.name]
        to_coords = coord_map[edge.to_node.name]
        travel_time = get_travel_time_tomtom(from_coords, to_coords)
        edge.weight = travel_time
