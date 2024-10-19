from ib_insync import IB, Contract, Order
import time
import logging
import traceback
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IBGateway:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1, max_retries=5):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.max_retries = max_retries
        self.ib = IB()
        self.connected = False

    def connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                logging.info(f"Attempting to connect to IB Gateway at {self.host}:{self.port} with client ID {self.client_id}.")
                self.ib.connect(self.host, self.port, clientId=self.client_id)
                self.connected = True
                logging.info("Successfully connected to IB Gateway.")
                return
            except Exception as e:
                retries += 1
                logging.error(f"Failed to connect to IB Gateway. Attempt {retries}/{self.max_retries}. Error: {e}")
                if retries >= self.max_retries:
                    logging.critical("Max retries reached. Could not connect to IB Gateway.")
                    raise ConnectionError("Could not connect to IB Gateway after maximum retries.")
                time.sleep(5)  # Delay before retrying

    def disconnect(self):
        if self.ib.isConnected():
            self.ib.disconnect()
            logging.info("Disconnected from IB Gateway.")
            self.connected = False

    def maintain_connection(self):
        while True:
            try:
                if not self.connected or not self.ib.isConnected():
                    logging.warning("Lost connection to IB Gateway. Reconnecting...")
                    self.connect()
                # Sleep for 10 seconds before checking the connection again
                time.sleep(10)
            except KeyboardInterrupt:
                logging.info("Keyboard interrupt received. Disconnecting from IB Gateway.")
                self.disconnect()
                sys.exit(0)
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                traceback.print_exc()
                time.sleep(5)

    def place_order(self, contract: Contract, order: Order):
        try:
            if not self.connected or not self.ib.isConnected():
                logging.warning("Not connected to IB Gateway. Attempting to reconnect...")
                self.connect()
            trade = self.ib.placeOrder(contract, order)
            logging.info(f"Placed order: {order}. Status: {trade.orderStatus.status}")
            return trade
        except Exception as e:
            logging.error(f"Failed to place order. Error: {e}")
            traceback.print_exc()
            return None

    def get_account_summary(self):
        try:
            if not self.connected or not self.ib.isConnected():
                logging.warning("Not connected to IB Gateway. Attempting to reconnect...")
                self.connect()
            summary = self.ib.accountSummary()
            logging.info("Account summary fetched successfully.")
            return summary
        except Exception as e:
            logging.error(f"Failed to fetch account summary. Error: {e}")
            traceback.print_exc()
            return None

if __name__ == "__main__":
    ib_gateway = IBGateway()
    try:
        ib_gateway.connect()
        ib_gateway.maintain_connection()
    except Exception as e:
        logging.critical(f"Critical error: {e}")
        ib_gateway.disconnect()