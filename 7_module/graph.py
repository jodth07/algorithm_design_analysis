class Node:
    def __init__(self, name, latitude=None, longitude=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.edges = []  # List of Edge objects

    def is_leaf(self):
        """Check if the node is a leaf (no outgoing edges)."""
        return len(self.edges) == 0

    def neighbors(self):
        if self.is_leaf():
            return []
        return [(edge.to_node.name, edge.weight) for edge in self.edges]

    def __repr__(self):
        return f"Node({self.name}, lat={self.latitude}, lon={self.longitude})"


class Edge:
    def __init__(self, from_node, to_node, base_weight):
        self.from_node = from_node
        self.to_node = to_node
        self.base_weight = base_weight
        self.weight = base_weight

    def __repr__(self):
        return f"Edge({self.from_node.name} -> {self.to_node.name}, {self.weight})"


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name, latitude=None, longitude=None):
        if name not in self.nodes:
            self.nodes[name] = Node(name, latitude, longitude)
        return self.nodes[name]

    def add_edge(
        self, from_name, to_name, base_weight, from_coords=None, to_coords=None
    ):
        """Add an edge, optionally adding coordinates for both nodes."""
        from_lat, from_lon = from_coords if from_coords else (None, None)
        to_lat, to_lon = to_coords if to_coords else (None, None)

        from_node = self.add_node(from_name, from_lat, from_lon)
        to_node = self.add_node(to_name, to_lat, to_lon)

        edge = Edge(from_node, to_node, base_weight)
        rev_edge = Edge(to_node, from_node, base_weight)
        from_node.edges.append(edge)
        to_node.edges.append(rev_edge)

    def get_node(self, name):
        return self.nodes.get(name)

    def get_all_edges(self):
        seen = set()
        edges = []
        for node in self.nodes.values():
            for edge in node.edges:
                key = tuple(sorted([edge.from_node.name, edge.to_node.name]))
                if key not in seen:
                    edges.append(edge)
                    seen.add(key)
        return edges

    def get_neighbors(self, node_name):
        node = self.get_node(node_name)
        return node.neighbors()
