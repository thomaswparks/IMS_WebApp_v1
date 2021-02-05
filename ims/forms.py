from django import forms
from django.db.models import fields
from django.forms import ModelForm
from . import models


# this form is to update an end item record
class item_update_form(forms.ModelForm):
    
    class Meta:
        model = models.EndItem
        exclude = ['end_item_account_number',]


# this fomr adds new end items
class new_item_form(ModelForm):
    class Meta:
        model = models.EndItem
        exclude = ('end_item_account_number',)


# this form adds new sub items
class new_sub_item_form(ModelForm):
    class Meta:
        model = models.SubItem
        exclude = ('sub_item_end_item',)


# this form updates sub items
class sub_item_update_form(forms.ModelForm):
    
    class Meta:
        model = models.SubItem
        exclude = ['sub_item_end_item','sub_item_id',]