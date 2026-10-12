from pricelevel import PriceLevel
from main import Side, OrderType, Order, Trade

class OrderBook:
    def __init__(self):
        # klucz: cena (int), wartość: obiekt PriceLevel
        self.bids: dict[int, PriceLevel] = {}  # Zlecenia kupna
        self.asks: dict[int, PriceLevel] = {}  # Zlecenia sprzedaży
        self.trades: list[Trade] = []          # Historia zrealizowanych transakcji

    def get_best_bid(self) -> int | None:
        """zwraca najwyższą cenę kupna w księdze"""
        return max(self.bids.keys()) if self.bids else None

    def get_best_ask(self) -> int | None:
        """zwraca najniższą cenę sprzedaży w księdze"""
        return min(self.asks.keys()) if self.asks else None

    def process_order(self, incoming_order: Order) -> list[Trade]:
        """
        1. dopasowuje przychodzące zlecenie z przeciwległą stroną księgi
        2. generuje obiekty Trade
        3. dodaje niewypełnioną resztę zlecenia LIMIT do księgi
        """
        generated_trades: list[Trade] = []

        if incoming_order.side == Side.BUY:
            generated_trades.extend(self._match_buy_order(incoming_order))
        else:
            generated_trades.extend(self._match_sell_order(incoming_order))

        # jeśli zlecenie LIMIT nie zostało w pełni zrealizowane, dodaj resztę do księgi
        if incoming_order.quantity > 0 and incoming_order.order_type == OrderType.LIMIT:
            self._add_to_book(incoming_order)

        self.trades.extend(generated_trades)
        return generated_trades

    def _match_buy_order(self, buy_order: Order) -> list[Trade]:
        trades = []

        while buy_order.quantity > 0 and self.asks:
            best_ask_price = self.get_best_ask()

            # dla zlecenia LIMIT: cena sprzedającego nie może być wyższa niż nasza maksymalna cena
            if buy_order.order_type == OrderType.LIMIT and buy_order.price < best_ask_price:
                break

            level = self.asks[best_ask_price]
            resting_sell_order = level.get_first_order()

            # wolumen transakcji to minimum z dostępnego i żądanego
            match_qty = min(buy_order.quantity, resting_sell_order.quantity)

            # cena transakcji zależy od zlecenia pasywnego w księdze
            trade = Trade(
                buy_order_id=buy_order.order_id,
                sell_order_id=resting_sell_order.order_id,
                quantity=match_qty,
                price=best_ask_price
            )
            trades.append(trade)

            # pomniejszamy wolumeny
            buy_order.quantity -= match_qty
            resting_sell_order.quantity -= match_qty
            level.total_quantity -= match_qty

            # usuwamy zrealizowane zlecenie z czoła kolejki
            if resting_sell_order.quantity == 0:
                level.remove_first_order()

            # usuwamy pusty poziom cenowy
            if len(level) == 0:
                del self.asks[best_ask_price]

        return trades

    def _match_sell_order(self, sell_order: Order) -> list[Trade]:
        trades = []

        while sell_order.quantity > 0 and self.bids:
            best_bid_price = self.get_best_bid()

            # dla zlecenia LIMIT: cena kupującego nie może być niższa niż nasza minimalna cena
            if sell_order.order_type == OrderType.LIMIT and sell_order.price > best_bid_price:
                break

            level = self.bids[best_bid_price]
            resting_buy_order = level.get_first_order()

            match_qty = min(sell_order.quantity, resting_buy_order.quantity)

            trade = Trade(
                buy_order_id=resting_buy_order.order_id,
                sell_order_id=sell_order.order_id,
                quantity=match_qty,
                price=best_bid_price
            )
            trades.append(trade)

            sell_order.quantity -= match_qty
            resting_buy_order.quantity -= match_qty
            level.total_quantity -= match_qty

            if resting_buy_order.quantity == 0:
                level.remove_first_order()

            if len(level) == 0:
                del self.bids[best_bid_price]

        return trades

    def _add_to_book(self, order: Order) -> None:
        """Pomocnicza funkcja dodająca zlecenie do księgi."""
        target_book = self.bids if order.side == Side.BUY else self.asks

        # sprawdzamy order.price zamiast order.side
        if order.price not in target_book:
            target_book[order.price] = PriceLevel(order.price)

        target_book[order.price].add_order(order)

    def __repr__(self) -> str:
        res = ["\n=== Order Book ==="]
        res.append("=== Asks (Sprzedaż) ===")
        for price in sorted(self.asks.keys(), reverse=True):
            level = self.asks[price]
            
            res.append(f" {price / 100:.2f} PLN | Wolumen: {level.total_quantity} (Zleceń: {len(level)})")

        res.append("------------------------")
        for price in sorted(self.bids.keys(), reverse=True):
            level = self.bids[price]
            
            res.append(f" {price / 100:.2f} PLN | Wolumen: {level.total_quantity} (Zleceń: {len(level)})")

        res.append("=== Bids (Kupno) ===")
        return "\n".join(res)