from collections import deque

from main import Side, OrderType, Order

class OrderBook:
    def __init__(self):
        #przechowuje zlecenia limit przypisane do cen
        self.bids = {}  # słownik zleceń kupna, klucz: cena, wartość: kolejka zleceń
        self.asks = {}  # słownik zleceń sprzedaży, klucz

    def add_order(self, order: Order):
        #dodaje zlecenie limit do odpowiedniej strony ksiegi zlecen
        if order.order_type == OrderType.MARKET:
            #zlecenia market jest od razu realizowane, więc nie dodajemy go do ksiegi zlecen
            return
        if order.side == Side.BUY:
            target_book = self.bids
        else:
            target_book = self.asks

        #jezeli dana cena nie istnieje w ksiedze zlecen, tworzymy nowa kolejke fifo
        if order.price not in target_book:
            target_book[order.price] = deque()

        target_book[order.price].append(order)  #dodajemy zlecenie do kolejki dla danej ceny

    def get_best_bid(self) -> int:
        #zwraca najwyzsza cene kupna w ksiedze zlecen
        if not self.bids:
            return None
        return max(self.bids.keys())

    def get_best_ask(self) -> int:
        #zwraca najnizsza cene sprzedazy w ksiedze zlecen
        if not self.asks:
            return None
        return min(self.asks.keys())

    def __repr__(self):
        #reprezentacja ksiegi zlecen w formie tekstowej
        res = ["\n=== Order Book ==="]
        res.append("===Asks===")
        for price in sorted(self.asks.keys(), reverse=True):
            total_qty = sum(order.quantity for order in self.asks[price])
            res.append(f" {price/100:.2f} PLN | Wolumen {total_qty} (Liczba zleceń: {len(self.asks[price])})")

        res.append("------------------------")
        for price in sorted(self.bids.keys(), reverse=True):
            total_qty = sum(order.quantity for order in self.bids[price])
            res.append(f" {price/100:.2f} PLN | Wolumen {total_qty} (Liczba zleceń: {len(self.bids[price])})")

        res.append("===Bids===")
        return "\n".join(res)  

