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
from key.forms import *

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

def licenses(request, vtemplate, typefree):
    u""" 
    Список лицензий
    """
    typetext = ''
    if typefree is None:
        object_list = License.objects.all()
    else:
        object_list = License.objects.filter(free=typefree)
        typetext =  u'беспланые' if typefree else u'коммерческие'
    return TemplateResponse(request, vtemplate, {'object_list': object_list, 'type': typetext})

def programs(request, prog, vtemplate, stud):
    u"""
    Программы
    """
    c = {}
    c.update(csrf(request))
    typetext = ''
    searchtext = ''
    if stud is None:
        object_list = Program.objects.all()
    else:
        object_list = Program.objects.filter(use_student=stud)
        typetext =  u'для студентов' if stud else u'не для студентов'
    if prog:
        object_list = object_list.filter(license=int(prog))
    if request.method == 'POST':
        searchtext = request.POST['progsearch']
        object_list = object_list.filter(name__icontains=searchtext)
    return TemplateResponse(request, vtemplate, {'object_list': object_list,
        'type': typetext,
        'searchtext': searchtext})

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

def get_obj_form(request, setobrj, SetForm):
    u"""
    Добавление или обновление данных об объектах 
    """
    saved = False
    if request.method == 'POST':
        form = SetForm(request.POST or None, request.FILES, instance=setobrj)
        if form.is_valid():
            with transaction.commit_on_success():
                setobrj = form.save()
                saved = True
    else:
        form = SetForm(instance=setobrj)
    return form, setobrj, saved

# license edit
@permission_required('key.change_license')
def license_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о лицензии 
    """
    c = {}
    c.update(csrf(request))
    license = get_object_or_404(License, id=int(id))
    form, license, saved = get_obj_form(request, license, LicenseForm)
    if saved:
        return redirect('/license/' + str(license.id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Редактирование'})

# license add
@permission_required('key.add_license')
def license_add(request, vtemplate):
    u""" 
    Добавление данных о лицензии 
    """
    c = {}
    c.update(csrf(request))
    form, license, saved = get_obj_form(request, None, LicenseForm)
    if saved:
        return redirect('/license/' + str(license.id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Добавление'})

# program edit
@permission_required('key.change_program')
def program_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о программе 
    """
    c = {}
    c.update(csrf(request))
    program = get_object_or_404(Program, id=int(id))
    form, program, saved = get_obj_form(request, program, ProgramForm)
    if saved:
        return redirect('/program/' + str(program.id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Редактирование'})

# license add
@permission_required('key.add_program')
def program_add(request, vtemplate):
    u""" 
    Добавление данных о программе 
    """
    c = {}
    c.update(csrf(request))
    form, program, saved = get_obj_form(request, None, ProgramForm)
    if saved:
        return redirect('/program/' + str(program.id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Добавление'})

# get license list by program ID
def get_keys(request, vtemplate, prog):
    u"""
    Получение списка ключей по номеру программы
    """
    if request.user.is_authenticated():
        keys = Key.objects.filter(program=int(prog))
    else:
        keys = None
    return TemplateResponse(request, vtemplate, {'keys': keys})
