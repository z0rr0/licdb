#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.db.models import Q, F, Sum
from django.utils import simplejson
from django.db import transaction
from django.contrib import auth
from django import forms

from filetransfers.api import serve_file

from django.contrib.auth.models import User
from main.settings import LEN_SALT, DEFAULT_FROM_EMAIL
from key.models import *
from eis.models import *
from key.forms import *

# import the logging library
import logging, urllib
# Get an instance of a logger
logger = logging.getLogger(__name__)

AUTOCOMPLETE_LIMIT = 10
PAGE_COUNT = 10
EMAIL_MESSAGE = u"""Здравствуйте.
Ваши личные дынные для license.apingtu.edu.ru были изменены:
  имя: %s
  фамилия: %s
"""

# --------- ADD FUNTIONS -------------
# decorator for ajax login
def login_required_ajax404(fn):
    def wrapper(*args, **kwargs):
        if args[0].user.is_authenticated():
            return fn(*args, **kwargs)
        else:
            return HttpResponseNotFound('Auth error')
    return wrapper

# --------- GENERAL FUNCTIONS -------------
def pagination_oblist(obj_list, page=1, page_count=PAGE_COUNT):
    u"""
    Получение объектов с возможным разбиение на страницы
    """
    if page:
        # постраничный просмотр 
        paginator = Paginator(obj_list, page_count)
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            obj = paginator.page(paginator.num_pages)
    else:
        obj = obj_list
        pagintor = None
    return obj, paginator

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

@login_required_ajax404
@transaction.autocommit
def obj_delete_ajax(request, id, model, perm):
    u""" 
    Удалении данных об объекте в Ajax запросе
    """
    status = 'ERROR'
    if request.user.has_perm(perm):
        obj = get_object_or_404(model, pk=int(id))
        obj.delete()
        status = 'OK'
    else:
        return HttpResponseNotFound('Error delete Key')
    return HttpResponse(status)

def obj_view(request, id, vtemplate, model):
    u""" 
    Просмотр данных об объекте 
    """
    obj = get_object_or_404(model, pk=int(id))
    return TemplateResponse(request, vtemplate, {'result': obj})

@login_required
def obj_view_private(request, id, vtemplate, model):
    u"""Просмотр данных об объекте о защищенном объекте"""
    return obj_view(request, id, vtemplate, model)

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

def divisibleby_obj(objects_list, num):
    u"""
    Разбиение списка объектов на группы
    """
    new_list = []
    for i in range(0, objects_list.count(), num):
        new_list.append(objects_list[i:i+num])
    return new_list

# --------- USER FUNTIONS -------------
@login_required
@transaction.autocommit
def user_edit(request, vtemplate):
    u""" 
    Редактирование данных о пользователе.

    Каждый зарегистированный пользотель может изменить свои данные 
    """
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            user_data = form.cleaned_data
            user = request.user
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            message = EMAIL_MESSAGE % (user.first_name, user.last_name)
            if user_data['password1']:
                if user_data['password1'] == user_data['password2']:
                    if user.check_password(user_data['password']):
                        user.set_password(user_data['password1'])
                        message += u"  новый пароль: " + user_data['password1']
                    else:
                        form.errors['password'] = u'Указан неверный пароль'
                else:
                    form.errors['password1'] = u'Пароли не совпали'
            if not form.errors:
                user.save()
                # email
                subject = u'Изменение личных данных'
                send_mail(subject, message, DEFAULT_FROM_EMAIL, [user.email])
                return redirect('/')
    else:
        form = UserForm(initial={
            'last_name': request.user.last_name,
            'first_name': request.user.first_name,
            'email': request.user.email})
    return TemplateResponse(request, vtemplate, {'form': form })

# --------- MAIN FUNTIONS -------------
def index(request, vtemplate):
    u""" 
    Главная страница, со статистикой по платному ПО
    """
    program = Program.objects.filter(license__free=False).only('name')
    stat = []
    for po in program:
        all_keys = Key.objects.filter(program=po)
        use_keys = all_keys.filter(use=True)
        stat.append({'program': po.name, 
            'all': all_keys.count(), 
            'use': use_keys.count()})
    # logger.info(program)
    return TemplateResponse(request, vtemplate, {'statistics': stat})

# --------- LICENSE FUNTIONS -------------
def licenses(request, vtemplate):
    u""" 
    Список лицензий
    """
    typetext = ''
    object_list = License.objects.all()
    if 'free' in request.GET:
        try:
            typefree = int(request.GET['free'])
            object_list = object_list.filter(free=typefree)
            typetext =  u'беспланые' if typefree else u'коммерческие'
        except ValueError:
            pass
    return TemplateResponse(request, vtemplate, {
        'object_list': divisibleby_obj(object_list, 3), 
        'type': typetext
        })

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

# --------- PROGRAM FUNTIONS -------------
def programs(request, vtemplate):
    u"""
    Прогрограммы, с возможым фильтром по лицензии, использованию студентами и/или названию ПО
    """
    c = {}
    c.update(csrf(request))
    typetext = ''
    searchtext = ''
    lic = None
    object_list = Program.objects.all()
    try:
        if 'stud' in request.GET:
            stud = int(request.GET['stud'])
            object_list = object_list.filter(use_student=stud)
            typetext =  u'для студентов' if stud else u'не для студентов'
        if 'lic' in request.GET:
            lic = License.objects.get(pk=int(request.GET['lic']))
            object_list = object_list.filter(license=lic)
        if request.method == 'POST':
            searchtext = request.POST['progsearch']
            object_list = object_list.filter(name__icontains=searchtext)
    except (IndexError, ValueError, License.DoesNotExist):
        pass
    return TemplateResponse(request, vtemplate, {
        'object_list': object_list,
        'type': typetext,
        'lic': lic,
        'searchtext': searchtext
        })

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

# --------- KEY FUNTIONS -------------
# none to 0
def NoneTo0(value):
    return value if value else 0

def key_map(key):
    u"""
    Сколько клиентов используют ключ и кто они
    """
    client_count = key.client_set.all().only('name', 'student')
    return client_count.count(), [client.name for client in client_count]

def key_get_stat(keys):
    u"""
    Получение статистики по ключам:

    - all - всего лицензий;
    - net - количество сетевых лицензий;
    - namyuse - максимальное количество рабочих станций;
    - clients_all - общее количество пользователей;
    - clients_manyuse - количество рабочих станций, использующих лицензии данной программы;
    - free - количество рабочих мест, на которых еще можно использовать данное ПО
    """
    try:
        clients = Client.objects.filter(key__in=keys)
        result = {'all': keys.count(), 
            'net': keys.filter(net=True).count(),
            'manyuse': NoneTo0(keys.aggregate(Sum('manyuse'))['manyuse__sum']),
            'use': keys.filter(use__gt=0).count(),
            'clients_all': clients.count(),
            'clients_manyuse': NoneTo0(clients.aggregate(Sum('manyuse'))['manyuse__sum'])
            }
        result['allfree'] = result['all'] - result['use']
        result['free'] = result['manyuse'] - result['clients_manyuse']
    except:
        return False
    return result

def paginator_list_page(pages, page, prange):
    u"""
    Уменьшение числа страниц просмотра для более удобного вида

    отображаются page+-prange страниц
    """
    newpages = []
    # есть страницы до диапазона
    if page - prange > 1:
        newpages.append(0)
        start = page - prange - 1
    else:
        start = 0
    # тут можно сделать по-другому
    newpages = newpages + pages[start:page+prange]
    # есть страницы после диапазона
    if page + prange < pages[-1]:
        newpages.append(0)
    return newpages

def paginator_list_page2(pages, page, median=5):
    u"""
    Формирование списка страниц с отбрасыванием слишком дальних от текущей (page)

    отображаются максимально (2*median+1) страниц, в возможным центрированием для ст.-page
    """
    median = int(median)
    median2 = median * 2
    pages_len = len(pages)
    if pages_len <= median2:
        # нужно вывести больше, чем есть страниц
        return pages
    if page - median < 1:
        # левая граница
        return pages[:median2+1]
    elif pages[-1] - page <= median:
        # правая граница
        return pages[pages_len-median2-1:]
    else:
        # общий вид
        return pages[page-median-1:page+median]

@login_required_ajax404
def keys_get(request, vtemplate, prog, obj_onpage=5):
    u"""
    Получение списка ключей по номеру программы:

    Авторизованные пользователи получают полный список ключей 
    и данные по статистике хранения и использования ключей; 
    """
    program = get_object_or_404(Program, pk=int(prog))
    # keys = Key.objects.filter(program=program)
    keys = program.key_set.all()
    try:
        if 'free' in request.GET:
            if int(request.GET['free']):
                alredy_use = not int(request.GET['free'])
                keys = keys.filter(use=alredy_use)
        page = int(request.GET['page']) if 'page' in request.GET else 1
    except ValueError:
        page = 1
    result = key_get_stat(keys)
    if not result:
        return HttpResponseNotFound('Get keys error')
    obj, paginator = pagination_oblist(keys, page, PAGE_COUNT)
    if paginator is None:
        return HttpResponseNotFound('Pagination error')
    # keys = obj.object_list
    return TemplateResponse(request, vtemplate, {
        'keys': obj, 
        'result': result, 
        'num_pages': paginator.num_pages,
        'srart': (obj.number - 1) *  PAGE_COUNT,
        'page_range': paginator_list_page2(paginator.page_range, obj.number, obj_onpage),
        'prog': program
        })

@login_required
def keys_search(request, vtemplate):
    u"""
    Страница поиска ключей или клиентов
    """
    # как статическая страница
    return TemplateResponse(request, vtemplate)

@login_required_ajax404
def keys_search_ajax(request, vtemplate):
    u"""
    Поиск ключей по пользователю или ключу
    """
    keys = Key.objects.all()
    page=1
    form_method = request.POST if request.method == 'POST' else request.GET
    # for GET
    # text_templ = urllib.unquote(request.GET['search'])
    text_templ = form_method['search'] if 'search' in form_method else False
    page = int(form_method['page']) if 'page' in form_method else 1
    if text_templ:
        keys = keys.filter(Q(key__icontains=text_templ) | Q(program__name__icontains=text_templ))
    obj, paginator = pagination_oblist(keys, page, PAGE_COUNT)
    if paginator is None:
        return HttpResponseNotFound('Pagination error')
    for key in obj.object_list:
        key.client_count, key.clients = key_map(key)
        key.clients = '<br />'.join(key.clients)
    return TemplateResponse(request, vtemplate, {
        'keys': obj, 
        'num_pages': paginator.num_pages,
        'obj_count': paginator.count,
        'srart': (obj.number - 1) *  PAGE_COUNT,
        'page_range': paginator_list_page2(paginator.page_range, obj.number),
        'search': text_templ
        })

@login_required
def key_home(request, vtemplate):
    u"""
    Список всех ключей - главная страница
    """
    try:
        prog = int(request.GET['prog']) if 'prog' in request.GET else 0
    except (KeyError, ValueError) as err:
        prog = 0
    form = ProgSelForm(initial={'programma': prog})
    program = Program.objects.all()
    CHOICES=[ 
        #(0, '--- все программы ---'),
        (u"Для студенов", [(p.id, p.name) for p in program.filter(use_student=True).only('id', 'name')]),
        (u"Только для ВУЗа", [(p.id, p.name) for p in program.filter(use_student=False).only('id', 'name')])]
    form.fields['programma'].choices = CHOICES
    return TemplateResponse(request, vtemplate, {'form': form })

@permission_required('key.change_key')
def key_edit(request, id, vtemplate):
    u""" 
    Редактирование данных о ключе 
    """
    c = {}
    c.update(csrf(request))
    key = get_object_or_404(Key, id=int(id))
    form, key, saved = get_obj_form(request, key, KeyForm)
    if saved:
        return redirect('/keys/?prog=' + str(key.program_id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Редактирование'})

@permission_required('key.add_key')
def key_add(request, vtemplate):
    u""" 
    Добавление данных о ключе 
    """
    c = {}
    c.update(csrf(request))
    if 'prog' in request.GET:
        try:
            program = Program.objects.get(pk=int(request.GET['prog']))
            key = Key(program=program)
        except Program.DoesNotExist:
            key = None
    else:
        key = None
    form, key, saved = get_obj_form(request, key, KeyForm)
    if saved:
        return redirect('/keys/?prog=' + str(key.program_id))
    return TemplateResponse(request, vtemplate, {'form': form, 'action': u'Добавление'})

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

# --------- CLIENTS FUNTIONS -------------
@login_required_ajax404
def clients_search_ajax(request, vtemplate):
    u"""Страница со списком пользователей, с возможостями:
             
    - поиск пользователя по его данным или номеру ключа
    - правка данных пользователя
    - удаление пользователя
    """ 
    clients = Client.objects.all()
    page = int(request.GET['page']) if 'page' in request.GET else 1
    search = request.GET['search'] if 'search' in request.GET else ''
    urlsearch = ""
    if search:
        clients = clients.filter(Q(name__icontains=search) | Q(key__key__icontains=search) | Q(key__program__name__icontains=search))
    obj, paginator = pagination_oblist(clients, page, PAGE_COUNT)
    if paginator is None:
        raise HttpResponseNotFound('Pagination error')
    return TemplateResponse(request, vtemplate, {
        'clients': obj, 
        'num_pages': paginator.num_pages,
        'obj_count': paginator.count,
        'srart': (obj.number - 1) *  PAGE_COUNT,
        'page_range': paginator_list_page2(paginator.page_range, obj.number)
        })

@login_required_ajax404
def client_edit(request, vtemplate, id, perm):
    if request.user.has_perm(perm):
        c = {}
        c.update(csrf(request))
        id = int(id)
        if id:
            action = u'Редактирование'
            client = get_object_or_404(Client, pk=id)
        else:
            action = u'Добавление'
            client = None
        form, client, saved = get_obj_form(request, client, ClientForm)
        try:
            page = int(request.GET['page']) if 'page' in request.GET else 1
        except:
            page = 1
        if saved:
            return HttpResponse('saved')
        return TemplateResponse(request, vtemplate, {
            'form': form, 
            'action': action,
            'id': id,
            'page': page
            })
    else:
        return HttpResponseNotFound('Auth perm error')

@login_required_ajax404
def obj_delete_client_ajax(request, id, perm):
    u""" 
    Удалении данных об объекте в Ajax запросе
    """
    status = 'ERROR'
    if request.user.has_perm(perm):
        try:
            with transaction.commit_on_success():
                client = get_object_or_404(Client, pk=int(id))
                key = Key.objects.filter(id=client.key_id).update(use=F('use')-client.manyuse)
                client.delete()
            status = 'OK'
        except:
            status = 'ERROR'
    else:
        return HttpResponseNotFound('Error delete Key')
    return HttpResponse(status)

@login_required_ajax404
def client_autocomplete(request):
    u"""
    автоподстановка данных пользователей: из уже существующих пользователей и студентов
    """
    result = []
    if request.method == 'POST':
        try:
            val = request.POST['val']
            # student
            students = Student.objects.filter(who__contains=val)
            students = list(students.values_list('who', flat=True)[:AUTOCOMPLETE_LIMIT])
            # clients
            clients = Client.objects.filter(name__contains=val)
            clients = list(clients.values_list('name', flat=True)[:AUTOCOMPLETE_LIMIT])
            # result
            result = list(set(clients+students))[:AUTOCOMPLETE_LIMIT]
            result.sort()
        except IndexError:
            pass
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')