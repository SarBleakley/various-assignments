from __future__ import unicode_literals
import re, bcrypt
from django.db import models

class userManager(models.Manager):
	def validate(self, postData):
		flag = False
		errors = {}
		if not postData['f_name'] or not postData['alias'] or not postData['email'] or not postData['password'] or not postData['c_password']:
			flag = True
			errors = {}
		if postData['password'] != postData['c_password']:
			errors['message_2'] = "Your passwords don't match."

		if not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
			flag = True
			errors['message_3'] = "Please enter a valid email."

		if flag:
			return (flag, errors)
		else:
			hashed = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
			
			User.objects.create(f_name = postData['f_name'], alias = postData['alias'], email = postData['email'], password = hashed)
			return(flag, "gratz")

class Poke(models.Model):
	# probably one more for the self user poking?
	poked = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
	f_name = models.CharField(max_length = 55)
	alias = models.CharField(max_length = 55)
	email = models.CharField(max_length = 55)
	password = models.CharField(max_length = 100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = userManager() 





# Create your models here.
