import requests

API_KEY = "<X515twqBz3meUpKG9Q1RL1g90K_gMjPf>"

class PolygonAPI:
    BASE_URL = "https://api.polygon.io/v2"

    @staticmethod
    def get_stock_data(ticker):
        url = f"{PolygonAPI.BASE_URL}/aggs/ticker/{ticker}/prev?apiKey={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch stock data")