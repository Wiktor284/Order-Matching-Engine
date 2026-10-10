from dataclasses import dataclass
from enum import Enum
import time

class Side(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

@dataclass
class Order:
    order_id: int
    side: Side
    order_type: OrderType
    quantity: int  #liczba akcji do kupienia
    price: int    # cena po jakiej chcemy kupic/sprzedac akcje
    timestamp: float = None #czas przyjecia zlecenia

    def __post_init__(self):  #ustawia aktualny timestamp
        if self.timestamp is None:
            self.timestamp = time.time_ns()

#walidacja danych wejsciowych
        if self.quantity <= 0:
            raise ValueError("Quantity musi byc wieksze od zera.")

        if self.order_type == OrderType.LIMIT and (self.price is None or self.price <= 0):
            raise ValueError("Cena musi byc wieksza od zera dla zlecen limitowych.")

    def __repr__(self):
        price_str = f"{self.price/ 100:.2f} PLN" if self.price else "Market"
        return (f"[{self.side.value}] ID:{self.order_id} | "
            f"Ilość: {self.quantity} | Cena: {price_str}")

if __name__ == "__main__":
    # przykładowe uzycie klasy Order
    o1 = Order(order_id=1, side=Side.BUY, order_type=OrderType.LIMIT, quantity=100, price=5000)
    print("Stworzono:", o1)
    
    o2 = Order(order_id=2, side=Side.SELL, order_type=OrderType.MARKET, quantity=50, price=None)
    print("Stworzono:", o2)

    try: 
        o_bad = Order(order_id=3, side=Side.BUY, order_type=OrderType.LIMIT, quantity=-10, price=-50)
    except ValueError as e:
        print("Wylapano oczekiwany blad walidacji :" , e)
