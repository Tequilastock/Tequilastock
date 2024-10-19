document.getElementById('stock-selection-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const tickers = document.getElementById('tickers').value;
    fetch(`/find-best-stocks?tickers=${tickers}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').innerHTML = `<p>Best Stocks: ${data.best_stocks.join(', ')}</p>`;
        })
        .catch(error => console.error('Error:', error));
});
