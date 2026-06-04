import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

df = pd.read_csv("btc_history.csv")

df["rsi"] = RSIIndicator(
    close=df["close"],
    window=14
).rsi()

df["ema9"] = EMAIndicator(
    close=df["close"],
    window=9
).ema_indicator()

df["ema21"] = EMAIndicator(
    close=df["close"],
    window=21
).ema_indicator()

df["ema_gap"] = df["ema9"] - df["ema21"]

print()
print("===== HISTORY ANALYSIS =====")
print()

print("Świeczek:", len(df))

print(
    "RSI średni:",
    round(df["rsi"].mean(), 2)
)

print(
    "EMA GAP średni:",
    round(df["ema_gap"].mean(), 2)
)

print()
print(df[
    [
        "timestamp",
        "close",
        "rsi",
        "ema_gap"
    ]
].tail(20))