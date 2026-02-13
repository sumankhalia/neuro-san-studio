import streamlit as st
import altair as alt
import pandas as pd


def render_risk_heatmap(df):

    risk_counts = df["Risk"].value_counts().reset_index()
    risk_counts.columns = ["Risk", "Count"]

    chart = alt.Chart(risk_counts).mark_bar().encode(
        x="Risk",
        y="Count"
    )

    st.altair_chart(chart, use_container_width=True)
