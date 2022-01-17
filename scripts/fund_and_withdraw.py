from brownie import FundMe

from scripts.utils import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    minimum = fund_me.getEntranceFee()

    print(f"Minimum entrance fee: {minimum}")
    print("Funding...")
    fund_me.fund({"from": account, "value": minimum})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
