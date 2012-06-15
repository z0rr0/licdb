#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.contrib.auth.views import login, logout
from key.models import *

urlpatterns = patterns('',
    # accounts
    url('^accounts/login/$', login),
    url('^accounts/logout/$' , logout),
    (r'^accounts/settings/$' , 'key.views.user_edit', {'vtemplate': 'user_edit.html'}),
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^main/', include('main.foo.urls')),

    # index page
    (r'^$', 'key.views.index', {'vtemplate': 'index.html'}),
    
    # all license
    (r'^licenses/$', 'key.views.licenses', {
        'vtemplate': 'license_home.html' }),
    # license view
    (r'^license/(?P<id>\d+)/?$', 'key.views.obj_view', {
        'vtemplate': 'license_view.html',
        'model': License}),
    # license delete
    (r'^license/delete/(?P<id>\d+)/?$', 'key.views.obj_delete', {
        'redirecturl': '/licenses/',
        'model': License, 
        'perm': 'key.delete_license'}),
    # license edit
    (r'^license/edit/(?P<id>\d+)/?$', 'key.views.license_edit', {
        'vtemplate': 'license_edit.html'}),
    # license add
    (r'^license/add/?$', 'key.views.license_add', {
        'vtemplate': 'license_edit.html'}),

    # all program
    (r'^programs/$', 'key.views.programs', {
        'vtemplate': 'program_home.html'}),
    # program delete
    (r'^program/delete/(?P<id>\d+)/?$', 'key.views.obj_delete', {
        'redirecturl': '/programs/',
        'model': Program,
        'perm': 'key.delete_program'}),
    # program edit
    (r'^program/edit/(?P<id>\d+)/?$', 'key.views.program_edit', {
        'vtemplate': 'program_edit.html'}),
    # program add
    (r'^program/add/?$', 'key.views.program_add', {
        'vtemplate': 'program_edit.html'}),
    # program view
    (r'^program/(?P<id>\d+)/?$', 'key.views.obj_view', {
        'vtemplate': 'program_view.html',
        'model': Program}),

    # get key
    (r'^keys/?$', 'key.views.key_home', {
        'vtemplate': 'key_home.html'}),
    # get key list by program ID
    (r'^key/statistics/(?P<prog>\d+)/?$', 'key.views.key_statistics', {
        'vtemplate': 'key_statistics.html'}),
    # key delete
    (r'^key/del/(?P<id>\d+)/?$', 'key.views.obj_delete_ajax', {
        'model': Key,
        'perm': 'key.delete_key'}),
    # key delete
    (r'^key/delete/(?P<id>\d+)/?$', 'key.views.obj_delete', {
        'redirecturl': '/keys/',
        'model': Key,
        'perm': 'key.delete_key'}),
    # download key
    (r'^key/download/(?P<id>\d+)/?$', 'key.views.download_handler',),
    # get keys list by program ID
    # (r'^keys/program/(?P<prog>\d+)/?$', 'key.views.keys_get', {
    #     'vtemplate': 'keys_program.html',
    #     'obj_onpage': 7}),   
    # key edit
    (r'^key/edit/(?P<id>\d+)/?$', 'key.views.key_edit', {
        'vtemplate': 'key_edit.html'}),
    # key add
    (r'^key/add/?$', 'key.views.key_add', {
        'vtemplate': 'key_edit.html'}),
    # key search
    (r'^key/search/?$', 'key.views.keys_search', {
        'vtemplate': 'key_search.html'}),
    # search in ajax
    (r'^key/search/ajax/?$', 'key.views.keys_search_ajax', {
        'vtemplate': 'key_search_ajax.html'}),
    # key view
    (r'^key/(?P<id>\d+)/?$', 'key.views.obj_view_private', {
        'vtemplate': 'key_view.html',
        'model': Key}),

    # clients
    (r'^clients/?$', 'key.views.keys_search', {
        'vtemplate': 'client_home.html'}),
    # search in ajax
    (r'^client/search/ajax/?$', 'key.views.clients_search_ajax', {
        'vtemplate': 'clients_search_ajax.html'}),
    # client delete
    (r'^client/del/(?P<id>\d+)/?$', 'key.views.obj_delete_client_ajax', {
        'perm': 'key.delete_client'}),
    # key edit
    (r'^client/edit/(?P<id>\d+)/?$', 'key.views.client_edit', {
        'vtemplate': 'client_edit.html',
        'add': False,
        'perm': 'key.edit_client'}),
    # key add
    (r'^client/add/(?P<id>\d+)/?$', 'key.views.client_edit', {
        'vtemplate': 'client_edit.html',
        'add': True,
        'perm': 'key.add_client'}),
    # autocomplete
    (r'^client/complete/?$', 'key.views.client_autocomplete'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# media content                   
# urlpatterns += patterns('',) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^robots.txt$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "robots.txt"}),
        url(r'^favicon.ico$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "favicon.ico"}),
   	)
    # urlpatterns += patterns('django.contrib.staticfiles.views',
    #     url(r'^static/(?P<path>.*)$', 'serve'),
    # )
