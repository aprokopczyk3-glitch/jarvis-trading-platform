import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD

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

# ===== MACD =====

macd = MACD(close=df["close"])

df["macd"] = macd.macd()
df["macd_signal"] = macd.macd_signal()

# ===== BACKTEST =====

in_position = False
buy_price = None

profit = 0

trades = 0
wins = 0
losses = 0

best_trade = None
worst_trade = None

for i in range(len(df)):

    rsi = df.iloc[i]["rsi"]
    ema_gap = df.iloc[i]["ema_gap"]
    price = df.iloc[i]["close"]

    macd_value = df.iloc[i]["macd"]
    macd_signal = df.iloc[i]["macd_signal"]

    if pd.isna(rsi):
        continue

    if pd.isna(macd_value) or pd.isna(macd_signal):
        continue

    # ===== BUY =====

    if not in_position:

        if (
            ema_gap > 20
            and rsi > 55
            and macd_value > macd_signal
        ):

            buy_price = price
            in_position = True

    # ===== SELL =====

    else:

        if (
            ema_gap < -20
            and rsi < 45
            and macd_value < macd_signal
        ):

            result = price - buy_price

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

            in_position = False

# ===== RAPORT =====

print()
print("====================================")
print(" POSITION BACKTEST V4 (MACD)")
print("====================================")
print()

print("Transakcji:", trades)
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