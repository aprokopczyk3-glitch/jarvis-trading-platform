import ccxt
from datetime import datetime
import time
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import pandas as pd
import os

exchange = ccxt.bybit()

session_start = datetime.now()

last_signal = None
last_signal_time = None

previous_ema9 = None
previous_ema21 = None

buy_count = 0
sell_count = 0

COOLDOWN_MINUTES = 5
STOP_LOSS_PERCENT = 1

# ===== POSITION TRACKING =====

in_position = False

entry_time = None
entry_price = None
entry_strength = None

# ===== FILES =====

if not os.path.exists("signals_5m_v2.csv"):
    with open("signals_5m_v2.csv", "w") as file:
        file.write(
            "time,signal,strength,price,rsi,ema9,ema21,ema_gap\n"
        )

if not os.path.exists("bot_log_5m_v2.csv"):
    with open("bot_log_5m_v2.csv", "w") as file:
        file.write(
            "time,price,rsi,ema9,ema21,ema_gap,signal,strength\n"
        )

if not os.path.exists("position_log_5m_v2.csv"):
    with open("position_log_5m_v2.csv", "w") as file:
        file.write(
            "entry_time,exit_time,entry_price,exit_price,profit,strength\n"
        )

try:

    while True:

        try:

            candles = exchange.fetch_ohlcv(
                "BTC/USDT",
                timeframe="5m",
                limit=50
            )

            closes = [candle[4] for candle in candles]

        except Exception as error:

            print()
            print("=" * 40)
            print("BYBIT CONNECTION ERROR")
            print("=" * 40)
            print(error)
            print("Retrying in 60 seconds...")
            print("=" * 40)

            time.sleep(60)
            continue

        close_series = pd.Series(closes)

        rsi = RSIIndicator(
            close_series,
            window=14
        ).rsi().iloc[-1]

        ema9 = EMAIndicator(
            close_series,
            window=9
        ).ema_indicator().iloc[-1]

        ema21 = EMAIndicator(
            close_series,
            window=21
        ).ema_indicator().iloc[-1]

        ema_gap = ema9 - ema21

        now = datetime.now()


        signal = "HOLD"
        strength = "NONE"

        # ===== STOP LOSS =====

        if in_position:

            stop_loss_price = (
                entry_price *
                (1 - STOP_LOSS_PERCENT / 100)
            )

            if closes[-1] <= stop_loss_price:

                trade_profit = (
                    closes[-1] - entry_price
                )

                with open(
                    "position_log_5m_v2.csv",
                    "a"
                ) as file:

                    file.write(
                        f"{entry_time},"
                        f"{now},"
                        f"{entry_price},"
                        f"{closes[-1]},"
                        f"{trade_profit:.2f},"
                        f"{entry_strength}\n"
                    )

                print()
                print("=" * 40)
                print("STOP LOSS HIT")
                print("=" * 40)

                print(
                    f"ENTRY : {entry_price}"
                )

                print(
                    f"EXIT  : {closes[-1]}"
                )

                print(
                    f"LOSS : {trade_profit:.2f} USD"
                )

                print("=" * 40)

                in_position = False

                entry_time = None
                entry_price = None
                entry_strength = None

        if abs(ema_gap) > 20:
            strength = "STRONG"
        elif abs(ema_gap) > 10:
            strength = "NORMAL"
        else:
            strength = "WEAK"

        if previous_ema9 is not None and previous_ema21 is not None:

            if (
                previous_ema9 <= previous_ema21
                and ema9 > ema21
                and rsi < 70
            ):
                signal = "BUY"

            elif (
                previous_ema9 >= previous_ema21
                and ema9 < ema21
                and rsi > 30
            ):
                signal = "SELL"

        # IGNORUJ WEAK SYGNAŁY

        if strength == "WEAK":
            signal = "HOLD"

        can_signal = True

        if last_signal_time is not None:

            minutes_since_signal = (
                now - last_signal_time
            ).total_seconds() / 60

            if minutes_since_signal < COOLDOWN_MINUTES:
                can_signal = False

        if (
            signal != "HOLD"
            and signal != last_signal
            and can_signal
        ):

            print()
            print("=" * 40)
            print(f"NEW {signal} SIGNAL")
            print("=" * 40)

            if signal == "BUY":

                buy_count += 1

                if not in_position:

                    in_position = True

                    entry_time = now
                    entry_price = closes[-1]
                    entry_strength = strength

            elif signal == "SELL":

                sell_count += 1

                if in_position:

                    trade_profit = (
                        closes[-1] - entry_price
                    )

                    with open(
                        "position_log_5m_v2.csv",
                        "a"
                    ) as file:

                        file.write(
                            f"{entry_time},"
                            f"{now},"
                            f"{entry_price},"
                            f"{closes[-1]},"
                            f"{trade_profit:.2f},"
                            f"{entry_strength}\n"
                        )

                    print()
                    print("=" * 40)
                    print("POSITION CLOSED")
                    print("=" * 40)
                    print(
                        f"ENTRY : {entry_price}"
                    )
                    print(
                        f"EXIT  : {closes[-1]}"
                    )
                    print(
                        f"PROFIT: {trade_profit:.2f} USD"
                    )
                    print("=" * 40)

                    in_position = False

                    entry_time = None
                    entry_price = None
                    entry_strength = None

            with open("signals_5m_v2.csv", "a") as file:
                file.write(
                    f"{now},"
                    f"{signal},"
                    f"{strength},"
                    f"{closes[-1]},"
                    f"{rsi:.2f},"
                    f"{ema9:.2f},"
                    f"{ema21:.2f},"
                    f"{ema_gap:.2f}\n"
                )

            last_signal = signal
            last_signal_time = now

        with open("bot_log_5m_v2.csv", "a") as file:
            file.write(
                f"{now},"
                f"{closes[-1]},"
                f"{rsi:.2f},"
                f"{ema9:.2f},"
                f"{ema21:.2f},"
                f"{ema_gap:.2f},"
                f"{signal},"
                f"{strength}\n"
            )

        previous_ema9 = ema9
        previous_ema21 = ema21

        print(f"Time: {now}")
        print(f"Price: {closes[-1]}")
        print(f"RSI: {rsi:.2f}")
        print(f"EMA9: {ema9:.2f}")
        print(f"EMA21: {ema21:.2f}")
        print(f"EMA GAP: {ema_gap:.2f}")
        print(f"Strength: {strength}")
        print(f"Signal: {signal}")

        print(f"BUY Count : {buy_count}")
        print(f"SELL Count: {sell_count}")

        if in_position:
            print(
                f"OPEN POSITION: "
                f"{entry_price}"
            )

        print("Waiting 300 seconds...")
        print("-" * 40)

        previous_ema9 = ema9
        previous_ema21 = ema21

        time.sleep(300)

except KeyboardInterrupt:

    session_end = datetime.now()
    duration = session_end - session_start

    print()
    print("=" * 40)
    print("      JARVIS SESSION REPORT")
    print("=" * 40)

    print(f"Session Start : {session_start}")
    print(f"Session End   : {session_end}")
    print(f"Duration      : {duration}")

    print()
    print(f"BUY Signals   : {buy_count}")
    print(f"SELL Signals  : {sell_count}")
    print(f"Total Signals : {buy_count + sell_count}")

    print("=" * 40)