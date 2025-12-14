#-----------------------------------------------------------------------------#
# Modules

import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading
from pathlib import Path

#-----------------------------------------------------------------------------#


class CryptoTicker:
    '''Reusable ticker component for any cryptocurrency'''

    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws = None

        # Create UI
        self.frame = tk.Frame(parent, relief="sunken", borderwidth=1,
                               background="#606060")

        # Title
        ttk.Label(self.frame, text=display_name,
                  font=("Helvetica", 16, "bold"), background="#606060",
                  foreground="White").pack(pady=10)

        # Price
        self.price_label = tk.Label(self.frame, text="--,---",
                                    font=("Helvetica", 28, "bold"),
                                    background="#606060",
                                    foreground="White")
        self.price_label.pack()

        # Change
        self.change_label = ttk.Label(self.frame, text="--",
                                      font=("Helvetica", 12),
                                      background="#606060",
                                      foreground="White")
        self.change_label.pack(pady=10)


    def start(self):
        '''Start websocket connection'''
        if self.is_active:
            return

        self.is_active = True
        ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"

        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=lambda ws, err: print(f"{(self.symbol).upper()} Error: {err}"),
            on_close=lambda ws, s, m: print(f"{(self.symbol).upper()} Closed"),
            on_open=lambda ws: print(f"{(self.symbol).upper()} Connected")
        )

        threading.Thread(target=self.ws.run_forever, daemon=True).start()


    def stop(self):
        '''Stop websocket connection'''
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None


    def on_message(self, ws, message):
        '''Handle price updates'''
        if not self.is_active:
            return

        data = json.loads(message)
        price = float(data['c'])
        change = float(data['p'])
        percent = float(data['P'])

        # Schedule GUI update on main thread
        self.parent.after(0, self.update_display, price, change, percent)


    def update_display(self, price, change, percent):
        '''Update the ticker display'''
        if not self.is_active:
            return

        color = "#00bf63" if change >= 0 else "red"
        self.price_label.config(text=f"{price:,.2f}", fg=color)

        sign = "+" if change >= 0 else ""
        self.change_label.config(
            text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",
            foreground=color
        )


    def pack(self, **kwargs):
        '''Allows placement of ticker'''
        self.frame.pack(**kwargs)


    def pack_forget(self):
        '''Hide the ticker'''
        self.frame.pack_forget()


class ToggleableTickerApp:
    def __init__(self, frame_parent, root):
        self.root = root
        self.frame_parent = frame_parent
        # self.root.title("Crypto Dashboard with Toggle")
        # self.root.geometry("1000x400")
        self.sol_visible = False

        # Ticker panel
        self.ticker_frame = tk.Frame(frame_parent, background="#323232")
        self.ticker_frame.pack(fill=tk.BOTH, expand=True)

        # Create tickers
        self.btc_ticker = CryptoTicker(self.ticker_frame, "btcusdt", "BTC/USDT")
        self.eth_ticker = CryptoTicker(self.ticker_frame, "ethusdt", "ETH/USDT")
        self.sol_ticker = CryptoTicker(self.ticker_frame, "solusdt", "SOL/USDT")
        self.doge_ticker = CryptoTicker(self.ticker_frame, "dogeusdt", "DOGE/USDT")
        self.shib_ticker = CryptoTicker(self.ticker_frame, "shibusdt", "SHIB/USDT")

        # Set visible state boolean
        self.btc_visible = False
        self.eth_visible = False
        self.sol_visible = False
        self.doge_visible = False
        self.shib_visible = False

    def set_preference(self):
        '''Get data from price_memory.txt and open the tickers
        that were open since last closed'''
        with open("../price_memory.txt", "r") as f:
            preference = f.readlines()

            # For cases when user accidentally deletes the content of
            # price_memory.txt
            if len(preference) == 0:
                self.btc_visible = True
                self.btc_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
                self.btc_ticker.start()

            else:
                # Read the values from .txt file
                values = [line.strip().split(" = ")[1] for line in preference]

                # Set the attribute value to the ones stored in the .txt
                self.btc_visible = values[0] == "True"
                self.eth_visible = values[1] == "True"
                self.sol_visible = values[2] == "True"
                self.doge_visible = values[3] == "True"
                self.shib_visible = values[4] == "True"

                # Start up the price tickers
                if self.btc_visible:
                    self.btc_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
                    self.btc_ticker.start()
                if self.eth_visible:
                    self.eth_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
                    self.eth_ticker.start()
                if self.sol_visible:
                    self.sol_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
                    self.sol_ticker.start()
                if self.doge_visible:
                    self.doge_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
                    self.doge_ticker.start()
                if self.shib_visible:
                    self.shib_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
                    self.shib_ticker.start()


    def ensure_file_valid(self):
        '''Ensure price_memory.txt exists'''
        path = Path("../price_memory.txt")

        # Create the file for first time users
        if not path.exists():
            path.write_text(
                "btc_visible = True\n"
                "eth_visible = False\n"
                "sol_visible = False\n"
                "doge_visible = False\n"
                "shib_visible = False\n"
            )


    def toggle_btc(self):
        '''Show or hide BTC ticker'''
        if self.btc_visible:
            # Hide BTC
            self.btc_ticker.stop()
            self.btc_ticker.pack_forget()
            self.btc_visible = False
        else:
            # Show BTC
            self.btc_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.btc_ticker.start()
            self.btc_visible = True


    def toggle_eth(self):
        '''Show or hide ETH ticker'''
        if self.eth_visible:
            # Hide ETH
            self.eth_ticker.stop()
            self.eth_ticker.pack_forget()
            self.eth_visible = False
        else:
            # Show ETH
            self.eth_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.eth_ticker.start()
            self.eth_visible = True


    def toggle_sol(self):
        '''Show or hide SOL ticker'''
        if self.sol_visible:
            # Hide SOL
            self.sol_ticker.stop()
            self.sol_ticker.pack_forget()
            self.sol_visible = False
        else:
            # Show SOL
            self.sol_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.sol_ticker.start()
            self.sol_visible = True


    def toggle_doge(self):
        '''Show or hide DOGE ticker'''
        if self.doge_visible:
            # Hide DOGE
            self.doge_ticker.stop()
            self.doge_ticker.pack_forget()
            self.doge_visible = False
        else:
            # Show SOL
            self.doge_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.doge_ticker.start()
            self.doge_visible = True


    def toggle_shib(self):
        '''Show or hide SHIB ticker'''
        if self.shib_visible:
            # Hide SHIB
            self.shib_ticker.stop()
            self.shib_ticker.pack_forget()
            self.shib_visible = False
        else:
            # Show SHIB
            self.shib_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.shib_ticker.start()
            self.shib_visible = True


    def on_closing(self):
        """Clean up when closing."""
        with open("../price_memory.txt", "w") as f:
            f.write(f"btc_visible = {self.btc_visible}\n"
                    f"eth_visible = {self.eth_visible}\n"
                    f"sol_visible = {self.sol_visible}\n"
                    f"doge_visible = {self.doge_visible}\n"
                    f"shib_visible = {self.shib_visible}")
        self.btc_ticker.stop()
        self.eth_ticker.stop()
        self.sol_ticker.stop()
        self.doge_ticker.stop()
        self.shib_ticker.stop()
        self.root.destroy()

