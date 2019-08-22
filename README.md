# bitcoin_OFAC

This is a simple Python program that uses a couple libraries to scrape the SDN List for bitcoin addresses. 
The program is built assuming that the list continues to denominate BTC addresses as "XBT" addresses.
The program also scrapes for LTC addresses, and can be modified easily to add any other coin with 34 char addresses.

Currently, this program does not check for ETH or ETC addresses on the SDN List, although that will be added.

Dependencies for this program are the Pandas, and Requests libraries.
