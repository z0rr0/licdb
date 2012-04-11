#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.db.models import Q, F, Sum
from django.db import transaction
from django.contrib import auth

from filetransfers.api import serve_file

from main.settings import LEN_SALT
from key.models import *
from key.forms import *

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# home page
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

# license list
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

# keys list by program
@login_required
def keys(request, vtemplate):
    u"""
    Список всех ключей - главная страница
    """
    try:
        if 'prog' in request.GET:
            prog = int(request.GET['prog'])
        else:
            prog = 0
    except (KeyError, ValueError) as err:
        prog = 0
    form = ProgSelForm(initial={'programma': prog})
    return TemplateResponse(request, vtemplate, {'form': form})

# search keys by program in ajax
def keys_by_program(request, vtemplate):
    u"""
    поиск списка ключей по программе, Ajax
    """
    if request.user.is_authenticated():
        object_list = Program.objects.all()
        try:
            if 'prog' in request.GET:
                prog = int(request.GET['prog'])
                if prog:
                    object_list = object_list.filter(id=prog)
        except (KeyError, ValueError) as err:
            pass
        for obj in object_list:
            obj.stat = key_get_stat(obj.id)
    else:
        return HttpResponseNotFound('Auth error')
    return TemplateResponse(request, vtemplate, {'object_list': object_list})

# program list
def programs(request, lic, vtemplate, stud):
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
    if lic:
        lic = get_object_or_404(Program, pk=int(lic))
        object_list = object_list.filter(license=lic)
    if request.method == 'POST':
        searchtext = request.POST['progsearch']
        object_list = object_list.filter(name__icontains=searchtext)
    return TemplateResponse(request, vtemplate, {'object_list': object_list,
        'type': typetext,
        'lic': lic,
        'searchtext': searchtext})
 
# delete object on page
@login_required
def obj_delete(request, id, redirecturl, model, perm):
    u""" 
    Удалении данных об объекте 
    """
    if request.user.has_perm(perm):
        obj = get_object_or_404(model, pk=int(id))
        with transaction.commit_on_success():
            obj.delete()
            to_url = redirecturl
    else:
        to_url = '/accounts/login/?next=%s' % request.path
    return HttpResponseRedirect(to_url)

# delete object in ajax
@transaction.autocommit
def obj_delete_ajax(request, id, model, perm):
    u""" 
    Удалении данных об объекте в Ajax запросе
    """
    status = 'ERROR'
    if request.user.is_authenticated() and request.user.has_perm(perm):
        obj = get_object_or_404(model, pk=int(id))
        obj.delete()
        status = 'OK'
    else:
        return HttpResponseNotFound('Error delete Key')
    return HttpResponse(status)

# object view
def obj_view(request, id, vtemplate, model):
    u""" 
    Просмотр данных об объекте 
    """
    obj = get_object_or_404(model, pk=int(id))
    return TemplateResponse(request, vtemplate, {'result': obj})

# summary object form
def get_obj_form(request, setobrj, SetForm):
    u"""
    Добавление или обновление данных об объектах, инициализации или сохранение данных формы
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

# none to 0
def NoneTo0(value):
    return value if value else 0

# get keys stats by program
def key_get_stat(prog):
    try:
        keys = Key.objects.filter(program=int(prog))
        clients = Client.objects.filter(key=keys)
        result = {'all': keys.count(), 
            'net': keys.filter(net=True).count(),
            'manyuse': NoneTo0(keys.aggregate(Sum('manyuse'))['manyuse__sum']),
            'use': keys.filter(use=True).count(),
            'clients_all': clients.count(),
            'clients_manyuse': NoneTo0(clients.aggregate(Sum('manyuse'))['manyuse__sum'])
            }
        result['allfree'] = result['all'] - result['use']
        result['free'] = result['manyuse'] - result['clients_manyuse']
    except:
        return False
    return result

# get license list by program ID
def keys_get(request, vtemplate, prog):
    u"""
    Получение списка ключей по номеру программы:

    Авторизованные пользователи получают полный список ключей 
    и данные по статистике хранения и использования ключей; 

    Не авторизованные - только статистику. Аторизация фильтруется в шаблоне (**html**)

    - all - всего лицензий;
    - net - количество сетевых лицензий;
    - namyuse - максимальное количество рабочих станций;
    - clients_all - общее количество пользователей;
    - clients_manyuse - количество рабочих станций, использующих лицензии данной программы;
    - free - количество рабочих мест, на которых еще можно использовать данное ПО
    """
    result = key_get_stat(prog)
    if not result:
        return HttpResponseNotFound('Get keys error')
    return TemplateResponse(request, vtemplate, {'keys': keys, 'result': result, 'prog': prog})

# download key
@login_required
def download_handler(request, id):
    u"""
    Загрузка ключевого файла на носитель авторизованного пользователя
    """
    upload = get_object_or_404(Key, pk=id)
    # get real name
    filename = upload.attach.name.rsplit('/')[-1]
    # get upload name
    filename = filename[LEN_SALT:]
    return serve_file(request, upload.attach, None, filename)
