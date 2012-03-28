#-*- coding: utf-8 -*-
from django.contrib import admin
from eis.models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'who')
    search_fields = ('who',)

admin.site.register(Student, StudentAdmin)
