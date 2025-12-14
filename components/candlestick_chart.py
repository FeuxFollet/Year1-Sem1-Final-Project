#-----------------------------------------------------------------------------#
# Modules

import tkinter as tk
import datetime
import requests
import numpy as np

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches

#-----------------------------------------------------------------------------#


class Candlestickchart:
    '''Candlestick Chart class'''

    def __init__(self, initial_currency, label, displaytext):
        self.currency = initial_currency
        # Display text is for appearance purposes only
        self.displaytext = displaytext
        self.label = label

        self.after_id = None
        self.is_active = False

        self.fig = None
        self.ax_price = None
        self.ax_volume = None
        self.canvas = None
        self.parent_frame = None


    def initialize_graph(self, parent_frame):
        '''Build the graph UI'''
        self.parent_frame = parent_frame
        self.label.configure(text=f"Showing {self.displaytext}")

        # Create figure
        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.fig.patch.set_facecolor("#313131")

        # Subplots
        self.ax_price = self.fig.add_subplot(2, 1, 1)
        self.ax_volume = self.fig.add_subplot(2, 1, 2, sharex=self.ax_price)

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initial draw
        self.update_graph()


    def timestamp_format(self, timestamp_ms):
        '''Convert Binance millisecond timestamp into Hours:Minutes format'''
        return datetime.datetime.fromtimestamp(timestamp_ms / 1000).strftime("%H:%M")


    def update_graph(self):
        '''Core update loop'''
        # Stop if inactive
        if not self.is_active:
            return

        # Cancel previous timer (avoid bugs)
        if self.after_id:
            self.parent_frame.after_cancel(self.after_id)

        # Fetch data
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": self.currency,
            "interval": "1h",
            "limit": 24
        }

        try:
            response = requests.get(url, params=params, timeout=5).json()
        except Exception:
            self.after_id = self.parent_frame.after(5000, self.update_graph)
            return

        timestamps = np.array([int(c[0]) for c in response])
        opens = np.array([float(c[1]) for c in response])
        highs = np.array([float(c[2]) for c in response])
        lows = np.array([float(c[3]) for c in response])
        closes = np.array([float(c[4]) for c in response])
        volumes = np.array([float(c[5]) for c in response])

        time_labels = [self.timestamp_format(t) for t in timestamps]

        # PRICE AXIS
        self.ax_price.clear()
        self.ax_price.set_facecolor("#1e1e1e")
        self.ax_price.set_title(f"{self.displaytext} 1H Candlestick", color="white")
        self.ax_price.set_ylabel("Price", color="white")

        for i in range(len(opens)):
            color = "#00bf63" if closes[i] >= opens[i] else "#ff4d4d"

            self.ax_price.plot([i, i], [lows[i], highs[i]], color=color, linewidth=1)
            self.ax_price.add_patch(
                matplotlib.patches.Rectangle(
                    (i - 0.3, min(opens[i], closes[i])),
                    0.6,
                    abs(closes[i] - opens[i]),
                    color=color
                )
            )

        self.ax_price.tick_params(axis="x", labelbottom=False, colors="white")
        self.ax_price.tick_params(axis="y", colors="white")

        # VOLUME AXIS
        self.ax_volume.clear()
        self.ax_volume.set_facecolor("#1e1e1e")
        self.ax_volume.bar(range(len(volumes)), volumes, color="#5c7cfa", width=0.6)
        self.ax_volume.set_ylabel("Volume", color="white")

        self.ax_volume.set_xticks(range(len(time_labels)))
        self.ax_volume.set_xticklabels(time_labels, rotation=45, ha="right", color="white")
        self.ax_volume.tick_params(axis="y", colors="white")

        # Style
        for ax in (self.ax_price, self.ax_volume):
            ax.grid(True, linestyle="--", alpha=0.15)
            for spine in ax.spines.values():
                spine.set_visible(False)

        self.canvas.draw_idle()

        # Schedule next update
        self.after_id = self.parent_frame.after(5000, self.update_graph)


    def start(self):
        '''Enable live updating, also for debugging'''
        if self.is_active:
            return

        self.is_active = True
        # Print out the status
        print(f"[Candlestick] Connected ({self.currency})")
        self.update_graph()


    def stop(self):
        '''Stops live updating, also for debugging'''
        self.is_active = False

        if self.after_id:
            self.parent_frame.after_cancel(self.after_id)
            self.after_id = None
        # Print out the status
        print("[Candlestick] Disconnected")


    def switch_graph(self, new_currency, new_displaytext):
        '''Switch graph to another currency (used for button command)'''
        self.stop()
        self.currency = new_currency
        self.displaytext = new_displaytext
        self.label.configure(text=f"Showing {self.displaytext}")
        self.start()

