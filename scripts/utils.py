from os import environ
from typing import Optional, Union

from brownie import MockV3Aggregator, accounts, config, network
from brownie.network.account import LocalAccount, PublicKeyAccount

FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

ETHUSD_FEED_DECIMALS = 8
ETHUSD_FEED_VALUE = 200000000000  # 2,000 USD


def get_deployment_network():
    deployment_network = network.show_active()
    print(f"get_deployment_network::Deployment Network - {deployment_network}")
    return deployment_network


def get_account(deployment_network: Optional[str] = None):
    print(f"get_account::params - deployment_network: {deployment_network}")
    if not deployment_network:
        deployment_network = get_deployment_network()

    if (
        deployment_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or deployment_network in FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        account = accounts[0]
    else:
        account = accounts.load(environ["ACCOUNT_NAME"])

    print(f"get_account::account - {account}")

    return account


def get_eth_usd_feed_address(
    account: Optional[Union[LocalAccount, PublicKeyAccount]] = None,
    deployment_network: Optional[str] = None,
):
    print(f"get_eth_usd_feed_address::params - account: {account}")
    print(
        f"get_eth_usd_feed_address::params - deployment_network: {deployment_network}"
    )

    if not deployment_network:
        deployment_network = get_deployment_network()

    if deployment_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if not account:
            raise Exception(
                f"'account' param is required when deploying to development network"
            )

        if len(MockV3Aggregator) == 0:
            print(f"get_eth_usd_feed_address::Deploying aggregator mock...")
            aggregator = MockV3Aggregator.deploy(
                ETHUSD_FEED_DECIMALS,
                ETHUSD_FEED_VALUE,
                {"from": account},
            )
        else:
            print(f"get_eth_usd_feed_address::Fetching last deployed aggregator...")
            aggregator = MockV3Aggregator[-1]

        print(f"get_eth_usd_feed_address::Mock aggregator ready")
        addr = aggregator.address

    else:
        if deployment_network not in config["networks"]:
            raise Exception(
                f"Not ETH/USD price feed address has been defined for this network: {deployment_network}"
            )
        addr = config["networks"][deployment_network]["eth_usd_price_feed_addr"]

    print(f"get_eth_usd_feed_address::ETH/USD price feed aggregator addr: {addr}")
    return addr
