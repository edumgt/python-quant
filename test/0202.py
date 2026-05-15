import yfinance as yf
import pandas as pd
import numpy as np

# 원달러 환율 (KRW=X) 및 코스피 ETF (EWY)
usdkrw = yf.download("KRW=X", start="2022-01-01", end="2025-12-31", auto_adjust=True)["Close"]
kospi  = yf.download("EWY",   start="2022-01-01", end="2025-12-31", auto_adjust=True)["Close"]

df = pd.DataFrame({"환율": usdkrw, "코스피ETF": kospi}).dropna()

correlation = df["환율"].corr(df["코스피ETF"])
print(f"원달러 환율 vs 코스피ETF 상관계수: {correlation:.3f}")
print("(음수: 환율 상승 시 코스피 하락 경향)")
