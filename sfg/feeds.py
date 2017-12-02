import hashlib as hasher
import datetime as date

class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.user = data[0]
    self.title= data[1]
    self.name = data[2]
    self.age  = data[3]
    self.sex  = data[4]   
    self.others =data[5]
    self.image  = data[6]
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  
  def hash_block(self):
    sha = hasher.sha256()
    a= str(self.index)+str(self.timestamp)+str(self.user)+ str(self.title)+str(self.name)+str(self.age)+str(self.sex)+str(self.others) + str(self.previous_hash)
    sha.update(a.encode())
    return sha.hexdigest()

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