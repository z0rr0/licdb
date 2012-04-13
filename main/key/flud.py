#-*- coding: utf-8 -*-
from django.db.models import Q, F, Sum
from django.db import transaction
from datetime import datetime
import string, random

from key.models import *
from eis.models import *

def gen_salt(size=15):
    chars = string.ascii_letters + string.digits * 5
    return ''.join(random.choice(chars) for x in range(size))


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

def key_clear(keys):
	obj_list = []
	for key in keys:
		clients = Client.objects.filter(key=key).count()
		freekey = key.manyuse - clients
		if freekey>0 or key.manyuse==0:
			for i in range(freekey):
				obj_list.append(key)
	# перемешать
	random.shuffle(obj_list)
	return obj_list

def client_generations(program=None, client_count=50, studbool=True):
	if not program:
		print "No program data"
		return False
	else:
		try:
			keys = key_clear(Key.objects.filter(program=program, use=False))
			studs = [s for s in Student.objects.all()]
			klen = len(keys)
			slen = len(studs)
			cl_count = client_count if client_count <= klen else klen
			for i in range(cl_count):
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
				client.save()
				print client
		except Client.DoesNotExist as err:
			print err
			return False
	print 'End function'
	return True
