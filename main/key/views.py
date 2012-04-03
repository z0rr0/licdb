#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.db.models import Q, F, Sum
from django.db import transaction
from django.contrib import auth

from key.models import *
from key.forms import LicenseForm

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request, vtemplate):
    u""" 
    Главная страница 
    """
    program = Program.objects.filter(license__free=False).only('name')
    stat = []
    for po in program:
    	all = Key.objects.filter(program=po)
    	use = all.filter(use=True)
    	stat.append({'program': po.name, 
    		'all': all.count(), 
    		'use': use.count()})
    # logger.info(program)
    return TemplateResponse(request, vtemplate, {'statistics': stat})

# license delete
@permission_required('key.delete_license')
def obj_delete(request, id, redirecturl, model):
    u""" 
    Удалении данных об объекте 
    """
    obj = get_object_or_404(model, pk=int(id))
    if obj:
        with transaction.commit_on_success():
            obj.delete()
    return HttpResponseRedirect(redirecturl)

# object view
def obj_view(request, id, vtemplate, model):
    u""" 
    Просмотр данных об объекте 
    """
    obj = get_object_or_404(model, pk=int(id))
    return TemplateResponse(request, vtemplate, {'result': obj})


# license edit
@permission_required('key.change_license')
def license_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о лицензии 
    """
    c = {}
    c.update(csrf(request))
    license = get_object_or_404(License, id=int(id))
    if request.method == 'POST':
        pass
    else:
        form = LicenseForm(instance=license)
    return TemplateResponse(request, vtemplate, {'form': form})

