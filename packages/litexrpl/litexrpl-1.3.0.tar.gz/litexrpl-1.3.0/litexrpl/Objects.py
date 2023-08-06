from decimal import Decimal
from typing import Union

from xrpl.clients import JsonRpcClient
from xrpl.models import (XRP, AccountObjects, AccountOffers, BookOffers,
                         CheckCancel, CheckCash, CheckCreate, EscrowCancel,
                         EscrowCreate, EscrowFinish, IssuedCurrency,
                         IssuedCurrencyAmount, OfferCancel, OfferCreate, Tx)
from xrpl.transaction import (safe_sign_and_autofill_transaction,
                              send_reliable_submission)
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, xrp_to_drops
from xrpl.wallet import Wallet

from Misc import hex_to_symbol, symbol_to_hex

"""
Manage Checks, Offers, Payment Channels
"""

class xObject(JsonRpcClient):
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

    # convert date_time object to ripple time
    # xMisc.datetime_to_ripple_time()
    def create_xrp_check(self, sender_seed: str, receiver_addr: str, amount: Union[int, float, Decimal], expiry_date: Union[int, None]) -> dict:
        """create xrp check"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        check_txn = CheckCreate(account=sender_wallet.classic_address, destination=receiver_addr, send_max=xrp_to_drops(amount), expiration=expiry_date)
        stxn = safe_sign_and_autofill_transaction(check_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}

    def account_xrp_checks(self, wallet_addr: str, limit: int = None) -> dict:
        """return a dict of xrp checks an account sent or received"""
        checks_dict = {}
        sent = []
        receive = []
        req = AccountObjects(account=wallet_addr, ledger_index="validated", type="check", limit=limit)
        response = self.client.request(req)
        result = response.result
        if "account_objects" in result:
            account_checks = result["account_objects"]
            for check in account_checks:
                if isinstance(check["SendMax"], dict):
                    pass
                else: 
                    check_data = {}
                    check_data["sender"] = check["Account"]
                    check_data["receiver"] = check["Destination"]
                    if "Expiration" in check:
                        check_data["expiry_date"] = str(ripple_time_to_datetime(check["Expiration"]))
                    check_data["amount"] = str(drops_to_xrp(check["SendMax"]))
                    check_data["check_id"] = check["index"]
                    if check_data["sender"] == wallet_addr:
                        sent.append(check_data)
                    elif check_data["sender"] != wallet_addr:
                        receive.append(check_data)
        checks_dict["sent"] = sent
        checks_dict["receive"] = receive
        return checks_dict

    def cash_xrp_check(self, sender_seed: str, check_id: str, amount: Union[int, Decimal, float]) -> dict:
        """cash a check, only the receiver defined on creation
        can cash a check"""
        # sender is the check casher
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        check_txn = CheckCash(account=sender_wallet.classic_address, check_id=check_id, amount=xrp_to_drops(amount))
        stxn = safe_sign_and_autofill_transaction(check_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}
    
    def cancel_check(self, sender_seed: str, check_id: str) -> dict:
        """cancel a check"""
        # sender is the check creator or recipient
        # create wallet object
        # If the Check has expired, any address can cancel it
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        check_txn = CheckCancel(account=sender_wallet.classic_address, check_id=check_id)
        stxn = safe_sign_and_autofill_transaction(check_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}  

    # xMisc.datetime_to_ripple_time()
    def create_token_check(self, sender_seed: str, receiver_addr: str, token: str, amount: str, issuer: str, expiry_date: Union[int, None]) -> dict:
        """create a token check"""
        # create wallet object 
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        check_txn = CheckCreate(account=sender_wallet.classic_address, destination=receiver_addr,
        send_max=IssuedCurrencyAmount(
            currency=symbol_to_hex(token), 
            issuer=issuer, 
            value=amount),
        expiration=expiry_date)
        stxn = safe_sign_and_autofill_transaction(check_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}
    
    def cash_token_check(self, sender_seed: str, check_id: str, token: str, amount: str, issuer: str) -> dict:
        """cash a check, only the receiver defined on creation
        can cash a check"""
        # sender is the check casher
        # create wallet object
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        check_txn = CheckCash(account=sender_wallet.classic_address, check_id=check_id, amount=IssuedCurrencyAmount(
            currency=symbol_to_hex(token),
            issuer=issuer,
            value=amount))
        stxn = safe_sign_and_autofill_transaction(check_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}

    def account_token_checks(self, wallet_addr: str, limit: int = None) -> dict:
        """return a dict of token checks an account sent or received"""
        checks_dict = {}
        sent = []
        receive = []
        req = AccountObjects(account=wallet_addr, ledger_index="validated", type="check", limit=limit)
        response = self.client.request(req)
        result = response.result
        if "account_objects" in result:
            account_checks = result["account_objects"]
            for check in account_checks:
                if isinstance(check["SendMax"], dict):
                    check_data = {}
                    check_data["sender"] = check["Account"]
                    check_data["receiver"] = check["Destination"]
                    if "Expiration" in check:
                        check_data["expiry_date"] = str(ripple_time_to_datetime(check["Expiration"]))
                    check_data["token"] = hex_to_symbol(check["SendMax"]["currency"])
                    check_data["issuer"] = check["SendMax"]["issuer"]
                    check_data["amount"] = check["SendMax"]["value"]
                    check_data["check_id"] = check["index"]
                    if check_data["sender"] == wallet_addr:
                        sent.append(check_data)
                    elif check_data["sender"] != wallet_addr:
                        receive.append(check_data)
        checks_dict["sent"] = sent
        checks_dict["receive"] = receive
        return checks_dict   
    
    def create_xrp_escrow(self, sender_seed: str, amount: Union[int, float, Decimal], receiver_addr: str, condition: Union[str, None], claim_date: Union[int, None], expiry_date: Union[int, None]) -> dict:
        """create an Escrow\n
        fill condition with `Misc.genCondition_Fulfillment["condition"]`\n
        You must use one `claim_date` or `expiry_date` unless this will fail"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        create_txn = EscrowCreate(account=sender_wallet.classic_address, amount=xrp_to_drops(amount), destination=receiver_addr, finish_after=claim_date, cancel_after=expiry_date, condition=condition)
        stxn = safe_sign_and_autofill_transaction(create_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}

    def schedule_xrp(self, sender_seed: str, amount: Union[int, float, Decimal], receiver_addr: str, claim_date: int, expiry_date: Union[int, None]) -> dict:
        """schedule an Xrp payment
        \n expiry date must be greater than claim date"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        create_txn = EscrowCreate(account=sender_wallet.classic_address, amount=xrp_to_drops(amount), destination=receiver_addr, finish_after=claim_date, cancel_after=expiry_date)
        stxn = safe_sign_and_autofill_transaction(create_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}

    def account_xrp_escrows(self, wallet_addr: str, limit: int = None) -> dict:
        """returns all account escrows, used for returning scheduled payments"""
        escrow_dict = {}
        sent = []
        received = []
        req = AccountObjects(account=wallet_addr, ledger_index="validated", type="escrow", limit=limit)
        response = self.client.request(req)
        result = response.result

        escrows = result["account_objects"]
        for escrow in escrows:
            escrow_data = {}
            if isinstance(escrow["Amount"], str):
                escrow_data["escrow_id"] = escrow["index"]
                escrow_data["sender"] = escrow["Account"]
                escrow_data["receiver"] = escrow["Destination"]
                escrow_data["amount"] = str(drops_to_xrp(escrow["Amount"]))
                if "PreviousTxnID" in escrow:
                    escrow_data["prev_txn_id"] = escrow["PreviousTxnID"] # needed to cancel or complete the escrow
                if "FinishAfter" in escrow:
                    escrow_data["redeem_date"] = str(ripple_time_to_datetime(escrow["FinishAfter"]))
                if "CancelAfter" in escrow:
                    escrow_data["expiry_date"] = str(ripple_time_to_datetime(escrow["CancelAfter"]))
                if "Condition" in escrow:
                    escrow_data["condition"] = escrow["Condition"]
                    
                if escrow_data["sender"] == wallet_addr:
                    sent.append(escrow_data)
                else:
                    received.append(escrow_data)
        escrow_dict["sent"] = sent
        escrow_dict["received"] = received
        return escrow_dict
    
    def r_seq_dict(self, prev_txn_id: str) -> dict:
        """return escrow seq or ticket sequence for finishing or cancelling \n use seq_back_up if seq is null"""
        info_dict = {}
        req = Tx(transaction=prev_txn_id)
        response = self.client.request(req)
        result = response.result
        if "Sequence" in result:
            info_dict["sequence"] = result["Sequence"]
        if "TicketSequence" in result:
            info_dict["seq_back_up"] = result["TicketSequence"]
        return info_dict
    
    def r_sequence(self, prev_txn_id: str) -> int:
        """return escrow seq for finishing or cancelling escrow"""
        seq = 0
        req = Tx(transaction=prev_txn_id)
        response = self.client.request(req)
        result = response.result
        if "Sequence" in result:
            seq = result["Sequence"]
        return seq

    def cancel_xrp_escrow(self, sender_seed: str, escrow_creator: str, prev_txn_id: str) -> dict:
        """cancel an escrow\n
        If the escrow does not have a CancelAfter time, it never expires """
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        seq = self.r_sequence(prev_txn_id)
        cancel_txn = EscrowCancel(account=sender_wallet.classic_address, owner=escrow_creator, offer_sequence=seq)
        stxn = safe_sign_and_autofill_transaction(cancel_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}

    def finish_xrp_escrow(self, sender_seed: str, escrow_creator: str, prev_txn_id: str, condition: Union[str, None], fulfillment: Union[str, None]) -> dict:
        """complete an escrow\n
        cannot be called until the finish time is reached"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        seq = self.r_sequence(prev_txn_id)
        finish_txn = EscrowFinish(account=sender_wallet.classic_address, owner=escrow_creator, offer_sequence=seq, condition=condition, fulfillment=fulfillment)
        stxn = safe_sign_and_autofill_transaction(finish_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
            "result": stxn_result["meta"]["TransactionResult"], 
            "txid": stxn_result["hash"],
            "link": f"{self.txn_url}{stxn_result['hash']}"}
    
    def create_offer(self, sender_seed: str, pay: Union[float, IssuedCurrencyAmount], receive: Union[float, IssuedCurrencyAmount], expiry_date: Union[int, None]) -> dict:
        """create an offer"""
        result = ""
        hash = ""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)

        if isinstance(receive, float) and isinstance(pay, IssuedCurrencyAmount): # check if pay == xrp and receive == asset
            create_txn = OfferCreate(account=sender_wallet.classic_address, taker_pays=xrp_to_drops(receive), taker_gets=pay, expiration=expiry_date)
            stxn = safe_sign_and_autofill_transaction(create_txn, sender_wallet, self.client)
            stxn_response = send_reliable_submission(stxn, self.client)
            stxn_result = stxn_response.result
            result, hash = stxn_result["meta"]["TransactionResult"], stxn_result["hash"]
        if isinstance(receive, IssuedCurrencyAmount) and isinstance(pay, float): # check if pay == asset and receive == xrp
            create_txn = OfferCreate(account=sender_wallet.classic_address, taker_pays=receive, taker_gets=xrp_to_drops(pay), expiration=expiry_date)
            stxn = safe_sign_and_autofill_transaction(create_txn, sender_wallet, self.client)
            stxn_response = send_reliable_submission(stxn, self.client)
            stxn_result = stxn_response.result
            result, hash = stxn_result["meta"]["TransactionResult"], stxn_result["hash"]
        if isinstance(receive, IssuedCurrencyAmount) and isinstance(pay, IssuedCurrencyAmount): # check if pay and receive are == asset
            create_txn = OfferCreate(account=sender_wallet.classic_address, taker_pays=receive, taker_gets=pay, expiration=expiry_date)
            stxn = safe_sign_and_autofill_transaction(create_txn, sender_wallet, self.client)
            stxn_response = send_reliable_submission(stxn, self.client)
            stxn_result = stxn_response.result
            result, hash = stxn_result["meta"]["TransactionResult"], stxn_result["hash"]
        return {
        "result": result, 
        "txid": hash,
        "link": f"{self.txn_url}{hash}"}
    
    def account_offers(self, wallet_addr: str, limit: int = None) -> list:
        """return all offers an account created"""
        offer_list = []
        req = AccountOffers(account=wallet_addr, ledger_index="validated", limit=limit)
        response = self.client.request(req)
        result = response.result
        if "offers" in result:
            offers = result["offers"]
            for offer in offers:
                of = {}
                of["sequence"] = offer["seq"]
                # The exchange rate of the offer, as the ratio of the original taker_pays divided by the original taker_gets. rate = pay/get
                of["rate"] = offer["quality"]# str(drops_to_xrp(offer["quality"])) # rate is subject to error from the blockchain because xrp returned in this call has no decimal
                if isinstance(offer["taker_pays"], dict):
                    give_info = {}
                    give_info["asset"] = hex_to_symbol(offer["taker_pays"]["currency"])
                    give_info["issuer"] = offer["taker_pays"]["issuer"]
                    give_info["amount"] = offer["taker_pays"]["value"]
                    of["give"] = give_info
                elif isinstance(offer["taker_pays"], str):
                    of["give"] = str(drops_to_xrp(offer["taker_pays"]))

                if isinstance(offer["taker_gets"], dict):
                    get_info = {}
                    get_info["asset"] = hex_to_symbol(offer["taker_gets"]["currency"])
                    get_info["issuer"] = offer["taker_gets"]["issuer"]
                    get_info["amount"] = offer["taker_gets"]["value"]
                    of["get"] = get_info
                elif isinstance(offer["taker_gets"], str):
                    of["get"] = str(drops_to_xrp(offer["taker_gets"]))
                offer_list.append(of)
        return offer_list
    
    def cancel_offer(self, sender_seed: str, offer_seq: int) -> dict:
        """cancel an offer"""
        sender_wallet = Wallet(seed=sender_seed, sequence=0)
        cancel_txn = OfferCancel(account=sender_wallet.classic_address, offer_sequence=offer_seq)
        stxn = safe_sign_and_autofill_transaction(cancel_txn, sender_wallet, self.client)
        stxn_response = send_reliable_submission(stxn, self.client)
        stxn_result = stxn_response.result
        return {
        "result": stxn_result["meta"]["TransactionResult"], 
        "txid": stxn_result["hash"],
        "link": f"{self.txn_url}{stxn_result['hash']}"}

    def all_offers(self, give: Union[XRP, IssuedCurrency], get: Union[XRP, IssuedCurrency], limit: int = None) -> list:
        """returns all offers for 2 pairs"""
        all_offers_list = []
        req = BookOffers(taker_gets=get, taker_pays=give, ledger_index="validated", limit=limit)
        response = self.client.request(req)
        result = response.result
        if "offers" in result:
            offers = result["offers"]
            for offer in offers:
                of = {}
                of["creator"] = offer["Account"]
                of["offer_id"] = offer["index"]
                of["sequence"] = offer["Sequence"] # offer id
                # of["owner_funds"] = offer["owner_funds"] # Amount of the TakerGets currency the side placing the offer has available to be traded.
                if isinstance(offer["TakerPays"], dict):
                    give_info = {}
                    give_info["asset"] = hex_to_symbol(offer["TakerPays"]["currency"])
                    give_info["issuer"] = offer["TakerPays"]["issuer"]
                    give_info["amount"] = offer["TakerPays"]["value"]
                    of["give"] = give_info
                elif isinstance(offer["TakerPays"], str):
                    of["give"] = str(drops_to_xrp(offer["TakerPays"]))
                
                if isinstance(offer["TakerGets"], dict):
                    get_info = {}
                    get_info["asset"] = hex_to_symbol(offer["TakerGets"]["currency"])
                    get_info["issuer"] = offer["TakerGets"]["issuer"]
                    get_info["amount"] = offer["TakerGets"]["value"]
                    of["get"] = get_info
                elif isinstance(offer["TakerGets"], str):
                    of["get"] = str(drops_to_xrp(offer["TakerGets"]))
                all_offers_list.append(of)
        return all_offers_list

    def ticket():
        pass
    

o = xObject("https://s.altnet.rippletest.net:51234", "", "")    

# print(o.account_xrp_escrows("rPKcw5cXUtREMgsQZqSLkxJTfpwMGg7WcP"))

print(o.create_xrp_escrow("sEdThjCR5Vy2MNqN6hWkFr4NhK9Bnkn", 12.4, "rBZJzEisyXt2gvRWXLxHftFRkd1vJEpBQP", "A0258020FBBB5CD5055BC331FC7447E17714B6D460067E86DDC371A4A7B9C6A0F6967BAB810133", 714293084, None))
wall = Wallet(seed="sEdThjCR5Vy2MNqN6hWkFr4NhK9Bnkn", sequence=0)
print(wall.classic_address)

# print(o.account_xrp_escrows(("r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW")))

# print(datetime_to_ripple_time(datetime.datetime.now() + datetime.timedelta(days=1)))
