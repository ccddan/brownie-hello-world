# Brownie Hello World

Basic brownie project configuration with multi network deployment and Chainlink integration

# Requirements

- Python 3
- NodeJS ^12.0
- Infura project id
- Ether Scan Token

# Env Setup

Create python env

```bash
$ python3 -m venv .env-brownie
```

Install Ganache CLI

```bash
$ npm i -g ganache-cli
```

Install python dependencies

```bash
$ pip install -r requirements.dev.txt
$ pip install -r requirements.txt
```

Create new account

> **NOTE:** When asked for your private key, make sure to add the prefix `0x`, for example: `0x<private-key>`.

```bash
brownie accounts new my-account
```

Open `.vscode/settings.json` and change `<brownie-folder-path>` with the correct absolute path to the `.brownie` folder in your machine.

# Deployment

Start local blockchain (Ganache GUI) by selecting `QUICKSTART ETHEREUM`:

```bash
$ ganache
```

From Ganache GUI, get the following information and create a new network in brownie:

```bash
brownie networks add Ethereum ganache-local host=http://<rpc-server-ip>:<rpc-server-port> chainid=<network-id>
```

Rename `.env.local` to `.env` and replace the default values with your owns and deploy your contracts:

```bash
$ brownie compile
$ brownie test --network {rinkeby|ganache-local|mainnet-fork}
$ brownie run scripts/deploy.py -t --network {rinkeby|ganache-local|mainnet-fork}
```
