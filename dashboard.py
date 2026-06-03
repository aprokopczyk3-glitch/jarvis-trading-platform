import pandas as pd

df = pd.read_csv("signals.csv")

buy_count = len(df[df["signal"] == "BUY"])
sell_count = len(df[df["signal"] == "SELL"])

profit = 0
trades = 0
wins = 0
losses = 0

capital = 10000

for i in range(len(df) - 1):

    current_signal = df.iloc[i]["signal"]
    current_price = df.iloc[i]["price"]

    next_signal = df.iloc[i + 1]["signal"]
    next_price = df.iloc[i + 1]["price"]

    if current_signal == "BUY" and next_signal == "SELL":

        result = next_price - current_price

        profit += result
        capital += result

        trades += 1

        if result > 0:
            wins += 1
        else:
            losses += 1

print()
print("=" * 40)
print("      JARVIS TRADING DASHBOARD")
print("=" * 40)

print(f"Kapitał początkowy : 10000 USD")
print(f"Kapitał obecny     : {round(capital,2)} USD")
print(f"Zysk               : {round(capital-10000,2)} USD")

print()

print(f"Liczba sygnałów BUY  : {buy_count}")
print(f"Liczba sygnałów SELL : {sell_count}")

print()

print(f"Liczba transakcji : {trades}")
print(f"Wygrane           : {wins}")
print(f"Przegrane         : {losses}")

if trades > 0:
    accuracy = wins / trades * 100
    print(f"Skuteczność       : {round(accuracy,2)} %")

print()
print("=" * 40)