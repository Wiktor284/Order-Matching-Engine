from collections import deque
from main import Side, OrderType, Order, Trade

class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.trades = []
        self.orders_map = {}

    def get_best_bid(self) -> int:
        if not self.bids:
            return None
        return max(self.bids.keys())

    def get_best_ask(self) -> int:
        if not self.asks:
            return None
        return min(self.asks.keys())

    def process_order(self, incoming_order: Order) -> list[Trade]:
        """Główna bramka wjazdowa: dopasowuje zlecenie lub wpisuje resztki do księgi."""
        generated_trades = []

        if incoming_order.side == Side.BUY:
            generated_trades = self._match_buy(incoming_order)
        else:
            generated_trades = self._match_sell(incoming_order)

        #jesli po dopasowaniu zostal niezrealizowany wolumen i jest to LIMIT wpisujemy do księgi
        if incoming_order.quantity > 0 and incoming_order.order_type == OrderType.LIMIT:
            self._add_to_book(incoming_order)

        self.trades.extend(generated_trades)
        return generated_trades

    def cancel_order(self, order_id: int) -> bool:
        """Anuluje zlecenie w czasie O(1) na podstawie jego ID."""
        if order_id not in self.orders_map:
            print(f"Nie można anulować: Zlecenie ID:{order_id} nie istnieje lub zostało zrealizowane.")
            return False

        #pobieramy zlecenie ze slownika indeksującego
        order = self.orders_map.pop(order_id)
        target_book = self.bids if order.side == Side.BUY else self.asks

        #usuwamy zlecenie z kolejki na danej cenie
        if order.price in target_book:
            queue = target_book[order.price]
            queue.remove(order)
            
            #jesli kolejka na tej cenie jest pusta czyszczymy poziom cenowy
            if not queue:
                del target_book[order.price]

        print(f"ANULOWANO zlecenie ID:{order_id}")
        return True

    def amend_order(self, order_id: int, new_quantity: int = None, new_price: int = None) -> bool:
        """Edytuje istniejace zlecenie z zachowaniem zasad priorytetu FIFO."""
        if order_id not in self.orders_map:
            print(f"Nie można edytować: Zlecenie ID:{order_id} nie istnieje.")
            return False

        order = self.orders_map[order_id]
    
        #przypadek 1: zmiana ceny lub zwiekszenie ilosci
        if (new_price and new_price != order.price) or (new_quantity and new_quantity > order.quantity):
            print(f"EDYCJA ID:{order_id} (Zmiana ceny/zwiększenie wolumenu) -> Przeniesienie na koniec kolejki!")
            self.cancel_order(order_id)
            
            updated_order = Order(
                order_id=order_id,
                side=order.side,
                order_type=order.order_type,
                quantity=new_quantity if new_quantity else order.quantity,
                price=new_price if new_price else order.price
            )
            self.process_order(updated_order)
            return True

        #przypadek 2: zmniejszenie ilosci
        if new_quantity and new_quantity < order.quantity:
            print(f"EDYCJA ID:{order_id} (Zmniejszenie wolumenu z {order.quantity} na {new_quantity}) -> Zachowano pozycję w kolejce.")
            order.quantity = new_quantity
            return True

        return False

    def _match_buy(self, buy_order: Order) -> list[Trade]:
        trades = []

        while buy_order.quantity > 0 and self.asks:
            best_ask = self.get_best_ask()

            if buy_order.order_type == OrderType.LIMIT and buy_order.price < best_ask:
                break

            ask_queue = self.asks[best_ask]

            while ask_queue and buy_order.quantity > 0:
                passive_sell = ask_queue[0]
                traded_qty = min(buy_order.quantity, passive_sell.quantity)

                trade = Trade(
                    buy_order_id=buy_order.order_id,
                    sell_order_id=passive_sell.order_id,
                    price=best_ask,
                    quantity=traded_qty
                )
                trades.append(trade)

                buy_order.quantity -= traded_qty
                passive_sell.quantity -= traded_qty

                #jesli pasywne zlecenie zostalo zrealizowane w calosci usuwamy je
                if passive_sell.quantity == 0:
                    ask_queue.popleft()
                    self.orders_map.pop(passive_sell.order_id, None)

            if not ask_queue:
                del self.asks[best_ask]

        return trades

    def _match_sell(self, sell_order: Order) -> list[Trade]:
        trades = []

        while sell_order.quantity > 0 and self.bids:
            best_bid = self.get_best_bid()

            if sell_order.order_type == OrderType.LIMIT and sell_order.price > best_bid:
                break

            bid_queue = self.bids[best_bid]

            while bid_queue and sell_order.quantity > 0:
                passive_buy = bid_queue[0]
                traded_qty = min(sell_order.quantity, passive_buy.quantity)

                trade = Trade(
                    buy_order_id=passive_buy.order_id,
                    sell_order_id=sell_order.order_id,
                    price=best_bid,
                    quantity=traded_qty
                )
                trades.append(trade)

                sell_order.quantity -= traded_qty
                passive_buy.quantity -= traded_qty

                if passive_buy.quantity == 0:
                    bid_queue.popleft()
                    self.orders_map.pop(passive_buy.order_id, None)

            if not bid_queue:
                del self.bids[best_bid]

        return trades

    def _add_to_book(self, order: Order):
        """Zapisuje zlecenie do księgi oraz rejestruje je w słowniku orders_map."""
        target_book = self.bids if order.side == Side.BUY else self.asks
        if order.price not in target_book:
            target_book[order.price] = deque()
            
        target_book[order.price].append(order)
        self.orders_map[order.order_id] = order  #rejestracja dla szybkiego O(1) lookupu

    def __repr__(self):
        res = ["\n=== ORDER BOOK ==="]
        res.append("--- ASKS (Sprzedaż - rosnąco) ---")
        for price in sorted(self.asks.keys(), reverse=True):
            total_qty = sum(o.quantity for o in self.asks[price])
            res.append(f"  {price / 100:.2f} PLN | Wolumen: {total_qty} (Liczba zleceń: {len(self.asks[price])})")

        res.append("------------------------")
        for price in sorted(self.bids.keys(), reverse=True):
            total_qty = sum(o.quantity for o in self.bids[price])
            res.append(f"  {price / 100:.2f} PLN | Wolumen: {total_qty} (Liczba zleceń: {len(self.bids[price])})")

        res.append("--- BIDS (Kupno - malejąco) ---")
        return "\n".join(res)


#TEST
if __name__ == "__main__":
    book = OrderBook()

    print("--- 1. Dodajemy zlecenia do Księgi ---")
    book.process_order(Order(1, Side.SELL, OrderType.LIMIT, quantity=50, price=10000)) # ID:1 Sell 50szt po 100 zł
    book.process_order(Order(2, Side.BUY, OrderType.LIMIT, quantity=30, price=9500))   # ID:2 Buy 30szt po 95 zł
    book.process_order(Order(3, Side.BUY, OrderType.LIMIT, quantity=20, price=9500))   # ID:3 Buy 20szt po 95 zł
    print(book)

    print("\n--- 2. TEST: Zmniejszenie ilości w ID:2 (Zachowuje pozycję FIFO) ---")
    book.amend_order(order_id=2, new_quantity=10)
    print(book)

    print("\n--- 3. TEST: Anulowanie zlecenia ID:1 ---")
    book.cancel_order(order_id=1)
    print(book)

    print("\n--- 4. TEST: Próba ponownego anulowania ID:1 (powinna zostać odrzucona) ---")
    book.cancel_order(order_id=1)