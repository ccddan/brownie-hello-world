import pytest
from brownie import network, accounts, exceptions

from scripts.deploy import deploy_contract_fund_me
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_contract_fund_me()
    entrance_fee = fund_me.getEntranceFee()

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.funders(account.address) == entrance_fee

    tx = fund_me.withdraw({"from": account})
    tx.wait(1)
    assert fund_me.funders(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    fund_me = deploy_contract_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
