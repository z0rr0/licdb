#-*- coding: utf-8 -*-
from key.models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.contrib import auth

def index(request, vtemplate):
    program = Program.objects.all().only('name')
    stat = []
    for po in program:
    	all = Key.objects.filter(program=po)
    	use = all.filter(use=True)
    	stat.append({'program': po.name, 
    		'all': all.count(), 
    		'use': use.count()})
    return TemplateResponse(request, vtemplate, {'statistics': stat})

