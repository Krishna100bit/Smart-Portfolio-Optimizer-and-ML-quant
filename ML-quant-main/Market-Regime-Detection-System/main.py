import importlib
import subprocess
import sys

packages = ["yfinance", "pandas", "numpy", "scikit-learn", "matplotlib"]

for package in packages:
    try:
        importlib.import_module(package.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

plt.style.use("dark_background")

ticker = "BTC-USD"

try:
    data = yf.download(ticker, period="1y", interval="1d")
    data = data[["Close"]]
except Exception:
    dates = pd.date_range(end=pd.Timestamp.today(), periods=365)
    prices = np.cumsum(np.random.randn(365)) + 100
    data = pd.DataFrame({"Close": prices}, index=dates)

data["Returns"] = data["Close"].pct_change()
data["Volatility"] = data["Returns"].rolling(10).std()
data["Momentum"] = data["Close"].pct_change(10)

dataset = data.dropna()[["Volatility", "Momentum"]]

model = KMeans(n_clusters=3, random_state=42, n_init=10)
data.loc[dataset.index, "Regime"] = model.fit_predict(dataset)

fig, ax = plt.subplots(figsize=(14, 7))
scatter = ax.scatter(
    data.index,
    data["Close"],
    c=data["Regime"],
    cmap="coolwarm",
    s=40
)

ax.set_title("Market Regime Detection System", fontsize=18)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
fig.colorbar(scatter, ax=ax)

plt.tight_layout()
plt.show()