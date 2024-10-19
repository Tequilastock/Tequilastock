TequilaStock LLC - Leprechaun 1.0

Welcome to TequilaStock, the home of the automated trading AI, Leprechaun 1.0. This repository contains all the code and resources you need to get started with TequilaStock's automated trading bot that aims for small, consistent gains in the stock market. Whether you're an experienced trader or just getting started, Leprechaun 1.0 is designed to make the process of investing simple, effective, and hands-free.

Project Overview

TequilaStock LLC is dedicated to making advanced trading technology accessible to everyone. Our AI-driven solution, Leprechaun 1.0, helps automate your trading while focusing on small, consistent gains every day the market is open. The goal is to empower individuals by leveraging automated trading without the need for constant monitoring or deep market expertise.

TequilaStock aims to:

Automate trading using Interactive Brokers and Polygon API.

Provide easy access through a cloud interface where users can log in to their accounts and let Leprechaun 1.0 do the rest.

Generate consistent returns, targeting small, achievable daily gains to compound over time.

Key Features

Interactive Brokers Integration: Connects directly to IB Gateway to execute trades automatically.

Polygon API Integration: Uses market data to determine the best opportunities and execute trades based on real-time analysis.

User-Friendly Interface: Log in, link your accounts, and start investing effortlessly. Get daily reports on how your portfolio is performing.

Cloud-Based Setup: The system operates in the cloud, meaning there's no need to keep any software running on your own computer.

Getting Started

Prerequisites

Interactive Brokers Account: You need an active account with Interactive Brokers for Leprechaun 1.0 to trade on your behalf.

Polygon API Key: Sign up at Polygon.io to obtain an API key for fetching market data.

Installation

Clone the repository to your local machine:

git clone https://github.com/TequilaStock/tequilastock.git
cd tequilastock

Install dependencies:

pip install -r requirements.txt

Update the configuration file with your Interactive Brokers API credentials and Polygon API Key.

Running the Bot

Start IB Gateway: Before running the bot, make sure your Interactive Brokers Gateway is open and API access is enabled.

Run the Bot:

python3 leprechaun1.0/modules/tablelimits.py

This script will use Polygon API data and Interactive Brokers to find the best stocks to bet on, executing trades based on strike price options and managing funds effectively.

Project Components

1. Polygon API Module (polygonapi.py)

This module is responsible for interacting with Polygon.io to get the top 150 highly traded stocks. It calculates metrics like EWMA volatility, average price, and current price difference to determine the most promising stocks.

2. IB Gateway Module (ibgateway.py)

Handles the connection to the Interactive Brokers Gateway, allowing the bot to place trades based on the selected stock data.

3. Table Limits Module (tablelimits.py)

This module finds the best stocks for trading based on the data provided by polygonapi.py. It calculates strike prices, buys premiums, and manages trades according to the balance available, mimicking the actions of Deal or No Deal Leprechaun and Cashier Leprechaun.

Usage

Once all modules are running, Leprechaun 1.0 will continuously analyze market data, execute trades, and monitor your portfolio.

You'll receive daily reports to keep you updated on your progress.

Supporting TequilaStock

We aim to bring advanced financial technology to everyone. You can support us by purchasing a "I Make 1% a Day" bracelet from tequilastock.com to help promote the message of consistent financial growth.

License

This project is released under the TequilaStock LLC License. Usage of Leprechaun 1.0 is free for educa python3 -m http.server 8000tional purposes under the terms defined in the license.

Contact

If you have questions, need support, or would like to collaborate, reach out to us at support@tequilastock.com.

Happy trading, and may the Leprechauns bring you luck!

