import importlib
import subprocess
import sys

packages = ["numpy", "scipy", "matplotlib"]

for package in packages:
    try:
        importlib.import_module(package.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

plt.style.use("dark_background")

S0 = 100
K = 105
T = 1
r = 0.05
sigma = 0.2
simulations = 1000
steps = 252

dt = T / steps
paths = np.zeros((steps, simulations))
paths[0] = S0

for t in range(1, steps):
    z = np.random.standard_normal(simulations)
    paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

payoffs = np.maximum(paths[-1] - K, 0)
mc_price = np.exp(-r * T) * np.mean(payoffs)

d1 = (np.log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

bs_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

fig, ax = plt.subplots(figsize=(14, 7))

for i in range(20):
    ax.plot(paths[:, i], linewidth=1)

ax.set_title(f"Monte Carlo Simulation | MC: {mc_price:.2f} | BS: {bs_price:.2f}")
ax.set_xlabel("Time")
ax.set_ylabel("Stock Price")

plt.tight_layout()
plt.show()