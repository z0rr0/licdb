#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.contrib.auth.views import login, logout
# from django.views.generic import list_detail
from key.models import *

# license_info = {
#     'queryset': License.objects.all(),
#     'template_name': 'license_home.html',
#     }

# license_free = {
#     'queryset': License.objects.filter(free=True),
#     'template_name': 'license_home.html',
#     'extra_context': {'type': '(беспланые)'}
#     }

# license_com = {
#     'queryset': License.objects.filter(free=False),
#     'template_name': 'license_home.html',
#     'extra_context': {'type': '(коммерческие)'}
#     }

urlpatterns = patterns('',
    # accounts
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$' , logout),
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^main/', include('main.foo.urls')),

    # index page
    url(r'^$', 'key.views.index', {'vtemplate': 'index.html'}),
    
    # all license
    url(r'^licenses/$', 'key.views.licenses', {
        'vtemplate': 'license_home.html',
        'typefree': None}),
    # free license
    url(r'^licenses/free/$', 'key.views.licenses', {
        'vtemplate': 'license_home.html',
        'typefree': True}),
    # no free license
    url(r'^licenses/com/$', 'key.views.licenses', {
        'vtemplate': 'license_home.html',
        'typefree': False}),
    # license view
    url(r'^license/(?P<id>\d+)/?$', 'key.views.obj_view', {
        'vtemplate': 'license_view.html',
        'model': License}),
    # license delete
    (r'^license/delete/(?P<id>\d+)/?$', 'key.views.obj_delete', {
        'redirecturl': '/licenses/',
        'model': License}),
    # license edit
    (r'^license/edit/(?P<id>\d+)/?$', 'key.views.license_edit', {
        'vtemplate': 'license_edit.html'}),
    # license edit
    (r'^license/add/?$', 'key.views.license_add', {
        'vtemplate': 'license_edit.html'}),

    # all program
    url(r'^programs/$', 'key.views.programs', {
        'vtemplate': 'program_home.html',
        'stud': None}),
    # student program
    url(r'^programs/stud/$', 'key.views.programs', {
        'vtemplate': 'program_home.html',
        'stud': True}),
    # no studnet program
    url(r'^programs/nostud/$', 'key.views.programs', {
        'vtemplate': 'program_home.html',
        'stud': False}),
    # license delete
    (r'^program/delete/(?P<id>\d+)/?$', 'key.views.obj_delete', {
        'redirecturl': '/programs/',
        'model': Program}),

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
