import unittest
from main import Side, OrderType, Order
from orderbook import OrderBook

class TestOrderMatchingEngine(unittest.TestCase):
    def setUp(self):
        """Uruchamia się przed każdym pojedynczym testem - tworzy czystą księgę."""
        self.book = OrderBook()

    def test_partial_fill_and_fifo(self):
        """Sprawdza częściową realizację oraz zasadę pierwszeństwa FIFO."""
        #1.sprzedaz 10 szt. po 100 zł (ID: 1)
        self.book.process_order(Order(1, Side.SELL, OrderType.LIMIT, quantity=10, price=10000))
        #2.sprzedaz 20 szt. po 100 zł (ID: 2)
        self.book.process_order(Order(2, Side.SELL, OrderType.LIMIT, quantity=20, price=10000))

        #3.kupno 15 szt. po 100 zł (ID: 3)
        trades = self.book.process_order(Order(3, Side.BUY, OrderType.LIMIT, quantity=15, price=10000))

        #powinny powstac 2 transakcje
        self.assertEqual(len(trades), 2)
        
        #pierwsza transakcja zgarnia cale zlecenie ID:1 (10 sztuk)
        self.assertEqual(trades[0].sell_order_id, 1)
        self.assertEqual(trades[0].quantity, 10)
        
        #druga transakcja zgarnia 5 sztuk ze zlecenia ID:2
        self.assertEqual(trades[1].sell_order_id, 2)
        self.assertEqual(trades[1].quantity, 5)

        #w ksiedze ze zlecenia ID:2 powinno zostac dokladnie 15 sztuk
        self.assertEqual(self.book.asks[10000][0].quantity, 15)

    def test_cancel_order(self):
        """Sprawdza anulowanie zlecenia."""
        self.book.process_order(Order(1, Side.BUY, OrderType.LIMIT, quantity=50, price=9500))
        
        #anulowanie powinno zwrocic True
        self.assertTrue(self.book.cancel_order(1))
        #poziom cenowy 95.00 PLN powinien zniknac z księgi
        self.assertNotIn(9500, self.book.bids)
        #ponowne anulowanie powinno zwrocic False
        self.assertFalse(self.book.cancel_order(1))

    def test_market_order_execution(self):
        """Sprawdza realizację zlecenia MARKET."""
        self.book.process_order(Order(1, Side.SELL, OrderType.LIMIT, quantity=10, price=10000))
        
        #zlecenie MARKET kupujace 5 sztuk
        trades = self.book.process_order(Order(2, Side.BUY, OrderType.MARKET, quantity=5, price=None))
        
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].quantity, 5)
        self.assertEqual(trades[0].price, 10000)

if __name__ == "__main__":
    unittest.main()