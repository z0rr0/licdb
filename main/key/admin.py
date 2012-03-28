#-*- coding: utf-8 -*-
from django.contrib import admin
from key.models import License, Program, Key, Client

class LicenseAdmin(admin.ModelAdmin):
	search_fields = ('name',)

class ProgramAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'license')
	search_fields = ('name',)
	list_filter = ('license',)

class KeyAdmin(admin.ModelAdmin):
	list_display = ('id', 'program', 'comment')
	search_fields = ('program__name', 'comment',)
	list_filter = ('use', 'date_start', 'date_end')

class ClientAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'student', 'comment', 'date_start')
	search_fields = ('name', 'comment', )
	list_filter = ('student', 'key__program', 'date_start')

admin.site.register(License, LicenseAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Client, ClientAdmin)