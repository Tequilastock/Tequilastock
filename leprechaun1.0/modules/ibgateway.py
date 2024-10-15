from ibapi.client import eClient
from ibapi.wrapper import eWrapper

class IBGateway(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def connect_gateway(self, host='127.0.0.1', port=7497, clientId=1):
        self.connect(host, port, clientId)
        self.run()

    def error(self, reqId, errorCode, errorString):
        print(f"Error {reqId}: {errorCode} - {errorString}")