from brownie import FundMe, config

from scripts.utils import get_account, get_deployment_network, get_eth_usd_feed_address


def deploy_contract_fund_me():
    deployment_network = get_deployment_network()
    account = get_account(deployment_network)

    fund_me = FundMe.deploy(
        get_eth_usd_feed_address(
            account=account, deployment_network=deployment_network
        ),
        {"from": account},
        publish_source=False,
    )

    if config["networks"][deployment_network]["verify"]:
        FundMe.publish_source(fund_me, silent=False)

    print("Contract deployed to:", fund_me.address)

    return fund_me


def main():
    deploy_contract_fund_me()
