#-*- coding: utf-8 -*-
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

class LicenseForm(forms.ModelForm):
    # pass
    # fields = ("name1", 'name2',)

    class Meta:
        model = License
        fields = ('name', 'url', 'attach', 'free', 'comment')
        widgets = {
            'attach': ShortNameClarableFileInput,
        }

class ProgramForm(forms.ModelForm):
    u"""
    Форма для добавления/правки данных о программном обеспечении
    """

    class Meta:
        model = Program
        fields = ('name', 'license', 'url', 'use_student', 'comment')

class ProgSelForm(forms.Form):
    u"""
    список для выбора программы
    """
    program = Program.objects.all()
    CHOICES=[(0, '--- все программы ---'),
        (u"Для студенов", [(p.id, p.name) for p in program.filter(use_student=True).only('id', 'name')]),
        (u"Не для студенов", [(p.id, p.name) for p in program.filter(use_student=False).only('id', 'name')]),
    ]
    # forms.Select(attrs={'onchange': 'alert("ok")'})
    programma = forms.ChoiceField(label='', widget=forms.Select(), choices=CHOICES)
