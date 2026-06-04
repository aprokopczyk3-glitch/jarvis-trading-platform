# JARVIS TRADING PLATFORM

## Cel projektu

Budowa własnej platformy tradingowej Jarvis.

Projekt ma rozwijać się etapami:

1. Zbieranie danych.
2. Generowanie sygnałów.
3. Backtesty.
4. Paper trading.
5. Handel na realnym kapitale.

---

## Giełda docelowa

BYBIT

Wszystkie przyszłe testy historyczne oraz handel docelowo mają być oparte o dane Bybit.

---

## Infrastruktura

### VPS

Serwer działa 24/7.

Na VPS uruchomiony jest bot generujący sygnały.

Bot zapisuje dane do:

signals.csv

---

## Repozytorium

GitHub:

jarvis-trading-platform

Repozytorium jest regularnie aktualizowane.

---

## Aktualne skrypty

main.py

Bot działający na VPS.

analyze.py

Podstawowa analiza sygnałów.

analyze_v2.py

Rozszerzona analiza transakcji.

backtest_strategy.py

Backtest sygnałów historycznych.

backtest_position.py

Backtest pozycyjny.

backtest_trend1h.py

Test filtrów trendu 1H.

history_analysis.py

Analiza danych historycznych.

download_1h.py

Pobieranie danych 1H.

---

## Aktualna strategia

Wskaźniki:

* RSI(14)
* EMA9
* EMA21

---

## Dotychczasowe wyniki

### EMA + RSI

Generuje sygnały.

Skuteczność niewystarczająca.

---

### STRONG ONLY

Lepsze wyniki niż NORMAL.

Nadal niewystarczające.

---

### MACD

Nie poprawił wyników.

---

### Filtr trendu 1H

Wymaga większej ilości danych historycznych.

---

## Najważniejsze odkrycia

1. Dane historyczne 5m są obecnie zbyt krótkie (~1000 świec).

2. Dane 1H obejmują znacznie dłuższy okres niż dane 5m.

3. Wyniki strategii mogą być zniekształcone przez zbyt małą próbkę.

4. Potrzebujemy większej historii danych 5m.

---

## Aktualny stan projektu

Projekt działa.

Bot generuje sygnały.

VPS działa stabilnie.

GitHub jest aktualny.

Rozwijamy część analityczną projektu.
