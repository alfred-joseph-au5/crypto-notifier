import sys

# try:
#     import Tkinter as tk
# except ImportError:
import tkinter as tk

# try:
#     import ttk
#     py3 = False
# except ImportError:
#     import tkinter.ttk as ttk
#     py3 = True
import gui
from coin import coin_full as coin
from currency import currency_code as currency

# Setting up variables used on the GUI
def set_Tk_var():
    global currency_opt
    currency_opt = currency
    global coin_opt
    coin_opt = coin
    global dd_currency
    dd_currency = tk.StringVar()
    global dd_coin
    dd_coin = tk.StringVar()
    global var_cb_limit
    var_cb_limit = tk.IntVar()
    global var_cb_notify
    var_cb_notify = tk.IntVar()
    global var_cb_twitter
    var_cb_twitter = tk.IntVar()
    global var_cb_email
    var_cb_email = tk.IntVar()
    global var_cb_text_msg
    var_cb_text_msg = tk.IntVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    gui.vp_start_gui()

