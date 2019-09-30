# bitcoin_OFAC

This is a simple Python program that uses a couple libraries to scrape the SDN List for bitcoin addresses. 
The program is built assuming that the list continues to denominate BTC addresses as "XBT" addresses.
The program also scrapes for LTC addresses, and can be modified easily to add any other coin with 34 char addresses.

Currently, this program does not check for ETH or ETC addresses on the SDN List, although that will be added.

Dependencies for this program are the Pandas, and Requests libraries.

Things to consider: This script needs to be modified to pull full 42 char XBT addresses (once they are added to the SDN List), I am being lazy and haven't implemented it yet, but I'd think it would be easy to use an "if" statement regarding the first few characters of the XBT address (i.e. if "bc1" in string[x:x], then pull 42 chars instead of 34). 
