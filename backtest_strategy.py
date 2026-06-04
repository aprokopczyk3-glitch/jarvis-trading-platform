import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

df = pd.read_csv("btc_history.csv")

# ===== WSKAŹNIKI =====

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

# ===== SYGNAŁY =====

signals = []

for i in range(len(df)):

    rsi = df.iloc[i]["rsi"]
    ema_gap = df.iloc[i]["ema_gap"]
    price = df.iloc[i]["close"]

    if pd.isna(rsi):
        continue

    signal = "HOLD"
    strength = "WEAK"

    if ema_gap > 20 and rsi > 55:
        signal = "BUY"
        strength = "STRONG"

    elif ema_gap > 10 and rsi > 50:
        signal = "BUY"
        strength = "NORMAL"

    elif ema_gap < -20 and rsi < 45:
        signal = "SELL"
        strength = "STRONG"

    elif ema_gap < -10 and rsi < 50:
        signal = "SELL"
        strength = "NORMAL"

    # TYLKO STRONG
    if signal != "HOLD" and strength == "STRONG":
        signals.append({
            "signal": signal,
            "strength": strength,
            "price": price
        })

# ===== BACKTEST =====

profit = 0
trades = 0

wins = 0
losses = 0

best_trade = None
worst_trade = None

for i in range(len(signals) - 1):

    current = signals[i]
    nxt = signals[i + 1]

    if current["signal"] == "BUY" and nxt["signal"] == "SELL":

        result = nxt["price"] - current["price"]

        profit += result
        trades += 1

        if result > 0:
            wins += 1
        else:
            losses += 1

        if best_trade is None or result > best_trade:
            best_trade = result

        if worst_trade is None or result < worst_trade:
            worst_trade = result

print()
print("====================================")
print(" HISTORICAL BACKTEST (STRONG ONLY)")
print("====================================")
print()

print("Sygnałów:", len(signals))
print("Transakcji:", trades)

print()
print("Profit:", round(profit, 2), "USD")

if trades > 0:

    accuracy = wins / trades * 100

    print("Skuteczność:", round(accuracy, 2), "%")
    print("Wygrane:", wins)
    print("Przegrane:", losses)

    print(
        "Najlepsza:",
        round(best_trade, 2),
        "USD"
    )

    print(
        "Najgorsza:",
        round(worst_trade, 2),
        "USD"
    )
else:
    print("Brak transakcji.")