from .models import *
import json
import datetime as date

class Blockchain:
  def create_genesis_block(self):
    if not Block.objects.all().exists():
      b=Block()
      b.index=0
      b.timestamp=date.datetime.now()
      b.title="Genesis Block"
      b.image="/media/"
      b.text="random text"
      b.previous_hash=-1
      sha = hasher.sha256()
      a= str(b.index)+str(b.timestamp)+str(b.title)+str(b.text)+str(b.image)+str(b.previous_hash)
      sha.update(a.encode())
      b.hash=sha.hexdigest()
      b.save()
      # return Block(index=0,title="Genesis Block",
      #     image="/media/",text="random text",previous_hash=-1)

  def __init__(self):
    self.create_genesis_block()

  def last_block(self):
    return Block.objects.latest('timestamp')

  # def get_next_block(self,last_block,data):
  #   this_index = last_block.index + 1
  #   this_timestamp = date.datetime.now()
  #   return Block(this_index, this_timestamp, data, last_block.hash)

  def add_block(self,data):
    # block_to_add=self.get_next_block(self.last_block(),data)
    # self.chain.append(block_to_add)
    # print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
    # print ("Hash: {}\n".format(block_to_add.hash))
    # return Block(index=last_block.index+1,title=data['title'],
    #       image=data['image'],text=data['text'],previous_hash=last_block.hash)
    last_block=self.last_block()
    b=Block()
    b.index=last_block.index+1
    b.timestamp=date.datetime.now()
    b.title=data['title']
    b.image=data['image']
    b.text=data['text']
    b.previous_hash=last_block.hash
    sha = hasher.sha256()
    a= str(b.index)+str(b.timestamp)+str(b.title)+str(b.text)+str(b.image)+str(b.previous_hash)
    sha.update(a.encode())
    b.hash=sha.hexdigest()
    b.save()

blockchain= Blockchain()