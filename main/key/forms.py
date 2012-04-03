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
