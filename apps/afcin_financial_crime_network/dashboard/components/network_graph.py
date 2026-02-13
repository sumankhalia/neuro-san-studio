import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random


def render_network_graph(df):

    G = nx.Graph()

    # Add nodes
    for _, row in df.iterrows():
        G.add_node(row["Customer"], risk=row["Risk"])

    customers = list(df["Customer"])

    # Synthetic connections (demo realism)
    for cust in customers:
        connections = random.sample(customers, k=min(2, len(customers)))
        for conn in connections:
            if cust != conn:
                G.add_edge(cust, conn)

    pos = nx.spring_layout(G)

    colors = []
    for node in G.nodes():
        risk = G.nodes[node]["risk"]

        if risk == "HIGH_RISK":
            colors.append("red")
        elif risk == "MEDIUM_RISK":
            colors.append("orange")
        else:
            colors.append("green")

    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color=colors)

    st.pyplot(plt)
