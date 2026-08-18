import importlib
import subprocess
import sys

packages = ["streamlit", "numpy", "pandas", "plotly"]

for package in packages:
    try:
        importlib.import_module(package.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown(
    "<style>body{background-color:#0d1117;color:white;}</style>",
    unsafe_allow_html=True
)

prices = np.linspace(95000, 105000, 60)
bids = np.random.randint(10, 100, 60)
asks = np.random.randint(10, 100, 60)

heatmap = pd.DataFrame({
    "Price": prices,
    "Bid": bids,
    "Ask": asks
})

imbalance = (heatmap["Bid"].sum() - heatmap["Ask"].sum())

st.title("Crypto Order Flow Heatmap")

col1, col2 = st.columns(2)

with col1:
    st.metric("Bid/Ask Imbalance", f"{imbalance:.2f}")

with col2:
    st.metric("Liquidity Zones", int((heatmap["Bid"] + heatmap["Ask"]).mean()))

fig = px.density_heatmap(
    heatmap,
    x="Price",
    y="Bid",
    z="Ask",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(fig, use_container_width=True)