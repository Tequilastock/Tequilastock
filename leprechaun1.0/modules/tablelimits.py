# tablelimits.py for Leprechaun 1.0

import yfinance as yf
from ib_insync import *
import math
import logging
import traceback
import time
import asyncio
from unittest.mock import MagicMock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TableLimits:
    def __init__(self, ib_api_key, balance):
        self.ib = IB()
        self.ib_api_key = ib_api_key
        self.balance = balance
        self.max_retries = 5
        self.retry_delay = 3
        self._connect_to_ib()

    def _connect_to_ib(self):
        retries = 0
        while retries < self.max_retries:
            try:
                logging.info(f"Attempting to connect to IB Gateway (Attempt {retries + 1}/{self.max_retries})...")
                self.ib.connect('127.0.0.1', 7497, clientId=1)  # Assuming paper trading port and client ID
                logging.info("Connected to IB Gateway successfully.")
                break
            except ConnectionRefusedError as e:
                logging.error(f"API connection failed: {e}")
                logging.error("Make sure API port on TWS/IBG is open")
                retries += 1
                time.sleep(self.retry_delay)
            except Exception as e:
                logging.error(f"Unexpected error during connection: {e}")
                traceback.print_exc()
                retries += 1
                time.sleep(self.retry_delay)
        else:
            logging.critical("Failed to connect to IB Gateway after multiple attempts.")
            raise ConnectionError("Unable to connect to IB Gateway.")

    def find_best_stocks(self, selected_stocks):
        try:
            best_stocks = []
            for stock in selected_stocks:
                ticker = stock['ticker']
                current_price = stock['current_price']
                price_diff_percentage = stock['price_diff_percentage']
                ewma_volatility_5d = stock['ewma_volatility_5d']
                ewma_volatility_1mo = stock['ewma_volatility_1mo']

                # Basic criterion for stock selection: low price difference and moderate volatility
                if 1 <= price_diff_percentage <= 15 and 0.05 <= ewma_volatility_5d <= 5:
                    best_stocks.append(stock)
                    logging.info(f"Selected Stock - Ticker: {ticker}, Price Difference (%): {price_diff_percentage}, EWMA Volatility (5d): {ewma_volatility_5d}, EWMA Volatility (1mo): {ewma_volatility_1mo}")
            return best_stocks
        except Exception as e:
            logging.error(f"Error finding best stocks: {e}")
            traceback.print_exc()
            raise

    def find_options_and_place_bets(self, stocks):
        try:
            for stock in stocks:
                ticker = stock['ticker']
                stock_price = stock['current_price']

                # Search for call and put options with Interactive Brokers API
                contract = Stock(ticker, 'SMART', 'USD')
                self.ib.qualifyContracts(contract)
                chains = self.ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)

                # Filter out the suitable strikes (closest strike prices)
                calls, puts = self._find_closest_strikes(chains, stock_price)

                # Place bets for call and put options
                if calls and puts:
                    for call in calls:
                        self._place_order(call, 'BUY')
                    for put in puts:
                        self._place_order(put, 'BUY')
        except Exception as e:
            logging.error(f"Error finding options or placing bets for stocks: {e}")
            traceback.print_exc()
            raise

    def _find_closest_strikes(self, chains, target_price):
        try:
            min_diff = math.inf
            closest_calls = []
            closest_puts = []

            # Iterate through all option chains and identify closest strikes
            for chain in chains:
                for strike in chain.strikes:
                    diff = abs(target_price - strike)
                    if diff < min_diff:
                        min_diff = diff
                        closest_calls = [Option(chain.symbol, chain.expirations[0], strike, 'C', 'SMART')]
                        closest_puts = [Option(chain.symbol, chain.expirations[0], strike, 'P', 'SMART')]
                    elif diff == min_diff:
                        closest_calls.append(Option(chain.symbol, chain.expirations[0], strike, 'C', 'SMART'))
                        closest_puts.append(Option(chain.symbol, chain.expirations[0], strike, 'P', 'SMART'))

            return closest_calls, closest_puts
        except Exception as e:
            logging.error(f"Error finding closest strike prices: {e}")
            traceback.print_exc()
            raise

    def _place_order(self, contract, action, quantity=1):
        retries = 0
        while retries < self.max_retries:
            try:
                order = MarketOrder(action, quantity)
                trade = self.ib.placeOrder(contract, order)
                self.ib.sleep(1)  # Allow the order to process
                if trade.orderStatus.status == 'Filled':
                    logging.info(f"Order {action} {quantity} of {contract.symbol} filled successfully.")
                    break
                else:
                    logging.warning(f"Order for {contract.symbol} not filled yet. Current status: {trade.orderStatus.status}")
                    retries += 1
                    time.sleep(self.retry_delay)
            except Exception as e:
                logging.error(f"Error placing order for {contract.symbol}: {e}")
                traceback.print_exc()
                retries += 1
                time.sleep(self.retry_delay)
        else:
            logging.critical(f"Failed to place order for {contract.symbol} after multiple attempts.")
            raise Exception(f"Order for {contract.symbol} could not be placed.")

    def manage_balance(self, initial_balance, bets):
        try:
            current_balance = initial_balance
            # Loop through bets to update balance and track gains or losses
            for bet in bets:
                # Update balance based on bet outcome
                current_balance += bet['profit']  # Assuming bet object contains 'profit' value
            logging.info(f"Current balance updated to: {current_balance}")
        except Exception as e:
            logging.error(f"Error managing balance: {e}")
            traceback.print_exc()
            raise

if __name__ == "__main__":
    # Replace with your IB account details and initial balance
    ib_api_key = "your_ib_api_key_here"
    initial_balance = 10000  # Set initial balance

    # Mocking IB connection for testing without actual IB Gateway
    mock_ib = MagicMock(spec=IB)
    TableLimits.ib = mock_ib
    table_limits = TableLimits(ib_api_key, initial_balance)

    try:
        # Assuming selected_stocks are fetched from polygonapi.py
        selected_stocks = [
            {
                'ticker': 'AAPL',
                'current_price': 150.0,
                'price_diff_percentage': 8.0,
                'ewma_volatility_5d': 0.3,
                'ewma_volatility_1mo': 1.2
            },
            # Add more stock data here...
        ]
        best_stocks = table_limits.find_best_stocks(selected_stocks)
        table_limits.find_options_and_place_bets(best_stocks)
        # Placeholder for managing balance after bets
        table_limits.manage_balance(initial_balance, bets=[])
    except Exception as e:
        logging.critical(f"Critical error occurred: {e}")

