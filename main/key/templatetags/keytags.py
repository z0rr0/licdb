#-*- coding: utf-8 -*-
from django import template
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
register = template.Library()

@register.filter(name='free')
def free(value):
    return 'беспланая' if value else 'коммерческая'