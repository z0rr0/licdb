#-*- coding: utf-8 -*-
from key.models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.contrib import auth

def index(request, vtemplate):
    latest_poll_list = License.objects.all().only('name')
    output = ', '.join([p.name for p in latest_poll_list])
    return TemplateResponse(request, vtemplate, {'output': output})

