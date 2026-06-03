import pandas as pd

try:

    df = pd.read_csv("signals.csv")

    if len(df) < 2:
        print("Za mało danych do analizy.")
        exit()

    print("=" * 50)
    print("         JARVIS ANALYSIS REPORT")
    print("=" * 50)

    print()
    print("Liczba rekordów:", len(df))

    print()
    print("BUY :", len(df[df["signal"] == "BUY"]))
    print("SELL:", len(df[df["signal"] == "SELL"]))

    print()
    print("STRONG:", len(df[df["strength"] == "STRONG"]))
    print("NORMAL:", len(df[df["strength"] == "NORMAL"]))
    print("WEAK  :", len(df[df["strength"] == "WEAK"]))

    print()
    print("Średni RSI:", round(df["rsi"].mean(), 2))
    print("Najwyższy RSI:", round(df["rsi"].max(), 2))
    print("Najniższy RSI:", round(df["rsi"].min(), 2))

    print()
    print("Średni EMA GAP:", round(df["ema_gap"].mean(), 2))
    print("Największy EMA GAP:", round(df["ema_gap"].max(), 2))
    print("Najmniejszy EMA GAP:", round(df["ema_gap"].min(), 2))

    print()
    print("=" * 50)
    print("BACKTEST")
    print("=" * 50)

    profit = 0
    trades = 0

    wins = 0
    losses = 0

    capital = 10000

    best_trade = None
    worst_trade = None

    total_win_amount = 0
    total_loss_amount = 0

    current_win_streak = 0
    current_loss_streak = 0

    max_win_streak = 0
    max_loss_streak = 0

    trade_results = []

    strength_stats = {
        "WEAK": {
            "profit": 0,
            "trades": 0,
            "wins": 0
        },
        "NORMAL": {
            "profit": 0,
            "trades": 0,
            "wins": 0
        },
        "STRONG": {
            "profit": 0,
            "trades": 0,
            "wins": 0
        }
    }

    for i in range(len(df) - 1):

        current_signal = df.iloc[i]["signal"]
        current_price = df.iloc[i]["price"]
        current_strength = df.iloc[i]["strength"]

        next_signal = df.iloc[i + 1]["signal"]
        next_price = df.iloc[i + 1]["price"]

        if current_signal == "BUY" and next_signal == "SELL":

            result = next_price - current_price

            trade_results.append(result)

            profit += result
            capital += result
            trades += 1

            strength_stats[current_strength]["profit"] += result
            strength_stats[current_strength]["trades"] += 1

            if result > 0:

                wins += 1

                total_win_amount += result

                current_win_streak += 1
                current_loss_streak = 0

                strength_stats[current_strength]["wins"] += 1

            else:

                losses += 1

                total_loss_amount += abs(result)

                current_loss_streak += 1
                current_win_streak = 0

            max_win_streak = max(
                max_win_streak,
                current_win_streak
            )

            max_loss_streak = max(
                max_loss_streak,
                current_loss_streak
            )

            if best_trade is None or result > best_trade:
                best_trade = result

            if worst_trade is None or result < worst_trade:
                worst_trade = result

            print(
                f"{current_strength} | "
                f"BUY {current_price} -> "
                f"SELL {next_price} = "
                f"{round(result, 2)} USD"
            )

    print()
    print("Liczba transakcji:", trades)
    print("Łączny wynik:", round(profit, 2), "USD")

    print()
    print("=" * 50)
    print("SKUTECZNOŚĆ")
    print("=" * 50)

    print("Wygrane:", wins)
    print("Przegrane:", losses)

    if trades > 0:

        accuracy = wins / trades * 100

        print("Skuteczność:", round(accuracy, 2), "%")

    print()

    if wins > 0:
        print(
            "Średni zysk:",
            round(total_win_amount / wins, 2),
            "USD"
        )

    if losses > 0:
        print(
            "Średnia strata:",
            round(total_loss_amount / losses, 2),
            "USD"
        )

    if total_loss_amount > 0:
        profit_factor = (
            total_win_amount /
            total_loss_amount
        )

        print(
            "Profit Factor:",
            round(profit_factor, 2)
        )

    print()

    if best_trade is not None:
        print(
            "Najlepsza transakcja:",
            round(best_trade, 2),
            "USD"
        )

    if worst_trade is not None:
        print(
            "Najgorsza transakcja:",
            round(worst_trade, 2),
            "USD"
        )

    print()

    print(
        "Najdłuższa seria wygranych:",
        max_win_streak
    )

    print(
        "Najdłuższa seria przegranych:",
        max_loss_streak
    )

    print()

    print("=" * 50)
    print("STRENGTH ANALYSIS")
    print("=" * 50)

    for strength in ["WEAK", "NORMAL", "STRONG"]:

        stats = strength_stats[strength]

        print()
        print(strength)

        print(
            "Transakcje:",
            stats["trades"]
        )

        print(
            "Profit:",
            round(stats["profit"], 2),
            "USD"
        )

        if stats["trades"] > 0:

            accuracy = (
                stats["wins"] /
                stats["trades"]
            ) * 100

            print(
                "Skuteczność:",
                round(accuracy, 2),
                "%"
            )

    print()

    print("=" * 50)
    print("KAPITAŁ")
    print("=" * 50)

    print("Kapitał początkowy: 10000 USD")
    print("Kapitał końcowy:", round(capital, 2), "USD")
    print(
        "Zysk:",
        round(capital - 10000, 2),
        "USD"
    )

except FileNotFoundError:

    print("Brak pliku signals.csv")