import importlib
import subprocess
import sys

packages = ["yfinance", "pandas", "numpy", "matplotlib"]

for package in packages:
    try:
        importlib.import_module(package.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")

tickers = ["AAPL", "MSFT", "NVDA", "GOOGL"]

try:
    data = yf.download(tickers, period="1y")["Close"]
except Exception:
    dates = pd.date_range(end=pd.Timestamp.today(), periods=252)
    data = pd.DataFrame(np.random.randn(252, 4).cumsum(axis=0), columns=tickers, index=dates)

returns = data.pct_change().dropna()

portfolio_returns = []
portfolio_risk = []
sharpe = []

for _ in range(5000):
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)

    expected_return = np.sum(returns.mean() * weights) * 252
    risk = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    ratio = expected_return / risk

    portfolio_returns.append(expected_return)
    portfolio_risk.append(risk)
    sharpe.append(ratio)

fig, ax = plt.subplots(figsize=(14, 7))

scatter = ax.scatter(
    portfolio_risk,
    portfolio_returns,
    c=sharpe,
    cmap="plasma",
    s=10
)

best = np.argmax(sharpe)

ax.scatter(
    portfolio_risk[best],
    portfolio_returns[best],
    marker="*",
    s=300
)

ax.set_title("Smart Portfolio Optimizer")
ax.set_xlabel("Risk")
ax.set_ylabel("Return")

fig.colorbar(scatter, ax=ax)

plt.tight_layout()
plt.show()