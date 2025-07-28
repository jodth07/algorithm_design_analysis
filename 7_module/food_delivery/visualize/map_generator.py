import folium

def generate_map_with_edges(path_nodes, output_path: str):
    fmap = folium.Map(location=[path_nodes[0].coords.lat, path_nodes[0].coords.lon], zoom_start=11)

    for node in path_nodes:
        folium.Marker(
            location=[node.coords.lat, node.coords.lon],
            tooltip=node.name
        ).add_to(fmap)

    for i in range(len(path_nodes) - 1):
        u, v = path_nodes[i], path_nodes[i + 1]
        tooltip_text = f"Approx. distance: {((u.coords.lat - v.coords.lat)**2 + (u.coords.lon - v.coords.lon)**2) ** 0.5:.4f}"
        folium.PolyLine(
            locations=[[u.coords.lat, u.coords.lon], [v.coords.lat, v.coords.lon]],
            tooltip=tooltip_text,
            color="blue",
            weight=4
        ).add_to(fmap)

    fmap.save(output_path)

import folium
from folium import plugins
from core.node_base import Node
from core.edge_base import Edge


def generate_map(graph, path=None, output_path="deliveries_map.html"):
    fmap = folium.Map(location=[26.1224, -80.1373], zoom_start=13)

    # Plot all edges in yellow
    for edge in graph.get_all_edges():
        coords = [
            [edge.u_node.coords.lat, edge.u_node.coords.lon],
            [edge.v_node.coords.lat, edge.v_node.coords.lon]
        ]
        folium.PolyLine(
            coords,
            color="yellow",
            weight=2.5,
            opacity=0.7
        ).add_to(fmap)

    # Plot all nodes in blue
    for node in graph.nodes.values():
        folium.Marker(
            [node.coords.lat, node.coords.lon],
            tooltip=node.name,
            icon=folium.Icon(color="blue", icon="cutlery", prefix="fa")
        ).add_to(fmap)

    # Highlight final path (destination and segments)
    if path and len(path) > 1:
        # Green marker for final destination
        end_node = graph.get_node(path[-1])
        folium.Marker(
            [end_node.coords.lat, end_node.coords.lon],
            tooltip=f"Destination: {end_node.name}",
            icon=folium.Icon(color="red", icon="flag", prefix="fa")
        ).add_to(fmap)

        # Yellow polylines (re-plot to ensure top layer)
        for i in range(len(path) - 1):
            u = graph.get_node(path[i])
            v = graph.get_node(path[i + 1])
            coords = [
                [u.coords.lat, u.coords.lon],
                [v.coords.lat, v.coords.lon]
            ]
            folium.PolyLine(
                coords,
                color="green",
                weight=4,
                opacity=1
            ).add_to(fmap)

    fmap.save(output_path)
