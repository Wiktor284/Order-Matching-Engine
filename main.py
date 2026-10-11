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
    price: int    #cena po jakiej chcemy kupic/sprzedac akcje
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

