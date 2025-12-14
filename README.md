# Y1S1 Final Project : ORBIT Cryptotracker

This is a simple cryptocurrency tracker app that displays informations such as price, candlestick chart, and orderbook of different cryptocurrencies.

## Features

 - Displays price, candlestick chart, and orderbook information.
 - Toggle price button to toggle what price tickers are visible.
 - Detailed display button to display candlestick chart and orderbook on the dashboard.
 - Memorizes which price tickers were active when the application was closed and restores them on the next launch.

 ## Project Structure
```bash
project_orbit/
├── main.py                     # Entry point
├── components/
│   ├── candlestick_chart.py    # Candlestickchart class
│   ├── orderbook.py            # OrderBookPanel class
│   ├── price_memory.txt        # File for saving preference
│   └── toggleable_ticker.py    # ToggleableTickerApp class
├── demonstrations/
│   ├── app_demonstration.mp4   # Demonstration video
│   └── preview.py              # UI preview image
└── requirements.txt            # Dependencies

```

## Running the program

To run the program, execute `main.py`:

```bash
python main.py