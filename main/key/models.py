#-*- coding: utf-8 -*-
from django.db import models

class Program (models.Model):
    u"""
    Название программы
    
    """
    name = models.CharField(max_length = 100, verbose_name = u'Название программы')
    use_student = models.BooleanField(verbose_name = u'Выдача студентам',)

class License (models.Model):
    u"""
    Лицензии на имеющиеся программы
    
    """
    program = models.ForeignKey(Program, verbose_name = u'Название программы')
    date_start = models.DateField(verbose_name = u'Дата получения лицензии',)
    date_end = models.DateField(null = True, verbose_name = u'Дата окончания лицензии')

class Tip (models.Model):
    u"""
    Тип лицензии
    
    """
    comment = models.TextField(blank = True, verbose_name = u'Комментарий')
    
class Key (models.Model):
    u"""
    Ключи и файлы лицензий
    
    """
    license = models.ForeignKey(License, verbose_name = u'Лицензия')
    key = models.CharField(max_length = 255, blank = True, unique = 'True', verbose_name = u'Ключ')
    use = models.BooleanField(verbose_name = u'Изпользуется',)
    tip = models.ForeignKey(Tip, verbose_name = u'Тип')
    comment = models.CharField(max_length = 500, blank = True, verbose_name = u'Комментарий')
    
class Client (models.Model):
    u"""
    Клиенты получившие лицензию
    
    """
    name = models.CharField(max_length = 300, verbose_name = u'Имя')
    gruppa = models.CharField(max_length = 30, blank = True, verbose_name = u'Группа')
    date_start = models.DateField(verbose_name = u'Дата выдачи',)
    key = models.ForeignKey(Key, verbose_name = u'Выданный ключ')
    comment = models.CharField(max_length = 500, blank = True, verbose_name = u'Комментарий')
    