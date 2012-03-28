#-*- coding: utf-8 -*-
from django.db import models

class Student (models.Model):
    u"""
    Студенты
    
    """
    who = models.CharField(max_length = 512, verbose_name = u'имя', help_text = u'даные пользователя, получившего лицензию', null = True, editable = False)

    def __unicode__(self):
        return self.who
