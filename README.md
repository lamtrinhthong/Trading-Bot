# MT5 Trading Bot

A Python-based trading bot for MetaTrader 5 (MT5) that implements various trading strategies, such as the Moving Average Crossover strategy.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project provides a framework for building and running trading bots using MetaTrader 5. The bot can be configured to use different trading strategies and is designed to be modular, making it easy to extend and customize.

## Features

- Connect to MetaTrader 5 account
- Implement different trading strategies
- Fetch market data
- Execute buy/sell orders
- Log trading activities
- Easy configuration using JSON files

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/mt5-trading-bot.git
    cd mt5-trading-bot
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Edit the `config/config.json` file to set up your trading bot's configuration. Here is an example configuration:

```json
{
  "account": 12345678,
  "password": "your_password",
  "server": "your_server",
  "symbol": "EURUSD",
  "timeframe": "M1",
  "lot_size": 0.1,
  "short_window": 50,
  "long_window": 200
}
