import random
import time
from main import Side, OrderType, Order
from orderbook import OrderBook

def run_benchmark(num_orders: int = 100000):
    book = OrderBook()
    orders = []

    print(f"Generowanie {num_orders:,} losowych zleceń...")
    base_price = 10000  # 100.00 PLN

    #przygotowujemy zlecenia przed uruchomieniem zegara, 
    #aby czas generowania nie falszował wynikow silnika
    for i in range(1, num_orders + 1):
        side = Side.BUY if random.random() > 0.5 else Side.SELL
        #losowa cena w przedziale 98.00 PLN - 102.00 PLN
        price = base_price + random.randint(-200, 200)
        qty = random.randint(1, 100)
        orders.append(Order(i, side, OrderType.LIMIT, qty, price))

    print("Uruchamianie testu wydajnościowego (Matching Engine)...")
    
    start_time = time.perf_counter()

    total_trades = 0
    for order in orders:
        trades = book.process_order(order)
        total_trades += len(trades)

    end_time = time.perf_counter()
    duration = end_time - start_time
    ops = num_orders / duration

    print("\n" + "="*35)
    print("      WYNIKI BENCHMARKU      ")
    print("="*35)
    print(f"Przetworzone zlecenia:   {num_orders:,}")
    print(f"Zrealizowane transakcje: {total_trades:,}")
    print(f"Czas całkowity:          {duration:.4f} sek.")
    print(f"Wydajność:               {ops:,.2f} zleceń/sek. (OPS)")
    print("="*35)

if __name__ == "__main__":
    run_benchmark(100000)