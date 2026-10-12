from main import Order, Side, OrderType
from orderbook import OrderBook

book = OrderBook()


book.process_order(Order(order_id=1, side=Side.SELL, order_type=OrderType.LIMIT, quantity=10, price=10500)) # 105.00 PLN
book.process_order(Order(order_id=2, side=Side.SELL, order_type=OrderType.LIMIT, quantity=15, price=10500)) # 105.00 PLN
book.process_order(Order(order_id=3, side=Side.SELL, order_type=OrderType.LIMIT, quantity=20, price=10600)) # 106.00 PLN

print("--- Stan księgi przed transakcją ---")
print(book)


buy_order = Order(order_id=4, side=Side.BUY, order_type=OrderType.LIMIT, quantity=20, price=10550)
trades = book.process_order(buy_order)

print("\n--- Wygenerowane Transakcje ---")
for trade in trades:
    print(trade)

print("\n--- Stan księgi po transakcji ---")
print(book)