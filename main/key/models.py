#-*- coding: utf-8 -*-
from django.db import models

class License (models.Model):
    u"""
    Тип лицензии
    
    """
    name = models.CharField(max_length = 127, verbose_name = u'название')
    attach = models.FileField(verbose_name = u'файл', blank = True, null = True, upload_to = 'license')
    url = models.URLField(max_length = 512, verbose_name = u'сайт', blank = True, null = True, help_text = u'адрес сайта')
    comment = models.TextField(verbose_name = u'комментарий', blank = True, null = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Program (models.Model):
    u"""
    Программное обеспечение
    
    """
    license = models.ForeignKey(License, verbose_name = u'лицензия')
    name = models.CharField(max_length = 255, verbose_name = u'название')
    use_student = models.BooleanField(verbose_name = u'выдача студентам', default = False, help_text=u'можно ли студентам использовать данное ПО')
    url = models.URLField(max_length = 512, verbose_name = u'сайт', blank = True, null = True, help_text = u'адрес сайта программы')
    comment = models.TextField(verbose_name = u'примечание', blank = True, null = True)
    # даты изменения и создания, заполняются автоматически
    modified = models.DateTimeField(auto_now = True, auto_now_add = True, editable = False)
    created = models.DateTimeField(auto_now_add = True, editable = False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
    
class Key (models.Model):
    u"""
    Ключи и файлы лицензий
    
    """
    program = models.ForeignKey(Program, verbose_name = u'программа')
    key = models.CharField(max_length = 255, blank = True, unique = 'True', verbose_name = u'ключ')
    attach = models.FileField(verbose_name = u'файл', blank = True, null = True, upload_to = 'keys')
    use = models.BooleanField(verbose_name = u'используется', default = False)
    date_start = models.DateField(verbose_name = u'начало', help_text = u'дата получения лицензии')
    date_end = models.DateField(verbose_name = u'окончание', blank = True, null = True, help_text = u'Дата окончания лицензии')
    comment = models.TextField(verbose_name = u'комментарий', blank = True, null = True)
    # дата создания
    created = models.DateTimeField(auto_now_add = True, editable = False)

    def __unicode__(self):
        return "%s %s" % (self.program.name, self.key)

    class Meta:
        ordering = ['use', 'program__name', 'key']
    
class Client (models.Model):
    u"""
    Пользователи (люди или отделы), получившие лицензию
    
    """
    name = models.CharField(max_length = 300, verbose_name = u'имя', help_text = u'даные пользователя, получившего лицензию')
    student = models.BooleanField(verbose_name = u'студент', default = False, help_text = u'используется студентом')
    date_start = models.DateField(verbose_name = u'дата выдачи',)
    key = models.ForeignKey(Key, verbose_name = u'ключ')
    comment = models.TextField(verbose_name = u'комментарий', blank = True, null = True)
    # даты изменения и создания, заполняются автоматически
    modified = models.DateTimeField(auto_now = True, auto_now_add = True, editable = False)
    created = models.DateTimeField(auto_now_add = True, editable = False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', 'key__program__name']
    