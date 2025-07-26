from abc import ABC, abstractmethod
import heapq

class RoutingAlgorithm(ABC):
    @abstractmethod
    def run(self, graph, start_name, end_name):
        pass


class DijkstraAlgorithm(RoutingAlgorithm):
    def run(self, graph, start_name, end_name):
        distances = {node.get_name(): float("inf") for node in graph.nodes.values()}
        previous = {node.get_name(): None for node in graph.nodes.values()}
        distances[start_name] = 0

        queue = [(0, start_name)]

        while queue:
            current_dist, current_node = heapq.heappop(queue)

            for neighbor_name, travel_time in graph.get_neighbors(current_node):
                new_dist = current_dist + travel_time
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

        return distances[end_name], path
