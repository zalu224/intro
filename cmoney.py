#!/usr/bin/env python3

import sys
import os
import hashlib
import binascii
from datetime import datetime
import rsa
import json

class CryptoCurrency:
    def __init__(self):
        self.name = "ZeroCoin"
        self.bigfoot = "ZALU"  # Special funding source
        
    def get_name(self):
        """Print the name of the cryptocurrency"""
        print(self.name)
    
    def generate_genesis(self):
        """Create the genesis block"""
        genesis_content = [
            "0000000000000000000000000000000000000000000000000000000000000000",
            "",
            "In the beginning, there was Zerocoin - forged in the digital realm where trust meets cryptography.",
            "",
            "nonce: 0"
        ]
        
        with open('block_0.txt', 'w') as f:
            f.write('\n'.join(genesis_content))
        
        print("Genesis block created in 'block_0.txt'")
    
    def generate_wallet(self, filename):
        """Generate a new RSA wallet"""
        # Generate 1024-bit RSA key pair
        (public_key, private_key) = rsa.newkeys(1024)
        
        # Convert keys to PEM format and then to hex for text storage
        public_pem = public_key.save_pkcs1().decode('ascii')
        private_pem = private_key.save_pkcs1().decode('ascii')
        
        wallet_data = {
            'public_key': public_pem,
            'private_key': private_pem
        }
        
        # Save wallet as JSON
        with open(filename, 'w') as f:
            json.dump(wallet_data, f, indent=2)
        
        # Generate wallet tag (first 16 chars of SHA-256 hash of public key)
        tag = self.get_wallet_tag_from_file(filename)
        
        print(f"New wallet generated in '{filename}' with tag {tag}")
    
    def get_wallet_tag_from_file(self, filename):
        """Get wallet tag from wallet file"""
        with open(filename, 'r') as f:
            wallet_data = json.load(f)
        
        public_key_bytes = wallet_data['public_key'].encode('ascii')
        hash_obj = hashlib.sha256(public_key_bytes)
        return hash_obj.hexdigest()[:16]
    
    def get_address(self, filename):
        """Print wallet tag/address"""
        tag = self.get_wallet_tag_from_file(filename)
        print(tag)
    
    def fund_wallet(self, wallet_tag, amount, statement_file):
        """Fund a wallet (create funding transaction statement)"""
        timestamp = str(datetime.now())
        
        # Create transaction statement for funding
        transaction_statement = [
            f"From: {self.bigfoot}",
            f"To: {wallet_tag}",
            f"Amount: {amount}",
            f"Date: {timestamp}",
            ""
        ]
        
        with open(statement_file, 'w') as f:
            f.write('\n'.join(transaction_statement))
        
        print(f"Funded wallet {wallet_tag} with {amount} {self.name}s on {timestamp}")
    
    def transfer_funds(self, source_wallet_file, dest_wallet_tag, amount, statement_file):
        """Create a transfer transaction statement"""
        # Load source wallet
        with open(source_wallet_file, 'r') as f:
            wallet_data = json.load(f)
        
        # Get source wallet tag
        source_tag = self.get_wallet_tag_from_file(source_wallet_file)
        timestamp = str(datetime.now())
        
        # Create transaction data to sign
        transaction_data = [
            f"From: {source_tag}",
            f"To: {dest_wallet_tag}",
            f"Amount: {amount}",
            f"Date: {timestamp}"
        ]
        
        # Create message to sign
        message_to_sign = '\n'.join(transaction_data)
        
        # Load private key and sign
        private_key = rsa.PrivateKey.load_pkcs1(wallet_data['private_key'].encode('ascii'))
        signature = rsa.sign(message_to_sign.encode('ascii'), private_key, 'SHA-256')
        signature_hex = binascii.hexlify(signature).decode('ascii')
        
        # Create complete transaction statement
        transaction_statement = transaction_data + ['', signature_hex]
        
        with open(statement_file, 'w') as f:
            f.write('\n'.join(transaction_statement))
        
        print(f"Transferred {amount} from {source_wallet_file} to {dest_wallet_tag} and the statement to '{statement_file}' on {timestamp}")
    
    def calculate_balance(self, wallet_tag):
        """Calculate balance from blockchain and mempool"""
        balance = 0
        
        # Check all blocks in blockchain
        block_num = 1  # Start from block 1 (skip genesis)
        while os.path.exists(f'block_{block_num}.txt'):
            with open(f'block_{block_num}.txt', 'r') as f:
                lines = f.readlines()
            
            # Process transaction lines (skip first line which is previous hash, and last line which is nonce)
            for line in lines[1:-1]:
                line = line.strip()
                if line and 'transferred' in line:
                    balance += self._process_transaction_line(line, wallet_tag)
            
            block_num += 1
        
        # Check mempool
        if os.path.exists('mempool.txt'):
            with open('mempool.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and 'transferred' in line:
                        balance += self._process_transaction_line(line, wallet_tag)
        
        print(balance)
    
    def _process_transaction_line(self, line, wallet_tag):
        """Process a single transaction line and return balance change"""
        # Parse transaction line: "sender transferred amount to receiver on date"
        parts = line.split(' transferred ')
        if len(parts) != 2:
            return 0
        
        sender = parts[0]
        rest = parts[1].split(' to ')
        if len(rest) != 2:
            return 0
        
        amount_str = rest[0]
        receiver_part = rest[1].split(' on ')[0]
        
        try:
            amount = int(amount_str)
        except ValueError:
            return 0
        
        balance_change = 0
        if receiver_part == wallet_tag:
            balance_change += amount
        if sender == wallet_tag:
            balance_change -= amount
        
        return balance_change
    
    def verify_transaction(self, wallet_file, statement_file):
        """Verify a transaction statement and add to mempool if valid"""
        with open(statement_file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        
        # Parse transaction statement
        from_line = next((line for line in lines if line.startswith('From: ')), '')
        to_line = next((line for line in lines if line.startswith('To: ')), '')
        amount_line = next((line for line in lines if line.startswith('Amount: ')), '')
        date_line = next((line for line in lines if line.startswith('Date: ')), '')
        
        if not all([from_line, to_line, amount_line, date_line]):
            print(f"Invalid transaction format in '{statement_file}'")
            return
        
        sender = from_line.replace('From: ', '')
        receiver = to_line.replace('To: ', '')
        amount = int(amount_line.replace('Amount: ', ''))
        date = date_line.replace('Date: ', '')
        
        # Check if this is a funding transaction (from bigfoot)
        if sender == self.bigfoot:
            # Add to mempool without signature verification
            transaction_line = f"{sender} transferred {amount} to {receiver} on {date}"
            self._add_to_mempool(transaction_line)
            print("Any funding request (i.e., from bigfoot) is considered valid; written to the mempool")
            return
        
        # For regular transactions, verify signature and balance
        signature_hex = lines[-1] if lines else ''
        
        # Verify signature
        try:
            with open(wallet_file, 'r') as f:
                wallet_data = json.load(f)
            
            public_key = rsa.PublicKey.load_pkcs1(wallet_data['public_key'].encode('ascii'))
            
            # Reconstruct message that was signed
            message_lines = []
            for line in lines:
                if line and not line.startswith('From: ') and not line.startswith('To: ') and \
                   not line.startswith('Amount: ') and not line.startswith('Date: ') and line != signature_hex:
                    continue
                if line.startswith('From: ') or line.startswith('To: ') or \
                   line.startswith('Amount: ') or line.startswith('Date: '):
                    message_lines.append(line)
            
            message = '\n'.join(message_lines)
            signature_bytes = binascii.unhexlify(signature_hex)
            
            rsa.verify(message.encode('ascii'), signature_bytes, public_key)
            
            # Check balance
            current_balance = self._get_balance_for_verification(sender)
            if current_balance < amount:
                print(f"Insufficient funds for transaction in '{statement_file}'")
                return
            
            # Add to mempool
            transaction_line = f"{sender} transferred {amount} to {receiver} on {date}"
            self._add_to_mempool(transaction_line)
            print(f"The transaction in file '{statement_file}' with wallet '{wallet_file}' is valid, and was written to the mempool")
            
        except Exception as e:
            print(f"Invalid signature or verification error for '{statement_file}': {str(e)}")
    
    def _get_balance_for_verification(self, wallet_tag):
        """Get balance for verification (similar to calculate_balance but returns int)"""
        balance = 0
        
        # Check all blocks in blockchain
        block_num = 1
        while os.path.exists(f'block_{block_num}.txt'):
            with open(f'block_{block_num}.txt', 'r') as f:
                lines = f.readlines()
            
            for line in lines[1:-1]:
                line = line.strip()
                if line and 'transferred' in line:
                    balance += self._process_transaction_line(line, wallet_tag)
            
            block_num += 1
        
        # Check mempool
        if os.path.exists('mempool.txt'):
            with open('mempool.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and 'transferred' in line:
                        balance += self._process_transaction_line(line, wallet_tag)
        
        return balance
    
    def _add_to_mempool(self, transaction_line):
        """Add transaction line to mempool"""
        with open('mempool.txt', 'a') as f:
            f.write(transaction_line + '\n')
    
    def mine_block(self, difficulty):
        """Mine a new block with given difficulty"""
        # Find the next block number
        block_num = 1
        while os.path.exists(f'block_{block_num}.txt'):
            block_num += 1
        
        # Get hash of previous block
        prev_block_file = f'block_{block_num - 1}.txt'
        prev_hash = self._get_file_hash(prev_block_file)
        
        # Read mempool transactions
        transactions = []
        if os.path.exists('mempool.txt'):
            with open('mempool.txt', 'r') as f:
                transactions = [line.strip() for line in f.readlines() if line.strip()]
        
        # Find nonce with required difficulty
        nonce = 0
        target_prefix = '0' * difficulty
        
        while True:
            # Create block content
            block_lines = [prev_hash] + [''] + transactions + [''] + [f'nonce: {nonce}']
            block_content = '\n'.join(block_lines)
            
            # Calculate hash
            block_hash = hashlib.sha256(block_content.encode('ascii')).hexdigest()
            
            if block_hash.startswith(target_prefix):
                # Found valid nonce
                break
            
            nonce += 1
        
        # Write new block
        new_block_file = f'block_{block_num}.txt'
        with open(new_block_file, 'w') as f:
            f.write(block_content)
        
        # Clear mempool
        if os.path.exists('mempool.txt'):
            os.remove('mempool.txt')
        
        print(f"Mempool transactions moved to {new_block_file} and mined with difficulty {difficulty} and nonce {nonce}")
    
    def _get_file_hash(self, filename):
        """Get SHA-256 hash of a file"""
        with open(filename, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def validate_blockchain(self):
        """Validate the entire blockchain"""
        # If only genesis block exists, it's valid
        if not os.path.exists('block_1.txt'):
            print("True")
            return
        
        block_num = 1
        while os.path.exists(f'block_{block_num}.txt'):
            # Read current block
            with open(f'block_{block_num}.txt', 'r') as f:
                lines = f.readlines()
            
            if not lines:
                print("False")
                return
            
            # Get claimed previous hash (first line)
            claimed_prev_hash = lines[0].strip()
            
            # Calculate actual hash of previous block
            prev_block_file = f'block_{block_num - 1}.txt'
            actual_prev_hash = self._get_file_hash(prev_block_file)
            
            if claimed_prev_hash != actual_prev_hash:
                print("False")
                return
            
            block_num += 1
        
        print("True")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cmoney.py <command> [args...]")
        return
    
    crypto = CryptoCurrency()
    command = sys.argv[1]
    
    if command == "name":
        crypto.get_name()
    elif command == "genesis":
        crypto.generate_genesis()
    elif command == "generate" and len(sys.argv) == 3:
        crypto.generate_wallet(sys.argv[2])
    elif command == "address" and len(sys.argv) == 3:
        crypto.get_address(sys.argv[2])
    elif command == "fund" and len(sys.argv) == 5:
        crypto.fund_wallet(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif command == "transfer" and len(sys.argv) == 6:
        crypto.transfer_funds(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5])
    elif command == "balance" and len(sys.argv) == 3:
        crypto.calculate_balance(sys.argv[2])
    elif command == "verify" and len(sys.argv) == 4:
        crypto.verify_transaction(sys.argv[2], sys.argv[3])
    elif command == "mine" and len(sys.argv) == 3:
        crypto.mine_block(int(sys.argv[2]))
    elif command == "validate":
        crypto.validate_blockchain()
    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    main()