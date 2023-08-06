from decimal import Decimal
from typing import Union

from xrpl.account import (get_account_info, get_account_payment_transactions,
                          get_balance, get_next_valid_seq_number)
from xrpl.clients import JsonRpcClient
from xrpl.core import keypairs
from xrpl.ledger import get_fee
from xrpl.models import (AccountInfo, AccountLines, IssuedCurrencyAmount,
                         Payment)
from xrpl.transaction import (safe_sign_and_autofill_transaction,
                              send_reliable_submission)
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, xrp_to_drops
from xrpl.wallet import Wallet

from Misc import hex_to_symbol, symbol_to_hex, xrp_format_to_transfer_fee


class xWallet(JsonRpcClient):
    def __init__(self, network_url: str, account_url: str, txn_url: str):
        self.network_url = network_url
        self.account_url = account_url
        self.txn_url = txn_url
        self.client = JsonRpcClient(network_url)

    def toTestnet(self) -> bool:
        self.network_url = "https://s.altnet.rippletest.net:51234"
        self.account_url = "https://testnet.xrpl.org/accounts/"
        self.txn_url = "https://testnet.xrpl.org/transactions/"
        self.client = JsonRpcClient(self.network_url)
        return True

    def toMainnet(self) -> bool:
        self.network_url = "https://xrplcluster.com"
        self.account_url = "https://livenet.xrpl.org/accounts/"
        self.txn_url = "https://livenet.xrpl.org/transactions/"
        self.client = JsonRpcClient(self.network_url)
        return True
    
    def show_account_in_explorer(self, wallet_addr: str) -> str:
        """show account in explorer"""
        return f"{self.account_url}{wallet_addr}"

    def show_transaction_in_explorer(self, txid: str) -> str:
        """show transaction in explorer"""
        return f"{self.txn_url}{txid}"

    def generate_xrp_wallet(self, name: str) -> dict:
        """generate a new xrp wallet"""
        wallet_info = {}
        wallet = Wallet.create()
        seed = wallet.seed
        public, private = keypairs.derive_keypair(seed)
        wallet_info["name"] = name
        wallet_info["classic_address"] = wallet.classic_address
        wallet_info["private_key"] = private
        wallet_info["public_key"] = public
        wallet_info["seed"] = seed
        return wallet_info

    def restore_wallet(self, name: str, seed: str) -> dict:
        """restore a wallet from a seed"""
        public, private = keypairs.derive_keypair(seed)
        wallet_info = {}
        wallet_info["name"] = name
        wallet_info["classic_address"] = keypairs.derive_classic_address(public)
        wallet_info["private_key"] = private
        wallet_info["public_key"] = public
        wallet_info["seed"] = seed
        return wallet_info

    def get_network_fee(self) -> str:
        """return transaction fee"""
        return drops_to_xrp(str(get_fee(self.client)))
    
    def xrp_balance(self, wallet_addr: str) -> Decimal:
        """return formatted xrp balance"""
        init_balance = int(get_balance(wallet_addr, self.client)) - 10000000
        response = get_account_info(wallet_addr, self.client).result
        owner_count = int(response["account_data"]["OwnerCount"])
        balance = init_balance - (2000000 * owner_count)
        return drops_to_xrp(str(balance))
    
    def detailed_xrp_balance(self, wallet_addr: str) -> dict:
        init_balance = int(get_balance(wallet_addr, self.client)) - 10000000
        response = get_account_info(wallet_addr, self.client).result
        owner_count = int(response["account_data"]["OwnerCount"])
        return {
        "xrp_balance": str(drops_to_xrp(str(init_balance))), 
        "object_count": owner_count}
    
    def get_account_next_seq_number(self, wallet_addr: str) -> int:
        """return next valid account sequence number"""
        return get_next_valid_seq_number(address=wallet_addr, client=self.client, ledger_index="validated")

    def xrp_transactions(self, wallet_addr: str) -> dict:
        """return all xrp payment transactions an address has carried out"""
        transactions_dict = {}
        sent = []
        received = []
        response = get_account_payment_transactions(wallet_addr, self.client)
        for transaction in response:
            transact = {}
            if isinstance(transaction["tx"]["Amount"], dict):
                pass
            else:
                transact["sender"] = transaction["tx"]["Account"]
                transact["receiver"] = transaction["tx"]["Destination"]
                transact["amount"] = str(drops_to_xrp(str(transaction["tx"]["Amount"])))
                transact["fee"] = str(drops_to_xrp(str(transaction["tx"]["Fee"])))
                transact["timestamp"] = str(ripple_time_to_datetime(transaction["tx"]["date"]))
                transact["final_result"] = transaction["meta"]["TransactionResult"]
                transact["txid"] = transaction["tx"]["hash"]
                # in ledger
                # flags
                # result
                transact["link"] = f'{self.txn_url}{transaction["tx"]["hash"]}'
                transact["tx_type"] = transaction["tx"]["TransactionType"]
                if transact["sender"] == wallet_addr:
                    sent.append(transact)
                elif transact["sender"] != wallet_addr:
                    received.append(transact)
        transactions_dict['sent'] = sent
        transactions_dict['received'] = received
        return transactions_dict

    def token_transactions(self, wallet_addr: str) -> dict:
        """return all asset payment transactions an account has carried out"""
        transactions_dict = {}
        sent = []
        received = []
        response = get_account_payment_transactions(wallet_addr, self.client)
        for transaction in response:
            if isinstance(transaction["tx"]["Amount"], dict):
                transact = {}
                transact["sender"] = transaction["tx"]["Account"]
                transact["receiver"] = transaction["tx"]["Destination"]
                transact["token"] = hex_to_symbol(transaction["tx"]["Amount"]["currency"])
                transact["issuer"] = transaction["tx"]["Amount"]["issuer"]
                transact["amount"] = transaction["tx"]["Amount"]["value"]
                transact["fee"] =  str(drops_to_xrp(str(transaction["tx"]["Fee"])))
                transact["timestamp"] = str(ripple_time_to_datetime(transaction["tx"]["date"]))
                transact["final_result"] = transaction["meta"]["TransactionResult"]
                transact["txid"] = transaction["tx"]["hash"]
                transact["link"] = f'{self.txn_url}{transaction["tx"]["hash"]}'
                transact["tx_type"] = transaction["tx"]["TransactionType"]
                if transact["sender"] == wallet_addr:
                    sent.append(transact)
                elif transact["sender"] != wallet_addr:
                    received.append(transact)
        transactions_dict['sent'] = sent
        transactions_dict['received'] = received
        return transactions_dict
    
    def payment_transactions(self, wallet_addr: str) -> dict:
        """return all payment transactions for xrp and tokens both sent and received"""
        transactions_dict = {}
        sent = []
        received = []
        response = get_account_payment_transactions(wallet_addr, self.client)
        for transaction in response:
            transact = {}
            transact["sender"] = transaction["tx"]["Account"]
            transact["receiver"] = transaction["tx"]["Destination"]
            if isinstance(transaction["tx"]["Amount"], dict):
                transact["token"] = hex_to_symbol(transaction["tx"]["Amount"]["currency"])
                transact["issuer"] = transaction["tx"]["Amount"]["issuer"]
                transact["amount"] = transaction["tx"]["Amount"]["value"]
            if isinstance(transaction["tx"]["Amount"], str):
                transact["token"] = "XRP"
                transact["issuer"] = ""
                transact["amount"] = str(drops_to_xrp(str(transaction["tx"]["Amount"])))
            # in ledger
            # flags
            # result
            transact["fee"] = str(drops_to_xrp(str(transaction["tx"]["Fee"])))
            transact["timestamp"] = str(ripple_time_to_datetime(transaction["tx"]["date"]))
            transact["final_result"] = transaction["meta"]["TransactionResult"]
            transact["txid"] = transaction["tx"]["hash"]
            transact["link"] = f'{self.txn_url}{transaction["tx"]["hash"]}'
            transact["tx_type"] = transaction["tx"]["TransactionType"]
            if transact["sender"] == wallet_addr:
                sent.append(transact)
            elif transact["sender"] != wallet_addr:
                received.append(transact)
        transactions_dict['sent'] = sent
        transactions_dict['received'] = received
        return transactions_dict

    def send_xrp(self, sender_seed: str, receiver_addr: str, amount: Union[float, Decimal, int]) -> dict:
        """send xrp"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        txn = Payment(account=sender_wallet.classic_address, amount=xrp_to_drops(amount), destination=receiver_addr)
        signed_txn = safe_sign_and_autofill_transaction(txn, sender_wallet, self.client)        
        product = send_reliable_submission(signed_txn, self.client)
        product_result = product.result
        return {
            "result": product_result["meta"]["TransactionResult"], 
            "txid": product_result["hash"],
            "link": f"{self.txn_url}{product_result['hash']}"}
    
    def send_token(self, sender_seed: str, receiver_addr: str, token: str,
        amount: str, issuer: str) -> dict:
        """send asset...
        max amount = 15 decimal places"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)

        txn_payment = Payment(account=sender_wallet.classic_address, destination=receiver_addr,
        amount=IssuedCurrencyAmount(
            currency=symbol_to_hex(token),
            issuer=issuer,
            value=amount
        ))
        stxn_payment = safe_sign_and_autofill_transaction(
            transaction=txn_payment,
            wallet=sender_wallet,
            client=self.client
        )
        stxn_response = send_reliable_submission(stxn_payment, self.client)
        stxn_result = stxn_response.result
        return {
        "result": stxn_result["meta"]["TransactionResult"], 
        "txid": stxn_result["hash"],
        "link": f"{self.txn_url}{stxn_result['hash']}"}

    def account_tokens(self, wallet_addr: str) -> list:
        """returns all tokens a wallet address is holding with their respective issuers, limit and balances"""
        assets = []
        acc_info = AccountLines(account=wallet_addr, ledger_index="validated")
        response = self.client.request(acc_info)
        result = response.result
        if "lines" in result:
            lines = result["lines"]
            for line in lines:
                asset = {}
                asset["token"] = hex_to_symbol(line["currency"])
                asset["issuer"] = line["account"]
                asset["amount"] = line["balance"]
                asset["limit"] = line["limit"] # the max an account can handle
                if 'no_ripple' in line:
                    asset["ripple_status"] = line["no_ripple"] # no ripple = true, means rippling is disabled which is good; else bad

                if 'freeze' in line:
                    asset["freeze_status"] = line["freeze"]
                else:
                    asset["freeze_status"] = False

                acc_info = AccountInfo(account=line["account"], ledger_index="validated")
                account_data = self.client.request(acc_info).result["account_data"]
                if "Domain" in account_data:
                    asset["domain"] = hex_to_symbol(account_data["Domain"])
                if "TransferRate" in account_data:
                    asset["token_transfer_fee"] = xrp_format_to_transfer_fee(account_data["TransferRate"])
                assets.append(asset)
        return assets


    
w = xWallet("https://s.altnet.rippletest.net:51234", "", "")
# print(w.account_tokens("r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW"))

print(w.get_network_fee())

add1 = "r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW"
s1 = "sEdThjCR5Vy2MNqN6hWkFr4NhK9Bnkn"

add2 = "r9ewzMXVRAD9CjZQ6LTQ4P21vUUucDuqd4"
s2 = "sEdTuywsDSBxUfWi5VozXnVdkUYTT1L"

print(w.send_xrp(s1, add2, 11.0))

print(w.account_tokens(add1))

print(w.payment_transactions(add1))

print(w.send_xrp(s1, add2, 11.0))

print(w.generate_xrp_wallet("jj"))

print(w.xrp_transactions("r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW"))
