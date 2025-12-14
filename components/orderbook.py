#-----------------------------------------------------------------------------#
# Modules

import tkinter as tk
import requests

#-----------------------------------------------------------------------------#


class OrderBookPanel:
    '''OrderBook class'''

    def __init__(self, parent, currency="BTCUSDT"):
        self.parent = parent
        self.currency = currency
        self.after_id = None
        self.is_active = False

        self._build_ui()
        self.start()


    def _build_ui(self):
        '''Build the OrderBook GUI'''
        self.container = tk.Frame(
            self.parent,
            bg="#1e1e1e"
        )
        self.container.pack(fill="y", expand=False)

        # HEADER
        header = tk.Frame(self.container, bg="#606060", relief="raised", bd=2)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Order Book Snapshot",
            bg="#606060",
            fg="white",
            font=("Helvetica", 11, "bold")
        ).pack(side="left", padx=8, pady=6)

        # SIDE TITLES
        self.side_titles = tk.Frame(self.container, bg="#1e1e1e")
        self.side_titles.pack(fill="x", pady=(5, 0))

        # Column layout
        # (This is only added so the side titles align with data frame)
        self.side_titles.columnconfigure(0, weight=1)
        self.side_titles.columnconfigure(1, weight=1)
        self.side_titles.columnconfigure(2, weight=0)
        self.side_titles.columnconfigure(3, weight=1)
        self.side_titles.columnconfigure(4, weight=1)

        # BIDs Title
        tk.Label(
            self.side_titles,
            text="BIDS (Buys)",
            fg="#00bf63",
            bg="#1e1e1e",
            font=("Helvetica", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=6)

        # ASKs Title
        tk.Label(
            self.side_titles,
            text="ASKS (Sells)",
            fg="#ff4d4d",
            bg="#1e1e1e",
            font=("Helvetica", 10, "bold")
        ).grid(row=0, column=3, columnspan=2, sticky="w", padx=6)


        # DATA FRAME
        self.data_frame = tk.Frame(self.container, bg="#1e1e1e")
        self.data_frame.pack(fill="both", expand=True, pady=4)

        # Column layout
        self.data_frame.columnconfigure(0, weight=1)  # BIDs price
        self.data_frame.columnconfigure(1, weight=1)  # BIDs quantity
        self.data_frame.columnconfigure(2, weight=0)  # Divider
        self.data_frame.columnconfigure(3, weight=1)  # ASKs price
        self.data_frame.columnconfigure(4, weight=1)  # ASKs quantity

        # COLUMN HEADERS
        header_style = {
            "bg": "#1e1e1e",
            "fg": "#a0a6ad",
            "font": ("Helvetica", 10, "bold")
        }

        # BIDs price & quantities header
        tk.Label(self.data_frame, text="Price", **header_style)\
            .grid(row=0, column=0, sticky="w", padx=6)
        tk.Label(self.data_frame, text="Quantity", **header_style)\
            .grid(row=0, column=1, sticky="e", padx=6)

        # ASKs price & quantity header
        tk.Label(self.data_frame, text="Price", **header_style)\
            .grid(row=0, column=3, sticky="w", padx=6)
        tk.Label(self.data_frame, text="Quantity", **header_style)\
            .grid(row=0, column=4, sticky="e", padx=6)

        # Create the vertical divider
        divider = tk.Frame(self.data_frame, bg="grey", width=3)
        divider.grid(row=0, column=2, rowspan=11, sticky="ns", padx=4)

        # Order rows
        self.bid_price_labels = []
        self.bid_qty_labels = []
        self.ask_price_labels = []
        self.ask_qty_labels = []

        # Top 10 BIDs and ASKs
        for i in range(10):
            r = i + 1

            bp = tk.Label(self.data_frame, bg="#1e1e1e", fg="#00bf63",
                          font=("Consolas", 9), anchor="w")
            bq = tk.Label(self.data_frame, bg="#1e1e1e", fg="#cfd8dc",
                          font=("Consolas", 9), anchor="e")

            ap = tk.Label(self.data_frame, bg="#1e1e1e", fg="#ff4d4d",
                          font=("Consolas", 9), anchor="w")
            aq = tk.Label(self.data_frame, bg="#1e1e1e", fg="#cfd8dc",
                          font=("Consolas", 9), anchor="e")

            bp.grid(row=r, column=0, sticky="w", padx=6)
            bq.grid(row=r, column=1, sticky="e", padx=6)
            ap.grid(row=r, column=3, sticky="w", padx=6)
            aq.grid(row=r, column=4, sticky="e", padx=6)

            self.bid_price_labels.append(bp)
            self.bid_qty_labels.append(bq)
            self.ask_price_labels.append(ap)
            self.ask_qty_labels.append(aq)


    def fetch_orderbook(self):
        '''Fetch data'''
        url = "https://api.binance.com/api/v3/depth"
        params = {"symbol": self.currency, "limit": 10}
        response = requests.get(url, params=params, timeout=5)
        return response.json()


    def start(self):
        '''Enable live updating, also for debugging'''
        if self.is_active:
            return

        self.is_active = True
        # Print out status
        print(f"[OrderBook] Connected ({self.currency})")
        self.update_orderbook()


    def stop(self):
        '''Stops live updating, also for debugging'''
        self.is_active = False

        if self.after_id:
            self.parent.after_cancel(self.after_id)
            self.after_id = None
        # Print out status
        print("[OrderBook] Disconnected")


    def update_orderbook(self):
        '''Core update loop'''
        if not self.is_active:
            return

        if self.after_id:
            self.parent.after_cancel(self.after_id)

        try:
            data = self.fetch_orderbook()
            bids = data["bids"][:10]
            asks = data["asks"][:10]
        except Exception:
            self.after_id = self.parent.after(3000, self.update_orderbook)
            return

        for i in range(10):
            bid_price, bid_qty = bids[i]
            ask_price, ask_qty = asks[i]

            self.bid_price_labels[i].config(text=f"{float(bid_price):,.2f}")
            self.bid_qty_labels[i].config(text=f"{float(bid_qty):.6f}")

            self.ask_price_labels[i].config(text=f"{float(ask_price):,.2f}")
            self.ask_qty_labels[i].config(text=f"{float(ask_qty):.6f}")

        self.after_id = self.parent.after(3000, self.update_orderbook)


    def switch_currency(self, new_currency):
        '''Switch orderbook to another currency (used for button command)'''
        self.stop()
        self.currency = new_currency
        self.start()