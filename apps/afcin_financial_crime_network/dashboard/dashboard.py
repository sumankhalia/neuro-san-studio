import streamlit as st
import json
import os
import pandas as pd

from components.network_graph import render_network_graph
from components.heatmap import render_risk_heatmap
from components.confidence_gauge import render_confidence_gauge


st.set_page_config(layout="wide")

st.title("AFCIN – Financial Crime Intelligence Dashboard")

# Load latest decision output
OUTPUT_FILE = "../outputs/runs/FC-001/final_result.json"

if not os.path.exists(OUTPUT_FILE):
    st.error("No decision data found. Run app.py first.")
    st.stop()

with open(OUTPUT_FILE, "r") as f:
    state = json.load(f)

risk_data = state.get("risk_classifications", {})
decision_data = state.get("portfolio_decisions", {})
confidence_data = state.get("confidence_scores", {})

# Convert to dataframe
df = pd.DataFrame({
    "Customer": list(risk_data.keys()),
    "Risk": list(risk_data.values()),
    "Decision": [decision_data.get(c, "UNKNOWN") for c in risk_data.keys()],
    "Confidence": [confidence_data.get(c, 0.75) for c in risk_data.keys()]
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud Network Graph")
    render_network_graph(df)

with col2:
    st.subheader("Risk Distribution Heatmap")
    render_risk_heatmap(df)

st.subheader("Decision Confidence Overview")

for _, row in df.iterrows():
    render_confidence_gauge(row["Customer"], row["Confidence"])
