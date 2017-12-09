from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import hashlib as hasher
import base64

class Block(models.Model):
	index=models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add=True)
	title  = models.CharField(max_length=250)
	image = models.CharField(max_length=5000)
	text = models.CharField(max_length=50000)
	previous_hash=models.CharField(max_length=256)
	hash=models.CharField(max_length=256)

	# def __init__(self,index,title,image,text,previous_hash):
	# 	self.index = index
	# 	self.timestamp =date.datetime.now()
	# 	self.title= title  
	# 	self.image  = image
	# 	self.text=text
	# 	self.previous_hash = previous_hash
	# 	self.hash = self.hash_block()
	# 	self.save()

	# def hash_block(self):
	# 	sha = hasher.sha256()
	# 	a= str(self.index)+str(self.timestamp)+str(self.title)+str(self.text)+str(self.image)+str(self.previous_hash)
	# 	sha.update(a.encode())
	# 	return sha.hexdigest()

	def __unicode__(self):
		return unicode(self.text)
