# Order Matching Engine

[Polski](#order-matching-engine-pl) | [English](#order-matching-engine-en)

---
<a name="order-matching-engine-pl"></a>
# Order Matching Engine (PL)

Silnik dopasowywania zleceń giełdowych napisany w języku Python. Projekt symuluje działanie rdzenia giełdy papierów wartościowych, przyjmując zlecenia kupna oraz sprzedaży i realizując transakcje w czasie rzeczywistym.

## Jak to działa? (Mechanizmy silnika)

1. Priorytet Cena-Czas (FIFO)
Zlecenia z najlepszą ceną realizowane są w pierwszej kolejności. Gdy kilka zleceń posiada tę samą cenę, o realizacji decyduje kolejność zgłoszenia (zasada First-In, First-Out).

2. Obsługa typów zleceń
- LIMIT: Zlecenie wykonuje się po określonej cenie lub lepszej. Jeśli brak natychmiastowego dopasowania, trafia do Księgi Zleceń (Order Book).
- MARKET: Zlecenie realizuje się natychmiast po najlepszych cenach dostępnych w danym momencie na rynku.

3. Szybkie anulowanie w czasie O(1)
Dzięki indeksowi słownikowemu `orders_map`, silnik odnajduje i usuwa anulowane zlecenie w czasie stałym, bez potrzeby przeszukiwania całej księgi.

4. Zasady edycji zleceń (Amend)
- Zmniejszenie wolumenu: Zlecenie zachowuje swoją pozycję w kolejce FIFO.
- Zwiększenie wolumenu lub zmiana ceny: Zlecenie traci priorytet i jest przenoszone na koniec kolejki.

5. Bezpieczeństwo finansowe
Ceny przechowywane są jako liczby całkowite (int) reprezentujące grosze, co zapobiega niedokładnościom obliczeniowym typu float.

## Struktura plików

- main.py: Klasy danych (Order, Trade, Side, OrderType) oraz walidacja wejściowa.
- orderbook.py: Logika Księgi Zleceń, algorytm dopasowywania i modyfikacji.
- test_engine.py: Testy jednostkowe sprawdzające reguły biznesowe giełdy.
- benchmark.py: Skrypt mierzący przepustowość zleceń na sekundę.

## Wymagania i uruchomienie

### Wymagania
- Python 3.10 lub nowszy (projekt nie wymaga instalacji zewnętrznych bibliotek).

### Pobranie z serwisu Git

1. Klonowanie repozytorium:
git clone https://github.com/Wiktor284/Order-Matching-Engine

2. Wejście do folderu z projektem:
cd Order-Matching-Engine

### Uruchamianie programu

1. Uruchomienie symulacji giełdy (dodawanie, anulowanie i edycja zleceń):
python orderbook.py

2. Uruchomienie automatycznych testów jednostkowych:
python test_engine.py

3. Uruchomienie testu wydajnościowego:
python benchmark.py


<a name="order-matching-engine-en"></a>
# Order Matching Engine (EN)

Stock exchange order matching engine written in Python. The project simulates the operation of a stock exchange core, receiving buy and sell orders and executing transactions in real time.

## How it works? (Engine mechanisms)

1. Price-Time Priority (FIFO)
Orders with the best price are executed first. When several orders have the same price, the order of submission determines execution (First-In, First-Out rule).

2. Order types support
- LIMIT: The order executes at a specified price or better. If there is no immediate match, it goes to the Order Book.
- MARKET: The order executes immediately at the best prices available on the market at that moment.

3. Fast cancellation in O(1) time
Thanks to the `orders_map` dictionary index, the engine finds and removes a canceled order in constant time, without the need to search the entire book.

4. Order edit rules (Amend)
- Decreasing volume: The order retains its position in the FIFO queue.
- Increasing volume or changing price: The order loses priority and is moved to the end of the queue.

5. Financial safety
Prices are stored as integers (int) representing cents, which prevents floating-point computational inaccuracies.

## File structure

- main.py: Data classes (Order, Trade, Side, OrderType) and input validation.
- orderbook.py: Order Book logic, matching and modification algorithm.
- test_engine.py: Unit tests verifying exchange business rules.
- benchmark.py: Script measuring order throughput per second.

## Requirements and running

### Requirements
- Python 3.10 or newer (the project does not require installing external libraries).

### Cloning from Git

1. Repository cloning:
git clone https://github.com/Wiktor284/Order-Matching-Engine

2. Enter the project folder:
cd Order-Matching-Engine

### Running the program

1. Run the exchange simulation (adding, canceling, and editing orders):
python orderbook.py

2. Run automatic unit tests:
python test_engine.py

3. Run the performance test:
python benchmark.py