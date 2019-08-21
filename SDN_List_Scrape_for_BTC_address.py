import requests, PyPDF2
import pandas as pd
import datetime

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
print(r.url)

string = r.text
bc1 = 'bc1'
xbt = 'xbt'
listt = []

def find_btc_address(item, string, listt):
    if item.lower() in string:
        location = string.find(str(item.lower()))
        print(string[location:(location + 38)])
        listt.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_btc_address(item, string, listt)
    elif item.upper() in string:
        location = string.find(str(item.upper()))
        print(string[location:(location + 38)])
        listt.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_btc_address(item, string, listt)
    elif item.capitalize() in string:
        location = string.find(str(item.capitalize()))
        print(string[location:(location + 38)])
        listt.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_btc_address(item, string, listt)
    else:
        print(str(item), "Is NOT in there")
    return listt

find_btc_address(xbt, string, listt)

l = []
for item in listt:
    a, b = str(item).split()
    l.append([a, b])

df = pd.DataFrame(l, columns=['Coin', 'Address'])
date = str(datetime.date.today())
csv = 'OFAC_BTC_ADDRESS_CHECK_' + date + '.csv'
df_csv = df.to_csv(csv)
