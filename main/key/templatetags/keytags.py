#-*- coding: utf-8 -*-
from main.settings import LEN_SALT
from django import template
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
register = template.Library()

@register.filter(name='free')
def free(value):
    u""" 
    Тип лицензии: коммерческая или беспланая 
    """
    return u"беспланая" if value else u"коммерческая"

@register.filter(name='errorcss')
def errorcss(value):
    u""" 
    Стиль для поля с ошибкой 
    """
    return " error" if value else ""

@register.filter(name='forstud')
def forstud(value):
    u""" 
    Для студентов программа или нет 
    """
    return u"для студентов" if value else u"не для студентов"

@register.filter(name='keyname')
def keyname(value, arg):
    u""" 
    Фомирование имени для файла ключа
    """
    left_str = len(arg) + LEN_SALT
    return value[left_str:]