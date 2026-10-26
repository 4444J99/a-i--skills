# Smart Contract Patterns

## Access Control

### Ownable (Single Admin)

```solidity
// Simplest pattern - one owner
address public owner;

modifier onlyOwner() {
    require(msg.sender == owner, "Not owner");
    _;
}

function transferOwnership(address newOwner) external onlyOwner {
    owner = newOwner;
}
```

### Role-Based Access

```solidity
// Multiple roles with different permissions
mapping(bytes32 => mapping(address => bool)) private _roles;

bytes32 public constant ADMIN_ROLE = keccak256("ADMIN");
bytes32 public constant MINTER_ROLE = keccak256("MINTER");

modifier onlyRole(bytes32 role) {
    require(_roles[role][msg.sender], "Missing role");
    _;
}

function grantRole(bytes32 role, address account) external onlyRole(ADMIN_ROLE) {
    _roles[role][account] = true;
}
```

---

## Upgrade Patterns

### Proxy Pattern

```
User → Proxy (storage) → Implementation (logic)
              ↓
         delegatecall
```

- Storage lives in proxy
- Logic can be swapped
- Address stays same

### Transparent Proxy

```solidity
// Admin calls go to proxy logic
// User calls go to implementation
function _fallback() internal {
    if (msg.sender == admin) {
        // Handle admin functions
    } else {
        // Delegate to implementation
        _delegate(implementation);
    }
}
```

### UUPS (Universal Upgradeable Proxy Standard)

```solidity
// Upgrade logic lives in implementation
function upgradeTo(address newImplementation) external onlyOwner {
    _authorizeUpgrade(newImplementation);
    _upgradeTo(newImplementation);
}
```

---

## Economic Patterns

### Pull Over Push

```solidity
// BAD: Push payments (can fail, DoS risk)
function distributeRewards(address[] calldata users) external {
    for (uint i = 0; i < users.length; i++) {
        payable(users[i]).transfer(amount); // Can fail!
    }
}

// GOOD: Pull payments (users withdraw)
mapping(address => uint256) public rewards;

function claimRewards() external {
    uint256 amount = rewards[msg.sender];
    rewards[msg.sender] = 0;
    payable(msg.sender).transfer(amount);
}
```

### Commit-Reveal

```solidity
// Phase 1: Commit (hidden)
mapping(address => bytes32) public commits;

function commit(bytes32 hash) external {
    commits[msg.sender] = hash;
}

// Phase 2: Reveal (after commit phase ends)
function reveal(uint256 value, bytes32 salt) external {
    require(keccak256(abi.encodePacked(value, salt)) == commits[msg.sender]);
    // Process revealed value
}
```

### Time Locks

```solidity
struct TimeLock {
    uint256 amount;
    uint256 unlockTime;
}

mapping(address => TimeLock) public locks;

function lock(uint256 duration) external payable {
    locks[msg.sender] = TimeLock(msg.value, block.timestamp + duration);
}

function unlock() external {
    TimeLock memory userLock = locks[msg.sender];
    require(block.timestamp >= userLock.unlockTime, "Still locked");
    delete locks[msg.sender];
    payable(msg.sender).transfer(userLock.amount);
}
```

---

## Security Patterns

### Reentrancy Guard

```solidity
uint256 private _status = 1;
uint256 private constant _ENTERED = 2;

modifier nonReentrant() {
    require(_status != _ENTERED, "Reentrant call");
    _status = _ENTERED;
    _;
    _status = 1;
}
```

### Checks-Effects-Interactions

```solidity
function withdraw(uint256 amount) external nonReentrant {
    // 1. CHECKS
    require(balances[msg.sender] >= amount, "Insufficient");
    
    // 2. EFFECTS (update state)
    balances[msg.sender] -= amount;
    
    // 3. INTERACTIONS (external calls)
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### Pausable

```solidity
bool public paused;

modifier whenNotPaused() {
    require(!paused, "Paused");
    _;
}

function pause() external onlyOwner {
    paused = true;
}

function unpause() external onlyOwner {
    paused = false;
}
```

---

## Token Patterns

### Mintable Token

```solidity
function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
    _totalSupply += amount;
    _balances[to] += amount;
    emit Transfer(address(0), to, amount);
}
```

### Burnable Token

```solidity
function burn(uint256 amount) external {
    require(_balances[msg.sender] >= amount);
    _balances[msg.sender] -= amount;
    _totalSupply -= amount;
    emit Transfer(msg.sender, address(0), amount);
}
```

### Capped Supply

```solidity
uint256 public constant MAX_SUPPLY = 1_000_000 * 10**18;

function mint(address to, uint256 amount) external {
    require(_totalSupply + amount <= MAX_SUPPLY, "Cap exceeded");
    // ... mint logic
}
```

### Snapshot

```solidity
// Capture balances at specific points for voting/airdrops
mapping(uint256 => mapping(address => uint256)) private _snapshotBalances;
uint256 private _currentSnapshotId;

function snapshot() external returns (uint256) {
    _currentSnapshotId++;
    // ... capture current balances
    return _currentSnapshotId;
}

function balanceOfAt(address account, uint256 snapshotId) external view returns (uint256) {
    return _snapshotBalances[snapshotId][account];
}
```

---

## Gas Optimization

### Packed Storage

```solidity
// BAD: 3 storage slots
uint256 a;  // slot 0
uint256 b;  // slot 1  
uint256 c;  // slot 2

// GOOD: 1 storage slot (if values fit)
uint128 a;  // slot 0 (first half)
uint64 b;   // slot 0 (next quarter)
uint64 c;   // slot 0 (last quarter)
```

### Short-Circuit

```solidity
// Check cheap conditions first
require(amount > 0 && balances[msg.sender] >= amount);
//       ^^^ cheap            ^^^ storage read (expensive)
```

### Cache Storage Reads

```solidity
// BAD: Multiple storage reads
function bad() external {
    doSomething(storageVar);
    doMore(storageVar);  // reads again
}

// GOOD: Cache in memory
function good() external {
    uint256 cached = storageVar;  // one read
    doSomething(cached);
    doMore(cached);
}
```

---

## Events

### Indexed Parameters

```solidity
// Up to 3 indexed params (searchable)
event Transfer(
    address indexed from,    // Can filter by sender
    address indexed to,      // Can filter by recipient
    uint256 amount           // Not indexed, in data
);
```

### Event Design

```solidity
// Include enough context to reconstruct state
event OrderFilled(
    bytes32 indexed orderId,
    address indexed maker,
    address indexed taker,
    uint256 makerAmount,
    uint256 takerAmount,
    uint256 timestamp
);
```
