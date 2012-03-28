#-*- coding: utf-8 -*-
from django.contrib import admin
from key.models import License, Program

class LicenseAdmin(admin.ModelAdmin):
	search_fields = ('name',)

class ProgramAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'license')
	# search_fields = ('name', 'license__name')
	search_fields = ('name',)
	list_filter = ('license',)



admin.site.register(License, LicenseAdmin)
admin.site.register(Program, ProgramAdmin)