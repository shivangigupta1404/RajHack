import hashlib as hasher
import datetime as date

class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  
  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
    return sha.hexdigest()


class Blockchain:
  def __init__(self):
    chain = [create_genesis_block()]


  def create_genesis_block():
    # Manually construct a block with index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0")

  def last_block():
    return blockchain[-1]

  def add_block():
    block_to_add=get_next_block(last_block())
    blockchain.append(block_to_add)
    print "Block #{} has been added to the blockchain!".format(block_to_add.index)
    print "Hash: {}\n".format(block_to_add.hash)

  def get_next_block(last_block):
    #change implementation
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    return Block(this_index, this_timestamp, this_data, last_block.hash)
