import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.last_nonce = 0

    def new_block(self, nonce, previous_hash=None):
        """
        创建一个新的区块到区块链中
        :param proof: <int> 由工作证明算法生成的证明
        :param previous_hash: (Optional) <str> 前一个区块的 hash 值
        :return: <dict> 新区块
        """

        if self.valid_proof(self.last_nonce, nonce) == True:
            block = {
                 'index': len(self.chain) + 1,
                 'timestamp': time(),
                 'transactions': self.current_transactions,
                 'last_nonce': nonce,
                 'previous_hash': previous_hash,
            }

             # 重置当前交易记录
            self.current_transactions = []

            self.last_nonce = nonce # 更新last_nonce
            self.chain.append(block)
            return block
        else:
            return "nonce(proof) is invalid!"

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
    @staticmethod
    def hash(block):
        """
        给一个区块生成 SHA-256 值
        :param block: <dict> Block
        :return: <str>
        """

        # 我们必须确保这个字典（区块）是经过排序的，否则我们将会得到不一致的散列
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
      
    def proof_of_work(self, last_nonce):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous nonce, and p' is the new nonce
        :param last_nonce: <int>
        :return: <int>
        """

        nonce = 0
        while self.valid_proof(last_nonce, nonce) is False:
            nonce += 1
            
        return nonce

    @staticmethod
    def valid_proof(last_nonce, nonce):
        """
        Validates the Proof: Does hash(last_nonce, nonce) contain 4 leading zeroes?
        :param last_nonce: <int> Previous Proof
        :param nonce: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
