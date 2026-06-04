import ccxt
import pandas as pd

exchange = ccxt.bybit()

print("Pobieranie danych...")

ohlcv = exchange.fetch_ohlcv(
    "BTC/USDT",
    timeframe="5m",
    limit=1000
)

df = pd.DataFrame(
    ohlcv,
    columns=[
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    unit="ms"
)

print()
print("Liczba świeczek:", len(df))
print()

print(df.head())

df.to_csv(
    "btc_history.csv",
    index=False
)

print()
print("Zapisano btc_history.csv")