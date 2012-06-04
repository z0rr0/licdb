#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from key.models import *
from django import forms
# from django.forms.extras.widgets import SelectDateWidget

from django.forms.widgets import ClearableFileInput

class ShortNameClarableFileInput(ClearableFileInput):
    initial_text = u'текущий'
    input_text = u'изменить'
    clear_checkbox_label = u'очистить'
    # template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'
    template_with_clear = u'%(clear)s %(clear_checkbox_label)s'

class ShortNameClarableFileInputHidden(ClearableFileInput):
    initial_text = u'текущий'
    input_text = u'изменить'
    clear_checkbox_label = u'очистить (удалить существующий файл)'
    template_with_initial = u'%(clear_template)s<br />%(input_text)s: %(input)s'
    template_with_clear = u'%(clear)s %(clear_checkbox_label)s'

class LicenseForm(forms.ModelForm):
    # pass
    # fields = ("name1", 'name2',)

    class Meta:
        model = License
        fields = ('name', 'url', 'attach', 'free', 'comment')
        widgets = {
            'attach': ShortNameClarableFileInput,
        }

class UserForm(forms.ModelForm):
    # pass
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

class ProgramForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных о программном обеспечении
    """

    class Meta:
        model = Program
        fields = ('name', 'license', 'url', 'use_student', 'comment')

class KeyForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных о ключе
    """

    class Meta:
        model = Key
        fields = ('program', 'key', 'attach', 'use', 'manyuse', 'net', 'date_start', 'date_end', 'comment')
        widgets = {
            'attach': ShortNameClarableFileInputHidden,
        }

class ProgSelForm(forms.Form):
    u"""
    список для выбора программы
    """
    program = Program.objects.all()
    CHOICES=[(0, '--- все программы ---'),
        (u"Для студенов", [(p.id, p.name) for p in program.filter(use_student=True).only('id', 'name')]),
        (u"Только для ВУЗа", [(p.id, p.name) for p in program.filter(use_student=False).only('id', 'name')]),
    ]
    # forms.Select(attrs={'onchange': 'alert("ok")'})
    programma = forms.ChoiceField(label=u'Программа', widget=forms.Select(), choices=CHOICES)
    onlyfree = forms.BooleanField(label=u'только доступные ключи', widget=forms.CheckboxInput())

class ProgrmaCount(forms.Form):
    u"""
    Список количества ключей
    """
    plist = forms.ChoiceField(label='', widget=forms.Select())
        
