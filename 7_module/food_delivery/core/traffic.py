import random
import os
import json
import requests

from dotenv import load_dotenv

load_dotenv(verbose=True)

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
print(TOMTOM_API_KEY)


def simulate_traffic(graph):
    for edge in graph.get_all_edges():
        traffic_factor = random.uniform(0.7, 2.0)
        edge.weight = round(edge.base_weight * traffic_factor, 2)


def get_travel_time_tomtom(from_coords, dest_coords, reload=False):
    cache_file = "data/tomtom_travel_times.json"
    key_from = f"{from_coords.lat}_{from_coords.lon}"
    key_to = f"{dest_coords.lat}_{dest_coords.lon}"

    # Load cache
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    # Check cache
    if not reload and key_from in cache and key_to in cache[key_from]:
        return cache[key_from][key_to]

    # Fetch from API
    url = (
        f"https://api.tomtom.com/routing/1/calculateRoute/"
        f"{from_coords.lat},{from_coords.lon}:{dest_coords.lat},{dest_coords.lon}/json"
        f"?traffic=true&travelMode=car&key={TOMTOM_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "routes" not in data:
        print("TomTom API error:", data.get("error", data))
        raise Exception("Error fetching travel time")

    summary = data["routes"][0]["summary"]
    travel_time_sec = summary["travelTimeInSeconds"]
    travel_time = round(travel_time_sec / 60, 2)

    # Update cache
    if key_from not in cache:
        cache[key_from] = {}
    cache[key_from][key_to] = travel_time

    with open(cache_file, "w") as f:
        json.dump(cache, f)

    return travel_time


def apply_real_traffic_data(graph, coord_map):
    for edge in graph.get_all_edges():
        from_coords = coord_map[edge.from_node.name]
        to_coords = coord_map[edge.to_node.name]
        travel_time = get_travel_time_tomtom(from_coords, to_coords)
        edge.weight = travel_time
