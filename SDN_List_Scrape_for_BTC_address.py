import requests
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
# The coin names/abbreviations on the SDN List
xbt_string = 'xbt'
# eth_string = '0x' # Not on SDN List yet
ltc_string = 'ltc'

address_list = []
# Accumulation list is outside of the function and passed in so that it's not overwritten

# find_coin_address function can be used for BTC, BCH, LTC and possibly others, but it
# cannot be used for ETH or ETC – We will need another function to collect that data
def find_coin_address(item, string, address_list):
    if item.lower() in string:
        location = string.find(str(item.lower()))
        print(string[location:(location + 38)])
        address_list.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_coin_address(item, string, address_list)
    elif item.upper() in string:
        location = string.find(str(item.upper()))
        print(string[location:(location + 38)])
        address_list.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_coin_address(item, string, address_list)
    elif item.capitalize() in string:
        location = string.find(str(item.capitalize()))
        print(string[location:(location + 38)])
        address_list.append(string[location:(location + 38)])
        string = string[(location + 38): len(string)]
        find_coin_address(item, string, address_list)
    else:
        print("")

find_coin_address(xbt_string, string, address_list)
find_coin_address(ltc_string, string, address_list)


l = [] # l is a list that will take the string list (address_list) that is split properly [[coin, address]]
for item in address_list:
    coin, address = str(item).split()
    l.append([coin, address])

df = pd.DataFrame(l, columns=['Coin', 'Address'])

print(len(df[df['Coin'] == 'XBT']), "Bitcoin addresses on the SDN List")
print(len(df[df['Coin'] == 'LTC']), "Litecoin addresses on the SDN List")

date = str(datetime.date.today())
csv = 'OFAC_BTC_ADDRESS_CHECK_' + date + '.csv'
df_csv = df.to_csv(csv, index=False)
