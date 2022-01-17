// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract PriceConsumerV3 {
    uint256 gweiScale = 10000000000;
    AggregatorV3Interface internal priceFeed;

    constructor(address feedAddr) {
        priceFeed = AggregatorV3Interface(feedAddr);
    }

    function getLatestPrice() public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData();

        return uint256(uint256(price) * gweiScale); // USD
    }
}
