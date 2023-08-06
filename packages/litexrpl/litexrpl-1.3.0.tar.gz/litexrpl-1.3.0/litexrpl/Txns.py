from xrpl.clients import JsonRpcClient
from xrpl.models.requests import Tx
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime

from Misc import hex_to_symbol

"""return more information on transactions"""

class xTxn(JsonRpcClient):
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
    
    def xrp_txn(self, txid: str) -> dict:
        """return more information on a single xrp transfer transaction"""
        pay_dict = {}
        query = Tx(transaction=txid)
        result = self.client.request(query).result
        if isinstance(result["Amount"], str):
            pay_dict["sender"] = result["Account"]
            pay_dict["receiver"] = result["Destination"]
            pay_dict["amount"] = str(drops_to_xrp(result["Amount"]))
            pay_dict["fee"] = str(drops_to_xrp(result["Fee"]))
            pay_dict["date"] = str(ripple_time_to_datetime(result["date"]))
            pay_dict["txid"] = result["hash"]
            pay_dict["link"] = f"{self.txn_url}{result['hash']}"
            pay_dict["txn_type"] = result["TransactionType"]
            # add flags
            pay_dict["sequence"] = result["Sequence"]
            pay_dict["in_ledger"] = result["inLedger"]
            pay_dict["txn_signature"] = result["TxnSignature"]
            pay_dict["txn_index"] = result["meta"]["TransactionIndex"]
            pay_dict["txn_result"] = result["meta"]["TransactionResult"]
            pay_dict["ledger_is_validated"] = result["validated"]
        return pay_dict
    
    def token_txn(self, txid: str) -> dict:
        """return more information on a single token transfer transaction"""
        pay_dict = {}
        query = Tx(transaction=txid)
        result = self.client.request(query).result
        if isinstance(result["Amount"], dict):
            pay_dict["sender"] = result["Account"]
            pay_dict["receiver"] = result["Destination"]
            pay_dict["token"] = hex_to_symbol(result["Amount"]["currency"])
            pay_dict["issuer"] = result["Amount"]["issuer"]
            pay_dict["amount"] = result["Amount"]["value"]
            pay_dict["fee"] = str(drops_to_xrp(result["Fee"]))
            pay_dict["date"] = str(ripple_time_to_datetime(result["date"]))
            pay_dict["txid"] = result["hash"]
            pay_dict["link"] = f"{self.txn_url}{result['hash']}"
            pay_dict["txn_type"] = result["TransactionType"]
            # add flags
            pay_dict["sequence"] = result["Sequence"]
            pay_dict["in_ledger"] = result["inLedger"]
            pay_dict["txn_signature"] = result["TxnSignature"]
            pay_dict["txn_index"] = result["meta"]["TransactionIndex"]
            pay_dict["txn_result"] = result["meta"]["TransactionResult"]
            pay_dict["ledger_is_validated"] = result["validated"]
        return pay_dict
    
    def offer_create_txn(self, txid: str) -> dict:
        """"""
        pass

    def check_create_txn(self, txid: str) -> dict:
        pass