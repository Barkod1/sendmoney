import cbpro
import requests
from coinbase.wallet.client import Client

type_account = input('1. transfer to your account (between pro and normal)\n2. transfer to other\'s accounts ')
if type_account == '1':
    type_account = input(
        'to pro from normal or to normal from pro? (p for to pro from normal) (n for to normal from pro) ')

    key = input('enter your api key: ')
    b64secret = input('enter your api secret: ')
    passphrase = input('enter your passphrase: ')
    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=b64secret, passphrase=passphrase)

    if auth_client.get_accounts().message != 'Invalid API Key':
        print('login succeed!')
        normal_accounts = auth_client.get_coinbase_accounts()
        pro_accounts = auth_client.get_accounts()
        for wallet in normal_accounts.data:
            if float(wallet.balance) != 0.0:
                print(wallet.balance, ':')
                print(wallet.balance, wallet.currency)
        print('balance of pro:')
        for wallet in pro_accounts.data:
            if float(wallet.balance) != 0.0:
                print(wallet.balance, wallet.currency)

        for i in range(4):
            amount = input('enter how much you want to transfer: ')
            currency = input('enter the currency: ')
            for wallet in normal_accounts.data:
                if wallet.currency == currency:
                    coinbase_account_id = wallet.id
            if type_account == 'n':
                res = auth_client.coinbase_withdraw(amount=amount, currency=currency,
                                                    coinbase_account_id=coinbase_account_id)

            elif type_account == 'p':
                res = auth_client.coinbase_deposit(amount=amount, currency=currency,
                                                   coinbase_account_id=coinbase_account_id)


elif type_account == '2':
    type_account = input('from pro or normal? (p) (n): ')
    if type_account == 'n':
        API_KEY = input('enter your API key: ')
        API_SECRET = input('enter your API secret: ')
        client = Client(API_KEY, API_SECRET)
        accounts = client.get_accounts()
        primary_account = client.get_primary_account()

        print('your balance: ')
        if float(primary_account.balance.amount) != 0.0:
            print(primary_account.name +': ')
            print(primary_account.balance.amount + ' ' + primary_account.balance.currency)
        for wallet in accounts.data:
            if float(wallet.balance.amount) != 0.0:
                print(wallet.balance.amount, ':')
                print(wallet.balance.amount, wallet.balance.currency)

        amount = input('enter how much you want to transfer: ')
        currency = input('enter the currency: ')
        address = input('enter the crypto address you want to transfer to: ')
        if primary_account.currency == currency:
            ac_id = primary_account.id
        for wallet in accounts.data:
            if wallet.currency == currency:
                ac_id = wallet.id

        account = client.get_account(ac_id)
        tx = account.send_money(to=address,
                                        amount=amount,
                                        currency=currency)
    elif type_account == 'p':
        key = input('enter your api key: ')
        b64secret = input('enter your api secret: ')
        passphrase = input('enter your passphrase: ')
        auth_client = cbpro.AuthenticatedClient(key=key, b64secret=b64secret, passphrase=passphrase)
        amount = input('enter how much you want to transfer: ')
        currency = input('enter the currency: ')
        address = input('enter the crypto address you want to transfer to: ')
        res = requests.post('https://api.pro.coinbase.com/withdrawals/crypto', amount=amount, currency=currency,
                            crypto_address=address)
