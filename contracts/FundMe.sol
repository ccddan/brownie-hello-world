// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./PriceConsumerV3.sol";

contract FundMe {
    address owner;
    PriceConsumerV3 feed;
    mapping(address => uint256) public funders;
    address[] fundersList = new address[](0); // empty list

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only account owner is allowed to perform this operation"
        );
        _;
    }

    constructor(address ethUSDFeedAddrs) {
        owner = msg.sender; // who deployed the contract is the owner automatically
        feed = new PriceConsumerV3(ethUSDFeedAddrs);
    }

    function fund() public payable {
        require(
            getConversionRate(msg.value) >= getEntranceFee(),
            "Minimum ETH is $5 (USD)"
        );
        funders[msg.sender] += msg.value;
        fundersList.push(msg.sender);
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 idx = 0; idx < fundersList.length; idx++) {
            funders[fundersList[idx]] = 0;
        }
        fundersList = new address[](0);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = feed.getLatestPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;

        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18; // 5 USD represented in wei
        uint256 price = feed.getLatestPrice();
        uint256 precision = 1 * 10**18;

        return (minimumUSD * precision) / price;
    }
}
