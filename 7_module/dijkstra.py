import heapq


def dijkstra(graph, start_name, end_name):
    distances = {node.name: float("inf") for node in graph.nodes.values()}
    previous = {node.name: None for node in graph.nodes.values()}
    distances[start_name] = 0

    queue = [(0, start_name)]

    while queue:
        current_distance, current_name = heapq.heappop(queue)

        if current_distance > distances[current_name]:
            continue

        for neighbor_name, travel_time in graph.get_neighbors(current_name):
            new_distance = current_distance + travel_time
            if new_distance < distances[neighbor_name]:
                distances[neighbor_name] = new_distance
                previous[neighbor_name] = current_name
                heapq.heappush(queue, (new_distance, neighbor_name))

    # Reconstruct path
    path = []
    node = end_name
    while node:
        path.insert(0, node)
        node = previous[node]

    return distances[end_name], path
