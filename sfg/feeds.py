import hashlib as hasher
import datetime as date
from .models import *


class Blockchain:
  def create_genesis_block(self):
    return Block(0, date.datetime.now(), "Genesis Block", "0")

  def __init__(self):
    self.chain = [self.create_genesis_block()]

  def last_block(self):
    return self.chain[-1]

  def get_next_block(self,last_block,data):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    return Block(this_index, this_timestamp, data, last_block.hash)

  def add_block(self,data):
    block_to_add=self.get_next_block(self.last_block(),data)
    self.chain.append(block_to_add)
    print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print ("Hash: {}\n".format(block_to_add.hash))

blockchain= Blockchain()