import numpy as np
from modules.polygonapi import PolygonAPI

class StockSelectionLeprechaun:
    def __init__(self, tickers):
        self.tickers = tickers

    def find_best_stocks(self):
        best_stocks = []
        for ticker in self.tickers:
            data = PolygonAPI.get_stock_data(ticker)
            current_price = data['results'][0]['c']
            avg_price = np.mean([x['c'] for x in data['results']])
            if 0.96 * avg_price <= current_price <= 1.04 * avg_price:
                best_stocks.append(ticker)
        return best_stocks