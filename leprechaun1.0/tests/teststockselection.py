import unittest
from modules.stockselection import StockSelectionLeprechaun

class TestStockSelection(unittest.TestCase):
    def test_find_best_stocks(self):
        tickers = ["AAPL", "TSLA", "GOOGL"]
        leprechaun = StockSelectionLeprechaun(tickers)
        result = leprechaun.find_best_stocks()
        self.assertIsInstance(result, list)

if __name__ == "__main__":
    unittest.main()