import streamlit as st
import altair as alt
import pandas as pd


def render_confidence_gauge(customer, confidence):

    st.write(f"**{customer}**")

    gauge_data = pd.DataFrame({
        "value": [confidence],
        "max": [1.0]
    })

    chart = alt.Chart(gauge_data).mark_arc(innerRadius=40).encode(
        theta=alt.Theta("value", scale=alt.Scale(domain=[0, 1])),
        color=alt.value("green" if confidence > 0.7 else "red")
    )

    st.altair_chart(chart, use_container_width=False)
