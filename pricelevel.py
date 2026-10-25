from collections import deque
from main import Order

class PriceLevel:
    def __init__(self, price: int):
        self.price : int = price
        self.orders : deque[Order] = deque()  #kolejka FIFO zlecen dla danego poziomu cenowego
        self.total_quantity: int = 0  #calkowita ilosc zlecen na tym poziomie cenowym

    def add_order(self, order: Order):
        self.orders.append(order)  #dodaje zlecenie do kolejki
        self.total_quantity += order.quantity  #aktualizuje calkowita ilosc zlecen na tym poziomie cenowym

    def get_first_order(self) -> Order | None:
        return self.orders[0] if self.orders else None 
    
    def remove_first_order(self) -> Order | None:
        if not self.orders:
            return None
        order = self.orders.popleft()  #usuwa pierwsze zlecenie z kolejki
        self.total_quantity -= order.quantity  #aktualizuje calkowita ilosc zlecen na tym poziomie cenowym
        return order
    
    def __len__(self) -> int:
        return len(self.orders)  #zwraca liczbe zlecen

    def __repr__(self) -> str:
        return (f"PriceLevel(Cena: {self.price/100:.2f} PLN | "
                f"Wolumen: {self.total_quantity} | Liczba zleceń: {len(self.orders)}")
