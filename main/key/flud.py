#-*- coding: utf-8 -*-
from django.db.models import Q, F, Sum
from django.db import transaction
from datetime import datetime
import string, random

from main.settings import DEBUG
from key.models import *
from eis.models import *

def nodebug(fn):
	def wrapper(*args, **kwargs):
		if not DEBUG:
			print 'It is work with DEBUG only'
			return False
		else:
			fn(*args, **kwargs)
	return wrapper

# generation random key value
def gen_salt(size=15):
    chars = string.ascii_letters + string.digits * 5
    return ''.join(random.choice(chars) for x in range(size))

# create many keys for custom program
@nodebug
def key_generations(program=None, keys_count=50, useval=False):
	if not program:
		print "No program data"
		return False
	else:
		try:
			for i in range(keys_count):
				key_val = gen_salt()
				key = Key(
					program=program,
					key=key_val,
					use=useval,
					date_start=datetime.now().date(),
					manyuse=1,
					comment='Test genarations field'
					# attach: '',  net: False, date_end: Null,
				)
				key.save()
				print key
		except Key.DoesNotExist as err:
			print err
			return False
	print 'End function'
	return True

# search freedom keys
def key_clear(keys):
	obj_list = []
	for key in keys:
		# clients = Client.objects.filter(key=key).count()
		freekey = key.manyuse - key.client_set.count()
		if freekey>0 or key.manyuse==0:
			# добавить столько раз, сколько ключей еще осталось
			for i in range(freekey):
				obj_list.append(key)
	# перемешать
	random.shuffle(obj_list)
	return obj_list

# create many clients for custom program
@nodebug
def client_generations(program=None, client_count=50, studbool=True):
	if not program:
		print "No program data"
		return False
	else:
		try:
			keys = key_clear(Key.objects.filter(program=program))
			studs = [s for s in Student.objects.all()]
			klen = len(keys)
			slen = len(studs)
			cl_count = client_count if client_count <= klen else klen
			for i in range(cl_count):
				with transaction.commit_on_success():
					key = keys[i]
					student = studs[random.randint(0, slen-1)]
					client = Client(
						key=key,
						name=student.who,
						student=studbool,
						manyuse=1,
						date_start=datetime.now().date(),
						comment='Test genarations field'
					)
					# Если ключ еще не испльзовался то сделаем его таковым
					key.use = F('use') + 1
					key.save()
					client.save()
					print client
		except Client.DoesNotExist as err:
			print err
			return False
	print 'End function'
	return True
