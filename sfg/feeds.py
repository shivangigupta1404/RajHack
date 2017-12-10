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
      #image="/media/",text="random text",previous_hash=-1)

  def __init__(self):
    self.create_genesis_block()

  def add_block(self,data):
    last_block=Block.objects.latest('timestamp')
    b=Block()
    b.user=User.objects.get(username=data['user'])
    b.index=last_block.index+1
    b.timestamp=date.datetime.now()
    b.title=data['title']
    b.image=data['image']
    b.text=data['text']
    b.previous_hash=last_block.hash
    sha = hasher.sha256()
    a= str(b.user)+str(b.index)+str(b.timestamp)+str(b.title)+str(b.text)+str(b.image)+str(b.previous_hash)
    sha.update(a.encode())
    b.hash=sha.hexdigest()
    b.save()

blockchain= Blockchain()
