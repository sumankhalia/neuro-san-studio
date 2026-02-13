import networkx as nx
from pyvis.network import Network
import os


def generate_fraud_network_graph(state, case_id):
    """
    Builds interactive fraud relationship graph
    """

    output_dir = f"outputs/graphs/{case_id}"
    os.makedirs(output_dir, exist_ok=True)

    net = Network(height="750px", width="100%", bgcolor="#0A0F1C", font_color="white")

    G = nx.Graph()

    classifications = state.get("risk_classifications", {})
    connections = state.get("network_connections", {})

    # Add customer nodes
    for cust_id, risk in classifications.items():

        if risk == "HIGH_RISK":
            color = "red"
            size = 35
        elif risk == "MEDIUM_RISK":
            color = "orange"
            size = 25
        else:
            color = "green"
            size = 18

        G.add_node(
            cust_id,
            label=cust_id,
            color=color,
            size=size
        )

    # Add network edges
    for cust_id, linked_entities in connections.items():

        for linked_id in linked_entities:

            if not G.has_node(linked_id):
                G.add_node(linked_id, label=linked_id, color="gray", size=12)

            G.add_edge(cust_id, linked_id)

    net.from_nx(G)

    graph_path = f"{output_dir}/fraud_network.html"
    net.save_graph(graph_path)

    return graph_path
