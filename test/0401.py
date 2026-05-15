import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = {
    "Samsung Electronics": "005930.KS",
    "SK Hynix": "000660.KS",
    "NVIDIA": "NVDA",
    "Intel": "INTC",
    "TSMC ADR": "TSM",
    "SOXX ETF": "SOXX",
}

def fetch_prices(tickers, period="1y"):
    prices = {}
    for name, ticker in tickers.items():
        data = yf.download(ticker, period=period, auto_adjust=True, progress=False)
        if data.empty or "Close" not in data.columns:
            print(f"skip: {name} ({ticker})")
            continue
        prices[name] = data["Close"]
    return pd.concat(prices, axis=1).dropna(how="all")

prices = fetch_prices(tickers, period="1y")
returns = (prices / prices.iloc[0] - 1) * 100
prices.to_csv("industry_prices.csv", encoding="utf-8-sig")

plt.figure(figsize=(12, 6))
for col in returns.columns:
    plt.plot(returns.index, returns[col], label=str(col), linewidth=1.4)

plt.axhline(0, color="black", linewidth=0.7, linestyle="--")
plt.title("Semiconductor Industry: 1Y Cumulative Return")
plt.ylabel("Return (%)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("industry_price_return.png", dpi=150, bbox_inches="tight")
# plt.show()  # 서버 환경에서는 생략
