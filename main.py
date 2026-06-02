import ccxt
from datetime import datetime
import time

exchange = ccxt.bybit()

while True:

    candles = exchange.fetch_ohlcv(
        "BTC/USDT",
        timeframe="1m",
        limit=20
    )

    closes = []

    for candle in candles:
        closes.append(candle[4])

    fast_ma = sum(closes[-5:]) / 5
    slow_ma = sum(closes) / 20

    now = datetime.now()

    if fast_ma > slow_ma:
        signal = "BUY"
    else:
        signal = "SELL"

    print(f"Time: {now}")
    print(f"Fast MA: {fast_ma}")
    print(f"Slow MA: {slow_ma}")
    print(f"Signal: {signal}")

    with open("signals.txt", "a") as file:
        file.write(
            f"{now} | {signal} | Fast={fast_ma} | Slow={slow_ma}\n"
        )

    print("Waiting 60 seconds...")
    time.sleep(60)