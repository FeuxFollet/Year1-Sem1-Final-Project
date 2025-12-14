#-----------------------------------------------------------------------------#
# Modules

import tkinter as tk
import requests
import numpy as np
import matplotlib

# Components Import

from components.toggleable_ticker import ToggleableTickerApp
from components.candlestick_chart import Candlestickchart

#-----------------------------------------------------------------------------#
# Creating Main Window

root = tk.Tk()
root.title("Project ORBIT")
root.geometry("960x540")
root.config(bg="#393939")

#-----------------------------------------------------------------------------#
# Top welcome message

welcomemsg = tk.Label(
    root,
    text="Welcome to ORBIT Cryptotracker",
    font=("Helvetica", 12, "bold"),
    foreground="#00bf63",
    background="#393939"
)
welcomemsg.pack(pady=(10, 10))

#-----------------------------------------------------------------------------#
# Toggler and dashboard frame

toggler_and_dashboard = tk.Frame(root, bg="#393939")
toggler_and_dashboard.pack(fill="both", expand=True)

#-----------------------------------------------------------------------------#
# Toggler frame (for interactive currency toggler)

# Frame for the toggler
grid_frame = tk.Frame(toggler_and_dashboard, background="#393939")
grid_frame.pack(side="left", fill="y", padx=15)

# 3 Column grid
grid_frame.columnconfigure(0, weight=1)  # Display currency name
grid_frame.columnconfigure(1, weight=1)  # Price toggle button
grid_frame.columnconfigure(2, weight=1)  # Detailed view button

togglerlabel = tk.Label(
    grid_frame,
    text="Currency toggle",
    font=("Helvetica", 12, "bold"),
    foreground="#00bf63",
    background="#393939"
)
togglerlabel.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

class CurrencyRow:
    '''Reusable interactive currency toggler row'''

    def __init__(self, parent, row, name):
        # Currency label
        self.displaytext = tk.Label(
            parent,
            text=name,
            font=("Helvetica", 10, "bold"),
            borderwidth=3,
            relief=tk.SUNKEN,
            background="#00bf63",
            foreground="#01600a",
            padx=10
        )

        # Toggle price button
        self.btn_left = tk.Button(
            parent,
            text="Toggle price",
            font=("Helvetica", 10),
            background="#606060",
            foreground="White",
            activebackground="#323232",
            activeforeground="Grey",
            padx=10,
        )

        # Show graph button
        self.btn_right = tk.Button(
            parent,
            text="Detailed display",
            font=("Helvetica", 10),
            background="#606060",
            foreground="White",
            activebackground="#323232",
            activeforeground="Grey",
            padx=10
        )

        # Grid all the components
        self.displaytext.grid(row=row, column=0, sticky="nsew", padx=10, pady=5)
        self.btn_left.grid(row=row, column=1, sticky="nsew", padx=10, pady=5)
        self.btn_right.grid(row=row, column=2, sticky="nsew", padx=10, pady=5)
        self.is_visible = False


    def set_price_toggle(self, command):
        '''Set the command for the price toggle button'''
        self.btn_left.config(command=command)


    def set_detailed_view(self, command):
        '''Set the command for the detailed view button'''
        self.btn_right.config(command=command)


# Create all the interactive currency toggler
BTCtoggle = CurrencyRow(grid_frame, row=1, name="Bitcoin (BTC)")
ETHtoggle = CurrencyRow(grid_frame, row=2, name="Ether (ETH)")
SOLtoggle = CurrencyRow(grid_frame, row=3, name="Solana (SOL)")
DOGEtoggle = CurrencyRow(grid_frame, row=4, name="Dogecoin (DOGE)")
SHIBtoggle = CurrencyRow(grid_frame, row=5, name="Shiba inu (SHIB)")

#-----------------------------------------------------------------------------#
# Dashboard frame

dashboard = tk.Frame(toggler_and_dashboard, background="#313131")
dashboard.pack(side="right", fill="both", expand=True)

#-----------------------------------------------------------------------------#
# Price dashboard

# Frame for the price dashboard
pricedashboard = tk.Frame(dashboard, background="#313131")
pricedashboard.pack(fill="x", padx=15)

dashboardlabel1 = tk.Label(
    pricedashboard,
    text="Price Dashboard",
    font=("Helvetica", 12, "bold"),
    foreground="#00bf63",
    background="#313131"
)
dashboardlabel1.pack(pady=(10, 10), padx=(20,0), anchor="w")

# Create price ticker
dashboard_app = ToggleableTickerApp(pricedashboard, root)

# Load up preferences
dashboard_app.ensure_file_valid()
dashboard_app.set_preference()

# Set price toggle button's command
BTCtoggle.set_price_toggle(dashboard_app.toggle_btc)
ETHtoggle.set_price_toggle(dashboard_app.toggle_eth)
SOLtoggle.set_price_toggle(dashboard_app.toggle_sol)
DOGEtoggle.set_price_toggle(dashboard_app.toggle_doge)
SHIBtoggle.set_price_toggle(dashboard_app.toggle_shib)

#-----------------------------------------------------------------------------#
# Detailed Dashboard

detaileddashboard = tk.Frame(dashboard, background="#313131")
detaileddashboard.pack(fill="both", padx=15)

dashboardlabel2 = tk.Label(
    pricedashboard,
    text="Currently showing [currency] detailed data",
    font=("Helvetica", 14, "bold"),
    foreground="#00bf63",
    background="#313131"
)
dashboardlabel2.pack(pady=(30, 10), padx=(20,0), anchor="w")

# Frame for the candlestick
chart_frame = tk.Frame(detaileddashboard, bg="#313131")
chart_frame.pack(side="left", fill="both", expand=True)

# Create the Candlestick chart and start it
candlestick = Candlestickchart("BTCUSDT", dashboardlabel2, "BTC/USDT")
candlestick.initialize_graph(chart_frame)
candlestick.start()


# Start main loop
root.mainloop()