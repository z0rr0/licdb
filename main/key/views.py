#-*- coding: utf-8 -*-
from key.models import *
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.db import transaction
from django.contrib import auth

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# home page
def index(request, vtemplate):
    program = Program.objects.filter(license__free=False).only('name')
    stat = []
    for po in program:
    	all = Key.objects.filter(program=po)
    	use = all.filter(use=True)
    	stat.append({'program': po.name, 
    		'all': all.count(), 
    		'use': use.count()})
    logger.info(program)
    return TemplateResponse(request, vtemplate, {'statistics': stat})

# license delete
@permission_required('key.delete_license')
@transaction.autocommit
def license_delete(request, id, redirecturl):
    license = get_object_or_404(License, pk=int(id))
    if license:
         license.delete()
    return HttpResponseRedirect(redirecturl)

