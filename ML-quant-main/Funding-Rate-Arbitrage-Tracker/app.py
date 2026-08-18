import importlib
import subprocess
import sys

packages = ["streamlit", "ccxt", "pandas", "plotly"]

for package in packages:
    try:
        importlib.import_module(package.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

exchanges = ["Binance", "Bybit", "OKX", "KuCoin"]

rates = pd.DataFrame({
    "Exchange": exchanges,
    "FundingRate": np.random.uniform(-0.05, 0.05, len(exchanges))
})

rates["Opportunity"] = rates["FundingRate"].abs()

st.title("Funding Rate Arbitrage Tracker")

st.dataframe(rates)

fig = px.bar(
    rates,
    x="Exchange",
    y="FundingRate",
    color="Opportunity",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)