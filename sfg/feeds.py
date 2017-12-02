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
    a= str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
    sha.update(a.encode())
    return sha.hexdigest()

class Blockchain:
  def create_genesis_block(self):
    return Block(0, date.datetime.now(), "Genesis Block", "0")

  def __init__(self):
    self.chain = [self.create_genesis_block()]

  def last_block(self):
    return self.chain[-1]

  def get_next_block(self,last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    return Block(this_index, this_timestamp, this_data, last_block.hash)

  def add_block(self,data):
    block_to_add=self.get_next_block(self.last_block())
    self.chain.append(block_to_add)
    print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print ("Hash: {}\n".format(block_to_add.hash))

blockchain= Blockchain()

