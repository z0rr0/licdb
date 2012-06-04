#-*- coding: utf-8 -*-
from django.db import models
import string, random
from main.settings import LEN_SALT, KEYS_DIRS, LICENSE_DIRS

class License (models.Model):
    u"""
    Типы лицензий на программное обеспечение
    
    """
    name = models.CharField(max_length = 127, verbose_name = u'название', unique = True, help_text = u'название лицензии')
    attach = models.FileField(verbose_name = u'файл', blank = True, null = True, upload_to = LICENSE_DIRS)
    free = models.BooleanField(verbose_name = u'бесплатная', default = False, help_text = u'указывается для бесплатного ПО')
    url = models.URLField(max_length = 512, verbose_name = u'сайт', blank = True, null = True, help_text = u'адрес сайта')
    comment = models.TextField(verbose_name = u'комментарий', blank = True, null = True)
    # даты изменения и создания, заполняются автоматически
    modified = models.DateTimeField(auto_now = True, auto_now_add = True, editable = False, help_text = u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add = True, editable = False, help_text = u'дата создания объекта')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Program (models.Model):
    u"""
    Программное обеспечение: прикладные и иструментальные программы, операционные системы и т.д.
    
    """
    license = models.ForeignKey(License, verbose_name = u'лицензия', blank=True, null=True, on_delete=models.SET_NULL, help_text=u'лицензия программы')
    name = models.CharField(max_length = 255, verbose_name = u'название', unique = True, help_text=u'название программы')
    use_student = models.BooleanField(verbose_name = u'выдача студентам', default = False, help_text=u'можно ли студентам использовать данное ПО')
    url = models.URLField(max_length = 512, verbose_name = u'сайт', blank = True, null = True, help_text = u'адрес сайта программы')
    comment = models.TextField(verbose_name = u'примечание', blank = True, null = True)
    # даты изменения и создания, заполняются автоматически
    modified = models.DateTimeField(auto_now = True, auto_now_add = True, editable = False, help_text = u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add = True, editable = False, help_text = u'дата создания объекта')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
    
class Key (models.Model):
    u"""
    Ключи и файлы лицензий для программого обеспечения
    
    """
    def gen_filename(instance, filename):
        def gen_salt(size=LEN_SALT - 1):
            # chars = string.ascii_lowercase + string.digits * 2
            chars = string.ascii_letters + string.digits * 5
            return ''.join(random.choice(chars) for x in range(size))
        # new name
        return KEYS_DIRS + '/' + gen_salt() + "_" + filename

    program = models.ForeignKey(Program, verbose_name = u'программа')
    key = models.CharField(max_length = 255, blank = True, null= True, verbose_name = u'ключ', help_text = u'ключ / серийной номер продукта')
    attach = models.FileField(verbose_name = u'файл', blank = True, null = True, upload_to = gen_filename)
    use = models.BooleanField(verbose_name = u'используется', default = False, help_text = u'ключ уже используется')
    manyuse = models.PositiveSmallIntegerField(verbose_name = u'количество', default = 1, help_text = u'количество использований (раб.станций), 0 - если нет ограничений')
    net = models.BooleanField(verbose_name = u'сетевой', default = False, help_text = u'ключ предназначен для сетевого использования')
    date_start = models.DateField(verbose_name = u'начало', help_text = u'дата получения лицензии')
    date_end = models.DateField(verbose_name = u'окончание', blank = True, null = True, help_text = u'дата окончания лицензии')
    comment = models.TextField(verbose_name = u'комментарий', blank = True, null = True)
    # даты изменения и создания, заполняются автоматически
    modified = models.DateTimeField(auto_now = True, auto_now_add = True, editable = False, help_text = u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add = True, editable = False, help_text = u'дата создания объекта')

    def __unicode__(self):
        return u"ключ для \"%s\" %s" % (self.program.name, self.key)

    class Meta:
        ordering = ['use', 'program__name', 'id']
    
class Client (models.Model):
    u"""
    Пользователи (люди или отделы), получившие или использующие лицензию/ключ
    
    """
    key = models.ForeignKey(Key, verbose_name = u'ключ')
    name = models.CharField(max_length = 512, verbose_name = u'имя', help_text = u'даные пользователя, получившего лицензию')
    student = models.BooleanField(verbose_name = u'студент', default = False, help_text = u'используется студентом')
    manyuse = models.PositiveSmallIntegerField(verbose_name = u'количество мест', default = 1, help_text = u'количество рабочих мест')
    date_start = models.DateField(verbose_name = u'дата выдачи',)
    comment = models.TextField(verbose_name = u'комментарий', blank = True, null = True)
    # даты изменения и создания, заполняются автоматически
    modified = models.DateTimeField(auto_now = True, auto_now_add = True, editable = False, help_text = u'дата редактирования объекта')
    created = models.DateTimeField(auto_now_add = True, editable = False, help_text = u'дата создания объекта')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['student', 'name', 'key__program__name']
