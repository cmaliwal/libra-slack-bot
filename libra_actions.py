#Libra Wallet in Python
from pylibra import LibraClient, LibraWallet
from pylibra.transaction import TransferTransaction
from termcolor import colored, cprint
import pyqrcode, sys

client = LibraClient()

def account(words=None):
    print("\n")
    wallet = LibraWallet() if words is None else LibraWallet(words)

    account = wallet.get_account(0)
    cprint(f"address: {account.address}", "blue")
    cprint(f"mnemonic: {wallet.to_mnemonic()}", "blue")
    cprint(f"public key: {account.public_key}", "blue")
    cprint(f"private key: {account.private_key}", "blue")
    if client.get_account_state(account) == None or round(client.get_account_state(account).balance/1000000) == 0:
        balance = 0
        cprint(f"Balance: 0 tLibra", "red")
    else:
        balance = round(client.get_account_state(account).balance/1000000)
        cprint(f"Balance: {round(client.get_account_state(account).balance/1000000)} tLibra", "green")
    
    account_details = {
        'address': account.address,
        'mnemonic': wallet.to_mnemonic(),
        'public_key': account.public_key,
        'private_key': account.private_key,
        'balance': balance
    }
    return account_details

def balance(account):
    account_state = client.get_account_state(account)
    if client.get_account_state(account) == None or round(client.get_account_state(account).balance/1000000) == 0:
        balance = 0
        cprint(f"Balance: 0 tLibra", "red")
    else:
        balance = round(client.get_account_state(account).balance/1000000)
        cprint(f"Balance: {round(client.get_account_state(account).balance/1000000)} tLibra", "green")
    return balance

def mint(account, amount):
    balance(account)
    try:
        client.mint_with_faucet(account, int(amount)*1000000)
        cprint(f"\n{amount} tLibra sent to account {account}!", "green")
    except:
        cprint("\nCould not mint that amount", "yellow")
    return balance(account)
    

def qr_create(address):
    qr = pyqrcode.create(address)
    print(qr.text().replace("0","⬜").replace("1","⬛"))
    return qr.text().replace("0","⬜").replace("1","⬛")
