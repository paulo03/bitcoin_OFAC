#!/Users/paulo/Documents/python_venv/venv1/bin/python

import pandas as pd
import tkinter as tk
import sys
from tkinter.ttk import *
import requests
import datetime

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # SDN List Scrape for Crypto Addresses
        self.SDN = tk.Button(self, fg="orange")
        self.SDN["text"] = "SDN"
        self.SDN["command"] = self.check_list
        self.SDN.grid(row = 0, column = 0, ipadx = 5, ipady = 5,
                      padx = 5, pady = 5)
        # QUIT
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 1, column = 0, ipadx = 5, ipady = 5,
                       padx = 5, pady = 5)
        # LABEL
        self.label1 = tk.Label(self)
        txt1 = "CHECK SDN LIST FOR CRYPTO ADDRESSES"
        self.label1["text"] = txt1
        self.label1.grid(row = 0, column = 1)
        txt2 = "NOTE: Currently only BTC (XBT) and LTC are checked"
        self.label2 = tk.Label(self)
        self.label2["text"] = txt2
        self.label2.grid(row = 1, column = 1)
        # TEXT DISPLAY
        self.text = tk.Text(self, wrap="word")
        self.text.grid(row = 3, column = 1,
                       ipadx = 50, ipady = 100,
                       padx = 10, pady = 10)
        self.text.tag_configure("stderr", foreground="#b22222")

        sys.stdout = TextRedirector(self.text, "stdout")
        # sys.stderr = TextRedirector(self.text, "stderr")
        
    def check_list(self):
        '''
563. What is the structure of a digital currency address on OFAC’s SDN List?

Digital currency addresses listed on the SDN List include their unique
alphanumeric identifier (up to 256 characters) and identify the digital
currency to which the address corresponds (e.g., Bitcoin (XBT), Ethereum
(ETH), Litecoin (LTC), Neo (NEO), Dash (DASH), Ripple (XRP), Iota (MIOTA),
Monero (XMR), and Petro (PTR)). Each digital currency address listed on the SDN
list will have its own field: the structure will always begin with “Digital
Currency Address”, followed by a dash and the digital currency’s symbol 
(e.g., “Digital Currency Address - XBT”, “Digital Currency Address - ETH”).
This information is followed by the unique alphanumeric identifier of the
specific address. [06-06-2018]
        '''

        r = requests.get('https://www.treasury.gov/ofac/downloads/sdn.csv')
        print(r.url + '\n')

        string = r.text
        # The coin names/abbreviations on the SDN List
        xbt_string = 'xbt'
        # eth_string = '0x'
        ltc_string = 'ltc'

        address_list = []
        # Accumulation list is outside of the function
        # and passed in so that it's not overwritten

        find_coin_address(xbt_string, string, address_list)
        find_coin_address(ltc_string, string, address_list)

        l = []
        # a list that will take the string list (address_list) and split it
        for item in address_list:
            a, b = str(item).split()
            l.append([a, b])

        df = pd.DataFrame(l, columns=['Coin', 'Address'])

        print(len(df[df['Coin'] == 'XBT']),
                         "Bitcoin addresses on the SDN List")
        print(len(df[df['Coin'] == 'LTC']),
                         "Litecoin addresses on the SDN List")

        date = str(datetime.date.today())
        csv = 'OFAC_BTC_ADDRESS_CHECK_' + date + '.csv'
        df_csv = df.to_csv(csv, index=False)
        
def find_coin_address(item, string, address_list):
    if item.lower() in string:
        location = string.find(str(item.lower()))
        sys.stdout.write(str(string[location:(location + 38)]) + '\n')
        address_list.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_coin_address(item, string, address_list)
    elif item.upper() in string:
        location = string.find(str(item.upper()))
        sys.stdout.write(str(string[location:(location + 38)]) + '\n')
        address_list.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_coin_address(item, string, address_list)
    elif item.capitalize() in string:
        location = string.find(str(item.capitalize()))
        sys.stdout.write(str(string[location:(location + 38)]) + '\n')
        address_list.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_coin_address(item, string, address_list)
    else:
        sys.stdout.write('\n')
        
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        
root = tk.Tk()
root_top = tk.Frame(root)
root_bottom = tk.Frame(root)
app = Application(master=root)
app.mainloop()
