from abc import ABC, abstractmethod
import heapq


class RoutingAlgorithm(ABC):
    @abstractmethod
    def run(self, graph, start_name, end_name):
        pass


class DijkstraAlgorithm(RoutingAlgorithm):
    def run(self, graph, start_name, end_name):
        distances = {node.name: float("inf") for node in graph.nodes.values()}
        previous = {node.name: None for node in graph.nodes.values()}
        distances[start_name] = 0

        queue = [(0, start_name)]
        print(f"Queue is initialized with: {queue}")

        while queue:
            current_dist, current_node = heapq.heappop(queue)

            all_neighbors = graph.get_neighbors(current_node)
            print(f"{current_node} has {len(all_neighbors)} neighbors")

            for neighbor_name, travel_time in graph.get_neighbors(current_node):
                new_dist = current_dist + travel_time
                print(
                    f"Checking neighbor {neighbor_name} with travel time {travel_time} from {current_node}. Current distance: {current_dist}, New distance: {new_dist}"
                )
                if new_dist < distances[neighbor_name]:
                    distances[neighbor_name] = new_dist
                    previous[neighbor_name] = current_node
                    heapq.heappush(queue, (new_dist, neighbor_name))

        # Reconstruct path
        path = []
        node = end_name
        while node:
            path.insert(0, node)
            node = previous[node]

        print(f"The shortest path from {start_name} to {end_name} is {path}")
        print(
            f"The distances path from {start_name} to {end_name} is {distances[end_name]}"
        )

        return distances[end_name], path
