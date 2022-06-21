pragma solidity ^0.8.13;

contract Greeter {
    string public name;
    constructor(string memory _name) {
      name = _name;
    }

    function setName(string calldata _name) public {
        name = _name;
    }

    function greet() public view returns (string memory) {
        return string.concat("hello ", name);
      }
}
