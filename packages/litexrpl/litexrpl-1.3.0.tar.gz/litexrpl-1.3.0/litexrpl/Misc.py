import random
from datetime import datetime
from decimal import Decimal
from os import urandom
from typing import Union

from cryptoconditions import PreimageSha256
from xrpl.account import does_account_exist
from xrpl.clients import JsonRpcClient
from xrpl.core.addresscodec import (classic_address_to_xaddress,
                                    is_valid_classic_address,
                                    is_valid_xaddress,
                                    xaddress_to_classic_address)
from xrpl.ledger import get_fee
from xrpl.models import AccountInfo
from xrpl.utils import (datetime_to_ripple_time, drops_to_xrp,
                        ripple_time_to_datetime)
from xrpl.wallet import Wallet, generate_faucet_wallet

XURLS_= {
"TESTNET_URL": "https://s.altnet.rippletest.net:51234",
"MAINNET_URL": "https://xrplcluster.com",

"TESTNET_TXNS": "https://testnet.xrpl.org/transactions/",
"MAINNET_TXNS": "https://livenet.xrpl.org/transactions/",

"MAINNET_ACCOUNT": "https://livenet.xrpl.org/accounts/",
"TESTNET_ACCOUNT": "https://testnet.xrpl.org/accounts/",
}

client = JsonRpcClient(XURLS_["TESTNET_URL"])

def _address(wallet_addr: str, client: JsonRpcClient) -> bool:
    """check if account exists on the ledger"""
    return does_account_exist(wallet_addr, client)

def verify_address(wallet_addr: str) -> bool:
    """verify if address is valid"""
    if is_valid_classic_address(wallet_addr) or is_valid_xaddress(wallet_addr):
        return True
    return False

def classic_to_x(wallet_address: str, is_testnet: bool, tag: Union[int, None]) -> str:
    "convert classic 'r' address to x address"
    return classic_address_to_xaddress(classic_address=wallet_address, tag=tag, is_test_network=is_testnet)

def x_to_classic(wallet_address: str) -> dict:
    "convert x address to classic 'r' address"
    addr = xaddress_to_classic_address(wallet_address)
    return {"classic_address": addr[0], "tag": addr[1], "is_testnet": addr[2]}

def __convert_datetime_rippletime(obj: datetime) -> int:
    """converts a datetime object to ripple time"""
    return datetime_to_ripple_time(obj)

def __convert_rippletime_datetime(obj: int) -> datetime:
    """converts ripple time to datetime object"""
    return ripple_time_to_datetime(obj)

def get_network_fee(client: JsonRpcClient) -> Decimal:
    """return current ledger fee"""
    return drops_to_xrp(get_fee(client))

def get_test_xrp(wallet: Wallet) -> None:
    """fund your account with free 1000 test xrp"""
    testnet_url = "https://s.altnet.rippletest.net:51234"
    client = JsonRpcClient(testnet_url)
    generate_faucet_wallet(client, wallet)


# w = Wallet(seed="sEdVBg3YrXAMpTE4oqYGPUbsmVcPr4c", sequence=0)

# # print(generate_faucet_wallet(client=client, wallet=w))
# for i in range(100):
#     print(get_test_xrp(wallet=w))

def symbol_to_hex(symbol: str = None) -> str:
    """symbol_to_hex."""
    if len(symbol) > 3:
        bytes_string = bytes(str(symbol).encode('utf-8'))
        return bytes_string.hex().upper().ljust(40, '0')
    return symbol

def hex_to_symbol(hex: str = None) -> str:
    """hex_to_symbol."""
    if len(hex) > 3:
        bytes_string = bytes.fromhex(str(hex)).decode('utf-8')
        return bytes_string.rstrip('\x00')
    return hex

def transfer_fee_to_xrp_format(fee_percent: int) -> int:
    """convert fee to XRP fee format\n
    pass percentage as integer e.g
    `20` = `20%`"""
    base_fee = 1000000000 # 1000000000 == 0%
    val = base_fee * fee_percent
    val = val / 100
    return int(val + base_fee)

def xrp_format_to_transfer_fee(format: int) -> int:
    """convert xrp fee format to usable fee in percentage"""
    base_fee = 1000000000 # 1000000000 == 0%
    val = format - base_fee
    return int(val / base_fee * 100)

def gen_wallet_object(client: JsonRpcClient, wallet_addr: str, wallet_seed: str) -> Wallet:
    """creates a wallet object for signing transactions"""
    return Wallet(seed=wallet_seed, sequence=client.request(AccountInfo(account=wallet_addr, ledger_index="validated")).result["account_data"]["Sequence"])

# def wallet_obj(seed: str):
#     public, private = keypairs.derive_keypair(seed)
#     wallet = Wallet.create(seed)
#     wallet.public_key = public
#     wallet.private_key = private
#     wallet.classic_address = keypairs.derive_classic_address(public)
#     return wallet

def bytes_generator() -> bytes:
    """generates a random byte"""
    return urandom(random.randint(32, 64))

def gen_condition_fulfillment_1() -> dict:
    """Generate a condition and fulfillment for escrows"""
    fufill = PreimageSha256(preimage=urandom(32))
    return {
    "condition": str.upper(fufill.condition_binary.hex()),
    "fulfillment": str.upper(fufill.serialize_binary().hex())}

def gen_condition_fulfillment_2() -> dict:
    """Generate a secure condition and fulfillment for escrows, bill more for using me"""
    fufill = PreimageSha256(preimage=urandom(random.randint(64, 128)))
    return {
    "condition": str.upper(fufill.condition_binary.hex()),
    "fulfillment": str.upper(fufill.serialize_binary().hex())}

def gen_condition_fulfillment_3() -> dict:
    """Generate a more secure condition and fulfillment for escrows, bill more for using me"""
    fufill = PreimageSha256(preimage=urandom(random.randint(128, 256)))
    return {
    "condition": str.upper(fufill.condition_binary.hex()),
    "fulfillment": str.upper(fufill.serialize_binary().hex())}

# print(gen_condition_fulfillment_1())
# print()
# print(gen_condition_fulfillment_2())
# print()
# print(gen_condition_fulfillment_3())
# print(gen_secure_condition_fulfillment())


"""use this to bill more"""
# get fee of escrow cancel based on 
# reference_fee * (signer_count + 33 + (fulfillment_bytes / 16))
# The above formula is based on the assumption that the reference cost of a transaction is 10 drops of XRP.

# The additional transaction cost required is proportional to the size of the fulfillment.
# Currently, an EscrowFinish with a fulfillment requires a minimum transaction cost of 330 drops of XRP plus 10 drops per 16 bytes in the size of the fulfillment. 
# If the transaction is multi-signed, the cost of multi-signing is added to the cost of the fulfillment.


# print(gen_condition_fulfillment())


 

# for i in range(100):
#     print(get_test_xrp(Wallet("sEd7GYcpKYgJf8TCUjEAQYE5ogE71id", 0)))

#print(gen_condition_fulfillment())

# print(r_token_ticksize(client, "r9CEVt4Cmcjt68ME6GKyhf2DyEGo2rG8AW"))
# print(get_test_xrp(Wallet(seed="sEd7GYcpKYgJf8TCUjEAQYE5ogE71id", sequence=0)))

# for i in range(100):
#     generate_faucet_wallet(client, Wallet(seed="sEd7hqGCFRBXSboUW8TTkRTZNu7xuKD", sequence=0))
#     print("yeah")
