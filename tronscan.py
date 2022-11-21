import requests

def balance_constructor(api_balance, decimal, symbol):
    '''Tronscan API returns balances with no decimals or anything
    but there is a key called tokenDecimal that tells the web page 
    how to construct it, I implemented the same logic here to get
    the correct values'''
    decimal=int(decimal)*-1
    balance=symbol+' ' + api_balance[:decimal]+'.'+api_balance[decimal:]

    return balance


def tronscan_scraper(wallet_address):

    # base url for tronscan API
    base_url='https://apilist.tronscanapi.com/api/accountv2?address='

    # add wallet address to base url
    wallet_url=base_url+wallet_address
    print(f'Getting data for {wallet_address} from {wallet_url}')

    # API request
    response = requests.get(wallet_url)
    
    # read as json
    data = response.json()

    tokenlist=data['withPriceTokens']

    trx, usdt, btt='0 TRX', None, None
    # loop through json to find the data we want
    for token in tokenlist:
        if token['tokenAbbr'] == 'trx':
            api_balance=token['amount']
            api_decimal_place=token['tokenDecimal']
            trx='TRX ' + api_balance
            # trx = balance_constructor(api_balance, api_decimal_place)
        elif token['tokenAbbr'] == 'USDT':
            api_balance=token['balance']
            api_decimal_place=token['tokenDecimal']
            usdt = balance_constructor(api_balance, api_decimal_place, 'USDT')
        elif token['tokenAbbr'] == 'BTT':
            api_balance=token['balance']
            api_decimal_place=token['tokenDecimal']
            btt = balance_constructor(api_balance, api_decimal_place, 'BTT')
    
    if len(trx)>4:
        balances=[]
        balances.append(trx)
        if usdt != None:
            balances.append(usdt)

        if btt != None:
            balances.append(btt)

        return balances
    else:
        print('Could not get data from tronscan, trying again...')
        tronscan_scraper(wallet_address)


    