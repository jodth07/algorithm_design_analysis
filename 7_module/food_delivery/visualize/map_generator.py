import folium
from core.edge_with_traffic import EdgeWithTraffic


def generate_map(delivery_points: list, edges: list, output_path: str):
    fmap = folium.Map(location=[26.1224, -80.1373], zoom_start=13)

    # Add all delivery markers
    for point in delivery_points:
        folium.Marker(
            location=[point.coords.lat, point.coords.lon],
            tooltip=point.name,
            icon=folium.Icon(color="blue" if point.name != "Warehouse" else "green"),
        ).add_to(fmap)

    # Draw edges (paths between nodes)
    for edge in edges:
        coords = [
            [edge.u_node.coords.lat, edge.u_node.coords.lon],
            [edge.v_node.coords.lat, edge.v_node.coords.lon],
        ]
        folium.PolyLine(
            coords,
            color="gray",
            weight=2.5,
            opacity=0.8,
            tooltip=f"{edge.u_node.name} -> {edge.v_node.name} ({edge.weight:.2f} min)",
        ).add_to(fmap)

    fmap.save(output_path)
