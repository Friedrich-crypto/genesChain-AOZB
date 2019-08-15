pragma solidity ^0.4.24;

import "./MintableToken.sol";

contract CappedToken is MintableToken {

  uint256 public cap;

  constructor(uint256 _cap) public {
    require(_cap > 0);
    cap = _cap;
  }

  function mint(
    address _to,
    uint256 _amount
  )
    public
    returns (bool)
  {
    require(totalSupply().add(_amount) <= cap);

    return super.mint(_to, _amount);
  }

}
