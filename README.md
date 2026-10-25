# Order Matching Engine

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