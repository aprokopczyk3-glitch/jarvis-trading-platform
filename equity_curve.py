import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("signals.csv")

capital = 10000

equity = [capital]

for i in range(len(df) - 1):

    current_signal = df.iloc[i]["signal"]
    current_price = df.iloc[i]["price"]

    next_signal = df.iloc[i + 1]["signal"]
    next_price = df.iloc[i + 1]["price"]

    if current_signal == "BUY" and next_signal == "SELL":

        result = next_price - current_price

        capital += result

        equity.append(capital)

plt.figure(figsize=(10, 5))
plt.plot(equity)

plt.title("Jarvis Equity Curve")
plt.xlabel("Transakcja")
plt.ylabel("Kapitał (USD)")

plt.grid(True)

plt.show()