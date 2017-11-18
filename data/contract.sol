pragma solidity ^0.4.18;


/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}


/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
  address public owner;


  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);


  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  function Ownable() internal {
    owner = msg.sender;
  }


  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }


  /**
   * @dev Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) onlyOwner public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }

}

contract DocLedger is Ownable {
    using SafeMath for uint256;
    
    event DocCreated(address creator, bytes32 hash);
    event DocOutdated(bytes32 hash);
    
    enum State { Empty, Active, Outdated }
    
    struct Doc {
        address creator;
        State state;
    }
    
    mapping(bytes32 => Doc) public docs;
    
    mapping(address => bool) registered;
    
    
    modifier onlyRegistered() {
        require(registered[msg.sender]);
        _;
    }
    
    function register(address user) onlyOwner public {
        require(user != 0x0);
        
        registered[user] = true;
    }
    
    function unregister(address user) onlyOwner public {
        require(user != 0x0);
        
        registered[user] = false;
    }
    
    function createDoc(bytes32 hash) onlyRegistered public {
        require(docs[hash].state == State.Empty);
        
        docs[hash] = Doc(msg.sender, State.Active);
        DocCreated(msg.sender, hash);
    }
    
    function outdateDoc(bytes32 hash) onlyRegistered public {
        require(docs[hash].state == State.Active);
        require(msg.sender == docs[hash].creator);
        
        docs[hash].state = State.Outdated;
        DocOutdated(hash);
    }
}

