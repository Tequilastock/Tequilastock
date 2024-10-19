from flask import Flask, request, jsonify, render_template
from modules.stockselection import StockSelectionLeprechaun

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find-best-stocks', methods=['GET'])
def find_best_stocks():
    tickers = request.args.get('tickers').split(',')
    leprechaun = StockSelectionLeprechaun(tickers)
    best_stocks = leprechaun.find_best_stocks()
    return jsonify({"best_stocks": best_stocks})

if __name__ == "__main__":
    app.run(debug=True)

