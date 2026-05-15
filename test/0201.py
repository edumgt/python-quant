import yfinance as yf
import pandas as pd

# WTI 원유 선물 가격 (CL=F) 수집
#################################################################################

# 20일 이동평균 추가
oil_ma20 = oil.rolling(20).mean()

print(f"최근 종가: ${oil.iloc[-1]:.2f}/배럴")
print(f"20일 이동평균: ${oil_ma20.iloc[-1]:.2f}/배럴")
print(f"52주 최고: ${oil[-252:].max():.2f}")
print(f"52주 최저: ${oil[-252:].min():.2f}")
