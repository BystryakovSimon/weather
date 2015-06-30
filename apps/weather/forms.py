# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
import datetime
from models import Town, GeneralHashtag

class CitySelect(forms.Form):
    city = forms.ModelChoiceField(queryset=Town.objects.all())

class GHashtagSelect(forms.Form):
    g_hashtag_selected = forms.ModelChoiceField(queryset=GeneralHashtag.objects.all())

#class SelectFromModel(forms.Field):
#    widget = forms.Select()
#    def __init__(self, objects, *args, **kwargs):
#        self.objects = objects
#        super(SelectFromModel, self).__init__(*args, **kwargs)
#        self.loadChoices()
#    def loadChoices(self):
#        choices = ()
#        for object in self.objects.order_by('id'):
#            choices += ((object.id, object.title),)
#        self.widget.choices = choices
#    def clean(self, value):
#        value = int(value)
#        for cat_id, cat_title in self.widget.choices:
#            if cat_id == value:
#                return self.objects.get(pk=cat_id)
#        raise forms.ValidationError(u'Неверный ввод')

#class CitySelect(forms.Form):
#    citys = SelectFromModel(objects=Town.objects.all())

