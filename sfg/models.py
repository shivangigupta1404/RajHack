from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import hashlib as hasher
import base64

class Block:
	index=models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add=True)
	user = models.CharField(max_length=100, default=None)
	title  = models.CharField(max_length=250)
	name = models.CharField(max_length=150, default=None)
	age = models.IntegerField()
	sex = models.CharField(max_length=6)
	others = models.CharField(max_length=250, default=None,null=True)
	image = models.CharField(max_length=50000)


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
