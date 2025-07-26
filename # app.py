# app.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Portfolio Simulation Dashboard",
    layout="wide"
)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("Inputs")

# Tickers
tickers = st.sidebar.text_input(
    "Tickers (comma-separated)", 
    value="SPY,AGG,VNQ,DBC"
).upper().split(",")

# Date range
col1, col2 = st.sidebar.columns(2)
start = col1.date_input("Start date", pd.to_datetime("2018-01-01"))
end   = col2.date_input("End date",   pd.to_datetime("2024-12-31"))

# Number of portfolios
n_portfolios = st.sidebar.slider(
    "Number of portfolios", 1000, 20_000, 5_000, step=500
)

# ─── Data Download ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data(tickers, start, end):
    df = yf.download(tickers, start=start, end=end, progress=False)
    # handle MultiIndex vs single
    if isinstance(df.columns, pd.MultiIndex):
        prices = df["Adj Close"] if "Adj Close" in df.columns.get_level_values(0) else df["Close"]
    else:
        prices = df["Adj Close"] if "Adj Close" in df.columns else df["Close"]
    returns = prices.pct_change().dropna()
    return prices, returns

prices, returns = load_data(tickers, start, end)

# ─── Compute Stats ─────────────────────────────────────────────────────────────
# 1) Trading days
trading_days = len(pd.bdate_range(start=start, end=end))

# 2) Daily mean & cov
mean_daily_ret = returns.mean()
cov_daily      = returns.cov()

# 3) Annualize
mean_annual_ret = mean_daily_ret * trading_days
cov_annual      = cov_daily * trading_days

# Display stats
st.header("Sample Statistics")
st.markdown(f"**Trading days in sample:** {trading_days}")
stats_df = pd.DataFrame({
    "Mean Ann. Return": mean_annual_ret,
    "Volatility (Ann.)": np.sqrt(np.diag(cov_annual))
})
st.dataframe(stats_df.style.format("{:.2%}"))

# ─── Monte Carlo Simulation ────────────────────────────────────────────────────
st.header("Monte Carlo Portfolio Simulation")

# Run simulation
n_assets = len(mean_annual_ret)
results = np.zeros((3, n_portfolios))

for i in range(n_portfolios):
    w = np.random.random(n_assets)
    w /= np.sum(w)
    port_ret = w @ mean_annual_ret
    port_vol = np.sqrt(w.T @ cov_annual @ w)
    results[0, i] = port_vol
    results[1, i] = port_ret
    results[2, i] = port_ret / port_vol  # Sharpe (rf=0)

# Plot
fig, ax = plt.subplots()
sc = ax.scatter(
    results[0], results[1],
    c=results[2], cmap="viridis", s=10, alpha=0.5
)
ax.set_xlabel("Annualized Volatility")
ax.set_ylabel("Annualized Return")
ax.set_title(f"Efficient Frontier ({trading_days} trading days)")
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("Sharpe Ratio")

st.pyplot(fig)

# ─── Show Data Samples ─────────────────────────────────────────────────────────
with st.expander("Show last 5 rows of prices & returns"):
    st.subheader("Prices")
    st.dataframe(prices.tail())
    st.subheader("Returns")
    st.dataframe(returns.tail())

