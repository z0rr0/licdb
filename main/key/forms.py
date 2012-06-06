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

class UserForm(forms.Form):
    first_name = forms.CharField(label=u'Имя', max_length=30)
    last_name = forms.CharField(label=u'Фамилия', max_length=30)
    email = forms.EmailField(label=u'E-mail', help_text=u'Адрес электронной почты')
    password = forms.CharField(label=u'Старый пароль', max_length=127, widget=forms.PasswordInput, help_text=u'Текущий пароль', required=False)
    password1 = forms.CharField(label=u'Новый пароль', max_length=127, min_length=6, widget=forms.PasswordInput, help_text=u'Новый пароль', required=False)
    password2 = forms.CharField(label=u'Подтверждение', max_length=127, min_length=6, widget=forms.PasswordInput, help_text=u'Повтор нового пароля', required=False)

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
    programma = forms.ChoiceField(label=u'Программа', widget=forms.Select(), choices=[])
    onlyfree = forms.BooleanField(label=u'только доступные ключи', widget=forms.CheckboxInput())

class ProgrmaCount(forms.Form):
    u"""
    Список количества ключей
    """
    plist = forms.ChoiceField(label='', widget=forms.Select())
        
