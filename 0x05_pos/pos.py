import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.poser = {}
        self.staking_threhold = 100

    def staking_to_become_a_poser(self, poser_name, staking_money):
        if staking_money >= self.staking_threhold:
            self.poser[poser_name] = staking_money
            return self.poser
        else:
            return "you are not staking enough money!"
    
    def get_back_money(self, poser_name, money_he_want):
        if money_he_want >= 0:
            if poser_name in self.poser.keys():
                if self.poser[poser_name] >= money_he_want:
                    self.poser[poser_name] -= money_he_want
                    return self.poser
                else:
                    return "you are not staking enough money!"
            else:
                return "poser_name is invalid!"
        else:
            return "money could not be positive!"

    def new_block(self, poser_name, previous_hash=None):
        """
        创建一个新的区块到区块链中
        :param proof: <int> 由工作证明算法生成的证明
        :param previous_hash: (Optional) <str> 前一个区块的 hash 值
        :return: <dict> 新区块
        """
        if poser_name in self.poser.keys():
            if self.poser[poser_name] >= self.staking_threhold:
                block = {
                    'index': len(self.chain) + 1,
                    'timestamp': time(),
                    'transactions': self.current_transactions,
                    'previous_hash': previous_hash,
                }

                # 重置当前交易记录
                self.current_transactions = []
                self.chain.append(block)
                return block
            else:
                return "poser is not staking enough money!"
        else:
            return "poser_name is invalid!"

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
