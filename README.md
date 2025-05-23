# CyberCoin - Cryptocurrency Implementation

A complete cryptocurrency implementation featuring wallet management, transaction processing, blockchain mining, and validation using RSA digital signatures and SHA-256 hashing.

## Overview

CyberCoin is a educational cryptocurrency implementation that demonstrates core blockchain concepts including:
- Public/private key cryptography for wallet security
- Digital signatures for transaction authentication
- Proof-of-work mining with configurable difficulty
- Blockchain validation and integrity checking
- Mempool transaction management

## Features

### 🔐 Secure Wallet System
- **RSA 1024-bit** key pair generation
- **Text-based storage** using JSON format for cross-platform compatibility
- **Wallet tags** using first 16 characters of SHA-256 hash of public key
- **Digital signatures** for all transactions using RSA with SHA-256

### 💰 Transaction Processing
- **Transaction statements** with sender, receiver, amount, timestamp, and signature
- **Balance verification** before allowing transactions
- **Mempool management** for pending transactions
- **Special funding source** ("bigfoot") for initial wallet funding

### ⛏️ Mining & Blockchain
- **Proof-of-work mining** with configurable difficulty (leading zeros)
- **Genesis block** with custom message
- **Chain validation** ensuring proper hash linking between blocks
- **Nonce calculation** through brute-force method

### 📊 Balance & Validation
- **Real-time balance calculation** from blockchain and mempool
- **Complete blockchain validation** checking all block hashes
- **Transaction verification** with signature and fund availability checks

## Installation & Setup

### Prerequisites
- Python 3.x
- `rsa` Python package

### Install Dependencies
```bash
pip install rsa
```

### Setup Files
1. Save the main code as `cmoney.py`
2. Create shell script `cryptomoney.sh`:
   ```bash
   #!/bin/bash
   python3 cmoney.py $@
   ```
3. Make executable:
   ```bash
   chmod 755 cryptomoney.sh
   ```
4. Create `Makefile`:
   ```makefile
   main:
   	echo "CryptoCurrency build complete"
   ```

## Usage Guide

### Basic Commands

#### Get Cryptocurrency Name
```bash
./cryptomoney.sh name
# Output: CyberCoin
```

#### Create Genesis Block
```bash
./cryptomoney.sh genesis
# Output: Genesis block created in 'block_0.txt'
```

#### Generate Wallet
```bash
./cryptomoney.sh generate alice.wallet.txt
# Output: New wallet generated in 'alice.wallet.txt' with tag e1f3ec14abcb45da
```

#### Get Wallet Address
```bash
./cryptomoney.sh address alice.wallet.txt
# Output: e1f3ec14abcb45da
```

#### Fund Wallet
```bash
./cryptomoney.sh fund e1f3ec14abcb45da 100 funding.txt
# Output: Funded wallet e1f3ec14abcb45da with 100 CyberCoins on [timestamp]
```

#### Transfer Funds
```bash
./cryptomoney.sh transfer alice.wallet.txt d96b71971fbeec39 50 transfer.txt
# Output: Transferred 50 from alice.wallet.txt to d96b71971fbeec39 and the statement to 'transfer.txt' on [timestamp]
```

#### Verify Transaction
```bash
./cryptomoney.sh verify alice.wallet.txt transfer.txt
# Output: The transaction in file 'transfer.txt' with wallet 'alice.wallet.txt' is valid, and was written to the mempool
```

#### Check Balance
```bash
./cryptomoney.sh balance e1f3ec14abcb45da
# Output: 50
```

#### Mine Block
```bash
./cryptomoney.sh mine 2
# Output: Mempool transactions moved to block_1.txt and mined with difficulty 2 and nonce 1029
```

#### Validate Blockchain
```bash
./cryptomoney.sh validate
# Output: True
```

## Complete Example Workflow

```bash
# 1. Setup
./cryptomoney.sh genesis
./cryptomoney.sh generate alice.wallet.txt
./cryptomoney.sh generate bob.wallet.txt

# 2. Get wallet addresses
export alice=$(./cryptomoney.sh address alice.wallet.txt)
export bob=$(./cryptomoney.sh address bob.wallet.txt)

# 3. Fund wallets
./cryptomoney.sh fund $alice 100 alice-funding.txt
./cryptomoney.sh fund $bob 100 bob-funding.txt

# 4. Create transfers
./cryptomoney.sh transfer alice.wallet.txt $bob 25 alice-to-bob.txt
./cryptomoney.sh transfer bob.wallet.txt $alice 10 bob-to-alice.txt

# 5. Verify transactions (adds to mempool)
./cryptomoney.sh verify alice.wallet.txt alice-funding.txt
./cryptomoney.sh verify bob.wallet.txt bob-funding.txt
./cryptomoney.sh verify alice.wallet.txt alice-to-bob.txt
./cryptomoney.sh verify bob.wallet.txt bob-to-alice.txt

# 6. Check balances
./cryptomoney.sh balance $alice  # Should show 85
./cryptomoney.sh balance $bob    # Should show 115

# 7. Mine block and validate
./cryptomoney.sh mine 2
./cryptomoney.sh validate
```

## File Formats

### Wallet File (JSON)
```json
{
  "public_key": "-----BEGIN RSA PUBLIC KEY-----\n...",
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n..."
}
```

### Transaction Statement
```
From: e1f3ec14abcb45da
To: d96b71971fbeec39
Amount: 25
Date: Tue Apr 02 23:09:13 EDT 2019

[RSA signature in hex]
```

### Block File
```
[previous block hash]

[transaction line 1]
[transaction line 2]
...

nonce: [mining nonce]
```

### Mempool
```
bigfoot transferred 100 to e1f3ec14abcb45da on Tue Apr 02 23:09:01 EDT 2019
e1f3ec14abcb45da transferred 25 to d96b71971fbeec39 on Tue Apr 02 23:09:02 EDT 2019
```

## Security Features

- **RSA-1024 encryption** for wallet key pairs
- **SHA-256 hashing** for wallet addresses and blockchain integrity
- **Digital signatures** prevent transaction forgery
- **Balance verification** prevents overspending
- **Proof-of-work mining** secures the blockchain
- **Chain validation** ensures blockchain integrity

## Technical Details

### Mining Algorithm
- Uses proof-of-work with configurable difficulty
- Difficulty = number of leading zeros required in block hash
- Brute-force nonce finding (suitable for educational purposes)
- Mining clears mempool and creates new block

### Transaction Verification
1. Parse transaction statement format
2. Verify RSA digital signature
3. Check sender has sufficient balance
4. Add valid transactions to mempool

### Balance Calculation
- Processes all blocks in blockchain (block_1.txt, block_2.txt, etc.)
- Includes pending transactions in mempool
- Handles both incoming and outgoing transactions
- Special handling for "bigfoot" funding source

## Limitations & Assumptions

- **Educational purpose**: Not suitable for production use
- **Single file storage**: All code in one Python file
- **Text-based**: All data stored in human-readable format
- **Sequential blocks**: Assumes consecutive block numbering
- **Integer amounts**: No floating-point currency values
- **Basic mining**: Simple brute-force proof-of-work

## Error Handling

The implementation includes robust error handling for:
- Invalid transaction formats
- Insufficient funds
- Invalid signatures
- Missing files
- Corrupted blockchain data

## License

This implementation is for educational purposes as part of a cryptocurrency course assignment.

## Author

Created as part of a computer science cryptocurrency implementation assignment.