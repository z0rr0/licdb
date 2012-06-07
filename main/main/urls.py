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
    url('^accounts/settings/$' , 'key.views.user_edit', {'vtemplate': 'user_edit.html'}),
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^main/', include('main.foo.urls')),

    # index page
    url(r'^$', 'key.views.index', {'vtemplate': 'index.html'}),
    
    # all license
    url(r'^licenses/$', 'key.views.licenses', {
        'vtemplate': 'license_home.html' }),
    # license view
    url(r'^license/(?P<id>\d+)/?$', 'key.views.obj_view', {
        'vtemplate': 'license_view.html',
        'model': License}),
    # license delete
    url('^license/delete/(?P<id>\d+)/?$', 'key.views.obj_delete', {
        'redirecturl': '/licenses/',
        'model': License, 
        'perm': 'key.delete_license'}),
    # license edit
    url('^license/edit/(?P<id>\d+)/?$', 'key.views.license_edit', {
        'vtemplate': 'license_edit.html'}),
    # license add
    url('^license/add/?$', 'key.views.license_add', {
        'vtemplate': 'license_edit.html'}),

    # all program
    url(r'^programs/$', 'key.views.programs', {
        'vtemplate': 'program_home.html'}),
    # program delete
    url('^program/delete/(?P<id>\d+)/?$', 'key.views.obj_delete', {
        'redirecturl': '/programs/',
        'model': Program,
        'perm': 'key.delete_program'}),
    # program edit
    url('^program/edit/(?P<id>\d+)/?$', 'key.views.program_edit', {
        'vtemplate': 'program_edit.html'}),
    # program add
    url('^program/add/?$', 'key.views.program_add', {
        'vtemplate': 'program_edit.html'}),
    # program view
    url(r'^program/(?P<id>\d+)/?$', 'key.views.obj_view', {
        'vtemplate': 'program_view.html',
        'model': Program}),

    # get license list by program ID
    url(r'^keys/?$', 'key.views.keys', {
        'vtemplate': 'key_home.html'}),
    # get license list by program ID
    url(r'^get_keys/(?P<prog>\d+)/?$', 'key.views.keys_get', {
        'vtemplate': 'key_get_list.html'}),
    # license delete
    url(r'^key/delete/(?P<id>\d+)/?$', 'key.views.obj_delete_ajax', {
        'model': Key,
        'perm': 'key.delete_key'}),
    # get license list by program ID
    url(r'^key/download/(?P<id>\d+)/?$', 'key.views.download_handler',),
    # get keys list by program ID
    url(r'^keys/program/(?P<prog>\d+)/?$', 'key.views.keys_get', {
        'vtemplate': 'keys_program.html',
        'obj_onpage': 7}),   
    # key edit
    url(r'^key/edit/(?P<id>\d+)/?$', 'key.views.key_edit', {
        'vtemplate': 'key_edit.html'}),
    # license add
    url(r'^key/add/?$', 'key.views.key_add', {
        'vtemplate': 'key_edit.html'}),

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
