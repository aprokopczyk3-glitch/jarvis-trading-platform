import ccxt

exchange = ccxt.bybit()

candles = exchange.fetch_ohlcv(
    "BTC/USDT",
    timeframe="1m",
    limit=5
)

closes = []

for candle in candles:
    closes.append(candle[4])

average = sum(closes) / len(closes)

current_price = closes[-1]

print(f"Current price: {current_price}")
print(f"Average price: {average}")

if current_price > average:
    print("BUY SIGNAL")
else:
    print("SELL SIGNAL")