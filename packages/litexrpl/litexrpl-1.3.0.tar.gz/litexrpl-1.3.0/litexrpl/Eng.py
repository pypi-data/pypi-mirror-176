
import json
from http import client

from xrpl.clients import JsonRpcClient
from xrpl.models import (AccountCurrencies, AccountDelete, AccountInfo,
                         GatewayBalances, IssuedCurrencyAmount, LedgerData,
                         LedgerEntry, TrustSet)
from xrpl.models.requests.ledger_entry import Offer
from xrpl.transaction import (safe_sign_and_autofill_transaction,
                              send_reliable_submission)
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime
from xrpl.wallet import Wallet

from Misc import hex_to_symbol, symbol_to_hex, xrp_format_to_transfer_fee


class xEng(JsonRpcClient):
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
    
    def holding_tokens(self, wallet_addr: str) -> list:
        """retrieves a list of tokens that an account can send or receive, based on its trust lines."""
        token_holdings = []
        req = AccountCurrencies(account=wallet_addr, ledger_index="validated", strict=True)
        response = self.client.request(req)
        result = response.result
        r_tokens = result["receive_tokens"]
        s_tokens = result["send_tokens"]
        if s_tokens == []:
            pass
        if r_tokens == []:
            pass
        else:
            for currency in r_tokens:
                token_holdings.append(hex_to_symbol(currency))
            for currency in s_tokens:
                token_holdings.append(hex_to_symbol(currency))
        return token_holdings
    
    def created_tokens_issuer(self, wallet_addr: str) -> list:
        """returns all tokens an account has created as the issuer"""
        created_assets = []
        req = GatewayBalances(account=wallet_addr, ledger_index="validated")
        response = self.client.request(req)
        result = response.result
        if 'obligations' in result:
            obligations = result["obligations"]
            for key, value in obligations.items():
                asset = {}
                asset["token"] = hex_to_symbol(key)
                asset["amount"] = value
                asset["issuer"] = wallet_addr
                acc_info = AccountInfo(account=wallet_addr, ledger_index="validated")
                account_data = self.client.request(acc_info).result["account_data"]
                if "Domain" in account_data:
                    asset["domain"] = hex_to_symbol(account_data["Domain"])
                if "TransferRate" in account_data:
                    asset["transfer_fee"] = xrp_format_to_transfer_fee(account_data["TransferRate"])
                created_assets.append(asset)
        return created_assets
    
    def created_tokens_manager(self, wallet_addr: str) -> list:
        """returns all tokens an account thas created as the manager"""
        created_assets = []
        req = GatewayBalances(account=wallet_addr, ledger_index="validated")
        response = self.client.request(req)
        result = response.result
        if 'assets' in result:
            assets = result["assets"]
            for issuer, issuings in assets.items():
                for iss_cur in issuings:
                    asset = {}
                    asset["issuer"] = issuer
                    asset["token"] = hex_to_symbol(iss_cur["currency"])
                    asset["amount"] = iss_cur["value"]
                    asset["manager"] = wallet_addr
                    acc_info = AccountInfo(account=asset["cold_address"], ledger_index="validated")
                    account_data = self.client.request(acc_info).result["account_data"]
                    if "Domain" in account_data:
                        asset["domain"] = hex_to_symbol(account_data["Domain"])
                    if "TransferRate" in account_data:
                        asset["transfer_fee"] = xrp_format_to_transfer_fee(account_data["TransferRate"])
                    created_assets.append(asset)
        return created_assets

    def add_token(self, sender_seed: str, token: str, issuer: str, value: str, rippling: bool = False) -> dict:
        """enable transacting with a token"""
        flag = 131072
        if rippling:
            flag = 262144
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        cur = IssuedCurrencyAmount(currency=symbol_to_hex(token), issuer=issuer, value=value)
        my_payment = TrustSet(account=sender_wallet.classic_address, limit_amount=cur, flags=flag)
        signed_tx = safe_sign_and_autofill_transaction(my_payment, sender_wallet, self.client)
        prelim_result = send_reliable_submission(signed_tx, self.client)
        result = prelim_result.result
        return {
        "result": result["meta"]["TransactionResult"], 
        "txid": result["hash"],
        "link": f"{self.txn_url}{result['hash']}"}
    
    def modify_token_ripple_status(self, sender_seed: str, token: str, issuer: str, value: str, rippling: bool = False) -> dict:
        """modify ripple status of a token"""
        flag = 131072
        if rippling:
            flag = 262144
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        cur = IssuedCurrencyAmount(currency=symbol_to_hex(token), issuer=issuer, value=value)
        my_payment = TrustSet(account=sender_wallet.classic_address, limit_amount=cur, flags=flag)
        signed_tx = safe_sign_and_autofill_transaction(my_payment, sender_wallet, self.client)
        prelim_result = send_reliable_submission(signed_tx, self.client)
        result = prelim_result.result
        return {
        "result": result["meta"]["TransactionResult"], 
        "txid": result["hash"],
        "link": f"{self.txn_url}{result['hash']}"}

    # can only be called if user empties balance
    def remove_token(self, sender_seed: str, token: str, issuer: str) -> dict:
        """disable transacting with a token"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        trustset_cur = IssuedCurrencyAmount(currency=symbol_to_hex(token), issuer=issuer, value="0")
        trustset = TrustSet(account=sender_wallet.classic_address, limit_amount=trustset_cur)
        signed_tx = safe_sign_and_autofill_transaction(trustset, sender_wallet, self.client)
        prelim_result = send_reliable_submission(signed_tx, self.client)
        result = prelim_result.result
        return {
        "result": result["meta"]["TransactionResult"], 
        "txid": result["hash"],
        "link": f"{self.txn_url}{result['hash']}"}
    
    def delete_account(self, sender_seed: str, receiver_addr: str) -> dict:
        """delete an account from the ledger \n
        account must not own any ledger object, costs 2 xrp_chain fee, acc_seq + 256 > current_ledger_seq \n
        account can still be re-created after deletion"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        del_txn = AccountDelete(account=sender_wallet.classic_address, destination=receiver_addr)
        stxn = safe_sign_and_autofill_transaction(del_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
        "result": result["meta"]["TransactionResult"], 
        "txid": result["hash"],
        "link": f"{self.txn_url}{result['hash']}"}
    
    def merge_account(self, sender_seed: str, receiver_addr: str) -> dict:
        """merge accounts on the ledger \n
        account must not own any ledger object, costs 2 xrp_chain fee, acc_seq + 256 > current_ledger_seq \n
        account can still be created after merge"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        del_txn = AccountDelete(account=sender_wallet.classic_address, destination=receiver_addr)
        stxn = safe_sign_and_autofill_transaction(del_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
        "result": result["meta"]["TransactionResult"], 
        "txid": result["hash"],
        "link": f"{self.txn_url}{result['hash']}"}
    
    def get_offer_info(self, offer_creator: str, sequence: int) -> dict:
        """returns information about an offer"""
        offer_info = {}
        query = LedgerEntry(ledger_index="validated", offer=Offer(account=offer_creator, seq=sequence))
        result = self.client.request(query).result
        if "Account" in result["node"]:
            offer_info["index"] = result["index"]
            offer_info["creator"] = result["node"]["Account"]
            offer_info["sequence"] = result["node"]["Sequence"]
            offer_info["object_type"] = result["node"]["LedgerEntryType"]

            if isinstance(result["node"]["TakerPays"], dict):
                taker_pays_info = {}
                taker_pays_info["token"] = hex_to_symbol(result["node"]["TakerPays"]["currency"])
                taker_pays_info["issuer"] = result["node"]["TakerPays"]["issuer"]
                taker_pays_info["amount"] = result["node"]["TakerPays"]["value"]
                offer_info["taker_pays"] = taker_pays_info
            elif isinstance(result["node"]["TakerPays"], str):
                offer_info["taker_pays"] = str(drops_to_xrp(result["node"]["TakerPays"]))
            
            if isinstance(result["node"]["TakerGets"], dict):
                taker_gets_info = {}
                taker_gets_info["token"] = hex_to_symbol(result["node"]["TakerGets"]["currency"])
                taker_gets_info["issuer"] = result["node"]["TakerGets"]["issuer"]
                taker_gets_info["amount"] = result["node"]["TakerGets"]["value"]
                offer_info["taker_gets"] = taker_gets_info
            elif isinstance(result["node"]["TakerGets"], str):
                offer_info["taker_gets"] = str(drops_to_xrp(result["node"]["TakerGets"]))

            if "Expiration" in result["node"]:
                offer_info["expiry_date"] = str(ripple_time_to_datetime(result["node"]["Expiration"]))
        # add support for flags
        return offer_info

    def get_account_info(self, wallet_addr: str) -> dict:
        """returns information about an account"""
        account_info = {}
        query = AccountInfo(account=wallet_addr, ledger_index="validated")
        result = self.client.request(query).result
        if "account_data" in result:
            account_data = result["account_data"]
            account_info["index"] = account_data["index"]
            account_info["address"] = account_data["Account"]
            account_info["balance"] = drops_to_xrp(account_data["Balance"])
            account_info["object_type"] = account_data["LedgerEntryType"]
            # add support for flags
            account_info["account_objects"] = account_data["OwnerCount"]
            account_info["sequence"] = account_data["Sequence"]
            if "TickSize" in account_data:
                account_info["tick_size"] = account_data["TickSize"]
            if "TransferRate" in account_data:
                account_info["token_transfer_fee"] = xrp_format_to_transfer_fee(account_data["TransferRate"])
            if "Domain" in account_data:
                account_info["domain"] = hex_to_symbol(account_data["Domain"])
        return account_info

    def get_xrp_escrow_info(self, escrow_id: str) -> dict:
        """returns information about an escrow"""
        escrow_info = {}
        query = LedgerEntry(ledger_index="validated", escrow=escrow_id)
        result = self.client.request(query).result
        if "Account" in result["node"] and isinstance(result["node"]["Amount"], str):
            escrow_info["index"] = result["index"]
            escrow_info["creator"] = result["node"]["Account"]
            escrow_info["amount"] = drops_to_xrp(result["node"]["Amount"])
            escrow_info["receiver"] = result["node"]["Destination"]
            escrow_info["object_type"] = result["node"]["LedgerEntryType"]
            # add support for flags
            if "PreviousTxnID" in result["node"]:
                escrow_info["prex_txn_id"] = result["node"]["PreviousTxnID"] # needed to cancel or complete the escrow
            if "CancelAfter" in result["node"]:
                escrow_info["expiry_date"] = str(ripple_time_to_datetime(result["node"]["CancelAfter"]))
            if "FinishAfter" in result["node"]:
                escrow_info["redeem_date"] = str(ripple_time_to_datetime(result["node"]["FinishAfter"]))
            if "Condition" in result["node"]:
                escrow_info["condition"] = result["node"]["Condition"]
        return escrow_info

    def get_check_info(self, check_id: str) -> dict:
        check_info = {}
        query = LedgerEntry(ledger_index="validated", check=check_id)
        result = self.client.request(query).result
        if "Account" in result["node"]:
            check_info["index"] = result["index"]
            check_info["sender"] = result["node"]["Account"]
            check_info["receiver"] = result["node"]["Destination"]
            check_info["sequence"] = result["node"]["Sequence"]
            check_info["object_type"] = result["node"]["LedgerEntryType"]
            if "Expiration" in result["node"]:
                check_info["expiry_date"] = str(ripple_time_to_datetime(result["node"]["Expiration"]))
            # add support for flags
            if isinstance(result["node"]["SendMax"], str):
                check_info["amount"] = str(drops_to_xrp(result["node"]["SendMax"]))
            elif isinstance(result["node"]["Amount"], dict):
                check_info["token"] = hex_to_symbol(result["node"]["SendMax"]["currency"])
                check_info["issuer"] = result["node"]["SendMax"]["issuer"]
                check_info["amount"] = result["node"]["SendMax"]["value"]
        return check_info

    def get_token_info(self, issuer: str) -> dict:
        """returns information about a token"""
        issuer_info = {}
        query = AccountInfo(account=issuer, ledger_index="validated")
        result = self.client.request(query).result
        if "account_data" in result:
            account_data = result["account_data"]
            issuer_info["index"] = account_data["index"]
            issuer_info["issuer"] = account_data["Account"]
            issuer_info["balance"] = drops_to_xrp(account_data["Balance"])
            # add support for flags
            if "TickSize" in account_data:
                issuer_info["tick_size"] = account_data["TickSize"]
            if "TransferRate" in account_data:
                issuer_info["token_transfer_fee"] = xrp_format_to_transfer_fee(account_data["TransferRate"])
            if "Domain" in account_data:
                issuer_info["domain"] = hex_to_symbol(account_data["Domain"])
        return issuer_info

    def mint_token():
        pass
    
    def black_hole_account():
        pass

    def update_domain():
        pass

    def update_transfer_fee():
        pass

    def update_ticksize():
        pass
    # work
    def manage_trust_set():
        pass

    def manage_account_set():
        pass

    def get_nft_info():
        pass

    def get_payment_channel_info():
        pass

    




   
    



eng = xEng("https://s.altnet.rippletest.net:51234", "", "")

client = JsonRpcClient(eng.network_url)

req = GatewayBalances(account="r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW", ledger_index="validated")
response = client.request(req)
result = response.result

print(json.dumps(result, indent=4))

print(eng.created_tokens_issuer("r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW"))
print()
print()
print(eng.created_tokens_manager("r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW"))
# r = XRP()
# a = IssuedCurrency(currency=symbol_to_hex("LegitXRP"), issuer="r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8Aw")



# # print(json.dumps(eng.accountEscrows("rJVV8spek9H6cTJxGnTguVAk5zUU4njZ6P"), indent=2))
# # xeng = xEng("https://s.altnet.rippletest.net:51234", "", "")

# # print(json.dumps(xeng.accountOffers("r9ewzMXVRAD9CjZQ6LTQ4P21vUUucDuqd4"), indent=2))

# for i in range(100):
#     print(eng.create_xrp_check("sEd7GYcpKYgJf8TCUjEAQYE5ogE71id", "r9woHo14kZamXX2yZ7rvqtwMUTkC2Xa46x", randint(1, 5), None))
# print(eng.account_xrp_checks("rJL5MvGssucULib12cR2GMzkAjQShosMfX"))

# # l = LedgerEntry()

# eng = xEng("https://xrplcluster.com", "", "")

# print(eng.created_tokens_hot_addr("rGFuMiw48HdbnrUbkRYuitXTmfrDBNTCnX"))
# print(eng.create_escrow("sEd7GYcpKYgJf8TCUjEAQYE5ogE71id", 213, "rGFuMiw48HdbnrUbkRYuitXTmfrDBNTCnX", "A0258020729420D862B3A236C1166D6C15C58F9F8AE8F1F266FA2BE3906DCD3F2FB94C5C810139", (datetime_to_ripple_time(datetime.now() + timedelta(days=1))), (datetime_to_ripple_time(datetime.now() + timedelta(days=4)))))


is1 = "r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8Aw"
is2 = "rJidpkvxknBWJREp6P5zC9wp5Z66fRyAnu"
a1 = IssuedCurrencyAmount(currency=symbol_to_hex("TestXRP"), issuer=is2, value=500093)
#print(eng.create_offer("sEdS7BaibbbUkj3VBZrz7FfRsPwtWug", 10.0, a1, None))

# rJVV8spek9H6cTJxGnTguVAk5zUU4njZ6P

# with open("u.json", "wt") as f:
#     json.dump(eng.account_offers("rJidpkvxknBWJREp6P5zC9wp5Z66fRyAnu", limit=None), f, indent=2)

o = LedgerEntry(ledger_index="validated", offer="0807CD4B67A8A08F96A9CE683371A6D7137324184BD16EF361144C0608647787")

import Misc

o = LedgerData(id=28643065)# account_root="rJVV8spek9H6cTJxGnTguVAk5zUU4njZ6P")
response = Misc.client.request(o)
# print(response)
