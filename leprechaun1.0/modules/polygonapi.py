import requests
import yfinance as yf
import time
from datetime import datetime, timedelta
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PolygonAPI:
    def __init__(self, api_key, max_retries=5, retry_delay=3):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _get_response(self, endpoint):
        retries = 0
        while retries < self.max_retries:
            try:
                url = f"{self.base_url}{endpoint}?apiKey={self.api_key}"
                response = requests.get(url)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    logging.error(f"Authentication failed. Check your API key. Response: {response.text}")
                    raise PermissionError("Invalid API key provided.")
                else:
                    logging.warning(f"Non-success status code {response.status_code} received. Response: {response.text}")
                    retries += 1
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                retries += 1
                traceback.print_exc()
            time.sleep(self.retry_delay)
        raise Exception(f"Failed to get response after {self.max_retries} retries.")

    def get_top_150_highly_traded_tickers(self):
        # Instead of fetching data from Polygon.io, use a predefined list of tickers
        predefined_tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NVDA", "JPM", "V", "JNJ",
            "UNH", "HD", "PG", "PYPL", "DIS", "MA", "ADBE", "NFLX", "INTC", "PFE",
            "KO", "PEP", "T", "CSCO", "XOM", "NKE", "MRK", "ABT", "CRM", "COST",
            "CVX", "MDT", "ACN", "AVGO", "WMT", "LLY", "QCOM", "MCD", "TXN", "ORCL",
            "AMGN", "NEE", "IBM", "HON", "SBUX", "GS", "RTX", "NOW", "BLK", "TMO",
            "BA", "BMY", "LIN", "UNP", "CVS", "LOW", "SPGI", "PM", "ISRG", "FIS",
            "CHTR", "INTU", "GE", "PLD", "CAT", "ZTS", "BKNG", "DE", "MMC", "AMT",
            "ADP", "GILD", "MS", "AXP", "MO", "LMT", "SCHW", "SYK", "CCI", "CME",
            "MDLZ", "DHR", "EL", "BDX", "LRCX", "ATVI", "DUK", "TGT", "PGR", "ILMN",
            "FISV", "CI", "ICE", "CSX", "NSC", "EOG", "FDX", "GM", "APD", "COP",
            "ITW", "ADI", "SHW", "SO", "CL", "ETN", "PSA", "MMM", "MET", "SPG",
            "AON", "AEP", "WM", "EW", "FCX", "MCO", "BAX", "CMG", "KLAC", "AIG",
            "MAR", "MPC", "SRE", "WBA", "TRV", "EBAY", "MCK", "VLO", "OXY", "RMD"
        ]
        return predefined_tickers

    def fetch_stock_data(self, ticker):
        stock = yf.Ticker(ticker)
        try:
            # Fetch historical data for different periods
            hist_3mo = stock.history(period="3mo")
            hist_1mo = stock.history(period="1mo")
            hist_5d = stock.history(period="5d")

            if not hist_3mo.empty and not hist_1mo.empty and not hist_5d.empty:
                current_price = hist_1mo['Close'].iloc[-1]
                average_price_1mo = hist_1mo['Close'].mean()
                ewma_volatility_5d = hist_5d['Close'].ewm(span=5).std().iloc[-1]
                ewma_volatility_1mo = hist_1mo['Close'].ewm(span=20).std().iloc[-1]
                return current_price, average_price_1mo, ewma_volatility_5d, ewma_volatility_1mo
            else:
                raise ValueError(f"No sufficient historical data found for ticker {ticker}")
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
            traceback.print_exc()
            raise

    def find_stocks_with_criteria(self, tickers):
        selected_stocks = []
        for ticker in tickers:
            try:
                # Fetch stock data for the given ticker
                current_price, average_price_1mo, ewma_volatility_5d, ewma_volatility_1mo = self.fetch_stock_data(ticker)
                price_diff = average_price_1mo - current_price
                price_diff_percentage = (price_diff / average_price_1mo) * 100

                # Selection criteria
                if 1 <= price_diff_percentage <= 15 and 0.05 <= ewma_volatility_5d <= 5:
                    selected_stocks.append({
                        'ticker': ticker,
                        'current_price': current_price,
                        'average_price_1mo': average_price_1mo,
                        'price_diff_percentage': price_diff_percentage,
                        'ewma_volatility_5d': ewma_volatility_5d,
                        'ewma_volatility_1mo': ewma_volatility_1mo
                    })
                    logging.info(f"Ticker: {ticker}, Current Price: {current_price}, 1-Month Average: {average_price_1mo}, Difference (%): {price_diff_percentage:.2f}%, EWMA Volatility (5d): {ewma_volatility_5d}, EWMA Volatility (1mo): {ewma_volatility_1mo}")
                time.sleep(0.05)  # Reduce sleep time to speed up processing
            except ValueError as e:
                logging.warning(e)
            except Exception as e:
                logging.error(f"Unexpected error while processing {ticker}: {e}")
                traceback.print_exc()
        return selected_stocks

if __name__ == "__main__":
    polygon_api_key = "X515twqBz3meUpKG9Q1RL1g90K_gMjPf"  # Replace with your Polygon.io API key
    polygon_api = PolygonAPI(polygon_api_key)

    try:
        top_150_tickers = polygon_api.get_top_150_highly_traded_tickers()
        selected_stocks = polygon_api.find_stocks_with_criteria(top_150_tickers)
    except PermissionError as e:
        logging.critical(f"Critical permission error occurred: {e}")
    except Exception as e:
        logging.critical(f"Critical error occurred: {e}")
