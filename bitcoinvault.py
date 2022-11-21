import requests
from bs4 import BeautifulSoup
import re

def bitcoinvault_scraper(wallet_address):
    
    # base url for bitcoinvault
    base_url='https://explorer.bitcoinvault.global/address/'

    # add wallet address to base url
    wallet_url=base_url+wallet_address

    print(f'Getting data for {wallet_address} from {wallet_url}')

    # get the page
    response=requests.get(wallet_url)

    # make some soup
    soup = BeautifulSoup(response.content,features="lxml")

    # they did not use ids or anything in the HTML source 
    # so we'll have to do some tricks
    balance='BTCV: '+soup.find(text=re.compile('Balance')).find_next('span').text 
    if len(balance)>5:
        balances=[]
        balances.append(balance)
    else:
        print('Could not get data from BTCVault, trying again...')
        bitcoinvault_scraper(wallet_address)

    return balances